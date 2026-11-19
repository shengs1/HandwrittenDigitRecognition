"""Thực nghiệm ảnh ngoài tách khỏi notebook/Digits: validation, train, lock, test, verify.

Không dùng test để chọn phương pháp. Đọc protocol.json trước khi chạy; mỗi action
từ chối ghi đè kết quả. Collector và prepare_data tạo danh sách trước các action này.
"""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import gzip
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from time import perf_counter
from unittest.mock import patch
import warnings

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'tmp/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from threadpoolctl import threadpool_limits
import app
from external_preprocessing import VARIANTS, preprocess_external_image


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                          default=lambda value: value.item() if isinstance(value,np.generic) else value.tolist()), encoding='utf-8')


def now():
    return datetime.now(timezone.utc).isoformat()


def check_locks(out):
    protocol = json.loads((out/'protocol.json').read_text(encoding='utf-8'))
    assert sha(out/'protocol.json') == (out/'protocol.sha256').read_text().strip()
    assert sha(out/'mnist_train_split.csv') == protocol['mnist_train_split_sha256']
    assert sha(out/'mnist_test_eligibility.csv') == protocol['mnist_test_eligibility_sha256']
    lock = json.loads((ROOT/'data/external_handwriting/sample_lock.json').read_text())
    assert sha(ROOT/'data/external_handwriting/manifest.csv') == lock['manifest_sha256']
    return protocol


def read_mnist(out, part):
    prefix = 'train' if part=='train' else 't10k'
    source = out/'mnist_source'
    raw = gzip.decompress((source/f'{prefix}-images-idx3-ubyte.gz').read_bytes())
    target = gzip.decompress((source/f'{prefix}-labels-idx1-ubyte.gz').read_bytes())
    count = 60000 if part=='train' else 10000
    return np.frombuffer(raw[16:],np.uint8).reshape(count,28,28), np.frombuffer(target[8:],np.uint8)


def dataset(out, name):
    if name.startswith('mnist'):
        final = name=='mnist_test'
        images, labels = read_mnist(out,'test' if final else 'train')
        if final:
            split = pd.read_csv(out/'mnist_test_eligibility.csv')
            ids = split.loc[split.eligible_final_test,'mnist_test_id'].to_numpy()
        else:
            split = pd.read_csv(out/'mnist_train_split.csv')
            ids = split.loc[split.split==('train' if name=='mnist_train' else 'validation'),'mnist_train_id'].to_numpy()
        buffers = []
        for index in ids:
            buffer = BytesIO()
            Image.fromarray(images[index]).save(buffer,format='PNG')
            buffers.append(buffer.getvalue())
        return pd.DataFrame({'sample_id':ids.astype(str),'true_label':labels[ids],'source':'mnist'}), buffers
    frame = pd.read_csv(ROOT/'data/external_handwriting/manifest.csv')
    frame = frame.loc[frame.split==('test' if name=='handwriting_test' else 'validation')].copy()
    assert len(frame)==300
    for item in frame.itertuples():
        assert sha(ROOT/'data/external_handwriting'/item.path)==item.sha256
    return frame.rename(columns={'path':'sample_id','label':'true_label'})[['sample_id','true_label','source']], [
        (ROOT/'data/external_handwriting'/path).read_bytes() for path in frame.path]


def features(out, name, buffers, variant):
    cache = out/'arrays'
    cache.mkdir(exist_ok=True)
    path = cache/f'{name}_{variant}.npz'
    if path.exists():
        stored = np.load(path,allow_pickle=False)
        return stored['X']
    side = 28 if variant=='mnist28' else 8
    dtype = np.float32 if side==28 else np.float64
    values, rejected = [], []
    started = perf_counter()
    for index, data in enumerate(buffers):
        try:
            pixels = preprocess_external_image(data,variant=variant)[1]
            assert pixels.shape==(side,side) and np.isfinite(pixels).all()
            values.append(pixels.reshape(-1).astype(dtype))
        except ValueError as exc:
            values.append(np.full(side*side,np.nan,dtype))
            rejected.append({'row_index':index,'reason':str(exc)})
    array = np.stack(values)
    np.savez_compressed(path,X=array)
    write_json(cache/f'{name}_{variant}.json',{'seconds':perf_counter()-started,'n':len(buffers),
               'shape':list(array.shape),'dtype':str(array.dtype),'rejections':rejected,'preprocessing_module_sha256':sha(ROOT/'external_preprocessing.py')})
    print('features',name,variant,len(buffers),'rejected',len(rejected),flush=True)
    return array


