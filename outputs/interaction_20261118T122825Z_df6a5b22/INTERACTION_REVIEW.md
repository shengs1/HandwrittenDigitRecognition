# Kiểm tra tương tác và thông tin kỹ thuật

Ngày18/11/2026. Chỉ sửa UI; giữ các thay đổi responsive/polish local đã có. Không huấn luyện, chạy notebook, đổi artifact hoặc thêm dependency.

| Hạng mục | Bằng chứng | Kết quả |
|---|---|---|
| Nguyên nhân chồng chữ | [DOM trước sửa](diagnostics_before.json): caption19,6px, margin-bottom=-14px, wrapper5,6px, chồng code6px | Đã bỏ caption/repr khỏi technical; reset margin caption |
| Dropdown | [Trước](select_before.json), [sau](select_after.json): arrow40px vượt field35px →33,4px nằm trong field | CSS scoped, native giữ nguyên |
| Bấm chữ/khoảng giữa/mũi tên trên5 dropdown | [15 phép bấm và bàn phím](dropdown_checks.json) |15/15 mở; ArrowDown/Escape/Enter/Tab hoạt động |
| Bảng KNN/MLP/LR đổi theo lựa chọn | [DOM thật](technical_checks.json), [đối chiếu Pipeline](verification.json) | Cả3 bảng khớp Pipeline; không fit |
| Không che/cắt/chồng văn bản |6 phép đo technical, scroll dimensions các ô/p và khoảng cách nhóm | Không clipping/tràn ngang; min-height auto/overflow visible, gap≥18px |
| Màn hình chính compact | [12 phép đo đóng](layout_checks.json), innerWidth/innerHeight/scale/dpr/document/stMain |0px tràn dọc/ngang;10 phép empty/pred ở5 viewport,1 upload,1 đóng lại |
| Ảnh test/mẫu và xóa kết quả khi đổi model | [Test ID21](test_selection_checks.json), [nguồn ảnh](source_checks.json), unittest | Chạy đúng; ID lấy split đã lưu |
| Upload preview/prediction/lỗi | source_checks.json; ảnh10–12 | Harness dùng bytes fixture và app thật; không thử lại hộp chọn file OS |
| Toàn bộ unittest | [Log cuối](tests_final.log) |43/43 PASS,6,843s |
| Bảo toàn notebook/model/kết quả/fixture/tài liệu | [Trước](protected_before.json), [sau](protected_after.json), verification.json |94 SHA256 không đổi;8 hàm ngoài UI giữ nguyên AST |

Viewport desktop thực:1920×1080,1920×900,1536×864,1366×768,1280×720. Browser zoom100%: visualViewport.scale1, dpr≈1, CSS zoom1, transform none. Technical mở cho cuộn tự nhiên; kiểm thêm390×844 không tràn ngang. Screenshot fullPage=false; kích thước JPEG ghi trong verification.json (ảnh mobile390×843 do công cụ, innerHeight844).

Các thông số được đọc trực tiếp: KNN3/Uniform/minkowski/p2/StandardScaler; MLP64→32/relu/adam/alpha0.0001/early stopping/max_iter300/StandardScaler; LR C1/lbfgs/l2/max_iter3000/pixel thô. Bảng dữ liệu từ data_summary của run canonical. Những giá trị này là mô tả artifact hiện có, không phải hardcode của UI. Run ID/checksum và kết quả MNIST3/10 mỗi model vẫn nguyên trong metadata/notebook/README/tài liệu/artifact.

Ảnh test KNN id10 nhãn0→0,100%; id21 nhãn1→1. Mẫu Digits id7 nhãn7→7,100%. Upload MNIST7→3 với33,33% (đồng hạng3/5/8), giữ kết quả thật. File hỏng báo lỗi và khóa nút; không có prediction cũ. Harness mock return của native uploader, không mô phỏng hộp chọn file Windows; không đưa harness vào ứng dụng.

Lần test đầu có lỗi test mới lọc cả style tag chứa technical-info và lỗi socket môi trường WinError10055. Đã sửa bộ lọc chỉ nhận div nội dung (giữ assertion toàn bộ HTML); chạy lại có quyền loopback thì43 test qua. [Log ban đầu](tests_initial.log) được giữ. Không giảm kiểm tra cũ.

Lệnh:

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.venv/Scripts/python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8510 --server.headless true --browser.gatherUsageStats false
.venv/Scripts/python.exe -X utf8 tmp/verify_interaction.py
git diff --check
```

Script verify và harness trong tmp bị ignore; JSON/log và ảnh ở đây là bằng chứng lưu dài hạn. Server thử đã dừng; viewport trả mặc định. Không commit/push trong lượt này.

Ảnh viewport:

- [Technical KNN1366×768](02_technical_knn_1366x768.jpg), [MLP](14_technical_mlp_final_1366x768.jpg), [Logistic Regression](04_technical_logreg_1366x768.jpg).
- [Technical KNN1920×900](07_technical_knn_1920x900.jpg), [mobile](08_technical_mobile_390x844.jpg).
- [Empty1366×768](05_empty_1366x768.jpg), [prediction](06_prediction_1366x768.jpg).
- [Empty1920×900](05_empty_1920x900.jpg), [prediction](06_prediction_1920x900.jpg).
- [Mẫu Digits](09_sample_prediction_1366x768.jpg), [test ID21](13_test_id21_1366x768.jpg).
- [Upload preview](10_upload_preview_1366x768.jpg), [prediction](11_upload_prediction_1366x768.jpg), [file lỗi](12_upload_invalid_1366x768.jpg).
