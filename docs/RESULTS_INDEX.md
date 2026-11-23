# Chỉ mục số liệu và hình cho báo cáo

Cập nhật tài liệu 23/11/2026. Bảng/hình A/B giữ từ các run đã khóa, không tính lại hoặc huấn luyện mới để đổi kết quả. Code giao diện `f47a709` dùng tên model tiếng Anh và nhãn tiếng Việt; các ảnh chụp trong outputs/ giữ đúng thời điểm tạo nên có thể có chữ cũ. Đối chiếu trạng thái kiểm thử và phần còn thiếu ở [FINAL_REVIEW](FINAL_REVIEW.md).

**A — Thực nghiệm chính Digits:** các mục1–10 giữ số liệu run chính thức. **B — Mở rộng ảnh ngoài:** mục11 bên dưới, không thay kết quả hoặc lựa chọn KNN của phầnA. Code/UI/thực nghiệm đã chốt; nhận định vẫn cần nhóm rà/xác nhận trước xuất bản nộp.

Run thực nghiệm cố định: **20261117T081201Z_fd32180f**; nguồn thật trong [outputs](../outputs/20261117T081201Z_fd32180f/).
Quy tắc và thời điểm khóa: [selection_lock.json](../outputs/20261117T081201Z_fd32180f/selection_lock.json).
Mô hình mặc định **knn** được chọn bằng CV trước test.
Các bảng và nhận định dưới là dự thảo có nguồn thật, chưa được nhóm xác nhận. Không dùng ba run support cũ làm điểm mô hình.

## 1. Dữ liệu

1.797 mẫu, 64 pixel, ảnh 8×8; float64 cho X, int64 cho y; nhãn 0–9, pixel 0–16.
Train 1.437/test 360; stratify=y, seed 42. Các kiểm tra thiếu, sai miền/nhãn, trùng đều 0.
Ba id train có cờ IQR độ sáng: 1747,818,1766; không bị loại.
Nguồn: [summary](../outputs/20261117T081201Z_fd32180f/data_summary.json), [schema/tỷ lệ thiếu từng cột](../outputs/20261117T081201Z_fd32180f/column_schema.csv),
[quality](../outputs/20261117T081201Z_fd32180f/data_quality.json), [split](../outputs/20261117T081201Z_fd32180f/split_summary.json),
[kiểm tra CV](../outputs/20261117T081201Z_fd32180f/cv_fold_audit.csv), [chẩn đoán ảnh](../outputs/20261117T081201Z_fd32180f/train_image_diagnostics.csv).

## 2. Độ đo CV và test

Nguồn: [model_comparison.csv](../outputs/20261117T081201Z_fd32180f/model_comparison.csv). CV mean/std là macro F1, ddof=0.
Mỗi điểm test dùng cùng 360 ảnh. CV sau tuning có thiên lệch lựa chọn.

| Mô hình | CV mean | CV std | Accuracy test | Precision macro | Recall macro | F1 macro |
|---|---|---|---|---|---|---|
| logreg_raw | 0.963687 | 0.007866 | 0.958333 | 0.958731 | 0.958012 | 0.958075 |
| knn | 0.976170 | 0.007575 | 0.966667 | 0.967759 | 0.966424 | 0.966304 |
| mlp | 0.962365 | 0.008314 | 0.961111 | 0.961798 | 0.960944 | 0.960888 |

## 3. Chi phí (cùng máy, một luồng thư viện tính toán)

Fit cuối một lần; predict median 5 lần trên cùng test sau warm-up; tuning là wall time riêng, refit=False.
Bytes là joblib nén mức 3 của toàn Pipeline. Baseline tuning=0 vì không tìm tham số, vẫn có chi phí CV.
Nguồn: [bảng tổng hợp](../outputs/20261117T081201Z_fd32180f/model_comparison.csv), [từng lần predict](../outputs/20261117T081201Z_fd32180f/timing_details.json).

| Mô hình | Fit cuối (s) | Predict median (s) | Tuning (s) | Pipeline (bytes) |
|---|---|---|---|---|
| logreg_raw | 0.098705 | 0.000798 | 0.000000 | 5935 |
| knn | 0.003107 | 0.004730 | 0.635378 | 140738 |
| mlp | 0.279319 | 0.001538 | 4.231378 | 159039 |

## 4. Cấu hình đã khóa

