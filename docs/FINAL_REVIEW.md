# Final review trước buổi bảo vệ — đề tài 13

## Trạng thái mới nhất — Final Completion (2026-11-17)

**Thay thế kết luận về TODO nội dung của snapshot phía dưới.** Đã bổ sung 15 markdown cells: nhật ký làm sạch, 6 EDA, lỗi/learning history, so sánh/chi phí/giới hạn và đủ 5 câu đề tài. Đây là **dự thảo chưa được nhóm xác nhận**. Báo cáo 10 mục và nội dung 12 slide đã có trong Markdown; chưa có sản phẩm PDF/DOCX/PPTX chính thức. Phần kỹ thuật đã kiểm chứng, chưa xác nhận sẵn sàng nộp.

Không phát hiện Critical mới. Hai thiếu sót thực tế đã xử lý: notebook còn TODO nhận định; app chưa phân biệt mẫu test. Thuật toán tiền xử lý chưa phát hiện lỗi khách quan qua kiểm thử, được giữ nguyên. Các lỗi cũ và bằng chứng Run All ở phần lịch sử phía dưới.

| Mức | Vấn đề hiện tại | Trạng thái |
|---|---|---|
| Critical | Chưa phát hiện lỗi làm sai kết quả trong phạm vi kiểm tra | Không có lỗi mở được xác định |
| Major | Thiếu báo cáo/slide chính thức và thông tin, phân công thật | Còn mở; đã chuẩn bị nội dung dự thảo |
| Major | Nhận định và quyết định dữ liệu chưa được nhóm xác nhận | Còn mở; đã có dự thảo có bằng chứng |
| Minor | Mẫu Digits trong demo chưa phân biệt train/test | Đã sửa; thêm nguồn test theo split lưu và kiểm thử |

| Kiểm tra hiện tại | Trạng thái / bằng chứng |
|---|---|
| Toàn bộ test trên source checkout sạch với diff mới, không tmp ban đầu | **37/37 PASS**, 4,807 s; [log](../outputs/completion_20261117T100609Z_b8981ac1/clean_checkout_tests.log) |
| Môi trường | Dùng lại venv Python 3.12.14 sạch của review trước; mọi pin requirements khớp; [versions](../outputs/completion_20261117T100609Z_b8981ac1/clean_environment.json) |
| Notebook | nbformat/syntax hợp lệ; 23/23 cell có execution_count, 15 PNG, 0 error; markdown không TODO; mã cell không đổi; [checks](../outputs/completion_20261117T100609Z_b8981ac1/completion_checks.json) |
| Artifact canonical | 60 file gồm model/registry/toàn outputs chính thức giữ SHA256; [trước](../outputs/completion_20261117T100609Z_b8981ac1/protected_before.json), [sau](../outputs/completion_20261117T100609Z_b8981ac1/protected_after.json) |
| Preprocessing | Source hash không đổi; đảo nền/RGB/RGBA/vị trí trên 10 ảnh train, EXIF, ảnh trống, tỷ lệ/centering và miền pixel qua tests |
| Ảnh test trong app | 360 id đọc từ split chính thức, membership khớp prediction cả 3 model; AppTest kiểm tra mỗi lớp và dự đoán 3 model |
| Streamlit thật | HTTP 200; KNN test id 10→ 0 đúng; upload MNIST 7→ 3 (33,3%, đồng hạng3/5/8), có gốc/8×8/chart; [ghi nhận](../outputs/completion_20261117T100609Z_b8981ac1/streamlit_check.json), [ảnh](../outputs/completion_20261117T100609Z_b8981ac1/streamlit_test_sample.jpg) |
| Mã notebook | Không Run All thêm lượt này vì mã/output không đổi; sử dụng bằng chứng rerun độc lập thành công bên dưới, không huấn luyện để tăng điểm |

### Đối chiếu PDF sau hoàn thiện

