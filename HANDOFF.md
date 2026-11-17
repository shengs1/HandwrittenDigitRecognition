# Chuyển giao Codex / Antigravity

## Phase hiện tại

Phase 2: demo Streamlit, hoàn thiện code thực nghiệm và tài liệu chuẩn bị báo cáo. Người dùng đã xác nhận huấn luyện lần đầu bằng cấu hình đã thống nhất. Không tự huấn luyện lại để cải thiện điểm.

## Trạng thái mới nhất đã xác minh

**Phase 2 thay thế trạng thái khung cũ bên dưới:** run `20261117T081201Z_fd32180f` đã hoàn tất huấn luyện lần đầu, 23 cell chạy qua kernel thật, xuất 3 Pipeline và 55 file kết quả, không stderr trong cell. `models/registry.json` khóa bộ mô hình demo, chọn KNN bằng mean CV macro F1. App hoạt động với ảnh mẫu/upload, xác suất và xử lý lỗi; **25/25 test qua trên môi trường sạch**, đã thử trực tiếp cả hai luồng bằng trình duyệt. Bằng chứng ở `outputs/demo_20261117T082316Z_b269f12c/phase2_status.json`. Nhóm còn tự viết phân tích chính, báo cáo/slide, phân công và bổ sung ảnh tự chụp. Các mục “chưa có mô hình”, “TODO SV-01…09”, “không Streamlit” bên dưới chỉ mô tả lịch sử Phase 1.

**Cập nhật Git (2026-11-17):** đã khởi tạo, liên kết, commit và push bản khung lên https://github.com/shengs1/HandwrittenDigitRecognition, nhánh `main` theo yêu cầu người dùng. Commit nguồn đầu tiên `a5ded5b44d9fcfc3ae02f9fb6ca99bf69b814232` đã được xác minh trên remote; `main` theo dõi `origin/main`. Các ghi nhận “chưa khởi tạo Git” bên dưới là lịch sử trước yêu cầu này. Xem `git log -1` để lấy commit mới nhất, bao gồm các cập nhật nhật ký sau commit nguồn.

**Ngày 2026-11-17 (Asia/Saigon): phần khung hỗ trợ đã chạy được; thực nghiệm cốt lõi chưa triển khai.** Notebook cuối có 51 cell (23 cell mã), chạy bằng kernel thật, 6 hình nhúng, 0 lỗi thực thi, 0 stderr trong cell. Không mô hình nào đã được huấn luyện. Các cụm bên dưới là nhật ký lịch sử; trạng thái ở đây và cụm 3 thay thế các dòng “đang chạy” trước đó.

- Run hiện khớp với output nhúng trong notebook: `outputs/20261117T070246Z_4ebb5029/`.
- Bằng chứng: `support_verification.json`, `run_status.json`, `environment.json`, CSV và 6 hình trong run đó.
- `models/` chỉ có `.gitkeep`, chưa có Pipeline `.joblib`, accuracy/F1/report/ma trận nhầm lẫn hoặc kết quả CV mô hình.
- Sinh viên tiếp tục từ nhật ký mục 3 và TODO SV-01…SV-09; không bật cờ thực nghiệm khi các hàm còn NotImplementedError.

## Cụm 1: đọc yêu cầu và kiểm tra môi trường (2026-11-17, Asia/Saigon)

- Đã đọc toàn bộ 6 trang PDF bằng pypdf, render cả 6 trang và xem bản ghép.
- Ban đầu thư mục chỉ có `docs/Huong_Dan_Do_An_CuoiKy.pdf`; không có notebook hay thay đổi mã nguồn để ghi đè.
- Đã tạo `AGENTS.md`, `.gitignore`, `requirements.txt`, `HANDOFF.md`.
- Quyết định: khung hỗ trợ chạy độc lập, TODO cốt lõi thuộc sinh viên; không tạo điểm mô hình khi chưa có triển khai.
- `git status --short --branch`: lỗi `not a git repository`; chưa khởi tạo Git.
- `python --version`: alias WindowsApps không chạy được. Tìm được Python đóng gói của Codex; có NumPy/Pandas/pypdf nhưng thiếu sklearn, matplotlib, seaborn, joblib, Jupyter.
- Lần đầu `uv venv` lỗi quyền ghi cache mặc định; đã dừng, sẽ chuyển cache vào workspace.
- Tiếp theo: dựng môi trường cục bộ, tạo notebook, tài liệu đối chiếu, kiểm tra và chạy phần hỗ trợ.
- Sinh viên cần tự viết phần cốt lõi và nhận định; chưa có thông tin đóng góp thực tế.

