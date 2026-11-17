# Nhật ký sử dụng AI

## Đã xác minh trong phiên 2026-11-17

| Công cụ | Công việc hỗ trợ thực tế | Giới hạn |
|---|---|---|
| OpenAI Codex | Đọc toàn bộ PDF; đề xuất cấu trúc; tạo khung notebook 16 mục; mã hỗ trợ kiểm tra dữ liệu, split, EDA, đo thời gian/lưu kết quả; tài liệu, kiểm tra khung và sửa lỗi phát hiện khi chạy | Không hoàn thành thay nhóm các TODO SV-01…SV-09; không viết nhận định thực nghiệm hoặc tạo điểm mô hình |

Codex đã tra tài liệu API chính thức scikit-learn. Các lệnh/kết quả kiểm tra thực tế ghi trong `HANDOFF.md`. Mã hỗ trợ và tài liệu hiện tại do AI tạo; không trình bày là đóng góp của sinh viên. Kiểm thử khung hỗ trợ không phải thí nghiệm huấn luyện mô hình.

Sau khi người dùng thông báo tạo repo GitHub `shengs1/HandwrittenDigitRecognition`, Codex kiểm tra Git cục bộ/remote ở chế độ chỉ đọc và cập nhật liên kết, trạng thái trong tài liệu. Ở bước đó chưa init, commit hoặc push. Việc tạo repo được người dùng thông báo; chưa có thông tin để gán công việc này cho một thành viên sinh viên cụ thể.

Theo yêu cầu tiếp theo của người dùng, Codex đã khởi tạo Git nhánh `main`, liên kết `origin`, kiểm tra file bị loại bởi `.gitignore` và chạy lại 8 kiểm tra hợp đồng (đều qua), chuẩn bị commit/push bản khung. Kết quả push và kiểm tra đồng bộ sẽ ghi trong `HANDOFF.md`; không coi các thao tác Git là đóng góp triển khai thuật toán của nhóm.

## Đóng góp thực tế của nhóm sinh viên

**Chưa có thông tin được xác minh về thành viên hoặc đóng góp triển khai.** Không ghi tên, vai trò, phần code hoặc nhận định giả định. Nhóm điền bảng này sau khi thực hiện, kèm cell/commit/bằng chứng:

| Thành viên | Ngày | Công việc đã thực sự làm | Cell/file/commit làm bằng chứng | Đã tự giải thích được |
|---|---|---|---|---|
| Chưa cung cấp | — | Chưa xác minh | — | Chưa xác minh |

## Những phần phải do nhóm thực hiện

Nhóm trực tiếp triển khai Pipeline, đối chứng scaling, CV/tuning, độ đo, phân tích lỗi, learning curve và lựa chọn bằng CV; tự viết nhật ký xử lý, 6 nhận định EDA, phân tích kết quả/giới hạn và báo cáo/slide. Mỗi thành viên cần hiểu, chỉnh sửa và bảo vệ toàn bộ bài. Việc sửa tên biến hoặc chép lời giải AI không thay thế học và đóng góp thực tế.

## Phiên hỗ trợ tiếp theo

Sau mỗi phiên, ghi đúng tên công cụ (Codex, Antigravity hoặc công cụ khác), yêu cầu đã hỏi, phần được gợi ý/sửa, cách nhóm kiểm chứng và phần nhóm tự triển khai. **Antigravity chưa được sử dụng trong phiên này**; không ghi như đã có hỗ trợ.
