"""Chỉ dẫn xuất bảng/hình từ dữ liệu đã khóa; không fit/tuning hoặc thay kết quả."""
from pathlib import Path
from io import BytesIO
import sys,os,json,hashlib,platform,argparse
from importlib.metadata import version
os.environ.setdefault('MPLCONFIGDIR','tmp/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.datasets import load_digits
from threadpoolctl import threadpool_info,threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
import optimize_external as experiment
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory',type=Path,required=True)
out=parser.parse_args().directory.resolve()
assert out.is_relative_to((ROOT/'outputs').resolve())
assert (out/'final_test/complete.json').is_file(), 'Chỉ vẽ lại sau đánh giá đã khóa.'
folder=out/'analysis';folder.mkdir(exist_ok=True)
figures=folder/'figures';figures.mkdir(exist_ok=True)
validation=pd.read_csv(out/'validation/metrics.csv')
special=pd.read_csv(out/'specialist/validation_metrics.csv')
all_val=pd.concat([validation,special],ignore_index=True)
all_val.to_csv(folder/'validation_all.csv',index=False)
for name in ['mnist_validation','handwriting_validation']:
    view=all_val[all_val.dataset.eq(name)&all_val.source.eq('all')].copy()
    view[['model','variant']]=view.system.str.split('--',expand=True)
    for metric in ['accuracy','f1_macro']:
        view.pivot(index='variant',columns='model',values=metric).to_csv(folder/f'{name}_{metric}.csv')
final=pd.read_csv(out/'final_test/metrics_with_cost.csv')
comparisons=[]
for row in final.itertuples():
    model=row.system.split('--')[0]
    base_model=model if model!='mlp_mnist' else 'knn'
    baseline=final[final.dataset.eq(row.dataset)&final.source.eq(row.source)&final.system.eq(base_model+'--baseline')].iloc[0]
    comparisons.append({'dataset':row.dataset,'source':row.source,'system':row.system,'reference':baseline.system,
                        'accuracy':row.accuracy,'f1_macro':row.f1_macro,
                        'accuracy_change_pp':100*(row.accuracy-baseline.accuracy),
                        'f1_change_pp':100*(row.f1_macro-baseline.f1_macro)})
pd.DataFrame(comparisons).to_csv(folder/'final_comparisons.csv',index=False)
final[final.dataset.eq('handwriting_test')].pivot(index='system',columns='source',values='accuracy').to_csv(folder/'accuracy_by_source.csv')
final[final.dataset.eq('handwriting_test')].pivot(index='system',columns='source',values='f1_macro').to_csv(folder/'f1_by_source.csv')
descriptors=[]
def add_descriptors(group,images,labels):
    images=np.asarray(images,dtype=float)
    for i,(image,label) in enumerate(zip(images,labels)):
        side=image.shape[0]; ys,xs=np.indices(image.shape); mask=image>=.2*image.max(); y,x=np.where(mask)
        descriptors.append({'dataset':group,'row':i,'label':int(label),'mean_pixel_0_16':float(image.mean()),
            'peak':float(image.max()),'zero_fraction':float((image==0).mean()),'foreground_fraction':float(mask.mean()),
            'bbox_width':float((x.max()-x.min()+1)/side),'bbox_height':float((y.max()-y.min()+1)/side),
            'aspect':float((x.max()-x.min()+1)/(y.max()-y.min()+1)),
            'centroid_x':float(((xs+.5)*image).sum()/image.sum()/side),
            'centroid_y':float(((ys+.5)*image).sum()/image.sum()/side)})
digits=load_digits()
split=pd.read_csv(ROOT/'outputs/20261117T081201Z_fd32180f/split_indices.csv')
ids=split.loc[split.split.eq('train'),'sample_index'].to_numpy()
add_descriptors('digits_train',digits.images[ids],digits.target[ids])
for dataset_name in ['mnist_validation','handwriting_validation']:
    records,buffers=experiment.dataset(out,dataset_name)
    for variant in experiment.VARIANTS:
        X=np.load(out/f'arrays/{dataset_name}_{variant}.npz')['X']
        add_descriptors(dataset_name+'--'+variant,X.reshape(-1,8,8),records.true_label)
    X=np.load(out/f'arrays/{dataset_name}_mnist28.npz')['X']
    add_descriptors(dataset_name+'--mnist28',X.reshape(-1,28,28)*16/255,records.true_label)
descriptor_frame=pd.DataFrame(descriptors)
descriptor_frame.to_csv(folder/'validation_image_descriptors.csv',index=False)
metrics=list(descriptor_frame.columns[3:])
descriptor_frame.groupby('dataset')[metrics].agg(['mean','std']).to_csv(folder/'validation_distribution.csv')
descriptor_frame.groupby(['dataset','label'])[metrics].mean().to_csv(folder/'validation_distribution_by_digit.csv')
records,_=experiment.dataset(out,'handwriting_validation')
images_by_row=[digits.images[ids][digits.target[ids]==d].mean(0) for d in range(10)]
fig,axes=plt.subplots(4,10,figsize=(16,8),layout='constrained')
names=['Digits train','Ngoài · cũ','Ngoài · gray_bbox','Ngoài · MNIST28']
for digit in range(10):
    arrays=[images_by_row[digit]]
    for variant,side,scale in [('baseline',8,1),('gray_bbox',8,1),('mnist28',28,16/255)]:
        X=np.load(out/f'arrays/handwriting_validation_{variant}.npz')['X']
        arrays.append(X[records.true_label.eq(digit)].reshape(-1,side,side).mean(0)*scale)
    for row,array in enumerate(arrays):
        axes[row,digit].imshow(array,cmap='gray',vmin=0,vmax=16,interpolation='nearest')
        axes[row,digit].set(title=str(digit),xticks=[],yticks=[])
        if digit==0:axes[row,digit].set_ylabel(names[row])
fig.suptitle('Chỉ dùng train/validation — ảnh trung bình và vị trí nét, cùng đơn vị 0–16')
fig.savefig(figures/'validation_class_means.png',dpi=160,bbox_inches='tight');plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(14,4),layout='constrained')
groups=['digits_train','handwriting_validation--baseline','handwriting_validation--gray_bbox','handwriting_validation--mnist28']
for ax,metric in zip(axes,['mean_pixel_0_16','aspect','centroid_y']):
    edges=np.histogram_bin_edges(descriptor_frame[descriptor_frame.dataset.isin(groups)][metric],bins=20)
    for group in groups:
        values=descriptor_frame.loc[descriptor_frame.dataset.eq(group),metric]
        ax.hist(values,bins=edges,density=True,alpha=.4,label=group)
    ax.set(xlabel=metric,ylabel='Mật độ');ax.legend(fontsize=7)
