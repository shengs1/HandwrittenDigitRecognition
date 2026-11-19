# FINAL AUDIT — đề tài 13: Phân loại chữ số viết tay

**Snapshot audit lịch sử.** Trạng thái mới nhất: [Final Completion trong FINAL_REVIEW](FINAL_REVIEW.md). Nhận định đã có dự thảo từ output thật và app có sampler test; chưa nhóm xác nhận, chưa báo cáo/slide chính thức. Kết quả37 tests mới và checksum xem HANDOFF; các số test/trạng thái bên dưới giữ theo thời điểm audit.

Ngày cập nhật: 2026-11-17 (Asia/Saigon). Theo yêu cầu mới, mục 6 về sử dụng công cụ trong PDF không thuộc phạm vi audit và không nằm trong việc còn phải xử lý. Giữ nguyên PDF gốc; các kiểm tra kỹ thuật notebook/code vẫn giữ.

Đây là bản tổng hợp A–I từ kiểm tra đã thực sự chạy ở lượt final review ngay trước. Lượt cập nhật này chỉ sửa phạm vi/tài liệu, không tuyên bố đã chạy lại một đợt train mới. Code, Pipeline, dependency và số liệu được bảo vệ bằng checksum vẫn giữ nguyên.

## A. Đánh giá tổng quan

**NOT READY** cho việc nộp trọn bộ: kỹ thuật chạy và tái lập được, nhưng nhận định EDA/phân tích chính chưa được nhóm xác nhận và chưa có báo cáo/slide nộp chính thức. Không có Critical được phát hiện trong phạm vi code/artifact/kiểm thử. Không tự điền thông tin cá nhân hoặc xác nhận thay nhóm.

Repo giữ kiến trúc notebook chính + app.py, không backend/database riêng. KNN được chọn bằng mean CV macro F1 trước test. Mọi nguồn bảng/hình chính thức vẫn dùng run `20261117T081201Z_fd32180f` và models/registry.json.

## B. Bảng đối chiếu yêu cầu PDF



PASS = đã có bằng chứng trong phạm vi ghi rõ; PARTIAL = có một phần nhưng thiếu nội dung/xác nhận; FAIL = sản phẩm/nội dung bắt buộc còn thiếu. Không dùng PASS kỹ thuật để suy ra nhóm đã hiểu bài hoặc đạt điểm.

