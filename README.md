# Phân loại chữ số viết tay — đề tài 13

Repository GitHub: [shengs1/HandwrittenDigitRecognition](https://github.com/shengs1/HandwrittenDigitRecognition). Trạng thái liên kết Git cục bộ và đồng bộ mã nguồn được ghi trong `HANDOFF.md`.

Khung hỗ trợ đồ án học phần Lập trình cho Trí tuệ nhân tạo và Khoa học dữ liệu. Dataset duy nhất: `sklearn.datasets.load_digits()`. Tài liệu gốc: [hướng dẫn đồ án](docs/Huong_Dan_Do_An_CuoiKy.pdf). Đã đọc đủ 6 trang; đối chiếu yêu cầu tại [REQUIREMENTS_MAP.md](docs/REQUIREMENTS_MAP.md).

**Chưa phải bài nộp hoàn chỉnh.** Notebook mặc định chạy phần hỗ trợ: đọc/kiểm tra dữ liệu, chia train/test, kiểm tra trùng xuyên tập/CV và 6 hình EDA trên train. Các phần SV-01…SV-09 thuộc nhóm sinh viên; chưa có điểm accuracy/F1, mô hình đã fit hoặc kết luận thực nghiệm. Chạy hết khung không đồng nghĩa hoàn thành thực nghiệm.

## Cài đặt và chạy trên Windows PowerShell

Cần Python 3.12+ hoạt động (đã kiểm thử bằng Python 3.12). Chạy từ thư mục project:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m notebook digit_classification.ipynb
```

Nếu `py`/`python` trỏ tới alias Microsoft Store không hoạt động, dùng đường dẫn Python đã cài thay cho `py -3.12`. Không cần activate và không cần đổi ExecutionPolicy. Chọn kernel của `.venv`, Restart Kernel rồi Run All.

Môi trường của phiên Codex hiện tại được tạo bằng `uv venv` từ Python đóng gói; `.venv` không mang sang máy khác. `requirements.txt` ghim phiên bản trực tiếp đã dùng; phiên bản cả SciPy/threadpoolctl được ghi thêm để giữ hành vi tính toán. Mỗi run lưu thông tin môi trường thực tế trong `outputs/<run_id>/environment.json`.

## Kiểm tra khung hỗ trợ

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -p "test_*.py" -v
.\.venv\Scripts\python.exe -X utf8 tests/run_support_notebook.py
```

Lệnh thứ hai chạy notebook qua kernel thật, cập nhật output hiển thị trong notebook và ghi `support_verification.json` vào thư mục run mới. Script từ chối chạy nếu cờ thực nghiệm đã bật, để tránh vô tình fit mô hình. Phép kiểm tra này không xác minh các TODO cốt lõi chưa triển khai.

## Sinh viên tự triển khai

Đọc `AGENTS.md`, `HANDOFF.md` và mục 6 PDF trước khi tiếp tục. Điền nhật ký làm sạch, 6 nhận định EDA, mục tiêu/độ đo và phân công thật. Tự viết các TODO:

| TODO | Nội dung |
|---|---|
| SV-01 | Baseline Logistic Regression pixel thô |
| SV-02 | Pipeline KNN và MLP |
| SV-03 | Đối chứng MLP có/không chuẩn hóa, chỉ train/CV |
| SV-04 | CV, GridSearchCV và tổng hợp kết quả train |
| SV-05 | Độ đo và classification report |
| SV-06 | Ma trận nhầm lẫn, cặp nhầm, ảnh sai |
| SV-07 | Learning curve theo số mẫu |
| SV-08 | Loss và validation accuracy theo iteration MLP |
| SV-09 | Chọn mô hình theo CV đã định trước |

Notebook có hợp đồng đầu vào/đầu ra và API tham khảo cho từng TODO. Hoàn thành, kiểm thử và giải thích các hàm trước khi bật `RUN_STUDENT_EXPERIMENTS=True`; điền `CLEANING_DECISION` và `STUDENT_PROTOCOL_NOTE`. Không dùng test để điều chỉnh. Kết quả CV của cấu hình đã tuning có thiên lệch lựa chọn; không gọi đó là ước lượng độc lập.

## File và kết quả

```text
digit_classification.ipynb   tài liệu thực nghiệm chính (16 mục)
requirements.txt            phiên bản môi trường
AGENTS.md                   quy tắc cho Codex/Antigravity
HANDOFF.md                  trạng thái và bằng chứng kiểm tra
AI_USAGE.md                 khai báo hỗ trợ AI / đóng góp thật
models/                     Pipeline sau thực nghiệm thật
outputs/<run_id>/           dữ liệu kiểm tra, hình, kết quả thật
tests/                      kiểm tra hợp đồng và chạy khung
docs/                       PDF gốc và bản đối chiếu yêu cầu
```

Mỗi lần Run All tạo thư mục riêng, không ghi đè kết quả cũ. Phase hỗ trợ xuất schema/tỷ lệ thiếu từng cột, kiểm tra chất lượng, chỉ số split, kiểm tra CV, dữ liệu PCA và 6 hình EDA. Mục 16 chỉ xuất kết quả mô hình khi cốt lõi đã chạy thành công: bảng so sánh, CV/grid, đối chứng scaling, dự đoán test, report, confusion pairs, learning curve, MLP history, thời gian và toàn bộ Pipeline joblib. Giữ run_id cùng notebook/báo cáo; không trộn kết quả khác lần chạy. Đọc `run_status.json` trước khi sử dụng output. Thư mục support không có mô hình.

Chưa xây demo, báo cáo hoặc slide trong phase này. Nhóm tự hoàn thành các sản phẩm nộp và trả lời 5 câu hỏi định hướng. Không sửa tay số liệu trong output. Không tải file joblib từ nguồn không tin cậy.
