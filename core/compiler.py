import os
import subprocess
import uuid
from pdf2image import convert_from_path

from PIL import Image

def compile_tikz_to_pdf_png(tikz_code: str, transparent: bool = False):
    """
    Biên dịch đoạn TikZ thành PDF (standalone) và sử dụng thư viện để convert sang PNG.
    """
    # 1. Bọc thẻ Preamble ẩn
    preamble = r"""\documentclass[tikz,border=2bp]{standalone}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{pgfplots}
\usepackage{tkz-euclide}
\pgfplotsset{compat=1.18}
\begin{document}
"""
    doc_tail = r"""
\end{document}
"""
    full_latex = f"{preamble}\n{tikz_code}\n{doc_tail}"
    
    # Tạo thư mục tạm tại tmp thư mục LaTextoPic
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    tmp_folder = os.path.join(base_dir, "temp_render")
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
        
    unique_id = str(uuid.uuid4())[:8]
    tex_path = os.path.join(tmp_folder, f"target_{unique_id}.tex")
    
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(full_latex)
        
    # 2. Biên dịch bằng subprocess (pdflatex)
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"target_{unique_id}.tex"],
            cwd=tmp_folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        error_logs = e.stdout.decode('utf-8', errors='ignore')
        print("Lỗi biên dịch LaTeX:")
        print(error_logs)
        raise RuntimeError(f"Biên dịch LaTeX thất bại! Vui lòng kiểm tra kỹ cú pháp.\n\nChi tiết lỗi từ pdflatex:\n```\n{error_logs[-1500:]}\n```")
        
    pdf_path = os.path.join(tmp_folder, f"target_{unique_id}.pdf")
    png_path = os.path.join(tmp_folder, f"target_{unique_id}.png")
    
    if not os.path.exists(pdf_path):
        raise RuntimeError(f"Biên dịch LaTeX thất bại! File PDF không được sinh ra: {pdf_path}")
        
    # 3. Sử dụng pdf2image convert sang PNG độ phân giải cap (DPI=300)
    try:
        # Nếu Windows, cần cài đặt poppler và thêm vào path, hoặc gọi poppler path
        images = convert_from_path(
            pdf_path,
            dpi=300,
            fmt='png',
            transparent=transparent,
            use_pdftocairo=True
        )
        
        if images:
            image = images[0]
            if transparent:
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
            else:
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                background = Image.new('RGBA', image.size, (255, 255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background.convert('RGB')
            image.save(png_path, 'PNG')
    except Exception as e:
        raise RuntimeError(f"Lỗi chuyển đổi PDF sang PNG bằng Poppler. Bạn có thể cần cài poppler-windows. Chi tiết: {str(e)}")
        
    return pdf_path, png_path