## Cụm 2: khung và tài liệu

- Đã tạo `digit_classification.ipynb`: 50 cell, 16 mục, 6 EDA train, TODO SV-01…SV-09, quy tắc CV, helper đo/lưu và điều phối test sau khóa lựa chọn. Chưa triển khai hoặc chạy mô hình.
- Đã tạo `README.md`, `AI_USAGE.md`, `docs/REQUIREMENTS_MAP.md`, `tests/test_contracts.py`, `tests/run_support_notebook.py`, `models/.gitkeep`, `outputs/.gitkeep`.
- Đã tạo `.venv` bằng Python 3.12.14; chuyển cache uv vào `.uv-cache`. Cài requirements từ PyPI thành công sau khi chạy ngoài giới hạn mạng sandbox; không có yêu cầu xác nhận bổ sung từ người dùng.
- `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`: **8/8 qua**, 0.180 giây theo unittest, có DeprecationWarning từ sklearn 1.7.2 với NumPy 2.5.5.
- Đang chạy kernel thật qua `tests/run_support_notebook.py`; chưa có xác nhận thành công tại thời điểm ghi cụm này. Chưa có hình hoặc số liệu mô hình để công bố.
- Quyết định: lựa chọn macro F1 CV đã định trước; file khóa trước test; run riêng không ghi đè; ghi rõ early stopping validation nội bộ và thiên lệch lựa chọn CV. Không tự khởi tạo Git.

## Cụm 3: chạy thật, chỉnh hình và kiểm tra cuối

### File đã tạo/chỉnh sửa

- `digit_classification.ipynb`: 16 mục đúng thứ tự; schema đủ 65 cột gồm nhãn, kiểm tra chất lượng, split/CV không trùng, 6 hình train, chẩn đoán ảnh train, API/hợp đồng và 9 TODO cốt lõi; helper đo chi phí/lưu Pipeline; điều phối khóa CV trước test.
- `requirements.txt`: ghim 12 thư viện trực tiếp/tính toán, Python 3.12+; NumPy 2.3.5 và sklearn 1.7.2. `README.md`: cách cài/chạy/kiểm tra và giới hạn khung.
- `AGENTS.md`, `AI_USAGE.md`, `HANDOFF.md`: quy tắc phối hợp, liêm chính và trạng thái thật. `docs/REQUIREMENTS_MAP.md`: đối chiếu yêu cầu, thang điểm và 5 câu hỏi.
- `.gitignore`, `models/.gitkeep`, `outputs/.gitkeep`, `tests/test_contracts.py`, `tests/run_support_notebook.py`.
- `.venv/`, `.uv-cache/`, `tmp/` là môi trường/cache/tiện ích tạo file tạm đã gitignore, không phải module của đồ án. Không cần đưa vào bài nộp.
- PDF gốc không bị chỉnh sửa; SHA256 hiện tại: `6D9CC9630C84AD1C33E55182F867B473DD721E809C411B996FA4C95C33B2B893`.

### Kết quả thực tế hiện có