| Nguồn / yêu cầu | Trạng thái | File tương ứng / bằng chứng |
|---|---|---|
| A.1, A.3 bước 1: xác định phân lớp 0–9, mục tiêu, baseline | PASS | Notebook mục 1,6; LR thô và quy tắc chọn CV đặt trước |
| A.2: nhóm 3–5, đăng ký đề tài và ≥3 mục tiêu được giảng viên xác nhận | PARTIAL | Có mục tiêu trong notebook; chưa có danh sách/đăng ký/xác nhận trong repo |
| A.3 bước 2: nguồn chính thức, số mẫu/đặc trưng/shape/dtype | PASS | Notebook 2; data_summary.json, dataset_description.txt; Digits=(1797,64), ảnh 8×8 |
| A.3 bước 2: tỷ lệ thiếu từng cột | PASS | column_schema.csv đủ 65 cột (64 pixel + nhãn), missing ratio=0 |
| A.3 bước 3: kiểm tra thiếu/sai kiểu/trùng/nhãn/pixel/bất thường | PASS | Notebook 3–5, data_quality/quality_flags/train_image_diagnostics; cờ IQR chỉ train |
| A.3 bước 3: nhật ký quyết định có lý do và nhóm xác nhận | PARTIAL | Có CLEANING_DECISION giữ nguyên dữ liệu; bảng nhật ký nhóm vẫn TODO |
| A.3 bước 4: ≥5 EDA, tiêu đề/trục/chú thích | PASS | 6 EDA trên train; 15 PNG và source plot đã kiểm tra |
| A.3 bước 4: nhận định thực tế kèm từng EDA do nhóm xác nhận | FAIL | 6 ô Nhận định EDA trong notebook vẫn TODO; run_status student_interpretations_reviewed=false |
| A.3 bước 5, A.5: mọi preprocessing học được nằm trong Pipeline/fit train | PASS | Scaler trong CV/final Pipeline; scaler lưu có n_samples_seen_=1437, mean khớp đúng train; PCA chỉ EDA |
| A.3 bước 6: baseline Logistic Regression pixel thô | PASS | make_baseline, logreg_raw.joblib; scale=passthrough, C=1, seed 42 |
| A.3 bước 6: ≥2 mô hình so với baseline | PASS | KNN và MLP, 3 artifact có checksum; config khớp grid đã khóa |
| A.3 bước 6: split/stratify/seed | PASS | Train/test 1437/360, stratify=y, seed 42; test indices đúng train_test_split |
| A.3 bước 7: CV và tinh chỉnh trong Pipeline | PASS | StratifiedKFold 5/shuffle/42; KNN 6 cấu hình, MLP 4; GridSearchCV refit=False, train-only |
| A.5: không ảnh trùng xuyên train/test/CV | PASS | image_keys, cv_fold_audit; dataset và các fold kiểm tra trùng=0 |
| A.5: không dùng test để tuning/chọn mô hình | PASS | Đường gọi train/CV chỉ nhận train; selection_lock ghi trước predict test; registry chọn KNN bằng CV |
| Đề tài 13: đối chứng chuẩn hóa MLP cùng điều kiện | PASS | mlp_scaling_cv.csv 2 điều kiện×5 folds; cùng MLP_INITIAL/seed/folds; không test |
| A.3 bước 7: accuracy/precision/recall/F1/report | PASS | 4 metric được tính lại từ 360 dự đoán mỗi model; CSV report đã sửa, JSON và số đo gốc giữ nguyên |
| A.3 bước 7–8: confusion matrix, cặp nhầm và ảnh sai | PASS | confusion_matrix/pairs/misclassified CSV/PNG khớp test_predictions; cặp có hướng |
| A.3 bước 8: phân tích lỗi và giới hạn do nhóm viết | PARTIAL | Có dữ liệu/ảnh và cảnh báo giới hạn, chưa có phân tích chính được nhóm xác nhận |
| Đề tài 13: learning curve theo số mẫu và MLP training curve | PASS | Learning curve 15 điểm tổng hợp/75 hàng fold, loss và validation score 52 iterations; khớp artifact |
| Đề tài 13: kết luận overfitting có bằng chứng | PARTIAL | Có curves và hướng dẫn không ép kết luận; phần nhận định vẫn TODO |
| Đề tài 13: so chi phí/độ chính xác | PASS | Fit cuối, predict median 5 lần cùng test, tuning riêng, joblib bytes; median/timing/size đối chiếu đúng |
| A.5: seed và phiên bản thư viện, tính tái lập | PASS | requirements, metadata/env; rerun metric difference=0, CV/learning curves và prediction khớp |
| A.5: giải thích lựa chọn metric | PARTIAL | Có mô tả macro F1/accuracy; chưa xác nhận nhóm tự giải thích được quyết định nghiệp vụ |
| Nhất quán notebook/model/bảng/biểu đồ | PASS | Registry và checksum giữ nguyên; test_artifacts đối chiếu độc lập; docs bảng dùng cùng canonical run |
| Nhất quán với báo cáo và slide chính thức | PARTIAL | Chỉ kiểm tra được dàn ý/RESULTS_INDEX; chưa có bản nộp để đối chiếu |
| A.3 bước 9 (tùy chọn): demo dùng nguyên Pipeline joblib, không fit | PASS | AppTest chặn Pipeline.fit; app.py không gọi fit, cache/registry/hash; server clean checkout HTTP 200 |
| Demo: grayscale/nền/alpha/căn giữa/resize/0–16, không scale hai lần | PASS | test_demo kiểm đảo nền/alpha/tâm/miền; mẫu Digits giữ nguyên, proba khớp gọi Pipeline trực tiếp |
| Demo: file hỏng/trống/mất model | PASS | AppTest và unit test báo lỗi không crash; giới hạn 10 MB/16 triệu pixel |
| Demo: kiểm thử ngoài Digits và trung thực giới hạn | PASS | 10 MNIST chọn trước, mỗi model 3/10; không tuning lại, không diễn giải như accuracy ảnh chụp |
| Demo: chất lượng trên ảnh camera/ảnh thực tế của nhóm | PARTIAL | Chưa có bộ ảnh tự chụp có nhãn; không xác nhận tổng quát hóa |
| A.4: mã nguồn chạy từ đầu đến cuối | PASS | Notebook mới chạy 23 cell, 0 lỗi; app/test hoạt động trên clean checkout |
| A.4: requirements/README trên môi trường sạch | PASS | Venv mới từ requirements, 120 package tương thích; 31 test; checkout có dấu cách |
| A.4: model và nguồn dữ liệu kèm bài | PASS | 3 Pipeline/metadata/registry, load_digits và nguồn UCI, fixture ngoài có manifest |
| A.4: báo cáo PDF/DOCX | FAIL | Chỉ có REPORT_OUTLINE.md; PDF hiện có là đề bài, không phải báo cáo nhóm |
| A.4: slide trình bày | FAIL | Chỉ có SLIDE_OUTLINE.md, chưa có deck PDF/PPTX hoặc liên kết Slides |
| A.4: Git hoặc zip | PASS | Repo Git; dùng git archive kiểm tra checkout độc lập; cache/venv/tmp không track |
| A.7: báo cáo theo 10 mục | PARTIAL | Dàn ý có 10 mục đúng nguồn, nhưng chưa có báo cáo chính thức |
| A.8 câu 3: trình bày/demo/vấn đáp từng thành viên | PARTIAL | Demo đã test, có 30 câu gợi ý; chưa có buổi vấn đáp/đóng góp thành viên để xác minh |
| Đường dẫn riêng máy phát triển | PASS | Không thấy hardcoded machine path trong source; đã bỏ path trong output notebook; checkout mới có dấu cách chạy được |
| Code/dependency/kiến trúc đơn giản | PASS | Notebook chính + app.py, các file còn lại là test/tài liệu; các dependency trực tiếp có vai trò thực nghiệm/demo/kiểm thử, không backend/database phụ |

