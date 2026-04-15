import os
from core.compiler import compile_tikz_to_pdf_png


def test_compile_tikz_to_pdf_png_white_background():
    tikz_code = r"""
\begin{tikzpicture}[line join=round,line cap=round,thick]
\coordinate (A) at (0,0);
\coordinate (B) at (2,0);
\draw (A) -- (B);
\end{tikzpicture}
"""
    pdf_path, png_path = compile_tikz_to_pdf_png(tikz_code, transparent=False)

    assert os.path.exists(pdf_path), f"Expected PDF file to exist: {pdf_path}"
    assert os.path.exists(png_path), f"Expected PNG file to exist: {png_path}"
    assert pdf_path.endswith('.pdf')
    assert png_path.endswith('.png')

    os.remove(pdf_path)
    os.remove(png_path)


def test_compile_tikz_to_pdf_png_transparent_background():
    tikz_code = r"""
\begin{tikzpicture}[line join=round,line cap=round,thick]
\coordinate (A) at (0,0);
\coordinate (B) at (2,0);
\draw (A) -- (B);
\end{tikzpicture}
"""
    pdf_path, png_path = compile_tikz_to_pdf_png(tikz_code, transparent=True)

    assert os.path.exists(pdf_path), f"Expected PDF file to exist: {pdf_path}"
    assert os.path.exists(png_path), f"Expected PNG file to exist: {png_path}"
    assert png_path.endswith('.png')

    os.remove(pdf_path)
    os.remove(png_path)