| Kiểm tra | Kết quả đã chạy |
|---|---|
| Dữ liệu | X=(1797,64), ảnh=(1797,8,8), y=(1797,), X float64, y int64 |
| Nhãn / pixel | 0–9 / 0–16 |
| Thiếu, sai miền pixel, sai nhãn, trùng, nhãn mâu thuẫn, ảnh hằng | Đều 0 theo các phép kiểm tra đã cài; không có nghĩa đã chứng minh mọi ảnh đều bình thường |
| Split | Train 1437, test 360; 80/20, stratify=y, seed 42 |
| Trùng ảnh train/test và từng CV fold | 0 |
| CV | Đã dựng/kiểm tra 5 folds; **chưa tính điểm CV mô hình** |
| EDA | 6 hình train, đủ tiêu đề/trục/chú thích; đã xem hình và chỉnh legend/grid |
| Chẩn đoán ảnh train | 1437 hàng; 3 ảnh gắn cờ IQR độ sáng, cần nhóm xem; không tự loại ảnh |
| PCA EDA | PC1=0.14759158271185724, PC2=0.13742697243389737, tổng khoảng 28.50% phương sai; chỉ dùng train |
| Mô hình / tuning / test metrics | Chưa chạy; không có số liệu để kết luận |

Run cuối có 20 file thực tế: schema, summary, DESCR, data quality/flags, environment, split indices/summary, CV fold audit, train counts/PCA/image diagnostics, run status/support verification và 6 PNG. Hai run trước giữ lại để không ghi đè lịch sử: `20261117T065811Z_92ed829e` (NumPy 2.5.5) và `20261117T070056Z_e9dcb2cd` (trước chỉnh legend cuối). Khi dùng hình/số liệu hiện tại, dùng run cuối nêu trên.

### Lệnh và kiểm tra

- `uv --cache-dir .uv-cache venv .venv --python <Python-đóng-gói-Codex>`: thành công, Python 3.12.14.
- `uv --cache-dir .uv-cache pip install --python .venv/Scripts/python.exe -r requirements.txt`: lần đầu trong sandbox lỗi DNS PyPI; chạy có quyền truy cập mạng thành công. Lần cập nhật requirements đổi NumPy 2.5.5 → 2.3.5 thành công.
- `uv --cache-dir .uv-cache pip check --python .venv/Scripts/python.exe`: **107 package tương thích**, 23 ms.
- `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`: **8/8 qua**, lần sau cập nhật NumPy 0.117 giây, không còn DeprecationWarning.
- `.venv/Scripts/python.exe -X utf8 tests/run_support_notebook.py`: lần đầu sandbox bị kẹt socketpair của asyncio trước chạy cell; đã dừng và dùng faulthandler xác định nguyên nhân. Chạy với socket localhost được phép thành công. Lần cuối: **Executed 23 code cells; embedded figures=6; errors=0; student models=0**.
- Kiểm tra sau chạy: nbformat hợp lệ, cả 23 cell có execution_count, không output lỗi/không stderr, run status là support-only, không file joblib; chẩn đoán ảnh chỉ chứa id train, không id test. Xem trực tiếp cả 6 hình và bản cập nhật của các hình được chỉnh.
- `git status --short --branch`, `git diff --stat`: không có Git repository; chưa init, commit hoặc có diff Git để bàn giao.

### Lỗi, giới hạn và phần chưa kiểm thử

- Không còn lỗi thực thi được phát hiện ở phần hỗ trợ. Kernel có cảnh báo khởi động TCP không mã hóa của Jupyter (kết nối nội bộ); không có cảnh báo trong output cell ở bản cuối. Chưa kiểm tra thao tác tương tác bằng giao diện web Jupyter.
- Các hàm SV-01…SV-09 còn cố ý `NotImplementedError`, chưa được triển khai hoặc kiểm thử. Cờ False làm bỏ qua nhánh thực nghiệm; Run All thành công chỉ xác nhận **khung hỗ trợ**.
- Helper fit/predict cuối, xuất/đọc lại Pipeline, khóa lựa chọn và nhánh xuất kết quả mô hình chưa được thực thi do chưa có code cốt lõi; không tuyên bố round-trip joblib đã qua kiểm tra.
- Chưa có nhật ký quyết định của nhóm, nhận định EDA, kết luận CV/test, phân tích lỗi/quá khớp, báo cáo, slide hoặc đóng góp thành viên xác minh được. Chưa có BM06 trong project để đối chiếu chi tiết hơn.
- Cài môi trường sạch lần đầu và import/chạy khung đã thực hiện trên máy này; chưa thử trên máy khác. requirements ghim thư viện trực tiếp, không khóa toàn bộ dependency bắc cầu.

