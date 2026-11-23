# Phân loại chữ số viết tay — đề tài 13

[GitHub](https://github.com/shengs1/HandwrittenDigitRecognition) · Python 3.12 · scikit-learn · Streamlit

Cập nhật tài liệu: **23/11/2026**. Mã ứng dụng hiện tại dựa trên commit `f47a709`: tên mô hình bằng tiếng Anh; nhãn, chú thích và hướng dẫn trên giao diện bằng tiếng Việt.

**UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Phần kỹ thuật đã được kiểm thử; nhóm vẫn cần xác nhận nhận định, hoàn thiện báo cáo/slide, thông tin thành viên, phân công và chuẩn bị bảo vệ. Không huấn luyện hoặc tuning thêm để làm đẹp kết quả demo.

## Hai phần của dự án

| Phần | Dữ liệu và phương pháp | Vai trò |
|---|---|---|
| A — Thực nghiệm chính | Digits 1.797 ảnh 8×8; Logistic Regression trên điểm ảnh thô, K-Nearest Neighbors (KNN), Multilayer Perceptron (MLP) | Trả lời yêu cầu và năm câu hỏi đề tài 13; KNN được chọn bằng kiểm định chéo |
| B — Mở rộng ảnh ngoài | So sánh tiền xử lý upload; một MLP riêng học MNIST 28×28; đánh giá thêm ba nguồn chữ viết tay | Cải thiện demo ảnh ngoài, giữ nguyên mô hình và số liệu phần A |

Notebook `digit_classification.ipynb` gồm 16 mục là tài liệu thực nghiệm chính của phần A. Phần B ở [báo cáo mở rộng](outputs/external_optimization_20261118T175401Z_4ca3a08f/REPORT.md). [Chỉ mục kết quả](docs/RESULTS_INDEX.md) tập hợp nguồn CSV/JSON và hình cho cả hai phần.

## Kết quả chính trên Digits

Nguồn: [model_comparison.csv](outputs/20261117T081201Z_fd32180f/model_comparison.csv). Chia 1.437 ảnh huấn luyện/360 ảnh kiểm tra, `stratify=y`, `random_state=42`; kiểm định chéo phân tầng 5 phần, có xáo trộn, seed 42. Scaler chỉ học bên trong Pipeline của tập huấn luyện mỗi phần.

| Mô hình | Macro F1 kiểm định chéo: mean ± std | Độ chính xác kiểm tra | Macro F1 kiểm tra |
|---|---:|---:|---:|
| Logistic Regression — điểm ảnh thô | 0,963687 ± 0,007866 | 95,8333% | 0,958075 |
| K-Nearest Neighbors (KNN) | **0,976170 ± 0,007575** | **96,6667%** | **0,966304** |
| Multilayer Perceptron (MLP) | 0,962365 ± 0,008314 | 96,1111% | 0,960888 |

KNN được khóa theo macro F1 kiểm định chéo trước khi xem tập kiểm tra. Độ lệch chuẩn dùng `ddof=0`; điểm kiểm định chéo sau tuning có thiên lệch lựa chọn, không phải đánh giá độc lập. Bộ mô hình chính thức: `models/registry.json`, run `20261117T081201Z_fd32180f`.

## Kết quả mở rộng ảnh ngoài

Chọn `gray_bbox` bằng macro F1 trung bình của ba Pipeline Digits trên 300 ảnh xác thực ngoài: **0,59260**, so với **0,48980** của cách xử lý cũ. Một MLP MNIST dùng MinMaxScaler, lớp ẩn `(128,64)`, seed 42, dừng sớm; học từ 54.000 ảnh MNIST, giữ 6.000 ảnh xác thực ngoài. Không dùng 600 ảnh ba nguồn mới để huấn luyện.

| Hệ thống đã khóa trước kiểm tra | Độ chính xác MNIST 9.890 ảnh | Độ chính xác ngoài 300 ảnh | Macro F1 ngoài |
|---|---:|---:|---:|
| KNN + xử lý cũ | 41,9312% | 48,0000% | 0,490304 |
| KNN + gray_bbox | 47,0677% | 58,0000% | 0,573268 |
| MLP MNIST28 | 97,3913% | 87,3333% | 0,871326 |

Nguồn: [bảng cuối của bảy hệ thống](outputs/external_optimization_20261118T175401Z_4ca3a08f/final_test/metrics.csv). MLP MNIST28 đúng 9.632/9.890 ảnh MNIST và 262/300 ảnh ngoài, còn 38 lỗi; BHMSDS 82/100, Bitmap Numbers 82/100, HwD-1000 98/100. Toàn bộ 110 ảnh MNIST kiểm tra đã xem trước đó được loại khỏi 9.890 ảnh cuối. Không gộp Digits, MNIST và ba nguồn ngoài thành một độ chính xác.

600 ảnh gốc có seed lấy mẫu 42, chia 300 xác thực/300 kiểm tra, mỗi nguồn/chữ số có 10 ảnh mỗi tập. Xem [manifest](data/external_handwriting/manifest.csv), [nguồn và giấy phép](data/external_handwriting/SOURCES.md), [contact sheets](data/external_handwriting/contact_sheets), [ghi công MNIST và hình biến đổi](outputs/external_optimization_20261118T175401Z_4ca3a08f/SOURCES.md).

Ảnh gồm giấy đã cắt, scan và vẽ tay kỹ thuật số; **chưa đại diện ảnh điện thoại bất kỳ**. Không có mã người viết đáng tin để xác nhận tách người viết; Bitmap thiếu ánh xạ nguồn gốc từng ảnh. MLP mới đồng thời đổi dữ liệu, lượng mẫu, kiến trúc và độ phân giải, nên không quy toàn bộ cải thiện cho riêng tiền xử lý. Xác suất chưa hiệu chỉnh, giá trị cao vẫn có thể sai.

## Cài môi trường trên Windows PowerShell

```powershell
git clone -c core.longpaths=true https://github.com/shengs1/HandwrittenDigitRecognition.git
cd HandwrittenDigitRecognition
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Chạy từ thư mục gốc dự án; không cần kích hoạt venv hoặc thay ExecutionPolicy. Đã kiểm tra Python 3.12.14 và phiên bản ghim trong requirements. Nếu `py` không hoạt động, dùng Python 3.12 đã cài thật để tạo venv. Nếu tạo venv bằng `uv` không có pip, dùng `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`.

`core.longpaths=true` hỗ trợ tên artifact dài trên Windows. `.gitattributes` giữ nguyên byte LF/CRLF cho các tệp có checksum; không tự chuyển line ending của manifest, lock, mô hình hoặc kết quả đã chốt. Không sao chép venv giữa máy.

## Chạy ứng dụng

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Mở [http://localhost:8501](http://localhost:8501). Chọn nguồn ảnh, mô hình và bấm **Nhận diện chữ số**.

| Lựa chọn trên giao diện | Mô hình và dữ liệu đầu vào |
|---|---|
| Ảnh kiểm tra Digits — mặc định | 360 mã ảnh đúng split đã lưu; ba mô hình Digits; giữ nguyên 8×8, 64 đặc trưng, miền 0–16 |
| Ảnh mẫu Digits | Toàn bộ Digits, có thể gồm ảnh huấn luyện; ba mô hình Digits; giữ nguyên điểm ảnh |
| Tải ảnh từ máy | Ba mô hình Digits dùng gray_bbox 8×8/0–16; hoặc chọn rõ **Multilayer Perceptron (MLP) — MNIST** dùng 28×28/784 đặc trưng/0–255 |

Tên mô hình: **Logistic Regression**, **K-Nearest Neighbors (KNN)**, **Multilayer Perceptron (MLP)** và bản MNIST. Ba thẻ **Bộ dữ liệu Digits**, **Tốt nhất qua kiểm định chéo**, **Độ chính xác kiểm tra · KNN** luôn là số liệu Digits, không phải độ chính xác của mô hình đang nhận ảnh tải lên.

Ảnh tải lên có bản gốc và bản sau tiền xử lý. App xử lý hướng ảnh, nền, vùng trong suốt, thang xám, vùng nét, tỷ lệ và căn giữa; dùng đúng hàm đã chọn theo validation. Chuẩn hóa đặc trưng chỉ chạy trong Pipeline. MLP MNIST chỉ xuất hiện ở nguồn tải ảnh; không tự chuyển mô hình theo xác suất. Đổi ảnh hoặc mô hình sẽ xóa kết quả cũ.

Hỗ trợ PNG/JPEG/BMP/WebP, tối đa 10 MB và 16 triệu điểm ảnh; ảnh trống/hỏng hoặc thiếu mô hình được báo lỗi. App chỉ tải joblib, **không huấn luyện hoặc tải MNIST khi mở**. Chỉ dùng joblib tin cậy của dự án.

Giữ `app.py`, `external_preprocessing.py`, `.streamlit/config.toml`, hai registry và các Pipeline được registry trỏ tới. Cần bốn tệp `data_summary.json`, `selection_lock.json`, `model_comparison.csv`, `split_indices.csv` trong run Digits và `selection_lock.json` của run mở rộng. Dataset MNIST/600 ảnh đánh giá/mảng cache không bắt buộc để chạy demo. Registry phụ ràng buộc checksum model, module ảnh và lựa chọn đã khóa.

## Notebook, kiểm thử và tái lập

```powershell
.\.venv\Scripts\python.exe -m notebook digit_classification.ipynb
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

Notebook đã có output thật; không cần Run All để chạy app. `RUN_EXPERIMENTS=True` sẽ tạo run huấn luyện mới; chỉ dùng khi chủ động tái lập, không chạy để tìm seed/điểm tốt hơn và không thay registry chính thức. Lệnh tái lập notebook khi cần: `.\.venv\Scripts\python.exe -X utf8 tests/run_notebook.py`.

Kết quả gần nhất của mã giao diện: **53/53 unittest PASS ngày 21/11/2026**, 12,229 giây, ghi trong [HANDOFF](HANDOFF.md). Lượt cập nhật tài liệu 23/11 không thay code và không tuyên bố chạy lại 53 test. [Kiểm tra sạch ngày 19/11](outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md) đã cài venv mới 120 gói, kiểm bốn Pipeline, 14 tình huống demo, 8 lỗi model, bản demo tối thiểu và 1.200 suy luận replay; [log Git checkout sạch](outputs/optimization_freeze_20261119T045133Z_728f35c1/git_index_unittest.log).

[Hướng dẫn tái lập mở rộng](outputs/external_optimization_20261118T175401Z_4ca3a08f/README.md) và các script trong tests/ là hồ sơ của run đã chốt. Các manifest checksum toàn snapshot và verifier lịch sử có cả mã/test/tài liệu tại thời điểm đó; đổi nhãn giao diện hoặc tài liệu có thể tạo khác biệt hợp lệ. Không sửa manifest cũ để che khác biệt. Với mã hiện tại, dùng bộ unittest và checksum Pipeline trong registry; không xem việc khác checksum của tài liệu lịch sử là thay đổi trọng số.

`tests/check_demo.py` kiểm hồi quy baseline với 10 fixture MNIST lịch sử, không đo chất lượng ảnh điện thoại của bản tối ưu. Kết quả cũ 3/10 mỗi mô hình và lượt 100 MNIST 46/40/37 được giữ riêng trong outputs/, không bị thay bằng kết quả mới.

## Ảnh tự chụp và việc còn lại

Chưa có ảnh điện thoại có nhãn do nhóm cung cấp. Viết một chữ số trên giấy, chụp đủ sáng, tránh bóng/nhòe, giữ ảnh gốc và nhãn thật trước suy luận. Dùng nguồn **Tải ảnh từ máy**, chọn rõ mô hình, kiểm preview rồi nhận diện; ghi filename, nhãn thật, mô hình, dự đoán và đúng/sai. HEIC cần xuất JPEG/PNG trước khi dùng; giữ bản gốc. Không dùng ảnh AI/font thay ảnh chụp, không loại ảnh sai hoặc chỉnh mô hình đã chốt từ kết quả thử. Nếu tổng hợp độ chính xác, báo riêng nguồn/cỡ mẫu/mô hình.

Nhóm cần rà soát và xác nhận nhận định dự thảo; điền tên/MSSV/lớp/phân công thật; xuất báo cáo PDF/DOCX và slide PPTX/PDF; tập giải thích code, dữ liệu, độ đo, lỗi và giới hạn. Hiện chưa xác nhận có các sản phẩm nộp chính thức hoặc kết quả vấn đáp.

## Tài liệu và hồ sơ

| Tài liệu | Mục đích |
|---|---|
| [Yêu cầu và đối chiếu](docs/REQUIREMENTS_MAP.md) | PDF, tiêu chí và năm câu đề tài 13 |
| [Chỉ mục kết quả](docs/RESULTS_INDEX.md) | Bảng/hình/nguồn phần A và B |
| [Dự thảo báo cáo](docs/REPORT_OUTLINE.md) | Đúng 10 mục của PDF |
| [Dự thảo 12 slide](docs/SLIDE_OUTLINE.md) | Nội dung trình bày và minh họa |
| [Câu hỏi vấn đáp](docs/VIVA_QUESTIONS.md) | Giải thích code và kết quả thật |
| [Final review](docs/FINAL_REVIEW.md), [Final audit](docs/FINAL_AUDIT.md) | Trạng thái, bằng chứng và việc còn thiếu |
| [AGENTS](AGENTS.md), [HANDOFF](HANDOFF.md) | Quy tắc tiếp tục và lịch sử bàn giao |

Các tệp trong `outputs/` và README/LICENSE của nguồn bên thứ ba giữ theo thời điểm tạo; không chỉnh sửa để mô tả lại hiện tại. Không đưa `.venv/`, cache hoặc `tmp/` vào Git/gói nộp. Không trộn các run hoặc đánh đồng dàn ý Markdown với báo cáo/slide đã nộp.
