# BÁO CÁO CÔNG VIỆC: HOÀN THIỆN KHO TÀI NGUYÊN MẪU TIKZ CHÍNH THỨC & Ý TƯỞNG CỖ MÁY LẮP RÁP TIKZ

## 1. MỤC TIÊU LÀM VIỆC

Xây dựng, tổng hợp và chuẩn hóa form trình bày cho bản chính thức của các mẫu hình vẽ không gian và đồ thị hàm số (Topology gốc). Đây là bước đệm quan trọng nằm trong dự án nhận diện và dựng ảnh tự động bằng TikZ (LA-TEX-TO-PIC).

## 2. CHI TIẾT CÁC HẠNG MỤC ĐÃ HOÀN THÀNH

**A. Tinh chỉnh bố cục và kích thước hiển thị:**

- Thu nhỏ tỷ lệ hiển thị (`scale=0.5` hoặc `scale=0.6`) cho các đồ thị: **F.2 (Bậc 3), F.3 (Trùng phương), F.4 (Nhất biến) và F.6 (Lũy thừa)** để hình ảnh gọn gàng, vừa vặn không bị rớt dòng và tràn lề biên PDF.
- Tái cấu trúc bố cục hiển thị cho **F.5 (Đồ thị hàm Sin)** và **G.5 (Bảng xét dấu 3 dòng)**: Chuyển từ định dạng chia cột ngang (trái - phải) sang định dạng xếp dọc khối (Hình vẽ căn giữa ở trên, Code gốc TikZ đặt trong `tcolorbox` ở dưới). Việc này giúp hình vẽ trải dài toàn bộ chiều rộng trang, hiển thị rõ ràng hơn.

**B. Cập nhật và bổ sung các mẫu hình học & đồ thị mới:**

- **C.3. Lăng trụ xiên tam giác**: Bổ sung cấu trúc hình lăng trụ xiên cơ bản với lưới ảo và lệnh tịnh tiến vector gọn gàng.
- **F.7. Đồ thị hàm số Mũ ($a^x$)**: Thể hiện nét đồ thị đặc trưng đi lên và đi xuống.
- **F.8. Đồ thị hàm số Logarit ($\log_a x$)**: Dựng trục tiệm cận đứng, thể hiện đặc tính logarit chuẩn.
- **Nhóm đồ thị lượng giác còn thiếu** (áp dụng bố cục xếp dọc cấu trúc center-codebox giống hàm Sin):
  - **F.9. Đồ thị hàm lượng giác (Cosin)**
  - **F.10. Đồ thị hàm lượng giác (Tan)**: Xử lý ngắt đoạn đồ thị ở các điểm $x = \pm \frac{\pi}{2}, \pm \frac{3\pi}{2}$ và vẽ đường tiệm cận đứng bằng nét đứt đỏ.
  - **F.11. Đồ thị hàm lượng giác (Cotan)**: Tương tự như hàm Tan nhưng với tiệm cận đứng tại các điểm $x = k\pi$.

**C. Khắc phục sự cố và kiểm thử biên dịch:**

- Sửa các lỗi biên dịch phát sinh (thiếu dấu ngoặc, lỗi formatting nối string qua script) trong các khối mã lệnh mới chèn.
- Đảm bảo biên dịch thành công tuyệt đối qua lệnh `pdflatex -interaction=nonstopmode KhoMau_LaTextoPic_Official.tex`.
- Hoàn thành xuất bản file **`KhoMau_LaTextoPic_Official.pdf`** với dữ liệu đầy đủ 10 trang trang in, các topology chuẩn xác.

---

## 3. Ý TƯỞNG ĐỀ XUẤT: "CỖ MÁY LẮP RÁP TIKZ" BẰNG GIAO DIỆN (GUI) WEB APP

Sau phiên làm việc hôm nay, chúng ta đã có một cơ sở dữ liệu cốt lõi (Kho mẫu Base Topology chuẩn mực). Sự đồng bộ này mở ra một khái niệm mạnh mẽ hơn việc người dùng phải "copy-paste mã lệnh": **Xây dựng một "Cỗ máy lắp ráp TikZ"**.

**Phương thức hoạt động đề xuất:**

1. **Giao diện trực quan (Visual Selection):** Giáo viên chỉ cần truy cập vào Web App (như ứng dụng LaTextoPic đã triển khai PWA) -> Nhấp chuột vào hình mẫu mong muốn trên màn hình (Ví dụ: Chóp tứ giác đáy là hình vuông, SA $\perp$ đáy).
2. **Bảng điều khiển thông số (Parameters Form):** Form sẽ tự động hiện ra các trường điền (Inputs) thân thiện:
   - Tên các đỉnh (mặc định S, A, B, C, D).
   - Kí hiệu thêm cho góc vuông hay góc cắt.
   - Tỷ lệ chiều cao đồ thị...
