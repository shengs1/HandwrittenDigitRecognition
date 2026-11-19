from pathlib import Path
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen
import gzip, hashlib, json, shutil, struct, sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedGroupKFold
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from external_preprocessing import VARIANTS
parser=argparse.ArgumentParser(description='Khóa dữ liệu/protocol MNIST trước tối ưu; không fit model.')
parser.add_argument('--directory',type=Path,required=True)
args=parser.parse_args()
out=args.directory.resolve()
assert out.is_relative_to((ROOT/'outputs').resolve())
assert not out.exists(), 'Dùng thư mục mới; không ghi đè experiment cũ.'
out.mkdir(parents=True)
import subprocess
paths=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))-{''}
old_run=ROOT/'outputs/external_evaluation_20261118T165317Z_7e5a90dc'
paths.update(p.relative_to(ROOT).as_posix() for p in old_run.rglob('*') if p.is_file())
editable={'app.py','README.md','AGENTS.md','HANDOFF.md'}
(out/'protected_before.json').write_text(json.dumps({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths-editable)},indent=2))
(out/'stable_source').mkdir()
for name in editable:shutil.copyfile(ROOT/name,out/'stable_source'/name)
source=out/'mnist_source';source.mkdir(exist_ok=True)
files={'train-images-idx3-ubyte.gz':'f68b3c2dcbeaaa9fbdd348bbdeb94873','train-labels-idx1-ubyte.gz':'d53e105ee54ea40749a09fcbcd1e9432','t10k-images-idx3-ubyte.gz':'9fb629c4189551a2d022fa330f9573f3','t10k-labels-idx1-ubyte.gz':'ec29112dd5afa0611ce80d1b7f02629c'}
metadata={}
for name,expected in files.items():
    cached=ROOT/'tmp/mnist'/name
    if cached.exists():blob=cached.read_bytes()
    else:
        with urlopen('https://storage.googleapis.com/cvdf-datasets/mnist/'+name,timeout=45) as response:blob=response.read()
        cached.parent.mkdir(parents=True,exist_ok=True);cached.write_bytes(blob)
    assert hashlib.md5(blob).hexdigest()==expected
    (source/name).write_bytes(blob)
    metadata[name]={'md5':expected,'sha256':hashlib.sha256(blob).hexdigest(),'url':'https://storage.googleapis.com/cvdf-datasets/mnist/'+name}
raw=gzip.decompress((source/'train-images-idx3-ubyte.gz').read_bytes());target=gzip.decompress((source/'train-labels-idx1-ubyte.gz').read_bytes())
assert struct.unpack('>IIII',raw[:16])==(2051,60000,28,28)
assert struct.unpack('>II',target[:8])==(2049,60000)
images=np.frombuffer(raw[16:],np.uint8).reshape(60000,28,28);labels=np.frombuffer(target[8:],np.uint8)
hashes=np.array([hashlib.sha256(image.tobytes()).hexdigest() for image in images])
ids=np.arange(60000)
train_ids,val_ids=train_test_split(ids,test_size=.1,stratify=labels,random_state=42)
overlap=set(hashes[train_ids])&set(hashes[val_ids]);group_fallback=False
if overlap:
    train_ids,val_ids=next(StratifiedGroupKFold(10,shuffle=True,random_state=42).split(ids,labels,hashes));group_fallback=True
