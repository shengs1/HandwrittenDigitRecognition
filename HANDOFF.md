# Chuyển giao Codex / Antigravity

## UI FROZEN — phiên bản chính thức đã được duyệt (2026-11-18)

**Trạng thái: UI FROZEN.** Người dùng chốt giao diện hiện tại; dừng chỉnh thiết kế/màu/typography/bố cục và thêm tính năng. Lượt này không phát hiện lỗi chức năng cần sửa, không đổi app.py, .streamlit/config.toml, tests/test_demo.py hoặc requirements.txt. Chỉ bổ sung trạng thái trong README/AGENTS/HANDOFF và bằng chứng kiểm thử cuối; giữ toàn bộ thay đổi UI đã duyệt từ các lượt trước để đưa vào Git.

**Kiểm thử thật:** toàn bộ43/43 unittest PASS,9,618s. Kiểm tra AppTest bổ sung9/9 tổ hợp KNN/MLP/LR × ảnh test/mẫu/upload; nhãn dự đoán và xác suất khớp Pipeline thật, đủ10 lớp. Có15 tình huống xóa kết quả cũ khi đổi model/nguồn/chữ số/ID/nội dung ảnh upload, gồm thay bytes rồi khôi phục ảnh với cả3 model. Các test bổ sung chặn Pipeline.fit; không fit/tuning hoặc chạy notebook.

**Trình duyệt thật:** resetCtrl+0; kiểm đủ9/9 tổ hợp, dự đoán và10 xác suất hiển thị khớp suy luận Pipeline (so cả phần làm tròn). 15/15 lần bấm phần chữ/khoảng giữa/mũi tên trên5 dropdown đều mở. ArrowDown mở, Escape giữ lựa chọn, Tab chuyển sang nguồn; chọn bằng Enter được dùng suốt ma trận. Kiểm cả3 bảng cấu hình: không ô/dòng bị cắt, không chồng nhóm/tràn ngang, min-height auto/overflow visible, cuộn tự nhiên khi mở. Cả10 trạng thái empty/prediction ở5 actual viewport1920×1080,1920×900,1536×864,1366×768,1280×720 có tràn dọc/ngang0px khi đóng technical; scale1/dpr≈1. Có12 screenshot viewport (không full-page).

**Nguồn ảnh và giới hạn kiểm tra:** ảnh test ID10 và mẫu ID0 đều dự đoán0 trên3 model. Upload fixture MNIST7: LR→7(91,26%), KNN→3(33,33%, đồng hạng3/5/8), MLP→7(94,19%); giữ nguyên kết quả thật. File hỏng hiện thông báo, khóa nút và không giữ prediction cũ. Upload qua harness tạm giữ native widget/call app.main nhưng mock bytes trả về, và AppTest; **không thử lại hộp chọn file Windows** trong lượt này. Không tuyên bố đã kiểm thao tác chọn file OS. Kết quả thí nghiệm cũ10 MNIST vẫn3/10 mỗi model, không thay bằng kết quả một fixture.

**Checksum:**3 Pipeline khớp SHA256 trong registry;94 file bảo vệ (notebook, model/registry, artifact canonical, fixture, kết quả ảnh ngoài, tài liệu nguồn số liệu) giữ nguyên SHA256 và không có diff so HEAD. SHA256 của4 file app/theme/tests/requirements khớp snapshot đầu lượt, xác nhận giữ nguyên UI được duyệt. Không sửa thuật toán ảnh, dataset, metadata hoặc kết quả; không thêm dependency. Syntax/diff-check và HTTP health app/harness đều200.

**Bằng chứng mới:** `outputs/freeze_20261118T154422Z_32ced9af/`: FREEZE_REVIEW.md, unittest.log, functional_matrix.json/log, browser_matrix.json, browser_stale_checks.json, dropdown/keyboard/technical/layout/error JSON, verification.json/log, checksum trước/sau, frozen_source.json, git_before.txt và12 JPEG. Scripts kiểm thêm ở tmp bị ignore. README đã có trạng thái mới; lệnh tạo môi trường/chạy demo hiện tại vẫn đúng. Không tạo lại file nhật ký công cụ đã được yêu cầu xóa.

