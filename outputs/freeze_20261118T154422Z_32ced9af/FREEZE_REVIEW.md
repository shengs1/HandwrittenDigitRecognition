# UI FROZEN — kiểm tra bản chính thức

Người dùng duyệt giao diện ngày18/11/2026. Không sửa source app/theme/tests/requirements trong lượt freeze. Không huấn luyện, tuning, chạy notebook, đổi preprocessing hoặc artifact.

| Kiểm tra | Kết quả và bằng chứng |
|---|---|
| Toàn bộ unittest | **43/43 PASS,9,618s** — [log](unittest.log) |
| Ma trận chức năng3 model ×3 nguồn | **9/9 PASS**, dự đoán/xác suất khớp Pipeline thật, đủ10 lớp — [AppTest](functional_matrix.json), [log](functional_matrix.log) |
| Xóa kết quả cũ | **15 tình huống PASS** trong AppTest: đổi model, nguồn, chữ số, ID, đổi/khôi phục bytes ảnh upload — functional_matrix.json |
| Trình duyệt thật | **9/9 tổ hợp**, đối chiếu nhãn và từng phần trăm đã làm tròn với Pipeline — [DOM](browser_matrix.json), [đối chiếu](verification.json) |
| Dropdown | **15/15** bấm chữ/khoảng giữa/mũi tên trên5 dropdown mở — [tọa độ và trạng thái](dropdown_checks.json); [bàn phím](keyboard_checks.json) |
| Technical | Cả3 model: bảng khớp tham số thật, không clipping/tràn ngang/chồng nhóm, min-height auto, overflow visible — [DOM](technical_checks.json) |
| Compact khi technical đóng | **10/10** empty/pred ở5 viewport:0px tràn dọc/ngang, zoom100% — [kích thước thực](layout_checks.json) |
| File ảnh hỏng | Thông báo rõ, nút khóa, không có prediction cũ — [DOM](browser_error.json) |
| Pipeline/artifact |3 SHA256 khớp registry;94 file bảo vệ trước/sau khớp; git diff rỗng với HEAD — [xác minh](verification.json), [trước](protected_before.json), [sau](protected_after.json) |
| UI/source đã duyệt | App/theme/tests/requirements không đổi so đầu lượt — [hash đóng băng](frozen_source.json) |
| Khởi chạy app | Streamlit health app8512/harness8513 trả HTTP200 — verification.json |

Actual viewport:1920×1080,1920×900,1536×864,1366×768,1280×720. ResetCtrl+0; scale1/dpr≈1. Screenshot fullPage=false, kích thước đúng viewport. Khi technical mở, cuộn tự nhiên; khi đóng giữ bố cục compact.

Lượt đo responsive đầu áp override vào tab upload đang active, tab app vẫn1366×768. Bản đó được giữ riêng [chẩn đoán thao tác công cụ](layout_initial_diagnostic.json), không dùng làm bằng chứng5 viewport. Đã mở lại app riêng cổng8514, xác nhận actual viewport đúng từng kích thước trước khi đo và chụp lại; layout_checks.json và screenshot hiện tại là kết quả đo lại. Không sửa source UI. Verification kiểm cả tập actual viewport và kích thước JPEG để tránh nhầm.

Upload được kiểm bằng AppTest và harness fixture giữ widget native, gọi đúng app.main/preprocess/Pipeline nhưng thay bytes trả về. **Không thử lại hộp chọn file Windows**; không coi harness là bằng chứng thao tác chọn file OS. Không thêm harness vào ứng dụng. Ảnh MNIST7: LR→7,91,26%; KNN→3,33,33% (đồng hạng3/5/8); MLP→7,94,19%. Đây là một fixture; kết quả10 MNIST chính thức3/10 mỗi model được giữ nguyên trong notebook/docs/artifact.

Không phát hiện lỗi chức năng cần sửa. Giới hạn ảnh ngoài vẫn còn; báo cáo/slide/phân công cần nhóm xác nhận và hoàn thiện. Các kiểm thử ở chế độ bare có cảnh báo ScriptRunContext, không phải test fail. HTTP health chạy cần quyền loopback; lần đầu sandbox chặn, lần có quyền đạt. Không thay app để vượt kiểm tra.

Lệnh thực tế:

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.venv/Scripts/python.exe -X utf8 tmp/check_frozen_demo.py
.venv/Scripts/python.exe -X utf8 tmp/verify_freeze.py
.venv/Scripts/python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8512 --server.headless true --browser.gatherUsageStats false
git fetch origin main
git diff --check
```

Scripts/harness tạm ở tmp bị ignore; các JSON/log ở đây lưu kết quả thực. Người dùng yêu cầu commit/push toàn bộ UI đã duyệt cùng bằng chứng; kết quả Git xem mục UI FROZEN trong HANDOFF.

Ảnh kiểm tra:

- [Technical MLP](02_technical_mlp_1366x768.jpg), [KNN](02_technical_knn_1366x768.jpg), [LR](02_technical_logreg_raw_1366x768.jpg).
- [Upload LR](03_upload_logreg_raw_1366x768.jpg), [KNN](03_upload_knn_1366x768.jpg), [MLP](03_upload_mlp_1366x768.jpg), [ảnh hỏng](04_invalid_upload_1366x768.jpg).
- [Empty1366×768](05_empty_1366x768.jpg), [prediction](06_prediction_1366x768.jpg).
- [Empty1920×900](05_empty_1920x900.jpg), [prediction](06_prediction_1920x900.jpg).
- [Ảnh mẫu Digits](01_digits_prediction_1366x768.jpg).
