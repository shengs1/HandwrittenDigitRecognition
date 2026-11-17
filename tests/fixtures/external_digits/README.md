# Ảnh viết tay bên ngoài Digits để kiểm thử demo

10 ảnh thật từ **tập test MNIST**, tác giả dữ liệu Yann LeCun, Corinna Cortes và Christopher J. C. Burges; nguồn tải là [mirror CVDF](https://github.com/cvdfoundation/mnist). Thông tin bộ dữ liệu và kích thước ảnh tham khảo [TensorFlow Datasets](https://www.tensorflow.org/datasets/catalog/mnist). Không cần cài TensorFlow.

Quy tắc lấy mẫu đặt trước dự đoán: ảnh đầu tiên của mỗi nhãn 0–9 theo thứ tự gốc của tập test. `manifest.json` ghi index, nhãn, URL nguồn, checksum file nguồn và PNG trích xuất. Không chọn lại ảnh để đạt kết quả đẹp. Các ảnh chỉ dùng để thử đường upload/tiền xử lý/suy luận; không dùng huấn luyện, CV, chọn tham số, scaler hay mô hình. Dữ liệu huấn luyện dự án vẫn chỉ là `load_digits()`.

MNIST khác Digits (28×28 so với 8×8), vì vậy thử nghiệm này có thể sai nhiều hơn và không đại diện ảnh chụp điện thoại. Biến thể đảo màu là kiểm tra chức năng cùng ảnh, không phải mẫu độc lập bổ sung. Nhóm cần bổ sung ảnh tự chụp nếu muốn khẳng định chất lượng với ảnh thực tế.