def frozen_pipelines():
    registry = app.read_model_registry()
    result = {}
    for name, entry in registry['models'].items():
        path = ROOT/'models'/entry['path']
        stat = path.stat()
        result[name] = app.load_saved_pipeline(str(path),entry['sha256'],stat.st_mtime_ns,stat.st_size)
    return result


def score(folder, data_name, system, pipeline, X, records):
    valid = np.isfinite(X).all(axis=1)
    prediction = np.full(len(X),-1,int)
    probabilities = np.full((len(X),10),np.nan)
    names = getattr(pipeline,'feature_names_in_',None)
    if names is None:
        names = getattr(pipeline.steps[-1][1],'feature_names_in_',None)
    inputs = pd.DataFrame(X[valid],columns=names) if names is not None else X[valid]
    with patch.object(Pipeline,'fit',side_effect=AssertionError('Evaluation must not fit')),threadpool_limits(limits=2):
        start = perf_counter()
        if valid.any():
            prediction[valid] = pipeline.predict(inputs)
            probabilities[valid] = pipeline.predict_proba(inputs)
        seconds = perf_counter()-start
    assert np.array_equal(pipeline.classes_,np.arange(10))
    assert not valid.any() or np.allclose(probabilities[valid].sum(axis=1),1)
    frame = records.copy().reset_index(drop=True)
    frame['predicted_label'] = prediction
    frame['correct'] = frame.true_label.to_numpy()==prediction
    frame['rejected'] = ~valid
    for digit in range(10):
        frame[f'probability_{digit}'] = probabilities[:,digit]
    prefix = f'{data_name}__{system}'
    frame.to_csv(folder/f'{prefix}__predictions.csv',index=False)
    rows = []
    groups = [('all',frame)] if data_name.startswith('mnist') else [('all',frame), *list(frame.groupby('source'))]
    for source, group in groups:
        report = classification_report(group.true_label,group.predicted_label,labels=np.arange(10),output_dict=True,zero_division=0)
        labels = np.r_[np.arange(10),-1] if group.rejected.any() else np.arange(10)
        cm = confusion_matrix(group.true_label,group.predicted_label,labels=labels)[:10]
        columns = list(map(str,labels))
        if columns[-1]=='-1':
            columns[-1]='rejected'
        pd.DataFrame(cm,index=range(10),columns=columns).to_csv(folder/f'{prefix}__{source}__confusion.csv',index_label='true_label')
        pd.DataFrame([{'digit':d,**report[str(d)]} for d in range(10)]).to_csv(folder/f'{prefix}__{source}__per_digit.csv',index=False)
        write_json(folder/f'{prefix}__{source}__report.json',report)
        rows.append({'dataset':data_name,'source':source,'system':system,'n':len(group),'rejected':int(group.rejected.sum()),
                     'accuracy':accuracy_score(group.true_label,group.predicted_label),
                     'f1_macro':f1_score(group.true_label,group.predicted_label,labels=np.arange(10),average='macro',zero_division=0),
                     'precision_macro':report['macro avg']['precision'],'recall_macro':report['macro avg']['recall'],
                     'predict_and_proba_seconds':seconds if source=='all' else np.nan})
    frame.loc[frame.correct].to_csv(folder/f'{prefix}__correct.csv',index=False)
    frame.loc[~frame.correct].to_csv(folder/f'{prefix}__incorrect.csv',index=False)
    return rows


def validation(out):
    protocol = check_locks(out)
    folder = out/'validation'
    folder.mkdir(exist_ok=False)
    write_json(folder/'start.json',{'at_utc':now(),'protocol_sha256':sha(out/'protocol.json'),
              'external_manifest_sha256':sha(ROOT/'data/external_handwriting/manifest.csv'),
              'external_preprocessing_sha256':sha(ROOT/'external_preprocessing.py')})
    pipelines = frozen_pipelines()
    rows = []
    for name in ['mnist_validation','handwriting_validation']:
        records,buffers = dataset(out,name)
        for variant in protocol['variants']:
            X = features(out,name,buffers,variant)
            for model,pipeline in pipelines.items():
                rows.extend(score(folder,name,f'{model}--{variant}',pipeline,X,records))
            pd.DataFrame(rows).to_csv(folder/'metrics.csv',index=False)
            print(name,variant,pd.DataFrame(rows).tail(3)[['source','system','accuracy','f1_macro']].to_dict('records'),flush=True)


