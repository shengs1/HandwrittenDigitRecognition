# Chỉ mục thực nghiệm ảnh ngoài — 19/11/2026

[REPORT.md](REPORT.md) chứa phương pháp, bảng validation, cùng-tập-test, chi phí, phân tích có giới hạn và đề xuất giữ bản tối ưu để review. Không thay thực nghiệm Digits chính thức. Bản này còn local, chưa commit/push theo yêu cầu.

| File/thư mục | Bằng chứng |
|---|---|
|`protocol.json`, `protocol.sha256`|Không gian thử/tiêu chí đặt trước; seed42; ngoại lệ110 MNIST test cũ|
|`mnist_train_split.csv`, `mnist_test_eligibility.csv`|54000 train/6000 validation;9890 test còn lại|
|`selection_lock.json`, `.sha256`|Chọn gray_bbox và MLP MNIST bằng validation trước test|
|`validation/`, `specialist/validation_metrics.csv`|Tất cả phương án,3 nguồn tách riêng|
|`specialist/mlp_mnist.joblib`, `metadata.json`|Một lần train,30 iterations,23,8956s; Pipeline đủ scaler|
|`final_test/`|Accuracy/macro F1, report từng chữ số/nguồn, confusion, dự đoán/xác suất/đúng-sai|
|`analysis/`|Bảng so sánh/descriptor validation;7 hình kết quả/training/lỗi|
|`arrays/`|Đầu vào suy luận chính xác; JSON ghi preprocessing/time/rejection|
|`browser/`|Ảnh viewport thật, ma trận chức năng/dropdown/technical/responsive|
|`tests_final.log`, `verification.json`|53 unittest;600 ảnh/35 metric rows/587 checksum|
|`protected_before.json`, `protected_after.json`|Bảo toàn notebook/models/registry/artifact cũ|
|`stable_source/`, `stable_source_sha256.json`|Nguồn trước tối ưu, không ghi đè lịch sử|
|`validation_float32_diagnostic/`, `arrays_float32_diagnostic/`|Bản đầu dùng float32; replay đồng loạt8×8 float64 trước selection; metric không đổi|

Dữ liệu handwriting: [manifest600 ảnh](../../data/external_handwriting/manifest.csv), [nguồn/license](../../data/external_handwriting/SOURCES.md), [contact sheets](../../data/external_handwriting/contact_sheets).31200 ảnh nguồn được kiểm trước sampling; chưa có ID writer đáng tin. Tập test đã xem kết quả, không dùng lại để tuning.

## Kiểm tra lại kết quả có sẵn (không train)

Chạy từ thư mục gốc repository, cùng `.venv` đã cài `requirements.txt` theo README gốc. Không thêm dependency; dùng Python3.12.14 và phiên bản trong environment.json.

```powershell
$run = 'outputs/external_optimization_20261118T175401Z_4ca3a08f'
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py verify --directory $run
.\.venv\Scripts\python.exe -X utf8 tests/summarize_external_optimization.py --directory $run
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

`verify` tính lại độ đo từ prediction đã lưu, kiểm khóa/checksum/manifest. Script summarize chỉ dẫn xuất bảng/hình, không gọi fit hoặc suy luận lại. Không chạy lại `validation/train/lock/test` trên thư mục đã hoàn tất. Model checksum có thể khác khi huấn luyện trên môi trường/phần cứng khác dù cùng seed; không ghi đè bản đã khóa để cố khớp điểm số.

## Tái lập một run mới khi chủ động thực nghiệm

Collector tải repository gốc ở commit cố định, kiểm giấy phép/ảnh và khóa manifest trước model. Lệnh dưới chỉ dùng khi dữ liệu chưa có; collector từ chối ghi đè đích đã có. Cache ZIP nằm trong tmp/ và không cần cho demo. Không thực thi mã từ repo nguồn.

```powershell
.\.venv\Scripts\python.exe -X utf8 tests/collect_external_handwriting.py
$newRun = 'outputs/external_optimization_reproduction_01'
.\.venv\Scripts\python.exe -X utf8 tests/prepare_external_optimization.py --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py validation --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py train --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py lock --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py test --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/optimize_external.py verify --directory $newRun
.\.venv\Scripts\python.exe -X utf8 tests/summarize_external_optimization.py --directory $newRun
```

Prepare yêu cầu thư mục mới, tải MNIST IDX HTTPS/kiểm MD5, ghi split/protocol. Train chỉ thực hiện nếu điều kiện đã định trước đạt; không sửa cấu hình theo test. Đây là replay thiết kế đã biết kết quả, **không tạo test độc lập mới**. Không tự cập nhật registry hoặc copy Pipeline mới vào demo sau replay. Để nghiên cứu thêm cần validation/test mới chưa dùng; hiện không có yêu cầu đó.

## Đóng gói demo và khôi phục

Giữ các file demo gốc và bộ models/Digits/split chính thức, thêm `external_preprocessing.py`, `models/external_registry.json`, model mới ở đường dẫn registry và selection_lock.json của run này. Không cần60k MNIST, ZIP repo, mảng npz hoặc600 ảnh để mở app. Không bỏ scaler ra khỏi joblib.

Ảnh Digits không đi qua preprocessing upload. MLP mới chỉ có khi chọn nguồn upload. Muốn trở lại app ổn định trước tối ưu mà vẫn giữ dữ liệu/bằng chứng:

```powershell
Copy-Item -LiteralPath 'outputs/external_optimization_20261118T175401Z_4ca3a08f/stable_source/app.py' -Destination 'app.py'
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Lệnh rollback ghi đè **app hiện tại** bằng snapshot đã lưu; chỉ chạy khi đã quyết định rollback. Không cần xóa dữ liệu/model/registry phụ. Snapshot README/AGENTS/HANDOFF chỉ để tham khảo, không chép đè tài liệu chuyển giao mới. Không thực hiện rollback trong lượt này.

## Giới hạn xác nhận

53/53 tests đạt trên venv hiện có, không tạo/cài lại venv sạch trong lượt này (requirements không đổi). Browser thật kiểm5 viewport zoom100%,15 vị trí dropdown,3×2 nguồn Digits,4 model upload PNG, scan BMP và lỗi; upload dùng harness giữ widget nhưng cấp bytes fixture, chưa thử lại hộp chọn file Windows. Không có số liệu ảnh chụp mới của nhóm hoặc giảng viên. Bản scan Bitmap thiếu mapping từng ảnh về writer/sheet upstream; không thể bảo đảm độc lập writer hoặc xác minh toàn bộ lịch sử từng ảnh. Nhóm cần xác nhận nhận định trước khi đưa vào bản nộp.
