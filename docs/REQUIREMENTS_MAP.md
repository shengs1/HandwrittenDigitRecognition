# Đối chiếu yêu cầu và tiến độ — đề tài 13

Cập nhật 23/11/2026. Nguồn: [PDF học phần](Huong_Dan_Do_An_CuoiKy.pdf). Phần A là Digits; phần B mở rộng MNIST/ảnh ngoài không thay yêu cầu chính. [Final review](FINAL_REVIEW.md) ghi bằng chứng kiểm tra.

| Yêu cầu | Hiện có | Nhóm cần hoàn thiện |
|---|---|---|
| Bài toán, mục tiêu, baseline | Notebook 1/6: phân lớp 0–9, Logistic Regression thô, chọn macro F1 kiểm định chéo | Xác nhận mục tiêu và giải thích độ đo |
| Nguồn, schema, thiếu theo cột | Notebook 2: 1.797×64, X float64/y int64, 65 cột gồm nhãn thiếu 0% | Trích bảng và nguồn vào báo cáo |
| Làm sạch có lý do | Không sai miền/trùng/hằng; giữ ba ảnh IQR, có nhật ký dự thảo | Nhóm xác nhận quyết định |
| EDA≥5, có nhãn/nhận định | Sáu hình trên train và nhận định dự thảo | Rà soát, xác nhận và chèn hình |
| Đặc trưng không rò rỉ | Scaler trong Pipeline theo fold; PCA chỉ train/EDA | Giải thích validation nội bộ MLP |
| Baseline+ít nhất hai model | Logistic Regression, KNN, MLP; run chính đã lưu | Hiểu cấu hình và API, không buộc MLP thắng |
| Chia dữ liệu/CV/tuning | 1.437/360, stratify/42; 5 folds shuffle/42; grid chỉ train; khóa trước test | Không chọn lại theo test; nêu thiên lệch CV sau tuning |
| Độ đo, lỗi, curves, chi phí | Accuracy, precision/recall/F1 macro, report/confusion/ảnh sai/curves/timing/bytes | Xác nhận phân tích có căn cứ |
| Demo tùy chọn | Streamlit, bốn Pipeline, ba nguồn ảnh, không train lúc mở | Thử ảnh tự chụp và tập demo/vấn đáp |
| Tái lập/môi trường sạch | Requirements ghim; venv mới và 53 tests đã kiểm 19/11; 53 tests giao diện 21/11 | Chạy đúng README, không đóng gói venv/cache |
| Báo cáo 10 mục PDF/DOCX | REPORT_OUTLINE và RESULTS_INDEX có nội dung/nguồn | Chưa xác nhận có bản nộp chính thức |
| Slide, nhóm, phân công, vấn đáp | 12 slide dự thảo, bộ câu hỏi, chưa điền thành viên | Thông tin thật, bản xuất, khả năng giải thích của từng người |

## Năm câu hỏi đề tài 13

| Câu hỏi | Bằng chứng phần A | Giới hạn |
|---|---|---|
| Vector/shape, vì sao chuẩn hóa? | 8×8→64, miền 0–16; MLP scaling CV F1 94,3452%→96,2365% | PCA chỉ EDA, scaler fit train; MNIST 28×28→784 là model khác |
| Baseline và MLP cải thiện? | LR test 95,8333%, MLP 96,1111%; CV MLP thấp hơn LR | +0,2778 điểm phần trăm trên một split, không chứng minh MLP luôn tốt hơn |
| Cặp chữ số nhầm? | 8→1 nhiều nhất LR/KNN/MLP:4/3/3; KNN 4→7 hai lần | Hướng thật→dự đoán; không đổi nhãn/xóa ảnh |
| Learning curve và quá khớp? | Gap cuối 3,70/1,15/3,11 điểm; MLP 52 iterations | Chưa xác định epoch quá khớp; loss và accuracy khác đơn vị |
| Chi phí so độ chính xác? | Fit cuối, predict median5, tuning riêng, bytes; KNN thắng CV | Cùng máy/một luồng; không so trực tiếp với batch predict+proba hai luồng phần B |

## Phần mở rộng và giới hạn nộp bài

600 ảnh gốc, seed42, chia 300 xác thực/300 kiểm tra; không dùng train. Gray_bbox chọn bằng validation; MLP MNIST học54k/6k, loại110 test cũ, khóa trước 9.890 MNIST và300 test ngoài. KNN ngoài48%→58%; MLP MNIST97,3913% trên9.890 và87,3333% trên300, F1 ngoài0,871326. Không gộp độ chính xác các tập. Nguồn/giấy phép và giới hạn người viết/Bitmap/ảnh điện thoại ở README và RESULTS_INDEX.

Điểm PDF: dữ liệu/EDA/chuẩn bị4; mô hình/đánh giá4; trình bày/vấn đáp2. Checklist kỹ thuật không bảo đảm điểm hoặc khả năng bảo vệ. Nhận định, thông tin/phân công và bản nộp vẫn cần nhóm hoàn thiện. Mục6 PDF không thuộc phạm vi audit theo quyết định đã ghi trong AGENTS; giữ nguyên PDF gốc.

Notebook có16 mục,51 cell,23 cell code. Mục1–5 chuẩn bị/EDA; 6–14 định nghĩa phương pháp; 15 khóa rồi đánh giá; 16 lưu kết quả. `run_status.json` là snapshot lúc huấn luyện, không phải xác nhận tiến độ hôm nay; không rerun notebook chỉ để cập nhật ngày/trạng thái tài liệu.