### Việc nhóm cần làm tiếp

1. Đọc PDF, các output thật, kiểm tra 3 ảnh IQR bằng `review_train_image(id)`; tự ghi quyết định xử lý có lý do, không mặc định xóa ảnh.
2. Tự triển khai và kiểm thử SV-01…SV-09 theo hợp đồng trong notebook; giữ baseline thô, Pipeline/fold đúng và grid nhỏ. Tự viết 6 nhận định EDA và giải thích metric.
3. Khi code sẵn sàng, ghi CLEANING_DECISION và STUDENT_PROTOCOL_NOTE rồi bật cờ thực nghiệm; Restart Kernel/Run All, kiểm tra warning. Không chọn lại bằng test; không sửa tay output.
4. Kiểm chứng các nhánh chưa chạy: model fit, CV/scaling, metric, confusion pairs/ảnh sai, curves, thời gian và round-trip Pipeline. Ghi số liệu thật và giới hạn, chấp nhận không thấy MLP cải thiện/không có bằng chứng overfitting.
5. Tự viết báo cáo/slide, phân công và đóng góp thực tế trong AI_USAGE.md; mọi thành viên giải thích được bài. Cập nhật HANDOFF.md sau mỗi cụm việc. Git hiện vẫn chưa khởi tạo; không có commit hoặc thay đổi người dùng bị ghi đè.

## Cụm 4: ghi nhận repo GitHub do người dùng tạo

- Repo: https://github.com/shengs1/HandwrittenDigitRecognition, do người dùng thông báo đã tạo.
- `git status --short --branch`, `git remote -v`, `git log -1`: đều báo `not a git repository` tại thư mục project.
- `git -c credential.interactive=false ls-remote --symref <repo>.git HEAD` và `git -c credential.interactive=false ls-remote <repo>.git`: exit 0, không có output/ref. Truy cập mạng trong sandbox ban đầu lỗi DNS; kiểm tra chỉ đọc ngoài sandbox thành công.
- Đã thêm liên kết repo vào `README.md`, cập nhật `HANDOFF.md`, `AI_USAGE.md`. Không sửa notebook, dữ liệu, requirements hoặc output.
- Chưa init Git/đặt origin/commit/push: thông báo tạo repo chưa phải yêu cầu thực hiện các bước đó. Chưa có mã nguồn nào được đồng bộ trong phiên này.
- Không chạy lại test vì chỉ cập nhật tài liệu; kết quả kiểm thử code gần nhất vẫn là cụm 3. TODO học thuật và các nhánh chưa kiểm thử không thay đổi.
- Bước tiếp theo khi có yêu cầu đồng bộ: kiểm tra lại remote và file cần đưa lên, khởi tạo/liên kết Git cục bộ rồi commit/push theo phạm vi được yêu cầu; không đưa `.venv`, cache hoặc `tmp` lên repo.

## Cụm 5: khởi tạo và đồng bộ Git theo yêu cầu người dùng

