# Dự thảo báo cáo — đúng 10 mục của PDF

**Chưa được nhóm xác nhận; chưa phải bản nộp PDF/DOCX.** Các đoạn dưới để nhóm kiểm tra, sửa và sử dụng. PhầnA chính: Digits run `20261117T081201Z_fd32180f`; phầnB mở rộng: `external_optimization_20261118T175401Z_4ca3a08f`. [RESULTS_INDEX](RESULTS_INDEX.md) có bảng/hình nguồn cho cả hai phần. UI/CODE/EXPERIMENTS FROZEN, tài liệu/thuyết trình đang hoàn thiện. Giữ đúng10 mục dưới, phân biệt A/B trong từng mục; không lấy log kiểm thử làm điểm mô hình.

## 1. Trang bìa

Đề tài 13: **Phân loại chữ số viết tay bằng Digits**. Học phần Lập trình cho Trí tuệ nhân tạo và Khoa học dữ liệu (04224), học kỳ I năm học 2026–2027 theo PDF.

| Thông tin | Nội dung nhóm cần điền |
|---|---|
| Tên nhóm / lớp | [Chưa cung cấp] |
| Họ tên / MSSV từng thành viên | [Chưa cung cấp] |
| Giảng viên | [Chưa cung cấp] |
| Ngày nộp | [Chưa xác nhận lịch] |

## 2. Giới thiệu bài toán và mục tiêu

Bài toán phân lớp có giám sát nhận một ảnh và dự đoán nhãn0–9. PhầnA dùng Digits8×8, so LR pixel thô với KNN/MLP, kiểm tra chuẩn hóa, phân tích lỗi và chi phí. PhầnB giữ nguyên ba Pipeline Digits, so preprocessing upload và huấn luyện riêng một MLP MNIST28 để đánh giá giới hạn ảnh ngoài; không thay dataset hoặc mô hình chính của phầnA.

Chọn macro F1 trung bình CV cao nhất, hòa tuyệt đối theo tên tăng dần, trước khi xem test. Macro F1 cho mỗi chữ số vai trò ngang nhau, kết hợp precision/recall; accuracy bổ sung tỷ lệ dự đoán đúng dễ hiểu. Thành công còn gồm tái lập và không rò rỉ, không buộc mạng nơ-ron phải thắng. Phạm vi đã kiểm chứng là ảnh giống Digits, chưa đủ bằng chứng cho ảnh điện thoại.

## 3. Dữ liệu và làm sạch

`load_digits()` có 1.797 ảnh 8×8; X=(1797,64) float64, y=(1797,) int64. Pixel thực tế nguyên trong 0–16, nhãn 0–9. Nguồn scikit-learn/UCI được ghi ở notebook mục 2 và dataset_description.txt. 64 pixel và nhãn đều thiếu 0%; không sai miền, ảnh hằng, ảnh trùng chính xác hoặc nhãn mâu thuẫn. Giữ toàn bộ dữ liệu, không thêm imputer khi không missing.

Ba ảnh train id 1747/818/1766 vượt IQR độ sáng (mean 6,671875/6,765625/6,546875). Khi xem trực tiếp, chúng là số 1 nét dày, có 36/39/39 pixel khác 0, không hằng hoặc sai miền. Cờ thống kê không đủ lý do loại; run giữ cả ba. Nhóm cần kiểm tra/xác nhận nhật ký mục 3 notebook, không xem quyết định này là đã được nhóm thông qua.

Chia 1.437 train/360 test, stratify=y, seed=42. Không có ảnh trùng chính xác xuyên train/test hay trong 5 folds. Chèn bảng schema/tỷ lệ thiếu và nhật ký; dẫn data_quality.json, train_image_diagnostics.csv, split_indices.csv, cv_fold_audit.csv trong RESULTS_INDEX.

PhầnB:600 ảnh gốc từ3 nguồn,seed42,300 validation/300 test cân bằng. Chỉ10 ảnh/lớp/nguồn/split, không dùng để train. MNIST train60000 chia54000/6000 stratify/42; loại110 test đã xem trước khi đánh giá9890 còn lại. Ghi license/nguồn/manifest và giới hạn writer/Bitmap; không gọi scan/ảnh giấy đã cắt/ảnh vẽ số là ảnh điện thoại nguyên bản.

## 4. Khám phá và trực quan hóa

Chèn đủ 6 hình train EDA 01–06, giữ tiêu đề/trục/thang màu; mỗi hình dùng nhận định dự thảo mục 5 notebook và chú thích trong RESULTS_INDEX:

1. Lớp gần cân bằng, 139–146 mẫu; lớp 8 ít nhất, 1/3 nhiều nhất.
2. Reshape 64 pixel theo hàng; nét nghiêng/dày/mỏng khác nhau, độ phân giải thấp mất chi tiết.
3. 48,86% pixel train bằng 0: nền hợp lệ, không phải missing.
4. Trung bình lớp 0 còn vùng giữa rỗng, lớp 1 nét dọc; trung bình làm mờ khác biệt vị trí.
5. Std lớn nhất 6,5311 ở hàng 5/cột 2; giữ các vị trí hằng, std không phải tầm quan trọng dự đoán.
6. PCA 2D giữ 28,5019% phương sai; nhiều lớp chồng lấn. Không suy ra accuracy mô hình 64 chiều từ hình chiếu.

