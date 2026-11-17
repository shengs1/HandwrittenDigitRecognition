# Hướng dẫn tiếp tục đồ án

## Trạng thái hiện tại — Final Completion

Run chính thức `20261117T081201Z_fd32180f` và registry/Pipeline/số liệu được giữ nguyên. Lượt hoàn thiện này được phép soạn nhận định **dự thảo có nguồn thật**, chưa xác nhận thay nhóm. Notebook là bản thực nghiệm đầy đủ, không còn TODO nhận định; báo cáo Markdown 10 mục và nội dung 12 slide vẫn cần nhóm rà soát và xuất bản nộp. Sau lượt hoàn thiện, người dùng đã yêu cầu **commit và push các thay đổi mới lên main** (2026-11-17); yêu cầu này thay thế việc giữ local ở lượt trước. Không force-push hoặc đổi lịch sử remote.

Demo có nguồn “Ảnh test Digits” đọc đúng `outputs/<registry.run_id>/split_indices.csv`; không chia lại. Kiểm thử bất biến tiền xử lý dùng ảnh train; không dùng 10 MNIST đã xem để tối ưu. Chỉ sửa preprocessing khi có lỗi khách quan; hiện giữ thuật toán cũ. Đọc HANDOFF.md để lấy bằng chứng kiểm thử mới nhất; các phase cũ trong đó là lịch sử.

## Bắt đầu mỗi phiên

Đọc toàn bộ `docs/Huong_Dan_Do_An_CuoiKy.pdf`, `HANDOFF.md`, notebook và outputs trước khi sửa. Chạy `git status --short --branch` và `git diff`. Không xóa hoặc ghi đè thay đổi của người dùng. Chỉ khởi tạo Git, commit hoặc push khi người dùng đã yêu cầu; không đổi dataset. Repo là `https://github.com/shengs1/HandwrittenDigitRecognition`, nhánh `main`. Không force-push hoặc thay đổi lịch sử remote.

## Mục tiêu và yêu cầu

Đề tài 13: phân loại chữ số 0–9 bằng `sklearn.datasets.load_digits()`. Python, NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, Jupyter và Joblib. Phase 2 được phép dùng Streamlit và Pillow để làm demo local đơn giản. Không database, tài khoản hoặc backend riêng.

PDF: có baseline, ≥2 mô hình so với baseline, EDA ≥5 biểu đồ có nhãn và nhận định, kiểm tra/làm sạch có lý do, Pipeline, chia dữ liệu đúng, CV/tuning, phân tích lỗi, seed và phiên bản thư viện. Thang điểm: dữ liệu/EDA/chuẩn bị 4; mô hình/đánh giá 4; trình bày/vấn đáp 2. Nhóm cần báo cáo, slide, phân công thật và khả năng giải thích toàn bộ bài; demo là tùy chọn trong quy trình PDF.

Năm câu hỏi đề tài: (1) vector/shape và chuẩn hóa pixel; (2) baseline đạt bao nhiêu, MLP cải thiện thế nào; (3) cặp nhầm lẫn; (4) learning curve và bằng chứng quá khớp; (5) chi phí so với độ chính xác. Không giả định có cải thiện hoặc quá khớp.

## Kiến trúc và quyết định

Notebook `digit_classification.ipynb` là tài liệu chính, 16 mục đúng thứ tự yêu cầu người dùng. Chỉ dùng hàm ngắn, không framework/module/class phụ. `tests/` kiểm tra hợp đồng dữ liệu và khung notebook; `docs/` giữ tài liệu gốc, hướng dẫn đối chiếu. `models/`, `outputs/` chỉ chứa kết quả thật, có nguồn gốc rõ ràng.

Người dùng đã yêu cầu hoàn thiện code cốt lõi và xác nhận huấn luyện lần đầu theo cấu hình hiện tại (2026-11-17). Run xác nhận: `20261117T081201Z_fd32180f`; giữ nguyên Pipeline và kết quả này, không tự fit/tuning lại chỉ để tăng điểm. KNN được chọn bằng CV; registry/hash tại `models/registry.json` là bộ artifact cố định của demo. Notebook chạy offline tạo run mới nhưng không tự thay registry đang có.

`app.py` chứa giao diện và các hàm ngắn tiền xử lý/tải Pipeline/suy luận; import không chạy UI. App chỉ load joblib, cache theo checksum/mtime/size, không `.fit`, không tự chọn theo test. Mẫu Digits giữ nguyên pixel, ảnh upload xử lý màu nền/grayscale/crop/căn giữa/resize 8×8/0–16. StandardScaler chỉ nằm trong Pipeline, không chuẩn hóa hai lần. Xác suất phải gắn đúng classes_, không gọi là xác suất đã hiệu chỉnh.

10 ảnh MNIST test trong `tests/fixtures/external_digits/` chỉ dùng kiểm thử suy luận bên ngoài; không đổi dataset huấn luyện, chọn lại ảnh hoặc sửa mô hình theo kết quả này. Chưa có ảnh chụp của nhóm, không giả định MNIST đại diện ảnh điện thoại.

