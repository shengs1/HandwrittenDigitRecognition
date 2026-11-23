# FINAL AUDIT — tổng hợp hiện hành

Cập nhật23/11/2026, thay kết luận tiến độ cũ; hồ sơ trong outputs/ giữ nguyên theo thời điểm. Lượt này chỉ cập nhật tài liệu. Chi tiết bằng chứng: [FINAL_REVIEW](FINAL_REVIEW.md),[RESULTS_INDEX](RESULTS_INDEX.md),[HANDOFF](../HANDOFF.md).

## A. Tổng quan

**UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Code giao diện `f47a709`, tên model tiếng Anh/nhãn tiếng Việt; 53/53 tests đã ghi nhận21/11. Kỹ thuật đã kiểm nhưng chưa xác nhận đủ sản phẩm nộp và khả năng bảo vệ. Chưa có Critical mở được xác định trong phạm vi đã kiểm.

## B. Đối chiếu PDF

PASS là có bằng chứng kỹ thuật; PARTIAL là còn thiếu nội dung/xác nhận; FAIL là chưa có sản phẩm bắt buộc được xác nhận. Không dùng checklist để dự đoán điểm. Mục6 PDF không được tính lại thành blocker theo phạm vi đã chốt; PDF gốc giữ nguyên.

| Yêu cầu | Trạng thái | Bằng chứng hoặc việc thiếu |
|---|---|---|
|Bài toán/baseline/nguồn/schema/thiếu|PASS|Notebook1–3; Digits1797×64, nhãn0–9,65 cột thiếu0%|
|Làm sạch có lý do|PARTIAL|Không sai miền/trùng/hằng; giữ3 ảnh IQR; có nhật ký dự thảo, chờ nhóm xác nhận|
|Ít nhất5 EDA có nhãn/nhận định|PARTIAL|6 hình train và nhận định đã có, chờ nhóm rà/xác nhận|
|Baseline+2 model/Pipeline/split/CV/tuning|PASS|LR thô, KNN/MLP; 1437/360, stratify/42,5fold và grid chỉ train; khóa CV trước test|
|Độ đo/report/confusion/ảnh sai/curves/chi phí|PASS|CSV/JSON/hình và các lần kiểm đã ghi trong FINAL_REVIEW|
|Phân tích chính của nhóm|PARTIAL|Có dự thảo có nguồn, chưa có xác nhận/đóng góp thật|
|Năm câu đề tài13|PASS về bằng chứng|Notebook/RESULTS_INDEX trả lời đủ; không xác nhận thay vấn đáp|
|Seed/phiên bản/môi trường sạch|PASS|Requirements ghim, venv mới120 gói/53 tests, Git checkout giữ bytes|
|Demo suy luận bốn model|PASS|Không train/scale hai lần; Digits8×8, upload8×8 hoặc28×28; MNIST chỉ upload|
|Báo cáo PDF/DOCX, slide PPTX/PDF|FAIL/chưa xác nhận|Hiện có dự thảo Markdown10 mục/12 slide|
|Nhóm/phân công/đăng ký/vấn đáp|PARTIAL|Chưa có đầy đủ thông tin hoặc bằng chứng xác nhận|
|Ảnh điện thoại của nhóm|CHƯA KIỂM|Chưa có ảnh có nhãn; không dùng ảnh AI/font thay thế|

[REQUIREMENTS_MAP](REQUIREMENTS_MAP.md) có từng yêu cầu và năm câu chi tiết.

## C. Mô hình và số liệu

Phần A:run `20261117T081201Z_fd32180f`; KNN chọn theo CV macro F1 0,976170±0,007575, test accuracy96,6667%/F1 0,966304. LR95,8333%/F1 0,958075; MLP96,1111%/F1 0,960888. Giữ scaling/CV/grid/curves và chi phí gốc; không đổi mô hình theo demo.

Phần B:gray_bbox mean validation F1 0,59260 so0,48980 cũ; MLP MNIST54k/6k, khóa trước9890 MNIST và300 test ngoài. Đúng9632/9890=97,3913%; 262/300=87,3333%, F1 ngoài0,871326, còn38 lỗi; 82/82/98 trên100 ảnh mỗi nguồn. KNN ngoài48%→58%. Không gộp accuracy các dataset hoặc quy toàn bộ tăng cho tiền xử lý. Bảng7 hệ thống ở RESULTS_INDEX.