PASS chỉ cho nội dung kỹ thuật có bằng chứng; PARTIAL không phải đã được nhóm xác nhận.

| Yêu cầu PDF | Trạng thái | File và bằng chứng |
|---|---|---|
| Nhóm 3–5, đăng ký nguồn và ≥3 mục tiêu, giảng viên xác nhận | PARTIAL | Có 3 mục tiêu ở notebook/REPORT_OUTLINE; chưa có danh sách/đăng ký/xác nhận thật |
| Bài toán/nhãn/tiêu chí/baseline | PASS | Notebook 1,6,15; model_comparison/selection_lock; test_artifacts |
| Nguồn, shape/dtype/tỷ lệ thiếu từng cột | PASS | Notebook 2–3, data_summary/column_schema; test_contracts |
| Làm sạch có bằng chứng và lý do | PARTIAL | Nhật ký dự thảo notebook 3, kiểm tra 0 lỗi, 3 IQR giữ nguyên; nhóm còn xác nhận |
| ≥5 EDA đủ nhãn và nhận định | PARTIAL | 6 PNG train + 6 nhận định dự thảo notebook 5, đã xem hình; chưa nhóm xác nhận |
| Đặc trưng/Pipeline, fit train, chống leakage | PASS | Notebook 4–9/15; cv_fold_audit, tests kiểm trùng/scaler/selection |
| ≥2 mô hình so baseline, split đúng | PASS | LR thô/KNN/MLP, 1437/360, stratify42; artifacts và test_artifacts |
| Độ đo phù hợp và giải thích | PASS | Notebook 1/11/15 nêu macro F1/accuracy; metric tính lại từ 1080 predictions khớp |
| CV/tuning trong Pipeline | PASS | StratifiedKFold 5/shuffle42, grid nhỏ, cv_details; tests đối chiếu best params/CV |
| Phân tích lỗi/giới hạn | PARTIAL | Notebook 13–15 + REPORT_OUTLINE 7 có dự thảo và ảnh thật; nhóm xác nhận diễn giải |
| Demo/lưu toàn Pipeline (tùy chọn) | PASS | app/registry/3 joblib; 37 tests + HTTP/browser; không fit |
| Seed/phiên bản/tái lập môi trường sạch | PASS | environment/requirements; rerun notebook review trước + checkout 37 tests hiện tại |
| Báo cáoPDF/DOCX theo 10 mục | PARTIAL | REPORT_OUTLINE đã có nội dung10 mục; chưa xuất và rà soát bản nộp |
| Mã chạy từ đầu đến cuối | PASS | Rerun review 23cell/0error, code hash không đổi; 37 test mới qua |
| requirements/README/data hoặc nguồn/model | PASS | READMEWindows, pin khớp, modelhash và nguồn dataset có thật |
| Slide, trình bày/phân công/vấn đáp | PARTIAL |12 slide nội dung + VIVA; thiếu file trình chiếu, thông tin/đóng góp và xác nhận tập bảo vệ |
| Đề tài13: vector/shape/chuẩn hóa | PASS | Notebook 2/5/8 và câu1 cuối; scalingCV + stats |
| Đề tài13: baseline/MLP cải thiện thế nào | PASS | Notebook 15/câu2; LR 95,8333%, MLP 96,1111% test accuracy; không ép kết luận cải thiện chắc chắn |
| Đề tài13: cặp nhầm | PASS | Notebook 13/15/câu3; 8→ 1: 4/3/3; test so CM với CSV/predictions |
| Đề tài13: learning curve/overfitting | PASS | Notebook 14/câu4; learningcurve/history khớp; nêu chưa đủ xác định epoch |
| Đề tài13: chi phí/độ chính xác | PASS | Notebook 12/15/câu5; fit/predict/tuning/bytes tách riêng, số thật |

