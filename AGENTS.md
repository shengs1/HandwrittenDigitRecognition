# Hướng dẫn tiếp tục đồ án

Cập nhật 23/11/2026. Đây là quy tắc hiện hành; lịch sử quyết định nằm trong HANDOFF.md, Git và outputs/.

## Trạng thái và phạm vi

**UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Bản tối ưu được duyệt ngày 19/11; ngôn ngữ giao diện được duyệt và push tại `f47a709` ngày 21/11. Ngày 23/11, người dùng yêu cầu đồng bộ tài liệu và push lên main. Không mở thêm phase mô hình hoặc UI, huấn luyện lại hay tuning để tăng điểm demo.

Đề tài 13: phân loại chữ số 0–9. Phần A chính dùng `load_digits()`, baseline Logistic Regression trên điểm ảnh thô và KNN/MLP. Phần B mở rộng dùng một MLP MNIST riêng và đánh giá ảnh ngoài; không thay dataset, lựa chọn hoặc số liệu phần A. Kiến trúc hiện tại cho phép Streamlit; không thêm database, tài khoản hoặc backend riêng.

## Quy trình mỗi phiên

- Đọc PDF `docs/Huong_Dan_Do_An_CuoiKy.pdf`, HANDOFF.md, notebook và tài liệu/kết quả liên quan trước khi sửa. AI_USAGE.md đã xóa theo yêu cầu người dùng, không tạo lại.
- Chạy `git status --short --branch` và `git diff`. Không xóa hoặc ghi đè thay đổi có sẵn của người dùng.
- Chỉ commit/push khi đã được yêu cầu. Repo `https://github.com/shengs1/HandwrittenDigitRecognition`, nhánh main; không force-push hoặc sửa lịch sử remote.
- Sau cụm việc lớn, cập nhật HANDOFF: việc thực sự làm, file, lý do, lệnh và kết quả kiểm tra, lỗi/giới hạn, việc nhóm cần làm và trạng thái Git. Không báo đã chạy test hoặc huấn luyện khi chưa chạy.

## Yêu cầu và tính trung thực

PDF yêu cầu baseline, ít nhất hai mô hình so sánh, ít nhất năm EDA có nhãn/nhận định, làm sạch có lý do, Pipeline, chia dữ liệu đúng, kiểm định chéo/tuning, độ đo, phân tích lỗi, seed/phiên bản và tái lập. Điểm: dữ liệu/EDA/chuẩn bị 4; mô hình/đánh giá 4; trình bày/vấn đáp 2. Xem docs/REQUIREMENTS_MAP.md.

Năm câu đề tài: vector/shape và chuẩn hóa; baseline và MLP cải thiện thế nào; cặp nhầm; learning curve và bằng chứng quá khớp; chi phí so độ chính xác. Không ép MLP phải thắng hoặc xác định epoch quá khớp khi chưa đủ bằng chứng.

Nhóm cần báo cáo 10 mục, slide, thông tin/phân công thật và khả năng giải thích toàn bài. Nhận định hiện là dự thảo từ output thật, chưa được nhóm xác nhận. Không bịa dữ liệu, số liệu, đóng góp hoặc kết quả vấn đáp; fixture tổng hợp không phải accuracy ảnh thực tế. Theo phạm vi người dùng đã chốt, mục 6 PDF không được đưa lại thành blocker của audit; giữ nguyên PDF gốc.

## Kiến trúc và giao diện

Notebook `digit_classification.ipynb` gồm 16 mục là tài liệu chính. `app.py` chứa giao diện/tải mô hình/suy luận; `external_preprocessing.py` chứa các biến thể ảnh ngoài đã khóa. Dùng hàm ngắn, tránh framework/class/module phụ không cần thiết. tests/ kiểm hợp đồng, artifact và luồng app; docs/ phục vụ báo cáo, slide và vấn đáp.

Tên mô hình bằng tiếng Anh: Logistic Regression, K-Nearest Neighbors (KNN), Multilayer Perceptron (MLP), Multilayer Perceptron (MLP) — MNIST. Nhãn/chú thích bằng tiếng Việt. Ba thẻ: Bộ dữ liệu Digits, Tốt nhất qua kiểm định chéo, Độ chính xác kiểm tra · KNN. Tên thuật toán/thư viện và giá trị kỹ thuật giữ đúng tên gốc.

Nguồn hiển thị: Ảnh kiểm tra Digits, Ảnh mẫu Digits, Tải ảnh từ máy. Khóa nội bộ `Ảnh test Digits` được giữ; format_func chỉ đổi tên hiển thị. Đọc đúng split_indices.csv của registry, không chia lại hoặc cho chọn ID ngoài tập. Ảnh Digits giữ nguyên điểm ảnh. MLP MNIST chỉ có ở nguồn tải ảnh, không tự đổi mô hình theo xác suất.

Giữ dark theme, typography, hai cột và native dropdown. Đổi ảnh/mô hình/nguồn/nền phải xóa kết quả cũ. Thông số đọc từ Pipeline/metadata, không hardcode kết quả. Không dùng CSS zoom/scale/giấu overflow; văn bản tự xuống dòng, expander cuộn tự nhiên. Khi kiểm responsive, đo actual viewport và cả document/stMain.