- Phạm vi đã được yêu cầu: làm các bước Git và push bản khung hiện tại. Giữ nguyên giới hạn hỗ trợ học thuật; không tự hoàn thành TODO cốt lõi hoặc viết nhận định thay nhóm.
- Đã kiểm tra `git ls-remote <repo>.git`: exit 0, không ref; không có lịch sử remote cần ghi đè. Git author đã được cấu hình sẵn, không đổi danh tính hoặc cấu hình global.
- `git init -b main`: thành công. `git remote add origin https://github.com/shengs1/HandwrittenDigitRecognition.git`: thành công.
- `git check-ignore` xác nhận `.venv/`, `.uv-cache/`, `tmp/`, `tests/__pycache__/` bị loại. Đã đưa notebook, PDF gốc, tài liệu, requirements, tests, thư mục models rỗng và cả 3 run hỗ trợ lên repo; không bỏ lịch sử output. Tổng 72 file, khoảng 3.29 MB dữ liệu file trước nén Git. Quét mẫu private key/token GitHub trên các file text trước stage không phát hiện khớp.
- Kiểm tra trước push: `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`: **8/8 qua**, 0.141 giây, không warning/lỗi. Không chạy lại notebook vì không thay mã thực nghiệm; bằng chứng kernel gần nhất vẫn là cụm 3.
- Đã chỉnh `AGENTS.md` ghi rõ yêu cầu Git hiện tại; cập nhật `HANDOFF.md`, `AI_USAGE.md`. Chưa thay notebook hoặc kết quả.
- `git add -- <các đường dẫn đã kiểm tra>` và `git diff --cached --check`: thành công, không lỗi whitespace. Git có thông báo chuyển LF/CRLF theo cấu hình máy Windows, không gây lỗi commit.
- `git commit -m 'Add Digits project scaffold and verified EDA outputs'`: thành công, commit `a5ded5b44d9fcfc3ae02f9fb6ca99bf69b814232`, 72 file.
- `git -c credential.interactive=false push -u origin main`: thành công, tạo nhánh `main` trên remote và cấu hình upstream. Không force-push, không sửa lịch sử hoặc cấu hình Git global.
- `git ls-remote origin refs/heads/main`: trả về đúng `a5ded5b44d9fcfc3ae02f9fb6ca99bf69b814232`. `git status --short --branch` sau push nguồn: `## main...origin/main`, không có thay đổi chưa commit tại thời điểm đó. Bản ghi nhận kết quả này được lưu ở cập nhật tài liệu tiếp theo.
- Không phát hiện lỗi đồng bộ. Việc đưa mã lên GitHub không thay đổi trạng thái học thuật: TODO SV-01…SV-09, nhận định và các nhánh mô hình chưa triển khai/kiểm thử vẫn cần sinh viên thực hiện theo cụm 3.

## Cụm 6: Phase 2 — hoàn thiện thực nghiệm và dựng demo

- Đã đọc lại đầy đủ 6 trang PDF, AGENTS, HANDOFF, notebook và tất cả trạng thái run cũ; Git ban đầu sạch trên main, commit dd6c86c. Xác minh chưa có Pipeline trước Phase 2.
- Người dùng xác nhận rõ được huấn luyện **lần đầu theo cấu hình hiện tại**. Đã triển khai đủ 9 hàm cốt lõi, giữ nguyên split/seed/grids/kiến trúc/tiêu chí CV. Không giả định kết quả tồn tại trước đó, không tuning sau test.
- `.venv/Scripts/python.exe -X utf8 tests/run_notebook.py`: thành công; run `20261117T081201Z_fd32180f`, chọn `knn`, 3 Pipeline round-trip joblib khớp dự đoán test. Đây là lần chạy đầy đủ đầu tiên, không phải thay một kết quả đã xác nhận.
- Kết quả test thật (accuracy / macro F1): Logistic Regression 0.958333 / 0.958075; KNN 0.966667 / 0.966304; MLP 0.961111 / 0.960888. Mean CV macro F1: 0.963687 / 0.976170 / 0.962365. Chi tiết thời gian, độ lệch chuẩn và kích thước có trong model_comparison.csv.
- Đã tạo `app.py`, `tests/run_notebook.py`, `tests/test_demo.py`, 10 fixture MNIST test có manifest nguồn/checksum; cập nhật notebook, requirements, tests/test_contracts và AGENTS. Thay runner hỗ trợ cũ bằng runner notebook đầy đủ. Xóa file nhật ký công cụ riêng theo yêu cầu mới.
- App không fit: đọc registry, kiểm checksum/cache Pipeline; hai nguồn ảnh, grayscale/đảo nền/alpha/căn giữa/resize 8×8/0–16, preview và xác suất; ảnh Digits không đi qua nhánh crop/resize upload.
- Cài Streamlit 1.67.0 và Pillow 13.0.0 trong .venv; các phiên bản tính toán đã dùng trước đó được giữ nguyên.
- Đang kiểm thử chức năng và chuẩn bị dàn ý báo cáo/slide/vấn đáp; chưa coi Phase 2 hoàn tất. Nhóm vẫn cần tự viết phân tích chính và phân công thực tế.