Các PASS của 5 câu hỏi xác nhận có câu trả lời và bằng chứng số liệu; không xác nhận thay khả năng giải thích của từng thành viên. Chưa có ảnh điện thoại của nhóm, BM06, báo cáo/slide nộp, thông tin cá nhân hoặc bằng chứng vấn đáp. Không auto commit/push. Danh mục bản nộp ở README.

## Snapshot Final Review trước hoàn thiện — lịch sử

Ngày review: 2026-11-17, Asia/Saigon. Base Git: `70ad779`. Đã đọc toàn bộ 6 trang [PDF giảng viên](Huong_Dan_Do_An_CuoiKy.pdf), AGENTS/HANDOFF/README, notebook, app, tests, model/registry, số liệu và tài liệu hiện có. Không có BM06 để đối chiếu thêm. Theo yêu cầu mới, mục 6 của PDF được loại khỏi phạm vi audit và không còn là việc cần xử lý. PDF gốc không bị chỉnh sửa. Bản tổng hợp A–I: [FINAL_AUDIT.md](FINAL_AUDIT.md).

**Kết luận: phần kỹ thuật chạy và tái lập được sau sửa; đồ án chưa đủ điều kiện xác nhận sẵn sàng nộp.** Thiếu nhận định được nhóm xác nhận, nội dung phân tích chính, báo cáo/slide hoàn chỉnh và bằng chứng phân công/vấn đáp. Không viết thay các phần đó hoặc tự cho điểm.

## Bằng chứng thực thi

Run chính thức giữ nguyên: `20261117T081201Z_fd32180f`, model mặc định KNN. Review chạy trên bản checkout độc lập có dấu cách trong đường dẫn, không có tmp ban đầu, bằng môi trường Python 3.12.14 mới tạo từ requirements. Cài offline từ cache, 120 package tương thích; chưa kiểm tra máy/OS khác.

| Kiểm tra | Kết quả | Bằng chứng |
|---|---|---|
| Tái hiện test trên HEAD cũ và checkout sạch | 25 tests, 4 errors do thiếu tmp | [Log trước sửa](../outputs/review_20261117T090347Z_9df57e69/baseline_fresh_checkout_tests.log) |
| Toàn bộ test sau sửa, môi trường mới | **31/31 PASS**, 7.283 giây theo unittest | [Log sau sửa](../outputs/review_20261117T090347Z_9df57e69/clean_checkout_tests.log), [environment](../outputs/review_20261117T090347Z_9df57e69/clean_environment.json) |
| Notebook chạy từ đầu đến cuối | 23 code cells, 15 hình nhúng, 0 error/0 stderr trong cell | [Notebook đã chạy riêng](../outputs/review_20261117T090347Z_9df57e69/executed_notebook.ipynb), [log](../outputs/review_20261117T090347Z_9df57e69/notebook_rerun.log) |
| Tái lập số liệu | Metric max absolute difference=0; 1.080 dự đoán (3×360) khớp; CV/scaling/learning curve và tham số khớp | [review_checks.json](../outputs/review_20261117T090347Z_9df57e69/review_checks.json), [bảng rerun](../outputs/review_20261117T090347Z_9df57e69/rerun_model_comparison.csv) |
| Bảo toàn kết quả đã xác nhận | Model, registry, model_comparison, test_predictions và report JSON không đổi SHA256 | [Trước](../outputs/review_20261117T090347Z_9df57e69/protected_artifacts_before.json), [sau](../outputs/review_20261117T090347Z_9df57e69/protected_artifacts_after.json) |
| Streamlit | AppTest qua mẫu/upload/lỗi ảnh/mất model; server checkout sạch trả HTTP 200 | tests/test_demo.py, [HTTP check](../outputs/review_20261117T090347Z_9df57e69/streamlit_server_check.json) |
| Hình biểu đồ | Kiểm tra 15 PNG: EDA, confusion/error, learning/history, so sánh | [Bản ghép QA](../outputs/review_20261117T090347Z_9df57e69/plots_contact_sheet.jpg) |

