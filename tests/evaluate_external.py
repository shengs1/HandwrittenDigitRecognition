"""Đánh giá MNIST ngoài Digits, chỉ suy luận; prepare khóa mẫu trước run, verify đọc lại.

Chạy từ gốc repo bằng Python trong requirements. Không import TensorFlow/torchvision,
không thay UI, Pipeline, preprocessing hoặc artifact cũ. Xem README trong run kết quả.
"""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import gzip
import hashlib
from io import BytesIO
from importlib.metadata import version
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
from urllib.request import urlopen
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline
import app

SEED = 42
BASE_URL = 'https://storage.googleapis.com/cvdf-datasets/mnist/'
# Digest công bố trong torchvision/datasets/mnist.py; SHA256 còn đối chiếu manifest cũ.
ARCHIVES = {'t10k-images-idx3-ubyte.gz': '9fb629c4189551a2d022fa330f9573f3',
            't10k-labels-idx1-ubyte.gz': 'ec29112dd5afa0611ce80d1b7f02629c'}
LABELS = np.arange(10)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')


def read_idx(directory):
    old = json.loads((ROOT / 'tests/fixtures/external_digits/manifest.json').read_text(encoding='utf-8'))
    payloads = {}
    for name, expected_md5 in ARCHIVES.items():
        blob = (directory / 'source' / name).read_bytes()
        assert hashlib.md5(blob).hexdigest() == expected_md5, f'MD5 không khớp: {name}'
        assert hashlib.sha256(blob).hexdigest() == old['download_sha256'][name]
        payloads[name] = gzip.decompress(blob)
    raw, target = payloads.values()
    assert struct.unpack('>IIII', raw[:16]) == (2051, 10000, 28, 28)
    assert struct.unpack('>II', target[:8]) == (2049, 10000)
    assert len(raw) == 16 + 10000*28*28 and len(target) == 8 + 10000
    images = np.frombuffer(raw[16:], dtype=np.uint8).reshape(10000, 28, 28)
    labels = np.frombuffer(target[8:], dtype=np.uint8)
    assert set(labels) == set(range(10))
    return images, labels, old


def select_ids(images, labels, old):
    """Không gọi preprocessing/model; pool tăng dần ID, loại trùng nội dung rồi lấy ngẫu nhiên."""
    old_ids = {item['mnist_test_index'] for item in old['images']}
    old_hashes = {hashlib.sha256(images[index].tobytes()).hexdigest() for index in old_ids}
    rng = np.random.default_rng(SEED)
    chosen, pool_sizes = [], {}
    seen = set(old_hashes)
    for label in range(10):
        pool = []
        for index in np.flatnonzero(labels == label):
            digest = hashlib.sha256(images[index].tobytes()).hexdigest()
            if int(index) not in old_ids and digest not in seen:
                pool.append(int(index))
                seen.add(digest)  # Trong pool giữ ID đầu tiên của mỗi ảnh byte-identical.
        pool_sizes[str(label)] = len(pool)
        chosen.extend(sorted(int(index) for index in rng.choice(pool, 10, replace=False)))
    assert len(chosen) == len(set(chosen)) == 100 and not set(chosen) & old_ids
    assert np.array_equal(np.bincount(labels[chosen], minlength=10), np.full(10, 10))
    assert not {hashlib.sha256(images[i].tobytes()).hexdigest() for i in chosen} & old_hashes
    return chosen, pool_sizes


def verify_protected(directory):
    before = json.loads((directory / 'protected_before.json').read_text(encoding='utf-8'))
    after = {name: sha(ROOT / name) for name in before}
    assert before == after, 'Một file được bảo vệ đã thay đổi'
    return after