**Lệnh đã chạy:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v`; `.venv/Scripts/python.exe -X utf8 tmp/check_frozen_demo.py`; `.venv/Scripts/python.exe -X utf8 tmp/verify_freeze.py`; `python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8512 --server.headless true --browser.gatherUsageStats false`; harness tạm cổng8513; `git fetch origin main`; `git diff --check`. Kiểm HTTP cần quyền socket loopback của môi trường; lần gọi bị sandbox chặn đã chạy lại có quyền và đạt, không sửa app.

Đã dừng hai server thử8512/8513, đóng các tab kiểm tra và reset viewport; không để harness thay luồng ứng dụng. Kiểm tra chốt liên kết nội bộ và git diff --check đều qua.

Kiểm tra chốt kích thước screenshot phát hiện lượt đo responsive đầu áp viewport lên tab upload đang active, còn tab app vẫn1366×768. Đã giữ bản đầu riêng layout_initial_diagnostic.json, mở lại duy nhất app cổng8514 và đo lại với assertion actual viewport phải khớp từng kích thước yêu cầu. Bảng layout_checks.json cuối đúng5 viewport,10 trạng thái, tràn0px; screenshot1366×768 và1920×900 có kích thước pixel đúng. Không sửa giao diện để xử lý lỗi thao tác công cụ này.

Server đo lại8514 cũng đã dừng; viewport trả mặc định. HTTP health8514 đạt200 trước khi dừng; ghi cùng các health check trước trong verification.json.

**Lỗi còn tồn tại/việc nhóm cần làm:** không phát hiện lỗi chức năng trong phạm vi đã kiểm. Ảnh ngoài Digits vẫn có giới hạn đã ghi; hộp chọn file OS chưa thử lại. Nhóm hoàn thiện/xác nhận báo cáo, slide, thông tin và phân công thật, tập bảo vệ; không tiếp tục chỉnh UI đã chốt. Phần kiểm UI không thay việc hoàn thiện tài liệu nộp.

**Git:** đầu lượt main...origin/main tại45ce4b8 với5 file UI/tài liệu đã sửa, .streamlit và4 thư mục bằng chứng UI chưa commit. Fetch xác nhận không lệch remote. Người dùng đã yêu cầu commit và push bản UI này sau kiểm thử; tất cả kiểm tra đã đạt. Kết quả commit/push được ghi ở mục xác nhận ngay dưới khi hoàn tất. Các phần sau là lịch sử trước đóng băng.

**Xác nhận commit/push UI FROZEN:** đã commit toàn bộ UI đã duyệt và bằng chứng bằng `36148add08ef5f05f6491dd614553978b604c750` (`Freeze approved demo UI and record final verification`), chạy `git push origin main` thành công. `git ls-remote origin refs/heads/main` xác nhận đúng SHA36148ad trên GitHub; `git status --short --branch` sạch và đồng bộ tại thời điểm kiểm tra. Commit tài liệu tiếp theo chỉ ghi nhận kết quả push này, không thay code/UI/model hoặc kết quả test. Không force-push. Phiên bản mới nhất xem `git log -1`; giữ UI FROZEN cho các lượt tiếp theo.

## Trạng thái hiện tại — Final UI Interaction & Technical Information Fix (2026-11-18)

Đã sửa đúng phạm vi giao diện, giữ bản compact/dark hiện tại. Nguyên nhân chồng chữ được đo trên DOM trước sửa: caption có margin-bottom=-14px; dòng chữ cao19,6px nhưng wrapper chỉ5,6px, code block bắt đầu trước đáy chữ6px. Đã reset margin caption trong phạm vi demo; thay repr/code block bằng HTML ngữ nghĩa có chiều cao tự nhiên, line-height và khoảng cách rõ, tự xuống dòng. Không fixed/min-height vùng văn bản. Khi mở expander, trang cuộn tự nhiên; khi đóng không tăng chiều cao chính.

Thông tin kỹ thuật gồm4 nhóm: dữ liệu đọc metadata run chính thức; bảng cấu hình đọc trực tiếp estimator.get_params/scaler của Pipeline đã lưu; quy trình ảnh đúng EXIF/alpha/grayscale/nền/crop/giữ tỷ lệ/căn giữa/8×8/0–16/vector theo hàng; giới hạn ngắn theo yêu cầu. Digits giữ nguyên pixel; chuẩn hóa chỉ trong Pipeline. Đổi KNN/MLP/LR cập nhật đúng bảng. Không hiển thị run ID/checksum hoặc đoạn kết quả MNIST dài trên giao diện; toàn bộ thông tin và kết quả3/10 mỗi mô hình vẫn giữ trong notebook/README/tài liệu/artifact, xác minh94 SHA256 không đổi.

Dropdown: DOM cho thấy input đã phủ phần thanh; bấm khoảng giữa mô hình trước sửa vẫn mở được. Xung đột thực tế là CSS button chung min-height40px làm nút mũi tên vượt field35px. Đã scope lại nút native listbox (min-height0, tự giãn theo field), input flex/min-width/cursor. Sau sửa nút33,4px nằm trong field35px. Không JS chặn sự kiện, overlay hoặc custom dropdown. Trình duyệt thật kiểm15/15 lần bấm: phần chữ/khoảng giữa/mũi tên của mô hình, nguồn, chữ số, ID và màu nền. ArrowDown mở, Escape đóng/giữ lựa chọn, Enter chọn, Tab sang nguồn ảnh hoạt động.

**Kiểm thử:** 43/43 unittest PASS,6,843s; giữ40 test cũ và thêm3 test kiểm tra thông số thật, đọc tham số động không fit/không đổi artifact, bảng đổi theo3 model. Lần đầu test mới lọc nhầm cả style HTML chứa tên class nên thất bại; sửa bộ lọc nhận đúng div nội dung, giữ assertion so toàn bộ HTML. Lần đầu còn lỗi socket WinError10055 của môi trường AppTest; chạy lại có quyền loopback thì cả43 qua. Log đầu/cuối được giữ. Không sửa test cũ để bỏ điều kiện, không fit/tuning/chạy notebook.

**Trình duyệt:** zoom100% (scale1, dpr≈1, CSS zoom1/transform none), actual viewport1920×1080,1920×900,1536×864,1366×768,1280×720; cả10 trạng thái test empty/prediction có document/stMain scrollHeight đúng chiều cao viewport, tràn dọc/ngang0px. Đóng lại expander MLP ở1366×768 vẫn0px. Thêm upload prediction tổng12 phép đo đóng không tràn. Sáu phép kiểm technical gồm cả3 model,1920×900 và390×844: không ô/dòng chữ bị cắt hoặc tràn ngang, nhóm cách nhau≥18px, overflow visible/min-height auto; nội dung dài cuộn tự nhiên. Screenshot viewport thực, không full-page; ảnh mobile do công cụ trả390×843 dù innerHeight844, ghi rõ trong verification.

Đã dự đoán test KNN id10/nhãn0→0,100%; đổi chữ số1/ID21 hợp lệ rồi dự đoán→1; đổi model xóa kết quả cũ. Mẫu toàn bộ Digits id7/nhãn7→7,100%. Upload fixture MNIST7 có cả ảnh gốc và8×8, dự đoán3,33,33% (đồng hạng3/5/8); file hỏng hiện lỗi, khóa nút và không giữ kết quả cũ. **Giới hạn kiểm thử upload:** harness tạm mock giá trị trả về của uploader native, gọi đúng app.main/preprocessing/Pipeline; không thử lại hộp chọn file Windows trong lượt này do độ trễ công cụ đã ghi trước. Tests vẫn kiểm upload thực qua bytes, ảnh trống/hỏng/nền.

**File lượt này:** app.py, tests/test_demo.py, AGENTS.md, README.md, HANDOFF.md; bằng chứng mới `outputs/interaction_20261118T122825Z_df6a5b22/` có INTERACTION_REVIEW.md,16 screenshot, JSON DOM/dropdown/layout/bảng cấu hình, checksum và log tests. Script tạm tmp/verify_interaction.py và harness bị ignore, không thuộc luồng ứng dụng. Tám hàm registry/load/preprocess/predict/data/split/preview/prediction HTML giữ nguyên AST đầu lượt. Notebook,94 file bảo vệ, model/registry, fixture, tài liệu số liệu và requirements không đổi; không thêm dependency.

**Lệnh thực tế:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v`; `.venv/Scripts/python.exe -X utf8 tmp/verify_interaction.py`; `.venv/Scripts/python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8510 --server.headless true --browser.gatherUsageStats false`; harness tương tự cổng8511. Syntax, bảng trình duyệt so Pipeline thật,94 checksum và git diff --check qua. Server thử đã dừng và viewport đã reset.

