# Đối chiếu PDF và phạm vi hỗ trợ

Đã đọc toàn bộ `Huong_Dan_Do_An_CuoiKy.pdf` (6 trang). Bảng này hướng dẫn kiểm tra, không thay báo cáo. Trạng thái mới nhất ở bảng Final Completion đầu FINAL_REVIEW: đã có dự thảo nhật ký/6 EDA/phân tích/5 câu hỏi, chưa nhóm xác nhận; báo cáo10 mục/12 slide mới là nội dung Markdown, chưa file nộp. PDF nhắc BM06 nhưng project không có BM06; không suy đoán chi tiết chấm điểm ngoài bảng đã cung cấp.

Kết quả kiểm tra cuối có trạng thái PASS/FAIL/PARTIAL và bằng chứng thực thi: [FINAL_REVIEW.md](FINAL_REVIEW.md). Bảng hướng dẫn dưới đây không thay cho trạng thái review và không chứng minh nhóm đã hoàn thành nhận định/báo cáo/vấn đáp.

Phạm vi cập nhật theo yêu cầu mới: không đánh giá mục 6 của PDF; vẫn giữ kiểm tra notebook/code. Bản tổng hợp A–I: [FINAL_AUDIT.md](FINAL_AUDIT.md).

## Yêu cầu chung và thang điểm

| Nguồn | Bằng chứng cần có | Vị trí / trạng thái phase hỗ trợ |
|---|---|---|
| Trang 1–2, quy trình 1–10 | Bài toán, nguồn, schema/tỷ lệ thiếu, làm sạch có lý do, EDA, đặc trưng, mô hình, đánh giá, phân tích lỗi, trình bày | Notebook 1–16 đã chạy thực nghiệm; nhận định/báo cáo chính do nhóm viết |
| Trang 2, mục 4 | Báo cáo PDF/DOCX, mã chạy hết, requirements, README, slide, mô hình nếu demo; Git hoặc zip, môi trường sạch | Có notebook/Pipeline/demo và dàn ý báo cáo/slide; chưa có báo cáo hoặc slide nộp chính thức |
| Trang 2, mục 5 | Baseline, Pipeline fit train, seed, phiên bản và giải thích độ đo | Notebook 1,4,6–12,15; đủ 3 mô hình đã chạy, khóa lựa chọn bằng CV |
| Câu 1: 4 điểm | Dữ liệu, baseline, làm sạch, ≥5 EDA có nhận định, đặc trưng không leakage, tái lập | Đã có 6 hình train và code cốt lõi; nhóm hoàn thiện nhật ký/nhận định |
| Câu 2: 4 điểm | ≥2 mô hình so baseline; split, metric, confusion matrix, CV/tuning, phân tích lỗi | Đã chạy run cố định; hình/bảng thật trong RESULTS_INDEX; nhóm viết phân tích |
| Câu 3: 2 điểm | Trình bày, demo và vấn đáp từng thành viên | Có Streamlit, dàn ý 12 slide và 30 câu hỏi; nhóm tập bảo vệ |

## Năm câu hỏi đề tài 13 (trang 5–6)

| Câu hỏi | Notebook | Nhóm cần tự trả lời từ bằng chứng |
|---|---|---|
| Biểu diễn vector/shape, vì sao chuẩn hóa pixel | 2,5,7–8 | Shape thực tế; reshape; đối chứng scaling cùng điều kiện; không đánh đồng Digits và MNIST |
| Baseline đạt bao nhiêu, MLP cải thiện ra sao | 6–11,15–16 | CV mean/std và test thật; chấp nhận MLP không cải thiện |
| Cặp nhầm từ confusion matrix | 13,15–16 | Số đếm, chiều thật→dự đoán, ảnh sai cụ thể |
| Learning curve cho thấy quá khớp ở đâu | 14 | Đường train/validation theo số mẫu; loss/validation theo epoch; chỉ kết luận nếu có bằng chứng |
| Chi phí và độ chính xác mô hình đơn giản/mạng nơ-ron | 12,15–16 | Fit cuối, predict cùng test, tuning riêng, dung lượng Pipeline cùng chuẩn joblib |

## Thứ tự thực thi và đầu ra

Mục 1–5 kiểm tra dữ liệu/EDA. Mục 6–14 định nghĩa hàm và cấu hình, không predict test. Mục 15 thực thi: chọn bằng CV, lưu selection_lock rồi đánh giá test. Mục 16 xuất số liệu và kiểm tra tải lại Pipeline. Giữ đúng thứ tự 16 mục nhưng bảo vệ test.

Run xác nhận `20261117T081201Z_fd32180f` có `experiments_completed=true`; ba run support cũ không có điểm mô hình. Trạng thái này không xác nhận chất lượng nhận định hoặc sẵn sàng nộp: ready_to_submit vẫn false để nhóm rà soát báo cáo/phân công. App chỉ load registry/Pipeline của run cố định, không train; 10 MNIST test chỉ dùng kiểm thử ngoài Digits.
