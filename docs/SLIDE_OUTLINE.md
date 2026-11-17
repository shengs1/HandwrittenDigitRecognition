# Nội dung dự thảo 12 slide

**Chưa được nhóm xác nhận; chưa có PPTX/PDF nộp chính thức.** Run `20261117T081201Z_fd32180f`; nguồn bảng/hình tại [RESULTS_INDEX](RESULTS_INDEX.md). Mỗi slide 3–4 ý, hình đủ lớn; nhóm diễn đạt lại lời nói.

## 1. Đề tài

- Phân loại chữ số viết tay — đề tài 13.
- Lập trình cho Trí tuệ nhân tạo và Khoa học dữ liệu (04224).
- Nhóm/họ tên/MSSV/lớp/giảng viên: **[Chưa cung cấp — nhóm điền]**.

Hình/bảng: Một ảnh Digits 8×8.

Gợi ý lời nói: Nêu ngay dataset là Digits, MNIST chỉ fixture ngoài.

## 2. Bài toán và mục tiêu

- 8×8 → 64 pixel → nhãn 0–9.
- So LR thô, KNN, MLP; chuẩn hóa, lỗi và chi phí.
- Chọn mean CV macro F1; accuracy bổ sung tỷ lệ đúng.

Hình/bảng: Sơ đồ đầu vào → phân lớp.

Gợi ý lời nói: Macro F1 cân bằng vai trò 10 lớp; không buộc MLP thắng.

## 3. Dataset

- load_digits: 1.797 mẫu, X float64/y int64, pixel 0–16.
- Nguồn scikit-learn/UCI; thiếu 0% từng cột.
- Train/test 1.437/360, stratify=y, seed 42.

Hình/bảng: data_summary và split_summary.

Gợi ý lời nói: Float64 hợp lệ vì giá trị pixel là số nguyên.

## 4. Kiểm tra và làm sạch

- Không sai miền/nhãn, ảnh hằng, trùng hoặc nhãn mâu thuẫn.
- Không trùng xuyên train/test/CV.
- Giữ 1747/818/1766: số 1 nét dày, cờ IQR không chứng minh lỗi.

Hình/bảng: Ba ảnh IQR (train) và bảng kiểm tra.

Gợi ý lời nói: Giữ nguyên dữ liệu là quyết định có bằng chứng; không cần imputer.

## 5. EDA train

- Lớp 139–146 mẫu; 48,86% pixel bằng 0.
- Ảnh trung bình có vùng nét chung; std cao ở nhiều vị trí bên trong.
- PCA 2D giữ 28,50% phương sai, nhiều lớp chồng lấn.

Hình/bảng: EDA lớp + ảnh trung bình + PCA; các hình khác để phụ lục.

Gợi ý lời nói: Báo cáo đủ 6 EDA; PCA chỉ quan sát, không suy ra accuracy.

## 6. Pipeline và đánh giá

- Train → StratifiedKFold 5/shuffle/42 → GridSearchCV → khóa → test.
- Scaler fit train fold; test không tuning.
- Precision/recall/F1 macro, accuracy, report và confusion matrix.

Hình/bảng: Sơ đồ chuỗi trên.

Gợi ý lời nói: CV sau lựa chọn có thiên lệch; validation nội bộ MLP khác outer fold.

## 7. Ba mô hình và chuẩn hóa

- LR: passthrough, C=1/lbfgs.
- KNN: StandardScaler, k=3/uniform; grid 6 cấu hình.
- MLP: (64,32), relu/adam, alpha=0.0001, early stopping; grid 4.
- MLP scaling CV F1: 94,3452%→ 96,2365%,+1,8913 điểm phần trăm.

Hình/bảng: Bảng cấu hình + scaling mean/std.

Gợi ý lời nói: Khoảng 2,00% tương đối, không gọi là tăng accuracy test.

## 8. Kết quả và chi phí

- CV F1 LR/KNN/MLP: 96,3687/97,6170/96,2365%.
- Accuracy test: 95,8333/96,6667/96,1111%; KNN khóa trước test.
- Fit(s): 0,098705/0,003107/0,279319; predict 360 ảnh(s): 0,000798/0,004730/0,001538.
- LR nhỏ nhất5.935 byte; MLP tuning4,231378s, KNN 0,635378s.

Hình/bảng: model_comparison.csv/png; ghi một máy/một luồng, median5 predict.

Gợi ý lời nói: KNN lưu mẫu nên fit nhanh nhưng predict chậm; không luôn thắng mọi bài toán.

## 9. Lỗi và đường cong học

- Sai15/12/14 ảnh; 8→ 1 có 4/3/3 lần; KNN 4→ 7 hai lần.
- Gap cuối train−validation: 3,70/1,15/3,11 điểm phần trăm; validation tăng theo mẫu.
- MLP 52 iterations, validation nội bộ bão hòa; chưa xác định epoch quá khớp.

Hình/bảng: Confusion KNN + ảnh 1553/1022 + learning curve; history để phụ lục.

Gợi ý lời nói: Mô tả nét chỉ là giả thuyết; không sửa model sau test.

## 10. Demo

- Chọn model và Ảnh test Digits đúng split lưu.
- Upload: ảnh gốc/8×8/0–16, dự đoán và xác suất10 lớp.
- Không fit/scale hai lần; file hỏng/trống/mất model báo lỗi.
- 10 MNIST đã thử: 3/10 đúng mỗi model; xác suất chưa hiệu chỉnh.

Hình/bảng: Screenshot thật lượt kiểm tra cuối.

Gợi ý lời nói: Mẫu test đã xem không là đánh giá độc lập mới; chuẩn bị ảnh offline dự phòng.

## 11. Giới hạn và hướng sau

- Digits nhỏ/8×8; random split chưa bảo đảm tách người viết.
- CV dùng chọn tham số; timing phụ thuộc máy.
- 10 ảnh ngoài ít, chưa có ảnh tự chụp; kiểu nét/nền có thể khác.
- Thu ảnh có nhãn, chốt quy trình rồi đánh giá tập ngoài mới.

Hình/bảng: Một ví dụ ảnh ngoài sai, có nguồn fixture.

Gợi ý lời nói: Tiền xử lý hợp lệ không bảo đảm cùng phân phối; không tuning10 ảnh đã xem.

## 12. Kết luận và phân công

- Đủ quy trình6 EDA, baseline+KNN/MLP, scaling/CV/grid/lỗi/curves/demo.
- KNN tốt nhất run này; LR gọn; MLP chưa có lợi thế tổng thể.
- Đối chiếu5 câu trả lời cuối notebook.
- Phân công thật:**[Nhóm điền người, việc, bằng chứng]**.

Hình/bảng: Bảng phân công sau nhóm xác nhận.

Gợi ý lời nói: Mỗi thành viên tập mở code/CSV, giải thích và thay đổi ở bản thử riêng.

Có thể gộp3–4 và 11–12 thành10 slide. Ghi metric/tập/run_id/nguồn dưới hình; std CV không phải CI. Không ghi đóng góp chưa xác nhận.
