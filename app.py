import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime, timedelta, timezone
from core.compiler import compile_tikz_to_pdf_png

# Xóa bỏ hiệu ứng mờ lóa (blur) mặc định của Streamlit để thao tác mượt mà hơn
st.markdown("""
<style>
    /* Vô hiệu hóa hiệu ứng mờ/lóa (blur) khi đang re-run state của Streamlit */
    [data-testid="stAppViewBlockContainer"], 
    .stApp > header {
        opacity: 1 !important;
        filter: none !important;
        transition: none !important;
    }
    .stApp [data-testid="stVerticalBlock"] > div {
        opacity: 1 !important;
        filter: none !important;
    }
    /* Ẩn trạng thái 'running...' ở góc phải trên cùng để giao diện sạch sẽ */
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="LaTextoPic - TikZ to Image", page_icon="🎨", layout="wide")

def main():
    st.title("🎨 LaTextoPic v1.0")
    st.markdown("**Tác giả:** Nguyễn Quản Quý | Biên dịch TikZ sang PNG & PDF tự động.")
    if "rendered" not in st.session_state:
        st.session_state.rendered = False
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""
    if "trigger_tutorial" not in st.session_state:
        st.session_state.trigger_tutorial = False

    def trigger_render():
        st.session_state.rendered = True

    # Apply generated code before widgets are created
    if st.session_state.generated_code:
        st.session_state.tikz_code = st.session_state.generated_code
        st.session_state.generated_code = ""
        st.session_state.rendered = False

    # Tabs
    tab1, tab_gen, tab2 = st.tabs(["🚀 Text-to-Pic (Trình biên dịch)", "⚙️ Cỗ máy lắp ráp TikZ", "🔍 Pic-to-Text (AI Trích xuất code)"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            default_tikz = """\\begin{tikzpicture}[scale=1, font=\\footnotesize, line join=round, line cap=round, >=stealth]
    \\draw[->] (-1,0)--(3,0) node[below]{$x$};
    \\draw[->] (0,-1)--(0,3) node[left]{$y$};
    \\fill (0,0) circle (1.5pt) node[below left]{$O$};
    \\draw[thick, blue] (-1,-1) -- (2,2);
\\end{tikzpicture}"""
            if "tikz_code" not in st.session_state:
                st.session_state.tikz_code = default_tikz

            def clear_code():
                st.session_state.tikz_code = ""

            with st.expander("📝 Nhập/Sửa mã TikZ của bạn tại đây", expanded=not st.session_state.rendered):
                row1, row2 = st.columns([5, 1])
                with row1:
                    st.markdown("**Dán mã TikZ vào đây.**")
                with row2:
                    st.button("🗑️ Xóa mã", on_click=clear_code, use_container_width=True)

                tikz_code = st.text_area("Chỉ cần copy phần \\begin{tikzpicture}...", value=st.session_state.tikz_code, key="tikz_code", height=250)
                bg_mode = st.radio(
                    "Chế độ nền PNG",
                    options=["Nền trắng", "Nền trong suốt"],
                    index=0,
                    horizontal=True
                )
                transparent = bg_mode == "Nền trong suốt"

            with st.expander("📖 Giải mã cấu trúc bản vẽ TikZ & Mẹo tùy chỉnh", expanded=False):
                if "plot" in tikz_code or "\\clip" in tikz_code or "grid" in tikz_code:
                    # Giao diện Giải mã cho Đồ thị hàm số
                    st.markdown("""
**1. 📈 3 Nhóm thông số chính trong Đồ thị hàm số**
- **🛠️ Khai báo giới hạn:** `\\def\\xmin`, `\\xmax`, `\\ymin`, `\\ymax`
  *(Định hình khung hộp giới hạn vùng vẽ và các trục)*
- **📐 Trục tọa độ & Lưới:** Lệnh `\\draw[...dashed] ... grid ...` và `\\draw[->]`
  *(Tạo lưới nền nhạt và mũi tên cho trục $Oxy$)*
- **🖌️ Vẽ đồ thị hàm số:** `\\draw[smooth,samples=100] plot(\\x, {...})`
  *(Tiệm cận/Khoảng vẽ được giới hạn qua `domain` và đường nét đứt, biểu thức nằm trong ngoặc nhọn `{...}`)*

**2. ✍️ Bảng tra cứu Đồ thị**
| Lệnh TikZ | Ý nghĩa thực tế |
| --- | --- |
| `domain=a:b` | Chỉ định khoảng vẽ đồ thị trên trục $Ox$ (Rất cần cho hàm phân thức) |
| `grid` | Lệnh sinh ra lưới tọa độ ô vuông |
| `\\clip` | Cắt xén gọn gàng phần đường cong nhô ra ngoài khung |
| `plot(\\x, {...})` | Hàm vẽ nét đồ thị (Biến số trục hoành là `\\x`) |
""")
                    st.info("""
**💡 Mẹo nhỏ - Tùy chỉnh Đồ thị**
1. **Chia nhánh đồ thị:** Với các hàm phân thức gián đoạn, luôn dùng thuộc tính `domain` và gộp làm 2 lệnh `plot` riêng biệt để không bị vẽ đè đường tiệm cận đứng.
2. **Độ mịn hàm số:** Mặc định `samples=100` là ổn cho đa thức, nhưng phân thức nên tăng thành `150` để đường cong gần tiệm cận trơn tru hơn.
""")

                elif "ball color" in tikz_code or "shade" in tikz_code:
                    # Giao diện Giải mã cho Hình Cầu
                    st.markdown("""
**1. 🔮 Các yếu tố hình thành khối Cầu (3D)**
- **🎨 Lệnh Đổ bóng:** `\\shade[ball color=..., opacity=0.8]`
  *(Đây là linh hồn của hình cầu, giúp tạo ra dải gradient xoay tròn như thật)*
- **🌐 Khung ngoài & Xích đạo:** Vòng tròn biên `\\draw circle (\\R);` và 2 nét cung `arc` diễn tả xích đạo.
- **Tham số R:** Được định nghĩa ở `\\def\\R{...}` thay vì viết cứng giá trị số.

**2. ✍️ Bảng tra cứu Hình Tròn Xoay**
| Lệnh TikZ | Ý nghĩa thực tế |
| --- | --- |
| `shade` | Phủ vùng không gian kèm hiệu ứng ánh sáng / bóng đổ |
| `opacity` | Độ trong suốt (0.0 là tàng hình, 1.0 là đặc hoàn toàn) |
| `arc (0:180:...)` | Góc vẽ cung tròn (Ví dụ vẽ nửa đường tròn nét đứt) |
""")
                    st.info("""
**💡 Mẹo nhỏ - Hiệu ứng bóng bẩy**
- Bảng màu TikZ: Bạn có thể đổi `ball color=blue!10` thành `red!20` (đỏ nhạt) hoặc `gray!30` (xám) để tạo khối cầu nhiều sắc thái.
- Điều chỉnh elip xích đạo: Parameter `\\R\\space and \\R/3` mang nghĩa trục lớn là $R$, trục nhỏ là $R/3$. Nếu đổi thành `R/4` thì góc nhìn nhô cao từ trên xuống sẽ dẹt hơn.
""")

                elif "ellipse" in tikz_code or ("(A) -- (S) -- (B)" in tikz_code) or "arc" in tikz_code:
                    # Giao diện Hình Nón / Hình Trụ
                    st.markdown("""
**1. 🥫 Thông số cấu tạo Nón / Trụ**
- **Điểm neo (Coordinate):** Sử dụng `\\coordinate (Tên) at (x,y)` để định vị tâm, đỉnh thay vì lệnh khối chóp.
- **🔄 Đường cong đáy (Elip):** Trong Nón có 2 cung `arc` (một đứt, một liền), trong Trụ có thêm nét vẽ nguyên vòng Elip cho đáy trên.
- **📐 Chiều cao:** Chỉ số $h$ quyết định tọa độ trục $y$ của các cực trị biên.

**2. ✍️ Bảng tra cứu Elip**
| Lệnh TikZ | Ý nghĩa thực tế |
| --- | --- |
| `\\coordinate` | Khai báo gán biến Tọa độ điểm ảo không hiển thị dấu chấm |
| `ellipse` | Lệnh vẽ Hình Elip (cần 2 thông số trục bán kính) |
| `node[midway]` | Đặt Text ở trung điểm của đoạn thẳng (Dành để ghi chú R và h) |
""")
                    st.info("""
**💡 Mẹo nhỏ - Biến đổi cấu trúc**
- Có thể kết hợp `\\fill` vào điểm O và O' để hiện lên dấu chấm rõ ràng.
- Gắn biến `node[midway, right]` giúp nhãn $h$ hay $R$ không bị chẹt đè gạch nối đứt mà nổi gọn gàng sang bên trái / phải.
""")

                else:
                    # Giao diện Giải mã cho Khối hình đa diện / chóp chuẩn
                    st.markdown("""
**1. 🏗️ 3 Nhóm thông số chính trong Khối đa diện**
- **📍 Tọa độ điểm:** Nằm ở lệnh `\\tkzDefPoints{x/y/Tên}`. 
  *(Thay đổi số X/Y để dời vị trí các điểm chóp/đáy)*
- **✏️ Lệnh vẽ kết nối:** `Polygon` (Vẽ mặt bao quanh), `Segments` (Vẽ cạnh đơn - nét đứt/liền).
- **🏷️ Nhãn & Ký hiệu:** `\\tkzLabelPoints`, `\\tkzMarkRightAngles` (Tên đỉnh, Góc vuông).

**2. ✍️ Bảng tra cứu Không gian**
| Lệnh TikZ | Ý nghĩa thực tế |
| --- | --- |
| `\\tkzDefPoints` | Định vị các đỉnh trong không gian lưới |
| `... at ...` | Dịch chuyển nhanh để xác định chiều cao đỉnh chóp |
| `\\tkzDrawPolygon` | Nối các điểm thành chu trình khép kín (Mặt bao) |
| `[dashed]` | Ký hiệu biến cạnh liền thành nét đứt (cạnh khuất) |
| `\\tkzLabelPoints` | Đặt tên nhãn chữ cái cho đỉnh tương ứng |
""")
                    st.info("""
**💡 Mẹo nhỏ - Căn chỉnh "Bộ 3 tham số vàng"**
1. **Trục X/Y:** Thay đổi số đầu tiên `(x)` để kéo sang trái/phải, số thứ hai `(y)` để nâng cao/hạ thấp đỉnh.
2. **Scale:** Sửa giá trị `scale=...` ở dòng đầu tiên `\\begin{tikzpicture}` để phóng to/thu nhỏ toàn bộ hình.
3. **Nét đứt/Liền:** Tùy ý bù/trừ chữ `dashed` trong ngoặc vuông của `\\tkzDrawSegments` để biến cạnh đứt thành nét liền và ngược lại.
""")

            render_button = st.button("🚀 Render Ảnh Lập Tức", type="primary", use_container_width=True, on_click=trigger_render)
            
        with col2:
            st.subheader("Kết quả")
            if st.session_state.rendered:
                pdf_path, png_path, compile_error = None, None, None
                
                # Biến cờ kiểm tra xem có cần biên dịch lại không
                if "last_compiled_code" not in st.session_state or st.session_state.last_compiled_code != tikz_code or st.session_state.get("last_transparent") != transparent:
                    with st.spinner("Đang biên dịch mã LaTeX... Vui lòng đợi trong giây lát."):
                        try:
                            pdf_path, png_path = compile_tikz_to_pdf_png(tikz_code, transparent=transparent)
                            st.session_state.last_pdf = pdf_path
                            st.session_state.last_png = png_path
                            st.session_state.last_error = None
                        except Exception as e:
                            st.session_state.last_error = str(e)
                            st.session_state.last_pdf = None
                            st.session_state.last_png = None
                        
                    st.session_state.last_compiled_code = tikz_code
                    st.session_state.last_transparent = transparent
                
                # Nạp kết quả từ bộ nhớ tạm
                pdf_path = st.session_state.get("last_pdf")
                png_path = st.session_state.get("last_png")
                compile_error = st.session_state.get("last_error")
                
                # Ra khỏi khối spinner, lúc này việc parse UI sẽ độc lập và hiển thị các nút dứt khoát
                if compile_error:
                    st.error(f"Lỗi hệ thống: {compile_error}")
                elif png_path and os.path.exists(png_path):
                    st.image(png_path, caption="Hình ảnh PNG độ phân giải cao")
                    
                    vn_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
                    timestamp = vn_time.strftime("%Y%m%dT%H%M%S") + "VN"
                    png_name = f"LaTextoPic_{timestamp}.png"
                    pdf_name = f"LaTextoPic_{timestamp}.pdf"
                    
                    # Đọc bytes bên ngoài Button để tránh lỗi "giữ file/tùy chọn"
                    with open(png_path, "rb") as f_png:
                        png_data = f_png.read()
                    
                    # Download Buttons
                    col_dl1, col_dl2 = st.columns(2)
                    col_dl1.download_button(
                        label="📥 Tải xuống PNG",
                        data=png_data,
                        file_name=png_name,
                        mime="image/png",
                        use_container_width=True
                    )
                    
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f_pdf:
                            pdf_data = f_pdf.read()
                        col_dl2.download_button(
                            label="📥 Tải xuống PDF (Vector)",
                            data=pdf_data,
                            file_name=pdf_name,
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.error("Rất tiếc! Xảy ra lỗi trong quá trình biên dịch (Log lỗi phía trên). Hãy kiểm tra lại cú pháp TikZ của bạn.")
            else:
                st.info("Ảnh kết quả sẽ hiển thị tại đây sau khi bạn nhấn nút Render bên trái.")
                
    with tab_gen:
        st.header("⚙️ Cỗ máy lắp ráp TikZ (Template Generator)")
        st.markdown("Chọn một mẫu hình và điền các tham số. Hệ thống sẽ tự động ghép thành mã TikZ chuẩn và gửi sang Trình biên dịch.")
        
        template_choice = st.selectbox("Chọn mẫu hình:", [
            "Hình chóp S.ABC (SA ⊥ đáy)", 
            "Hình Cầu, mặt cầu (3D bóng mờ)",
            "Hình Nón",
            "Hình Trụ",
            "Đồ thị hàm bậc 3 (ax³+bx²+cx+d)",
            "Đồ thị hàm phân thức (ax+b)/(cx+d)"
        ])
        
        generated_code = ""

        if template_choice == "Hình chóp S.ABC (SA ⊥ đáy)":
            st.subheader("1. Tham số khối chóp")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                S_name = st.text_input("Tên đỉnh chóp", value="S")
                A_name = st.text_input("Tên đỉnh góc vuông đáy", value="A")
            with col_b:
                B_name = st.text_input("Tên đỉnh đáy (trái)", value="B")
                C_name = st.text_input("Tên đỉnh đáy (phải)", value="C")
            with col_c:
                h_val = st.slider("Chiều cao khối chóp (h)", min_value=2.0, max_value=8.0, value=3.0, step=0.5)
                scale_val = st.slider("Tỷ lệ thu phóng (scale)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
                
            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize, line join=round, line cap=round]
	\\tkzDefPoints{{0/0/{A_name}, 1.2/-1.5/{B_name}, 4/0/{C_name}}}
	\\coordinate ({S_name}) at ($({A_name})+(0,{h_val})$);
	\\tkzDrawPolygon({S_name},{A_name},{B_name},{C_name})
	\\tkzDrawSegments({S_name},{B_name})
	\\tkzDrawSegments[dashed]({A_name},{C_name})
	\\tkzDrawPoints[fill=black,size=4]({A_name},{B_name},{C_name},{S_name})
	\\tkzMarkRightAngles[size=0.16]({S_name},{A_name},{B_name} {S_name},{A_name},{C_name})
	\\tkzLabelPoints[above]({S_name})
	\\tkzLabelPoints[below]({B_name})
	\\tkzLabelPoints[left]({A_name})
	\\tkzLabelPoints[right]({C_name})
\\end{{tikzpicture}}"""

        elif template_choice == "Đồ thị hàm bậc 3 (ax³+bx²+cx+d)":
            st.subheader("1. Tham số Đồ thị")
            col_a, col_b = st.columns(2)
            with col_a:
                a_val = st.number_input("Hệ số a", value=1.0)
                b_val = st.number_input("Hệ số b", value=-6.0)
                c_val = st.number_input("Hệ số c", value=9.0)
                d_val = st.number_input("Hệ số d", value=1.0)
            with col_b:
                x_min = st.number_input("x min", value=-6.0)
                x_max = st.number_input("x max", value=6.0)
                y_min = st.number_input("y min", value=-8.0)
                y_max = st.number_input("y max", value=8.0)
                scale_val = st.slider("Tỷ lệ thu phóng (scale) ", min_value=0.3, max_value=2.0, value=0.5, step=0.1)

            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize, line join=round, line cap=round]
	\\def\\a{{{a_val}}} \\def\\b{{{b_val}}} \\def\\c{{{c_val}}} \\def\\d{{{d_val}}} % Hệ số
	\\def\\xmin{{{x_min}}} \\def\\xmax{{{x_max}}}
	\\def\\ymin{{{y_min}}} \\def\\ymax{{{y_max}}} 
	\\draw[color=gray!50,dashed] (\\xmin,\\ymin) grid (\\xmax,\\ymax); 
	\\draw[->] (\\xmin,0)--(\\xmax,0) node [below]{{$x$}};
	\\draw[->] (0,\\ymin)--(0,\\ymax) node [left]{{$y$}};
	\\node at (0,0) [below left]{{$O$}};
	\\clip (\\xmin+0.1,\\ymin+0.1) rectangle (\\xmax-0.5,\\ymax-0.1);
	\\draw[smooth,samples=100] plot(\\x,{{\\a*(\\x)^3+\\b*(\\x)^2+\\c*(\\x)+\\d}});