def prepare():
    directory = ROOT / 'outputs' / ('external_evaluation_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8])
    directory.mkdir(exist_ok=False)
    for name in ['source', 'originals']:
        (directory / name).mkdir()
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    # HANDOFF là file duy nhất đã có được phép cập nhật sau phép đánh giá này.
    protected = {name: sha(ROOT / name) for name in tracked if name and name != 'HANDOFF.md'}
    write_json(directory / 'protected_before.json', protected)
    downloads = {}
    try:
        for name, expected in ARCHIVES.items():
            with urlopen(BASE_URL + name, timeout=45) as response:
                blob = response.read()
                downloads[name] = {'url': response.url, 'http_status': response.status,
                                   'downloaded_at_utc': now(), 'bytes': len(blob),
                                   'md5': hashlib.md5(blob).hexdigest(), 'sha256': hashlib.sha256(blob).hexdigest()}
            assert hashlib.md5(blob).hexdigest() == expected
            (directory / 'source' / name).write_bytes(blob)
        images, labels, old = read_idx(directory)
        for item in old['images']:
            original = np.asarray(Image.open(ROOT / 'tests/fixtures/external_digits' / item['filename']))
            np.testing.assert_array_equal(original, images[item['mnist_test_index']])
            assert int(labels[item['mnist_test_index']]) == item['label']
        chosen, pool_sizes = select_ids(images, labels, old)
        records = []
        for order, index in enumerate(chosen):
            label = int(labels[index])
            name = f'mnist_test_{index:05d}_label_{label}.png'
            path = directory / 'originals' / name
            Image.fromarray(images[index]).save(path)
            records.append({'sample_order': order, 'mnist_test_index': index, 'true_label': label,
                            'original_file': 'originals/' + name, 'original_png_sha256': sha(path),
                            'raw_pixels_sha256': hashlib.sha256(images[index].tobytes()).hexdigest()})
        pd.DataFrame(records).to_csv(directory / 'sample_ids.csv', index=False)
        lock = {'locked_at_utc': now(), 'inference_started': False, 'sample_seed': SEED,
                'rng': 'numpy.random.default_rng / PCG64', 'numpy_version': version('numpy'),
                'selection_rule': 'Labels 0..9; ascending-ID pool; exclude old IDs and old/duplicate raw pixel hashes; choose 10 per label without replacement; sort within label.',
                'excluded_old_ids': sorted(item['mnist_test_index'] for item in old['images']),
                'old_manifest_sha256': sha(ROOT / 'tests/fixtures/external_digits/manifest.json'),
                'eligible_pool_sizes': pool_sizes, 'sample_ids_csv_sha256': sha(directory / 'sample_ids.csv'),
                'samples': records, 'source_downloads': downloads,
                'app_sha256': sha(ROOT / 'app.py'),
                'registry_sha256': sha(ROOT / 'models/registry.json'),
                'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
                'error_example_rule': 'First 8 misclassified IDs in ascending MNIST test index, separately per model.',
                'diagnostics_only': 'Image descriptors use a 20%-of-image-maximum mask; no diagnostic transform enters predictions.',
                'prohibited': ['fit', 'tuning', 'model reselection', 'preprocessing change', 'sample replacement after predictions']}
        write_json(directory / 'sample_lock.json', lock)
        (directory / 'sample_lock.sha256').write_text(sha(directory / 'sample_lock.json') + '\n', encoding='ascii')
        write_json(directory / 'source_provenance.json', {
            'authors': ['Yann LeCun', 'Corinna Cortes', 'Christopher J. C. Burges'],
            'dataset': 'MNIST official test split, original IDX 0-based indices',
            'mirror_page': 'https://github.com/cvdfoundation/mnist',
            'original_homepage': 'http://yann.lecun.com/exdb/mnist/',
            'checksum_reference': 'https://github.com/pytorch/vision/blob/main/torchvision/datasets/mnist.py',
            'documentation': 'https://www.tensorflow.org/api_docs/python/tf/keras/datasets/mnist/load_data',
            'license_as_documented_by_tensorflow': 'CC BY-SA 3.0',
            'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/',
            'modifications': 'Subset extraction as lossless PNG; derived 8x8 copies from unchanged app preprocessing.',
            'downloads': downloads})
    except Exception as exc:
        write_json(directory / 'BLOCKER.json', {'at_utc': now(), 'error': str(exc), 'inference_performed': False})
        raise
    print('SAMPLE_LOCKED', directory.relative_to(ROOT).as_posix())
    print('Sample lock SHA256:', sha(directory / 'sample_lock.json'))
    return directory


def image_descriptors(image):
    """Chỉ mô tả, không trả về đầu vào thay thế cho model. image ở miền 0..16."""
    image = np.asarray(image, dtype=float)
    height, width = image.shape
    ys, xs = np.indices(image.shape)
    mask = image >= 0.2 * image.max()
    y, x = np.where(mask)
    mass = image.sum()
    edge = np.zeros_like(mask)
    edge[[0, -1], :] = True
    edge[:, [0, -1]] = True
    return {'mean_pixel': float(image.mean()), 'peak_pixel': float(image.max()),
            'zero_fraction': float((image == 0).mean()), 'foreground_fraction_20pct': float(mask.mean()),
            'centroid_x': float(((xs + 0.5) * image).sum() / mass / width),
            'centroid_y': float(((ys + 0.5) * image).sum() / mass / height),
            'ink_width_fraction': float((x.max()-x.min()+1)/width),
            'ink_height_fraction': float((y.max()-y.min()+1)/height),
            'bbox_aspect_ratio': float((x.max()-x.min()+1)/(y.max()-y.min()+1)),
            'edge_mass_fraction': float(image[edge].sum()/mass)}


def save_figure(fig, path):
    fig.savefig(path, dpi=160, bbox_inches='tight')
    plt.close(fig)


def run(directory):
    lock = json.loads((directory / 'sample_lock.json').read_text(encoding='utf-8'))
    lock_sha = (directory / 'sample_lock.sha256').read_text().strip()
    assert sha(directory / 'sample_lock.json') == lock_sha
    assert sha(directory / 'sample_ids.csv') == lock['sample_ids_csv_sha256']
    verify_protected(directory)
    images, labels, old = read_idx(directory)
    chosen, pool_sizes = select_ids(images, labels, old)
    assert chosen == [item['mnist_test_index'] for item in lock['samples']]
    assert pool_sizes == lock['eligible_pool_sizes']
    results = directory / 'results'
    results.mkdir(exist_ok=False)  # Không ghi đè một đánh giá đã chạy.
    (directory / 'processed').mkdir(exist_ok=False)
    figures = directory / 'figures'
    figures.mkdir(exist_ok=False)
    write_json(results / 'inference_start.json', {'started_at_utc': now(), 'sample_lock_sha256': lock_sha,
               'app_sha256': sha(ROOT / 'app.py'), 'evaluation_script_sha256': sha(__file__)})
    registry = app.read_model_registry()
    assert registry['run_id'] == '20261117T081201Z_fd32180f'
    pixels, diagnostics, rows, descriptors = [], [], [], []
    with ExitStack() as guards:
        guards.enter_context(patch.object(Pipeline, 'fit', side_effect=AssertionError('Inference only')))
        pipelines = {}
        for name, entry in registry['models'].items():
            path = ROOT / 'models' / entry['path']
            stat = path.stat()
            pipelines[name] = app.load_saved_pipeline(str(path), entry['sha256'], stat.st_mtime_ns, stat.st_size)
            for _, step in pipelines[name].steps:
                if not isinstance(step, str):
                    guards.enter_context(patch.object(type(step), 'fit', side_effect=AssertionError('No estimator/scaler fit')))
        for item in lock['samples']:
            path = directory / item['original_file']
            assert sha(path) == item['original_png_sha256']
            original_array = np.asarray(Image.open(path))
            np.testing.assert_array_equal(original_array, images[item['mnist_test_index']])
            data = path.read_bytes()
            original, processed, info = app.preprocess_uploaded_image(data, 'Tự động')
            # Đo kiểm bất biến bằng chính API ứng dụng, không đưa phiên bản đảo màu vào model.
            repeat = app.preprocess_uploaded_image(data, 'Tự động')[1]
            inverse = BytesIO()
            ImageOps.invert(original).save(inverse, format='PNG')
            inverse_pixels = app.preprocess_uploaded_image(inverse.getvalue(), 'Tự động')[1]
            assert processed.shape == (8, 8) and processed.dtype == np.float64
            assert np.isfinite(processed).all() and processed.min() >= 0 and processed.max() <= 16
            assert np.count_nonzero(processed) >= 3
            assert np.array_equal(processed, repeat), 'Preprocessing không deterministic'
            assert np.array_equal(processed, inverse_pixels), 'Đảo nền làm đổi input'
            pixels.append(processed)
            processed_file = 'processed/' + path.name
            Image.fromarray(np.rint(processed*255/16).astype(np.uint8)).save(directory / processed_file)
            diagnostics.append({**item, **info, 'processed_file': processed_file, 'processed_png_sha256': sha(directory / processed_file),
                                'repeat_equal': True, 'polarity_inversion_equal': True})
            for group, array in [('mnist_raw_28', original_array*16.0/255), ('mnist_app_8', processed)]:
                descriptors.append({'dataset': group, 'sample_id': item['mnist_test_index'],
                                    'true_label': item['true_label'], **image_descriptors(array)})
            for name, pipeline in pipelines.items():
                prediction, table = app.predict_digit(pipeline, processed)
                rows.append({'model': name, **item, 'processed_file': processed_file,
                             'predicted_label': prediction, 'correct': prediction == item['true_label'],
                             'probability_predicted': float(table.loc[str(prediction), 'Xác suất']),
                             **{f'probability_{label}': float(table.loc[str(label), 'Xác suất']) for label in LABELS}})
    pixel_array = np.stack(pixels)
    np.save(directory / 'processed_pixels.npy', pixel_array, allow_pickle=False)
    write_json(results / 'preprocessing_diagnostics.json', diagnostics)
    predictions = pd.DataFrame(rows)
    predictions.to_csv(results / 'predictions.csv', index=False)
    summaries = []
    fig, axes = plt.subplots(1, 3, figsize=(17, 5), layout='constrained')
    for ax, (name, group) in zip(axes, predictions.groupby('model', sort=False)):
        truth, predicted = group.true_label, group.predicted_label
        report = classification_report(truth, predicted, labels=LABELS, output_dict=True, zero_division=0)
        per_digit = pd.DataFrame([{'digit': label, **report[str(label)]} for label in range(10)])
        per_digit.to_csv(results / f'per_digit_{name}.csv', index=False)
        write_json(results / f'classification_report_{name}.json', report)
        cm = confusion_matrix(truth, predicted, labels=LABELS)
        pd.DataFrame(cm, index=LABELS, columns=LABELS).to_csv(results / f'confusion_matrix_{name}.csv', index_label='true_label')
        group.loc[group.correct].to_csv(results / f'correct_{name}.csv', index=False)
        group.loc[~group.correct].to_csv(results / f'incorrect_{name}.csv', index=False)
        summaries.append({'model': name, 'n_images': len(group), 'correct': int(group.correct.sum()),
                          'accuracy': accuracy_score(truth, predicted), 'f1_macro': f1_score(truth, predicted, labels=LABELS, average='macro'),
                          'precision_macro': report['macro avg']['precision'], 'recall_macro': report['macro avg']['recall']})
        display = ax.imshow(cm, cmap='Blues', vmin=0, vmax=10)
        for y in range(10):
            for x in range(10):
                ax.text(x, y, str(cm[y, x]), ha='center', va='center', fontsize=9, color='white' if cm[y, x] > 5 else 'black')
        ax.set(title=app.MODEL_SHORT_NAMES[name], xlabel='Nhãn dự đoán', ylabel='Nhãn thật', xticks=LABELS, yticks=LABELS)
        fig.colorbar(display, ax=ax, label='Số ảnh (10 ảnh thật mỗi lớp)', shrink=0.8)
        mistakes = group.loc[~group.correct].sort_values('mnist_test_index').head(8)
        chosen_errors = mistakes[['mnist_test_index', 'true_label', 'predicted_label', 'probability_predicted']]
        chosen_errors.to_csv(results / f'error_examples_{name}.csv', index=False)
        if len(mistakes):
            error_fig, error_axes = plt.subplots(len(mistakes), 2, figsize=(7, 2.2*len(mistakes)), layout='constrained', squeeze=False)
            for pair, item in zip(error_axes, mistakes.itertuples()):
                array = pixel_array[item.sample_order]
                pair[0].imshow(images[item.mnist_test_index], cmap='gray', vmin=0, vmax=255, interpolation='nearest')
                pair[0].set_title(f'MNIST id={item.mnist_test_index} · thật {item.true_label}')
                pair[1].imshow(array, cmap='gray', vmin=0, vmax=16, interpolation='nearest')
                pair[1].set_title(f'8×8 · dự đoán {item.predicted_label} · p={item.probability_predicted:.1%}')
                for a in pair:
                    a.set(xlabel='Cột pixel', ylabel='Hàng pixel')
            error_fig.suptitle(app.MODEL_SHORT_NAMES[name] + ' — 8 lỗi đầu theo ID tăng dần (không chọn lại mẫu đánh giá)')
            save_figure(error_fig, figures / f'errors_{name}.png')
    fig.suptitle('MNIST test mới — 100 ảnh đã khóa, 10 ảnh mỗi chữ số; Pipeline giữ nguyên')
    save_figure(fig, figures / 'confusion_matrices.png')
    summary = pd.DataFrame(summaries)
    summary.to_csv(results / 'external_metrics.csv', index=False)
    canonical = ROOT / 'outputs' / registry['run_id']
    official = pd.read_csv(canonical / 'model_comparison.csv')[['model', 'accuracy', 'f1_macro']]
    comparison = official.merge(summary[['model', 'accuracy', 'f1_macro']], on='model', suffixes=('_digits_test', '_mnist100'), validate='one_to_one')
    comparison['accuracy_change_percentage_points'] = 100*(comparison.accuracy_mnist100-comparison.accuracy_digits_test)
    comparison['f1_change_percentage_points'] = 100*(comparison.f1_macro_mnist100-comparison.f1_macro_digits_test)
    comparison.to_csv(results / 'comparison_with_digits.csv', index=False)
    digits = load_digits()
    data_hash = hashlib.sha256(np.ascontiguousarray(digits.data).tobytes() + np.ascontiguousarray(digits.target).tobytes()).hexdigest()
    split = pd.read_csv(canonical / 'split_indices.csv')
    train_ids = split.loc[split.split == 'train', 'sample_index'].to_numpy()
    test_ids = split.loc[split.split == 'test', 'sample_index'].to_numpy()
    for group, indices in [('digits_train_8', train_ids), ('digits_test_8', test_ids)]:
        for index in indices:
            descriptors.append({'dataset': group, 'sample_id': int(index), 'true_label': int(digits.target[index]),
                                **image_descriptors(digits.images[index])})
    descriptor_frame = pd.DataFrame(descriptors)
    descriptor_frame.to_csv(results / 'image_descriptors.csv', index=False)
    metrics = [key for key in image_descriptors(digits.images[0])]
    descriptor_frame.groupby('dataset')[metrics].agg(['mean', 'std']).to_csv(results / 'distribution_summary.csv')
    descriptor_frame.groupby(['dataset', 'true_label'])[metrics].mean().to_csv(results / 'distribution_by_digit.csv')
    fig, axes = plt.subplots(2, 10, figsize=(16, 4.5), layout='constrained')
    for label in range(10):
        train_mean = digits.images[train_ids][digits.target[train_ids] == label].mean(axis=0)
        external_mean = pixel_array[labels[chosen] == label].mean(axis=0)
        for row, array in enumerate([train_mean, external_mean]):
            axes[row, label].imshow(array, cmap='gray', vmin=0, vmax=16, interpolation='nearest')
            axes[row, label].set(title=f'Chữ số {label}', xticks=[], yticks=[])
    axes[0, 0].set_ylabel('Digits train')
    axes[1, 0].set_ylabel('MNIST qua app')
    fig.suptitle('Ảnh trung bình theo lớp — cùng miền 0–16, không dùng chọn preprocessing')
    save_figure(fig, figures / 'class_mean_comparison.png')
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), layout='constrained')
    for ax, metric, title in zip(axes, ['mean_pixel', 'bbox_aspect_ratio', 'centroid_y'],
                                ['Độ sáng trung bình', 'Tỷ lệ rộng/cao vùng nét (≥20% đỉnh)', 'Tâm nét dọc (chuẩn hóa theo chiều cao)']):
        groups = ['digits_train_8', 'mnist_raw_28', 'mnist_app_8']
        for group in groups:
            values = descriptor_frame.loc[descriptor_frame.dataset == group, metric]
            ax.hist(values, bins=15, density=True, alpha=0.45, label=f'{group} (n={len(values)})')
        ax.set(title=title, xlabel=metric, ylabel='Mật độ')
        ax.legend(fontsize=8)
    save_figure(fig, figures / 'distribution_comparison.png')
    metadata = json.loads((ROOT / 'models' / registry['run_id'] / 'metadata.json').read_text())
    assert data_hash == metadata['data_sha256']
    write_json(directory / 'protected_after.json', verify_protected(directory))
    write_json(results / 'run_metadata.json', {'finished_at_utc': now(), 'sample_lock_sha256': lock_sha,
               'training_run_id': registry['run_id'], 'official_selected_model_unchanged': registry['selected_model'],
               'preprocessing_api': 'app.preprocess_uploaded_image(data, background="Tự động")',
               'prediction_api': 'app.predict_digit(saved_pipeline, pixels)', 'no_fit_guard': True,
               'n_images': 100, 'class_counts': np.bincount(labels[chosen], minlength=10).tolist(),
               'old_id_overlap': 0, 'old_image_pixel_overlap': 0, 'preprocessing_rejections': 0,
               'preprocessing_repeat_checks': len(diagnostics), 'background_inversion_checks': len(diagnostics),
               'data_sha256': data_hash, 'protected_count': len(verify_protected(directory)),
               'packages': {name: version(name) for name in ['numpy', 'pandas', 'scikit-learn', 'pillow', 'matplotlib', 'joblib']}})
    print(summary.to_string(index=False))
    print('EXTERNAL_EVALUATION_COMPLETE', directory.relative_to(ROOT).as_posix())


