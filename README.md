# Phân loại chữ số viết tay — đề tài 13

[Repository GitHub](https://github.com/shengs1/HandwrittenDigitRecognition) · Python 3.12 · Digits · Streamlit.

**Final review trước bảo vệ:** [bảng PASS/FAIL/PARTIAL và lỗi còn mở](docs/FINAL_REVIEW.md). Sau sửa, 31/31 test và notebook đã chạy lại trên checkout sạch/venv mới; metric và dự đoán khớp bộ đã khóa. Nhận định của nhóm, báo cáo và slide chính thức vẫn cần hoàn thiện.

Bản tổng hợp theo cấu trúc A–I: [FINAL_AUDIT.md](docs/FINAL_AUDIT.md).

Notebook `digit_classification.ipynb` là tài liệu thực nghiệm chính, gồm 16 mục: dữ liệu/làm sạch, 6 EDA train, baseline Logistic Regression pixel thô, KNN/MLP bằng Pipeline, đối chứng chuẩn hóa, CV/tuning, đánh giá, phân tích lỗi và lưu mô hình. `app.py` là demo tiếng Việt, chỉ tải Pipeline đã lưu; mở app **không huấn luyện lại**.

## Kết quả đã chạy

Bộ mô hình cố định: `models/registry.json`, run `20261117T081201Z_fd32180f`. Dữ liệu huấn luyện duy nhất là `sklearn.datasets.load_digits()`: 1.797 ảnh 8×8, 64 pixel, nhãn 0–9, giá trị 0–16. Train/test 80/20, stratify=y, seed 42; 1.437/360 mẫu. Scaler chỉ fit trong Pipeline theo fold.

| Mô hình | CV macro F1 mean ± std | Accuracy test | Macro F1 test |
|---|---:|---:|---:|
| Logistic Regression pixel thô | 0.963687 ± 0.007866 | 0.958333 | 0.958075 |
| KNN | 0.976170 ± 0.007575 | 0.966667 | 0.966304 |
| MLP | 0.962365 ± 0.008314 | 0.961111 | 0.960888 |

Nguồn: [model_comparison.csv](outputs/20261117T081201Z_fd32180f/model_comparison.csv), std theo ddof=0. **KNN được chọn theo CV trước test.** CV sau tuning có thiên lệch lựa chọn; không phải ước lượng độc lập. Không điều chỉnh mô hình vì điểm test hoặc ảnh demo.

## Cài môi trường trên Windows PowerShell

Nếu chưa có mã nguồn:

```powershell
git clone https://github.com/shengs1/HandwrittenDigitRecognition.git
cd HandwrittenDigitRecognition
```

Từ thư mục gốc project, dùng Python 3.12 đã cài:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Không cần activate hoặc thay ExecutionPolicy. Nếu `py`/`python` là alias Microsoft Store bị lỗi, thay `py -3.12` bằng đường dẫn Python thật. Với môi trường tạo bằng `uv` không có pip, dùng `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`. Không chép `.venv` sang máy khác. requirements ghim các thư viện trực tiếp đã kiểm tra; môi trường thực nghiệm tại `outputs/<run_id>/environment.json`.

## Chạy demo

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Mở [http://localhost:8501](http://localhost:8501). Chọn mô hình, chọn ảnh mẫu Digits hoặc tải PNG/JPEG/BMP/WebP từ máy, xem ảnh gốc/ảnh 8×8 rồi bấm **Dự đoán**. Bảng xác suất có đủ 10 chữ số. Model mặc định là KNN đã chọn bằng CV.

Ảnh Digits giữ đúng pixel gốc. Ảnh tải lên: đọc hướng EXIF, grayscale/ghép alpha, nhận biết nền từ viền (hoặc chọn màu nền), lấy vùng nét, giữ tỷ lệ, căn giữa và thu nhỏ về 8×8, đổi miền về 0–16. Không gọi StandardScaler bên ngoài Pipeline. Giới hạn file 10 MB, 16 triệu pixel; file hỏng, ảnh trống và thiếu model được báo trong giao diện.

Registry trỏ đến đúng run và checksum của cả Pipeline. Giữ toàn bộ `models/<run_id>/`; không chỉ copy estimator. Nếu thiếu registry/model, khôi phục từ bản đã xác nhận trong Git; app không tự fit để bù. Chỉ sử dụng joblib do project tin cậy. Khi sai phiên bản sklearn, cài đúng requirements.

## Mở và chạy notebook

```powershell
.\.venv\Scripts\python.exe -m notebook digit_classification.ipynb
```

Chọn kernel `.venv`. Notebook đã có output thật; **không cần Run All để dùng demo**. Khi chủ động tái lập thí nghiệm, Restart Kernel/Run All, hoặc:

```powershell
.\.venv\Scripts\python.exe -X utf8 tests/run_notebook.py
```

`RUN_EXPERIMENTS=True` thực hiện CV/grid/learning curve/fit cuối và tạo run mới. Đổi thành False nếu chỉ cần dữ liệu/EDA. Mỗi run có thư mục riêng, không ghi đè; registry đang có không tự thay bằng run mới. Không chạy lại để tìm seed hoặc điểm tốt hơn, không dùng test tuning.

## Kiểm thử và giới hạn

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe -X utf8 tests/check_demo.py
```

Test kiểm tra miền pixel, leakage, notebook, ảnh sáng/tối/trong suốt/trống/hỏng, checksum/mất model, xác suất, khớp 360 dự đoán test đã lưu và luồng Streamlit. `check_demo.py` chỉ suy luận, tạo thư mục `outputs/demo_...` với CSV/ảnh xử lý/báo cáo checksum, không fit hoặc thay model.

Ở Phase 2 đã cài môi trường mới: 120 gói tương thích và 25/25 test đạt ([log cũ](outputs/demo_20261117T082316Z_b269f12c/tests_clean_environment.log)). Final review bổ sung kiểm tra khoa học dữ liệu và sửa điều kiện checkout mới: **31/31 test đạt**, [log mới](outputs/review_20261117T090347Z_9df57e69/clean_checkout_tests.log), [môi trường mới](outputs/review_20261117T090347Z_9df57e69/clean_environment.json), [đối chiếu rerun](outputs/review_20261117T090347Z_9df57e69/review_checks.json). Ảnh chọn mẫu/upload đã thử ở Phase 2: [giao diện](outputs/demo_20261117T082316Z_b269f12c/streamlit_demo.jpg).

[Bằng chứng kiểm thử ảnh](outputs/demo_20261117T082316Z_b269f12c/demo_verification.json): 10 ảnh mẫu Digits (ảnh đầu mỗi lớp), LR đúng 10/10, KNN và MLP đúng 9/10. Với 10 ảnh viết tay MNIST bên ngoài, cả ba đúng 3/10. Đây là minh họa rất nhỏ, **không phải accuracy tổng quát trên ảnh ngoài Digits**. Mẫu Digits có thể thuộc train. MNIST chỉ là fixture suy luận, không đổi dataset huấn luyện. Chưa thử ảnh tự chụp của nhóm. Xác suất cao vẫn có thể sai, chưa hiệu chỉnh. Không tối ưu lại sau các kết quả này.

## File và tài liệu báo cáo

| Đường dẫn | Mục đích |
|---|---|
| `digit_classification.ipynb` | Thực nghiệm và hình/bảng gốc |
| `app.py` | Demo và xử lý ảnh/tải Pipeline/suy luận |
| `models/registry.json`, `models/<run_id>/` | Bộ mô hình cố định |
| `outputs/<run_id>/` | CV/test, thời gian, report, lỗi, curves, EDA |
| `tests/` | Kiểm thử và fixture bên ngoài có nguồn |
| `docs/REPORT_OUTLINE.md` | Dàn ý báo cáo đúng 10 mục PDF |
| `docs/RESULTS_INDEX.md` | Bảng số liệu và chỉ mục hình có nguồn |
| `docs/SLIDE_OUTLINE.md` | Dàn ý 12 slide |
| `docs/VIVA_QUESTIONS.md` | Câu hỏi vấn đáp và thao tác code |
| `AGENTS.md`, `HANDOFF.md` | Quyết định và trạng thái chuyển giao |

Nhóm tự viết nhận định EDA/nội dung phân tích chính, hoàn thành báo cáo/slide, phân công thật và tập bảo vệ. Nguồn: [PDF đồ án](docs/Huong_Dan_Do_An_CuoiKy.pdf), [đối chiếu yêu cầu](docs/REQUIREMENTS_MAP.md).