\\end{{tikzpicture}}"""

        elif template_choice == "Hình Cầu, mặt cầu (3D bóng mờ)":
            st.subheader("1. Tham số Hình Cầu")
            col_a, col_b = st.columns(2)
            with col_a:
                R_val = st.slider("Bán kính R", min_value=1.0, max_value=8.0, value=3.0, step=0.5)
            with col_b:
                scale_val = st.slider("Tỷ lệ thu phóng (scale) ", min_value=0.3, max_value=2.0, value=1.0, step=0.1)

            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize]
	\\def\\R{{{R_val}}}
	\\shade[ball color=blue!10, opacity=0.8] (0,0) circle (\\R);
	\\draw (0,0) circle (\\R);
	\\draw[dashed] (\\R,0) arc (0:180:{{\\R}} and {{\\R/3}});
	\\draw (\\R,0) arc (0:-180:{{\\R}} and {{\\R/3}});
	\\fill (0,0) circle (1.5pt) node[below] {{$O$}};
	\\draw[dashed] (0,0) -- (\\R,0) node[midway, above] {{$R$}};
\\end{{tikzpicture}}"""

        elif template_choice == "Hình Nón":
            st.subheader("1. Tham số Hình Nón")
            col_a, col_b = st.columns(2)
            with col_a:
                R_val = st.slider("Bán kính đáy R", min_value=1.0, max_value=6.0, value=2.0, step=0.5)
                h_val = st.slider("Chiều cao h", min_value=2.0, max_value=8.0, value=4.0, step=0.5)
            with col_b:
                scale_val = st.slider("Tỷ lệ thu phóng (scale) ", min_value=0.3, max_value=2.0, value=1.0, step=0.1)

            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize, line join=round, line cap=round]
	\\def\\R{{{R_val}}}
	\\def\\h{{{h_val}}}
	\\coordinate (O) at (0,0);
	\\coordinate (S) at (0,\\h);
	\\coordinate (A) at (-\\R,0);
	\\coordinate (B) at (\\R,0);
	\\draw[dashed] (\\R,0) arc (0:180:{{\\R}} and {{\\R/3}});
	\\draw (\\R,0) arc (0:-180:{{\\R}} and {{\\R/3}});
	\\draw (A) -- (S) -- (B);
	\\draw[dashed] (A) -- (B);
	\\draw[dashed] (O) -- (S) node[midway, right] {{$h$}};
	\\draw[dashed] (O) -- (B) node[midway, below] {{$R$}};
	\\fill (O) circle (1.5pt) node[below] {{$O$}};
	\\fill (S) circle (1.5pt) node[above] {{$S$}};
