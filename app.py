"""Demo Digits: chỉ đọc Pipeline đã lưu; không fit hoặc tuning trong ứng dụng."""
from io import BytesIO
from pathlib import Path
from html import escape
import base64
import hashlib
import json
import warnings

import joblib
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, UnidentifiedImageError
import streamlit as st
from sklearn.datasets import load_digits
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted
from external_preprocessing import preprocess_external_image

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"
MODEL_NAMES = {"logreg_raw": "Logistic Regression", "knn": "K-Nearest Neighbors (KNN)",
               "mlp": "Multilayer Perceptron (MLP)"}
MODEL_SHORT_NAMES = {"logreg_raw": "Logistic Regression", "knn": "KNN", "mlp": "MLP"}
EXTERNAL_MODEL_NAME = "Multilayer Perceptron (MLP) — MNIST"
MODEL_SHORT_NAMES["mlp_mnist"] = "MLP · MNIST"
BACKGROUND_OPTIONS = ["Tự động", "Nền sáng, nét tối", "Nền tối, nét sáng"]
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000


def read_model_registry(model_dir=None):
    """Manifest cố định; không tự tìm model có điểm test cao nhất hoặc file mới nhất."""
    model_dir = Path(model_dir) if model_dir is not None else MODEL_DIR
    path = model_dir / "registry.json"
    if not path.is_file():
        raise FileNotFoundError("Chưa có danh sách mô hình đã lưu (models/registry.json). Hãy khôi phục bộ mô hình của dự án.")
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ValueError("Không đọc được danh sách mô hình. Kiểm tra models/registry.json.") from exc
    if not isinstance(registry, dict) or not isinstance(registry.get("models"), dict) or not registry["models"]:
        raise ValueError("Danh sách mô hình chưa đúng định dạng.")
    if registry.get("selected_model") not in registry["models"]:
        raise ValueError("Mô hình mặc định không có trong danh sách.")
    for name, entry in registry["models"].items():
        if name not in MODEL_NAMES or not isinstance(entry, dict):
            raise ValueError("Tên hoặc thông tin mô hình không hợp lệ.")
        relative = entry.get("path")
        if not isinstance(relative, str) or Path(relative).is_absolute():
            raise ValueError("Đường dẫn mô hình phải nằm trong models/.")
        candidate = (model_dir / relative).resolve()
        if not candidate.is_relative_to(model_dir.resolve()) or candidate.suffix != ".joblib":
            raise ValueError("Đường dẫn mô hình phải nằm trong models/ và có đuôi .joblib.")
        checksum = entry.get("sha256")
        if not isinstance(checksum, str) or len(checksum) != 64:
            raise ValueError("Thiếu mã kiểm tra toàn vẹn mô hình.")
    return registry


@st.cache_resource(show_spinner=False)
def load_saved_pipeline(path_text, expected_sha256, modified_ns, file_size, expected_features=64):
    """Cache theo file/hash/mtime/size; chỉ load artifact local tin cậy của project."""
    path = Path(path_text)
    if not path.is_file():
        raise FileNotFoundError("Thiếu tệp mô hình đã chọn. Khôi phục đúng thư mục models/ đã lưu.")
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError("File mô hình không khớp mã kiểm tra trong registry. Không sử dụng file này.")
    with warnings.catch_warnings():
        # Cảnh báo sai phiên bản sklearn được chuyển thành lỗi dễ xử lý trong giao diện.
        from sklearn.exceptions import InconsistentVersionWarning
        warnings.simplefilter("error", InconsistentVersionWarning)
        pipeline = joblib.load(path)
    if not isinstance(pipeline, Pipeline) or not callable(getattr(pipeline, "predict_proba", None)):
        raise ValueError("Tệp mô hình phải chứa đầy đủ chuỗi xử lý và hỗ trợ dự đoán xác suất.")
    check_is_fitted(pipeline)
    classifier = pipeline.steps[-1][1]
    # sklearn 1.7 không chuyển tiếp n_features_in_ qua bước đầu là chuỗi passthrough.
    if expected_features not in {64, 784} or getattr(classifier, "n_features_in_", None) != expected_features or not np.array_equal(pipeline.classes_, np.arange(10)):
        raise ValueError(f"Mô hình phải nhận {expected_features} điểm ảnh và phân loại đủ các nhãn 0–9.")
    return pipeline


