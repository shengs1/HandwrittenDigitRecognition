"""Xuất bằng chứng suy luận demo; không fit/tuning hoặc sửa artifact mô hình."""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import os
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "tmp" / "matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
from unittest.mock import patch
import app


def main():
    registry = app.read_model_registry()
    data = load_digits()
    run_id = 'demo_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:8]
    out = ROOT / 'outputs' / run_id
    out.mkdir(parents=True, exist_ok=False)
    (out / 'preprocessed').mkdir()
    hashes_before, pipelines = {}, {}
    for name, entry in registry['models'].items():
        path = ROOT / 'models' / entry['path']
        hashes_before[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        stat = path.stat()
        pipelines[name] = app.load_saved_pipeline(str(path), entry['sha256'], stat.st_mtime_ns, stat.st_size)
    sample_rows, external_rows = [], []
    fixture_dir = ROOT / 'tests/fixtures/external_digits'
    fixtures = json.loads((fixture_dir / 'manifest.json').read_text(encoding='utf-8'))
    fig, axes = plt.subplots(2, 10, figsize=(18, 5), layout='constrained')
    with patch.object(Pipeline, 'fit', side_effect=AssertionError('Inference checks cannot fit')):
        for label in range(10):
            index = int(np.flatnonzero(data.target == label)[0])
            for name, pipeline in pipelines.items():
                prediction, probabilities = app.predict_digit(pipeline, data.images[index])
                sample_rows.append({'model': name, 'sample_index': index, 'true_label': label,
                                    'predicted_label': prediction,
                                    'probability_predicted': float(probabilities.loc[str(prediction), 'Xác suất'])})
        for col, item in enumerate(fixtures['images']):
            original, pixels, info = app.preprocess_uploaded_image((fixture_dir / item['filename']).read_bytes())
            buffer = BytesIO()
            ImageOps.invert(original).save(buffer, format='PNG')
            inverted_pixels = app.preprocess_uploaded_image(buffer.getvalue())[1]
            assert np.array_equal(pixels, inverted_pixels), 'Background inversion changed processed input'
            Image.fromarray(np.rint(pixels*255/16).astype(np.uint8)).save(out / 'preprocessed' / item['filename'])
            for name, pipeline in pipelines.items():
                prediction, probabilities = app.predict_digit(pipeline, pixels)
                external_rows.append({'model': name, 'filename': item['filename'],
                    'mnist_test_index': item['mnist_test_index'], 'true_label': item['label'],
                    'predicted_label': prediction, 'correct': prediction == item['label'],
                    'probability_predicted': float(probabilities.loc[str(prediction), 'Xác suất']),
                    'background_inversion_equal': True})
            axes[0, col].imshow(original)
            axes[0, col].set_title(f"Thật: {item['label']}\nid={item['mnist_test_index']}")
            axes[1, col].imshow(pixels, cmap='gray', vmin=0, vmax=16)
            chosen = next(row for row in reversed(external_rows) if row['model'] == registry['selected_model'])
            axes[1, col].set_title(f"KNN: {chosen['predicted_label']}\n{chosen['probability_predicted']:.1%}")
            for ax in axes[:, col]:
                ax.set_xticks([])
                ax.set_yticks([])
                ax.grid(False)
        axes[0, 0].set_ylabel('MNIST gốc 28×28')
        axes[1, 0].set_ylabel('Sau xử lý 8×8')
        fig.suptitle('Kiểm thử ngoài Digits — 10 ảnh MNIST chọn trước suy luận; không dùng tuning')
        fig.savefig(out / 'external_image_preview.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
    sample_frame, external_frame = pd.DataFrame(sample_rows), pd.DataFrame(external_rows)
    sample_frame.to_csv(out / 'digits_sample_predictions.csv', index=False)
    external_frame.to_csv(out / 'external_predictions.csv', index=False)
    hashes_after = {name: hashlib.sha256((ROOT / 'models' / entry['path']).read_bytes()).hexdigest()
                    for name, entry in registry['models'].items()}
    assert hashes_before == hashes_after
    summary = {'demo_run_id': run_id, 'training_run_id': registry['run_id'],
               'inference_only': True, 'model_files_unchanged': True,
               'model_sha256': hashes_after, 'app_sha256': hashlib.sha256((ROOT / 'app.py').read_bytes()).hexdigest(),
               'digits_examples_per_model': 10, 'external_examples_per_model': 10,
               'digits_correct_per_model': {name: int((group.true_label == group.predicted_label).sum())
                                            for name, group in sample_frame.groupby('model')},
               'external_correct_per_model': {name: int(group.correct.sum()) for name, group in external_frame.groupby('model')},
               'external_source': fixtures['source_page'],
               'selection_rule': fixtures['selection_rule'],
               'camera_photos_tested': False,
               'limitations': '10 MNIST examples are a small illustrative check, not an accuracy estimate for arbitrary camera photos.'}
    (out / 'demo_verification.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print('DEMO_VERIFIED', out)


if __name__ == '__main__':
    main()