**Lỗi/việc còn lại:** không còn lỗi đã xác định trong các trạng thái đã kiểm tra. Chưa thử lại hộp chọn file OS; nâng phiên bản Streamlit cần kiểm CSS/native DOM. Nhóm xem screenshot, xác nhận báo cáo/slide và chuẩn bị bảo vệ như lịch sử bên dưới. Không tuyên bố tài liệu nộp của nhóm đã hoàn tất.

**Git:** main...origin/main tại45ce4b8; đầu lượt đã có thay đổi UI chưa commit trong5 file và .streamlit cùng3 thư mục evidence UI. Giữ toàn bộ; thêm evidence interaction, không commit/push hoặc sửa lịch sử trong lượt này. Các phần sau là lịch sử.

## Trạng thái hiện tại — Final Responsive Layout Fix (2026-11-18)

Đã sửa bố cục để dùng ở browser zoom100%, giữ dark mode/màu sắc/typography. Khung max-width1280px, padding20px; giảm gap và khoảng trống theo chiều cao viewport. Chuyển chữ số/ID vào cột ảnh, thay slider dài bằng selectbox, giữ đúng danh sách ID và key theo nguồn/lớp. Model/nguồn vẫn nằm cùng hàng trên. Ảnh Digits200px ở viewport thấp,212px ở màn hình cao; nearest-neighbor không đổi. Empty state280–320px; bố cục dự đoán không làm giao diện vượt viewport. Upload có hai preview nhỏ hơn phù hợp chiều cao.

Nguyên nhân kỹ thuật đã xác định: hàng slider toàn chiều rộng tốn chỗ; min-height empty quá lớn; margin-bottom âm14px của Streamlit Markdown làm wrapper HTML tính thiếu chiều cao và có thể chồng chữ. Đã đặt margin-bottom=0 trong phạm vi demo, sau đó tính lại luồng bố cục thật. Không dùng CSS zoom/transform scale hoặc overflow hidden để giấu nội dung. CSS overflow có sẵn trong thanh xác suất chỉ để vẽ track, không áp lên khung ứng dụng.

**Kiểm tra trình duyệt thật:** resetCtrl+0; đo trực tiếp window.innerWidth/innerHeight, visualViewport.scale=1, devicePixelRatio≈1, CSS zoom1/transform none. Kiểm cả document.scrollingElement và vùng stMain của Streamlit; không suy ra vừa màn hình từ full-page screenshot. Tất cả ảnh dùng fullPage=false. Có45 phép đo tại5 viewport,40 trạng thái đóng technical đều tràn dọc0px và không tràn ngang;5 trạng thái mở technical cuộn tự nhiên, đóng lại trở về0px.

| Viewport thực tế | document scrollHeight lớn nhất khi đóng | stMain scrollHeight lớn nhất khi đóng | Tràn dọc/ngang |
|---|---:|---:|---|
|1920×1080|1080|1080|0px / Không|
|1920×900|900|900|0px / Không|
|1536×864|864|864|0px / Không|
|1366×768|768|768|0px / Không|
|1280×720|720|720|0px / Không|

Mỗi viewport đã thử empty, dự đoán test, đổi MLP/xóa kết quả cũ, đổi chữ số1 và ID21 hợp lệ/xóa kết quả cũ, dự đoán mới, mở/đóng technical, upload preview và upload prediction. Dự đoán test đối chiếu CSV canonical khớp. Nhánh upload kiểm bằng harness tạm cung cấp fixture qua mock return của uploader, vẫn render widget native và gọi chính app.main/preprocessing/Pipeline; không thử lại hộp chọn file OS vì độ trễ công cụ đã ghi nhận ở lượt trước. Harness được reload module app trước các lần đo cuối để tránh CSS cũ trong cache; không sửa ứng dụng để chạy fixture. Các lần đo chẩn đoán tràn nhỏ trước sửa giữ riêng ở layout_diagnostics.json.

**Bảo toàn và test:** toàn bộ40 unittest PASS,14,551s. Test chỉ đổi truy cập slider sang selectbox và thao tác select; giữ assertion đầy đủ option từng lớp đúng saved test indices và cả3 Pipeline, không bỏ/giảm test. Chín hàm ngoài main khớp AST với snapshot đầu lượt, gồm registry/load/preprocess/predict/data/split/summary/preview/prediction HTML. Notebook cùng60 artifact/model/registry chính thức giữ nguyên61 SHA256; không fit, tuning hoặc chạy notebook. Không dependency mới.

**File chỉnh lượt này:** app.py, tests/test_demo.py, HANDOFF.md, AGENTS.md, README.md. Bằng chứng mới: `outputs/responsive_20261118T035501Z_c6f49df4/` có browser_matrix.json(45 dòng), layout_diagnostics.json, verification.json, tests_initial.log/tests_final.log, protected_before/after.json, LAYOUT_REVIEW.md và40 screenshot viewport. Giữ nguyên mọi thay đổi UI chưa commit từ các lượt trước, không ghi đè nội dung khác. Script fixture chỉ ở tmp bị ignore.