## Cụm 7: Phase 2 — kiểm thử, tài liệu và bàn giao

### File và chức năng

- `app.py`: chọn 3 mô hình, chọn lớp/id mẫu Digits hoặc upload PNG/JPEG/BMP/WebP; preview gốc/8×8, dự đoán và xác suất đúng classes_. Nhận dạng nền tự động hoặc chọn nền, alpha/EXIF/grayscale, crop/căn giữa/giữ tỷ lệ/resize, miền 0–16; không StandardScaler bên ngoài Pipeline. File 10 MB/16 triệu pixel; lỗi ảnh hỏng/trống/thiếu model được hiển thị gọn.
- `models/registry.json`, `models/20261117T081201Z_fd32180f/{logreg_raw,knn,mlp}.joblib`, `metadata.json`: artifact thật. Checksum của cả 3 không đổi sau kiểm thử/demo. KNN k=3, uniform; MLP (64,32), alpha=0.0001, chuẩn hóa, relu/adam/early stopping; baseline LR C=1 pixel thô. Giữ mọi quyết định CV đã đặt trước.
- Notebook đã triển khai code cốt lõi, giữ 16 mục, chưa viết thay nhóm các nhận định EDA/nội dung phân tích chính. Tạo đủ CV/scaling/report/errors/learning curve/history/cost/export trong run nêu trên; không chạy lại training khi sửa app.
- `requirements.txt`: thêm Streamlit 1.67.0/Pillow 13.0.0, giữ nguyên phiên bản tính toán. `README.md`: Windows setup, notebook/demo/tests, run cố định, lỗi và giới hạn. `AGENTS.md`: cập nhật scope Phase 2, khóa model, chống leakage và quy tắc ảnh upload.
- `docs/REPORT_OUTLINE.md`: đúng 10 mục PDF; `docs/SLIDE_OUTLINE.md`: 12 slide; `docs/VIVA_QUESTIONS.md`: 30 câu; `docs/RESULTS_INDEX.md`: bảng metric/cost/scaling/cặp nhầm/curves và liên kết nguồn thật. Cập nhật REQUIREMENTS_MAP cho trạng thái mới.
- `tests/test_demo.py`, `tests/test_contracts.py`, `tests/check_demo.py`, `tests/run_notebook.py`, fixture MNIST và manifest. Runner support cũ đã thay. File nhật ký riêng được xóa đúng yêu cầu, không tạo lại.

### Lệnh đã chạy và kết quả thật

