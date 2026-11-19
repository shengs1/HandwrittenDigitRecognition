# Tối ưu nhận diện ảnh ngoài — kết quả ngày19/11/2026

Nhận định **dự thảo để nhóm rà soát/xác nhận**. UI giữ thiết kế FROZEN; code upload được thay đổi trong phạm vi yêu cầu mới. Không đổi notebook,3 Pipeline Digits, registry chính thức hoặc số liệu cũ. Không push main trước review.

## Dữ liệu, nguồn và khóa trước thực nghiệm

600 ảnh nguyên bản từ3 repository:200 BHMSDS,200 Bitmap Numbers,200 HwD-1000; mỗi nguồn20/chữ số. Seed42, chọn không hoàn lại rồi chia10/chữ số/nguồn vào validation và10 vào test:300+300. Lưu bytes nguyên gốc, nhãn tác giả, filename/path/kích thước/mode/SHA256/commit/split trong [manifest](../../data/external_handwriting/manifest.csv); [nguồn và license](../../data/external_handwriting/SOURCES.md),6 contact sheet và audit31200 ảnh trong cùng thư mục data. Không có ảnh hỏng/trùng pixel/conflicting label trong pool; không bỏ ảnh vì dự đoán sai. Tất cả600 mẫu đã được xem ở mức audit nhãn/tính hợp lệ, không dùng test predictions để chọn phương pháp.

BHMSDS là ảnh giấy được tác giả chụp rồi cắt/resize28×28, MIT. Bitmap là scan đổi PDF→PNG→BMP/resize128×128 từ nguồn public-domain/CC0 được README dẫn; mất mapping người viết và có méo/nhiễu sẵn. HwD-1000 là người vẽ tay số28×28, MIT. Không gọi cả3 là ảnh điện thoại nguyên bản. Không có writer/sheet ID đáng tin ở các bản dẫn xuất; không suy diễn nhóm từ số file, nên chia theo ảnh và chỉ bảo đảm không trùng pixel. Không chứng minh độc lập người viết/style. Bitmap upstream có cả dữ liệu tự động/chữ in; bản dẫn xuất tự mô tả là handwritten, review600 ảnh không thấy mẫu rõ ràng là font/AI/MNIST, nhưng không khôi phục được lịch sử đầy đủ từng ảnh.

MNIST dùng archive CVDF có MD5 đối chiếu torchvision. MNIST train60000 được chia54000/6000, stratify, seed42; hash ảnh không giao train/validation. Không dùng augmentation. [Danh sách split](mnist_train_split.csv) được lưu trước model. Loại chính xác110 MNIST test đã xem ở hai lượt cũ và nội dung trùng chúng; không có giao pixel với train. Còn9890 test. [Eligibility](mnist_test_eligibility.csv) và protocol được khóa trước validation. Không dùng Digits test, MNIST110,9890 test hoặc external300 test để chọn cấu hình.

[Protocol](protocol.json) khóa18:03:44UTC18/11, tức01:03:44 ngày19/11 Việt Nam. [Selection lock](selection_lock.json) khóa18:12:59UTC, trước final_test/start.json18:13:05UTC. External manifest khóa sớm hơn tại18:01:14UTC. Hash tương ứng giữ trong các file .sha256/JSON. Đây là thiết kế lập sau khi đã biết100 ảnh MNIST cũ, không phải đăng ký trước từ đầu đồ án.

## Cơ sở kỹ thuật và không gian thử nhỏ

[UCI mô tả](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) ảnh gốc nhị phân32×32 được chia các khối4×4 không chồng lấn và đếm pixel nét, tạo8×8 số nguyên0–16. App cũ dùng crop/ngưỡng nét, resize lên canvas64×64, căn trọng tâm có chặn cắt nét và BOX về8×8, tạo giá trị liên tục0–16. Khác cách biểu diễn là giả thuyết có cơ sở; không mặc định đó là nguyên nhân duy nhất.

Giữ nguyên trọng số của cả3 Pipeline, thử7 phương án chung trong external_preprocessing.py:

| Biến thể | Quy tắc cố định |
|---|---|
|baseline|Đúng hàm app.preprocess_uploaded_image cũ, giữ nguyên trong app để đối chiếu|
|gray_bbox|Grayscale/nền/EXIF/alpha; crop mask≥max(12;20% tương phản), chuẩn hóa đỉnh tương phản; giữ tỷ lệ trong canvas32×32 với nét tối đa24×32; căn bbox; tổng grayscale từng khối4×4,0–16|
|gray_com|Như gray_bbox nhưng dịch theo trọng tâm, chặn dịch cắt nét|
|binary35|Như gray_com, nhị phân ngưỡng0,35 rồi đếm pixel4×4|
|binary50|Ngưỡng0,50|
|binary35_thick|Ngưỡng0,35 rồi MaxFilter3×3 một lần ở canvas32|
|gray_wide|Grayscale+trọng tâm, khung nét tối đa28×32|

