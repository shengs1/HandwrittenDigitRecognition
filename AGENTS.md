# Hướng dẫn tiếp tục đồ án

## Bắt đầu mỗi phiên

Đọc toàn bộ `docs/Huong_Dan_Do_An_CuoiKy.pdf`, `HANDOFF.md`, `AI_USAGE.md` và notebook trước khi sửa. Chạy `git status --short --branch` và `git diff`; nếu chưa có repository thì ghi nhận đúng thực tế. Không xóa hoặc ghi đè thay đổi của người dùng. Chỉ khởi tạo Git, commit hoặc push khi người dùng đã yêu cầu; không đổi dataset. Người dùng đã yêu cầu khởi tạo/liên kết, commit và push bản khung hiện tại lên `https://github.com/shengs1/HandwrittenDigitRecognition`, nhánh `main`, ngày 2026-11-17. Không force-push hoặc thay đổi lịch sử remote.

## Mục tiêu và yêu cầu

Đề tài 13: phân loại chữ số 0–9 bằng `sklearn.datasets.load_digits()`. Python, NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, Jupyter và Joblib. Không xây Streamlit trong phase hỗ trợ này.

PDF: có baseline, ≥2 mô hình so với baseline, EDA ≥5 biểu đồ có nhãn và nhận định, kiểm tra/làm sạch có lý do, Pipeline, chia dữ liệu đúng, CV/tuning, phân tích lỗi, seed và phiên bản thư viện. Thang điểm: dữ liệu/EDA/chuẩn bị 4; mô hình/đánh giá 4; trình bày/vấn đáp 2. Nhóm cần báo cáo, slide, phân công thật và khả năng giải thích toàn bộ bài; demo là tùy chọn trong quy trình PDF.

Năm câu hỏi đề tài: (1) vector/shape và chuẩn hóa pixel; (2) baseline đạt bao nhiêu, MLP cải thiện thế nào; (3) cặp nhầm lẫn; (4) learning curve và bằng chứng quá khớp; (5) chi phí so với độ chính xác. Không giả định có cải thiện hoặc quá khớp.

## Kiến trúc và quyết định

Notebook `digit_classification.ipynb` là tài liệu chính, 16 mục đúng thứ tự yêu cầu người dùng. Chỉ dùng hàm ngắn, không framework/module/class phụ. `tests/` kiểm tra hợp đồng dữ liệu và khung notebook; `docs/` giữ tài liệu gốc, hướng dẫn đối chiếu. `models/`, `outputs/` chỉ chứa kết quả thật, có nguồn gốc rõ ràng.

Train/test 80/20, `stratify=y`, `random_state=42`. Baseline Logistic Regression trên pixel thô, bước preprocessing `passthrough`. Hai mô hình KNN và MLP dùng Pipeline. MLP ban đầu `(64,32)`, relu, adam, early_stopping=True; seed 42. Chuẩn hóa dùng StandardScaler trong Pipeline. Thử MLP thô/chuẩn hóa cùng cấu hình và folds. StratifiedKFold 5, shuffle=True, seed 42. Grid nhỏ; chọn theo CV macro F1, hòa tuyệt đối dùng thứ tự tên ổn định; không chọn theo điểm test. Ghi rõ CV sau tuning có thiên lệch lựa chọn, không phải đánh giá độc lập.

Đo fit cuối bằng clone Pipeline rồi fit một lần trên cùng train; predict cùng test, cùng máy và số luồng, lặp đo có ghi rõ; tuning tính riêng, không nhập thời gian refit vào fit cuối. Dung lượng là byte của toàn bộ Pipeline với cùng quy tắc joblib. Learning curve chỉ dùng train/CV; loss MLP và validation score khác đơn vị. Thứ tự mục 11–14 là nơi hướng dẫn/khai báo hàm; chỉ gọi test sau khi khóa lựa chọn ở mục 15.

## Chống rò rỉ

- Không fit scaler, PCA, imputer hoặc lựa chọn đặc trưng trên toàn bộ dữ liệu trước CV. PCA EDA chỉ fit train, không đưa tọa độ EDA vào mô hình.
- Không sử dụng test để tuning, chọn preprocessing, threshold, số vòng lặp, mô hình hoặc xử lý ảnh khó. Chỉ kiểm tra hợp lệ và trùng xuyên tập; không xem phân bố/ảnh test trước đánh giá cuối.
- Kiểm tra ảnh giống hệt trong dữ liệu, giữa train/test và giữa các fold. Nếu gặp trùng xuyên tập: dừng; nhóm ghi quyết định loại trùng trước split hoặc đề xuất chia theo nhóm; không âm thầm đổi tỷ lệ/seed/yêu cầu.
- Không xóa ảnh chỉ vì khó hoặc dự đoán sai. Bất thường thống kê chỉ là gợi ý xem xét; mọi quyết định làm sạch do nhóm ghi bằng chứng và lý do.
- StandardScaler trong Pipeline được fit trên train của mỗi CV fold. Early stopping MLP có validation nội bộ; scaler thấy các đặc trưng của phần validation nội bộ đó nhưng không thấy fold validation ngoài hay test. Nêu giới hạn này khi diễn giải.
- Mục 15 khóa lựa chọn bằng kết quả CV trước predict test. Sau xem test chỉ phân tích, không quay lại tuning.

## Liêm chính học thuật

Tuân thủ mục 6 PDF: không nộp bài có toàn bộ mã hoặc phân tích do AI sinh. AI hỗ trợ kiến trúc, khung, giải thích API, kiểm tra/sửa lỗi. Để sinh viên tự triển khai TODO cốt lõi: Pipeline mô hình, thí nghiệm chuẩn hóa, CV/GridSearchCV, độ đo, phân tích lỗi, learning curve và lựa chọn bằng CV. Không tự hoàn thành thay nhóm các TODO này. Nhóm tự viết nhận định và bảo vệ từng quyết định.

Không bịa số liệu, đóng góp thành viên hoặc kết quả test. Không dùng dữ liệu giả làm kết quả mô hình. Cập nhật `AI_USAGE.md` đúng công cụ/phạm vi thực tế; đóng góp sinh viên chưa được xác minh phải ghi chưa có thông tin.

Sau mỗi cụm việc lớn cập nhật `HANDOFF.md`: phase, việc thực sự hoàn thành, file, quyết định, TODO sinh viên, lệnh và test thật, lỗi, bước tiếp theo, Git. Phân biệt chạy hết khung hỗ trợ và hoàn thành thực nghiệm; không tuyên bố đồ án hoàn tất khi TODO chưa triển khai.