**Lệnh thực tế:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v`; `python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8507 --server.headless true --browser.gatherUsageStats false`; tương tự cho harness tạm cổng8508. Syntax/diff-check được kiểm tra; kết quả chi tiết trong verification.json. Khi technical mở, stMain cao1079–1135px tùy viewport là cuộn hợp lệ, không giấu nội dung. Màn hình nhỏ hơn các viewport kiểm tra vẫn cuộn tự nhiên. Widget upload native còn vài nhãn tiếng Anh như trước.

Kiểm tra chốt: syntax, link tài liệu nội bộ, diff-check và61 checksum kiểm lại đều qua. Đã dừng server thử8507/8508 và reset viewport; không để harness thay luồng chạy chính.

**Git:** tiếp tục trên45ce4b8 với các thay đổi local có sẵn; không commit/push trong lượt này. Việc tiếp: xem screenshot đặc biệt1366×768 và1920×900 ở empty/prediction, hoặc chạy app bình thường với zoom100%; nhóm tiếp tục hoàn thiện báo cáo/slide. Các trạng thái bên dưới là lịch sử.

## Trạng thái hiện tại — Final UI Polish (2026-11-18)

Đã tinh chỉnh vừa đủ trên bản UI Redesign đang có, không thiết kế lại: tiêu đề chính 25px ở viewport thấp/26px desktop lớn; tiêu đề khu vực 17px/weight600; số liệu thẻ20px; số dự đoán80/88px. Tăng tương phản chữ phụ, khoảng cách giữa thống kê và cấu hình; ảnh Digits224/232px, vẫn nearest-neighbor. Chọn chữ số/ID cùng hàng theo tỷ lệ1:4, giữ nguyên toàn bộ option/key/split. Phân biệt rõ “Accuracy test” ở tổng quan với “Xác suất ảnh này” ở kết quả; có nhãn “Đúng/Sai · nhãn gốc”. Giữ dark mode, màu sắc, hai cột và các thanh xác suất hiện có.

Sửa selector `.section-heading span` thành `.section-heading > span`: selector cũ áp luôn font chữ phụ vào span mà Streamlit chèn trong h2, khiến chữ tiêu đề thực tế nhỏ hơn cấu hình. Đã kiểm computed style trên chính span chứa chữ:17px/600. Empty state cao369px ở1366×768, vùng kết quả thực368,35px, chênh dưới1px nên hai trạng thái gần như giữ nguyên vị trí nội dung dưới. Radius12px và padding/thang chữ được thống nhất trong các card hiện có.

**File chỉnh lượt này:** `app.py`, `HANDOFF.md`; thêm bằng chứng `outputs/ui_polish_20261118T033513Z_4b692dfe/`. `.streamlit/config.toml`, requirements, tests và notebook không sửa thêm. Có script kiểm tra tạm `tmp/ui_polish_fixture.py`, không phải chức năng sản phẩm, bị Git ignore. Giữ nguyên các thay đổi UI Redesign chưa commit từ lượt trước; không ghi đè hoặc loại bỏ chúng.

**Kiểm thử:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v` →40/40 PASS,18,004s; syntax qua. Notebook và60 file artifact/model/registry chính thức (tổng61 file) giữ nguyên SHA256. Tám hàm ngoài phần trình bày/main khớp AST với snapshot đầu lượt, gồm preprocessing, suy luận, đọc dữ liệu/split/registry, summary và preview. Không fit, tuning hoặc chạy notebook; không tạo số liệu/dự đoán giả.

**Trình duyệt thật:** app chính cổng8505 được kiểm tại1366×768 và1920×1080, có screenshot empty/prediction. Không tràn ngang; ảnh, nút và card kết quả chính nằm trong viewport. KNN id10→0,100%; id1790 nhãn8→1,66,67%, xác nhận trực tiếp cả nhãn đúng/sai. Các dự đoán dùng nguyên Pipeline. Footer/expander kỹ thuật ở viewport768px có thể cần cuộn ngắn.

**Giới hạn phép thử upload:** dùng trang kiểm thử tạm cổng8506 nhập đúng `app.main`, vẫn vẽ widget file native nhưng thay giá trị trả về bằng bytes fixture qua mock. Đây là kiểm tra trực quan nhánh upload/lỗi với dữ liệu kiểm thử, **không phải thử lại hộp chọn file OS** trong lượt này. Tránh lặp lại độ trễ công cụ setFiles54 phút của lượt trước. Fixture MNIST7 hiển thị gốc/8×8, Pipeline vẫn dự đoán3 với33,33%; file không hợp lệ hiện lỗi và khóa nút, không có kết quả cũ. Chức năng upload/ảnh trống/file hỏng tiếp tục được toàn bộ unittest kiểm tra. Không đưa harness vào app hoặc bản nộp.

**Bằng chứng:** `tests.log`, `protected_before/after.json`, `browser_checks.json`, `polish_checks.json`, `screenshots.md` và8 JPEG. Tên screenshot thể hiện viewport kiểm tra; kích thước JPEG thực được ghi trong polish_checks vì công cụ có thể giới hạn/thu ảnh màn hình lớn. Không dùng ảnh screenshot để suy ra cỡ font; lấy computed style của DOM. Thư viện và thuật toán ảnh không thay đổi; các hạn chế ảnh ngoài và vài nhãn tiếng Anh của widget native vẫn như cũ.

Kiểm tra cuối: `git diff --check` qua, syntax và61 checksum kiểm lại vẫn khớp; đã dừng hai server thử8505/8506, trả viewport mặc định. Không để harness/server thử thay luồng chạy chính.

**Git:** đầu lượt đã có thay đổi local của UI Redesign trên `45ce4b8`; giữ nguyên các thay đổi đó. Lượt polish không commit/push. Việc tiếp theo: xem screenshot hoặc chạy app; nhóm tiếp tục báo cáo/slide theo lịch sử bên dưới. Các mục sau mô tả những lượt trước.

