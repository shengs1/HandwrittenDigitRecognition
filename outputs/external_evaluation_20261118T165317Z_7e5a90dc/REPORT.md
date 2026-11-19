# MNIST100 — kết quả thật và phân tích giới hạn

Đây là nội dung **dự thảo để nhóm rà soát/xác nhận**, không phải nhận định đã được nhóm thông qua. Tất cả số liệu dưới đây lấy từ các CSV/JSON cùng run. Không chỉnh UI FROZEN, Pipeline, notebook hoặc tiền xử lý sau khi xem kết quả.

## Thiết kế phép đánh giá

Nguồn [MNIST test qua CVDF](https://github.com/cvdfoundation/mnist):10.000 ảnh grayscale28×28, pixel0–255, nhãn0–9; [tài liệu TensorFlow](https://www.tensorflow.org/api_docs/python/tf/keras/datasets/mnist/load_data) xác nhận cấu trúc và quyền sử dụng. Hai archive được tải mới qua HTTPS và kiểm MD5 theo torchvision/SHA256 theo manifest có sẵn. Không sử dụng MNIST train hoặc thêm dữ liệu vào huấn luyện Digits.

Chọn100 ảnh bằng seed42 (PCG64),10/lớp, không hoàn lại. Loại ID cũ `[0,1,2,3,4,7,8,11,18,61]` và mọi nội dung pixel trùng ảnh cũ. Pool trong lần tải này có9.990 ảnh hợp lệ. Không có ID/nội dung pixel nào giao với10 mẫu đã thử. Danh sách và PNG được lưu trong sample_ids.csv/sample_lock.json **trước** inference_start.json; hash khóa không đổi qua run/verify. Mỗi mô hình nhận chính xác cùng100 ảnh, không loại ảnh vì khó/sai.

Gọi `app.preprocess_uploaded_image(data, background="Tự động")` rồi `app.predict_digit(saved_pipeline, pixels)`; không có nhánh xử lý MNIST riêng, không StandardScaler ngoài Pipeline. Tải3 joblib từ registry cố định. Pipeline.fit cùng fit của scaler/estimator được chặn trong lúc đánh giá. Dữ liệu huấn luyện, seed42, split1437/360 và lựa chọn KNN theo CV giữ nguyên.

## So sánh với test Digits chính thức

| Mô hình | Đúng MNIST/100 | Accuracy MNIST | Macro F1 MNIST | Accuracy Digits/360 | Macro F1 Digits | Đổi accuracy (điểm %) |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression pixel thô |46|46,00%|0,480071|95,8333%|0,958075|−49,8333|
| KNN |40|40,00%|0,422498|96,6667%|0,966304|−56,6667|
| MLP |37|37,00%|0,371433|96,1111%|0,960888|−59,1111|

Nguồn: [external_metrics.csv](results/external_metrics.csv), [comparison_with_digits.csv](results/comparison_with_digits.csv), CSV chính thức `outputs/20261117T081201Z_fd32180f/model_comparison.csv`. Không chạy lại test để tạo điểm mới. Macro precision lần lượt0,628755/0,503718/0,499637; macro recall0,46/0,40/0,37. Recall macro bằng accuracy ở mẫu này vì10 lớp đều có10 ảnh.

Điểm giảm mạnh trên mẫu ngoài cho thấy kết quả test Digits không chuyển trực tiếp sang MNIST qua luồng upload hiện có. LR cao nhất trong mẫu này; **không dùng thứ hạng này để chọn lại mô hình chính thức**. KNN vẫn là lựa chọn đã khóa bằng CV Digits. Không kiểm định chênh lệch giữa mô hình hoặc khẳng định thứ hạng phổ quát từ100 ảnh.

## Precision và recall theo chữ số

Mỗi lớp support10. Các cặp dưới là precision/recall, làm tròn4 chữ số:

| Chữ số | Logistic Regression | KNN | MLP |
|---|---|---|---|
|0|1,0000 /0,3000|0,7143 /0,5000|0,3333 /0,2000|
|1|0,3333 /0,4000|0,5385 /0,7000|1,0000 /0,4000|
|2|0,3750 /0,3000|0,2500 /0,3000|0,2308 /0,3000|
|3|0,6250 /0,5000|0,3571 /0,5000|0,5000 /0,1000|
|4|0,2286 /0,8000|0,1154 /0,3000|0,2353 /0,8000|
|5|1,0000 /0,4000|0,8000 /0,4000|0,3636 /0,4000|
|6|1,0000 /0,4000|0,6667 /0,4000|0,7500 /0,3000|
|7|0,6364 /0,7000|0,5000 /0,2000|0,5000 /0,5000|
|8|0,3750 /0,3000|0,4286 /0,3000|0,3333 /0,4000|
|9|0,7143 /0,5000|0,6667 /0,4000|0,7500 /0,3000|

Nguồn: [per_digit_all_models.csv](results/per_digit_all_models.csv), report JSON từng model. Precision1 của LR ở lớp0 nghĩa là3/3 lần dự đoán0 đúng; recall vẫn3/10. Một ảnh thay đổi làm recall lớp thay10 điểm phần trăm, nên không suy rộng số đo từng lớp này cho toàn bộ MNIST.

## Nhầm lẫn và ảnh sai

[Hình3 ma trận](figures/confusion_matrices.png), [các cặp nhầm](results/confusion_pairs.csv), các CSV correct/incorrect/predictions chứa đầy đủ danh sách và đường dẫn ảnh. Hàng là nhãn thật, cột là dự đoán; mỗi hàng tổng10.

LR/KNN/MLP dự đoán nhãn4 lần lượt35/26/34 lần, dù chỉ có10 ảnh thật lớp4. Riêng0→4 xuất hiện7/5/8 lần. KNN còn2→4 năm lần và6→4 bốn lần; MLP5→4 sáu lần,3→5 năm lần. Mẫu nhầm này khác với8→1 hay gặp trên test Digits, phù hợp khả năng lệch phân phối; chưa chứng minh nguyên nhân của từng quyết định.

Mỗi mô hình có một bảng8 cặp gốc/8×8, lấy **8 ID sai nhỏ nhất** theo quy tắc đã ghi trước. Không chọn lại100 ảnh để làm đẹp kết quả:

- [LR](figures/errors_logreg_raw.png): id102 nhãn5, nét ngang/vòng dưới nhạt và gộp ở8×8; dự đoán4. Id962 nhãn9 có vòng trên và đuôi dài, sau thu nhỏ vòng chỉ còn vài pixel; cả3 model đều dự đoán3.
- [KNN](figures/errors_knn.png): id997 nhãn0 có vòng nghiêng; vòng vẫn nhìn thấy ở8×8 nhưng cả3 model đều dự đoán4. Vì thế không thể giải thích mọi lỗi bằng việc mất hoàn toàn nét. KNN sai với xác suất100% ở ảnh này.
- [MLP](figures/errors_mlp.png): đối chiếu nhãn gốc, dự đoán và xác suất trong hình/CSV. Id1324 nhãn8 có hai vòng không đều; vòng dưới ở8×8 còn rất ít pixel. LR/MLP dự đoán7, KNN dự đoán3. Đây là quan sát hình ảnh, không phải lời giải thích nhân quả của mạng.

Trong54/60/63 ảnh sai của LR/KNN/MLP, số ảnh sai có xác suất≥0,9 là32/19/20. [Bảng đếm](results/high_confidence_errors.csv) cho thấy xác suất cao vẫn có thể sai trên miền ngoài; không gọi đây là xác suất đã hiệu chỉnh hoặc dùng nó để đặt ngưỡng mới.

## Phân phối dữ liệu, độ sáng, hình dạng và vị trí nét

[Ảnh trung bình từng lớp](figures/class_mean_comparison.png) và [histogram](figures/distribution_comparison.png) mô tả dữ liệu; chúng không đi vào dự đoán. Đối chiếu chính với **1437 ảnh train Digits đã lưu**, không fit lại hay tự chia train/test. CSV cũng giữ thống kê360 ảnh test để truy vết.

Các số dưới là mean trên ảnh; trước khi mô tả MNIST gốc, chỉ đổi đơn vị cường độ từ0–255 sang0–16 để so số đo. Đây là phép tính thống kê, **không phải đầu vào preprocessing thay thế**. Vùng nét dùng mask≥20% đỉnh riêng từng ảnh; tọa độ tâm chuẩn hóa theo kích thước ảnh,0,5 là giữa. Độ lệch chuẩn trong CSV dùng ddof1, khác std CV(ddof0) của thí nghiệm chính.

| Đặc trưng mô tả | Digits train8×8 (n1437) | MNIST gốc28×28 (n100) | MNIST qua app8×8 (n100) |
|---|---:|---:|---:|
|Độ sáng trung bình (0–16)|4,8951|2,0917|3,2737|
|Đỉnh cường độ trung bình|15,9791|15,9925|14,1095|
|Tỷ lệ pixel đúng0|48,8550%|80,7385%|40,2500%|
|Tỷ lệ vùng nét≥20% đỉnh|42,2125%|16,1811%|34,7656%|
|Chiều cao vùng nét/chiều cao ảnh|1,0000|0,7007|0,9200|
|Tỷ lệ rộng/cao vùng nét|0,6964|0,7975|0,8110|
|Tâm nét x|0,5087|0,5190|0,4998|
|Tâm nét y|0,4975|0,5170|0,4917|

Nguồn: [distribution_summary.csv](results/distribution_summary.csv), [distribution_by_digit.csv](results/distribution_by_digit.csv), định nghĩa trong tests/evaluate_external.py.

MNIST có nhiều lề đen ở28×28. App cắt vùng nét, giữ tỷ lệ trong khung tối đa48×64 rồi đặt vào canvas64×64, dịch tâm trong giới hạn không cắt nét, cuối cùng BOX về8×8. Do đó kích thước và vị trí nét sau app thay đổi so ảnh MNIST gốc. Trung bình tâm ngang gần0,5 với std0,0049, trong khi Digits train std0,0371; đưa tâm về giữa không bảo đảm bố trí nét giống dữ liệu học. Tâm dọc trung bình gần nhau nhưng độ phân tán và hình dạng lớp vẫn khác.

Ảnh sau app vẫn tối hơn Digits train (3,2737 so4,8951), đỉnh sáng thấp hơn và tỷ lệ vùng nét mạnh nhỏ hơn. Đồng thời pixel đúng0 ít hơn do các mức xám yếu sau nội suy/lấy trung bình. Điều này cho thấy cùng shape64 và miền0–16 chưa đủ đồng nhất phân phối. Hình trung bình lớp0/4/8 cho thấy khác hình và độ phủ nét; mỗi lớp MNIST chỉ10 ảnh nên hình trung bình còn nhiễu.

Việc thu784 vị trí gốc thành64 vị trí, kèm crop/nội suy/tạo trung bình, làm nét mảnh, khe hở và vòng nhỏ khó giữ. Các ảnh sai có ví dụ hỗ trợ khả năng này; id997 vẫn giữ vòng nhưng sai nên độ phân giải không giải thích toàn bộ. Phép đánh giá **không có đối chứng thay riêng độ phân giải hoặc preprocessing**, vì vậy không định lượng được bao nhiêu điểm accuracy mất do28→8, ngưỡng nét, căn giữa hoặc khác cách viết. Không suy luận quan hệ nhân quả chỉ từ histogram hoặc ảnh sai.

## Kiểm tra lỗi khách quan trong tiền xử lý

[Audit](results/preprocessing_audit.json), [diagnostics từng ảnh](results/preprocessing_diagnostics.json) và code app được đối chiếu. Cả100 ảnh gốc là28×28; crop box đều hợp lệ, nhận đúng nền tối, đầu ra100×8×8 float64 hữu hạn trong[0;15,937255], tối thiểu16 pixel khác0 và100 ảnh đầu ra khác nhau. Không ảnh bị từ chối. Lặp cùng bytes và đảo màu nền qua chính API đều cho mảng bằng hệt ở100/100 trường hợp; không có lỗi đảo nền hoặc ngẫu nhiên quan sát được. Verify replay100 preprocessing và300 dự đoán/xác suất khớp file lưu.

Không phát hiện lỗi khách quan về shape/miền/đọc file/đảo nền/trình tự pixel trong các kiểm tra đã thực hiện. Việc cắt theo ngưỡng20%, giữ tỷ lệ và BOX8×8 là hành vi đang có trong app; thông số và điểm số thấp chưa đủ chứng minh đây là bug. Các phép kiểm hợp đồng không chứng minh preprocessing tối ưu cho MNIST. Chưa đánh giá ảnh mờ, nền phức tạp hoặc ảnh điện thoại trong lượt này.

Chưa thay thuật toán. Nếu nghiên cứu tiếp, cần chốt tiêu chí giữ chi tiết/căn giữa và thử các giả thuyết trên **một tập validation ngoài mới chưa xem**; không dùng100 ảnh này hoặc10 ảnh cũ để chỉnh ngưỡng, chọn Pipeline hoặc thay registry. Một thay đổi về xử lý ảnh cần được đánh giá bằng quy trình riêng có tập cuối giữ kín.

## Độ tin cậy và phạm vi kết luận

Đây là100 ảnh trong10.000 test, lấy cân bằng có chủ đích. Accuracy mô tả tập cân bằng này, không ước lượng đúng theo tần suất tự nhiên của toàn bộ MNIST, càng không đại diện ảnh điện thoại. Không có writer ID để khẳng định tách người viết. Mẫu ảnh chưa trùng10 ảnh đã xem nhưng thiết kế phép đánh giá được lập sau khi biết kết quả cũ; không gọi nó là một thiết kế được đăng ký trước từ đầu đồ án. Có khóa mẫu trước suy luận và giữ nguyên app/model giúp hạn chế chọn kết quả thuận lợi.

332 file có sẵn, trừ HANDOFF được phép cập nhật, giữ SHA256 trước/sau. [Ba Pipeline khớp registry](results/model_integrity.csv), Digits hash khớp metadata chính thức; không đổi seed/split/mô hình. [Verify](verification.json) kiểm lại lựa chọn, tất cả dự đoán/xác suất, công thức precision/recall/F1 từ confusion matrix và phân hoạch đúng/sai. Toàn bộ43 unittest PASS trong7,309s, [log](unittest.log). Giữ nguyên kết quả10 MNIST cũ3/10 mỗi model; không gộp nó vào100 ảnh mới hoặc thay artifact chính thức.

## Đoạn nhận định ngắn dùng cho báo cáo — dự thảo

Trên100 ảnh MNIST test mới, lấy ngẫu nhiên với seed42 và10 ảnh mỗi chữ số, Logistic Regression, KNN và MLP lần lượt đạt46%,40%,37% accuracy; macro F1 tương ứng0,4801;0,4225;0,3714. Các điểm này thấp hơn đáng kể so với test Digits của cùng Pipeline. Ảnh MNIST sau luồng upload vẫn khác Digits về độ sáng, tỷ lệ và vị trí nét; việc giảm28×28 xuống8×8 có thể làm mất chi tiết nhưng phép thử chưa tách riêng ảnh hưởng từng bước. Không phát hiện lỗi hợp đồng tiền xử lý trong100 ảnh; xác suất cao vẫn có thể sai. Kết quả giới hạn khả năng sử dụng trên ảnh ngoài, không dùng để tuning hoặc chọn lại KNN chính thức, và chưa đại diện ảnh điện thoại.

## Gợi ý vấn đáp từ kết quả thật

1. **Vì sao cùng64 pixel vẫn giảm điểm?** Shape và miền là hợp đồng; histogram/hình trung bình cho thấy phân phối độ sáng và bố trí nét vẫn khác.
2. **Làm sao biết không chọn ảnh có lợi?** Xem seed/quy tắc/100 ID/hash trong sample_lock, thời điểm khóa trước inference_start;0 giao với10 ảnh cũ.
3. **Vì sao precision lớp0 của LR bằng1 nhưng recall0,3?** Chỉ3 ảnh được dự đoán0 và đều đúng, trong10 ảnh thật0 có7 ảnh bị bỏ sót sang4.
4. **Có đổi sang LR vì46% cao nhất không?** Không. Mô hình chính thức đã chọn bằng CV Digits;100 ảnh ngoài phục vụ phân tích giới hạn.
5. **Có thể kết luận giảm độ phân giải gây mất50 điểm không?** Không; chưa có đối chứng riêng từng bước, các yếu tố nguồn/cách viết/crop/độ sáng cùng thay đổi.
6. **Xác suất100% có bảo đảm đúng?** Không. KNN id997 nhãn0→4 với100%; đây là xác suất chưa hiệu chỉnh trên miền ngoài.
