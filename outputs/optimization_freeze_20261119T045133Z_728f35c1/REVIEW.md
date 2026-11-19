# Kiểm tra cuối và chốt phiên bản tối ưu —19/11/2026

**UI FROZEN · CODE FROZEN · EXPERIMENTS FROZEN · DOCUMENTATION AND PRESENTATION IN PROGRESS.** Người dùng duyệt giữ gray_bbox và MLP MNIST28 sau kiểm tra. Không fit/tuning,không đổi notebook/model/preprocessing/UI/requirements trong lượt này. Git commit/push được thực hiện sau kiểm tra cuối;SHA và đồng bộ remote xem HANDOFF/Git.

| Hạng mục | Trạng thái | Bằng chứng và giới hạn |
|---|---|---|
|Manifest600,300 validation+300 test,cân bằng|PASS|scientific_review.json/manifest_review.csv;bytes/pixel/size/nhãn theo tác giả khớp|
|Trùng xuyên nguồn/tập và biến thể đã biết|PASS trong phép kiểm|0 trùng byte/RGBA,grayscale/đảo nền/crop lề/nearest64;không chứng minh loại mọi near-duplicate/style|
|Độc lập người viết|PARTIAL|Không có writer/sheet ID đáng tin;không suy đoán group từ filename|
|License BHMSDS/HwD|PASS|MIT và attribution gốc giữ trong data/.../provenance;README nói rõ dataset được dùng|
|License Bitmap|PASS theo công bố nguồn|README dẫn tất cả ảnh từ kensanata/numbers public-domain/CC0;giữ LICENSE upstream. Không có LICENSE riêng cho derivative|
|Nguồn gốc từng ảnh Bitmap|PARTIAL|Mất mapping về ảnh/người viết upstream,không chứng nhận đầy đủ lịch sử từng ảnh;giữ cảnh báo,không đổi nhãn/mẫu|
|Ghi công/điều kiện MNIST|PASS sau bổ sung tài liệu|SOURCES.md của run mở rộng ghi tác giả,CVDF,CC BY-SA3.0 và biến đổi;không đổi dữ liệu|
|110 MNIST test cũ bị loại,9890 cuối|PASS|scientific_review.json tái tạo union10+100 và kiểm eligibility/không giao pixel train|
|54000 train/6000 validation/seed42|PASS theo bằng chứng|Tái lập split;scaler.n_samples_seen_=54000 vàmin/max khớp inputtrain;MLP.t_ tương ứng48600 gradient/iteration,5400 internalval;source train() không nhận test|
|Chọn theo validation/khóa trước test|PASS|gray_bbox mean F1 0,59260>0,48980;protocol/selection/module/model hash và timestamp trước final_test/start;không chọn lại|
|Độ đo mọi giai đoạn|PASS|145 dòng metric validation/specialist/test tái tính từprediction;report/per-digit/confusion khớp|
|MLP28 final|PASS|9632/9890=97,391304%;262/300=87,333333%;F1 ngoài0,871326407;38 sai;BHMSDS82,Bitmap82,HwD98 trên100/nguồn|
|KNN ngoài|PASS|Cùng300test:48%→58%,+10 điểm phần trăm;không thay96,6667% Digits|
|Venv mới/requirements|PASS|Snapshot2422 file/225654612byte ban đầu,không copyvenv/tmp/cache;Python3.12.14,120gói cài mới --no-cache;dependency check tương thích|
|Unittest sạch|PASS|53/53,0FAIL;lầnđầu15,096s clean_unittest.log;lầncuối sau đồngbộ7,374s clean_unittest_final.log;43 test cũ giữ nguyên|
|Git checkout giữchecksum|PASS sau sửa|2455/2455file export từindex bằngbytesworkingtree;53/53test PASS11,204s trênbảnexport bằngvenv mới;git_index_checks.json/git_index_unittest.log|
|Bốn Pipeline/registry/đặc trưng|PASS|clean_replay.log:1200 app predictions/pixels/proba khớp;4 model load,64/784/shape/classes/scaler đúng|
|Demo với3 model Digits×2 nguồn và4 model upload|PASS|clean_smoke.json:14 tình huống;PNG viết số+BMP scan;AppTest fixturebytes,gọi app/Pipeline thật|
|Thiếu/hỏng model|PASS|8 tình huống/4 model đều bị chặn ValueError/FileNotFoundError;không fit bù|
|Demo tối thiểu không dataset|PASS|minimal_demo.log:Digits0/uploadMNIST7,khi chặnfit/download;không códata/tests/tmp/MNISTIDX/arrays củaproject|
|Streamlit/browser thật từ venv mới|PASS|clean_browser.json;Digits0/MLPupload7,thông tin784/54000/MinMax;upload thật qua filechooser API nhận7-007.png|
|UI FROZEN vàstale result|PASS|CSS/app/module hash giữ nguyên;AppTest53 kiểmclear/model-onlyupload;browser chuyểnnguồn xóa result,technical0cellclipped|
|Responsive|PASS tại1366×768 trong lượt này|scale1,document/stMain768,overflow0;870×667 cuộn tự nhiên115px.5 viewport lịch sử giữ nguyên vìCSS không đổi|
|Ảnh điện thoại nhóm|CHƯA KIỂM|Chưa được cung cấp;README có hướng dẫn dùng app,không tạoảnh/sốliệu thay thế|