## D. Kiểm thử và tái lập

Notebook Run All/đối chiếu metric đã chạy17/11, không chạy lại23/11. Ngày19/11 kiểm venv mới Python3.12.14/120 gói,53 tests; bản xuất Git index đạt53 tests/11,204s. Có14 tình huống demo,8 lỗi model, bản demo tối thiểu không dataset,1200 replay và145 dòng độ đo được kiểm. Xem [hồ sơ freeze](../outputs/optimization_freeze_20261119T045133Z_728f35c1/REVIEW.md).

Ngày21/11 sau đổi ngôn ngữ:53/53 PASS,12,229s; browser1366×768 không tràn, thông tin kỹ thuật không cắt chữ, ghi trong HANDOFF. Ngày23/11 chỉ kiểm tài liệu/liên kết/số liệu/bảo toàn file; không gán lại thành lần chạy53 tests hoặc train mới.

## E. Lỗi và giới hạn

Các lượt trước đã sửa dòng accuracy trong CSV report, mẫu kiểm tra đúng split, UI/dropdown/thông tin kỹ thuật, byte Git/longpaths Windows và ngôn ngữ giao diện. Chưa có lỗi mô hình mới được xác định cần đổi trọng số hoặc thuật toán ảnh.

Còn giới hạn người viết, nguồn gốc từng ảnh Bitmap, xác suất chưa hiệu chỉnh và thiếu ảnh điện thoại có nhãn. 600 ảnh scan/giấy đã cắt/vẽ số không đại diện mọi ảnh thực tế. Không ép kết luận epoch quá khớp hoặc một nguyên nhân duy nhất cho lỗi ảnh ngoài.

## F. Tài liệu và sản phẩm

README hướng dẫn Windows/app/notebook/test và ảnh tự chụp; AGENTS là quy tắc hiện hành; HANDOFF giữ lịch sử. REPORT_OUTLINE có10 mục, SLIDE_OUTLINE có12 slide, VIVA_QUESTIONS có câu hỏi A/B; RESULTS_INDEX chỉ bảng/hình nguồn. Nhóm cần xác nhận nhận định và xuất bản nộp; không bịa tên/MSSV, phân công hoặc kết quả bảo vệ.

## G. Đóng gói và Git

Giữ bốn Pipeline/hai registry/module ảnh, metadata/split/lock cần app, requirements, notebook, docs và bằng chứng. Không đưa venv/cache/tmp/token vào Git. Giữ ghi công MIT/CC0/CC BY-SA và giới hạn nguồn; không sửa README/LICENSE bên thứ ba hoặc outputs/ để viết lại lịch sử.

Manifest snapshot có code/test/docs tại ngày chốt; đổi nhãn/tài liệu hợp lệ tạo khác biệt theo phiên bản. Không sửa manifest để che khác biệt hoặc train lại để cố khớp. Dùng test/registry cho hiện trạng; Git/HANDOFF để truy vết. Người dùng đã yêu cầu commit/push cụm tài liệu23/11 lên main; không force-push.

## H. Việc trước nộp

Nhóm rà/xác nhận nhật ký và phân tích, điền thông tin/phân công thật, xuất báo cáo PDF/DOCX và slide PPTX/PDF, kiểm hình/chữ/nguồn, tập vấn đáp/demo offline và thử ảnh tự chụp riêng. Giữ ảnh sai, không tuning theo test đã xem. Chưa có BM06 hoặc lịch nộp được xác nhận, không ước đoán điểm/ngày nộp.

## I. Lệnh chạy và tiếp tục

Từ gốc repo, Python3.12 tạo venv và cài requirements. Chạy `.venv/Scripts/python.exe -m streamlit run app.py` hoặc `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v`. [README](../README.md) có lệnh PowerShell đầy đủ, clone longpaths và quy tắc byte. Đối chiếu số liệu từ RESULTS_INDEX/file gốc; không lấy log hoặc fixture làm điểm mô hình chính.