Block-count chỉ tái hiện bước gộp khối UCI, không tái hiện toàn bộ chuẩn hóa NIST trước đó. Không có hàng trăm cấu hình, denoise tùy ảnh hoặc chọn phương án dựa vào nhãn/xác suất từng ảnh. Chuẩn hóa tương phản là xử lý ảnh; scaler học đặc trưng vẫn chỉ ở Pipeline. Không áp dụng scaler hai lần.

## Validation và lựa chọn đã đặt trước

Chọn preprocessing chung theo **mean macro F1 của3 Pipeline trên external validation300**; hòa dùng mean accuracy rồi phương án đơn giản hơn/thứ tự khai báo. Chỉ tích hợp nếu mean F1 tăng≥0,02 và KNN không giảm F1. MNIST validation6000 báo riêng; không gộp hai dataset thành một accuracy.

| Phương án | F1 LR ngoài | F1 KNN ngoài | F1 MLP ngoài | Mean F1 ngoài | Mean accuracy MNIST6000 |
|---|---:|---:|---:|---:|---:|
|baseline|0,5867|0,4784|0,4042|0,48980|39,694%|
|gray_bbox|0,6394|0,5998|0,5385|**0,59260**|43,722%|
|gray_com|0,5993|0,4906|0,4300|0,50661|40,178%|
|binary35|0,5849|0,4844|0,4551|0,50816|40,217%|
|binary50|0,5906|0,4855|0,4410|0,50569|40,511%|
|binary35_thick|0,6123|0,3473|0,3502|0,43660|34,611%|
|gray_wide|0,6366|0,4361|0,4115|0,49473|41,061%|

Nguồn đầy đủ per-model/per-source: [validation/metrics.csv](validation/metrics.csv), [bảng tổng hợp](analysis/validation_all.csv) và các pivot trong analysis/. Mean là trung bình điểm của3 mô hình để chọn phương án, không phải accuracy của một hệ thống hoặc số đo gộp dataset. gray_bbox đạt điều kiện tăng0,10280 mean F1 và KNN tăng từ0,4784 lên0,5998, nên được khóa cho upload8×8. Kết quả bbox tốt hơn trọng tâm trong phạm vi này; không kết luận trọng tâm luôn kém hoặc có bug.

Các phương án8×8 chưa đạt mốc tham khảo90% mean accuracy MNIST validation, nên thực hiện đúng điều kiện đã đặt trước: **một MLP MNIST**, không thử thêm kiến trúc sau khi thấy test. Ảnh train/validation đều qua cùng mnist28: đọc nền/grayscale, crop/chuẩn hóa tương phản, nét tối đa20×20 trên canvas28×28, căn trọng tâm có chặn cắt nét. Flatten784; Pipeline MinMaxScaler→MLP(128,64), relu, adam, alpha0,0001, seed42, batch256, max_iter60, early stopping, n_iter_no_change8. Không huấn luyện bằng600 ảnh mới hoặc MNIST test.

| Tập validation của MLP28 | N | Accuracy | Macro F1 |
|---|---:|---:|---:|
|MNIST validation ngoài|6000|97,3167%|0,972961|
|Ba nguồn ngoài cân bằng|300|90,0000%|0,896684|
|BHMSDS|100|86,00%|0,853380|
|Bitmap Numbers|100|85,00%|0,833128|
|HwD-1000|100|99,00%|0,989975|

Nguồn [specialist/validation_metrics.csv](specialist/validation_metrics.csv). Điều kiện thêm lựa chọn upload là MNIST validation≥90% và F1 ngoài vượt mô hình8×8 tốt nhất ít nhất0,02; cả hai đạt. Pipeline.fit nhận54000 ảnh, MLP giữ5400 ảnh bên trong để early stopping; scaler thấy đặc trưng cả outer train trước lần chia nội bộ đó, nhưng không thấy6000 validation ngoài. Đây là giới hạn diễn giải validation nội bộ. MLP dừng30 iterations, lưu trọng số tốt nhất theo accuracy validation nội bộ, không theo test. Không refit trên train+validation sau khóa.

## Đánh giá cuối cùng trên đúng cùng các tập test

