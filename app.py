"""Demo Digits: chỉ đọc Pipeline đã lưu; không fit hoặc tuning trong ứng dụng."""
from io import BytesIO
from pathlib import Path
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

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "models"
MODEL_NAMES = {"logreg_raw": "Logistic Regression — pixel thô", "knn": "K láng giềng gần nhất (KNN)",
               "mlp": "Mạng nơ-ron nhiều lớp (MLP)"}
BACKGROUND_OPTIONS = ["Tự động", "Nền sáng, nét tối", "Nền tối, nét sáng"]
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000


def read_model_registry(model_dir=None):
    """Manifest cố định; không tự tìm model có điểm test cao nhất hoặc file mới nhất."""
    model_dir = Path(model_dir) if model_dir is not None else MODEL_DIR
    path = model_dir / "registry.json"
    if not path.is_file():
        raise FileNotFoundError("Chưa có models/registry.json. Cần xuất Pipeline từ notebook trước khi dự đoán.")
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
def load_saved_pipeline(path_text, expected_sha256, modified_ns, file_size):
    """Cache theo file/hash/mtime/size; chỉ load artifact local tin cậy của project."""
    path = Path(path_text)
    if not path.is_file():
        raise FileNotFoundError("Thiếu file Pipeline đã chọn. Khôi phục đúng bộ models/ đã xuất.")
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError("File mô hình không khớp mã kiểm tra trong registry. Không sử dụng file này.")
    with warnings.catch_warnings():
        # Cảnh báo sai phiên bản sklearn được chuyển thành lỗi dễ xử lý trong giao diện.
        from sklearn.exceptions import InconsistentVersionWarning
        warnings.simplefilter("error", InconsistentVersionWarning)
        pipeline = joblib.load(path)
    if not isinstance(pipeline, Pipeline) or not callable(getattr(pipeline, "predict_proba", None)):
        raise ValueError("File phải chứa toàn bộ Pipeline có predict_proba.")
    check_is_fitted(pipeline)
    classifier = pipeline.steps[-1][1]
    # sklearn 1.7 không chuyển tiếp n_features_in_ qua bước đầu là chuỗi passthrough.
    if getattr(classifier, "n_features_in_", None) != 64 or not np.array_equal(pipeline.classes_, np.arange(10)):
        raise ValueError("Pipeline phải nhận 64 pixel và phân loại đủ các nhãn 0–9.")
    return pipeline


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
    pixels = np.asarray(pixels, dtype=float)
    if pixels.shape != (8, 8) or not np.isfinite(pixels).all() or pixels.min() < 0 or pixels.max() > 16:
        raise ValueError("Đầu vào phải là ảnh 8×8, giá trị hữu hạn trong 0–16.")
    features = pixels.reshape(1, 64)
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
        raise ValueError("Thiếu mã run hợp lệ để đọc tập test.")
    path = ROOT / "outputs" / run_id / "split_indices.csv"
    if not path.is_file():
        raise FileNotFoundError("Thiếu split_indices.csv của run đã lưu. Không tự chia lại tập test.")
    try:
        split = pd.read_csv(path)
        indices = split["sample_index"].to_numpy()
        valid = (len(split) == 1797 and np.issubdtype(indices.dtype, np.integer)
                 and np.array_equal(np.sort(indices), np.arange(1797))
                 and split["split"].isin(["train", "test"]).all()
                 and int((split["split"] == "test").sum()) == 360)
    except (KeyError, ValueError, OSError) as exc:
        raise ValueError("Không đọc được split Digits đã lưu.") from exc
    if not valid:
        raise ValueError("Split đã lưu không đúng cấu trúc Digits 1.437 train / 360 test.")
    return indices[split["split"].to_numpy() == "test"]