\\end{{tikzpicture}}"""

        elif template_choice == "Hình Trụ":
            st.subheader("1. Tham số Hình Trụ")
            col_a, col_b = st.columns(2)
            with col_a:
                R_val = st.slider("Bán kính đáy R", min_value=1.0, max_value=6.0, value=2.0, step=0.5)
                h_val = st.slider("Chiều cao h", min_value=2.0, max_value=8.0, value=4.0, step=0.5)
            with col_b:
                scale_val = st.slider("Tỷ lệ thu phóng (scale) ", min_value=0.3, max_value=2.0, value=1.0, step=0.1)

            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize, line join=round, line cap=round]
	\\def\\R{{{R_val}}}
	\\def\\h{{{h_val}}}
	\\coordinate (O1) at (0,0);
	\\coordinate (O2) at (0,\\h);
	\\coordinate (A) at (-\\R,0);
	\\coordinate (B) at (\\R,0);
	\\coordinate (C) at (-\\R,\\h);
	\\coordinate (D) at (\\R,\\h);
	
	% Đáy dưới
	\\draw[dashed] (\\R,0) arc (0:180:{{\\R}} and {{\\R/3}});
	\\draw (\\R,0) arc (0:-180:{{\\R}} and {{\\R/3}});
	% Đáy trên
	\\draw (O2) ellipse ({{\\R}} and {{\\R/3}});
	
	\\draw (A) -- (C);
	\\draw (B) -- (D);
	\\draw[dashed] (O1) -- (O2) node[midway, right] {{$h$}};
	\\draw[dashed] (O1) -- (B) node[midway, below] {{$R$}};
	\\fill (O1) circle (1.5pt) node[below] {{$O$}};
	\\fill (O2) circle (1.5pt) node[above] {{$O'$}};
\\end{{tikzpicture}}"""

        elif template_choice == "Đồ thị hàm phân thức (ax+b)/(cx+d)":
            st.subheader("1. Tham số Đồ thị")
            col_a, col_b = st.columns(2)
            with col_a:
                a_val = st.number_input("Hệ số a", value=2.0)
                b_val = st.number_input("Hệ số b", value=-1.0)
                c_val = st.number_input("Hệ số c", value=1.0)
                d_val = st.number_input("Hệ số d", value=1.0)
            with col_b:
                x_min = st.number_input("x min", value=-5.0)
                x_max = st.number_input("x max", value=5.0)
                y_min = st.number_input("y min", value=-5.0)
                y_max = st.number_input("y max", value=5.0)
                scale_val = st.slider("Tỷ lệ thu phóng (scale) ", min_value=0.3, max_value=2.0, value=0.6, step=0.1)

            if st.button("⚙️ Sinh mã \& Gửi sang Trình biên dịch", type="primary"):
                st.session_state.trigger_tutorial = True
                generated_code = f"""\\begin{{tikzpicture}}[scale={scale_val},>=stealth, font=\\footnotesize, line join=round, line cap=round]
	\\def\\a{{{a_val}}} \\def\\b{{{b_val}}} \\def\\c{{{c_val}}} \\def\\d{{{d_val}}} % Hệ số
	\\def\\xmin{{{x_min}}} \\def\\xmax{{{x_max}}}
	\\def\\ymin{{{y_min}}} \\def\\ymax{{{y_max}}} 
	\\draw[color=gray!50,dashed] (\\xmin,\\ymin) grid (\\xmax,\\ymax); 
	\\draw[->] (\\xmin,0)--(\\xmax,0) node [below]{{$x$}};
	\\draw[->] (0,\\ymin)--(0,\\ymax) node [left]{{$y$}};
	\\node at (0,0) [below left]{{$O$}};
	\\clip (\\xmin+0.1,\\ymin+0.1) rectangle (\\xmax-0.5,\\ymax-0.1);
	
	% Nhánh 1: x < -d/c
	\\draw[smooth,samples=150,domain=\\xmin:{{-(\\d/\\c)-0.1}}] plot(\\x,{{(\\a*\\x+\\b)/(\\c*\\x+\\d)}});
	% Nhánh 2: x > -d/c
	\\draw[smooth,samples=150,domain={{-(\\d/\\c)+0.1}}:\\xmax] plot(\\x,{{(\\a*\\x+\\b)/(\\c*\\x+\\d)}});
	
	% Tiệm cận
	\\draw[dashed, color=red] ({{-(\\d/\\c)}},\\ymin) -- ({{-(\\d/\\c)}},\\ymax) node[above] {{x=$\\frac{{-d}}{{c}}$}};
	\\draw[dashed, color=red] (\\xmin,{{\\a/\\c}}) -- (\\xmax,{{\\a/\\c}}) node[right] {{y=$\\frac{{a}}{{c}}$}};
\\end{{tikzpicture}}"""

        if generated_code:
            st.success("✅ Đã lắp ráp xong mã TikZ! Hãy quay lại tab **Text-to-Pic** để kết xuất ảnh.")
            st.session_state.generated_code = generated_code
            st.code(generated_code, language="latex")

    with tab2:
        st.header("🔍 Pic-to-Text: Tìm kiếm ảnh TikZ (Tính năng đang phát triển)")
        st.info("Tính năng truy vấn bằng AI (Sử dụng CLIP & FAISS) giúp bạn upload ảnh và tìm ra đoạn code TikZ mẫu trong kho dữ liệu sẽ sớm được cập nhật ở phiên bản tiếp theo.")
        st.file_uploader("KÃ©o tháº£ hÃ¬nh áº£nh ToÃ¡n há»c táº¡i Ä‘Ã¢y Ä‘á»ƒ tÃ¬m kiáº¿m code", type=['png', 'jpg', 'jpeg'])

    # --- PWA INJECTION ---
    pwa_html = """
    <script>
        const head = window.parent.document.head;
        if (!head.querySelector('link[rel="manifest"]')) {
            const manifest = window.parent.document.createElement('link');
            manifest.rel = 'manifest';
            manifest.href = 'app/static/manifest.json';
            head.appendChild(manifest);
        }
        
        const metas = [
            {name: 'apple-mobile-web-app-capable', content: 'yes'},
            {name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent'},
            {name: 'mobile-web-app-capable', content: 'yes'}
        ];
        metas.forEach(m => {
            if (!head.querySelector('meta[name="' + m.name + '"]')) {
                const el = window.parent.document.createElement('meta');
                el.name = m.name; el.content = m.content;
                head.appendChild(el);
            }
        });
        
        if ('serviceWorker' in window.parent.navigator) {
            window.parent.navigator.serviceWorker.register('app/static/sw.js')
            .then(function(reg) {
                console.log('SW Registered', reg);
            }).catch(function(err) {
                console.log('SW Failed', err);
            });
        }
    </script>
    """
    components.html(pwa_html, height=0, width=0)

    # Kích hoạt JS Hiệu ứng Hole Punching & Tab Switching (Chuyển xuống cuối để tránh lag 1 nhịp)
    if st.session_state.trigger_tutorial:
        tutorial_js = """
        <script>
            // Các component html của Streamlit chạy trong iframe, nên cần trỏ ra window.parent.document
            const parentDoc = window.parent.document;
            
            setTimeout(() => {
                // Bước 1: Sang Tab Trình Biên Dịch
                const tabs = Array.from(parentDoc.querySelectorAll('button[data-baseweb="tab"]'));
                const targetTab = tabs.find(t => t.innerText.includes("🚀 Text-to-Pic") || t.innerText.includes("Trình biên dịch"));
                if (targetTab) {
                    targetTab.click();
                }
                
                // Bước 2: Chờ 0.5 giây để tab render xong, thực hiện Hole Punching mask lên nút "Xóa mã"
                setTimeout(() => {
                    const btns = Array.from(parentDoc.querySelectorAll('button'));
                    const targetBtn = btns.find(b => b.innerText.includes("Xóa mã"));
                    
                    if (targetBtn) {
                        const rect = targetBtn.getBoundingClientRect();
                        
                        // Tránh tạo nhiều lớp phủ
                        const oldOverlay = parentDoc.getElementById('tut-overlay');
                        if (oldOverlay) oldOverlay.remove();
                        
                        // Lớp phủ tối (Overlay)
                        const overlay = parentDoc.createElement('div');
                        overlay.id = 'tut-overlay';
                        overlay.style.position = 'fixed';
                        overlay.style.top = '0';
                        overlay.style.left = '0';
                        overlay.style.width = '100vw';
                        overlay.style.height = '100vh';
                        overlay.style.zIndex = '999990';
                        overlay.style.pointerEvents = 'none'; // Cho phép click xuyên lớp phủ xuống nút Xóa
                        
                        // "Lỗ đục" bằng box-shadow khổng lồ
                        const mask = parentDoc.createElement('div');
                        mask.className = 'tut-hole-mask';
                        mask.style.position = 'fixed'; // Cố định theo màn hình
                        mask.style.top = (rect.top - 4) + 'px';
                        mask.style.left = (rect.left - 4) + 'px';
                        mask.style.width = (rect.width + 8) + 'px';
                        mask.style.height = (rect.height + 8) + 'px';
                        mask.style.borderRadius = '8px';
                        mask.style.pointerEvents = 'none';
                        mask.style.zIndex = '999991';
                        
                        // Text nhấp nháy + Emoji
                        if (!parentDoc.getElementById('tut-blink-style')) {
                            const style = parentDoc.createElement('style');
                            style.id = 'tut-blink-style';
                            parentDoc.head.appendChild(style);
                        }
                        
                        // Cập nhật cấu trúc CSS hỗ trợ Responsive, Design Đẹp & Tooltip Chuyên Nghiệp
                        const styleNode = parentDoc.getElementById('tut-blink-style');
                        styleNode.innerHTML = `
                            .tut-hole-mask {
                                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.75), 0 0 0 2px rgba(255, 235, 59, 1);
                                animation: hole-pulse 2s infinite;
                            }
                            @keyframes hole-pulse {
                                0% { box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.75), 0 0 0 2px rgba(255, 235, 59, 1), 0 0 10px 2px rgba(255, 235, 59, 0.4); }
                                50% { box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.75), 0 0 0 4px rgba(255, 235, 59, 1), 0 0 20px 5px rgba(255, 235, 59, 0.8); }
                                100% { box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.75), 0 0 0 2px rgba(255, 235, 59, 1), 0 0 10px 2px rgba(255, 235, 59, 0.4); }
                            }
                            @keyframes tut-pulse { 
                                0% { box-shadow: 0 0 0 0 rgba(255, 235, 59, 0.8); } 
                                70% { box-shadow: 0 0 0 15px rgba(255, 235, 59, 0); } 
                                100% { box-shadow: 0 0 0 0 rgba(255, 235, 59, 0); } 
                            }
                            @keyframes tut-bounce {
                                0%, 100% { margin-top: 0; }
                                50% { margin-top: -8px; }
                            }
                            @keyframes tut-fade-in {
                                from { opacity: 0; }
                                to { opacity: 1; }
                            }
                            .tut-tooltip {
                                position: absolute;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                gap: 6px;
                                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                                color: white;
                                padding: 18px 24px;
                                border-radius: 12px;
                                border: 2.5px solid #ffeb3b;
                                font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
                                z-index: 999992;
                                animation: tut-pulse 2s infinite, tut-bounce 3s ease-in-out infinite;
                                pointer-events: none;
                                word-wrap: break-word;
                                text-align: center;
                                box-shadow: 0 8px 25px rgba(0,0,0,0.5);
                            }
                            .tut-tooltip::before {
                                content: '';
                                position: absolute;
                                border-style: solid;
                            }
                            .tut-tooltip::after {
                                content: '';
                                position: absolute;
                                border-style: solid;
                            }
                            .tut-emoji {
                                font-size: 32px;
                                line-height: 1;
                                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
                            }
                            .tut-msg {
                                font-size: 17px;
                                font-weight: 600;
                                line-height: 1.4;
                                letter-spacing: 0.3px;
                            }
                            .tut-msg-sub {
                                font-size: 13px;
                                font-weight: 400;
                                opacity: 0.85;
                                margin-top: 2px;
                            }
                            /* Màn hình ngang (Desktop) */
                            @media (min-width: 601px) {
                                .tut-tooltip {
                                    top: ` + (rect.top + rect.height / 2) + `px;
                                    left: ` + (rect.right + 25) + `px;
                                    transform: translateY(-50%);
                                    max-width: 320px;
                                }
                                .tut-tooltip::before {
                                    border-width: 12px 16px 12px 0;
                                    border-color: transparent #ffeb3b transparent transparent;
                                    left: -18.5px;
                                    top: calc(50% - 12px);
                                }
                                .tut-tooltip::after {
                                    border-width: 10px 14px 10px 0;
                                    border-color: transparent #1e3c72 transparent transparent;
                                    left: -14px;
                                    top: calc(50% - 10px);
                                }
                            }
                            /* Màn hình dọc nhỏ (Mobile) */
                            @media (max-width: 600px) {
                                .tut-tooltip {
                                    top: ` + (rect.bottom + 20) + `px;
                                    left: 20px;
                                    right: 20px;
                                }
                                .tut-tooltip::before {
                                    border-width: 0 12px 16px 12px;
                                    border-color: transparent transparent #ffeb3b transparent;
                                    top: -18.5px;
                                    left: calc(50% - 12px);
                                }
                                .tut-tooltip::after {
                                    border-width: 0 10px 14px 10px;
                                    border-color: transparent transparent #1e3c72 transparent;
                                    top: -14px;
                                    left: calc(50% - 10px);
                                }
                            }
                        `;

                        // Áp dụng animation cho Overlay
                        overlay.style.animation = 'tut-fade-in 0.4s ease-out forwards';

                        const text = parentDoc.createElement('div');
                        text.className = 'tut-tooltip';
                        text.innerHTML = '<div class="tut-emoji">✨</div><div class="tut-msg">Nhấn "Xóa mã" để dán nội dung mới</div><div class="tut-msg-sub">Biên dịch sẽ tự động bắt đầu</div>';
                        
                        overlay.appendChild(mask);
                        overlay.appendChild(text);
                        parentDoc.body.appendChild(overlay);
                        
                        // Xóa Overlay khi click vào Nút hoặc sau 8 giây tự hủy
                        targetBtn.addEventListener('click', () => {
                            const ov = parentDoc.getElementById('tut-overlay');
                            if (ov) ov.remove();
                        });
                        setTimeout(() => {
                            const ov = parentDoc.getElementById('tut-overlay');
                            if (ov) ov.remove();
                        }, 8000);
                    }
                }, 500); // 500ms delay cho đến khi render tab HTML hoàn chỉnh
            }, 100);
        </script>
        """
        components.html(tutorial_js, height=0, width=0)
        # Đặt lại sau khi tiêm thành công trong cùng một chu kỳ
        st.session_state.trigger_tutorial = False

if __name__ == "__main__":
    main()
