# Câu hỏi vấn đáp theo code và số liệu thật

Nhóm tự trả lời bằng lời của mình. Gợi ý chỉ vị trí kiểm chứng. Mỗi thành viên thử thao tác ở bản thử riêng; không tuning run đã khóa theo test.

| Câu hỏi | Kiểm chứng / gợi ý |
|---|---|
| 1. Bài toán gì? Shape/dtype/miền X,y? | Notebook 1–3, data_summary, column_schema |
| 2. Digits khác MNIST? 8×8 thành 64 thế nào? | reshape; MNIST fixture 28×28 chỉ suy luận |
| 3. Float64 có sai khi pixel mô tả số nguyên? | Kiểm tra giá trị bằng floor, không chỉ dtype |
| 4. Không missing có cần imputer? 3 IQR có xóa? | Quality/diagnostics và nhật ký giữ nguyên |
| 5. Stratify/seed/kiểm trùng giải quyết gì khác nhau? | Split và cv_fold_audit |
| 6. Ảnh trùng xuyên tập gây vấn đề gì? | image_keys/assert; không đổi split âm thầm |
| 7. Baseline thô có nghĩa LR không cần scaling? | Mục đích đối chứng ở make_baseline |
| 8. Pipeline chống leakage trong GridSearchCV thế nào? | Clone theo fold; lỗi fit scaler trước CV |
| 9. C/alpha/k và clf__n_neighbors nghĩa gì? | get_params, step names, hai grid |
| 10. Scaling đối chứng giữ gì cố định? | MLP_INITIAL, folds, seed; mlp_scaling_cv |
| 11. Vì sao chọn KNN thay mạng nơ-ron? | CV macro F1 mean 0.976170 cao nhất |
| 12. Test đổi thứ hạng có chọn lại không? | Hàm chọn không nhận test; selection_lock |
| 13. Macro F1 khác accuracy/weighted F1? | Tự minh họa 2 lớp lệch trên giấy |
| 14. std ddof=0 có phải CI 95%? | 5 fold scores; không suy diễn kiểm định |
| 15. refit=False có best_estimator_? Đo fit cuối ở đâu? | Clone/set_params và measure_final_pipeline |
| 16. Tuning baseline=0 có nghĩa không tốn CPU? | CV vẫn chạy; cv_details_logreg_raw |
| 17. Cặp nhầm có hướng là gì? Mở một ảnh sai thật. | Confusion_pairs/misclassified |
| 18. Có bằng chứng overfitting chưa? | Train/validation mean/std theo số mẫu |
| 19. Loss và validation score cùng đơn vị? Epoch cuối có phải trọng số giữ? | Early stopping; 52 iterations thực tế |
| 20. Scaler có thấy validation nội bộ MLP? | Fit train fold trước chia nội bộ; outer fold/test độc lập |
| 21. Đổi model/upload có train? Chứng minh. | Không fit; tests chặn Pipeline.fit; checksum |
| 22. Vì sao mẫu Digits không crop/resize lại? | Giữ vector gốc, so dự đoán joblib trực tiếp |
| 23. Upload có StandardScaler hai lần? | 0–16 bên ngoài, scaler bên trong Pipeline |
| 24. Vì sao lấy màu viền? Giả định sai ở ảnh nào? | Chạm biên, bóng đổ, nền phức tạp |
| 25. Alpha/đảo màu/trống được xử lý thế nào? | Tests ảnh, thử fixture đảo màu và ảnh trắng |
| 26. Xác suất 99% có chắc đúng? | External_predictions có nhãn thật; chưa calibration |
| 27. Test Digits ~96% nhưng MNIST 3/10 thì sao? | Khác phân phối, tiền xử lý, mẫu nhỏ; tự phân tích |
| 28. Mất .joblib/registry có crash/tự train? | Tests thiếu file/manifest; thử bản sao |
| 29. Muốn đổi default hoặc train lại sửa đâu? | Registry và notebook; không chọn bằng demo/test |
| 30. Có bảo đảm bit giống mọi máy? | Seed/phiên bản/luồng giúp tái lập; timing phụ thuộc máy |

Thực hành: chỉ ra đường đi dữ liệu trong app; đọc một cặp nhầm từ CSV; dự đoán một mẫu bằng predict_digit; giải thích fallback metadata passthrough (sklearn 1.7 chuyển thuộc tính từ bước đầu, app cần fallback classifier). Không fit toàn bộ Digits để làm đẹp demo và làm mất độc lập test.