| Mô hình | Preprocessing | Cấu hình |
|---|---|---|
| logreg_raw | passthrough | C=1.0, solver=lbfgs, max_iter=3000 |
| knn | StandardScaler | k=3, weights=uniform |
| mlp | StandardScaler | hidden=(64,32), alpha=0.0001, relu/adam, early_stopping=True, max_iter=300 |

Nguồn: Pipeline được registry trỏ tới và [metadata](../models/20261117T081201Z_fd32180f/metadata.json); seed 42.


## 5. Đối chứng MLP scaling

Nguồn: [10 hàng CV](../outputs/20261117T081201Z_fd32180f/mlp_scaling_cv.csv); cùng MLP_INITIAL/folds/seed.

| Điều kiện | Mean macro F1 | Std macro F1 (ddof=0) |
|---|---|---|
| raw | 0.943452 | 0.018458 |
| standard | 0.962365 | 0.008314 |

## 6. Các cặp nhầm có hướng nhiều nhất

Chỉ số đếm thực, thật → dự đoán; hòa xếp theo nhãn. Nhóm cần kiểm tra và xác nhận phần phân tích dự thảo cuối tài liệu.


### logreg_raw

Nguồn: [toàn bộ cặp](../outputs/20261117T081201Z_fd32180f/confusion_pairs_logreg_raw.csv), [ảnh sai/id](../outputs/20261117T081201Z_fd32180f/misclassified_logreg_raw.csv).

| Thật | Dự đoán | Số lần |
|---|---|---|
| 8 | 1 | 4 |
| 1 | 8 | 3 |
| 0 | 2 | 1 |
| 1 | 3 | 1 |
| 5 | 3 | 1 |

### knn

Nguồn: [toàn bộ cặp](../outputs/20261117T081201Z_fd32180f/confusion_pairs_knn.csv), [ảnh sai/id](../outputs/20261117T081201Z_fd32180f/misclassified_knn.csv).

| Thật | Dự đoán | Số lần |
|---|---|---|
| 8 | 1 | 3 |
| 4 | 7 | 2 |
| 1 | 2 | 1 |
| 3 | 2 | 1 |
| 7 | 2 | 1 |

### mlp

Nguồn: [toàn bộ cặp](../outputs/20261117T081201Z_fd32180f/confusion_pairs_mlp.csv), [ảnh sai/id](../outputs/20261117T081201Z_fd32180f/misclassified_mlp.csv).

| Thật | Dự đoán | Số lần |
|---|---|---|
| 8 | 1 | 3 |
| 9 | 8 | 2 |
| 0 | 4 | 1 |
| 1 | 2 | 1 |
| 1 | 3 | 1 |

## 7. Learning curve và lịch sử MLP

Nguồn: [curve](../outputs/20261117T081201Z_fd32180f/learning_curve.csv), [điểm từng fold](../outputs/20261117T081201Z_fd32180f/learning_curve_folds.csv), [history](../outputs/20261117T081201Z_fd32180f/mlp_history.json).

| Mô hình | Số mẫu train/fold cuối | Train mean | Validation mean | Validation std |
|---|---|---|---|---|
| logreg_raw | 1149 | 1.000000 | 0.963021 | 0.007842 |
| knn | 1149 | 0.987642 | 0.976170 | 0.007575 |
| mlp | 1149 | 0.981695 | 0.950548 | 0.016079 |

MLP chạy 52 iterations; best validation accuracy nội bộ 0.979167. Không phải macro F1 CV. Bảng này không tự kết luận overfitting.


## 8. Chỉ mục hình