3. **Trình lắp ráp động (Code Injector Maker):** Hệ thống Backend Python sẽ tiếp nhận các Param này, nhét trở lại (Inject) vào base template của hình tương ứng trong kho `KhoMau_LaTextoPic_Official.tex`.
4. **Vẽ theo giời gian thực (Live Render):** Trình tự động dịch mã `pdflatex` xử lý ngầm, và trả ngay về màn hình một tấm ảnh vector đẹp mắt cùng đoạn code đã cá nhân hóa.

**Lợi ích chiến lược đột phá:**

- **Giải phóng sự chán nản:** Giáo viên Toán/Lý không cần học sâu về cú pháp dài dòng của thư viện `tkz-euclide` hay `pgfplots`. Không lo sợ lỗi quên chấm phẩy hay dấu ngoặc nhọn.
- **Tiêu chuẩn hoá ngân hàng đề thi:** Toàn bộ khối hình học không gian và đồ thị hàm số giải tích sinh ra sẽ đồng nhất 100% về kích cỡ, loại nét đứt/liền, độ dày đường kẻ và font toán học.
- Đây sẽ là một "phễu gom người dùng" cực lớn cho dự án DataLatexMath2Q vì công cụ này giải quyết chính xác rào cản số 1 của người dùng gõ LaTeX: Vẽ hình không gian và đồ thị.

## 4. ĐÁNH GIÁ ỨNG DỤNG HIỆN TẠI

### 4.1. Ưu điểm

- Ứng dụng đã có workflow rõ ràng: nhập mã TikZ, biên dịch, hiển thị và tải PDF/PNG.
- Generator đã bước đầu tạo được template tự động, giúp giảm bớt thao tác copy-paste mã TikZ thô.
- Cấu trúc mã hiện tại đủ sạch để mở rộng thêm mẫu và tính năng.

### 4.2. Hạn chế cần khắc phục

- Thư viện template hiện chưa đủ phong phú so với kho mẫu chính thức.
- Tab `Pic-to-Text` chưa có chức năng thực tế, chỉ là placeholder.
- Chưa có tính năng lưu template hoặc tái sử dụng cấu hình từng mẫu.
- Chưa có hướng dẫn tương tác cho học sinh như hiển thị công thức, điểm đặc biệt, hay lời giải mẫu.

## 5. ĐỀ XUẤT HOÀN THIỆN APP

### 5.1. Mở rộng thư viện template

- Kéo thêm các mẫu hình học không gian và đồ thị từ `KhoMau_LaTextoPic_Official.tex` vào `LaTextoPic/app.py`.
- Nhóm template theo `Hình học không gian`, `Hình học phẳng`, `Đồ thị hàm số`, `Bảng biến thiên`.

### 5.2. Tăng cường tính năng generator

- Thêm tùy chọn `grid`, `labels`, `annotations`, `asymptotes` cho đồ thị.
- Cung cấp các checkbox để học sinh/giáo viên có thể bật tắt nhanh các yếu tố bổ sung.

### 5.3. Bổ sung quản lý template

- Thêm chức năng `Save template` / `Load template` lưu ở JSON.
- Cho phép đánh dấu template yêu thích và lưu lại cấu hình tham số.

### 5.4. Phát triển Pic-to-Text

- Xây dựng tab upload ảnh với roadmap nhận dạng đồ thị/hình học.
- Ít nhất trước mắt có thể lưu ảnh và trả về danh sách mẫu TikZ tương tự.

### 5.5. Nâng cao tính hỗ trợ học tập

- Thêm `Lesson mode` cho các dạng: parabola, đồ thị lượng giác, chóp, lăng trụ.
- Thêm `Practice mode` để giáo viên nhập đề bài và app sinh ảnh + mã mẫu.
- Hiển thị “Quick tips” như công thức đỉnh, tiệm cận, trục đối xứng.

## 6. ĐỀ XUẤT TIẾP THEO

1. Mở rộng template lên 12-15 mẫu chính thức.
2. Thêm options `grid` và `annotate` cho các đồ thị.
3. Tạo chức năng lưu/khôi phục template.
4. Hiển thị log biên dịch chi tiết khi lỗi xảy ra.
5. Khởi tạo roadmap phát triển `Pic-to-Text`.