Đối chiếu riêng với Digits test360 chính thức, không đổi preprocessing của ảnh Digits:

| Pipeline Digits cố định | Accuracy Digits360 | Macro F1 Digits360 |
|---|---:|---:|
|Logistic Regression thô|95,8333%|0,958075|
|KNN|96,6667%|0,966304|
|MLP Digits|96,1111%|0,960888|

Nguồn [bảng chính thức](../20261117T081201Z_fd32180f/model_comparison.csv). Đây là dataset khác với các bảng bên dưới; không dùng chúng để tính accuracy gộp. MLP MNIST28 không tham gia lựa chọn mô hình Digits chính thức.

| Hệ thống đã khóa | MNIST9890 accuracy | MNIST macro F1 | Ngoài300 accuracy | Ngoài macro F1 |
|---|---:|---:|---:|---:|
|LR + cũ|46,4105%|0,473055|63,3333%|0,642764|
|KNN + cũ|41,9312%|0,427209|48,0000%|0,490304|
|MLP Digits + cũ|36,8049%|0,380337|49,6667%|0,489448|
|LR + gray_bbox|49,4944%|0,502436|64,6667%|0,651633|
|KNN + gray_bbox|47,0677%|0,471308|58,0000%|0,573268|
|MLP Digits + gray_bbox|42,0829%|0,434002|53,3333%|0,538202|
|MLP MNIST28|97,3913%|0,973773|87,3333%|0,871326|

Nguồn [final_test/metrics.csv](final_test/metrics.csv). Tất cả hệ thống được đánh giá trên cùng9890 hoặc cùng300 ảnh, không có từ chối ở các tập này. Không so accuracy mới với100 ảnh cũ như phép đo tăng công bằng;100 ảnh cũ giữ nguyên kết quả46/40/37 trong run riêng.

Trên external300, gray_bbox tăng LR/KNN/MLP lần lượt**1,3333/10,0000/3,6667 điểm phần trăm accuracy** so preprocessing cũ. MLP28 hơn KNN cũ39,3333 điểm và LR cũ24,0000 điểm; trên MNIST9890 hơn KNN cũ55,4601 điểm. [Bảng delta](analysis/final_comparisons.csv) ghi reference rõ từng dòng. MLP28 đồng thời khác dữ liệu huấn luyện, lượng mẫu, kiến trúc và độ phân giải; không quy toàn bộ cải thiện cho resize hoặc preprocessing. Không quay lại tuning hoặc chọn lại phương pháp sau test.

| Hệ thống | BHMSDS100 accuracy | Bitmap100 accuracy | HwD100 accuracy |
|---|---:|---:|---:|
|LR cũ|54%|55%|81%|
|KNN cũ|44%|38%|62%|
|MLP Digits cũ|49%|35%|65%|
|LR gray_bbox|57%|55%|82%|
|KNN gray_bbox|55%|48%|71%|
|MLP Digits gray_bbox|54%|41%|65%|
|MLP MNIST28|82%|82%|98%|

Macro F1/precision/recall theo nguồn có trong metrics.csv; precision/recall/F1/support từng chữ số ở `final_test/<dataset>__<system>__<source>__per_digit.csv`, classification report JSON và confusion CSV cùng prefix. Không coi98% trên ảnh vẽ tay số là98% trên ảnh scan hoặc ảnh điện thoại. Accuracy87,3333% chỉ là mẫu ngoài cân bằng ba nguồn này.

## Hình ảnh, phân tích nguyên nhân và lỗi

[Ảnh trung bình train/validation](analysis/figures/validation_class_means.png), [phân phối](analysis/figures/validation_distributions.png), [lịch sử học](analysis/figures/mlp_mnist_training.png). Tất cả thống kê để phân tích nguyên nhân dùng train hoặc validation; mask nét≥20% đỉnh từng ảnh chỉ là descriptor, không làm đầu vào thay thế cho model. CSV giữ mean/std và từng lớp. Std descriptor dùng ddof1, khác std CV cũ(ddof0).

| Mean trên ảnh validation (đổi cường độ về0–16 để mô tả) | Digits train1437 | Ngoài300 cũ | Ngoài300 gray_bbox |
|---|---:|---:|---:|
|Độ sáng pixel|4,89509|1,98050|2,12786|
|Tỷ lệ pixel đúng0|48,855%|47,714%|53,031%|
|Tỷ lệ vùng nét≥20% đỉnh|42,213%|31,693%|31,307%|
|Rộng/cao vùng nét|0,69642|0,73072|0,72771|
|Chiều cao vùng nét/ảnh|1,00000|0,95125|0,95125|
|Tâm nét x/y chuẩn hóa|0,50870/0,49753|0,50024/0,48740|0,50131/0,48037|

