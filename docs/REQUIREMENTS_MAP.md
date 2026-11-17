# Đối chiếu PDF và phạm vi hỗ trợ

Đã đọc toàn bộ `Huong_Dan_Do_An_CuoiKy.pdf` (6 trang). Bảng này hướng dẫn kiểm tra, không thay báo cáo. PDF nhắc BM06 nhưng project không có BM06; không suy đoán chi tiết chấm điểm ngoài bảng đã cung cấp.

## Yêu cầu chung và thang điểm

| Nguồn | Bằng chứng cần có | Vị trí / trạng thái phase hỗ trợ |
|---|---|---|
| Trang 1–2, quy trình 1–10 | Bài toán, nguồn, schema/tỷ lệ thiếu, làm sạch có lý do, EDA, đặc trưng, mô hình, đánh giá, phân tích lỗi, trình bày | Notebook 1–16; huấn luyện/nhận định còn TODO sinh viên |
| Trang 2, mục 4 | Báo cáo PDF/DOCX, mã chạy hết, requirements, README, slide, mô hình nếu demo; Git hoặc zip, môi trường sạch | Khung và môi trường được kiểm tra; bài nộp hoàn chỉnh, báo cáo/slide chưa có |
| Trang 2, mục 5 | Baseline, Pipeline fit train, seed, phiên bản và giải thích độ đo | Notebook 1,4,6–12,15; baseline là TODO, không có điểm giả |
| Trang 2, mục 6 | Khai báo AI, không toàn bộ code/phân tích do AI; hiểu và chỉnh sửa được bài | AI_USAGE.md; SV-01…SV-09 và mọi nhận định thuộc sinh viên |
| Câu 1: 4 điểm | Dữ liệu, baseline, làm sạch, ≥5 EDA có nhận định, đặc trưng không leakage, tái lập | Đã có 6 hình train; nhật ký/nhận định và code cốt lõi chờ nhóm |
| Câu 2: 4 điểm | ≥2 mô hình so baseline; split, metric, confusion matrix, CV/tuning, phân tích lỗi | Có hợp đồng và khung điều phối, chưa có thí nghiệm mô hình |
| Câu 3: 2 điểm | Trình bày, demo và vấn đáp từng thành viên | Nhóm chuẩn bị trực tiếp; phase này không Streamlit |

## Năm câu hỏi đề tài 13 (trang 5–6)

| Câu hỏi | Notebook | Nhóm cần tự trả lời từ bằng chứng |
|---|---|---|
| Biểu diễn vector/shape, vì sao chuẩn hóa pixel | 2,5,7–8 | Shape thực tế; reshape; đối chứng scaling cùng điều kiện; không đánh đồng Digits và MNIST |
| Baseline đạt bao nhiêu, MLP cải thiện ra sao | 6–11,15–16 | CV mean/std và test thật; chấp nhận MLP không cải thiện |
| Cặp nhầm từ confusion matrix | 13,15–16 | Số đếm, chiều thật→dự đoán, ảnh sai cụ thể |
| Learning curve cho thấy quá khớp ở đâu | 14 | Đường train/validation theo số mẫu; loss/validation theo epoch; chỉ kết luận nếu có bằng chứng |
| Chi phí và độ chính xác mô hình đơn giản/mạng nơ-ron | 12,15–16 | Fit cuối, predict cùng test, tuning riêng, dung lượng Pipeline cùng chuẩn joblib |

## Thứ tự thực thi và đầu ra

Mục 1–5 và cấu hình/hàm hỗ trợ chạy ngay. Mục 6–14 định nghĩa/gợi ý, không predict test. Mục 15 chỉ gọi sau khi nhóm triển khai TODO và xác nhận quy trình; chọn bằng CV, lưu selection_lock rồi đánh giá test. Mục 16 xuất số liệu thật và kiểm tra tải lại Pipeline. Cách sắp xếp giữ nguyên thứ tự trình bày 16 mục nhưng bảo vệ test.

Chỉ kết quả `run_status.json` có `student_experiments_completed=true` mới có thể chứa kết quả huấn luyện đã chạy. Giá trị này không xác nhận chất lượng nhận định hoặc sẵn sàng nộp; `ready_to_submit` mặc định false cho đến khi nhóm rà soát đầy đủ. File hỗ trợ và notebook hiện có không đủ để nộp hoàn chỉnh.