def train(out):
    protocol = check_locks(out)
    metrics = pd.read_csv(out/'validation/metrics.csv')
    native = metrics.loc[(metrics.dataset=='mnist_validation') & (metrics.source=='all')].copy()
    native['variant'] = native.system.str.split('--').str[-1]
    trigger = native.groupby('variant').accuracy.mean().max()<.9
    if not trigger:
        write_json(out/'specialist_skipped.json',{'reason':'8x8 mean native-validation accuracy >=0.90 per protocol'})
        return
    folder = out/'specialist'
    folder.mkdir(exist_ok=False)
    train_records,train_buffers = dataset(out,'mnist_train')
    X = features(out,'mnist_train',train_buffers,'mnist28')
    assert np.isfinite(X).all(), 'Không âm thầm bỏ ảnh MNIST train'
    pipeline = Pipeline([('scale',MinMaxScaler()),('clf',MLPClassifier(**{
        **protocol['mnist_mlp'],'hidden_layer_sizes':tuple(protocol['mnist_mlp']['hidden_layer_sizes']), 'verbose':True}))])
    started = perf_counter()
    with warnings.catch_warnings(record=True) as captured,threadpool_limits(limits=2):
        warnings.simplefilter('always')
        pipeline.fit(X,train_records.true_label.to_numpy())
    fit_seconds = perf_counter()-started
    pipeline.named_steps['clf'].verbose=False
    model_path = folder/'mlp_mnist.joblib'
    joblib.dump(pipeline,model_path,compress=3)
    classifier = pipeline.named_steps['clf']
    write_json(folder/'metadata.json',{'training_dataset':'MNIST train only','train_n':len(X),'outer_validation_n':protocol['validation_n'],
              'input_shape':[None,784],'image_shape':[28,28],'pixel_range':[0,255], 'preprocessing':'mnist28',
              'parameters':protocol['mnist_mlp'],'fit_seconds':fit_seconds,'bytes':model_path.stat().st_size,
              'sha256':sha(model_path),'n_iter':int(classifier.n_iter_),'loss_curve':classifier.loss_curve_,
              'validation_scores':classifier.validation_scores_,'warnings':[str(w.message) for w in captured],
              'seed':42,'augmentation':False,'training_split_sha256':sha(out/'mnist_train_split.csv'),
              'outer_validation_used_in_fit':False,'internal_validation_scaler_caveat':'MinMaxScaler saw all outer train before MLP internal early-stopping split.'})
    rows=[]
    for name in ['mnist_validation','handwriting_validation']:
        records,buffers = dataset(out,name)
        values = features(out,name,buffers,'mnist28')
        rows.extend(score(folder,name,'mlp_mnist--mnist28',pipeline,values,records))
    pd.DataFrame(rows).to_csv(folder/'validation_metrics.csv',index=False)
    print('Specialist validation',pd.DataFrame(rows).to_string(index=False),flush=True)