## Trạng thái hiện tại — UI Redesign (2026-11-18)

Đã thiết kế lại giao diện theo ảnh tham chiếu: dark mode, màu nhấn xanh, khung giữa giới hạn 1.200 px, header/trạng thái, 3 thẻ tổng quan đọc từ artifact, cấu hình gọn và hai cột ảnh/kết quả. Mặc định ảnh test đúng split. Mẫu Digits chỉ có một preview phóng to nearest-neighbor; upload giữ ảnh gốc và ảnh 8×8 cạnh nhau. Nút “Nhận diện chữ số” dưới ảnh; kết quả có chữ số lớn, model, xác suất, đúng/sai khi có nhãn và 10 thanh ngang. Các giải thích dài chuyển vào expander; cảnh báo xác suất/giới hạn vẫn được giữ.

Kết quả lưu trong session state, gắn với model/checksum/nguồn/ID/nền/nội dung ảnh. Đổi model, ảnh, nguồn, chế độ nền hoặc xóa upload thì xóa kết quả cũ. Overview lấy từ data_summary, selection_lock và model_comparison của registry, không hardcode điểm/nhãn/xác suất. Không thêm dependency, framework hoặc thay kiến trúc notebook + app.

**File sửa/tạo:** `app.py`, `.streamlit/config.toml`, `tests/test_demo.py`, `README.md`, `AGENTS.md`, `HANDOFF.md`; bằng chứng ở `outputs/ui_20261118T015852Z_1c47689a/`. Notebook và requirements không sửa. Sáu hàm đọc registry/tải Pipeline/tiền xử lý/predict/đọc Digits/đọc split khớp AST với HEAD. SHA256 của 61 file (notebook cùng toàn bộ 60 artifact/model/registry chính thức) trước/sau khớp.