- `uv --cache-dir .uv-cache pip install --python .venv/Scripts/python.exe 'streamlit>=1.40,<2' 'pillow==13.0.0'`: thành công; sau đó requirements ghim đúng bản đã dùng.
- `.venv/Scripts/python.exe -X utf8 tests/run_notebook.py`: hoàn tất lần train đầu, 23 code cells; joblib round-trip kiểm khớp test. Không train lại sau đó.
- `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`: sau sửa loader, 24/24 qua, 3.585 giây theo unittest. Sau đó bổ sung một test nhánh thiếu file Pipeline.
- `uv --cache-dir .uv-cache venv tmp/clean-env --python .venv/Scripts/python.exe` và `uv --cache-dir .uv-cache pip install --offline --python tmp/clean-env/Scripts/python.exe -r requirements.txt`: tạo môi trường mới, cài đủ 120 gói từ cache. `uv ... pip check --python tmp/clean-env/Scripts/python.exe`: tất cả tương thích.
- `tmp/clean-env/Scripts/python.exe -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`: **25/25 qua, 14.673 giây**, log lưu trong run demo. Không fit trong tests; có test chặn Pipeline.fit, khớp lại 360 dự đoán test cho từng model và đối chiếu xác suất với nguyên Pipeline.
- `.venv/Scripts/python.exe -X utf8 tests/check_demo.py`: xuất run `demo_20261117T082316Z_b269f12c`, CSV từng dự đoán, 10 PNG sau xử lý, bảng ghép ảnh và checksum trước/sau khớp. Mẫu Digits đầu mỗi lớp: LR 10/10, KNN 9/10, MLP 9/10 (không phải phép đo test độc lập). **10 MNIST test ngoài Digits: mỗi model 3/10**; chọn ảnh trước suy luận, không chỉnh mô hình hoặc tiền xử lý theo accuracy này.
- `.venv/Scripts/python.exe -m streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false`: server local khởi động; đã thử mẫu Digits và upload thật qua browser. Ảnh MNIST test id=0, nhãn 7, KNN đoán 3 với xác suất 33.3%; giữ ảnh sai làm bằng chứng, không giấu. Screenshot tại `outputs/demo_20261117T082316Z_b269f12c/streamlit_demo.jpg`.
- Kiểm tra nbformat/cú pháp, liên kết Markdown nội bộ, file đã yêu cầu xóa, Git diff --check, checksum artifact: qua. Đã xem trực tiếp learning curves, MLP history, confusion matrix/ảnh sai KNN và giao diện.

### Lỗi đã sửa và giới hạn còn lại

- Lỗi cú pháp ngoặc trong test mới đã sửa trước chạy kiểm thử. Loader ban đầu dùng Pipeline.n_features_in_ bị lỗi với bước đầu passthrough ở sklearn 1.7; đã lấy metadata từ classifier khi cần, sửa feature_names fallback. Không đụng trọng số hoặc fit lại.
- Sandbox chặn socketpair khiến AppTest ban đầu kẹt; đã dừng và chạy test với localhost được phép. Import Streamlit ngoài runtime/AppTest có cảnh báo bare mode/ScriptRunContext; tests vẫn qua, không che lỗi. Kernel Jupyter có cảnh báo TCP lúc khởi động; notebook không stderr.
- Chưa có ảnh chụp của nhóm, chưa chứng minh chất lượng trên camera/nền phức tạp/nhiều ký tự. 10 MNIST chỉ là minh họa nhỏ; 3/10 không phải accuracy tổng quát. Xác suất chưa calibration, không bảo đảm đúng.
- Môi trường sạch được cài và test trên cùng máy Windows/Python 3.12.14, chưa thử máy khác. Dàn ý Markdown không phải báo cáo DOCX/PDF hoặc slide PPTX đã nộp. ready_to_submit vẫn false vì nội dung chính và phân công thuộc nhóm.

### Việc nhóm cần làm tiếp

1. Dùng app và bộ model cố định, không cần Run All notebook để demo. Nếu thiếu file thì khôi phục đúng registry/model, không train tự động.
2. Tự viết 6 nhận định EDA, nhật ký xử lý, phân tích kết quả/lỗi/curves/giới hạn, hoàn thành báo cáo 10 mục và slide 10–12 trang theo dàn ý. Đọc bảng/hình đúng run_id.
3. Bổ sung ảnh tự chụp có nhãn/nguồn thực tế nếu muốn đánh giá camera; ghi cả dự đoán sai. Không chọn/tuning lại model vì ảnh demo/test đã xem.
4. Điền phân công thật, tập 30 câu hỏi, giải thích và thay đổi được code. Chưa có thông tin để ghi tên hoặc đóng góp của thành viên.
5. Trạng thái Git trước đồng bộ Phase 2: main theo dõi origin/main, có các file sửa/thêm/xóa liệt kê trong cụm này; giữ nguyên 3 run support cũ và PDF. Tiếp tục commit/push theo yêu cầu đồng bộ trước đó, không force-push; xác minh HEAD remote sau push.