Phạm vi PASS về leakage: kiểm tra code và artifact hiện tại, không khẳng định lịch sử thao tác ngoài repository. Chia ngẫu nhiên không bảo đảm tách người viết; giới hạn đã được nêu. Early stopping MLP có validation nội bộ sau bước scaler trên train của fold; outer validation/test vẫn không tham gia fit. CV dùng lại để chọn scaler/grid có thiên lệch lựa chọn; không gọi đó là đánh giá độc lập.


### Năm câu hỏi riêng của đề tài 13



| Câu hỏi PDF trang 5–6 | Trạng thái | Bằng chứng / phần còn thiếu |
|---|---|---|
| Biểu diễn vector, shape; vì sao chuẩn hóa pixel | PASS | Notebook 2/7/8: 8×8→64; lý do về thang đầu vào/khoảng cách/tối ưu và thí nghiệm scaling train/CV |
| Baseline đạt bao nhiêu, MLP cải thiện ra sao | PARTIAL | Test LR=0.958333, MLP=0.961111; CV mean=0.963687/0.962365. Có bảng nhưng nhóm chưa viết so sánh có giới hạn |
| Cặp chữ số nào hay nhầm | PARTIAL | Ví dụ KNN 8→1 có 3 ca, 4→7 có 2; bảng/ảnh khớp dự đoán, chưa có phân tích nhóm |
| Learning curve cho thấy quá khớp ở đâu | PARTIAL | Có curves/raw fold/loss/validation; không có kết luận nhóm xác nhận, không tự bịa một mốc quá khớp |
| So chi phí và độ chính xác mô hình đơn giản/mạng nơ-ron | PARTIAL | Có timing/bytes/metrics đúng nguồn; chưa có diễn giải trade-off của nhóm |


## C. Những lỗi phát hiện và đã sửa



Không phát hiện **Critical** trong phạm vi code/artifact và các kiểm tra đã chạy. Điều này không chứng minh mọi ảnh bên ngoài đều được nhận dạng đúng.

| Mã | Mức | Vấn đề / ảnh hưởng | Trạng thái |
|---|---|---|---|
| M-01 | Major | Test phụ thuộc tmp/ chưa được track, khiến checkout mới lỗi 4 test và README chưa tái lập đầy đủ | **Đã sửa**: test_demo.setUpModule tự tạo tmp; kiểm tra trên checkout có dấu cách và venv mới |
| M-02 | Major | 6 nhận định EDA vẫn TODO, nhật ký/nhận định kết quả/lỗi/learning curve chưa có xác nhận của nhóm | **Chưa hoàn thiện**, thuộc nhóm; không tự điền |
| M-03 | Major | Chưa có báo cáo PDF/DOCX và slide nộp chính thức; dàn ý Markdown không thay các sản phẩm bắt buộc | **Chưa hoàn thiện**, thuộc nhóm |
| m-01 | Minor | pd.DataFrame(report).T broadcast scalar accuracy sang precision, recall và support; support thành 0.9667 thay vì 360 | **Đã sửa** exporter và 3 CSV canonical từ JSON gốc; precision/recall của dòng accuracy để trống, f1-score giữ accuracy, support=360 |
| m-02 | Minor | Notebook output nhúng đường dẫn riêng của workspace | **Đã sửa** print dùng đường dẫn tương đối, sửa text output tương ứng; không thay metric/ảnh/số liệu |
| m-03 | Minor | Snapshot Phase 1 còn nằm dưới tiêu đề trạng thái mới nhất của HANDOFF | **Đã làm rõ** bằng tiêu đề lịch sử và phần final review hiện hành |