Train/test 80/20, `stratify=y`, `random_state=42`. Baseline Logistic Regression trên pixel thô, bước preprocessing `passthrough`. Hai mô hình KNN và MLP dùng Pipeline. MLP ban đầu `(64,32)`, relu, adam, early_stopping=True; seed 42. Chuẩn hóa dùng StandardScaler trong Pipeline. Thử MLP thô/chuẩn hóa cùng cấu hình và folds. StratifiedKFold 5, shuffle=True, seed 42. Grid nhỏ; chọn theo CV macro F1, hòa tuyệt đối dùng thứ tự tên ổn định; không chọn theo điểm test. Ghi rõ CV sau tuning có thiên lệch lựa chọn, không phải đánh giá độc lập.

Đo fit cuối bằng clone Pipeline rồi fit một lần trên cùng train; predict cùng test, cùng máy và số luồng, lặp đo có ghi rõ; tuning tính riêng, không nhập thời gian refit vào fit cuối. Dung lượng là byte của toàn bộ Pipeline với cùng quy tắc joblib. Learning curve chỉ dùng train/CV; loss MLP và validation score khác đơn vị. Thứ tự mục 11–14 là nơi hướng dẫn/khai báo hàm; chỉ gọi test sau khi khóa lựa chọn ở mục 15.

## Chống rò rỉ

- Không fit scaler, PCA, imputer hoặc lựa chọn đặc trưng trên toàn bộ dữ liệu trước CV. PCA EDA chỉ fit train, không đưa tọa độ EDA vào mô hình.
- Không sử dụng test để tuning, chọn preprocessing, threshold, số vòng lặp, mô hình hoặc xử lý ảnh khó. Chỉ kiểm tra hợp lệ và trùng xuyên tập; không xem phân bố/ảnh test trước đánh giá cuối.
- Kiểm tra ảnh giống hệt trong dữ liệu, giữa train/test và giữa các fold. Nếu gặp trùng xuyên tập: dừng; nhóm ghi quyết định loại trùng trước split hoặc đề xuất chia theo nhóm; không âm thầm đổi tỷ lệ/seed/yêu cầu.
- Không xóa ảnh chỉ vì khó hoặc dự đoán sai. Bất thường thống kê chỉ là gợi ý xem xét; mọi quyết định làm sạch do nhóm ghi bằng chứng và lý do.
- StandardScaler trong Pipeline được fit trên train của mỗi CV fold. Early stopping MLP có validation nội bộ; scaler thấy các đặc trưng của phần validation nội bộ đó nhưng không thấy fold validation ngoài hay test. Nêu giới hạn này khi diễn giải.
- Mục 15 khóa lựa chọn bằng kết quả CV trước predict test. Sau xem test chỉ phân tích, không quay lại tuning.

## Nội dung báo cáo và tính trung thực

Code cốt lõi đã hoàn thiện và huấn luyện lần đầu được xác nhận; không còn TODO triển khai cũ. Theo yêu cầu Final Completion mới nhất, được viết nhận định dự thảo từ output thật; phải ghi chưa được nhóm xác nhận. Nhóm kiểm tra/sửa/xác nhận, hoàn thiện báo cáo/slide, hiểu và bảo vệ được quyết định. Không gán dự thảo hoặc công việc chưa xác minh thành đóng góp của sinh viên.

Không bịa số liệu, đóng góp thành viên hoặc kết quả test; không dùng fixture tổng hợp như số liệu thực nghiệm thật. Người dùng yêu cầu xóa file nhật ký công cụ riêng; không tạo lại file đó. Giữ lịch sử kỹ thuật trong HANDOFF.md, không chỉnh sửa lịch sử Git đã công bố.

Final review ở `docs/FINAL_REVIEW.md`. Chỉ PASS khi có bằng chứng; không biến dàn ý/TODO thành phân tích đã được nhóm xác nhận. Rerun kiểm chứng được phép trong checkout riêng theo yêu cầu review, giữ registry/model/số liệu canonical; không chọn run có điểm tốt hơn. Dòng accuracy trong CSV classification report là metric scalar: precision/recall để trống, support là số mẫu, không broadcast accuracy vào cột support.

Theo yêu cầu mới nhất, mục 6 về sử dụng công cụ trong PDF không thuộc phạm vi audit hoặc danh sách việc cần làm; không nhắc lại như điều kiện cản trở hoàn thành. Giữ nguyên PDF gốc. Quyết định này không bỏ các kiểm tra kỹ thuật notebook/code. Bản tổng hợp Final Audit A–I ở `docs/FINAL_AUDIT.md`.

Sau mỗi cụm việc lớn cập nhật `HANDOFF.md`: phase, việc thực sự hoàn thành, file, quyết định, TODO sinh viên, lệnh và test thật, lỗi, bước tiếp theo, Git. Phân biệt chạy hết khung hỗ trợ và hoàn thành thực nghiệm; không tuyên bố đồ án hoàn tất khi TODO chưa triển khai.