Ảnh ngoài mảnh/tối hơn và có bố trí nét/lề khác. Tỷ lệ foreground là proxy diện tích nét, không phải đo độ rộng bút vật lý. gray_bbox tăng sáng trung bình nhưng vẫn khác Digits; cải thiện còn hạn chế. Nhị phân và làm dày không thắng validation; việc khớp bước đếm khối không tự tái hiện toàn bộ miền Digits. Một số khác biệt hình dạng vẫn tồn tại ở cùng shape8×8. Thiếu đối chứng tách riêng từng yếu tố nên chưa xác định nguyên nhân duy nhất hoặc phần accuracy mất do mỗi bước.

[Ma trận MNIST](analysis/figures/mnist_test_confusion_annotated.png), [ma trận ngoài](analysis/figures/handwriting_test_confusion_annotated.png); cả7 hệ thống có nhãn, số đếm và màu. [Ví dụ lỗi MNIST trước/sau](analysis/figures/mnist_test_errors_before_after.png), [ngoài trước/sau](analysis/figures/handwriting_test_errors_before_after.png) lấy8 ID lỗi KNN cũ nhỏ nhất theo ID, không chọn theo mức tăng. Mỗi hàng giữ ảnh gốc, input8×8 cũ, input8×8 mới và input28×28 cùng dự đoán. Danh sách đúng/sai đầy đủ ở final_test/*correct.csv và *incorrect.csv.

Các hình cho phép quan sát mất khe/vòng/nét mảnh khi gộp8×8, thay vị trí nét do căn giữa và cách viết khác. Đây là quan sát hỗ trợ giả thuyết, không phải giải thích nhân quả quyết định của từng model. MLP28 còn38/300 ảnh sai; chưa phân tích lỗi để chỉnh lại nó. Không có bằng chứng rằng preprocessing cũ bị sai miền hoặc đảo nền; nó vẫn giữ nguyên cho baseline. Các kiểm thử mới xác nhận polarity/alpha/lề lớn/dịch chuyển/nét mỏng-dày, ngưỡng lỗi ảnh trống/hỏng/ít tương phản và phép đếm khối trên một hình chữ nhật biết trước. Fixture tổng hợp chỉ phục vụ regression, không nằm trong dữ liệu accuracy.

## Chi phí và độ tin cậy số đo

MLP28 fit23,8956s trên54000 input,30 iterations, joblib toàn Pipeline nén3 có1221502 byte. Loss đầu0,479294/cuối0,000754; validation nội bộ tốt nhất0,977593. [Metadata và cảnh báo](specialist/metadata.json), [training log](training.log), environment.json ghi thư viện/Python/BLAS. Không có warning hội tụ. Không so trực tiếp fit này với fit trên1437 Digits như cùng một khối lượng công việc.

| Model | Dung lượng Pipeline (byte) | Predict+predict_proba trên9890 MNIST | Trên300 ảnh ngoài |
|---|---:|---:|---:|
|LR gray_bbox|5935|0,010063s|0,003444s|
|KNN gray_bbox|140738|0,134679s|0,012868s|
|MLP Digits gray_bbox|159039|0,028096s|0,004562s|
|MLP MNIST28|1221502|0,090078s|0,004740s|

Nguồn metrics_with_cost.csv: cùng máy,2 luồng số học, **một lần đo batch gồm hai API**, không phải latency Streamlit hay benchmark nhiều lần. Preprocessing tách riêng:300 ảnh cũ0,4245s;gray_bbox0,2417s;MNIST28 0,3256s từ bytes đã có, không bao gồm tải/encode nguồn. Các file arrays/*.json ghi rõ. Không hứa tốc độ trên máy khác hoặc diễn giải sai số thời gian nhỏ.

## Tích hợp, kiểm thử, khôi phục

Thiết kế UI_STYLE, dark theme, typography, bố cục và3 thẻ Digits giữ nguyên. Upload của3 model Digits dùng gray_bbox; ảnh mẫu/test Digits vẫn lấy pixel gốc, kết quả360 ảnh/model không đổi. Có lựa chọn rõ **MLP — MNIST (ảnh ngoài)** chỉ ở nguồn upload; không tự chọn theo xác suất. Preview/header/vector/giới hạn/parameter table đổi đúng28×28/784/0–255/MinMaxScaler khi chọn nó. Chuyển về nguồn Digits sẽ trở lại KNN và xóa kết quả cũ vì model MNIST không dùng cho nguồn đó.

Model mới ở models/external_optimization_20261118T175401Z_4ca3a08f/, registry riêng models/external_registry.json ràng buộc hash model/module và selection lock. Không thay models/registry.json. App chỉ load joblib/cache, không fit. Hàm baseline cũ trong app được giữ nguyên để chạy đối chứng; preprocessing mới trong module riêng. Nếu thiếu cấu hình bổ sung, ba model Digits vẫn dùng luồng cũ; cấu hình/hash không hợp lệ hiện cảnh báo.

53/53 unittest PASS,8,451s; giữ nguyên43 test cũ.10 test mới kiểm dữ liệu600/shape64–784/scaler/proba, ảnh và session/upload-only/registry không tráo model ngoài lock. Lần đầu một test mới phụ thuộc thứ tự khởi tạo fixture nên lỗi; đã sửa fixture độc lập, không làm yếu assertion. [Log đầu](tests_initial.log), [log cuối](tests_final.log). Verify độc lập replay1200 suy luận qua API app trên300 test×4 model, khớp pixel/nhãn/xác suất đã lưu; tái tính report từng lớp, confusion và danh sách đúng/sai của35 dòng metric.

Browser thật zoom100% kiểm3 model×2 nguồn Digits,4 model upload PNG, scan BMP, file hỏng,15 vùng bấm dropdown, technical784 không clipping và5 actual viewport1920×1080/1920×900/1536×864/1366×768/1280×720 không tràn khi technical đóng. Screenshot/JSON ở browser/. Upload qua harness tạm giữ native widget nhưng mock bytes, không thử lại hộp chọn file Windows; app.main/Pipeline thật được gọi. Hai lần automation thao tác trước khi Streamlit cập nhật case/nguồn đã được chờ đúng nội dung mới rồi kiểm lại; không sửa app theo lỗi timing công cụ.

587 file cũ bảo vệ (gồm notebook/model/registry chính thức và toàn bộ MNIST100) khớp checksum trước/sau. Thiết kế CSS và AST hàm preprocessing baseline giữ nguyên; chỉ app logic/docs được cho phép đổi. Đợt đầu thử dùng float32 chung đã được giữ riêng *_float32_diagnostic, sau đó replay đồng loạt mọi ứng viên8×8 với float64 để giữ đúng pixel API baseline; metric không đổi. Đây là sửa độ chính xác số học trước selection/test, không thêm cấu hình hoặc chọn run có điểm tốt hơn. MLP784 dùng float32 nhất quán từ preprocessing đến Pipeline.

Đề xuất **giữ bản tối ưu để người dùng review**: đã có cải thiện validation và kiểm chứng cùng tập test, không thay lựa chọn bằng test. Vẫn còn38 lỗi/300, không có accuracy ảnh do giảng viên/người dùng chụp mới và không phát hiện được mọi ảnh không chứa chữ số bằng predict_proba. Chỉ dùng ảnh một chữ số, nền đơn giản; ảnh nhiều ký tự/phông in/mờ/bóng/lệch sáng chưa được xác nhận. Không có đảm bảo writer-independent. Nếu muốn trở lại bản ổn định, xem README trong run: snapshot app trước thay đổi được giữ, không cần xóa model/dữ liệu. Chưa CODE FROZEN và chưa push main.

## Đoạn nhận định dự thảo để nhóm xác nhận

Ba Pipeline Digits cho độ chính xác cao trên test Digits nhưng giảm rõ khi nhận ảnh ngoài. Trên300 test cân bằng từ ba nguồn, preprocessing gray_bbox tăng KNN từ48% lên58%; MLP huấn luyện riêng trên MNIST đạt87,33%, macro F1 là0,8713. Kết quả của MLP này khác theo nguồn:82% trên BHMSDS,82% Bitmap Numbers và98% ảnh vẽ tay số HwD-1000. Sự khác biệt về nét, độ sáng, vị trí và mất chi tiết khi giảm về8×8 là các giả thuyết được hình ảnh/thống kê hỗ trợ, chưa phải kết luận nhân quả. MLP mới thay cả dữ liệu huấn luyện, số mẫu và độ phân giải nên không thể quy toàn bộ mức tăng cho riêng preprocessing. Bộ test chưa đại diện ảnh chụp bất kỳ và chưa tách được người viết; nhóm giữ toàn bộ38 lỗi để trình bày giới hạn, không dùng chúng tinh chỉnh tiếp.