- [Phân bố lớp train](../outputs/20261117T081201Z_fd32180f/figures/eda_01_class_distribution.png)
- [Ảnh mẫu train](../outputs/20261117T081201Z_fd32180f/figures/eda_02_sample_images.png)
- [Histogram pixel train](../outputs/20261117T081201Z_fd32180f/figures/eda_03_pixel_histogram.png)
- [Ảnh trung bình theo lớp](../outputs/20261117T081201Z_fd32180f/figures/eda_04_class_mean_images.png)
- [Std pixel](../outputs/20261117T081201Z_fd32180f/figures/eda_05_pixel_std_heatmap.png)
- [PCA 2D, tổng phương sai khoảng 28,50%](../outputs/20261117T081201Z_fd32180f/figures/eda_06_pca_2d.png)
- [So sánh độ đo test sau khóa CV](../outputs/20261117T081201Z_fd32180f/figures/model_comparison.png)
- [Learning curves train/CV](../outputs/20261117T081201Z_fd32180f/figures/learning_curves.png)
- [Loss và validation accuracy MLP](../outputs/20261117T081201Z_fd32180f/figures/mlp_training_history.png)
- [Ma trận nhầm lẫn logreg_raw](../outputs/20261117T081201Z_fd32180f/figures/confusion_matrix_logreg_raw.png)
- [Ma trận nhầm lẫn knn](../outputs/20261117T081201Z_fd32180f/figures/confusion_matrix_knn.png)
- [Ma trận nhầm lẫn mlp](../outputs/20261117T081201Z_fd32180f/figures/confusion_matrix_mlp.png)
- [Ảnh sai logreg_raw](../outputs/20261117T081201Z_fd32180f/figures/misclassified_logreg_raw.png)
- [Ảnh sai knn](../outputs/20261117T081201Z_fd32180f/figures/misclassified_knn.png)
- [Ảnh sai mlp](../outputs/20261117T081201Z_fd32180f/figures/misclassified_mlp.png)

## 9. Hồ sơ minh họa ban đầu — không phải kết quả bản tối ưu hiện tại

Kiểm thử môi trường sạch: [25/25 tests](../outputs/demo_20261117T082316Z_b269f12c/tests_clean_environment.log), [trạng thái Phase 2](../outputs/demo_20261117T082316Z_b269f12c/phase2_status.json), [ảnh giao diện thật](../outputs/demo_20261117T082316Z_b269f12c/streamlit_demo.jpg).

Nguồn: [demo_verification.json](../outputs/demo_20261117T082316Z_b269f12c/demo_verification.json),
[dự đoán từng ảnh MNIST](../outputs/demo_20261117T082316Z_b269f12c/external_predictions.csv),
[ảnh gốc và sau xử lý](../outputs/demo_20261117T082316Z_b269f12c/external_image_preview.png),
[mẫu Digits](../outputs/demo_20261117T082316Z_b269f12c/digits_sample_predictions.csv),
[nguồn/quy tắc chọn fixture](../tests/fixtures/external_digits/README.md).

Mẫu Digits đầu mỗi lớp: LR 10/10, KNN 9/10, MLP 9/10; không thay cho đánh giá test vì có thể thuộc train.
10 MNIST bên ngoài chọn trước suy luận: mỗi mô hình 3/10. Đảo nền tạo cùng pixel đầu vào trong test chức năng,
không tính như mẫu độc lập. Không train/tune từ dữ liệu này; checksum model trước/sau khớp.
Chưa có ảnh chụp do nhóm cung cấp. Nhóm tự viết phân tích giới hạn, không suy ra accuracy tổng quát từ 10 mẫu.

## 10. Nhận định dự thảo và chú thích hình của phần A

**Chưa được nhóm xác nhận.** Các số bổ sung (tỷ lệ pixel 0/std) được tính từ đúng train theo split đã lưu, không huấn luyện lại. Các quan sát hình đã được xem trực tiếp.

**Nhật ký xử lý — dự thảo cần nhóm kiểm tra và xác nhận**

| Kiểm tra | Bằng chứng run chính thức | Quyết định thực nghiệm và lý do |
|---|---|---|
| Thiếu / sai kiểu | 65 cột gồm 64 pixel và nhãn đều thiếu 0%; pixel hữu hạn, nguyên dù lưu float64 | Giữ nguyên; không có cơ sở thêm imputer hoặc ép kiểu sửa dữ liệu |
| Trùng / nhãn mâu thuẫn | Không có ảnh trùng chính xác hoặc cùng ảnh khác nhãn | Giữ nguyên 1.797 mẫu; không cần loại trùng |
| Pixel ngoài miền / nhãn sai / ảnh hằng | Các số đếm đều 0 | Giữ nguyên; không có lỗi hợp đồng dữ liệu |
| Cờ IQR độ sáng, chỉ trên train | id 1747,818,1766; mean pixel 6,671875; 6,765625; 6,546875 | Giữ cả ba; đều là ảnh nhãn 1 có nét sáng dày, không hằng, không ngoài miền. Cờ thống kê không chứng minh ảnh lỗi |

