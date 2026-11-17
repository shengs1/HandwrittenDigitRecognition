# Gợi ý 12 slide

Dùng đúng run `20261117T081201Z_fd32180f`, hình/bảng trong RESULTS_INDEX.md. Nhóm tự viết lời thuyết trình và kết luận.

| Slide | Nội dung | Bằng chứng / hình |
|---:|---|---|
| 1 | Đề tài, nhóm/lớp thật, mục tiêu | Bìa, một ảnh Digits |
| 2 | Phân lớp 0–9, tiêu chí, baseline | 8×8→64; quy tắc CV đặt trước |
| 3 | Nguồn/chất lượng/split | summary/quality/split; 1797→1437/360 |
| 4 | EDA: lớp và ảnh | eda_01, eda_02; nhận định nhóm |
| 5 | EDA: pixel/trung bình/std/PCA | Chọn eda_03…06; hình còn lại ở phụ lục |
| 6 | Phương pháp/chống leakage | Train→CV Pipeline→khóa→test; 3 mô hình |
| 7 | Scaling và tuning | Scaling CV, grid 6 KNN/4 MLP, mean/std |
| 8 | Kết quả/chi phí | model_comparison.csv/png; chọn KNN trước test |
| 9 | Lỗi | Confusion matrix và 2–3 ảnh sai thật |
| 10 | Learning curve/giới hạn | Learning curves và MLP history; không ép kết luận overfitting |
| 11 | Demo/kiểm thử bên ngoài | Mẫu/upload; 10 MNIST chỉ 3/10 đúng mỗi model |
| 12 | Kết luận/phân công | 5 câu hỏi, ảnh chụp chưa thử, đóng góp thật |

Giữ hình đủ lớn, ít ý; ghi metric/tập dữ liệu/run_id/nguồn. Không lấy accuracy mẫu demo thay test. Tách thời gian fit/predict/tuning; std CV không phải khoảng tin cậy. Nếu cần 10 slide, gộp 4–5 và 9–10. Tập demo offline; giữ notebook/PNG làm phương án dự phòng.