## Phần A — Digits cố định

Run `20261117T081201Z_fd32180f`, registry `models/registry.json`: 1.797 ảnh, 8×8/64 đặc trưng/0–16; 1.437 huấn luyện, 360 kiểm tra; 80/20, stratify=y, seed 42. Không đổi dataset/split.

Baseline passthrough→LogisticRegression(C=1, lbfgs, max_iter=3000). KNN/MLP dùng StandardScaler. MLP ban đầu `(64,32)`, relu/adam, early_stopping=True, seed 42. Đối chứng MLP thô/chuẩn hóa giữ cùng cấu hình và folds. StratifiedKFold 5, shuffle=True, seed 42; grid nhỏ, chọn mean macro F1 cao nhất, hòa theo tên tăng dần. KNN chính thức k=3/uniform, khóa theo CV trước test; CV sau tuning có thiên lệch lựa chọn.

EDA/PCA chỉ fit train. Fit cuối một lần; predict median 5 lần sau warm-up, cùng test/máy/một luồng; tuning riêng, joblib nén 3 toàn Pipeline. Learning curve chỉ dùng train/CV; loss và validation accuracy MLP khác đơn vị. Mục 11–14 định nghĩa hàm; test chỉ gọi sau khóa ở mục 15.

## Phần B — mở rộng đã khóa

Run `external_optimization_20261118T175401Z_4ca3a08f`, registry phụ `models/external_registry.json`. Upload với ba model Digits dùng gray_bbox→8×8/64/0–16. MLP MNIST dùng mnist28→28×28/784/0–255, float32, Pipeline MinMaxScaler→MLP(128,64), relu/adam, alpha0,0001, dừng sớm, seed42. Không scaler ngoài Pipeline, không train khi mở app.

MNIST 60.000 chia 54.000/6.000, stratify/42, không augmentation hoặc dùng 600 ảnh mới để train. MLP giữ 5.400 xác thực nội bộ, còn 48.600 cập nhật gradient; scaler thấy outer train trước chia nội bộ nhưng không thấy 6.000 xác thực ngoài. Loại 110 MNIST test đã xem, còn 9.890 đánh giá sau khóa. Không refit train+validation sau chọn.

600 ảnh gốc từ BHMSDS/Bitmap Numbers/HwD-1000, 200/nguồn, 20/chữ số/nguồn; seed42, chia 300 xác thực/300 kiểm tra cân bằng. Chọn tiền xử lý theo mean macro F1 của ba model trên validation300; gray_bbox đạt 0,59260 so 0,48980 cũ, thỏa tăng≥0,02 và KNN không giảm. MLP mới thỏa tiêu chí validation đặt trước rồi mới kiểm test. Manifest, split, protocol, lựa chọn và hash module/model đã khóa.

Cả 9.890 MNIST và 300 test ngoài đều đã xem kết quả; không dùng tuning/chọn lại. Không đổi nhãn hoặc bỏ ảnh vì sai. Nguồn/giấy phép ở data/external_handwriting/SOURCES.md: không có writer/sheet ID đáng tin, Bitmap mất ánh xạ từng ảnh; không chứng minh độc lập người viết. Scan, giấy đã cắt và vẽ tay số không phải ảnh điện thoại nguyên bản.

## Bảo toàn và bàn giao

- Không fit scaler/PCA/imputer/lựa chọn đặc trưng trên toàn bộ dữ liệu trước CV. Không tuning bằng test hoặc dùng ảnh khó đã xem để chỉnh preprocessing.
- Nếu có ảnh trùng xuyên tập, dừng và ghi bằng chứng/quyết định; không âm thầm đổi split/seed/tỷ lệ. Không loại ảnh chỉ vì khó hoặc bất thường thống kê.
- Giữ đủ Pipeline/registry/selection lock khi đóng gói. Chỉ load joblib tin cậy. `.gitattributes` bảo toàn bytes; Windows clone cần core.longpaths=true khi đường dẫn sâu.
- App đã có 53/53 test PASS ngày 21/11. Sửa tài liệu không đồng nghĩa rerun mô hình hoặc venv sạch. Chỉ chạy lại kiểm tra phù hợp thay đổi.
- README và docs/ là tài liệu hiện hành; outputs/ và README/LICENSE nguồn bên thứ ba là hồ sơ lịch sử, không sửa lại để khớp hiện tại. Manifest snapshot chứa source/docs tại ngày chốt; thay nhãn/tài liệu không đồng nghĩa đổi trọng số. Kiểm Pipeline theo registry và test hiện tại, không sửa manifest để che khác biệt.
- Chưa có ảnh điện thoại nhóm, báo cáo/slide chính thức, thông tin/phân công hoặc xác nhận nhận định. Giữ trạng thái tài liệu/thuyết trình đang hoàn thiện; không tự đánh dấu đồ án sẵn sàng nộp.