Ba CSV chỉ được chỉnh **định dạng dòng accuracy**, không huấn luyện hay sửa dự đoán. Kiểm tra lại từng lớp, macro metric và confusion matrix bằng tính toán độc lập. Chi tiết [trước/sau sửa format](../outputs/review_20261117T090347Z_9df57e69/csv_format_correction.json). Không thay nội dung phân tích của sinh viên.


## D. Kết quả thực nghiệm cuối cùng

Nguồn duy nhất của bảng dưới: [model_comparison.csv](../outputs/20261117T081201Z_fd32180f/model_comparison.csv). CV mean/std là macro F1, ddof=0; test chung 360 mẫu. Chỉ tổng hợp số đo, không thay phần diễn giải của nhóm.

| Mô hình | Accuracy | Precision macro | Recall macro | F1 macro | CV macro F1 mean ± std |
|---|---|---|---|---|---|
| logreg_raw | 0.958333 | 0.958731 | 0.958012 | 0.958075 | 0.963687 ± 0.007866 |
| knn | 0.966667 | 0.967759 | 0.966424 | 0.966304 | 0.976170 ± 0.007575 |
| mlp | 0.961111 | 0.961798 | 0.960944 | 0.960888 | 0.962365 ± 0.008314 |

Fit cuối đo riêng, predict median 5 lượt sau warm-up, tuning wall time riêng; dung lượng toàn Pipeline joblib nén mức 3.

| Mô hình | Fit cuối (s) | Predict cùng test (ms) | Tuning (s) | Pipeline (bytes) |
|---|---|---|---|---|
| logreg_raw | 0.098705 | 0.7978 | 0.000000 | 5935 |
| knn | 0.003107 | 4.7295 | 0.635378 | 140738 |
| mlp | 0.279319 | 1.5384 | 4.231378 | 159039 |

Cấu hình đọc trực tiếp từ Pipeline đã lưu:

- **logreg_raw:** C=1.0, solver=lbfgs, max_iter=3000, pixel thô.
- **knn:** k=3, weights=uniform, StandardScaler.
- **mlp:** hidden=(64, 32), alpha=0.0001, activation=relu, solver=adam, early_stopping=True, max_iter=300, StandardScaler.


**Model chọn: KNN**, theo mean CV macro F1 cao nhất, không chọn lại bằng test. Accuracy được báo cáo để dễ đọc; tiêu chí lựa chọn đã chốt là macro F1 CV. Không đổi tiêu chí sau khi xem test chỉ để khớp cách gọi “độ đo chính” trong checklist mới. CV sau lựa chọn scaler/grid có thiên lệch lựa chọn đã được nêu; test không dùng tuning.

Để tránh nhầm mức cải thiện: từ LR sang MLP, accuracy test tăng đúng 1/360, tức khoảng 0,2778 **điểm phần trăm**; tăng tương đối khoảng 0,2899% so với accuracy baseline. Đây không tự chứng minh cải thiện có ý nghĩa thống kê. Nhóm cần tự diễn giải cùng CV và các giới hạn, không suy ra quan hệ nhân quả.

## E. Kết quả kiểm thử

| Nội dung | Kết quả thực tế | Bằng chứng |
|---|---|---|
| Notebook đầy đủ | 23 cell mã, 15 hình, 0 error/0 stderr trong cell | [Notebook kiểm chứng](../outputs/review_20261117T090347Z_9df57e69/executed_notebook.ipynb) |
| Test sau sửa | 31/31 PASS, 7.283 giây | [Log](../outputs/review_20261117T090347Z_9df57e69/clean_checkout_tests.log) |
| Môi trường sạch | Python 3.12.14, 120 package, cài requirements từ cache offline, pip check qua | [Environment](../outputs/review_20261117T090347Z_9df57e69/clean_environment.json) |
| Tái lập metric/prediction | Chênh lệch metric=0, 3×360 dự đoán khớp; CV/scaling/curves và tham số khớp | [Checks](../outputs/review_20261117T090347Z_9df57e69/review_checks.json) |
| App | AppTest các model/mẫu/upload/lỗi; HTTP 200 từ checkout sạch | [Server check](../outputs/review_20261117T090347Z_9df57e69/streamlit_server_check.json) |
| Ảnh ngoài Digits | 10 MNIST chọn trước, mỗi model đúng 3/10; không tuning lại | [Dự đoán](../outputs/demo_20261117T082316Z_b269f12c/external_predictions.csv) |

