# Chỉ mục số liệu và hình cho báo cáo

Run thực nghiệm cố định: **20261117T081201Z_fd32180f**; nguồn thật trong [outputs](../outputs/20261117T081201Z_fd32180f/).
Quy tắc và thời điểm khóa: [selection_lock.json](../outputs/20261117T081201Z_fd32180f/selection_lock.json).
Mô hình mặc định **knn** được chọn bằng CV trước test.
Các bảng dưới chỉ tổng hợp số liệu, không thay nhận định/phân tích của nhóm. Không dùng ba run support cũ làm điểm mô hình.

## 1. Dữ liệu

1.797 mẫu, 64 pixel, ảnh 8×8; float64 cho X, int64 cho y; nhãn 0–9, pixel 0–16.
Train 1.437/test 360; stratify=y, seed 42. Các kiểm tra thiếu, sai miền/nhãn, trùng đều 0.
Ba id train có cờ IQR độ sáng: 1747, 818, 1766; không bị loại.
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
| mlp | StandardScaler | hidden=(64, 32), alpha=0.0001, relu/adam, early_stopping=True, max_iter=300 |

Nguồn: Pipeline được registry trỏ tới và [metadata](../models/20261117T081201Z_fd32180f/metadata.json); seed 42.


## 5. Đối chứng MLP scaling

Nguồn: [10 hàng CV](../outputs/20261117T081201Z_fd32180f/mlp_scaling_cv.csv); cùng MLP_INITIAL/folds/seed.

| Điều kiện | Mean macro F1 | Std macro F1 (ddof=0) |
|---|---|---|
| raw | 0.943452 | 0.018458 |
| standard | 0.962365 | 0.008314 |

## 6. Các cặp nhầm có hướng nhiều nhất

Chỉ số đếm thực, thật → dự đoán; hòa xếp theo nhãn. Nhóm mở ảnh và tự giải thích.


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

## 9. Kiểm thử demo ngoài tập Digits

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