Ba ảnh IQR được xem trực tiếp trong lượt kiểm tra cuối; chúng có 36,39,39 pixel khác 0.
Người xác nhận của nhóm: **chưa có thông tin**. Chính sách giữ nguyên là chính sách đã dùng trong run,
không phải một quyết định mới dựa vào điểm test. Nguồn: `data_quality.json`, `column_schema.csv`,
`train_image_diagnostics.csv` trong thư mục run chính thức. Các kiểm tra trùng xuyên tập ở mục 4.

**EDA 1 — dự thảo.** Số mẫu lớp 0–9 lần lượt là 142,146,142,146,145,145,145,143,139,144.
Lớp 8 ít nhất (139), lớp 1 và 3 nhiều nhất (146), chênh 7 mẫu; phân bố khá cân bằng.
Không có cơ sở phải tăng mẫu nhân tạo chỉ từ phân bố này. Macro F1 vẫn cho mỗi lớp trọng số ngang nhau.
Nguồn: `train_class_counts.csv`.

**EDA 2 — dự thảo.** Mỗi hàng 64 đặc trưng được reshape theo thứ tự hàng thành ảnh 8×8;
pixel 0 là tối, 16 là sáng. Các ảnh mẫu có nét và độ nghiêng khác nhau; ví dụ số 1 id 151 nghiêng,
số 8 id 18 có hai vùng vòng nét ở độ phân giải thấp. Chỉ 64 pixel nên chi tiết nét mảnh dễ mất;
một ảnh mỗi lớp không đại diện toàn bộ cách viết. Các id hiển thị đều thuộc train.

**EDA 3 — dự thảo.** Pixel nằm trong 0–16; khoảng **48,86%** pixel train bằng 0,
phù hợp nền tối chiếm nhiều diện tích. Các giá trị sáng vẫn cần để mô tả nét chữ;
pixel 0 hợp lệ, không phải missing. Chuẩn hóa trong Pipeline đổi thang theo từng vị trí,
không phải thay pixel 0 bằng giá trị điền thiếu. Tỷ lệ tính trên 1.437×64 pixel train.

**EDA 4 — dự thảo.** Ảnh trung bình lớp 0 còn vùng rỗng ở giữa, lớp 1 tập trung thành nét dọc,
lớp 8 có vùng nét ở cả nửa trên và dưới. Nét trung bình mờ hơn ảnh riêng vì vị trí/cách viết thay đổi.
Một số vùng nét của 8 và 1 có thể chồng nhau khi ảnh nhỏ; đây chỉ là giả thuyết hình học,
được đối chiếu với lỗi 8→ 1 sau khóa mô hình, không dùng hình trung bình để dự đoán accuracy.

**EDA 5 — dự thảo.** Nhiều vị trí bên trong biến thiên mạnh hơn mép nền.
Độ lệch chuẩn lớn nhất khoảng **6,5311** ở hàng 5, cột 2 (đánh số từ 0).
Các cột vector 0,32,39 có độ lệch chuẩn 0 trên train. Biến thiên đo sự thay đổi cường độ,
không trực tiếp đo tầm quan trọng dự đoán; giữ đủ 64 cột cho phép so sánh cùng biểu diễn đầu vào.

**EDA 6 — dự thảo.** PC1 giữ 14,7592%, PC2 giữ 13,7427% phương sai, tổng **28,5019%**.
Một số vùng lớp 0/4 dễ nhìn hơn, nhiều lớp vẫn chồng lấn. Còn hơn 71% phương sai ngoài mặt phẳng này,
nên chồng lấn 2D không chứng minh các mô hình 64 chiều không phân loại được.
PCA chỉ fit train và không nằm trong Pipeline thực nghiệm. Nguồn: `train_pca_2d.csv` và hình PCA.

**Phân tích lỗi — dự thảo sau đánh giá cuối, không dùng để tuning.**

| Mô hình | Tổng ảnh sai / 360 | Cặp có hướng nhiều nhất |
|---|---:|---|
| Logistic Regression | 15 | 8→ 1: 4; 1→ 8: 3 |
| KNN | 12 | 8→ 1: 3; 4→ 7: 2 |
| MLP | 14 | 8→ 1: 3; 9→ 8: 2 |