Lệnh đã chạy trong lượt review kỹ thuật:

```powershell
uv --cache-dir .uv-cache venv <review-venv> --python .venv/Scripts/python.exe
uv --cache-dir .uv-cache pip install --offline --link-mode=copy --python <review-python> -r requirements.txt
uv --cache-dir .uv-cache pip check --python <review-python>
<review-python> -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
<review-python> -X utf8 tests/run_notebook.py
<review-python> -m streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
```

Placeholder chỉ interpreter trong venv review; các lệnh chạy ở checkout độc lập có dấu cách. Rerun id `20261117T091140Z_36eda884` chỉ để kiểm chứng, không thay model hoặc timing canonical. Cảnh báo khởi động kernel TCP và AppTest bare mode được giữ trong log, không ẩn convergence warning. Trong cell notebook kiểm chứng không có stderr. Chưa thử OS/máy khác hoặc bộ ảnh camera thật; chưa xác minh vấn đáp trực tiếp.

## F. Đánh giá theo thang điểm

**Ước lượng tham khảo, độ bất định cao, không phải điểm giảng viên đã chấm.** Không có BM06 nên không suy đoán trọng số chi tiết. Khoảng dưới giả định giảng viên cho chấm các phần kỹ thuật hiện có dù sản phẩm nộp còn thiếu; thực tế có thể thấp hơn nếu thiếu báo cáo/slide bị trừ theo quy định.

| Phần | Khoảng tham khảo | Căn cứ |
|---|---|---|
| Câu 1 | 2,0–3,0 / 4 | Dữ liệu, pipeline, 6 EDA có đủ; nhận định/journal nhóm còn thiếu |
| Câu 2 | 2,5–3,5 / 4 | Mô hình/CV/tuning/metric/error/curves đầy đủ; phân tích chính chưa xác nhận |
| Câu 3 | 0,5–1,0 / 2 | Demo có bằng chứng chạy; slide, trình bày và vấn đáp chưa thể xác minh |
| Tổng | **5,0–7,5 / 10** | Chưa phải điểm chính thức và không thể bảo đảm đạt mức trên |

Không coi “31 test PASS” là “đồ án 10/10”. Phần quyết định ở báo cáo, nhận định và bảo vệ thực tế chưa được kiểm chứng.

## G. Những việc còn thiếu trước khi nộp

1. Nhóm tự viết/xác nhận 6 nhận định EDA và nhật ký xử lý; phân tích kết quả, lỗi, learning curve và giới hạn.
2. Hoàn thành báo cáo PDF/DOCX theo 10 mục và slide chính thức; lấy số liệu/hình đúng canonical run.
3. Điền thành viên, phân công và đăng ký/mục tiêu đã duyệt bằng thông tin thật; tập giải thích và sửa code khi vấn đáp.
4. Chỉ khi muốn tuyên bố chất lượng ảnh camera, bổ sung ảnh tự chụp có nhãn/nguồn và giữ cả ca sai. Không cần thêm tính năng hoặc tuning để làm đẹp số test.

## H. Hướng dẫn chạy cuối cùng (Windows PowerShell)

Từ thư mục gốc project, với Python 3.12 đã cài:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m notebook digit_classification.ipynb
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Chọn kernel .venv. Notebook đã có kết quả; chỉ Restart Kernel/Run All khi chủ động tái lập thí nghiệm, không cần chạy lại để mở demo. Lệnh offline toàn notebook là `.\.venv\Scripts\python.exe -X utf8 tests/run_notebook.py`. Nếu Python là alias Microsoft Store không chạy, dùng interpreter Python thật. Với venv tạo bằng uv không có pip, dùng `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`. Xem README để xử lý thiếu model/registry; app không tự fit bù.

## I. Kết luận

**NOT READY.** Các kiểm tra kỹ thuật đã qua và model/kết quả giữ nguyên, nhưng báo cáo/slide và phần phân tích được nhóm xác nhận chưa hoàn thành. Không có blocker kỹ thuật đã biết trong phạm vi đã test; không tự đánh dấu hoàn thành những sản phẩm hoặc năng lực chưa có bằng chứng.