def main():
    st.set_page_config(page_title="Nhận dạng chữ số", page_icon="✍️", layout="centered")
    st.title("Nhận dạng chữ số viết tay")
    st.caption("Đồ án đề tài 13 · Digits 8×8 · Logistic Regression, KNN và MLP")
    registry = None
    try:
        registry = read_model_registry()
    except (FileNotFoundError, ValueError) as exc:
        st.warning(str(exc))
    options = list(registry["models"]) if registry else []
    if options:
        model_name = st.selectbox("Mô hình", options, index=options.index(registry["selected_model"]),
                                  format_func=lambda name: MODEL_NAMES[name], key="model")
    else:
        model_name = None
        st.selectbox("Mô hình", ["Chưa có Pipeline đã lưu"], disabled=True)
    source = st.radio("Chọn nguồn ảnh", ["Ảnh mẫu Digits", "Ảnh test Digits", "Tải ảnh từ máy"], horizontal=True, key="source")
    pixels, original, actual_label, info = None, None, None, {}
    if source in {"Ảnh mẫu Digits", "Ảnh test Digits"}:
        images, labels = sample_digits()
        test_mode = source == "Ảnh test Digits"
        try:
            available = saved_test_indices(registry) if test_mode else np.arange(len(labels))
            label = st.selectbox("Chữ số mẫu", list(range(10)), key="sample_label")
            indices = available[labels[available] == label].astype(int).tolist()
            key = f"test_sample_{label}" if test_mode else f"sample_{label}"
            index = st.select_slider("Mã ảnh trong Digits", options=indices, value=indices[0], key=key)
            pixels = images[index].copy()
            original = np.uint8(np.rint(pixels * 255/16))
            actual_label = int(labels[index])
            info = {"background": "Mẫu Digits: giữ nguyên 64 pixel gốc, không crop hoặc chuẩn hóa lại"}
            scope = f"Tập test đã lưu · run {registry['run_id']}" if test_mode else "Mẫu có thể thuộc train hoặc test"
            st.caption(f"Nhãn gốc: {actual_label}. {scope}; minh họa này không phải một lần đánh giá độc lập mới.")
        except (FileNotFoundError, ValueError) as exc:
            st.error(str(exc))
    else:
        st.info("Chọn ảnh chỉ chứa một chữ số, nét rõ, nền đơn giản; tránh ảnh nghiêng, bóng đổ hoặc nhiều ký tự.")
        upload = st.file_uploader("Ảnh chữ số (tối đa 10 MB)", type=["png", "jpg", "jpeg", "bmp", "webp"],
                                  max_upload_size=10)
        background = st.selectbox("Màu nền", BACKGROUND_OPTIONS, key="background")
        if upload is not None:
            try:
                original, pixels, info = preprocess_uploaded_image(upload.getvalue(), background)
            except ValueError as exc:
                st.error(str(exc))
        else:
            st.caption("Ảnh gốc và ảnh sau tiền xử lý sẽ xuất hiện ở đây.")
    if pixels is not None:
        left, right = st.columns(2)
        with left:
            st.image(original, caption="Ảnh gốc", width=250, clamp=True)
        with right:
            st.image(pixels/16, caption="Ảnh đầu vào 8×8 · pixel 0–16", width=250, clamp=True)
        st.caption(info["background"])
    if st.button("Dự đoán", type="primary", disabled=model_name is None or pixels is None):
        try:
            entry = registry["models"][model_name]
            path = (MODEL_DIR / entry["path"]).resolve()
            if not path.is_file():
                raise FileNotFoundError("Thiếu file Pipeline đã chọn. Khôi phục đúng bộ models/ đã xuất.")
            stat = path.stat()
            pipeline = load_saved_pipeline(str(path), entry["sha256"], stat.st_mtime_ns, stat.st_size)
            predicted, probabilities = predict_digit(pipeline, pixels)
            confidence = float(probabilities.loc[str(predicted), "Xác suất"])
            left, right = st.columns(2)
            left.metric("Chữ số dự đoán", str(predicted))
            right.metric("Xác suất mô hình", f"{confidence:.1%}")
            st.bar_chart(probabilities, height=260)
            if actual_label is not None:
                if predicted == actual_label:
                    st.success("Dự đoán khớp nhãn của ảnh mẫu.")
                else:
                    st.warning(f"Dự đoán khác nhãn mẫu {actual_label}.")
        except Exception as exc:
            st.error(f"Không thể dự đoán: {exc}")
    st.caption("Xác suất chưa được hiệu chỉnh; giá trị cao không bảo đảm đúng trên ảnh ngoài Digits. Demo không tự huấn luyện mô hình.")


if __name__ == "__main__":
    main()
