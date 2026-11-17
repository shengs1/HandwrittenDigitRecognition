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
    def test_dataset_mode_predicts_with_each_saved_model_without_fit(self):
        with patch.object(Pipeline, "fit", side_effect=AssertionError("App must not fit")), \
             patch.object(app, "preprocess_uploaded_image", side_effect=AssertionError("Digits must stay unchanged")):
            at = AppTest.from_string("from app import main\nmain()", default_timeout=30).run()
            self.assertFalse(at.exception)
            for name in app.read_model_registry()["models"]:
                at.selectbox(key="model").select(name).run()
                at.button[0].click().run()
                self.assertFalse(at.exception)
                self.assertEqual(len(at.metric), 2)
                self.assertIn(int(at.metric[0].value), range(10))

    def test_upload_flow_with_real_external_image(self):
        fixture = next((ROOT / "tests/fixtures/external_digits").glob("*.png"))
        script = ("from io import BytesIO\nfrom unittest.mock import patch\nimport app\n"
                  f"from pathlib import Path\ndata=Path({str(fixture)!r}).read_bytes()\n"
                  "with patch.object(app.st, 'file_uploader', return_value=BytesIO(data)):\n    app.main()")
        at = AppTest.from_string(script, default_timeout=30).run()
        at.radio(key="source").set_value("Tải ảnh từ máy").run()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 2)

    def test_upload_invalid_file_is_a_user_error_not_crash(self):
        script = ("from io import BytesIO\nfrom unittest.mock import patch\nimport app\n"
                  "with patch.object(app.st, 'file_uploader', return_value=BytesIO(b'broken')):\n    app.main()")
        at = AppTest.from_string(script, default_timeout=30).run()
        at.radio(key="source").set_value("Tải ảnh từ máy").run()
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


if __name__ == "__main__":
    unittest.main()
