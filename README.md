# Phân loại chữ số viết tay — đề tài 13

[Repository GitHub](https://github.com/shengs1/HandwrittenDigitRecognition) · Python 3.12 · Digits · Streamlit.

**Chốt kỹ thuật19/11/2026: UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Người dùng đã duyệt giữ gray_bbox và MLP MNIST28. Snapshot độc lập, Python3.12.14/venv mới cài đủ120 gói từ requirements: **53/53 unittest PASS**;14 tình huống demo/8 tình huống thiếu-hỏng model đạt; replay1200 dự đoán app khớp artifact. Bản demo tối thiểu chạy khi chặn fit/download, không cần MNIST/data/cache. [Kiểm tra chốt](outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md), [log venv sạch](outputs/optimization_freeze_20261119T045133Z_728f35c1/clean_unittest.log). Không huấn luyện/tuning lại. Các dòng “chờ review/chưa push” phía dưới ghi trạng thái lịch sử trước lần chốt này; Git hiện tại xem HANDOFF.

**UI FROZEN:** giữ nguyên thiết kế đã duyệt ngày18/11/2026. Yêu cầu mới ngày19/11 cho phép tối ưu nhánh upload và bổ sung lựa chọn MLP MNIST sau validation; CSS/theme/bố cục và thực nghiệm Digits vẫn giữ nguyên. [Bằng chứng đóng băng trước đó](outputs/freeze_20261118T154422Z_32ced9af/FREEZE_REVIEW.md).

**Bản tối ưu ảnh ngoài đã duyệt:** đã thu thập600 ảnh viết tay từ3 nguồn, seed42, chia300 validation/300 test; giữ nguyên bytes và khóa manifest trước suy luận. Chọn `gray_bbox` bằng validation cho upload8×8, bổ sung **MLP — MNIST (ảnh ngoài)** riêng cho upload28×28. Không tự chuyển model theo xác suất; không huấn luyện khi mở app.

| Hệ thống | Accuracy MNIST test9890 | Accuracy test300 ảnh ngoài | Macro F1 ngoài |
|---|---:|---:|---:|
|KNN + xử lý cũ|41,93%|48,00%|0,4903|
|KNN + gray_bbox|47,07%|58,00%|0,5733|
|MLP MNIST28|97,39%|87,33%|0,8713|

MLP MNIST28 đạt82% BHMSDS,82% Bitmap Numbers,98% HwD-1000 (100 ảnh test/nguồn). Đây là ảnh giấy đã cắt/scan và ảnh vẽ tay số, **không phải accuracy ảnh điện thoại bất kỳ**. Không có writer ID đáng tin; không chứng minh tách người viết. Còn38/300 lỗi. Không gộp các bộ dữ liệu thành một accuracy. Cả ba kết quả Digits chính thức bên dưới không đổi.

[Báo cáo đầy đủ, validation/tất cả7 hệ thống/giới hạn](outputs/external_optimization_20261118T175401Z_4ca3a08f/REPORT.md), [tái lập và khôi phục](outputs/external_optimization_20261118T175401Z_4ca3a08f/README.md), [nguồn/license/giới hạn nguồn gốc](data/external_handwriting/SOURCES.md), [manifest600 ảnh](data/external_handwriting/manifest.csv). **53/53 unittest đạt**, giữ43 test cũ;587 file bảo vệ không đổi. [Log test](outputs/external_optimization_20261118T175401Z_4ca3a08f/tests_final.log), [trình duyệt thật](outputs/external_optimization_20261118T175401Z_4ca3a08f/browser/checks.json). Các mục UI và kiểm thử cũ dưới đây là lịch sử.

Ghi công/điều kiện phân phối dữ liệu MNIST và hình biến đổi: [SOURCES của run mở rộng](outputs/external_optimization_20261118T175401Z_4ca3a08f/SOURCES.md). Giữ license MIT/CC0 gốc đi kèm600 ảnh;Bitmap có attribution CC0 công bố nhưng chưa truy được mapping từng ảnh. Sau cập nhật4 tài liệu báo cáo/slide được yêu cầu,583/587 file bảo vệ lịch sử giữ nguyên,4 file khác là tài liệu được phép đổi;toàn bộ model/notebook/số liệu vẫn khớp hash. Verifier có thể ghi bằng chứng mới mà không sửa run cũ:

```powershell
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py verify --directory outputs/external_optimization_20261118T175401Z_4ca3a08f --verification-output outputs/verify_release_local
```

**Thông tin kỹ thuật và tương tác:** expander hiển thị dữ liệu, bảng tham số đọc từ Pipeline đang chọn, quy trình ảnh và giới hạn ngắn. Cả5 dropdown giữ tương tác native; đã thử15 vị trí bấm và bàn phím. [Bằng chứng mới nhất, screenshot và giới hạn kiểm thử upload](outputs/interaction_20261118T122825Z_df6a5b22/INTERACTION_REVIEW.md), [43/43 unittest](outputs/interaction_20261118T122825Z_df6a5b22/tests_final.log). Không đổi model/notebook/kết quả thực nghiệm.

**Responsive ở zoom100%:** chọn chữ số/ID gọn trong cột ảnh; đã đo thực5 viewport từ1280×720 đến1920×1080, các trạng thái đóng thông tin kỹ thuật không tràn dọc/ngang. Xem [bảng kiểm và screenshot](outputs/responsive_20261118T035501Z_c6f49df4/LAYOUT_REVIEW.md), [40 tests](outputs/responsive_20261118T035501Z_c6f49df4/tests_final.log). Không cần giảm browser zoom; mở phần kỹ thuật sẽ cho phép cuộn tự nhiên.

**Giao diện mới (2026-11-18):** dark mode, hai cột ảnh/kết quả, nút nhận diện xanh và 10 thanh xác suất. Mặc định **Ảnh test Digits**; đổi lựa chọn sẽ xóa kết quả cũ. [Ảnh demo test](outputs/ui_20261118T015852Z_1c47689a/02_test_result_1366x768.jpg), [ảnh upload](outputs/ui_20261118T015852Z_1c47689a/08_upload_result_1366x768.jpg), [40/40 test](outputs/ui_20261118T015852Z_1c47689a/tests_final.log), [kiểm tra giao diện/checksum](outputs/ui_20261118T015852Z_1c47689a/ui_checks.json). Đã kiểm tra trực tiếp 1366×768, 1920×1080 và 390×844; không đổi notebook, model, tiền xử lý hoặc kết quả thực nghiệm.

**Final Completion:** notebook có nhận định dự thảo từ kết quả thật, nội dung báo cáo 10 mục và 12 slide đã chuẩn bị, **chưa được nhóm xác nhận**. Demo có lựa chọn ảnh test đúng split. **37/37 test qua trên checkout sạch**; model, số liệu và mã huấn luyện không đổi. Xem [đối chiếu yêu cầu và kiểm thử mới nhất](docs/FINAL_REVIEW.md), [HANDOFF](HANDOFF.md). Báo cáo PDF/DOCX, slide chính thức, thông tin nhóm và phân công vẫn cần hoàn thiện.

Các kiểm tra lịch sử được giữ ở [FINAL_AUDIT](docs/FINAL_AUDIT.md).

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
git clone -c core.longpaths=true https://github.com/shengs1/HandwrittenDigitRecognition.git
cd HandwrittenDigitRecognition
```

Từ thư mục gốc project, dùng Python 3.12 đã cài:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Không cần activate hoặc thay ExecutionPolicy. Nếu `py`/`python` là alias Microsoft Store bị lỗi, thay `py -3.12` bằng đường dẫn Python thật. Với môi trường tạo bằng `uv` không có pip, dùng `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`. Không chép `.venv` sang máy khác. requirements ghim các thư viện trực tiếp đã kiểm tra; môi trường thực nghiệm tại `outputs/<run_id>/environment.json`.

Git for Windows cần `core.longpaths=true` khi clone vào thư mục sâu vì một số tên artifact kiểm thử dài. Lệnh clone trên lưu cấu hình này cho repo mới. `.gitattributes` giữ nguyên bytes LF/CRLF của nguồn/manifest/lock/CSV có SHA256; không chạy công cụ đổi line ending trên artifact đã chốt.

## Chạy demo

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Mở [http://localhost:8501](http://localhost:8501). Chọn mô hình, chọn **Ảnh mẫu Digits** (toàn dataset), **Ảnh test Digits** (360 id đúng split đã lưu, mặc định) hoặc tải PNG/JPEG/BMP/WebP từ máy rồi bấm **Nhận diện chữ số**. Ảnh Digits hiển thị một lần, phóng to rõ từng pixel; upload có ảnh gốc và ảnh sau tiền xử lý. Kết quả bên phải có đủ 10 thanh xác suất. Model mặc định là KNN đã chọn bằng CV; các thẻ tổng quan đọc số liệu chính thức. Giải thích Pipeline/thông số/giới hạn nằm trong expander phía dưới.

Nguồn ảnh test đọc `outputs/<registry.run_id>/split_indices.csv`, không chia lại; thiếu/sai split thì báo lỗi. Dùng mẫu test để minh họa sau đánh giá không tạo một đánh giá độc lập mới. Ảnh Digits giữ đúng pixel gốc. Upload của ba model Digits dùng `gray_bbox`: EXIF/grayscale/alpha/nền, crop nét, giữ tỷ lệ/căn bbox trong32×32 rồi tổng từng khối4×4 thành8×8, miền0–16. Chọn nguồn **Tải ảnh từ máy tính**, sau đó chọn **MLP — MNIST (ảnh ngoài)** để dùng tiền xử lý28×28/0–255 và Pipeline784 đặc trưng; lựa chọn này không có ở hai nguồn Digits. Bảng tham số/preview cập nhật theo model. Scaler chỉ chạy bên trong Pipeline. Giới hạn file10 MB,16 triệu pixel; file hỏng, ảnh trống và thiếu model được báo trong giao diện.

Registry trỏ đến đúng run và checksum của cả Pipeline. Giữ toàn bộ `models/<run_id>/`; không chỉ copy estimator. Nếu thiếu registry/model, khôi phục từ bản đã xác nhận trong Git; app không tự fit để bù. Chỉ sử dụng joblib do project tin cậy. Khi sai phiên bản sklearn, cài đúng requirements.

Để dùng bản tối ưu, giữ thêm `external_preprocessing.py`, `models/external_registry.json`, `models/external_optimization_20261118T175401Z_4ca3a08f/mlp_mnist.joblib` và `outputs/external_optimization_20261118T175401Z_4ca3a08f/selection_lock.json`. Registry phụ ràng buộc SHA256 của module/model/lock; registry Digits gốc không đổi. Không cần dataset MNIST hay600 ảnh đánh giá để chạy demo. Nếu không có registry phụ, app dùng lại ba model/tiền xử lý cũ; hash sai hiển thị cảnh báo. Hướng dẫn khôi phục app ổn định nằm trong README của run bổ sung.

## Mở và chạy notebook

```powershell
.\.venv\Scripts\python.exe -m notebook digit_classification.ipynb
```

Chọn kernel `.venv`. Notebook đã có output thật; **không cần Run All để dùng demo**. Khi chủ động tái lập thí nghiệm, Restart Kernel/Run All, hoặc:

```powershell
.\.venv\Scripts\python.exe -X utf8 tests/run_notebook.py
```

`RUN_EXPERIMENTS=True` thực hiện CV/grid/learning curve/fit cuối và tạo run mới. Đổi thành False nếu chỉ cần dữ liệu/EDA. Mỗi run có thư mục riêng, không ghi đè; registry đang có không tự thay bằng run mới. Không chạy lại để tìm seed hoặc điểm tốt hơn, không dùng test tuning.

## Kiểm tra ảnh điện thoại của nhóm

Hiện **chưa có ảnh tự chụp do nhóm cung cấp**, chưa có số liệu accuracy cho nguồn này. Dùng lại app hiện có: viết một chữ số0–9 trên giấy, chụp đủ sáng, tránh bóng/nhòe, giữ ảnh gốc; lưu nhãn thật trước suy luận. Chọn **Tải ảnh từ máy**, chọn rõ **MLP — MNIST (ảnh ngoài)**, tải PNG/JPEG/BMP/WebP và kiểm ảnh gốc/preview28×28 trước khi bấm nhận diện. Có thể chọn từng model Digits để đối chiếu trên cùng ảnh; preview của chúng là8×8. Ghi filename/nhãn thật/model/dự đoán/xác suất/đúng-sai; giữ cả ảnh sai, không lấy ảnh AI/font hoặc ảnh tổng hợp thay ảnh chụp. File HEIC cần xuất JPEG/PNG trước khi dùng, không đổi file gốc lưu trữ.

Không sửa preprocessing/model vì một ảnh demo sai; tập ảnh mới chỉ để ghi nhận giới hạn bản đã chốt. Nếu tự tổng hợp accuracy, nêu rõ số ảnh/cách thu thập/nguồn và báo riêng từng model, không gộp với Digits/MNIST/300 test đã công bố. Xác suất chưa hiệu chỉnh. Công cụ `tests/check_demo.py` giữ vai trò kiểm hồi quy baseline với fixture lịch sử, không phải công cụ đo accuracy ảnh điện thoại của bản tối ưu.

## Kiểm thử và giới hạn

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe -X utf8 tests/check_demo.py
```

Test kiểm tra miền pixel, leakage, notebook, ảnh sáng/tối/trong suốt/trống/hỏng, checksum/mất model, xác suất, khớp 360 dự đoán test đã lưu và luồng Streamlit. `check_demo.py` chỉ suy luận, tạo thư mục `outputs/demo_...` với CSV/ảnh xử lý/báo cáo checksum, không fit hoặc thay model.

Ở Phase 2 đã cài môi trường mới: 120 gói tương thích và 25/25 test đạt ([log cũ](outputs/demo_20261117T082316Z_b269f12c/tests_clean_environment.log)). Final review bổ sung kiểm tra khoa học dữ liệu và sửa điều kiện checkout mới: **31/31 test đạt**, [log mới](outputs/review_20261117T090347Z_9df57e69/clean_checkout_tests.log), [môi trường mới](outputs/review_20261117T090347Z_9df57e69/clean_environment.json), [đối chiếu rerun](outputs/review_20261117T090347Z_9df57e69/review_checks.json). Ảnh chọn mẫu/upload đã thử ở Phase 2: [giao diện](outputs/demo_20261117T082316Z_b269f12c/streamlit_demo.jpg).

[Bằng chứng kiểm thử ảnh Phase 2](outputs/demo_20261117T082316Z_b269f12c/demo_verification.json): 10 ảnh mẫu Digits (ảnh đầu mỗi lớp), LR đúng10/10, KNN và MLP đúng9/10. Với10 ảnh viết tay MNIST bên ngoài, cả ba đúng3/10. Đây là minh họa rất nhỏ, **không phải accuracy tổng quát trên ảnh ngoài Digits**. Mẫu Digits có thể thuộc train. Trong phép minh họa này MNIST chỉ là fixture suy luận, không đổi dữ liệu huấn luyện của ba Pipeline Digits. Lượt tối ưu mới ở đầu README dùng validation riêng và model MNIST riêng; giữ nguyên kết quả cũ. Chưa thử ảnh tự chụp của nhóm. Xác suất cao vẫn có thể sai, chưa hiệu chỉnh.

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

Nhóm kiểm tra, sửa và xác nhận các nhận định dự thảo; xuất báo cáo/slide chính thức, điền thông tin/phân công thật và tập bảo vệ. Nguồn: [PDF đồ án](docs/Huong_Dan_Do_An_CuoiKy.pdf), [đối chiếu yêu cầu](docs/REQUIREMENTS_MAP.md).


## Kiểm tra phiên bản hiện tại và danh sách bản nộp

Lượt hoàn thiện: **37/37 tests PASS** (checkout sạch 4,807 s theo unittest), [log](outputs/completion_20261117T100609Z_b8981ac1/clean_checkout_tests.log), [kiểm tra notebook/checksum](outputs/completion_20261117T100609Z_b8981ac1/completion_checks.json), [phiên bản thư viện](outputs/completion_20261117T100609Z_b8981ac1/clean_environment.json), [Streamlit HTTP/giao diện/upload](outputs/completion_20261117T100609Z_b8981ac1/streamlit_check.json), [ảnh demo test](outputs/completion_20261117T100609Z_b8981ac1/streamlit_test_sample.jpg). Dùng lại venv sạch đã cài từ requirements ở lượt review trước; lượt này tạo bản nguồn sạch mới có diff hiện tại, ban đầu không có tmp. Không cài lại môi trường hoặc rerun huấn luyện: requirements và toàn bộ mã cell không đổi; lượt review trước đã Run All thành công với metric/prediction trùng. Cảnh báo ScriptRunContext khi chạy AppTest ở chế độ bare không phải lỗi ứng dụng.

Những file cần đưa vào bản nộp cuối:

- `digit_classification.ipynb` có output; `app.py`, `requirements.txt`, `README.md`.
- `models/registry.json` và toàn bộ `models/20261117T081201Z_fd32180f/`.
- Toàn bộ `outputs/20261117T081201Z_fd32180f/` (CSV/JSON/15 hình); giữ run_id nhất quán.
- `tests/*.py`, fixture ảnh/manifest/nguồn trong `tests/fixtures/`; PDF và tài liệu tham khảo ở `docs/`.
- Báo cáo **PDF hoặc DOCX** và slide **PPTX/PDF** sau nhóm hoàn thiện; hiện mới có nội dung Markdown dự thảo.
- AGENTS/HANDOFF, bảng đối chiếu và bằng chứng kiểm thử cần thiết nếu nộp repo.

Không đưa `.venv/`, `.uv-cache/`, `__pycache__/`, `.ipynb_checkpoints/`, `tmp/`, bản checkout thử hoặc log không cần thiết vào gói nộp. Giữ lịch sử/artifact có giá trị trong repo, nhưng gói nộp chỉ chọn run chính thức và bằng chứng cần thiết; không trộn các run hỗ trợ cũ vào bảng kết quả. Chưa tạo ZIP vì báo cáo/slide chính thức chưa hoàn thành. Sau lượt hoàn thiện, người dùng đã yêu cầu push: code và tài liệu đã có trên `main` tại [commit 3a2c850](https://github.com/shengs1/HandwrittenDigitRecognition/commit/3a2c85041c091a898a7d15a30759bdeb63364869); xem HANDOFF để biết xác minh Git.