Ba mô hình cùng gặp 8→ 1; đây là mẫu lỗi chung, không có nghĩa mọi số 8 đều khó.
KNN nhận đúng 31/35 số 8 và cả 36 số 0 trong test. Ảnh id 1553 (8→ 1) có nét dọc nổi bật,
vòng dưới không rõ ở 8×8; id 1022 (4→ 7) có nét ngang và nét chéo rõ; id 1100 (9→ 8) có
vùng dưới tạo nét cong. Các quan sát này gợi ý mất chi tiết/cách viết có thể liên quan nhầm lẫn,
chưa chứng minh nguyên nhân quyết định của mô hình. Không đổi nhãn hay xóa các ảnh này.
Nguồn: các CSV `confusion_pairs_*`, `misclassified_*` và hình cùng tên của run chính thức.

**Learning curve và lịch sử MLP — dự thảo.** Tăng train mỗi fold từ 229 lên 1.149 mẫu,
validation macro F1 tăng từ 93,13% lên 96,30% (LR), 91,73% lên 97,62% (KNN),
80,09% lên 95,05% (MLP). Ở mốc cuối, train/validation lần lượt là 100/96,30%,
98,76/97,62%, 98,17/95,05%: khoảng cách **3,70; 1,15; 3,11 điểm phần trăm**.
LR khớp hoàn toàn train nhưng validation thấp hơn; đây là dấu hiệu khoảng cách tổng quát hóa,
chưa đủ để gọi quá khớp nghiêm trọng. Validation vẫn tăng khi thêm dữ liệu; MLP dao động hơn ở mẫu ít.
Các cỡ mẫu dùng prefix đã shuffle trong fold; kết quả có thể khác CV chính do số lượng/thứ tự mẫu.

MLP cuối chạy **52 iterations**, loss train giảm từ 2,3952 xuống 0,0208;
accuracy validation nội bộ tốt nhất 97,9167%, cuối đường cong cũng 97,9167%.
Loss tiếp tục giảm trong khi validation gần bão hòa; chưa thấy sụt giảm kéo dài để chỉ ra chính xác epoch bắt đầu quá khớp.
Early stopping theo validation accuracy nội bộ và lưu trọng số tốt nhất, không theo macro F1 CV.
Validation nội bộ nhỏ và scaler đã thấy đặc trưng của phần này khi fit train fold;
không xem điểm nội bộ là một đánh giá độc lập. Nguồn: `learning_curve.csv`, `mlp_history.json`.

**So sánh và lựa chọn — dự thảo.**

| Mô hình | CV macro F1 mean ± std (%) | Accuracy test (%) | Macro F1 test (%) |
|---|---:|---:|---:|
| Logistic Regression thô | 96,3687 ± 0,7866 | 95,8333 | 95,8075 |
| KNN | **97,6170 ± 0,7575** | 96,6667 | 96,6304 |
| MLP | 96,2365 ± 0,8314 | 96,1111 | 96,0888 |

KNN được khóa theo CV trước test. MLP hơn baseline **0,2778 điểm phần trăm accuracy test**
và **0,2813 điểm phần trăm macro F1 test**, nhưng CV mean thấp hơn baseline khoảng 0,1322 điểm phần trăm.
Chênh lệch nhỏ trên một split không chứng minh MLP luôn tốt hơn LR. KNN hiệu quả nhất trong thực nghiệm này,
không khẳng định luôn tốt hơn MLP. Std 5 folds mô tả dao động, không phải khoảng tin cậy hay kiểm định khác biệt.

**Chuẩn hóa:** cùng MLP ban đầu và folds, mean macro F1 CV tăng từ **94,3452% lên 96,2365%**,
tăng khoảng **1,8913 điểm phần trăm** (khoảng 2,00% tương đối); std giảm từ 1,8458 xuống 0,8314 điểm phần trăm.
Đây là kết quả CV cho scaling, khác accuracy test 96,1111%. Không suy rộng rằng mọi bộ dữ liệu đều được lợi như vậy.

**Chi phí:** LR/KNN/MLP fit cuối lần lượt 0,098705/0,003107/0,279319 s; predict median trên 360 ảnh
0,000798/0,004730/0,001538 s; tuning riêng 0/0,635378/4,231378 s; Pipeline 5.935/140.738/159.039 byte.
KNN fit nhanh vì chủ yếu lưu mẫu, nhưng predict chậm nhất; LR nhỏ và predict nhanh nhất ở phép đo này.
MLP tốn tuning/fit hơn, chưa đạt điểm tốt nhất. Đây là số đo cùng máy/một luồng, fit chỉ một lần;
không coi chênh lệch thời gian nhỏ là bảo đảm trên mọi máy. Baseline không tuning vẫn tốn CV.

