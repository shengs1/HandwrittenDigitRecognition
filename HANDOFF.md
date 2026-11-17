# Chuyển giao Codex / Antigravity

## Phase hiện tại

Hỗ trợ khung notebook và quy trình thực nghiệm; chưa phải đồ án hoàn chỉnh. Không Streamlit.

## Trạng thái mới nhất đã xác minh

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
