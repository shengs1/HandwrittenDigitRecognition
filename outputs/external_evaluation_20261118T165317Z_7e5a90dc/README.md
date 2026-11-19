# Đánh giá bổ sung MNIST test ngoài Digits

Run `external_evaluation_20261118T165317Z_7e5a90dc`, mã nguồn nền `af7b7666eaf1046340524a0a5d109ef2783b75f2`. UI vẫn FROZEN ở36148ad. Không đổi notebook/app/thuật toán ảnh/requirements/mô hình hoặc kết quả chính thức.

**Kết quả:** Logistic Regression46/100 (macro F1=0,480071); KNN40/100 (0,422498); MLP37/100 (0,371433). [Báo cáo phân tích và đoạn nhận định để nhóm rà soát](REPORT.md). Đây là một mẫu phân tầng nhỏ, không phải accuracy toàn bộ MNIST hoặc ảnh điện thoại. KNN chính thức vẫn được giữ theo CV Digits.

| File/thư mục | Nội dung |
|---|---|
| sample_ids.csv, sample_lock.json, sample_lock.sha256 |100 ID gốc0-based, nhãn, checksum; khóa trước mọi suy luận |
| source_provenance.json, source/ |Nguồn/URL/license/digest và hai archive MNIST test đã tải, đủ tái lập offline |
| originals/ |100 PNG28×28 giữ đúng pixel của IDX, không dùng lại10 mẫu cũ |
| processed/, processed_pixels.npy |100 preview8×8 và mảng float64 chính xác đã đưa vào Pipeline; PNG chỉ để xem |
| results/external_metrics.csv |Accuracy, macro F1/precision/recall, số ảnh đúng |
| results/per_digit_*.csv, classification_report_*.json |Precision/recall/F1/support cho từng chữ số; per_digit_all_models.csv gộp3 mô hình |
| results/confusion_matrix_*.csv, confusion_pairs.csv |Ma trận hàng thật/cột dự đoán và cặp nhầm có hướng |
| results/predictions.csv, correct_*.csv, incorrect_*.csv |300 dòng dự đoán/xác suất; danh sách ảnh đúng/sai từng mô hình, có đường dẫn ảnh |
| results/comparison_with_digits.csv |So với test Digits chính thức360 ảnh; thay đổi điểm phần trăm |
| results/preprocessing_diagnostics.json, preprocessing_audit.json |Crop/shift/miền pixel, lặp/đảo nền, kiểm tra hợp đồng; không đổi preprocessing |
| results/image_descriptors.csv, distribution_summary.csv, distribution_by_digit.csv |Độ sáng/hình học, so Digits train/test và MNIST gốc/sau app; chỉ mô tả |
| results/high_confidence_errors.csv |Số lỗi có xác suất dự đoán≥0,9; chưa hiệu chỉnh xác suất |
| results/model_integrity.csv, protected_before/after.json |3 Pipeline khớp registry và332 file có sẵn được bảo vệ không đổi |
| figures/ |3 ma trận;8 cặp ảnh sai/model theo ID; ảnh trung bình lớp và histogram mô tả |
| verification.json/log, evaluation.log, unittest.log |Replay300 dự đoán/100 preprocessing, kiểm công thức metrics và43/43 unittest |
| final_checks.json, evaluation_artifacts_sha256.json |Đối chiếu bảng dẫn xuất/liên kết/hình và manifest checksum của riêng run mới |
| evaluation_script_at_inference.py, results/plot_label_correction.json |Snapshot script khớp hash lúc suy luận; sau đó chỉ sửa chữ>20% thành≥20% ở tiêu đề hình, không đổi thống kê |

Các tên không ghi prefix trong bảng nằm trong cùng thư mục với file đầu dòng tương ứng.

## Nguồn và quyền sử dụng

MNIST của Yann LeCun, Corinna Cortes và Christopher J. C. Burges. Hai tệp `t10k-images-idx3-ubyte.gz` và `t10k-labels-idx1-ubyte.gz` tải từ [CVDF mirror được tác giả cho phép](https://github.com/cvdfoundation/mnist), qua HTTPS. [TensorFlow mô tả dữ liệu/test và license](https://www.tensorflow.org/api_docs/python/tf/keras/datasets/mnist/load_data): MNIST được cung cấp theo [CC BY-SA3.0](https://creativecommons.org/licenses/by-sa/3.0/). Giữ ghi công và license này với dữ liệu MNIST/ảnh trích/ảnh8×8 biến đổi trong run; không gán license của dữ liệu cho toàn bộ mã nguồn project.

MD5 hai archive đối chiếu [mã nguồn torchvision](https://github.com/pytorch/vision/blob/main/torchvision/datasets/mnist.py); SHA256 còn khớp manifest tải trước của project. Không cài/import TensorFlow hoặc PyTorch. Hash/URL/thời điểm tải và phép biến đổi lưu trong source_provenance.json. Ảnh gốc là mã hóa PNG lossless từ IDX; ảnh8×8 là sản phẩm của đúng API app hiện có.

## Lấy mẫu và chạy lại

Seed lấy mẫu42, NumPy default_rng/PCG64 phiên bản2.3.5. Mỗi lớp dùng pool ID tăng dần, loại10 ID cũ và ảnh trùng byte pixel với ảnh cũ, giữ ID đầu của mỗi nội dung trùng trong pool; lấy10 không hoàn lại, sắp ID trong lớp. Không chạy model để lọc/chọn/thay ảnh. Khóa lúc16:53:21UTC; suy luận bắt đầu16:53:40UTC18/11/2026. Hash sample_lock: `388ce6152a4c12d71ba31e4884624a11689ad7ba9461de6fdc5303c010e80cf1`.

Từ gốc repo, môi trường requirements hiện có; **không cần chạy notebook**:

```powershell
# Kiểm lại chính run này offline; chỉ suy luận, không ghi đè số liệu.
.venv/Scripts/python.exe -X utf8 tests/evaluate_external.py verify --directory outputs/external_evaluation_20261118T165317Z_7e5a90dc

# Tái lập cùng thiết kế sang thư mục run mới (prepare cần mạng):
.venv/Scripts/python.exe -X utf8 tests/evaluate_external.py prepare
# Thay outputs/<run_moi> bằng đường dẫn SAMPLE_LOCKED vừa được in:
.venv/Scripts/python.exe -X utf8 tests/evaluate_external.py run --directory outputs/<run_moi>
.venv/Scripts/python.exe -X utf8 tests/evaluate_external.py verify --directory outputs/<run_moi>

.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
```

`prepare` với seed/các archive này tạo lại cùng100 ID để tái lập, không tạo một tập ngoài độc lập mới. `run` từ chối thư mục results đã có; không ghi đè. `verify` chỉ cập nhật bằng chứng verification/checksum, không thay sample lock/predictions/metrics. Script không được gọi từ app, không phải tính năng demo. Các bảng audit/gộp bổ sung được dẫn xuất từ CSV/JSON đã xuất, không thay kết quả suy luận.

Không dùng100 ảnh này hoặc10 ảnh cũ để tuning/chọn preprocessing/mô hình. Nghiên cứu sau cần một tập validation ngoài mới có quy trình chốt trước. Chưa đánh giá ảnh tự chụp hoặc chứng minh tách người viết. Việc commit/push kết quả mới chưa được thực hiện trong lượt đánh giá này; xem HANDOFF.