def lock(out):
    protocol = check_locks(out)
    assert not (out/'selection_lock.json').exists()
    metrics = pd.read_csv(out/'validation/metrics.csv')
    external = metrics.loc[(metrics.dataset=='handwriting_validation') & (metrics.source=='all')].copy()
    external[['model','variant']] = external.system.str.split('--',expand=True)
    ranked = external.groupby('variant').agg(mean_f1=('f1_macro','mean'),mean_accuracy=('accuracy','mean')).reset_index()
    ranked['complexity_order'] = ranked.variant.map({name:i for i,name in enumerate(VARIANTS)})
    ranked = ranked.sort_values(['mean_f1','mean_accuracy','complexity_order'],ascending=[False,False,True])
    winner = ranked.iloc[0]
    old_mean = ranked.set_index('variant').loc['baseline','mean_f1']
    per_knn = external.loc[external.model=='knn'].set_index('variant').f1_macro
    use_new = winner.mean_f1-old_mean>=.02 and per_knn[winner.variant]>=per_knn['baseline']
    chosen = winner.variant if use_new else 'baseline'
    ranked.to_csv(out/'validation/preprocessing_ranking.csv',index=False)
    systems=[{'system':f'{name}--baseline','model':name,'variant':'baseline'} for name in app.read_model_registry()['models']]
    if use_new:
        systems += [{'system':f'{name}--{chosen}','model':name,'variant':chosen} for name in app.read_model_registry()['models']]
    integrate_specialist=False
    if (out/'specialist/validation_metrics.csv').exists():
        specialist = pd.read_csv(out/'specialist/validation_metrics.csv')
        native = specialist.loc[(specialist.dataset=='mnist_validation') & (specialist.source=='all')].iloc[0]
        outside = specialist.loc[(specialist.dataset=='handwriting_validation') & (specialist.source=='all')].iloc[0]
        best_existing = external.loc[external.variant.isin(['baseline',chosen]),'f1_macro'].max()
        integrate_specialist = bool(native.accuracy>=.9 and outside.f1_macro>=best_existing+.02)
        systems += [{'system':'mlp_mnist--mnist28','model':'mlp_mnist','variant':'mnist28','sha256':sha(out/'specialist/mlp_mnist.joblib')}]
    result={'locked_at_utc':now(),'protocol_sha256':sha(out/'protocol.json'),'validation_metrics_sha256':sha(out/'validation/metrics.csv'),
            'external_manifest_sha256':sha(ROOT/'data/external_handwriting/manifest.csv'),
            'preprocessing_module_sha256':sha(ROOT/'external_preprocessing.py'),
            'shared_variant':chosen,'best_validation_variant':winner.variant,'shared_upload_update':bool(use_new),
            'specialist_upload_option':integrate_specialist,'evaluation_systems':systems,
            'test_used_to_choose':False,'official_digits_selected_model':'knn'}
    write_json(out/'selection_lock.json',result)
    (out/'selection_lock.sha256').write_text(sha(out/'selection_lock.json'))
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)


