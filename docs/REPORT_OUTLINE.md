# Dàn ý báo cáo theo đúng 10 mục PDF

Cấu trúc theo mục 7, trang 2 của `Huong_Dan_Do_An_CuoiKy.pdf`. Đây là dàn ý và danh mục bằng chứng; nhóm tự viết nhận định, lý giải, kết luận và đóng góp thật. Run sử dụng: `20261117T081201Z_fd32180f`, chỉ mục nguồn tại RESULTS_INDEX.md.

## 1. Trang bìa

Tên đề tài 13; học phần/lớp/giảng viên; tên nhóm, thành viên và mã sinh viên thật. Ngày nộp theo lịch giảng viên, không suy đoán.

## 2. Giới thiệu bài toán và mục tiêu

Phân lớp 0–9, ảnh 8×8 thành vector 64 pixel; phân biệt Digits/MNIST. Mục tiêu đặt trước: so baseline thô với KNN/MLP, chuẩn hóa, lỗi và chi phí. Chọn mean CV macro F1 cao nhất, hòa tuyệt đối theo tên tăng dần. Nhóm tự giải thích ứng dụng, tiêu chí và lựa chọn metric; không đặt mục tiêu “MLP nhất định tốt hơn”.

## 3. Dữ liệu và làm sạch

Nguồn load_digits/UCI ở notebook mục 2. Dẫn data_summary.json, column_schema.csv (tỷ lệ thiếu từng cột), data_quality.json, split_summary.json, cv_fold_audit.csv. Nêu 1.797 mẫu/64 đặc trưng, pixel 0–16, nhãn 0–9, không thiếu/trùng theo kiểm tra. 3 ảnh train có cờ IQR độ sáng không tự bị xóa.

Nhóm tự viết nhật ký giữ nguyên dữ liệu, bằng chứng xem ảnh và vì sao float64 chứa giá trị nguyên vẫn hợp lệ. Không dùng test thay chính sách làm sạch.

## 4. Khám phá và trực quan hóa

Đưa 6 hình EDA train: lớp, ảnh mẫu, histogram, ảnh trung bình, std heatmap, PCA 2D. Mỗi hình đủ tiêu đề/trục/chú thích và có nhận định do nhóm viết. PCA giữ khoảng 28,50% phương sai 2D, chỉ là EDA, không dùng trong mô hình. Tự bàn luận cân bằng lớp, nét/nền, biến thiên và giới hạn chiếu 2D; không suy ra accuracy từ PCA.

## 5. Phương pháp

Train/test 80/20 stratify seed 42; CV 5 folds shuffle seed 42. Baseline LR passthrough C=1, max_iter=3000. KNN/MLP Pipeline; scaler học theo fold. MLP ban đầu (64,32)/relu/adam/early stopping; đối chứng scaler cùng điều kiện. Grid nhỏ như notebook, chỉ chọn bằng train/CV.

Giải thích scaler fit train fold trước khi MLP tự chia validation nội bộ; khác outer validation/test. CV sau tuning có thiên lệch lựa chọn. Fit cuối đo riêng, predict median 5 lần sau warm-up, tuning wall time và bytes joblib compress=3.

## 6. Kết quả và so sánh baseline

Chèn model_comparison.csv và bảng scaling từ mlp_scaling_cv.csv. Tách CV mean/std khỏi test; KNN khóa bằng selection_lock trước test. Tách tuning khỏi fit cuối; baseline tuning=0 không có nghĩa CV miễn phí. Nhóm tự phân tích chênh lệch, độ ổn định và chi phí; không chọn lại mô hình theo test.

## 7. Phân tích lỗi và giới hạn

Ma trận nhầm lẫn cả 3, bảng cặp có hướng và ảnh sai. Dùng learning_curves.png/learning_curve.csv, mlp_training_history.png/mlp_history.json để tự đánh giá bằng chứng overfitting; có thể kết luận chưa đủ bằng chứng, không ép một điểm quá khớp.

Giới hạn: mẫu nhỏ, 8×8, chia ngẫu nhiên không bảo đảm tách người viết, CV dùng chọn tham số, xác suất chưa hiệu chỉnh. 10 MNIST chọn trước: mỗi model đúng 3/10; không suy ra accuracy ảnh chụp. Chưa có ảnh tự chụp; không loại hoặc giấu mẫu sai.

## 8. Triển khai demo

Chụp giao diện thật: chọn model/mẫu/upload, ảnh gốc/sau xử lý, dự đoán/xác suất. Mô tả ảnh→8×8/0–16, không chuẩn hóa hai lần, mẫu Digits giữ nguyên. App chỉ load Pipeline; registry/checksum/cache; lỗi file hỏng/trống/mất model. Không backend riêng hoặc train trong UI.

## 9. Kết luận

Nhóm tự trả lời 5 câu hỏi bằng số liệu đã dẫn; phần làm được/chưa kiểm chứng. Cải tiến chỉ đề xuất cho nghiên cứu sau (ảnh thật, đánh giá độc lập, tiền xử lý phù hợp hơn); không tuning mới sau test của thí nghiệm này.

## 10. Phân công, tài liệu tham khảo và phụ lục

Bảng thành viên/công việc/bằng chứng commit hoặc cell/ngày/thời lượng do nhóm tự ghi. Tham khảo PDF học phần; API scikit-learn, UCI; Streamlit/Pillow; nguồn fixture CVDF MNIST. Phụ lục: requirements, lệnh, run_id/checksum, CV/report, cấu hình và nhật ký kiểm thử. Không có BM06 trong project để suy đoán thêm chi tiết chấm điểm.