Lần chạy kiểm chứng riêng có id `20261117T091140Z_36eda884`; không dùng nó để thay model, bảng thời gian hoặc kết quả chính thức. Timing có thể khác theo tải máy; không ép timing khớp hoặc chọn lần nhanh nhất. Các source cell huấn luyện/tuning không đổi, chỉ cell `digits-048` được sửa cách xuất CSV và hiển thị đường dẫn.

## Phân loại lỗi

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

## Bảng đối chiếu PDF và yêu cầu review

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

## Năm câu hỏi riêng của đề tài 13

| Câu hỏi PDF trang 5–6 | Trạng thái | Bằng chứng / phần còn thiếu |
|---|---|---|
| Biểu diễn vector, shape; vì sao chuẩn hóa pixel | PASS | Notebook 2/7/8: 8×8→ 64; lý do về thang đầu vào/khoảng cách/tối ưu và thí nghiệm scaling train/CV |
| Baseline đạt bao nhiêu, MLP cải thiện ra sao | PARTIAL | Test LR=0.958333, MLP=0.961111; CV mean=0.963687/0.962365. Có bảng nhưng nhóm chưa viết so sánh có giới hạn |
| Cặp chữ số nào hay nhầm | PARTIAL | Ví dụ KNN 8→ 1 có 3 ca, 4→ 7 có 2; bảng/ảnh khớp dự đoán, chưa có phân tích nhóm |
| Learning curve cho thấy quá khớp ở đâu | PARTIAL | Có curves/raw fold/loss/validation; không có kết luận nhóm xác nhận, không tự bịa một mốc quá khớp |
| So chi phí và độ chính xác mô hình đơn giản/mạng nơ-ron | PARTIAL | Có timing/bytes/metrics đúng nguồn; chưa có diễn giải trade-off của nhóm |

## Việc nhóm phải hoàn thiện trước nộp

1. Tự viết và xác nhận 6 nhận định EDA, nhật ký làm sạch; phân tích kết quả, lỗi, learning curve và giới hạn theo đúng số liệu.
2. Hoàn thành báo cáo PDF/DOCX và slide chính thức; đối chiếu tên model, metric, tập dữ liệu, run_id và hình với RESULTS_INDEX/canonical run.
3. Điền tên/đóng góp thật, xác nhận đăng ký đề tài và các yêu cầu với giảng viên; tập vấn đáp để mỗi người giải thích và sửa được code.
4. Nếu muốn tuyên bố chất lượng ảnh chụp, bổ sung bộ ảnh tự chụp có nhãn/nguồn; ghi cả ca sai. Không tối ưu lại model theo test/demo đã xem.

Không có cam kết điểm số. ready_to_submit vẫn false. Việc chưa kiểm chứng: BM06, thời hạn/đăng ký, nhóm 3–5/phân công, xác nhận nhận định và trình độ vấn đáp, máy/OS khác, ảnh camera.

## Lệnh đã kiểm chứng

```powershell
uv --cache-dir .uv-cache venv <review-venv> --python .venv/Scripts/python.exe
uv --cache-dir .uv-cache pip install --offline --link-mode=copy --python <review-python> -r requirements.txt
uv --cache-dir .uv-cache pip check --python <review-python>
<review-python> -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
<review-python> -X utf8 tests/run_notebook.py
<review-python> -m streamlit run app.py --server.headless true --server.address 127.0.0.1 --server.port 8502 --browser.gatherUsageStats false
```

Placeholder là interpreter của venv review; lệnh chạy trong checkout sạch. Không cần chạy lại notebook để mở demo. Cảnh báo TCP của kernel và bare-mode/ScriptRunContext của AppTest được giữ trong log, không phải lỗi test. Chỉ sửa code test, format xuất report và path hiển thị; không thêm tính năng app, không đổi dependency/model/seed/grid hoặc viết thay phân tích của nhóm.