PCA chỉ fit train để EDA, không nằm trong model. Nhóm cần xem lại hình và xác nhận các quan sát trực quan.

## 5. Phương pháp (đặc trưng, mô hình, cách đánh giá)

LR baseline: passthrough → LogisticRegression(C=1, lbfgs, max_iter=3000). Thô là đối chứng theo đề tài, không phải khẳng định LR không cần scaler. KNN/MLP dùng StandardScaler → estimator. MLP ban đầu (64,32), relu/adam, early_stopping=True, seed 42, max_iter300.

StratifiedKFold(5, shuffle=True, random_state=42). KNN grid k={3,5,7}, weights={uniform, distance}; MLP hidden={(64,),(64,32)}, alpha={0.0001,0.001}. GridSearchCV scoring=f1_macro, refit=False, n_jobs=1 trên train. Đối chứng scaling cùng MLP/folds/seed. Chọn theo CV, lưu selection_lock rồi mới predict test; CV sau lựa chọn có thiên lệch.

Scaler fit train fold trước khi MLP chia validation nội bộ, nên thấy đặc trưng của phần nội bộ này nhưng không thấy outer validation/test. Early stopping theo accuracy nội bộ, khác CV macro F1. Đo fit cuối bằng clone một lần, predict median 5 lần sau warm-up cùng test, một luồng; tuning và bytes joblib nén mức 3 đo riêng.

PhầnB:7 preprocessing cố định, chọn gray_bbox theo mean macro F1 trên validation300, tăng≥0,02 và KNN F1 không giảm. Một MLP MNIST28 MinMaxScaler→(128,64),relu/adam,alpha0,0001,early stopping; validation ngoài6000 và nội bộ5400 khác nhau. Khóa model/module/lựa chọn trước hai tập test; không chọn theo xác suất mỗi ảnh. Chi phí mở rộng là một batch predict+proba/2 luồng, không đồng nhất cách đo với phầnA.

## 6. Kết quả và so sánh với baseline

Chèn bảng đầy đủ RESULTS_INDEX mục 2–5: precision/recall/F1, CV mean/std, cấu hình, scaling và chi phí. Tóm tắt:

| Mô hình | CV macro F1 mean ± std (%) | Accuracy test (%) | Macro F1 test (%) |
|---|---:|---:|---:|
| LR thô | 96,3687 ± 0,7866 | 95,8333 | 95,8075 |
| KNN | **97,6170 ± 0,7575** | 96,6667 | 96,6304 |
| MLP | 96,2365 ± 0,8314 | 96,1111 | 96,0888 |

KNN được chọn trước test (k=3/uniform/StandardScaler). MLP hơn LR 0,2778 điểm phần trăm accuracy test và 0,2813 điểm phần trăm F1 test, nhưng CV mean thấp hơn LR 0,1322 điểm phần trăm. Chênh lệch nhỏ trên một split chưa chứng minh MLP cải thiện chắc chắn; KNN không nhất thiết luôn tốt hơn.

MLP StandardScaler có CV F1 94,3452%→ 96,2365%: +1,8913 điểm phần trăm, khoảng 2,00% tương đối; std 1,8458→ 0,8314 điểm phần trăm. Đây không phải accuracy test.

KNN fit nhanh nhất (0,003107 s), predict chậm nhất (0,004730 s/360 ảnh). LR predict nhanh nhất (0,000798 s), nhỏ nhất (5.935 byte). MLP fit 0,279319 s, tuning 4,231378 s, chưa có lợi thế điểm số. Baseline tuning=0 vẫn có CV. Timing cùng máy/một luồng và fit một lần không bảo đảm thứ hạng tốc độ trên mọi máy/dataset.

PhầnB chèn bảng7 hệ thống từ RESULTS_INDEX mục11, báo riêng MNIST9890 và ngoài300. MLP28 đúng9632/9890 (97,3913%,F1 0,973773),262/300 (87,3333%,F1 0,871326); BHMSDS82/100,Bitmap82/100,HwD98/100. KNN cũ48%→gray_bbox58% trên cùng300 ảnh. MLP28 fit23,895571s,30 iterations,1221502byte. Không dùng score mới thay KNN CV/Digits và không gộp accuracy các dataset.

## 7. Phân tích lỗi và giới hạn

Chèn 3 confusion matrices, bảng cặp có hướng, vài ảnh sai, learning curve và MLP history. LR/KNN/MLP sai 15/12/14 ảnh; 8→ 1 nhiều nhất ở cả ba (4/3/3), KNN còn 4→ 7 hai lần. Ảnh 1553 (8→ 1) nét dọc nổi bật/vòng dưới kém rõ; 1022 (4→ 7) có nét ngang/chéo rõ; 1100 (9→ 8) vùng dưới có nét cong. Đây là giả thuyết trực quan, không chứng minh nguyên nhân quyết định của model. Không sửa nhãn hay xóa ảnh khó.