def final_test(out):
    check_locks(out)
    selection=json.loads((out/'selection_lock.json').read_text(encoding='utf-8'))
    assert sha(out/'selection_lock.json')==(out/'selection_lock.sha256').read_text().strip()
    assert selection['preprocessing_module_sha256']==sha(ROOT/'external_preprocessing.py')
    folder=out/'final_test';folder.mkdir(exist_ok=False)
    write_json(folder/'start.json',{'started_at_utc':now(),'selection_lock_sha256':sha(out/'selection_lock.json')})
    pipelines=frozen_pipelines()
    if any(s['model']=='mlp_mnist' for s in selection['evaluation_systems']):
        path=out/'specialist/mlp_mnist.joblib'
        pipelines['mlp_mnist']=joblib.load(path)
    rows=[]
    for data_name in ['mnist_test','handwriting_test']:
        records,buffers=dataset(out,data_name)
        for system in selection['evaluation_systems']:
            X=features(out,data_name,buffers,system['variant'])
            new_rows=score(folder,data_name,system['system'],pipelines[system['model']],X,records)
            rows.extend(new_rows)
            pd.DataFrame(rows).to_csv(folder/'metrics.csv',index=False)
            print('FINAL',data_name,system['system'],new_rows[0]['accuracy'],new_rows[0]['f1_macro'],flush=True)
    metrics=pd.DataFrame(rows)
    costs=[]
    for item in selection['evaluation_systems']:
        if item['model']=='mlp_mnist':
            path=out/'specialist/mlp_mnist.joblib'
        else:
            path=ROOT/'models'/app.read_model_registry()['models'][item['model']]['path']
        costs.append({'system':item['system'],'model_bytes':path.stat().st_size,'model_sha256':sha(path)})
    metrics.merge(pd.DataFrame(costs),on='system').to_csv(folder/'metrics_with_cost.csv',index=False)
    for data_name in ['mnist_test','handwriting_test']:
        systems=selection['evaluation_systems']
        fig,axes=plt.subplots((len(systems)+2)//3,3,figsize=(16,5*((len(systems)+2)//3)),layout='constrained',squeeze=False)
        for ax in axes.flat:
            ax.set_visible(False)
        for ax,item in zip(axes.flat,systems):
            ax.set_visible(True)
            cm=pd.read_csv(folder/f'{data_name}__{item["system"]}__all__confusion.csv',index_col=0)
            ax.imshow(cm.to_numpy(),cmap='Blues')
            ax.set(title=item['system'],xlabel='Dự đoán',ylabel='Nhãn thật',xticks=range(cm.shape[1]),yticks=range(10))
            ax.set_xticklabels(cm.columns,rotation=45)
        fig.suptitle(data_name+' — đánh giá sau khóa, không dùng chọn lại')
        fig.savefig(folder/f'{data_name}__confusions.png',dpi=140,bbox_inches='tight');plt.close(fig)
    write_json(folder/'complete.json',{'completed_at_utc':now(),'selection_lock_sha256':sha(out/'selection_lock.json'),'no_tuning_after_test':True})


def verify(out, verification_output=None):
    check_locks(out)
    selection=json.loads((out/'selection_lock.json').read_text())
    assert sha(out/'selection_lock.json')==(out/'selection_lock.sha256').read_text().strip()
    before=json.loads((out/'protected_before.json').read_text())
    after={name:sha(ROOT/name) for name in before}
    # Final Review cho phép cập nhật đúng 4 tài liệu này; không phải artifact thực nghiệm.
    editable_docs={'docs/RESULTS_INDEX.md','docs/REPORT_OUTLINE.md','docs/SLIDE_OUTLINE.md','docs/VIVA_QUESTIONS.md'}
    documentation_changes=[name for name in before if before[name]!=after[name] and name in editable_docs]
    assert all(before[name]==after[name] for name in before if name not in editable_docs)
    destination=Path(verification_output).resolve() if verification_output else out
    assert destination.is_relative_to((ROOT/'outputs').resolve())
    destination.mkdir(parents=True,exist_ok=True)
    write_json(destination/'protected_after.json',after)
    data=ROOT/'data/external_handwriting'
    manifest=pd.read_csv(data/'manifest.csv')
    assert len(manifest)==600 and manifest.groupby(['split','source','label']).size().eq(10).all()
    assert manifest.pixel_sha256.nunique()==600
    assert all(sha(data/row.path)==row.sha256 for row in manifest.itertuples())
    metrics=pd.read_csv(out/'final_test/metrics.csv')
    checked=0
    for row in metrics.itertuples():
        frame=pd.read_csv(out/f'final_test/{row.dataset}__{row.system}__predictions.csv')
        if row.source!='all':frame=frame.loc[frame.source==row.source]
        assert len(frame)==row.n
        assert np.isclose(accuracy_score(frame.true_label,frame.predicted_label),row.accuracy)
        assert np.isclose(f1_score(frame.true_label,frame.predicted_label,labels=np.arange(10),average='macro'),row.f1_macro)
        cm=pd.read_csv(out/f'final_test/{row.dataset}__{row.system}__{row.source}__confusion.csv',index_col=0)
        np.testing.assert_array_equal(cm.to_numpy(),confusion_matrix(frame.true_label,frame.predicted_label,labels=np.arange(10)))
        prefix=out/f'final_test/{row.dataset}__{row.system}__{row.source}'
        report=json.loads(Path(str(prefix)+'__report.json').read_text())
        recomputed=classification_report(frame.true_label,frame.predicted_label,labels=np.arange(10),output_dict=True,zero_division=0)
        for label in [*map(str,range(10)),'macro avg','weighted avg']:
            for key in ['precision','recall','f1-score','support']:
                assert np.isclose(report[label][key],recomputed[label][key])
        for correct,suffix in [(True,'correct'),(False,'incorrect')]:
            saved=pd.read_csv(out/f'final_test/{row.dataset}__{row.system}__{suffix}.csv',dtype={'sample_id':str})
            if row.source!='all':saved=saved[saved.source.eq(row.source)]
            assert set(saved.sample_id)==set(frame.loc[frame.correct.eq(correct),'sample_id'].astype(str))
        checked+=1
    # Replay qua API app thật, không fit hoặc thay đổi lựa chọn đã khóa.
    active=app.read_external_registry()
    active_run=bool(active and active['optimization_run']==out.name)
    config=active if active_run else {
        'shared_variant':selection['shared_variant'] if selection['shared_upload_update'] else 'baseline',
        'specialist_enabled':selection['specialist_upload_option']}
    records,buffers=dataset(out,'handwriting_test')
    original=json.loads((ROOT/'models/registry.json').read_text())
    replayed=0
    with threadpool_limits(limits=2),patch.object(Pipeline,'fit',side_effect=AssertionError('No fit in verify')):
        names=[*original['models']]+(['mlp_mnist'] if config['specialist_enabled'] else [])
        for name in names:
            if name=='mlp_mnist':
                path=ROOT/'models'/active['specialist']['path'] if active_run else out/'specialist/mlp_mnist.joblib'
                expected=next(item['sha256'] for item in selection['evaluation_systems'] if item['model']==name)
            else:
                entry=original['models'][name];path=ROOT/'models'/entry['path'];expected=entry['sha256']
            assert sha(path)==expected
            model=joblib.load(path)
            variant='mnist28' if name=='mlp_mnist' else config['shared_variant']
            X=np.load(out/f'arrays/handwriting_test_{variant}.npz')['X']
            saved=pd.read_csv(out/f'final_test/handwriting_test__{name}--{variant}__predictions.csv')
            assert saved.sample_id.tolist()==records.sample_id.tolist()
            for i,data_bytes in enumerate(buffers):
                pixels=app.preprocess_upload_for_model(data_bytes,'Tự động',name,config)[1]
                np.testing.assert_array_equal(pixels.reshape(-1),X[i])
                label,probabilities=app.predict_digit(model,pixels)
                assert label==saved.iloc[i].predicted_label
                np.testing.assert_allclose(probabilities['Xác suất'].to_numpy(),saved.iloc[i][[f'probability_{d}' for d in range(10)]].to_numpy(dtype=float),atol=1e-6,rtol=1e-5)
                replayed+=1
    import ast
    old_tree=ast.parse((out/'stable_source/app.py').read_text(encoding='utf-8'))
    new_tree=ast.parse((ROOT/'app.py').read_text(encoding='utf-8'))
    old_function=next(node for node in old_tree.body if isinstance(node,ast.FunctionDef) and node.name=='preprocess_uploaded_image')
    new_function=next(node for node in new_tree.body if isinstance(node,ast.FunctionDef) and node.name=='preprocess_uploaded_image')
    assert ast.dump(old_function)==ast.dump(new_function)
    old_style=next(node.value.value for node in old_tree.body if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='UI_STYLE' for target in node.targets))
    assert old_style==app.UI_STYLE
    assert json.loads((out/'final_test/start.json').read_text())['started_at_utc']>selection['locked_at_utc']
    write_json(destination/'verification.json',{'at_utc':now(),'protected_files_unchanged':len(after)-len(documentation_changes),'external_images_unchanged':600,
               'authorized_documentation_changes':documentation_changes,
               'external_split_counts_correct':True,'metrics_rows_recomputed':checked,'official_digits_model':'knn',
               'app_test_predictions_replayed':replayed,'frozen_css_unchanged':True,'original_preprocessing_ast_unchanged':True,
               'active_app_registry_matches_run':active_run,
               'per_class_reports_and_error_lists_verified':True,
               'test_started_after_lock':json.loads((out/'final_test/start.json').read_text())['started_at_utc']>selection['locked_at_utc']})
    print('VERIFIED',checked,'metric rows;',len(after)-len(documentation_changes),'unchanged protected files;',len(documentation_changes),'authorized docs;',replayed,'app predictions; frozen CSS and baseline AST',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['validation','train','lock','test','verify'])
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--verification-output',type=Path,help='Chỉ với verify: ghi bằng chứng mới ở outputs/, giữ nguyên run đã khóa.')
    args=parser.parse_args()
    out=args.directory.resolve()
    assert out.is_relative_to((ROOT/'outputs').resolve())
    if args.verification_output and args.action!='verify':parser.error('--verification-output chỉ dùng với verify')
    if args.action=='verify':verify(out,args.verification_output)
    else:{'validation':validation,'train':train,'lock':lock,'test':final_test}[args.action](out)