**Kiểm thử thực tế:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v` → **40/40 PASS, 5,885 s**. Giữ toàn bộ kiểm tra chức năng cũ; đổi truy cập widget nguồn từ radio sang selectbox, đổi kiểm tra st.metric thành kiểm tra dữ liệu thật và HTML kết quả/10 lớp. Thêm 3 test về empty state/overview/một preview, xóa kết quả khi đổi lựa chọn và khi đổi nền/xóa upload. Lần đầu có 3 lỗi ở test mới do gọi thuộc tính filtered_state không thuộc API AppTest hiện tại; đã sửa sang kiểm tra key qua mapping session_state rồi chạy lại cả 40 test. Không bỏ hoặc làm yếu kiểm tra chức năng.

`python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8504 --server.headless true --browser.gatherUsageStats false` chạy thành công, HTTP200. Đã thao tác bằng trình duyệt thật tại **1366×768, 1920×1080, 390×844**, kiểm tra và chụp empty/test/upload/preview/kết quả. Không tràn ngang; ảnh, nút và card kết quả nằm trong viewport desktop. Hai cột bắt đầu cùng độ cao; màn hình nhỏ xếp dọc, có cuộn. KNN test id43 nhãn7 →7, xác suất100%; upload MNIST nhãn7 →3, xác suất33,33% (đồng hạng3/5/8) đúng như suy luận trước, không sửa model để làm đẹp demo.

**Bằng chứng:** `tests_initial.log`, `tests_final.log`, `ui_checks.json`, `browser_layout_checks.json`, `protected_before.json`, `protected_after.json` và 8 JPEG. So với ảnh tham chiếu: giữ cấu trúc header/overview/cấu hình/hai cột/kết quả xanh/thanh ngang; dùng dữ liệu và xác suất thật thay số minh họa. Công cụ filechooser setFiles mất khoảng54 phút dù có timeout; sau cùng upload thành công. Đây là độ trễ công cụ kiểm tra, không đưa vào số đo thời gian suy luận của app.

**Giới hạn:** màn hình nhỏ cần cuộn dọc; nút Upload và nhắc dung lượng do Streamlit native tạo vẫn có tiếng Anh. CSS dùng class riêng, key container có tài liệu và một số data-testid; nâng Streamlit cần kiểm tra lại hình thức. Không còn lỗi giao diện được xác định trong các trạng thái đã kiểm tra. Hạn chế ảnh ngoài Digits, nhóm chưa xác nhận dự thảo/báo cáo/slide vẫn giữ như trước.

Kiểm tra chốt: syntax app/tests, link nội bộ README/HANDOFF/AGENTS và 61 checksum đều qua; `git diff --check` không lỗi. Đã dừng server thử cổng8504 sau khi kiểm tra, trả viewport trình duyệt về mặc định. Không huấn luyện lại hoặc chạy notebook.

**Git:** đầu lượt sạch ở `45ce4b8`, `main...origin/main`. Các thay đổi UI hiện còn local, chưa commit/push trong lượt thiết kế này. Không thay artifact chính thức hoặc lịch sử Git. Công việc tiếp: nhóm xem ảnh/giao diện mới, tiếp tục hoàn thiện tài liệu nộp theo mục bên dưới. Các mục tiếp theo là lịch sử trước UI Redesign.

## Git — đã push Final Completion (2026-11-17)

Người dùng đã yêu cầu push phần code mới; cho phép commit và push toàn bộ thay đổi Final Completion cùng tài liệu/bằng chứng liên quan lên `origin/main`. Đã fetch remote, kiểm tra diff và xác minh lại mã đã test cùng 60 artifact chính thức khớp checksum. Snapshot “chưa commit/push” bên dưới mô tả lượt hoàn thiện trước yêu cầu mới này.

Đã commit 22 file bằng `3a2c850` (`Complete notebook drafts and add saved test split demo`) và chạy `git push origin main` thành công. `git ls-remote origin refs/heads/main` xác nhận SHA `3a2c85041c091a898a7d15a30759bdeb63364869` trên GitHub; working tree sạch tại thời điểm kiểm tra. Commit tài liệu tiếp theo chỉ ghi nhận kết quả push này. Không chạy lại test vì code khớp bản đã qua 37/37 test; không đổi mô hình hoặc kết quả thực nghiệm. Không force-push.

## Trạng thái hiện tại — Final Completion (2026-11-17)

**Kỹ thuật đã kiểm chứng; chưa xác nhận sẵn sàng nộp.** Run `20261117T081201Z_fd32180f`, 60 file model/registry/toàn outputs giữ nguyên SHA256; không retrain/tuning.23 mã cell notebook, output nhúng và hàm preprocessing không đổi. Notebook đã có 15 markdown cells được hoàn thiện, không TODO nhận định; mọi diễn giải ghi là **dự thảo chưa nhóm xác nhận**. Báo cáo 10 mục và 12 slide có nội dung Markdown, chưa PDF/DOCX/PPTX nộp.

**Demo:** thêm “Ảnh test Digits” đọc đúng 360 id từ split run trong registry; giữ pixel gốc. Không chia lại hoặc fit. Thiếu/sai split báo lỗi. Kiểm thử ảnh tương đương trên 10 train (đảo nền, RGB/RGBA, dịch vị trí), EXIF, ảnh trống/tỷ lệ/centering đều qua; chưa thấy lỗi khách quan nên giữ preprocessing. Không dùng10 MNIST đã xem để tối ưu. Browser: KNN test id 10→ 0 đúng, proba1; upload MNIST 7→ 3 sai, proba1/3 đồng hạng3/5/8. Giới hạn ảnh ngoài được giữ nguyên/trình bày trung thực.

**Kiểm thử mới:**37/37 PASS trên project(6,163s) và source checkout sạch có dấu cách, ban đầu không tmp(4,807s). Checkout mới lấy HEAD `909f53d`+diff hiện tại; dùng lại venv sạch Python 3.12.14 từ review trước, toàn pin requirements khớp, không cài lại lần này. nbformat/syntax hợp lệ, 23 cell đã có output, 15 PNG, 0 errors; không Run All thêm vì code không đổi và đã có rerun độc lập thành công trước. Streamlit127.0.0.1: 8503 HTTP 200 và thao tác sample/upload thật đã kiểm tra; hộp filechooser công cụ phản hồi chậm, Upload button thành công. Cảnh báo bare AppTest ScriptRunContext không là lỗi app.

**File sửa:** app.py; tests/test_demo.py; digit_classification.ipynb(chỉ Markdown); README; AGENTS; HANDOFF; docs/REPORT_OUTLINE, SLIDE_OUTLINE, RESULTS_INDEX, VIVA_QUESTIONS, FINAL_REVIEW, FINAL_AUDIT, REQUIREMENTS_MAP. Bằng chứng mới ở `outputs/completion_20261117T100609Z_b8981ac1/`: protected_before/after, completion_checks, derived_train_statistics, clean_checkout_tests, clean_environment, streamlit_check, ảnh giao diện/ảnh kiểm tra. Script phụ/checkouts nằm tmp bị ignore, không thêm module/framework/dependency.

**Lệnh thực tế:** `.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v`→ 37PASS; cùng lệnh với venv sạch/cwd checkout→ 37PASS; script tạm kiểm nbformat/compile/link/hash/pin→ PASS; `python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8503 --server.headless true --browser.gatherUsageStats false`→ server chạy/HTTP 200; CUA thao tác test/upload→ kết quả trên. Không chạy lại notebook/train, không thay official model hoặc số liệu.

**Còn cần nhóm:** đọc/sửa/xác nhận nhận định dự thảo và nhật ký giữ 3 IQR; điền tên/MSSV/lớp/giảng viên/phân công thật, xuất/kiểm trang báo cáoPDF/DOCX và slidePPTX/PDF, tập vấn đáp từng thành viên, thử ảnh tự chụp nếu muốn nêu khả năng thực tế (không dùng để tuning canonical). Chưa có BM06/ảnh tự chụp/xác nhận đăng ký, không suy đoán. Chưa ZIP; danh mục bản nộp ở README. Xem bảng PASS/PARTIAL đầu FINAL_REVIEW.

**Git:** bắt đầu clean `main...origin/main`, HEAD909f53d. Thay đổi lượt này còn local, **không commit/push** theo yêu cầu hiện tại; không đổi lịch sử. Các nội dung bên dưới là lịch sử, không phải trạng thái mới nhất.

Kiểm tra chốt lượt Final Completion: `git diff --check` qua; link Markdown nội bộ không hỏng; báo cáo có 10 mục, slide có 12 mục; các giá trị chính trong dự thảo khớp nguồn. Mã app/tests/notebook/requirements khớp bản đã test trên checkout sạch (bỏ khác biệt CRLF/LF ở hai file không sửa). Output nhúng notebook và execution_count khớp HEAD; kiểm lại 60 checksum đều giữ nguyên. Server thử cổng 8503 đã dừng sau kiểm tra; repo còn 13 file sửa và thư mục bằng chứng mới, chưa commit/push.

## Lịch sử các phase và review trước

## Snapshot phase review trước

Final review trước bảo vệ: rà soát theo PDF, kiểm chứng tái lập, sửa lỗi kỹ thuật và lập bảng PASS/FAIL/PARTIAL. Đã chạy lại notebook trên bản checkout riêng theo yêu cầu review, không chọn tham số mới hoặc thay bộ mô hình đang xác nhận. Nhóm còn hoàn thiện nội dung nộp.

## Snapshot trạng thái review trước

**Phạm vi cập nhật:** theo yêu cầu mới nhất, bỏ đánh giá mục 6 của PDF khỏi checklist và việc cần làm. Không thay PDF, code hoặc kết quả. Các kiểm tra kỹ thuật notebook vẫn giữ; bản tổng hợp Final Audit theo A–I nằm tại `docs/FINAL_AUDIT.md`. Những phần thực sự còn thiếu là nhận định/phân tích được nhóm xác nhận, báo cáo/slide chính thức và phân công/vấn đáp.

**Final review (2026-11-17):** 31/31 tests qua trên checkout sạch có dấu cách và venv mới từ requirements; notebook chạy đủ 23 code cells/15 hình, 0 lỗi/0 stderr trong cell. Metric chênh lệch=0 và 1.080 dự đoán test khớp bản chính thức; registry/3 model/metric/test prediction/report JSON gốc giữ nguyên checksum. Đã sửa 4 lỗi test do thiếu tmp, định dạng dòng accuracy ở 3 CSV, path hiển thị notebook và phân loại snapshot lịch sử. Không phát hiện Critical trong phạm vi kiểm tra. **Chưa sẵn sàng nộp**: nhận định EDA/phân tích chưa nhóm xác nhận; chưa có báo cáo và slide chính thức. Xem `docs/FINAL_REVIEW.md` và `outputs/review_20261117T090347Z_9df57e69/review_checks.json`.

**Phase 2 thay thế trạng thái khung cũ bên dưới:** run `20261117T081201Z_fd32180f` đã hoàn tất huấn luyện lần đầu, 23 cell chạy qua kernel thật, xuất 3 Pipeline và 55 file kết quả, không stderr trong cell. `models/registry.json` khóa bộ mô hình demo, chọn KNN bằng mean CV macro F1. App hoạt động với ảnh mẫu/upload, xác suất và xử lý lỗi; **25/25 test qua trên môi trường sạch**, đã thử trực tiếp cả hai luồng bằng trình duyệt. Bằng chứng ở `outputs/demo_20261117T082316Z_b269f12c/phase2_status.json`. Nhóm còn tự viết phân tích chính, báo cáo/slide, phân công và bổ sung ảnh tự chụp. Các mục “chưa có mô hình”, “TODO SV-01…09”, “không Streamlit” bên dưới chỉ mô tả lịch sử Phase 1.

**Cập nhật Git (2026-11-17):** đã commit/push bản sửa và báo cáo final review lên https://github.com/shengs1/HandwrittenDigitRecognition, nhánh `main`, commit nội dung review `2852161` đã xác minh trên remote. `main` theo dõi `origin/main`; bản ghi nhận push được lưu trong cập nhật tài liệu tiếp theo. Xem `git log -1` để lấy commit mới nhất. Các ghi nhận Phase 1/2 bên dưới giữ nguyên lịch sử, không thay thế trạng thái final review.

## Snapshot Phase 1 — lịch sử, không phải trạng thái hiện tại

**Ngày 2026-11-17 (Asia/Saigon): phần khung hỗ trợ đã chạy được; thực nghiệm cốt lõi chưa triển khai.** Notebook lúc đó có 51 cell (23 cell mã), chạy bằng kernel thật, 6 hình nhúng, 0 lỗi thực thi, 0 stderr trong cell. Không mô hình nào được huấn luyện ở Phase 1. Các cụm bên dưới giữ lại lịch sử; trạng thái final review ở đầu file thay thế phần này.

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
5. Giữ bộ model/run đã xác nhận và cập nhật HANDOFF khi có công việc mới; không train lại hoặc đổi registry theo điểm demo/test. Repo Phase 2 đã đồng bộ như ghi nhận bên dưới.

### Đồng bộ Git Phase 2

- Remote trước cập nhật ở `dd6c86c`, không có xung đột. Đã stage đúng code/tài liệu/output/model và xóa các file được yêu cầu; môi trường/cache/tmp không được track.
- `git commit -m 'Complete fixed Digits experiments and Streamlit demo'`: commit `0aacb47`, 107 file thay đổi, 168 file trong toàn cây Git, khoảng 6.46 MB dữ liệu trước nén. Đã quét mẫu private key/token trong text, không phát hiện; PDF và model hash được giữ nguyên.
- `git push origin main`: thành công, `dd6c86c..0aacb47`; sau đó kiểm tra remote khớp HEAD. Không force-push hoặc viết lại lịch sử.
- Rà soát diff phát hiện một dòng trống thừa cuối RESULTS_INDEX.md; đã dọn trong cập nhật tài liệu sau push, không ảnh hưởng code/số liệu. Không chạy lại huấn luyện hay unit test cho chỉnh sửa tài liệu này.
- Giới hạn bàn giao còn lại là nội dung phân tích/báo cáo/slide/phân công thật và ảnh tự chụp như nêu trên; không còn TODO code cốt lõi hoặc lỗi thực thi đã biết trong phạm vi đã kiểm thử.

## Cụm 8: final review toàn repository

### Phạm vi và bằng chứng

- Git ban đầu sạch tại `70ad779`. Đã đọc đầy đủ 6 trang PDF, AGENTS/HANDOFF/README, notebook, app, tests, tất cả tài liệu, metadata/registry và bảng/ảnh thực nghiệm. File nhật ký công cụ riêng không còn tồn tại (đã xóa ở Phase 2); không tự tạo lại. BM06, báo cáo/slide chính thức và xác nhận của nhóm/giảng viên chưa có.
- Tạo snapshot từ git archive trong checkout độc lập có dấu cách, không có tmp. Tái hiện `unittest discover`: 25 tests, 4 errors FileNotFoundError do test phụ thuộc thư mục tmp chưa được track. Log giữ trong `outputs/review_20261117T090347Z_9df57e69/baseline_fresh_checkout_tests.log`.
- Tạo venv mới bằng `uv venv`, cài từ requirements qua cache offline (120 package), pip check tương thích. Áp dụng đúng các bản sửa vào checkout rồi chạy test trước khi runner notebook tạo tmp.
- `unittest discover -s tests -p 'test_*.py' -v`: **31/31 PASS**, 7.283 giây. 6 kiểm tra bổ sung xác minh metric/report, confusion pairs/ảnh sai, CV/grid, scaler/test indices/bytes, learning curves/history và path output. Log/environment/review_checks ở thư mục review.
- Chạy `tests/run_notebook.py` bằng venv mới trong snapshot: run `20261117T091140Z_36eda884`, 23 code cells, 15 hình, 0 error/0 stderr trong cell. Bộ registry vẫn trỏ canonical `20261117T081201Z_fd32180f`. Bản notebook đã chạy riêng và log được lưu trong outputs/review; không ghi đè output chính thức bằng timing rerun.
- So sánh rerun: metric max absolute difference=0,3×360 dự đoán test khớp; CV, scaling và learning-curve tổng hợp/từng fold khớp; tham số classifier không đổi. Không điều chỉnh seed, split, preprocessing, grid hoặc estimator để tăng điểm.
- Artifact gốc được bảo vệ bằng SHA256 trước/sau: 3 Pipeline, registry, model_comparison, test_predictions và classification report JSON đều không đổi. Chỉ 3 CSV report được sửa format dòng accuracy, không thay metric hoặc dự đoán. Timing được kiểm độc lập: median 5 lượt predict, fit cuối và bytes khớp bảng.
- Streamlit chạy bằng venv mới từ snapshot tại localhost: 8502, HTTP 200; AppTest qua cả mẫu, upload ảnh thật, ảnh hỏng/trống, thiếu registry/model và kiểm không fit/không scale hai lần. Không sửa app hoặc thêm tính năng. Kiểm tra 15 PNG qua bản ghép QA; ảnh không bị thay dữ liệu.

### Sửa đổi đã thực hiện

- `tests/test_demo.py`: setUpModule tạo tmp cho checkout mới. `tests/test_artifacts.py`: kiểm tra độc lập các artifact khoa học dữ liệu, không fit. `tests/test_contracts.py`: thêm kiểm tra path riêng máy trong output notebook.
- Notebook cell `digits-048`: accuracy là scalar, để precision/recall trống, support đúng số mẫu test; print đường dẫn tương đối. 3 CSV canonical tái xuất từ JSON gốc; output text của notebook bỏ prefix riêng máy. Các cell huấn luyện/tuning không đổi.
- `docs/FINAL_REVIEW.md`: phân loại Critical/Major/Minor, ma trận đối chiếu PDF và 5 câu hỏi có PASS/FAIL/PARTIAL cùng file/bằng chứng. Cập nhật README/REQUIREMENTS_MAP dẫn tới review và HANDOFF tách rõ snapshot lịch sử.
- Đã sửa lỗi tên thuộc tính `run` của test mới bị trùng unittest.TestCase.run trong lúc phát triển test; bản cuối đã qua đủ 31 tests. Đây không phải lỗi sản phẩm ban đầu. Cảnh báo kernel TCP và AppTest bare mode/ScriptRunContext giữ trong log, không bị tính nhầm thành lỗi thực thi.

### Các phần chưa thể xác nhận / nhóm cần hoàn thiện

- Major còn mở: 6 nhận định EDA và phân tích chính/ảnh sai/learning curve chưa có xác nhận trong repo; báo cáo PDF/DOCX và slide nộp chưa có. Không viết thay các phần này.
- Chưa xác nhận nhóm 3–5, đăng ký/≥3 mục tiêu được duyệt, phân công thật và khả năng vấn đáp. Dàn ý 10 mục/12 slide/30 câu hỏi không thay sản phẩm và bảo vệ thực tế.
- Hạng mục liên quan mục 6 của PDF trong review trước đã được loại khỏi phạm vi và danh sách việc tiếp theo theo yêu cầu mới.
- 10 ảnh MNIST chỉ minh họa, mỗi model 3/10; chưa có ảnh camera do nhóm cung cấp. Chưa thử máy/OS khác. Không có BM06 để tự quy đổi điểm. ready_to_submit vẫn false.
- Git: đã commit `2852161` (28 file thay đổi) và push `70ad779..2852161`; xác minh HEAD remote khớp local và working tree sạch tại thời điểm sau push. Không động code app/model/dependency, không force-push. Bản ghi nhận này nằm trong commit tài liệu tiếp theo.

## Cụm 9: cập nhật phạm vi và tổng hợp Final Audit A–I

- Đã đọc đầy đủ nội dung Final Audit người dùng đính kèm. Theo ngữ cảnh yêu cầu mới, bỏ mục 6 của PDF khỏi checklist và danh sách việc còn thiếu; vẫn giữ kiểm tra kỹ thuật notebook/code và PDF gốc.
- Đã cập nhật AGENTS, HANDOFF, README, FINAL_REVIEW, REQUIREMENTS_MAP và metadata phạm vi review. Không tạo lại file nhật ký riêng. Không đổi model, code ứng dụng/notebook, dependency hoặc kết quả thực nghiệm.
- Tạo `docs/FINAL_AUDIT.md` theo cấu trúc A–I: bảng đối chiếu, lỗi đã sửa, metric/cost/best params đọc từ artifact, kiểm thử đã chạy, khoảng điểm tham khảo có giới hạn, việc còn thiếu và lệnh Windows. Giữ macro F1 CV làm tiêu chí chọn đã định trước; không thay lựa chọn theo test hoặc cách gọi metric trong checklist mới.
- Kiểm tra cập nhật này: cấu trúc A–I đủ 9 mục, liên kết tài liệu hợp lệ, không còn hạng mục mục 6 trong bảng đánh giá/việc tiếp theo; model/registry/metric/prediction/report JSON được bảo vệ vẫn khớp SHA256. Đây là chỉnh sửa tài liệu nên không chạy lại training hoặc lặp test code không thay đổi. Bằng chứng kỹ thuật gần nhất vẫn là 31/31 tests và rerun metric difference=0 ở cụm 8.
- Trạng thái vẫn NOT READY vì nhận định/phân tích nhóm, báo cáo/slide chính thức và phân công/vấn đáp chưa hoàn thiện; hạng mục đã loại không còn là điều kiện cản trở.
- Git: cập nhật phạm vi/tài liệu được lưu trong commit chứa cụm này, trên main nối tiếp `1d4714f`; xem git log để lấy hash mới nhất. Không sửa lịch sử hoặc force-push.
