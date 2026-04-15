import streamlit as st
import os
from datetime import datetime, timedelta, timezone
from core.compiler import compile_tikz_to_pdf_png

st.set_page_config(page_title="LaTextoPic - TikZ to Image", page_icon="🎨", layout="wide")

def main():
    st.title("🎨 LaTextoPic v1.0")
    st.markdown("**Tác giả:** Nguyễn Quản Quý | Biên dịch TikZ sang PNG & PDF tự động.")
    if "rendered" not in st.session_state:
        st.session_state.rendered = False

    def trigger_render():
        st.session_state.rendered = True

    # Tabs
    tab1, tab2 = st.tabs(["🚀 Text-to-Pic (Trình biên dịch)", "🔍 Pic-to-Text (AI Trích xuất code)"])
    
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

            render_button = st.button("🚀 Render Ảnh Lập Tức", type="primary", use_container_width=True, on_click=trigger_render)
            
        with col2:
            st.subheader("Kết quả")
            if st.session_state.rendered:
                with st.spinner("Đang biên dịch mã LaTeX... Vui lòng đợi trong giây lát."):
                    try:
                        pdf_path, png_path = compile_tikz_to_pdf_png(tikz_code, transparent=transparent)
                        if png_path and os.path.exists(png_path):
                            st.image(png_path, caption="Hình ảnh PNG độ phân giải cao")
                            
                            vn_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
                            timestamp = vn_time.strftime("%Y%m%dT%H%M%S") + "VN"
                            png_name = f"LaTextoPic_{timestamp}.png"
                            pdf_name = f"LaTextoPic_{timestamp}.pdf"
                            
                            # Download Buttons
                            col_dl1, col_dl2 = st.columns(2)
                            with open(png_path, "rb") as f_png:
                                col_dl1.download_button(
                                    label="📥 Tải xuống PNG",
                                    data=f_png,
                                    file_name=png_name,
                                    mime="image/png",
                                    use_container_width=True
                                )
                            with open(pdf_path, "rb") as f_pdf:
                                col_dl2.download_button(
                                    label="📥 Tải xuống PDF (Vector)",
                                    data=f_pdf,
                                    file_name=pdf_name,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                        else:
                            st.error("Rất tiếc! Xảy ra lỗi trong quá trình biên dịch (Log lỗi phía trên). Hãy kiểm tra lại cú pháp TikZ của bạn.")
                    except Exception as e:
                        st.error(f"Lỗi hệ thống: {str(e)}")
            else:
                st.info("Ảnh kết quả sẽ hiển thị tại đây sau khi bạn nhấn nút Render bên trái.")
                
    with tab2:
        st.header("🔍 Pic-to-Text: Tìm kiếm ảnh TikZ (Tính năng đang phát triển)")
        st.info("Tính năng truy vấn bằng AI (Sử dụng CLIP & FAISS) giúp bạn upload ảnh và tìm ra đoạn code TikZ mẫu trong kho dữ liệu sẽ sớm được cập nhật ở phiên bản tiếp theo.")
        st.file_uploader("Kéo thả hình ảnh Toán học tại đây để tìm kiếm code", type=['png', 'jpg', 'jpeg'])

if __name__ == "__main__":
    main()