**Giới hạn và hướng sau:** Digits nhỏ, 8×8; split ngẫu nhiên không bảo đảm tách người viết.
CV dùng chọn tham số nên có thiên lệch lựa chọn. 10 ảnh MNIST đã thử chỉ đúng 3/10 mỗi model,
cho thấy cần thận trọng với ảnh ngoài Digits, chưa đủ ước lượng accuracy thực tế.
Tiền xử lý hợp lệ về hình học/miền pixel không bảo đảm phân phối nét trùng Digits; xác suất chưa hiệu chỉnh.
Có thể thu ảnh thật có nhãn, chốt quy trình trước và đánh giá bằng tập ngoài mới trong nghiên cứu sau;
không sửa run hiện tại theo test hoặc theo 10 ảnh đã xem. Nguồn: `model_comparison.csv`, `mlp_scaling_cv.csv`, chỉ mục kết quả.


Chú thích dùng khi chèn hình (tất cả ảnh/bảng chính lấy từ run ở đầu tài liệu):

| Hình | Chú thích đề xuất |
|---|---|
| EDA01 | Số mẫu từng nhãn trên 1.437 ảnh train; lớp 139–146 mẫu |
| EDA02 | Một ảnh train mỗi lớp, kèm nhãn/id và thang0–16; không đại diện mọi kiểu viết |
| EDA03 | Histogram của 1.437×64 pixel train; pixel 0 hợp lệ chiếm48,86% |
| EDA04 | Trung bình từng vị trí pixel theo lớp trên train, cùng thang màu0–16 |
| EDA05 | Std pixel train, ddof=0, chỉ số hàng/cột0–7; không phải feature importance |
| EDA06 | PCA fit train, PC1+PC2 giữ 28,5019% phương sai; chỉ để quan sát |
| model_comparison | Accuracy và macro F1 trên cùng360 ảnh test sau khóa lựa chọn bằng CV |
| confusion_matrix_* | Hàng nhãn thật, cột dự đoán; số đếm360 ảnh test/model |
| misclassified_* | Tối đa12 ảnh sai theo thứ tự test, nhãn thật/dự đoán/id; không dùng tuning |
| learning_curves | Macro F1 mean ± std trên 5 folds theo số mẫu train/fold; không dùng test |
| mlp_training_history | Loss train và accuracy validation nội bộ ở hai panel; 52 iterations, khác CV macro F1 |

Trả lời đủ 5 câu đề tài: xem phần cuối notebook. Chuẩn bị báo cáo10 mục và 12 slide từ REPORT_OUTLINE/SLIDE_OUTLINE; đây chưa phải xác nhận hoặc sản phẩm trình bày cuối của nhóm.

## 11. B — Mở rộng nhận diện ảnh ngoài

Run [external_optimization_20261118T175401Z_4ca3a08f](../outputs/external_optimization_20261118T175401Z_4ca3a08f/REPORT.md). Seed42,600 ảnh từBHMSDS/Bitmap Numbers/HwD-1000,300 validation+300 test,10/lớp/nguồn/split; giữ bytes/nhãn gốc. [Manifest](../data/external_handwriting/manifest.csv), [nguồn/license](../data/external_handwriting/SOURCES.md), [contact sheets](../data/external_handwriting/contact_sheets). Không có writer ID đáng tin; Bitmap thiếu mapping nguồn từng ảnh. Không chứng minh writer independence hoặc accuracy ảnh chụp điện thoại.

Preprocessing chung chọn bằng mean macro F1 của3 Pipeline Digits trên validation300: baseline0,48980;gray_bbox**0,59260**;gray_com0,50661;binary35 0,50816;binary50 0,50569;binary35_thick0,43660;gray_wide0,49473. Điều kiện tăng≥0,02 và KNN F1 không giảm đạt. [Bảng validation từng model/nguồn](../outputs/external_optimization_20261118T175401Z_4ca3a08f/validation/metrics.csv).

Một MLP MNIST28: MinMaxScaler→MLP(128,64),relu/adam,alpha0,0001,early stopping,seed42;54000 train/6000 validation ngoài, không augmentation/không train600 ảnh mới. Train23,895571s/30 iterations, Pipeline1221502byte. Validation MNIST97,3167%/F1 0,972961; ngoài90%/F1 0,896684. [Protocol](../outputs/external_optimization_20261118T175401Z_4ca3a08f/protocol.json) và [selection lock](../outputs/external_optimization_20261118T175401Z_4ca3a08f/selection_lock.json) có trước final test; loại110 MNIST test đã xem, còn9890.