Các kiểm tra tái tính dùng số gốc,không dùng số làm tròn. Không quy tăng củaMLP MNIST chỉ cho preprocessing vìdata/lượngtrain/architecture/resolution cùng đổi. Dữ liệu ngoài gồmảnh giấy đã cắt/scan/vẽ số,không đại diện mọi ảnh điện thoại.

## Lỗi và chỉnh sửa

-Không tìm thấy lỗi model/preprocessing hoặc sai số liệu cần thay thực nghiệm.
-Tài liệu cũ nóiMNIST chỉ làfixture vàupload luôn8×8:đã cập nhậtREADME/AGENTS/HANDOFF và4 tài liệu báo cáo/slide/vấn đáp để táchA:Digits,B:mở rộng.
-Run mở rộng thiếu thông báoMNISTlicense tại chỗ:thêmSOURCES.md,giữ attribution/license của3 nguồn600 ảnh.
-Verifier cũ bảo vệ cả4 tài liệu báo cáo nên báoassert khi chúng được cập nhật theo yêu cầu. Đã giới hạn ngoại lệ đúng4 path tài liệu;mọi artifact/model/codeảnh vẫn được kiểm. Thêm --verification-output để ghi kiểm tra sang thư mục mới,không ghi đèrun frozen. Không sửa/làm yếu53 unittest.
-Major đã sửa trướcpush:core.autocrlf=true làmGitindex đổi byteCSV/JSON/nguồn cóchecksum (manifest vàselection lock đã được chứng minh khácworkingbytes). Thêm.gitattributes bảo toànbyte mọifile vàstage renormalize;whitespace checks vẫn bật,nhậnCR-at-eol hợp lệ. Đây là thaybiểu diễn lineending trongGit để giữ bytes chính thức,không sửa nội dung/thuật toán/notebook/model hoặc sốliệu. Kiểm lại bản xuất từindex và53tests vớivenv mới trướccommit.
-Kiểm export Git ởđườngdẫn snapshot sâu gặpFilename too long;dữliệu khônghỏng. READMEclone dùng `-c core.longpaths=true`;export lại ởtmp/gix_728f35c1 cóđườngdẫnngắn,không đổi tênartifact. Không thaycấu hìnhGit toàncục.
-Lần tạo venv đầu uv bị sandbox từ chối cache mặc định;chuyển cache cài mới vào thư mục kiểm tra,install --no-cache đạt. Đây là lỗi môi trường công cụ,không sửarequirements.
-Filechooser browser phản hồi1398s dù đã đặt timeout,cuối cùng nhận đúng file qua uploader thật;không xem thời gian đó làbenchmarkapp. Không thử thêm filechooser để tránh lặp chậm. AppTest kiểm toàn bộmodel/PNG/BMP. Lần screenshot đầu ngay sau resize không chụp được;đã đọcDOM mới vàchụp lại đúng1366×768.

## Phạm vi bảo vệ và đóng gói

Đầu lượt tất cả587 file lịch sử và1834 entries của manifest tối ưu khớp. Sau cập nhật đúng4 tài liệu báo cáo được yêu cầu,583 file lịch sử giữ nguyên;4 file khác ghi rõlàdocumentation. RootREADME/AGENTS/HANDOFF vàhelperverify thay đổi cóchủđích;app.py/external_preprocessing.py/notebook/theme/requirements/4Pipeline/registry/metric/prediction/split/locks giữ hash. Manifest tối ưu trước là snapshot lịch sử,không sửa để giấu thay đổi tài liệu;release_checks.json ghi các ngoại lệ/hashes mới.

Git giữ600 ảnh đã lấy mẫu,manifest/README/license,4Pipeline vàbằng chứng thực nghiệm. ZIP31.200 ảnh nguồn,venv/cache/snapshot/tmp không đưaGit. IDX/npz trong run lànguồn/đầu vào suy luận đã khóa dùng tái lập,không phải dependency củaapp;float32diagnostic giữ để truy vết replay trước lựa chọn,không dùng tăng điểm. Không cófile>100MiB. Chỉ giữđữliệu cólicense/attribution công bố;Bitmap vẫncó giới hạn mapping đã nêu.

Nhóm còn phải xác nhận nhận định,điềnthôngtin/phâncôngthật,xuấtbáocáoPDF/DOCX vàslidePPTX/PDF,tậpvấnđáp vàthửảnh tựchụp riêng. Không mở tuning/model/UI mới. Lệnh kiểm vàkết quảGit trongHANDOFF;ảnhthực tế ởclean_upload_1366x768.jpg.
