# Ảnh viết tay bên ngoài Digits để kiểm thử demo

Cập nhật phạm vi tài liệu23/11/2026; ảnh vàmanifest gốc giữ nguyên. Đây là **10 fixture MNIST lịch sử** cho kiểm hồi quy,không phải tập đánh giá của bản tối ưu hiện tại. Không cần tải lại hoặc chọn mẫu mới để chạy app.

10 ảnh thật từ **tập test MNIST**, tác giả dữ liệu Yann LeCun, Corinna Cortes và Christopher J. C. Burges; nguồn tải là [mirror CVDF](https://github.com/cvdfoundation/mnist). Thông tin bộ dữ liệu và kích thước ảnh tham khảo [TensorFlow Datasets](https://www.tensorflow.org/datasets/catalog/mnist). Không cần cài TensorFlow.

Quy tắc lấy mẫu đặt trước dự đoán: ảnh đầu tiên của mỗi nhãn0–9 theo thứ tự gốc của tập kiểm tra. `manifest.json` ghi ID,nhãn,URL vàchecksum ảnh/nguồn. Không chọn lại để đạt điểm đẹp. Các ảnh chỉ dùng kiểm đường tải ảnh/tiền xử lý/suy luận,không dùng huấn luyện hoặc tuning. Ba Pipeline chính thức của phần A chỉ học `load_digits()`; phần B có MLP riêng học54.000 ảnh MNIST train,không học từ10 fixture này. Cả10 ID này cùng100 ID của lượt kiểm tra sau đã được loại khỏi9.890 MNIST test cuối của phần B.

MNIST khác Digits (28×28 so với 8×8), vì vậy thử nghiệm này có thể sai nhiều hơn và không đại diện ảnh chụp điện thoại. Biến thể đảo màu là kiểm tra chức năng cùng ảnh, không phải mẫu độc lập bổ sung. Nhóm cần bổ sung ảnh tự chụp nếu muốn khẳng định chất lượng với ảnh thực tế.

`tests/check_demo.py` giữ kiểm hồi quy baseline bằng các fixture này; không dùng điểm3/10 cũ thay độ chính xác của mô hình mới. Kết quả mở rộng và giới hạn ở [RESULTS_INDEX](../../../docs/RESULTS_INDEX.md). Chưa có ảnh tự chụp của nhóm được xác nhận.

Ghi công MNIST và điều kiện CC BY-SA3.0 cho dữ liệu/ảnh biến đổi được nêu trong [SOURCES của thực nghiệm mở rộng](../../../outputs/external_optimization_20261118T175401Z_4ca3a08f/SOURCES.md). Giữ nguồn,checksum vàghi công khi phân phối fixture;không gán giấy phép thư viện cho dữ liệu.