def verify(directory):
    """Kiểm số liệu lưu bằng công thức từ confusion matrix, và replay đúng API trên ảnh đã khóa."""
    lock = json.loads((directory / 'sample_lock.json').read_text(encoding='utf-8'))
    assert sha(directory / 'sample_lock.json') == (directory / 'sample_lock.sha256').read_text().strip()
    assert sha(directory / 'sample_ids.csv') == lock['sample_ids_csv_sha256']
    images, labels, old = read_idx(directory)
    ids, _ = select_ids(images, labels, old)
    assert ids == [row['mnist_test_index'] for row in lock['samples']]
    stored = np.load(directory / 'processed_pixels.npy', allow_pickle=False)
    results = directory / 'results'
    predictions = pd.read_csv(results / 'predictions.csv')
    registry = app.read_model_registry()
    with patch.object(Pipeline, 'fit', side_effect=AssertionError('Verify must not fit')):
        for item in lock['samples']:
            path = directory / item['original_file']
            assert sha(path) == item['original_png_sha256']
            np.testing.assert_array_equal(np.asarray(Image.open(path)), images[item['mnist_test_index']])
            processed = app.preprocess_uploaded_image(path.read_bytes())[1]
            np.testing.assert_array_equal(processed, stored[item['sample_order']])
        for name, entry in registry['models'].items():
            path = ROOT / 'models' / entry['path']
            stat = path.stat()
            pipeline = app.load_saved_pipeline(str(path), entry['sha256'], stat.st_mtime_ns, stat.st_size)
            group = predictions.loc[predictions.model == name].sort_values('sample_order')
            assert len(group) == 100 and group.mnist_test_index.tolist() == ids
            assert group.true_label.tolist() == labels[ids].tolist()
            for row in group.itertuples():
                prediction, probabilities = app.predict_digit(pipeline, stored[row.sample_order])
                assert prediction == row.predicted_label
                np.testing.assert_allclose([getattr(row, f'probability_{i}') for i in range(10)], probabilities['Xác suất'], atol=1e-12)
            cm = pd.read_csv(results / f'confusion_matrix_{name}.csv', index_col=0).to_numpy()
            np.testing.assert_array_equal(cm, confusion_matrix(group.true_label, group.predicted_label, labels=LABELS))
            assert cm.sum() == 100 and np.array_equal(cm.sum(axis=1), np.full(10, 10))
            precision = np.divide(np.diag(cm), cm.sum(axis=0), out=np.zeros(10, float), where=cm.sum(axis=0) != 0)
            recall = np.diag(cm) / cm.sum(axis=1)
            f1 = np.divide(2*precision*recall, precision+recall, out=np.zeros(10, float), where=precision+recall != 0)
            report = pd.read_csv(results / f'per_digit_{name}.csv')
            np.testing.assert_allclose(report.precision, precision, atol=1e-12)
            np.testing.assert_allclose(report.recall, recall, atol=1e-12)
            np.testing.assert_allclose(report['f1-score'], f1, atol=1e-12)
            summary = pd.read_csv(results / 'external_metrics.csv').set_index('model').loc[name]
            assert np.isclose(summary.accuracy, np.trace(cm)/100)
            assert np.isclose(summary.f1_macro, f1.mean())
            correct = pd.read_csv(results / f'correct_{name}.csv')
            incorrect = pd.read_csv(results / f'incorrect_{name}.csv')
            assert set(correct.mnist_test_index).isdisjoint(incorrect.mnist_test_index)
            assert set(correct.mnist_test_index) | set(incorrect.mnist_test_index) == set(ids)
            assert correct.correct.all() and not incorrect.correct.any()
    after = verify_protected(directory)
    write_json(directory / 'protected_after.json', after)
    check = {'verified_at_utc': now(), 'sample_lock_unchanged': True, 'selection_reproduced': True,
             'images_per_model': 100, 'classes': 10, 'images_per_class': 10,
             'replayed_preprocessing_equal': 100, 'replayed_predictions_equal': 300,
             'saved_probability_rows_checked': 300, 'metric_formula_checks': True,
             'correct_incorrect_lists_partition_sample': True, 'protected_count': len(after),
             'protected_sha256_unchanged': True, 'pipelines_match_registry': True, 'ui_frozen': True}
    write_json(directory / 'verification.json', check)
    print(json.dumps(check, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run', 'verify'])
    parser.add_argument('--directory', type=Path, help='Thư mục run đã prepare; không ghi đè kết quả.')
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        if args.directory is None:
            parser.error('--directory là bắt buộc với run/verify')
        directory = args.directory.resolve()
        if not directory.is_relative_to((ROOT / 'outputs').resolve()):
            parser.error('Run phải nằm trong outputs/')
        (run if args.action == 'run' else verify)(directory)