| Hệ thống | MNIST9890 accuracy | MNIST macro F1 | Ngoài300 accuracy | Ngoài macro F1 |
|---|---:|---:|---:|---:|
|LR cũ|46,4105%|0,473055|63,3333%|0,642764|
|KNN cũ|41,9312%|0,427209|48,0000%|0,490304|
|MLP Digits cũ|36,8049%|0,380337|49,6667%|0,489448|
|LR gray_bbox|49,4944%|0,502436|64,6667%|0,651633|
|KNN gray_bbox|47,0677%|0,471308|58,0000%|0,573268|
|MLP Digits gray_bbox|42,0829%|0,434002|53,3333%|0,538202|
|MLP MNIST28|97,3913%|0,973773|87,3333%|0,871326|

Nguồn [metrics.csv](../outputs/external_optimization_20261118T175401Z_4ca3a08f/final_test/metrics.csv), tính từ giá trị gốc rồi mới làm tròn. MLP28 đúng9632/9890 MNIST;262/300 ngoài, sai38. BHMSDS82/100,Bitmap82/100,HwD98/100. KNN gray_bbox tăng10 điểm phần trăm ngoài. Không quy toàn bộ tăng của MLP28 cho preprocessing vì dataset/lượng mẫu/kiến trúc/resolution cũng đổi. Không chọn lại theo test.

| Bằng chứng/hình | Vị trí trong run mở rộng |
|---|---|
|Precision/recall/F1/support từng chữ số và nguồn|final_test/*__per_digit.csv và *__report.json|
|Confusion từng model/cùng tập|analysis/figures/mnist_test_confusion_annotated.png, handwriting_test_confusion_annotated.png|
|Ảnh lỗi gốc/8×8 cũ/8×8 mới/28×28|analysis/figures/*_test_errors_before_after.png;8 ID lỗi KNN cũ đầu theo ID|
|Phân phối và ảnh trung bình, chỉ train/validation|analysis/figures/validation_distributions.png, validation_class_means.png|
|Training loss và early-stopping accuracy|analysis/figures/mlp_mnist_training.png; khác đơn vị, không suy ra epoch quá khớp chính xác|
|Đúng/sai/xác suất đầy đủ|final_test/*__predictions.csv, *__correct.csv, *__incorrect.csv|
|Chi phí và caveat phép đo|final_test/metrics_with_cost.csv; một batch predict+proba,2 luồng; khác benchmark Digits|
|Kiểm tra sạch/code freeze|[REVIEW](../outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md)|

Ảnh scan/cắt/vẽ tay số là ba kiểu nguồn khác nhau. Nhóm cần phân tích38 lỗi và giới hạn bằng bảng/hình đã xuất, không sửa model từ test. Các kết quả3/10 và46/40/37 trên100 MNIST cũ là lịch sử riêng, không thay bằng score mới hoặc gộp accuracy.

## 12. Giao diện, kiểm thử và trạng thái biên soạn hiện tại

Tên lựa chọn: Logistic Regression, K-Nearest Neighbors (KNN), Multilayer Perceptron (MLP), Multilayer Perceptron (MLP) — MNIST. Nguồn: **Ảnh kiểm tra Digits**, **Ảnh mẫu Digits**, **Tải ảnh từ máy**. Tên cũ trong ảnh/log không phải yêu cầu đổi lại giao diện.

53/53 unittest của bản ngôn ngữ21/11 đã ghi trong HANDOFF. Bằng chứng môi trường sạch19/11,14 tình huống demo/8 lỗi model,1.200 replay và145 dòng độ đo nằm trong [review freeze](../outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md). Không xem lần cập nhật tài liệu23/11 là test hoặc phép đo mô hình mới.

Nhóm cần rà/xác nhận nhật ký và nhận định, điền thông tin/phân công thật, xuất báo cáo/slide và tập bảo vệ. Chưa có ảnh điện thoại nhóm hoặc xác nhận sản phẩm nộp chính thức. Manifest snapshot toàn repo giữ lịch sử source/docs; dùng registry để đối chiếu checksum trọng số, không sửa manifest cũ cho khớp chữ mới.
