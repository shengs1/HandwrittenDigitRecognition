"""Không fit mô hình trong test: dùng artifact thật, kiểm tra ảnh và các luồng app."""
from copy import deepcopy
from io import BytesIO
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app


def setUpModule():
    # tmp/ không được track: checkout mới phải tự tạo trước các test dùng TemporaryDirectory.
    (ROOT / "tmp").mkdir(parents=True, exist_ok=True)


def png_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class ImagePreprocessingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = Image.new("RGB", (100, 120), "white")
        ImageDraw.Draw(cls.image).ellipse((25, 15, 70, 105), outline="black", width=12)

    def test_opaque_polarities_produce_same_input(self):
        _, normal, _ = app.preprocess_uploaded_image(png_bytes(self.image))
        _, inverted, _ = app.preprocess_uploaded_image(png_bytes(ImageOps.invert(self.image)))
        np.testing.assert_array_equal(normal, inverted)
        self.assertEqual(normal.shape, (8, 8))
        self.assertTrue(np.isfinite(normal).all() and normal.min() >= 0 and normal.max() <= 16)

    def test_transparent_white_and_black_strokes(self):
        outputs = []
        for color in ["black", "white"]:
            image = Image.new("RGBA", (100, 120), (0, 0, 0, 0))
            ImageDraw.Draw(image).ellipse((25, 15, 70, 105), outline=color, width=12)
            outputs.append(app.preprocess_uploaded_image(png_bytes(image))[1])
        np.testing.assert_array_equal(outputs[0], outputs[1])

    def test_blank_corrupt_empty_and_transparent_are_rejected(self):
        cases = [b"", b"not an image", png_bytes(Image.new("L", (40, 40), 255)),
                 png_bytes(Image.new("L", (40, 40), 0)), png_bytes(Image.new("RGBA", (40, 40), (0, 0, 0, 0)))]
        for case in cases:
            with self.subTest(size=len(case)), self.assertRaises(ValueError):
                app.preprocess_uploaded_image(case)

    def test_file_and_pixel_limits(self):
        with patch.object(app, "MAX_FILE_BYTES", 5), self.assertRaisesRegex(ValueError, "10 MB"):
            app.preprocess_uploaded_image(b"123456")
        with patch.object(app, "MAX_IMAGE_PIXELS", 100), self.assertRaisesRegex(ValueError, "quá lớn"):
            app.preprocess_uploaded_image(png_bytes(self.image))

    def test_off_center_digit_is_centered_without_stretch(self):
        image = Image.new("RGB", (180, 180), "white")
        ImageDraw.Draw(image).rectangle((5, 5, 20, 130), fill="black")
        _, pixels, _ = app.preprocess_uploaded_image(png_bytes(image))
        rows, cols = np.indices((8, 8))
        self.assertLess(abs(float((cols*pixels).sum()/pixels.sum()) - 3.5), 0.6)
        self.assertLess(abs(float((rows*pixels).sum()/pixels.sum()) - 3.5), 0.6)
        self.assertLess(np.count_nonzero(pixels.sum(axis=0)), np.count_nonzero(pixels.sum(axis=1)))

    def test_invalid_background_is_rejected(self):
        with self.assertRaises(ValueError):
            app.preprocess_uploaded_image(png_bytes(self.image), "unknown")

    def test_train_digits_keep_input_under_polarity_mode_and_translation(self):
        # Chỉ kiểm tra tính chất của ảnh tương đương trên train, không tối ưu theo test/MNIST.
        registry = app.read_model_registry()
        split = pd.read_csv(ROOT / 'outputs' / registry['run_id'] / 'split_indices.csv')
        train_ids = split.loc[split.split == 'train', 'sample_index'].to_numpy()
        digits = load_digits()
        for label in range(10):
            index = int(train_ids[digits.target[train_ids] == label][0])
            glyph = Image.fromarray(np.uint8(np.rint(digits.images[index] * 255/16))).resize(
                (80, 80), Image.Resampling.NEAREST)
            first = Image.new('L', (180, 180), 0)
            first.paste(glyph, (10, 20))
            shifted = Image.new('L', (220, 200), 0)
            shifted.paste(glyph, (120, 100))
            rgba = first.convert('RGBA')
            rgba.putalpha(first.point(lambda value: 255 if value else 0))
            expected = app.preprocess_uploaded_image(png_bytes(first))[1]
            for variant in [shifted, first.convert('RGB'), rgba, ImageOps.invert(first)]:
                with self.subTest(train_id=index, mode=variant.mode, size=variant.size):
                    actual = app.preprocess_uploaded_image(png_bytes(variant))[1]
                    np.testing.assert_array_equal(expected, actual)

    def test_exif_orientation_is_applied_before_crop(self):
        # PNG giữ nguyên pixel để không lẫn tác động nén JPEG vào phép kiểm tra orientation.
        rotated_storage = self.image.transpose(Image.Transpose.ROTATE_90)
        exif = Image.Exif()
        exif[274] = 6  # hiển thị xoay 90 độ theo chiều kim đồng hồ
        buffer = BytesIO()
        rotated_storage.save(buffer, format='PNG', exif=exif)
        expected = app.preprocess_uploaded_image(png_bytes(self.image))[1]
        actual = app.preprocess_uploaded_image(buffer.getvalue())[1]
        np.testing.assert_array_equal(expected, actual)


class SavedPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = app.read_model_registry()
        cls.data = load_digits()

    def load(self, name):
        entry = self.registry["models"][name]
        path = ROOT / "models" / entry["path"]
        stat = path.stat()
        return app.load_saved_pipeline(str(path), entry["sha256"], stat.st_mtime_ns, stat.st_size)

    def test_saved_test_predictions_match_all_three_pipelines(self):
        run = ROOT / "outputs" / self.registry["run_id"]
        predictions = pd.read_csv(run / "test_predictions.csv")
        with patch.object(Pipeline, "fit", side_effect=AssertionError("App/test must not fit")):
            for name in self.registry["models"]:
                records = predictions[predictions.model == name]
                pipeline = self.load(name)
                features = pd.DataFrame(self.data.data[records.sample_index], columns=self.data.feature_names)
                np.testing.assert_array_equal(pipeline.predict(features), records.predicted_label)
                np.testing.assert_array_equal(self.data.target[records.sample_index], records.true_label)
                self.assertEqual(len(records), 360)

    def test_probability_labels_and_no_double_scaling(self):
        with patch.object(Pipeline, "fit", side_effect=AssertionError("Unexpected fit")):
            for name in self.registry["models"]:
                pipeline = self.load(name)
                predicted, table = app.predict_digit(pipeline, self.data.images[0])
                features = pd.DataFrame(self.data.data[[0]], columns=self.data.feature_names)
                np.testing.assert_allclose(table["Xác suất"], pipeline.predict_proba(features)[0], rtol=1e-12)
                self.assertEqual(predicted, int(pipeline.predict(features)[0]))
                self.assertEqual(list(table.index), [str(i) for i in range(10)])

    def test_parameter_table_values_come_from_saved_pipelines(self):
        for name in self.registry['models']:
            pipeline = self.load(name)
            rows = dict(app.model_parameter_rows(pipeline))
            params = pipeline.steps[-1][1].get_params(deep=False)
            if name == 'knn':
                self.assertEqual(rows['Số láng giềng'], str(params['n_neighbors']))
                self.assertEqual(rows['Trọng số'].lower(), params['weights'])
                self.assertEqual(rows['Metric khoảng cách'], params['metric'])
            elif name == 'mlp':
                self.assertEqual(rows['Kiến trúc lớp ẩn'], ' → '.join(map(str, params['hidden_layer_sizes'])))
                self.assertEqual(rows['Activation'], params['activation'])
                self.assertEqual(rows['Optimizer / solver'], params['solver'])
                self.assertEqual(rows['Alpha'], str(params['alpha']))
            else:
                self.assertEqual(rows['C'], str(params['C']))
                self.assertEqual(rows['Solver'], params['solver'])
                self.assertIn('pixel thô', rows['Chuẩn hóa'])
            if name != 'logreg_raw':
                self.assertEqual(rows['Chuẩn hóa'], type(pipeline.named_steps['scale']).__name__)

    def test_parameter_reader_is_dynamic_without_training_or_changing_artifact(self):
        original = self.load('knn')
        old_neighbors = original.named_steps['clf'].n_neighbors
        # Chỉ thử API đọc tham số trên clone chưa fit; không tuning hoặc lưu model mới.
        with patch.object(Pipeline, 'fit', side_effect=AssertionError('Parameter display must not fit')):
            alternative = clone(original).set_params(clf__n_neighbors=old_neighbors + 2, clf__weights='distance')
            rows = dict(app.model_parameter_rows(alternative))
        self.assertEqual(rows['Số láng giềng'], str(old_neighbors + 2))
        self.assertEqual(rows['Trọng số'], 'Distance')
        self.assertEqual(original.named_steps['clf'].n_neighbors, old_neighbors)

    def test_invalid_feature_domain_is_rejected(self):
        pipeline = self.load("knn")
        for array in [np.zeros((7, 8)), np.full((8, 8), np.nan), np.full((8, 8), 17), np.full((8, 8), -1)]:
            with self.assertRaises(ValueError):
                app.predict_digit(pipeline, array)

    def test_missing_registry_and_path_traversal(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            directory = Path(directory)
            with self.assertRaises(FileNotFoundError):
                app.read_model_registry(directory)
            registry = deepcopy(self.registry)
            registry["models"]["knn"]["path"] = "../../outside.joblib"
            (directory / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
            with self.assertRaises(ValueError):
                app.read_model_registry(directory)

    def test_missing_or_corrupt_pipeline(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            path = Path(directory) / "invalid.joblib"
            with self.assertRaises(FileNotFoundError):
                app.load_saved_pipeline(str(path), "0"*64, 0, 0)
            path.write_bytes(b"invalid")
            with self.assertRaisesRegex(ValueError, "khớp mã"):
                app.load_saved_pipeline(str(path), "0"*64, 1, 7)

    def test_demo_test_indices_equal_official_prediction_membership(self):
        indices = app.saved_test_indices(self.registry)
        records = pd.read_csv(ROOT / 'outputs' / self.registry['run_id'] / 'test_predictions.csv')
        self.assertEqual(len(indices), 360)
        for name in self.registry['models']:
            np.testing.assert_array_equal(np.sort(indices), np.sort(records.loc[records.model == name, 'sample_index']))
        with self.assertRaises(ValueError):
            app.saved_test_indices({'run_id': '../invalid'})
        with self.assertRaises(FileNotFoundError):
            app.saved_test_indices({'run_id': 'missing_run'})

    def test_invalid_saved_split_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tmp') as directory:
            run = Path(directory) / 'outputs' / 'example'
            run.mkdir(parents=True)
            pd.DataFrame({'sample_index': [0, 0], 'split': ['test', 'test']}).to_csv(run / 'split_indices.csv', index=False)
            with patch.object(app, 'ROOT', Path(directory)), self.assertRaises(ValueError):
                app.saved_test_indices({'run_id': 'example'})

    def test_external_images_only_inference_and_both_polarities(self):
        directory = ROOT / "tests" / "fixtures" / "external_digits"
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["images"]), 10)
        with patch.object(Pipeline, "fit", side_effect=AssertionError("External data must not train")):
            for item in manifest["images"]:
                data = (directory / item["filename"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                original, pixels, _ = app.preprocess_uploaded_image(data)
                inverted = app.preprocess_uploaded_image(png_bytes(ImageOps.invert(original)))[1]
                np.testing.assert_array_equal(pixels, inverted)
                for name in self.registry["models"]:
                    prediction, probabilities = app.predict_digit(self.load(name), pixels)
                    self.assertIn(prediction, range(10))
                    self.assertAlmostEqual(float(probabilities["Xác suất"].sum()), 1)


class AppFlowTests(unittest.TestCase):
    def test_technical_information_updates_for_each_selected_model(self):
        registry = app.read_model_registry()
        summary = app.read_demo_summary(registry)
        with patch.object(Pipeline, 'fit', side_effect=AssertionError('Technical information must not fit')):
            at = AppTest.from_string('from app import main\nmain()', default_timeout=30).run()
            for name, entry in registry['models'].items():
                at.selectbox(key='model').select(name).run()
                self.assertFalse(at.exception)
                bodies = [item.proto.body for item in at.get('html') if '<div class="technical-info">' in item.proto.body]
                self.assertEqual(len(bodies), 1)
                path = ROOT / 'models' / entry['path']
                stat = path.stat()
                pipeline = app.load_saved_pipeline(str(path), entry['sha256'], stat.st_mtime_ns, stat.st_size)
                self.assertEqual(bodies[0], app.technical_information_html(summary, app.model_parameter_rows(pipeline)))
                for heading in ['Thông tin dữ liệu', 'Cấu hình mô hình', 'Quy trình xử lý ảnh', 'Giới hạn mô hình']:
                    self.assertIn(heading, bodies[0])
                self.assertIn(app.MODEL_LIMITS_TEXT, bodies[0])
                self.assertNotIn(registry['run_id'], bodies[0])
                self.assertNotIn(entry['sha256'], bodies[0])
                self.assertNotIn('3/10', bodies[0])

    def assert_visible_prediction(self, at):
        """Kiểm cả kết quả thật và HTML hiển thị, thay cho hai st.metric của giao diện cũ."""
        self.assertFalse(at.exception)
        result = at.session_state['prediction_result']
        self.assertEqual(result['classes'], [str(i) for i in range(10)])
        self.assertEqual(len(result['probabilities']), 10)
        self.assertAlmostEqual(sum(result['probabilities']), 1)
        rendered = '\n'.join(item.value for item in at.markdown)
        self.assertIn(f'data-prediction="{result["predicted"]}"', rendered)
        for label in result['classes']:
            self.assertIn(f'data-label="{label}"', rendered)
        self.assertIn('Xác suất chưa hiệu chỉnh', rendered)
        return result

    def test_test_only_sampler_uses_saved_split_and_each_pipeline(self):
        registry = app.read_model_registry()
        digits = load_digits()
        records = pd.read_csv(ROOT / 'outputs' / registry['run_id'] / 'test_predictions.csv')
        test_ids = app.saved_test_indices(registry)
        with patch.object(Pipeline, 'fit', side_effect=AssertionError('App must not fit')), \
             patch.object(app, 'preprocess_uploaded_image', side_effect=AssertionError('Digits must stay unchanged')):
            at = AppTest.from_string('from app import main\nmain()', default_timeout=30).run()
            at.selectbox(key='source').select('Ảnh test Digits').run()
            for label in range(10):
                at.selectbox(key='sample_label').select(label).run()
                expected = test_ids[digits.target[test_ids] == label].tolist()
                self.assertEqual(at.selectbox(key=f'test_sample_{label}').options, [str(i) for i in expected])
            at.selectbox(key='sample_label').select(0).run()
            index = int(at.selectbox(key='test_sample_0').value)
            for name in registry['models']:
                at.selectbox(key='model').select(name).run()
                at.button[0].click().run()
                self.assertFalse(at.exception)
                expected = records.loc[(records.model == name) & (records.sample_index == index), 'predicted_label'].item()
                self.assertEqual(self.assert_visible_prediction(at)['predicted'], expected)

    def test_missing_saved_split_disables_test_prediction(self):
        with patch.object(app, 'saved_test_indices', side_effect=FileNotFoundError('Thiếu split_indices.csv')):
            at = AppTest.from_string('from app import main\nmain()', default_timeout=30).run()
            at.selectbox(key='source').select('Ảnh test Digits').run()
            self.assertFalse(at.exception)
            self.assertTrue(at.error)
            self.assertTrue(at.button[0].disabled)

    def test_dataset_mode_predicts_with_each_saved_model_without_fit(self):
        with patch.object(Pipeline, "fit", side_effect=AssertionError("App must not fit")), \
             patch.object(app, "preprocess_uploaded_image", side_effect=AssertionError("Digits must stay unchanged")):
            at = AppTest.from_string("from app import main\nmain()", default_timeout=30).run()
            self.assertFalse(at.exception)
            at.selectbox(key='source').select('Ảnh mẫu Digits').run()
            for name in app.read_model_registry()["models"]:
                at.selectbox(key="model").select(name).run()
                at.button[0].click().run()
                self.assertFalse(at.exception)
                result = self.assert_visible_prediction(at)
                self.assertIn(result['predicted'], range(10))
                self.assertEqual(result['model'], name)

    def test_upload_flow_with_real_external_image(self):
        fixture = next((ROOT / "tests/fixtures/external_digits").glob("*.png"))
        script = ("from io import BytesIO\nfrom unittest.mock import patch\nimport app\n"
                  f"from pathlib import Path\ndata=Path({str(fixture)!r}).read_bytes()\n"
                  "with patch.object(app.st, 'file_uploader', return_value=BytesIO(data)):\n    app.main()")
        at = AppTest.from_string(script, default_timeout=30).run()
        at.selectbox(key="source").select("Tải ảnh từ máy").run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assert_visible_prediction(at)

    def test_upload_invalid_file_is_a_user_error_not_crash(self):
        script = ("from io import BytesIO\nfrom unittest.mock import patch\nimport app\n"
                  "with patch.object(app.st, 'file_uploader', return_value=BytesIO(b'broken')):\n    app.main()")
        at = AppTest.from_string(script, default_timeout=30).run()
        at.selectbox(key="source").select("Tải ảnh từ máy").run()
        self.assertFalse(at.exception)
        self.assertTrue(at.error)
        self.assertTrue(at.button[0].disabled)

    def test_missing_registry_disables_prediction_but_keeps_preview(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            script = ("from pathlib import Path\nfrom unittest.mock import patch\nimport app\n"
                      f"with patch.object(app, 'MODEL_DIR', Path({directory!r})):\n    app.main()")
            at = AppTest.from_string(script, default_timeout=30).run()
            self.assertFalse(at.exception)
            self.assertTrue(at.warning)
            self.assertTrue(at.button[0].disabled)
            self.assertIn('image-card', '\n'.join(item.value for item in at.markdown))

    def test_missing_pipeline_file_shows_error_without_crash(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            (Path(directory) / "registry.json").write_text(json.dumps(app.read_model_registry()), encoding="utf-8")
            script = ("from pathlib import Path\nfrom unittest.mock import patch\nimport app\n"
                      f"with patch.object(app, 'MODEL_DIR', Path({directory!r})):\n    app.main()")
            at = AppTest.from_string(script, default_timeout=30).run()
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(at.error)
            self.assertIn("Thiếu file Pipeline", at.error[0].value)

    def test_default_test_source_has_honest_empty_state_and_artifact_overview(self):
        at = AppTest.from_string('from app import main\nmain()', default_timeout=30).run()
        self.assertFalse(at.exception)
        self.assertEqual(at.selectbox(key='source').value, 'Ảnh test Digits')
        with self.assertRaises(KeyError):
            at.session_state['prediction_result']
        rendered = '\n'.join(item.value for item in at.markdown)
        self.assertIn('result-empty', rendered)
        self.assertNotIn('data-prediction=', rendered)
        summary = app.read_demo_summary(app.read_model_registry())
        self.assertIn(f'{summary["accuracy"]:.2%}'.replace('.', ','), rendered)
        self.assertIn(f'{summary["n_samples"]:,}'.replace(',', '.'), rendered)
        # Mẫu Digits chỉ có một ảnh pixel-grid, không nhân đôi preview gốc/8×8.
        self.assertEqual(rendered.count('data:image/png;base64,'), 1)
        self.assertIn('pixel-grid', rendered)

    def test_changed_model_label_id_or_source_clears_previous_result(self):
        at = AppTest.from_string('from app import main\nmain()', default_timeout=30).run()
        at.button(key='predict').click().run()
        self.assert_visible_prediction(at)
        actions = [lambda: at.selectbox(key='model').select('mlp').run(),
                   lambda: at.selectbox(key='sample_label').select(1).run(),
                   lambda: at.selectbox(key='test_sample_1').select(
                       int(at.selectbox(key='test_sample_1').options[1])).run(),
                   lambda: at.selectbox(key='source').select('Ảnh mẫu Digits').run()]
        for action in actions:
            action()
            self.assertFalse(at.exception)
            with self.assertRaises(KeyError):
                at.session_state['prediction_result']
            self.assertFalse(any('data-prediction=' in item.value for item in at.markdown))
            at.button(key='predict').click().run()
            self.assert_visible_prediction(at)

    def test_upload_background_change_and_removal_clear_prediction(self):
        fixture = next((ROOT / 'tests/fixtures/external_digits').glob('*.png'))
        script = ('from io import BytesIO\nfrom unittest.mock import patch\nfrom pathlib import Path\nimport app\n'
                  f'data=Path({str(fixture)!r}).read_bytes()\n'
                  "upload=BytesIO(data) if app.st.session_state.get('mock_upload', True) else None\n"
                  "with patch.object(app.st, 'file_uploader', return_value=upload):\n    app.main()")
        at = AppTest.from_string(script, default_timeout=30).run()
        at.selectbox(key='source').select('Tải ảnh từ máy').run()
        self.assertEqual('\n'.join(item.value for item in at.markdown).count('data:image/png;base64,'), 2)
        at.button(key='predict').click().run()
        self.assert_visible_prediction(at)
        at.selectbox(key='background').select('Nền tối, nét sáng').run()
        with self.assertRaises(KeyError):
            at.session_state['prediction_result']
        at.button(key='predict').click().run()
        self.assert_visible_prediction(at)
        at.session_state['mock_upload'] = False
        at.run()
        self.assertFalse(at.exception)
        with self.assertRaises(KeyError):
            at.session_state['prediction_result']
        self.assertTrue(at.button(key='predict').disabled)


if __name__ == "__main__":
    unittest.main()