fig.suptitle('Phân phối train/validation; mask vùng nét ≥20% đỉnh, chỉ mô tả')
fig.savefig(figures/'validation_distributions.png',dpi=160,bbox_inches='tight');plt.close(fig)
metadata=json.loads((out/'specialist/metadata.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
axes[0].plot(range(1,len(metadata['loss_curve'])+1),metadata['loss_curve']);axes[0].set(title='MLP MNIST — loss train',xlabel='Iteration',ylabel='Loss')
axes[1].plot(range(1,len(metadata['validation_scores'])+1),metadata['validation_scores']);axes[1].set(title='Early stopping nội bộ',xlabel='Iteration',ylabel='Accuracy validation nội bộ')
fig.savefig(figures/'mlp_mnist_training.png',dpi=160,bbox_inches='tight');plt.close(fig)
for dataset_name in ['mnist_test','handwriting_test']:
    records,buffers=experiment.dataset(out,dataset_name)
    baseline=pd.read_csv(out/f'final_test/{dataset_name}__knn--baseline__predictions.csv')
    positions=baseline[~baseline.correct].sort_values('sample_id').index[:8].tolist()
    variants=['baseline','gray_bbox','mnist28']
    systems=['knn--baseline','knn--gray_bbox','mlp_mnist--mnist28']
    arrays=[np.load(out/f'arrays/{dataset_name}_{v}.npz')['X'] for v in variants]
    predicted=[pd.read_csv(out/f'final_test/{dataset_name}__{s}__predictions.csv') for s in systems]
    fig,axes=plt.subplots(len(positions),4,figsize=(11,2.1*len(positions)),layout='constrained',squeeze=False)
    for row,position in enumerate(positions):
        image=Image.open(BytesIO(buffers[position]))
        axes[row,0].imshow(image,cmap='gray');axes[row,0].set_title(f'{records.iloc[position].sample_id}\nThật {records.iloc[position].true_label}',fontsize=8)
        for col,(X,table,side,maximum) in enumerate(zip(arrays,predicted,[8,8,28],[16,16,255]),start=1):
            axes[row,col].imshow(X[position].reshape(side,side),cmap='gray',vmin=0,vmax=maximum,interpolation='nearest')
            axes[row,col].set_title(f'{systems[col-1]}\nDự đoán {table.iloc[position].predicted_label}',fontsize=8)
        for ax in axes[row]:ax.set(xticks=[],yticks=[])
    fig.suptitle('8 ID lỗi KNN cũ đầu theo thứ tự ID — không chọn theo mức cải thiện')
    fig.savefig(figures/f'{dataset_name}_errors_before_after.png',dpi=150,bbox_inches='tight');plt.close(fig)
    systems=json.loads((out/'selection_lock.json').read_text())['evaluation_systems']
    fig,axes=plt.subplots(3,3,figsize=(18,17),layout='constrained')
    for ax in axes.flat:ax.set_visible(False)
    for ax,item in zip(axes.flat,systems):
        ax.set_visible(True)
        cm=pd.read_csv(out/f'final_test/{dataset_name}__{item["system"]}__all__confusion.csv',index_col=0)
        values=cm.to_numpy()
        heat=ax.imshow(values,cmap='Blues')
        for y in range(values.shape[0]):
            for x in range(values.shape[1]):
                ax.text(x,y,str(values[y,x]),ha='center',va='center',fontsize=7,
                        color='white' if values[y,x]>values.max()/2 else 'black')
        row=final[final.dataset.eq(dataset_name)&final.source.eq('all')&final.system.eq(item['system'])].iloc[0]
        ax.set(title=f'{item["system"]}\nAccuracy {row.accuracy:.2%} | Macro F1 {row.f1_macro:.4f}',
               xlabel='Dự đoán',ylabel='Nhãn thật',xticks=range(values.shape[1]),yticks=range(10))
        fig.colorbar(heat,ax=ax,shrink=.75,label='Số ảnh')
    fig.suptitle(dataset_name+' — cùng tập test sau khóa, không tuning lại')
    fig.savefig(figures/f'{dataset_name}_confusion_annotated.png',dpi=140,bbox_inches='tight');plt.close(fig)
with threadpool_limits(limits=2):
    environment={'python':sys.version,'platform':platform.platform(),'packages':{p:version(p) for p in ['numpy','pandas','scikit-learn','pillow','matplotlib','joblib','streamlit','threadpoolctl']},'numerical_threads':2,'threadpools':threadpool_info()}
(out/'environment.json').write_text(json.dumps(environment,ensure_ascii=False,indent=2),encoding='utf-8')
print('Summary tables, validation descriptors and 7 figures saved; no model fit')