assert not set(hashes[train_ids])&set(hashes[val_ids])
pd.DataFrame({'mnist_train_id':ids,'split':np.where(np.isin(ids,val_ids),'validation','train'),'pixel_sha256':hashes}).to_csv(out/'mnist_train_split.csv',index=False)
old10=json.loads((ROOT/'tests/fixtures/external_digits/manifest.json').read_text())
old100=json.loads((ROOT/'outputs/external_evaluation_20261118T165317Z_7e5a90dc/sample_lock.json').read_text())
old_ids={x['mnist_test_index'] for x in old10['images']}|{x['mnist_test_index'] for x in old100['samples']}
assert len(old_ids)==110
raw_test=gzip.decompress((source/'t10k-images-idx3-ubyte.gz').read_bytes());test_images=np.frombuffer(raw_test[16:],np.uint8).reshape(10000,28,28)
test_hashes=[hashlib.sha256(image.tobytes()).hexdigest() for image in test_images]
seen_hashes={test_hashes[i] for i in old_ids}
train_hash_set=set(hashes.tolist())
eligible=[i for i in range(10000) if i not in old_ids and test_hashes[i] not in seen_hashes and test_hashes[i] not in train_hash_set]
eligible_set=set(eligible)
pd.DataFrame({'mnist_test_id':range(10000),'eligible_final_test':[i in eligible_set for i in range(10000)],'previously_seen':[i in old_ids for i in range(10000)],'pixel_sha256':test_hashes}).to_csv(out/'mnist_test_eligibility.csv',index=False)
protocol={'locked_at_utc':datetime.now(timezone.utc).isoformat(),'seed':42,'variants':VARIANTS,
 'variant_definitions':{'baseline':'Exact original app preprocessing','gray_bbox':'32x32 canvas width24/height32, grayscale normalized contrast, bbox center, 4x4 gray sums','gray_com':'As gray_bbox, mass center with clipping guard','binary35':'gray_com then threshold0.35, 4x4 on-pixel counts','binary50':'Threshold0.50','binary35_thick':'Threshold0.35 then one 3x3 MaxFilter, 4x4 counts','gray_wide':'gray_com width28/height32'},
 'selection':'Shared 8x8 preprocessing: maximize mean external-validation macro F1 across the 3 fixed Digits pipelines; tie by mean accuracy then earlier variant order. Keep baseline unless mean F1 increases >=0.02 and KNN F1 does not decrease. Report MNIST6000 separately, never pool datasets.',
 'mnist_specialist_trigger':'If best mean MNIST validation accuracy among 8x8 variants is <0.90, fit exactly one MLP784 (128,64); no augmentation. Outer train/validation source IDs disjoint.',
 'mnist_mlp':{'hidden_layer_sizes':[128,64],'activation':'relu','solver':'adam','alpha':.0001,'early_stopping':True,'n_iter_no_change':8,'max_iter':60,'batch_size':256,'random_state':42},
 'mnist_preprocessing':'Same new function variant=mnist28 on train/validation/external: grayscale+background, crop, peak normalize, fit20x20, 28 canvas, clipped mass center. MinMaxScaler fitted only outer train inside Pipeline.',
 'integration':'8x8 upload update only if shared rule passes. Add explicit upload-only MLP MNIST choice only if MNIST validation accuracy>=0.90 and external-validation macro F1 exceeds the best old/best shared-8 model by>=0.02. No automatic probability-based switch. Test never used to decide.',
 'train_n':len(train_ids),'validation_n':len(val_ids),'group_split_fallback':group_fallback,'raw_train_val_duplicate_overlap':0,
 'excluded_mnist_test_ids':sorted(old_ids),'remaining_mnist_test_n':len(eligible),
 'external_data':'data/external_handwriting/manifest.csv:300 validation+300 test; no external images used to train MNIST specialist',
 'archives':metadata,'mnist_train_split_sha256':hashlib.sha256((out/'mnist_train_split.csv').read_bytes()).hexdigest(),
 'mnist_test_eligibility_sha256':hashlib.sha256((out/'mnist_test_eligibility.csv').read_bytes()).hexdigest(),
 'prohibited':'No tuning on Digits test, old110 MNIST test, remaining MNIST test, or external300 test; no overwriting official artifacts; no push main before review.'}
(out/'protocol.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'protocol.sha256').write_text(hashlib.sha256((out/'protocol.json').read_bytes()).hexdigest())
print(json.dumps({k:protocol[k] for k in ['train_n','validation_n','group_split_fallback','remaining_mnist_test_n','locked_at_utc']},ensure_ascii=False))
