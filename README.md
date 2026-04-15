# LaTextoPic

LaTextoPic là một WebApp Python/Streamlit giúp biên dịch mã TikZ thành ảnh PNG và PDF tự động.

## Tính năng hiện tại

- Nhập / dán mã TikZ trực tiếp
- Xuất PNG và PDF
- Chọn chế độ PNG: `Nền trắng` hoặc `Nền trong suốt`
- Quyền đặt tên file tải xuống theo giờ Việt Nam `VN`
- Xóa mã nhanh bằng nút `🗑️ Xóa mã`
- Hỗ trợ nhiều khối `tikzpicture` trên cùng 1 trang

## Cài đặt

1. Mở Terminal tại thư mục `LaTextoPic`
2. Cài Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Cài thêm hệ thống LaTeX và Poppler nếu cần:

- Windows: cài TeX Live / MiKTeX và Poppler for Windows
- Linux: cài `texlive-latex-base`, `poppler-utils`

## Chạy app

```powershell
cd LaTextoPic
python -m streamlit run app.py
```

## File quan trọng

- `app.py`: giao diện Streamlit và logic UI
- `core/compiler.py`: engine chuyển TikZ -> PDF -> PNG
- `requirements.txt`: thư viện Python cần cài
- `packages.txt`: gói hệ thống cần cài trên môi trường server
- `.github/workflows/python-app.yml`: workflow GitHub Actions
- `tests/test_compiler.py`: unit test cho công cụ biên dịch TikZ

## Documentation

### Hướng dẫn sử dụng

1. Mở Terminal tại thư mục `LaTextoPic`
2. Cài dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Khởi động ứng dụng:

```powershell
python -m streamlit run app.py
```

4. Nhập hoặc dán mã TikZ vào ô input.
5. Chọn `Nền trắng` hoặc `Nền trong suốt`.
6. Nhấn `🚀 Render Ảnh Lập Tức` để tạo PNG/PDF.
7. Tải file về bằng hai nút download.

### Cách dùng nhiều khối TikZ cùng lúc

Nếu bạn muốn xuất nhiều hình vào cùng một trang, hãy dán các khối `\begin{tikzpicture}...\end{tikzpicture}` liên tiếp trong ô code. App sẽ biên dịch chúng vào cùng một file PDF và PNG.

### Kiểm tra và phát triển

- Chạy test bằng `pytest`:

```powershell
pytest -q
```

- Nếu bạn muốn thêm tính năng, hãy chỉnh file `app.py` và `core/compiler.py`.

## Lời khuyên khi deploy

- Đảm bảo `pdflatex` và `pdftocairo` có sẵn trên máy chủ.
- Với Streamlit Cloud, `packages.txt` sẽ tự cài Poppler và TeX Live.
- Nếu deploy trên server khác, hãy kiểm tra trước bằng `python -m streamlit run app.py`.

## How to deploy to Streamlit Cloud

1. Đăng nhập vào Streamlit Cloud bằng tài khoản GitHub hoặc email.
2. Tạo một repository GitHub mới chứa toàn bộ thư mục `LaTextoPic`.
3. Đẩy code lên repository; đảm bảo có `app.py`, `requirements.txt`, `packages.txt`, và `.github/workflows`.
4. Trong Streamlit Cloud, chọn "New app" và kết nối đến repository chứa `LaTextoPic`.
5. Chọn branch và đặt `Main file` là `LaTextoPic/app.py`.
6. Nếu cần, thêm `packages.txt` vào danh sách cấu hình build để cài TeX Live và Poppler tự động.
7. Khởi chạy app. Nếu build lỗi do thiếu package, xem log và bổ sung package tương ứng trong `packages.txt`.

> Lưu ý: Streamlit Cloud có thể yêu cầu thời gian build lâu hơn vì phải cài LaTeX và Poppler. Nếu gặp lỗi tài nguyên, cân nhắc dùng server riêng hoặc dịch vụ cloud hỗ trợ hệ thống LaTeX đầy đủ.

## Optional: Deploy bằng Docker

Nếu bạn muốn host app trên một server riêng hoặc dịch vụ container, `LaTextoPic/Dockerfile` đã sẵn sàng để sử dụng.

1. Mở terminal tại thư mục `LaTextoPic`.
2. Build image:

```bash
docker build -t latextopic .
```

3. Chạy container:

```bash
docker run -p 8501:8501 latextopic
```

4. Mở trình duyệt tới `http://localhost:8501`.

> Tệp `Procfile` cũng đã được tạo để hỗ trợ các nền tảng deploy container/Platform-as-a-Service.

## PWA và cập nhật phiên bản

- PWA sẽ tự cập nhật khi người dùng mở lại trang hoặc refresh lại app.
- Khi có phiên bản mới, bạn nên hiện thông báo rõ ràng như:
  - “Có phiên bản mới, vui lòng tải lại.”
  - Người dùng nhấn `Reload` hoặc `F5` để lấy nội dung mới.
- Nếu app được thêm vào màn hình chính, cách đơn giản nhất là đóng app rồi mở lại hoặc kéo xuống để refresh.
- Để tránh giữ cache cũ, nên thiết kế `service worker` với cơ chế cập nhật: `skipWaiting()` và `clients.claim()`.

> Cách nhanh nhất để tải bản mới: refresh trang/app. Nếu vẫn thấy nội dung cũ, xóa cache trình duyệt hoặc mở lại app.

## Tiếp theo

Các bước hoàn thiện tiếp theo có thể là:

1. Thêm `LICENSE`
2. Thêm `GitHub Actions` cho lint/test
3. Thêm `tests/` cho `compiler.py`
4. Cải thiện thông báo lỗi nếu thiếu `pdflatex` hoặc `poppler`