def read_external_registry(model_dir=None):
    """Cấu hình upload riêng đã khóa bằng validation; không sửa registry Digits."""
    model_dir = Path(model_dir) if model_dir is not None else MODEL_DIR
    path = model_dir / "external_registry.json"
    if not path.is_file():
        return None
    config = json.loads(path.read_text(encoding="utf-8"))
    run = config["optimization_run"]
    if not isinstance(run, str) or not run or any(c not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_" for c in run):
        raise ValueError("Mã thực nghiệm ảnh ngoài không hợp lệ.")
    lock_path = ROOT / "outputs" / run / "selection_lock.json"
    if hashlib.sha256(lock_path.read_bytes()).hexdigest() != config["selection_lock_sha256"]:
        raise ValueError("Cấu hình ảnh ngoài không khớp lựa chọn đã khóa.")
    if hashlib.sha256((ROOT / "external_preprocessing.py").read_bytes()).hexdigest() != config["preprocessing_module_sha256"]:
        raise ValueError("Mã tiền xử lý ảnh ngoài không khớp bản đã đánh giá.")
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if config["shared_variant"] != lock["shared_variant"] or config["specialist_enabled"] != lock["specialist_upload_option"]:
        raise ValueError("Cấu hình ảnh tải lên khác lựa chọn từ tập xác thực.")
    entry = config["specialist"]
    selected_specialist = next((item for item in lock["evaluation_systems"] if item["model"] == "mlp_mnist"), None)
    if (not selected_specialist or entry["sha256"] != selected_specialist["sha256"]
            or config["preprocessing_module_sha256"] != lock["preprocessing_module_sha256"]):
        raise ValueError("Mô hình hoặc tiền xử lý khác phiên bản đã khóa bằng tập xác thực.")
    candidate = (model_dir / entry["path"]).resolve()
    if not candidate.is_relative_to(model_dir.resolve()) or candidate.suffix != ".joblib" or entry["input_features"] != 784:
        raise ValueError("Đường dẫn hoặc kích thước đầu vào của mô hình MNIST không hợp lệ.")
    return config


def preprocess_upload_for_model(data, background, model_name, external_config):
    if model_name == "mlp_mnist":
        if not external_config or not external_config["specialist_enabled"]:
            raise ValueError("Chưa có mô hình MNIST đã được xác nhận.")
        return preprocess_external_image(data, background, "mnist28")
    if external_config and external_config["shared_variant"] != "baseline":
        return preprocess_external_image(data, background, external_config["shared_variant"])
    return preprocess_uploaded_image(data, background)


def preprocess_uploaded_image(data, background="Tự động"):
    """Ảnh tải lên → nét sáng/nền 0 → căn giữa → 8×8, [0,16]; không StandardScaler ở đây."""
    if not data:
        raise ValueError("File ảnh rỗng. Hãy chọn một ảnh chữ số.")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("Ảnh vượt 10 MB. Hãy chọn file nhỏ hơn.")
    if background not in BACKGROUND_OPTIONS:
        raise ValueError("Chế độ màu nền không hợp lệ.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as opened:
                if opened.format not in {"PNG", "JPEG", "BMP", "WEBP"}:
                    raise ValueError("Chỉ hỗ trợ PNG, JPEG, BMP và WebP.")
                if opened.width * opened.height > MAX_IMAGE_PIXELS:
                    raise ValueError("Ảnh quá lớn (tối đa 16 triệu pixel). Hãy giảm kích thước ảnh.")
                original = ImageOps.exif_transpose(opened).convert("RGBA")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError("Không đọc được file ảnh. File có thể bị hỏng hoặc không phải ảnh hợp lệ.") from exc

    rgba = np.asarray(original)
    alpha = rgba[:, :, 3]
    visible = alpha > 64
    if not visible.any():
        raise ValueError("Ảnh trong suốt hoặc trống, không tìm thấy chữ số.")
    border_alpha = np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]])
    visible_gray = np.asarray(original.convert("L"))[visible]
    # Với nền trong suốt, chọn nền đối lập màu nét thay vì luôn ghép nền trắng.
    matte = 0 if border_alpha.mean() < 128 and np.median(visible_gray) >= 128 else 255
    composite = Image.new("RGBA", original.size, (matte, matte, matte, 255))
    composite.alpha_composite(original)
    original_rgb = composite.convert("RGB")
    gray = np.asarray(original_rgb.convert("L"), dtype=np.float32)
    border = np.concatenate([gray[0], gray[-1], gray[:, 0], gray[:, -1]])
    background_value = float(np.median(border))
    light_background = background_value >= 127.5 if background == "Tự động" else background == "Nền sáng, nét tối"
    ink = np.maximum((background_value - gray) if light_background else (gray - background_value), 0)
    contrast = float(ink.max())
    if contrast < 25:
        raise ValueError("Ảnh trống hoặc tương phản quá thấp, không tìm thấy nét chữ rõ.")
    mask = ink >= max(12, 0.2 * contrast)
    if int(mask.sum()) < 3:
        raise ValueError("Không đủ nét chữ để nhận dạng. Hãy dùng ảnh chỉ có một chữ số rõ.")
    ink = np.where(mask, ink, 0)
    ys, xs = np.where(mask)
    box = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
    crop = Image.fromarray(np.clip(ink, 0, 255).astype(np.uint8)).crop(box)
    # Nét Digits thường cao gần 8 hàng, rộng khoảng 6 cột. Giữ tỷ lệ hình học.
    factor = min(48 / crop.width, 64 / crop.height)
    size = (max(1, min(48, round(crop.width*factor))), max(1, min(64, round(crop.height*factor))))
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("L", (64, 64), 0)
    canvas.paste(resized, ((64-size[0])//2, (64-size[1])//2))
    array = np.asarray(canvas, dtype=np.float64)
    row_grid, col_grid = np.indices(array.shape)
    center_y = float((row_grid*array).sum()/array.sum())
    center_x = float((col_grid*array).sum()/array.sum())
    occupied_y, occupied_x = np.where(array > 0)
    # Không cho phép dịch tâm làm mất nét ở biên.
    dx = int(np.clip(round(31.5-center_x), -occupied_x.min(), 63-occupied_x.max()))
    dy = int(np.clip(round(31.5-center_y), -occupied_y.min(), 63-occupied_y.max()))
    canvas = canvas.transform((64, 64), Image.Transform.AFFINE, (1, 0, -dx, 0, 1, -dy),
                              resample=Image.Resampling.BILINEAR, fillcolor=0)
    pixels = np.asarray(canvas.resize((8, 8), Image.Resampling.BOX), dtype=np.float64) * (16.0/255.0)
    pixels = np.clip(pixels, 0, 16)
    if np.count_nonzero(pixels) < 3:
        raise ValueError("Ảnh sau thu nhỏ không còn đủ nét chữ.")
    info = {"background": "Nền sáng → đảo nét" if light_background else "Nền tối → giữ nét sáng",
            "original_size": list(original_rgb.size), "crop_box": list(box),
            "center_shift": [dx, dy], "pixel_min": float(pixels.min()), "pixel_max": float(pixels.max())}
    return original_rgb, pixels, info


def predict_digit(pipeline, pixels):
    """Gọi nguyên Pipeline một lần cho mỗi API; không fit/scale lại dữ liệu đầu vào."""
    count = getattr(pipeline.steps[-1][1], "n_features_in_", None)
    side, maximum = (8, 16) if count == 64 else (28, 255) if count == 784 else (0, 0)
    pixels = np.asarray(pixels, dtype=np.float32 if count == 784 else float)
    if not side or pixels.shape != (side, side) or not np.isfinite(pixels).all() or pixels.min() < 0 or pixels.max() > maximum:
        raise ValueError(f"Đầu vào phải là ảnh {side}×{side}, giá trị hữu hạn trong 0–{maximum}.")
    features = pixels.reshape(1, count)
    names = getattr(pipeline, "feature_names_in_", None)
    if names is None:
        names = getattr(pipeline.steps[-1][1], "feature_names_in_", None)
    if names is not None:
        features = pd.DataFrame(features, columns=names)
    predicted = int(pipeline.predict(features)[0])
    probabilities = np.asarray(pipeline.predict_proba(features)[0], dtype=float)
    if not np.isfinite(probabilities).all() or (probabilities < 0).any() or not np.isclose(probabilities.sum(), 1):
        raise ValueError("Mô hình trả về xác suất không hợp lệ.")
    table = pd.DataFrame({"Chữ số": pipeline.classes_.astype(str), "Xác suất": probabilities}).set_index("Chữ số")
    return predicted, table


@st.cache_data(show_spinner=False)
def sample_digits():
    dataset = load_digits()
    return dataset.images, dataset.target


def saved_test_indices(registry):
    """Đọc đúng split của run trong registry; không chia lại hoặc chọn theo kết quả dự đoán."""
    run_id = registry.get("run_id", "") if registry else ""
    if not isinstance(run_id, str) or not run_id or any(c not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_" for c in run_id):
        raise ValueError("Thiếu mã thực nghiệm hợp lệ để đọc tập kiểm tra.")
    path = ROOT / "outputs" / run_id / "split_indices.csv"
    if not path.is_file():
        raise FileNotFoundError("Thiếu tệp split_indices.csv của lần thực nghiệm đã lưu. Không tự chia lại tập kiểm tra.")
    try:
        split = pd.read_csv(path)
        indices = split["sample_index"].to_numpy()
        valid = (len(split) == 1797 and np.issubdtype(indices.dtype, np.integer)
                 and np.array_equal(np.sort(indices), np.arange(1797))
                 and split["split"].isin(["train", "test"]).all()
                 and int((split["split"] == "test").sum()) == 360)
    except (KeyError, ValueError, OSError) as exc:
        raise ValueError("Không đọc được cách chia dữ liệu Digits đã lưu.") from exc
    if not valid:
        raise ValueError("Cách chia đã lưu không đúng cấu trúc Digits: 1.437 ảnh huấn luyện và 360 ảnh kiểm tra.")
    return indices[split["split"].to_numpy() == "test"]


def read_demo_summary(registry):
    """Thẻ tổng quan đọc từ run đã khóa, không lấy số minh họa hoặc chọn lại theo test."""
    run_id = registry.get("run_id", "")
    if not isinstance(run_id, str) or not run_id or any(c not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_" for c in run_id):
        raise ValueError("Mã run không hợp lệ để đọc thông tin tổng quan.")
    directory = ROOT / "outputs" / run_id
    data = json.loads((directory / "data_summary.json").read_text(encoding="utf-8"))
    lock = json.loads((directory / "selection_lock.json").read_text(encoding="utf-8"))
    selected = lock["selected_model"]
    if selected != registry["selected_model"] or selected not in MODEL_SHORT_NAMES:
        raise ValueError("Thông tin mô hình được chọn không khớp registry.")
    comparison = pd.read_csv(directory / "model_comparison.csv")
    accuracy = float(comparison.loc[comparison.model == selected, "accuracy"].item())
    if not np.isfinite(accuracy) or not 0 <= accuracy <= 1 or int(data["n_samples"]) <= 0:
        raise ValueError("Số liệu tổng quan không hợp lệ.")
    return {"n_samples": int(data["n_samples"]), "selected_model": selected, "accuracy": accuracy,
            "image_shape": list(data["images_shape"][1:]), "n_features": int(data["n_features"]),
            "pixel_min": data["pixel_min"], "pixel_max": data["pixel_max"]}


def model_parameter_rows(pipeline):
    """Thông số chỉ đọc từ estimator/scaler thật; không lấy tên chọn trong UI để đoán giá trị."""
    classifier = pipeline.steps[-1][1]
    params = classifier.get_params(deep=False)
    class_name = type(classifier).__name__
    algorithms = {"KNeighborsClassifier": "K-Nearest Neighbors (KNN)", "MLPClassifier": "Multilayer Perceptron (MLP)",
                  "LogisticRegression": "Logistic Regression"}
    rows = [("Thuật toán", algorithms.get(class_name, class_name))]
    fields = {"KNeighborsClassifier": [("Số láng giềng", "n_neighbors"), ("Trọng số", "weights"),
                                       ("Độ đo khoảng cách", "metric"), ("Bậc khoảng cách (p)", "p")],
              "MLPClassifier": [("Kiến trúc lớp ẩn", "hidden_layer_sizes"), ("Hàm kích hoạt", "activation"),
                                ("Thuật toán tối ưu", "solver"), ("Hệ số phạt (alpha)", "alpha"),
                                ("Dừng sớm", "early_stopping"), ("Số vòng lặp tối đa", "max_iter")],
              "LogisticRegression": [("C", "C"), ("Thuật toán tối ưu", "solver"), ("Dạng phạt", "penalty"),
                                     ("Số vòng lặp tối đa", "max_iter")]}
    for label, key in fields.get(class_name, []):
        value = params[key]
        if key == "hidden_layer_sizes" and isinstance(value, (tuple, list)):
            value = " → ".join(str(item) for item in value)
        elif isinstance(value, bool):
            value = "Có" if value else "Không"
        elif key == "weights" and isinstance(value, str):
            value = {"uniform": "Đồng đều", "distance": "Theo khoảng cách"}.get(value, value)
        rows.append((label, str(value)))
    scale = pipeline.named_steps.get("scale")
    raw = scale is None or isinstance(scale, str) and scale == "passthrough"
    rows.append(("Chuẩn hóa", "Không chuẩn hóa · điểm ảnh thô" if raw else type(scale).__name__))
    return rows


MODEL_LIMITS_TEXT = ("Mô hình được huấn luyện trên bộ dữ liệu Digits. Nên sử dụng ảnh chứa một chữ số, "
                     "nền đơn giản và nét viết rõ ràng. Độ chính xác có thể giảm đối với ảnh bên ngoài do "
                     "sự khác biệt về nét viết, kích thước và chất lượng ảnh. Xác suất dự đoán không bảo đảm "
                     "kết quả luôn đúng.")


def technical_information_html(summary, parameter_rows):
    """HTML ngữ nghĩa, chiều cao tự nhiên; không dùng repr/code block hoặc caption bị co chiều cao."""
    def table(rows, name):
        return (f'<table class="technical-table" aria-label="{escape(name)}"><tbody>' + ''.join(
            f'<tr><th scope="row">{escape(str(label))}</th><td>{escape(str(value))}</td></tr>'
            for label, value in rows) + '</tbody></table>')

    if summary:
        shape = "×".join(str(value) for value in summary["image_shape"])
        features = str(summary["n_features"])
        pixel_range = f'{summary["pixel_min"]:g}–{summary["pixel_max"]:g}'
        dataset_name = summary.get("dataset_name", "Digits · scikit-learn")
        if dataset_name == "MNIST train":
            dataset_name = "MNIST (tập huấn luyện)"
        dataset_rows = [("Bộ dữ liệu", dataset_name), ("Số lượng mẫu", f'{summary["n_samples"]:,}'.replace(",", ".")),
                        ("Kích thước ảnh", shape), ("Số đặc trưng", features), ("Miền điểm ảnh", pixel_range)]
        data_html = table(dataset_rows, "Thông tin dữ liệu")
        flow = (f'Ảnh tải lên → Chuyển thang xám và xử lý nền → Cắt vùng chữ, giữ tỷ lệ và căn giữa → Đổi kích thước {shape} '
                f'({pixel_range}) → {features} điểm ảnh theo hàng → Chuỗi xử lý và mô hình → Kết quả dự đoán')
        digits_note = (f'Ảnh mẫu và ảnh kiểm tra Digits giữ nguyên {features} điểm ảnh gốc, không cắt hoặc đổi kích thước lại. '
                       'Ảnh kiểm tra lấy từ cách chia đã lưu; minh họa sau khi xem tập kiểm tra không phải đánh giá độc lập mới.')
        if summary.get("dataset_name"):
            digits_note = ('Mô hình MNIST chỉ dùng cho ảnh tải lên. Ảnh mẫu và ảnh kiểm tra Digits tiếp tục dùng ba mô hình 8×8 chính thức. '
                           'Số mẫu trên là phần MNIST thực sự dùng để huấn luyện, không gồm tập xác thực bên ngoài.')
    else:
        data_html = '<p>Chưa đọc được thông tin dữ liệu đã lưu.</p>'
        flow = 'Chưa đọc được thông tin kích thước đầu vào.'
        digits_note = 'Ảnh mẫu và ảnh kiểm tra Digits giữ nguyên điểm ảnh gốc.'
    parameters_html = (table(parameter_rows, "Cấu hình mô hình đang chọn") if parameter_rows else
                       '<p>Chưa đọc được cấu hình mô hình đang chọn. Kiểm tra tệp mô hình và phiên bản thư viện.</p>')
    limits_text = MODEL_LIMITS_TEXT.replace("Digits", dataset_name) if summary and summary.get("dataset_name") else MODEL_LIMITS_TEXT
    return ('<div class="technical-info"><section class="technical-group"><h3>Thông tin dữ liệu</h3>'
            + data_html + '</section><section class="technical-group"><h3>Cấu hình mô hình</h3>'
            + parameters_html + '</section><section class="technical-group wide"><h3>Quy trình xử lý ảnh</h3>'
            + f'<div class="technical-flow">{escape(flow)}</div><p>{escape(digits_note)}</p>'
            + '<p>Ảnh tải lên còn được xoay theo thông tin hướng ảnh và ghép nền cho vùng trong suốt trước khi chuyển thang xám. '
              'Bộ chuẩn hóa chỉ chạy trong chuỗi xử lý của mô hình, không chuẩn hóa hai lần.</p></section>'
            + '<section class="technical-group wide technical-limits"><h3>Giới hạn mô hình</h3>'
            + f'<p>{escape(limits_text)}</p></section></div>')


SCAN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M8 3H5a2 2 0 0 0-2 2v3m13-5h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3m8 0h3a2 2 0 0 0 2-2v-3M8 12h8"/></svg>'

UI_STYLE = """
<style>
/* Chỉ dùng class riêng và một số test-id ổn định của Streamlit, không dùng class sinh ngẫu nhiên. */
[data-testid="stMainBlockContainer"] {max-width:1280px;padding:12px 24px;}
[data-testid="stHeader"] {height:0;background:transparent;}
[data-testid="stToolbar"] {display:none;}
.st-key-demo {background:#18181b;border:1px solid #343438;border-radius:12px;padding:20px;gap:12px;}
.st-key-demo [data-testid="stVerticalBlock"] {gap:8px;}
.st-key-demo p {margin-bottom:0;}
.st-key-demo [data-testid="stMarkdownContainer"] {margin-bottom:0;}
.st-key-demo [data-testid="stCaptionContainer"] {margin-bottom:0;}
.st-key-demo label p {color:#d4d4d8;font-size:13px;}
.st-key-demo button {font-weight:550;min-height:40px;transition:background .15s ease;}
.st-key-demo button[kind="primary"] {background:#2563eb;border-color:#2563eb;}
.st-key-demo button[kind="primary"]:hover {background:#3b82f6;border-color:#3b82f6;}
.st-key-demo button:focus-visible {outline:2px solid #93c5fd;outline-offset:3px;}
.st-key-demo [data-testid="stSelectbox"] [role="combobox"] {background:#18181b;min-width:0;flex:1 1 auto;cursor:pointer;}
.st-key-demo [data-testid="stSelectbox"] [role="combobox"][aria-expanded="true"] {cursor:text;}
.st-key-demo [data-testid="stSelectbox"] button[aria-haspopup="listbox"] {min-height:0;height:auto;align-self:stretch;cursor:pointer;}
.demo-header {display:flex;align-items:center;justify-content:space-between;gap:16px;padding-bottom:10px;border-bottom:1px solid #343438;}
.brand {display:flex;gap:12px;align-items:center;}
.brand-icon {width:25px;height:25px;color:#d4d4d8;flex-shrink:0;}
.brand h1 {font-size:26px;line-height:1.2;letter-spacing:-.4px;margin:0;padding:0;font-weight:650;}
.brand p {font-size:12px;color:#b5b5bf;margin:4px 0 0;}
.status-pill {white-space:nowrap;border:1px solid #175d39;background:#102c1f;color:#70dba0;font-size:11px;padding:4px 9px;border-radius:20px;}
.status-pill.offline {background:#29221a;border-color:#5e4425;color:#e3bd83;}
.status-dot {display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:5px;vertical-align:middle;}
.overview {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;}
.overview-card {background:#222225;border:1px solid #29292d;border-radius:10px;padding:8px 14px;min-height:64px;}
.overview-label {font-size:12px;color:#b5b5bf;line-height:1.4;}
.overview-value {font-size:20px;color:#f4f4f5;font-weight:600;line-height:1.5;letter-spacing:-.2px;}
.st-key-controls {padding:0;}
.st-key-sample_controls [data-testid="stHorizontalBlock"] {gap:12px;}
.section-heading {display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0;}
.section-heading h2 {font-size:17px;line-height:1.4;font-weight:600;margin:0;padding:0;}
.section-heading > span {font-size:12px;color:#b5b5bf;}
.st-key-workspace {border-top:1px solid #343438;padding-top:12px;}
.image-card {background:#101012;border:1px solid #2e2e33;border-radius:12px;height:240px;display:flex;justify-content:center;align-items:center;padding:12px;gap:12px;}
.preview {margin:0;min-width:0;text-align:center;flex:1;}
.preview img {display:block;width:212px;height:212px;max-width:100%;object-fit:contain;margin:auto;}
.preview img.pixel-grid {image-rendering:pixelated;image-rendering:crisp-edges;}
.preview figcaption {font-size:12px;color:#b5b5bf;margin-top:6px;}
.image-card.upload .preview img {width:176px;height:184px;}
.image-card.upload {gap:12px;}
.image-card.placeholder {color:#71717a;text-align:center;flex-direction:column;font-size:12px;}
.image-card.placeholder svg {width:36px;height:36px;opacity:.6;}
.image-meta {color:#b5b5bf;font-size:12px;line-height:1.5;margin:0;}
.result-card {background:#101012;border:1px solid #2e2e33;border-radius:12px;text-align:center;padding:8px 16px;}
.prediction-digit {font-size:88px;line-height:1;letter-spacing:-3px;font-weight:600;color:#60a5fa;}
.prediction-probability {color:#60a5fa;font-size:19px;font-weight:600;line-height:1.25;margin-top:3px;}
.prediction-model {font-size:12px;color:#b5b5bf;line-height:1.3;margin-top:4px;}
.prediction-match {font-size:12px;color:#70dba0;line-height:1.3;margin-top:3px;}
.prediction-match.incorrect {color:#e3bd83;}
.probability-title {font-size:13px;font-weight:600;margin:10px 0 8px;color:#d4d4d8;}
.probability-list {display:grid;gap:3px;}
.probability-row {display:grid;grid-template-columns:14px 1fr 54px;align-items:center;gap:9px;font-size:12px;line-height:14px;color:#c5c5cb;}
.probability-track {background:#303036;height:6px;border-radius:10px;overflow:hidden;}
.probability-fill {background:#71717a;height:100%;border-radius:10px;}
.probability-row.best {color:#f4f4f5;font-weight:600;}
.probability-row.best .probability-fill {background:#3b82f6;}
.probability-value {text-align:right;font-variant-numeric:tabular-nums;}
.result-empty {min-height:320px;background:#101012;border:1px dashed #343438;border-radius:12px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:24px;}
.result-empty svg {height:34px;width:34px;color:#71717a;margin-bottom:16px;}
.result-empty strong {font-size:16px;font-weight:600;color:#d4d4d8;}
.result-empty p {font-size:13px;color:#b5b5bf;max-width:280px;line-height:1.6;margin-top:7px;}
.workspace-footnote {font-size:12px;color:#b5b5bf;line-height:1.5;margin:0;}
.st-key-technical {margin-top:2px;}
.technical-info {display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;padding:4px 0;}
.technical-group {min-width:0;}
.technical-group h3 {font-size:16px;font-weight:600;line-height:1.5;margin:0 0 10px;color:#f4f4f5;}
.technical-group p {font-size:13px;line-height:1.65;margin:8px 0 0;color:#b5b5bf;overflow-wrap:anywhere;}
.technical-table {width:100%;border-collapse:collapse;table-layout:fixed;font-size:13px;line-height:1.55;}
.technical-table th,.technical-table td {padding:7px 10px;border-bottom:1px solid #343438;text-align:left;vertical-align:top;white-space:normal;overflow-wrap:anywhere;}
.technical-table th {width:46%;font-weight:500;color:#b5b5bf;}
.technical-table td {color:#f4f4f5;}
.technical-flow {font-size:13px;line-height:1.8;padding:10px 12px;background:#101012;border:1px solid #343438;border-radius:10px;overflow-wrap:anywhere;}
.technical-group.wide {grid-column:1 / -1;}
.technical-limits {color:#d4d4d8;}
@media (max-width:760px) {.technical-info {grid-template-columns:minmax(0,1fr);gap:18px;}}
@media (max-height:820px) and (min-width:761px) {
 [data-testid="stMainBlockContainer"] {padding-top:12px;}
 .st-key-demo {padding:20px;gap:10px;}
 .demo-header {padding-bottom:8px;}
 .st-key-demo [data-testid="stVerticalBlock"] {gap:8px;}
 .overview-card {padding:8px 12px;}
 .brand h1 {font-size:25px;}
 .image-card {height:228px;}
 .preview img {width:200px;height:200px;}
 .image-card.upload .preview img {height:160px;}
 .image-card.upload {height:216px;}
 .result-empty {min-height:300px;}
 .probability-list {gap:2px;}
 .prediction-digit {font-size:80px;}
}
@media (max-width:760px) {
 [data-testid="stMainBlockContainer"] {padding:12px;}
 .st-key-demo {padding:16px;}
 .brand h1 {font-size:20px;}
 .brand p {font-size:10px;}
 .status-pill {font-size:10px;}
 .overview-card {padding:9px 10px;}
 .overview-label {font-size:11px;}
 .overview-value {font-size:17px;}
 .st-key-workspace [data-testid="stHorizontalBlock"] {flex-direction:column;}
 .st-key-workspace [data-testid="stColumn"] {width:100%;flex:1 1 100%;}
 .image-card {height:248px;}
 .preview img {height:220px;width:220px;}
 .result-empty {min-height:300px;}
}
@media (max-height:740px) and (min-width:761px) {
 [data-testid="stMainBlockContainer"] {padding-top:6px;padding-bottom:6px;}
 .st-key-demo {gap:8px;}
 .st-key-demo [data-testid="stVerticalBlock"] {gap:6px;}
 .demo-header {padding-bottom:6px;}
 .st-key-workspace {padding-top:8px;}
 .result-card {padding-top:6px;padding-bottom:6px;}
 .probability-title {margin-top:8px;margin-bottom:6px;}
 .result-empty {min-height:280px;}
 .image-card.upload {height:200px;}
 .image-card.upload .preview img {height:148px;}
}
@media (max-width:480px) {
 .demo-header {align-items:flex-start;}
 .brand {gap:8px;}
 .brand-icon {width:20px;height:20px;margin-top:2px;}
 .status-pill {padding:3px 6px;}
 .status-pill .status-dot {display:none;}
 .st-key-controls [data-testid="stHorizontalBlock"] {flex-direction:column;}
 .st-key-controls [data-testid="stColumn"] {width:100%;flex:1 1 100%;}
 .overview {gap:6px;}
 .overview-label {font-size:9px;}
 .overview-value {font-size:13px;}
}
</style>
"""


def preview_image_html(image, caption="", pixel_grid=False):
    """Chỉ tạo ảnh hiển thị; không thay mảng pixel đưa vào Pipeline."""
    if not isinstance(image, Image.Image):
        image = Image.fromarray(np.asarray(image, dtype=np.uint8))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    css_class = "pixel-grid" if pixel_grid else ""
    return (f'<figure class="preview"><img class="{css_class}" src="data:image/png;base64,{encoded}" '
            f'alt="{escape(caption or "Ảnh chữ số")}"><figcaption>{escape(caption)}</figcaption></figure>')


def prediction_html(result, actual_label):
    """Kết quả và 10 thanh ngang lấy trực tiếp từ predict/predict_proba."""
    predicted = result["predicted"]
    probability = result["probabilities"][result["classes"].index(str(predicted))]
    match = ""
    if actual_label is not None:
        correct = predicted == actual_label
        text = f'{"Đúng" if correct else "Sai"} · nhãn gốc {actual_label}'
        match = f'<div class="prediction-match {"" if correct else "incorrect"}">{text}</div>'
    percent = f"{probability:.2%}".replace(".", ",")
    html = (f'<div class="result-card" role="status" data-prediction="{predicted}">'
            f'<div class="prediction-digit">{predicted}</div><div class="prediction-probability">{percent}</div>'
            f'<div class="prediction-model">Xác suất ảnh này · {escape(MODEL_SHORT_NAMES[result["model"]])}</div>{match}</div>'
            '<div class="probability-title">Phân bố xác suất · 10 chữ số</div><div class="probability-list">')
    pairs = sorted(zip(result["classes"], result["probabilities"]), key=lambda pair: (-pair[1], int(pair[0])))
    for label, value in pairs:
        percent = f"{value:.2%}".replace(".", ",")
        best = " best" if label == str(predicted) else ""
        html += (f'<div class="probability-row{best}" data-label="{label}" aria-label="Chữ số {label}: {percent}">'
                 f'<span>{label}</span><div class="probability-track"><div class="probability-fill" '
                 f'style="width:{min(100, value*100):.6f}%"></div></div><span class="probability-value">{percent}</span></div>')
    return html + '</div>'


def main():
    st.set_page_config(page_title="Nhận diện chữ số", page_icon="✍️", layout="wide")
    st.html(UI_STYLE)
    registry, registry_error, summary = None, None, None
    try:
        registry = read_model_registry()
    except (FileNotFoundError, ValueError) as exc:
        registry_error = str(exc)
    if registry:
        try:
            summary = read_demo_summary(registry)
        except (OSError, ValueError, KeyError) as exc:
            registry_error = f"Chưa đọc được thông tin tổng quan: {exc}"
    external_config, external_error = None, None
    try:
        external_config = read_external_registry()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        external_error = f"Chưa dùng được cấu hình ảnh ngoài: {exc}"

    with st.container(key="demo"):
        files_present = registry and all((MODEL_DIR / item["path"]).is_file() for item in registry["models"].values())
        status = "Mô hình đã lưu" if files_present else "Thiếu mô hình"
        st.markdown(f'<header class="demo-header"><div class="brand"><div class="brand-icon">{SCAN_ICON}</div>'
                    '<div><h1>Nhận diện chữ số viết tay</h1><p>Ứng dụng minh họa · Đề tài 13</p></div></div>'
                    f'<span class="status-pill {"" if files_present else "offline"}"><span class="status-dot"></span>{status}</span></header>',
                    unsafe_allow_html=True)
        if summary:
            best_name = MODEL_SHORT_NAMES[summary["selected_model"]]
            cards = [("Bộ dữ liệu Digits", f'{summary["n_samples"]:,} ảnh'.replace(",", ".")),
                     ("Tốt nhất qua kiểm định chéo", best_name),
                     (f"Độ chính xác kiểm tra · {best_name}", f'{summary["accuracy"]:.2%}'.replace(".", ","))]
        else:
            cards = [("Bộ dữ liệu Digits", "—"), ("Tốt nhất qua kiểm định chéo", "—"), ("Độ chính xác kiểm tra", "—")]
        st.markdown('<div class="overview">' + ''.join(
            f'<div class="overview-card"><div class="overview-label">{escape(label)}</div>'
            f'<div class="overview-value">{escape(value)}</div></div>' for label, value in cards) + '</div>', unsafe_allow_html=True)
        if registry_error:
            st.warning(registry_error)
        if external_error:
            st.warning(external_error)

        with st.container(key="controls"):
            model_column, source_column = st.columns(2, gap="medium")
            options = list(registry["models"]) if registry else []
            if options and st.session_state.get("source") == "Tải ảnh từ máy" and external_config and external_config["specialist_enabled"]:
                options.append("mlp_mnist")
            if options and st.session_state.get("model", registry["selected_model"]) not in options:
                st.session_state["model"] = registry["selected_model"]
            with model_column:
                model_name = st.selectbox("Mô hình phân loại", options, index=options.index(registry["selected_model"]),
                    format_func=lambda name: MODEL_NAMES.get(name, EXTERNAL_MODEL_NAME), key="model") if options else None
                if not options:
                    st.selectbox("Mô hình phân loại", ["Chưa có mô hình đã lưu"], disabled=True)
            with source_column:
                source = st.selectbox("Nguồn ảnh", ["Ảnh test Digits", "Ảnh mẫu Digits", "Tải ảnh từ máy"],
                                      index=0 if registry else 1, key="source",
                                      format_func=lambda value: "Ảnh kiểm tra Digits" if value == "Ảnh test Digits" else value)

        with st.container(key="workspace"):
            left, right = st.columns(2, gap="medium")
            side, pixel_maximum = (28, 255) if model_name == "mlp_mnist" else (8, 16)
            with left:
                st.markdown(f'<div class="section-heading"><h2>Ảnh đầu vào</h2><span>{side} × {side} điểm ảnh · 0–{pixel_maximum}</span></div>', unsafe_allow_html=True)
                pixels, original, actual_label, info = None, None, None, {}
                image_meta, upload_data, index, background = "", None, None, None
                if source in {"Ảnh mẫu Digits", "Ảnh test Digits"}:
                    images, labels = sample_digits()
                    test_mode = source == "Ảnh test Digits"
                    try:
                        available = saved_test_indices(registry) if test_mode else np.arange(len(labels))
                        with st.container(key="sample_controls"):
                            label_column, id_column = st.columns([1, 2], gap="small", vertical_alignment="bottom")
                            label = label_column.selectbox("Chữ số mẫu", list(range(10)), key="sample_label")
                            indices = available[labels[available] == label].astype(int).tolist()
                            key = f"test_sample_{label}" if test_mode else f"sample_{label}"
                            index = id_column.selectbox("Mã ảnh trong Digits", options=indices, index=0, key=key)
                        pixels = images[index].copy()
                        original = np.uint8(np.rint(pixels * 255/16))
                        actual_label = int(labels[index])
                        subset = "Tập kiểm tra chính thức" if test_mode else "Toàn bộ Digits · gồm tập huấn luyện và kiểm tra"
                        image_meta = f"{subset} · Mã ảnh {index} · Nhãn {actual_label} · 8×8"
                    except (FileNotFoundError, ValueError) as exc:
                        st.error(str(exc))
                else:
                    with st.container(key="upload_controls"):
                        file_column, background_column = st.columns([2, 1], gap="medium")
                        with file_column:
                            upload = st.file_uploader("Tải ảnh chữ số · PNG, JPG, BMP, WebP · tối đa 10 MB",
                                type=["png", "jpg", "jpeg", "bmp", "webp"], max_upload_size=10, key="upload")
                        background = background_column.selectbox("Màu nền", BACKGROUND_OPTIONS, key="background")
                    if upload is not None:
                        upload_data = upload.getvalue()
                        try:
                            original, pixels, info = preprocess_upload_for_model(upload_data, background, model_name, external_config)
                            image_meta = f'{original.width}×{original.height} → {side}×{side} · {info["background"]}'
                        except ValueError as exc:
                            st.error(str(exc))

                entry = (external_config["specialist"] if model_name == "mlp_mnist" else registry["models"][model_name]) if model_name else None
                context_data = [model_name, entry["sha256"] if entry else None, source, index, background,
                                external_config["shared_variant"] if external_config and source == "Tải ảnh từ máy" else None,
                                hashlib.sha256(upload_data).hexdigest() if upload_data is not None else None]
                context = hashlib.sha256(json.dumps(context_data).encode() + (pixels.tobytes() if pixels is not None else b"")).hexdigest()
                if st.session_state.get("prediction_context") != context:
                    st.session_state.pop("prediction_result", None)
                    st.session_state["prediction_context"] = context
                if pixels is None:
                    st.markdown(f'<div class="image-card placeholder">{SCAN_ICON}<span>Chọn ảnh chỉ chứa một chữ số rõ nét</span></div>', unsafe_allow_html=True)
                elif source == "Tải ảnh từ máy":
                    processed = np.uint8(np.rint(pixels * 255/pixel_maximum))
                    st.markdown('<div class="image-card upload">' + preview_image_html(original, "Ảnh gốc")
                                + preview_image_html(processed, f"Sau tiền xử lý · {side}×{side}", True) + '</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="image-card">' + preview_image_html(original, "", True) + '</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="image-meta">{escape(image_meta or "Nền đơn giản, tương phản rõ; tránh nhiều ký tự hoặc bóng đổ.")}</div>', unsafe_allow_html=True)
                if st.button("Nhận diện chữ số", key="predict", type="primary", width="stretch",
                             icon=":material/center_focus_strong:", disabled=model_name is None or pixels is None):
                    st.session_state.pop("prediction_result", None)
                    try:
                        with st.spinner("Đang nhận diện…"):
                            path = (MODEL_DIR / entry["path"]).resolve()
                            if not path.is_file():
                                raise FileNotFoundError("Thiếu tệp mô hình đã chọn. Khôi phục đúng thư mục models/ đã lưu.")
                            stat = path.stat()
                            pipeline = load_saved_pipeline(str(path), entry["sha256"], stat.st_mtime_ns, stat.st_size, side*side)
                            predicted, probabilities = predict_digit(pipeline, pixels)
                            st.session_state["prediction_result"] = {"context": context, "model": model_name,
                                "predicted": predicted, "classes": probabilities.index.tolist(),
                                "probabilities": probabilities["Xác suất"].tolist()}
                    except Exception as exc:
                        st.error(f"Không thể dự đoán: {exc}")
            with right:
                st.markdown('<div class="section-heading"><h2>Kết quả dự đoán</h2><span>Mô hình đã huấn luyện</span></div>', unsafe_allow_html=True)
                result = st.session_state.get("prediction_result")
                if result:
                    st.markdown(prediction_html(result, actual_label), unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-empty">{SCAN_ICON}<strong>Sẵn sàng nhận diện</strong>'
                                '<p>Chọn ảnh và mô hình, sau đó nhấn <b>Nhận diện chữ số</b> để xem kết quả và xác suất.</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="workspace-footnote">Xác suất chưa hiệu chỉnh; giá trị cao không bảo đảm đúng trên ảnh ngoài Digits.</div>', unsafe_allow_html=True)

        with st.expander("Thông tin mô hình và quy trình xử lý ảnh", key="technical"):
            parameter_rows = None
            if model_name:
                try:
                    path = MODEL_DIR / entry["path"]
                    stat = path.stat()
                    pipeline = load_saved_pipeline(str(path), entry["sha256"], stat.st_mtime_ns, stat.st_size, side*side)
                    parameter_rows = model_parameter_rows(pipeline)
                except Exception:
                    pass  # Giữ phần thông tin đọc được và báo chưa có Pipeline trong bảng.
            technical_summary = summary
            if model_name == "mlp_mnist":
                technical_summary = {"dataset_name": external_config["specialist"]["dataset"],
                    "n_samples": external_config["specialist"]["train_n"], "image_shape": [side, side],
                    "n_features": side*side, "pixel_min": 0, "pixel_max": pixel_maximum}
            st.html(technical_information_html(technical_summary, parameter_rows))



if __name__ == "__main__":
    main()
