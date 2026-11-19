# Hướng dẫn tiếp tục đồ án

## FINAL FREEZE —19/11/2026

Người dùng đã review và duyệt gray_bbox/MLP MNIST28 sau kiểm tra cuối. Trạng thái: **UI FROZEN; CODE FROZEN; EXPERIMENTS FROZEN; DOCUMENTATION AND PRESENTATION IN PROGRESS.** Không mở thêm thử nghiệm, tuning hoặc redesign. Lượt này được yêu cầu commit/push lên main sau kiểm thử đạt; quyền này thay việc “chưa push trước review” ở các mục lịch sử. Không force-push, không đổi lịch sử remote.

Bằng chứng chốt `outputs/optimization_freeze_20261119T045133Z_728f35c1/`: venv mới120 gói tương thích/53 tests,14 chức năng+8 lỗi model, bản demo tối thiểu không data/download/fit,1200 replay app và audit145 dòng metric.4 Pipeline,notebook,module ảnh,CSS/requirements và artifact số liệu không đổi. Bảy tài liệu root/docs được phép cập nhật; không coi đổi tài liệu là đổi thực nghiệm. Ghi rõ giới hạn writer/Bitmap/ảnh điện thoại. Khi tiếp tục chỉ hoàn thiện tài liệu/thuyết trình hoặc sửa lỗi kỹ thuật có bằng chứng, rồi chạy kiểm tra liên quan; không dùng các test đã xem làm validation mới.

## Quyết định mới nhất — ảnh ngoài (2026-11-19)

Yêu cầu EXTERNAL RECOGNITION OPTIMIZATION cho phép thử preprocessing và huấn luyện một MLP MNIST riêng, sau đó tích hợp có điều kiện vào upload. Đây là ngoại lệ có phạm vi với các quy tắc lịch sử bên dưới: **giữ thiết kế UI FROZEN**, notebook,3 Pipeline/registry/số liệu Digits và toàn bộ đánh giá MNIST100 cũ. Không push bản tối ưu lên main trước người dùng review. Không thêm dependency hoặc tự huấn luyện khi mở app.

Run mới `outputs/external_optimization_20261118T175401Z_4ca3a08f/`: protocol/manifest/split khóa trước suy luận, lựa chọn khóa trước test.600 ảnh bytes gốc từ3 repo,300 validation/300 test, seed42,10/lớp/nguồn/split; không có writer ID đáng tin nên không tuyên bố tách người viết. Bitmap có giới hạn truy vết từng ảnh upstream; xem data/external_handwriting/SOURCES.md. Không đổi nhãn/bỏ mẫu vì dự đoán sai.

Validation chọn `gray_bbox` cho upload8×8. Một Pipeline MinMaxScaler→MLP(128,64) MNIST,54000 train/6000 validation, seed42, không augmentation; dùng `mnist28` nhất quán từ external_preprocessing.py. Loại110 MNIST test đã xem, đánh giá9890 còn lại sau khóa. Không dùng600 ảnh mới để train. Cả9890 MNIST và300 handwriting test **đã xem kết quả**, không được dùng chúng tuning hoặc chọn lại trong lượt tiếp theo.

`models/external_registry.json` riêng ràng buộc hash module/model/selection lock. MLP MNIST chỉ có ở upload,784 đặc trưng/28×28/0–255;3 model Digits giữ64/8×8/0–16. Scaler ở Pipeline, không gọi ngoài. Không tự chuyển model theo confidence. Ba thẻ thống kê vẫn là Digits chính thức. Hàm baseline app.preprocess_uploaded_image và UI_STYLE giữ nguyên để đối chiếu/khôi phục. Thay đổi model/module sau khóa phải được coi là thực nghiệm mới với validation/test độc lập.

Đọc REPORT.md/README.md trong run và HANDOFF để lấy số liệu, lệnh tái lập,53 tests/bằng chứng browser, giới hạn và cách rollback. Không sửa bảng số liệu chỉ để khớp nhận định. Nhận định mới là dự thảo cần nhóm rà soát/xác nhận; không bịa đóng góp. Mục UI phía dưới phản ánh phiên bản trước khi có ngoại lệ mới này.

## UI FROZEN — phiên bản chính thức (2026-11-18)

Người dùng đã duyệt và chốt giao diện hiện tại. Không tiếp tục đổi thiết kế, màu, typography, bố cục hoặc thêm tính năng. Chỉ sửa lỗi chức năng có bằng chứng khi được yêu cầu. Không tự fit/tuning/chỉnh notebook, tiền xử lý hay artifact để thay đổi kết quả demo. Đọc mục UI FROZEN trong HANDOFF để lấy kiểm thử cuối và trạng thái Git; các mục UI bên dưới là lịch sử quyết định. Người dùng đã yêu cầu commit/push toàn bộ phiên bản UI đã duyệt và bằng chứng lên origin/main sau khi kiểm thử đạt; không force-push.

## UI hiện tại (2026-11-18)

Technical expander dùng bảng thông số đọc trực tiếp Pipeline đã lưu và metadata dữ liệu; không repr/code block, run ID/checksum dài trên giao diện người dùng. Giữ kết quả MNIST3/10 mỗi model trong notebook/README/tài liệu/artifact. Văn bản technical tự giãn/đổi dòng, không fixed height. Reset cả margin âm stCaptionContainer trong phạm vi demo. CSS nút predict không được ép min-height lên nút native dropdown; giữ hành vi chuột/bàn phím native. Bằng chứng mới nhất15 vùng bấm/3 model/43 tests và screenshot trong HANDOFF mục Interaction Fix.

Bản Responsive Fix đặt chọn chữ số/ID selectbox trong cột ảnh, chỉ lấy option từ đúng nguồn/lớp/split đã lưu. Không đưa slider ID ra hàng toàn trang. Đánh giá vừa màn hình phải đo cả document và stMain (Streamlit có vùng cuộn riêng), ở zoom100% và actual innerWidth/innerHeight. Không dùng CSS zoom/scale/giấu nội dung để vượt kiểm tra. Margin âm của Markdown đã được reset trong phạm vi demo để wrapper HTML không chồng nhau. Bằng chứng45 trạng thái/năm viewport và40 tests mới nhất ở đầu HANDOFF.

Giao diện được thiết kế lại trong app.py + `.streamlit/config.toml`, giữ nguyên notebook/requirements/Pipeline/tiền xử lý. Mặc định nguồn test đúng split; preview Digits nearest-neighbor chỉ phục vụ hiển thị. Overview đọc artifact chính thức. Session state lưu kết quả kèm ngữ cảnh model/checksum/nguồn/ID/nền/ảnh, phải xóa kết quả khi ngữ cảnh đổi. Giữ các kiểm tra chức năng khi chỉnh widget, không thay số liệu hoặc xác suất để giống ảnh tham chiếu. CSS ưu tiên class riêng và class theo key container, không dùng class sinh ngẫu nhiên. Đọc HANDOFF để lấy log 40 tests, screenshot 3 viewport và trạng thái Git mới nhất.

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
