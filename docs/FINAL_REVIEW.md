# Final review hiện hành — đề tài 13

Cập nhật23/11/2026, đồng bộ với code `f47a709` ngày21/11. **UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Lượt23/11 chỉ sửa tài liệu, không huấn luyện hoặc gán kết quả test mới.

## Kết luận và vấn đề còn mở

Không có lỗi Critical đang mở được xác định trong phạm vi đã kiểm. Phần kỹ thuật có notebook/Pipeline/demo và bằng chứng môi trường sạch. Chưa xác nhận sẵn sàng nộp trọn bộ: còn nhận định nhóm, báo cáo/slide chính thức, thông tin/phân công và vấn đáp. Không suy điểm từ checklist kỹ thuật.

| Mức | Vấn đề | Trạng thái |
|---|---|---|
| Critical | Sai kết quả hoặc rò rỉ được xác định | Chưa có lỗi mở trong phạm vi kiểm tra; không phải bảo đảm tuyệt đối |
| Major | Báo cáo PDF/DOCX, slide PPTX/PDF, thông tin/phân công thật | Chưa xác nhận có bản nộp; đã có dự thảo10 mục/12 slide |
| Major | Nhóm xác nhận nhận định và giải thích code | Chưa có bằng chứng xác nhận; test PASS không thay vấn đáp |
| Giới hạn | Ảnh điện thoại, độc lập người viết, nguồn gốc từng ảnh Bitmap | Chưa xác nhận; không gọi87,33% là accuracy ảnh điện thoại |
| Đã sửa | Git tự đổi LF/CRLF, sai checksum | .gitattributes giữ byte; 2.455 file xuất từ index khớp |
| Đã sửa | Đường dẫn Windows dài | README clone với core.longpaths=true; không đổi tên artifact |
| Đã sửa | Ngôn ngữ giao diện lẫn lộn | Tên model tiếng Anh, nhãn tiếng Việt; f47a709,53 tests PASS21/11 |

## Bằng chứng theo thời điểm

| Ngày | Kiểm tra đã thực hiện | Nguồn |
|---|---|---|
|17/11|Notebook Run All ở checkout riêng; metric/CV/curves/prediction khớp,31 tests|[Review cũ](../outputs/review_20261117T090347Z_9df57e69/review_checks.json)|
|17/11|Nhận định dự thảo và mẫu kiểm tra; 37 tests checkout sạch|[Completion](../outputs/completion_20261117T100609Z_b8981ac1/clean_checkout_tests.log)|
|19/11|Venv mới Python3.12.14/120 gói,53 tests; 4 model,14 chức năng/8 lỗi model,1.200 replay|[Review freeze](../outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md)|
|19/11|Sau sửa byte Git:53/53 tests,11,204s trên bản xuất từ index|[Log Git checkout](../outputs/optimization_freeze_20261119T045133Z_728f35c1/git_index_unittest.log)|
|21/11|53/53 tests,12,229s sau đổi nhãn; browser1366×768 không tràn/cắt chữ|[HANDOFF](../HANDOFF.md), commit f47a709; log/screenshot local được ghi trong đó|
|23/11|Đồng bộ tài liệu, kiểm liên kết/số liệu/bảo toàn file|Cụm23/11 trong HANDOFF; không phải lần chạy53 tests mới|

## A — Digits chính thức

Run `20261117T081201Z_fd32180f`, registry gốc; 1.797 ảnh8×8/64/0–16, chia1.437/360, stratify/42. Baseline Logistic Regression passthrough, KNN/MLP StandardScaler; 5 folds shuffle/42, grid nhỏ, khóa theo macro F1 CV trước test. KNN CV0,976170±0,007575, test accuracy0,966667/F1 0,966304; không chọn lại theo test.

Sáu EDA, nhật ký và nhận định dự thảo đã có; không còn TODO triển khai cốt lõi. Nhóm vẫn cần rà/xác nhận. Baseline test95,8333%, MLP96,1111% nhưng CV MLP không vượt LR. Có confusion/cặp nhầm/ảnh sai, learning/training curve và chi phí; chưa đủ chỉ ra epoch quá khớp chính xác. [RESULTS_INDEX](RESULTS_INDEX.md) giữ bảng/hình và diễn giải có giới hạn.

## B — Mở rộng ảnh ngoài

Giữ ba Pipeline Digits, so bảy tiền xử lý trên validation300; gray_bbox được chọn trước test. Một MLP MNIST(128,64)/MinMaxScaler học54.000 ảnh, giữ6.000 xác thực ngoài. Loại110 MNIST test đã xem, còn9.890 đánh giá sau khóa.600 ảnh ngoài ba nguồn cân bằng, không dùng train; nguồn/giấy phép/bytes/manifest được ghi trước suy luận.

MLP MNIST đúng9.632/9.890 (97,3913%) và262/300 (87,3333%), F1 ngoài0,871326, còn38 lỗi; BHMSDS82/100, Bitmap82/100, HwD98/100. KNN cũ48%→gray_bbox58% trên cùng300 test. Không gộp accuracy hoặc quy toàn bộ tăng cho tiền xử lý; 145 dòng độ đo đã audit ở lượt freeze. [Báo cáo mở rộng](../outputs/external_optimization_20261118T175401Z_4ca3a08f/REPORT.md) giữ nhận định dự thảo và ảnh lỗi.

## Demo hiện tại và bảo toàn

Tên model tiếng Anh; nhãn/gợi ý tiếng Việt. **Ảnh kiểm tra Digits** đọc đúng360 ID;**Ảnh mẫu Digits** có thể gồm train;**Tải ảnh từ máy** cho chọn thêm **Multilayer Perceptron (MLP) — MNIST**. Digits giữ điểm ảnh gốc; upload dùng gray_bbox/64 hoặc mnist28/784, scaler trong Pipeline. Đổi ảnh/model xóa kết quả; không tự chọn theo xác suất, không train/tải MNIST khi mở app. Ba thẻ đầu luôn là số liệu Digits KNN.

Giữ dark theme/hai cột, ảnh gốc/preview,10 xác suất và thông số từ model. Hash bốn Pipeline kiểm theo registry. Manifest snapshot lịch sử có cả code/test/docs ở ngày chốt; thay đổi nhãn/tài liệu hợp lệ không đồng nghĩa đổi trọng số. Không ghi đè manifest hoặc số liệu để che khác biệt.

## Việc trước nộp

Nhóm xác nhận nhật ký/nhận định, điền tên/MSSV/lớp/phân công thật, xuất báo cáo10 mục và slide, tập vấn đáp/demo offline, thử ảnh tự chụp có nhãn. Báo riêng A/B; giữ10 MNIST3/10 và100 MNIST46/40/37 như lịch sử. Không tuning từ test đã xem. Xem [yêu cầu PDF](REQUIREMENTS_MAP.md),[báo cáo](REPORT_OUTLINE.md),[slide](SLIDE_OUTLINE.md),[vấn đáp](VIVA_QUESTIONS.md).
