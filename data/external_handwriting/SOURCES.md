# Nguồn 600 ảnh viết tay ngoài Digits

Lấy mẫu seed42 trước suy luận:20 ảnh/chữ số/nguồn, chia10 validation+10 test. Mỗi tập300 ảnh; mỗi nguồn100/tập. Giữ nguyên bytes tải từ repository gốc, không resize/làm sạch file cấp cho preprocessing. PNG contact sheet chỉ là bản xem. Manifest ghi đường dẫn, nhãn tác giả, tên/path gốc, mode/kích thước, SHA256 byte và pixel, commit và split. sample_lock.json khóa manifest lúc18:01:14UTC18/11 (01:01:14 ngày19/11/2026 Việt Nam).

| Nguồn | Commit tải | Quyền sử dụng dữ liệu | Bản chất ảnh |
|---|---|---|---|
|[BHMSDS](https://github.com/wblachowski/bhmsds)|07d208e41923b061e338c241e59daacdd2752d53|MIT, copyright2019 wblachowski, giữ LICENSE|Một vài người điền giấy; tác giả chụp, cắt, lọc và resize28×28. Đây là ảnh giấy đã xử lý, không phải ảnh điện thoại nguyên bản. Chỉ lấy symbols/0–9.|
|[Bitmap Numbers](https://github.com/KentoNishi/Bitmap-Numbers-Dataset)|b83f099dd981cda1933f27726021594fa6995bb4|Repo dẫn xuất không có LICENSE riêng; README quy chiếu toàn bộ mẫu về kensanata/numbers public-domain; upstream LICENSE.md xác nhận CC0-1.0.|Ảnh scan giấy, tác giả đổi PDF→PNG→BMP và resize128×128 RGB. Có màu, méo tỷ lệ/lề/artifact có sẵn. Không sửa chúng khi thu thập.|
|[HwD-1000](https://github.com/niklashenning/hwd-1000-dataset)|93b3ba9e45624ee557360229a42298eaa6b3a106|MIT, copyright2024 Niklas Henning, giữ LICENSE|Chữ do người vẽ thủ công bằng bút số trên nền trắng28×28, nhiều độ rộng/style; không phải ảnh giấy/ảnh camera và không phải font sinh tự động. Nhãn từ dataset.csv đối chiếu tên file.|

README/LICENSE gốc lưu ở provenance/<source>/. Bản [numbers upstream](https://github.com/kensanata/numbers) được kiểm tại fb1f8fb90eddd4c43b22bbbdff7d146cfafc2d3a; LICENSE.md/README lưu dưới bitmap_numbers/upstream_numbers. Upstream có cả tập tự động lẫn chữ in; bản Bitmap dẫn xuất tự mô tả mẫu của nó là chữ viết tay nhưng không giữ mapping về tập/người viết. Sáu contact sheet đã được xem để kiểm hình dạng/nhãn; không thấy mẫu rõ ràng là chữ in/font/AI/MNIST trong600 ảnh được chọn. Không thể xác minh đầy đủ lịch sử từng ảnh của bản dẫn xuất chỉ từ README và tên file tuần tự; đây là giới hạn nguồn gốc cần nêu khi bảo vệ.

Không sử dụng MNIST/ảnh AI/font để đủ600 ảnh. 31.200 ảnh chữ số ứng viên gồm15.000 BHMSDS,15.200 Bitmap,1.000 HwD. Kiểm đọc/nhãn/ảnh hằng, SHA256 và decoded RGBA pixel:0 ảnh hỏng,0 trùng,0 conflicting label trong pool này. Chỉ chọn nhãn0–9; không chọn theo dự đoán. provenance/inventory.csv và các CSV invalid/duplicate/conflicting lưu toàn bộ kết quả kiểm.

Không có writer/sheet ID đáng tin trong3 repository được lấy. Số thứ tự file không được xem là writer ID. Upstream numbers có metadata người viết nhưng bản Bitmap đã làm mất mapping; không gán đoán người viết. Do đó chia ngẫu nhiên theo ảnh, kiểm exact pixel không giao hai tập; không tuyên bố tách người viết hoặc độc lập style. Không loại ảnh chỉ vì nét giống chữ khác, nhạt, khó hoặc sau này dự đoán sai.

Contact sheets:6 trang, mỗi trang100 ảnh, bao phủ600 ảnh. Nhãn lấy từ tác giả, review hình chỉ để kiểm tính hợp lệ. Một số kiểu1/4/7, số2 có vòng và nét5 mảnh dễ gây nhầm; giữ nguyên mẫu/nhãn. Test đã được xem ở mức kiểm dữ liệu theo yêu cầu, không dùng dự đoán/test metrics để chọn preprocessing. Việc nhìn contact sheet không chứng minh tính mù hoàn toàn của con người; giới hạn này được ghi rõ.

Lệnh lấy mẫu từ gốc repo: `.venv/Scripts/python.exe -X utf8 tests/collect_external_handwriting.py`. Script tải archive ở commit/digest cố định nếu cache tmp chưa có, không chạy code trong repository nguồn. Từ chối ghi đè manifest đã khóa. Phiên bản script chỉ đổi font contact sheet sang font mặc định Pillow để chạy không cần đường dẫn Windows; mẫu và bytes ảnh không đổi.