Tăng train/fold 229→ 1.149, validation F1 tăng cả ba. Gap cuối LR/KNN/MLP là 3,70/1,15/3,11 điểm phần trăm. LR train 100% nhưng validation96,30% cho thấy khoảng cách tổng quát hóa, chưa đủ gọi quá khớp nghiêm trọng. MLP ít mẫu dao động hơn. MLP cuối chạy 52 iterations, loss2,3952→ 0,0208, best/cuối accuracy validation nội bộ97,9167%. Validation bão hòa; chưa xác định chính xác epoch quá khớp. Loss và accuracy khác đơn vị.

Giới hạn: dataset nhỏ/8×8, chia ngẫu nhiên chưa bảo đảm tách người viết, CV có thiên lệch lựa chọn, xác suất chưa hiệu chỉnh. Mỗi model đúng 3/10 MNIST đã thử; 10 mẫu không đại diện ảnh ngoài và không dùng tuning. Chưa có ảnh tự chụp nhóm. Hướng sau: thu ảnh thật có nhãn, chốt quy trình trước và dùng tập ngoài mới độc lập; không đổi run hiện tại theo test.

PhầnB chèn confusion theo nguồn/chữ số và ảnh lỗi trước/sau; giữ38 ảnh sai. Thống kê train/validation cho thấy khác độ sáng/tỷ lệ nét/vị trí,8×8 có thể mất chi tiết; đây là mô tả và giả thuyết, chưa tách hiệu ứng nhân quả. MLP28 đổi cả dữ liệu/lượng mẫu/kiến trúc/resolution. Test độc lập với bước lựa chọn ở mức ảnh, **chưa xác nhận độc lập người viết**, chưa có ảnh tự chụp. Bitmap chưa khôi phục được mapping từng ảnh upstream. Không dùng38 lỗi hoặc9890 test để tuning tiếp.

## 8. Triển khai (tùy chọn)

Streamlit tiếng Việt chỉ load Pipeline qua registry/checksum, không fit. Hai nguồn Digits dùng3 model chính/pixel gốc. Upload dùng gray_bbox8×8/0–16 cho model Digits hoặc lựa chọn rõ MLP — MNIST (ảnh ngoài),mnist28/0–255/784 đặc trưng. Flatten theo hàng, scaler chỉ trong Pipeline. Ba thẻ thống kê vẫn là Digits, không tự chọn model theo confidence.

Giao diện có ảnh gốc/preview đúng8×8 hoặc28×28, dự đoán và xác suất10 lớp chưa hiệu chỉnh. File trống/hỏng/quá lớn, thiếu registry/model/split báo lỗi, không tự train. Chèn screenshot/53 unittest venv mới và ma trận14 chức năng+8 lỗi model ở lần freeze. Giữ baseline ảnh cũ để đối chứng; upload mới được chọn bằng validation riêng, không điều chỉnh từ10 MNIST cũ hay test đã xem.

## 9. Kết luận

Đồ án có quy trình tái lập, 6 EDA, baseline và hai model Pipeline, scaling/CV/grid/lỗi/curves/demo. KNN được chọn bằng CV F1 97,6170%, accuracy test 96,6667%. LR nhẹ/nhanh khi predict; MLP chưa có lợi thế tổng thể. Chuẩn hóa giúp MLP trong đối chứng CV. Lỗi8→ 1 đáng chú ý; ảnh ngoài còn hạn chế, không cam kết mọi ảnh thực tế. Chưa xác định epoch quá khớp chính xác. Đối chiếu 5 câu trả lời cuối notebook trước chốt.

PhầnB cải thiện nhận diện trong các tập ngoài đã kiểm bằng gray_bbox và MLP MNIST28; không thay kết luận chọn KNN của phầnA. Giữ bản tối ưu đã duyệt, không tiếp tục tuning; nhóm xác nhận diễn giải và kiểm ảnh tự chụp bằng app theo README trước buổi bảo vệ.

## 10. Phân công công việc, tài liệu tham khảo; phụ lục

| Thành viên / MSSV | Công việc thực tế | Bằng chứng (commit/cell/tài liệu) | Xác nhận |
|---|---|---|---|
| [Chưa cung cấp] | [Nhóm tự điền việc đã làm] | [Chưa cung cấp] | [Chưa xác nhận] |

Tham khảo: [PDF học phần](Huong_Dan_Do_An_CuoiKy.pdf); [scikit-learn load_digits](https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_digits.html); [UCI Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits); API Pipeline/MLP trong notebook; Streamlit/Pillow theo requirements; [nguồn MNIST fixture](../tests/fixtures/external_digits/README.md). Phụ lục: phiên bản/seed/grid/run_id/checksum, CV/report/CSV/hình và lệnh từ README/HANDOFF. Không có BM06 để suy đoán thêm thang điểm.

Trước xuất PDF/DOCX: nhóm đọc/sửa/xác nhận dự thảo, điền thông tin thật, chèn hình đủ lớn có nguồn/chú thích, kiểm tra trang và số liệu, hoàn thành phân công và tập bảo vệ. Bản Markdown này chưa thay sản phẩm nộp.
