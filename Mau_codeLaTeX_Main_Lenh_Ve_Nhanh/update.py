import json, re

with open(r"d:\vPT-LaTeX\LaTextoPic\Mau_codeLaTeX_Main_Lenh_Ve_Nhanh\KhoMau_LaTextoPic_Official.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Scale down F.2, F.3, F.4, F.6
def scale_down(sec_title):
    global text
    idx = text.find(sec_title)
    if idx == -1: return
    idx2 = text.find(r"\subsection*", idx + 10)
    if idx2 == -1: idx2 = text.find(r"\Closesolutionfile", idx + 10)
    if idx2 == -1: idx2 = text.find(r"\vspace", idx + 10)
    if idx2 == -1: idx2 = idx + 1000
    
    block = text[idx:idx2]
    new_block = block.replace("scale=0.8", "scale=0.5").replace("scale=1", "scale=0.5")
    text = text[:idx] + new_block + text[idx2:]

scale_down("F.2. Đồ thị")
scale_down("F.3. Đồ thị")
scale_down("F.4. Đồ thị")
scale_down("F.6. Đồ thị")

# 2. Layout change for F.5 and G.5
def vert_layout(sec_title):
    global text
    idx = text.find(sec_title)
    if idx == -1: return
    idx2 = text.find(r"\vspace{0.5cm}", idx)
    if idx2 == -1: idx2 = text.find(r"\Closesolutionfile", idx)
    
    block = text[idx:idx2]
    if "minipage" in block:
        tikz_match = re.search(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", block, flags=re.DOTALL)
        verb_match = re.search(r"\\begin\{tcolorbox\}\[codebox\].*?\\end\{tcolorbox\}", block, flags=re.DOTALL)
        if tikz_match and verb_match:
            new_block = sec_title + "\n\\begin{center}\n" + tikz_match.group(0) + "\n\\end{center}\n\n" + verb_match.group(0) + "\n"
            text = text[:idx] + new_block + text[idx2:]

vert_layout("F.5. Đồ thị")
vert_layout("G.5. Bảng xét dấu")

# 3. Add Lăng trụ xiên
l_tr_xien = r"""
\vspace{0.5cm}

\subsection*{C.3. Lăng trụ xiên tam giác}
\noindent
\begin{minipage}[c]{0.45\textwidth}
\centering
\begin{tikzpicture}[scale=0.9,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \tkzDefPoints{0/0/A,1.2/-1.5/B,3.5/0/C}
        \coordinate (H) at ($(A)!1/2!(B)$);
        \coordinate (A') at ($(H)+(0,4)$);
        \tkzDefPointsBy[translation = from A to A'](B,C){B'}{C'}
        \tkzDrawPolygon(A,B,C,C',B',A')
        \tkzDrawSegments(A',C' B',B A',H)
        \tkzDrawSegments[dashed](A,C)
        \tkzDrawPoints[fill=black,size=4](A,C,B,A',B',C')
        \tkzLabelPoints[above](B')
\end{tikzpicture}
\end{minipage}\hfill
\begin{minipage}[c]{0.52\textwidth}
\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.9,>=stealth,...]
  \tkzDefPoints{0/0/A,1.2/-1.5/B,3.5/0/C}
  \coordinate (H) at ($(A)!1/2!(B)$);
  \coordinate (A') at ($(H)+(0,4)$);
  \tkzDefPointsBy[translation = from A to A'](B,C){B'}{C'}
  \tkzDrawPolygon(A,B,C,C',B',A')
  \tkzDrawSegments(A',C' B',B A',H)
  \tkzDrawSegments[dashed](A,C)
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
\end{minipage}
"""
if "Lăng trụ xiên" not in text:
    target = r"\section*{D. NHÓM KHỐI TRÒN XOAY SERIES}"
    text = text.replace(target, l_tr_xien + "\n\n% -------------------------------------------------------------------------\n" + target)

# 4. Add Đồ thị hàm số mũ và Hàm số logarit
ham_mu = r"""
\vspace{0.5cm}

\subsection*{F.7. Đồ thị hàm số Mũ ($a^x$)}
\noindent
\begin{minipage}[c]{0.45\textwidth}
\centering
\begin{tikzpicture}[scale=0.6,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \def\xmin{-6} \def\xmax{6} \def\ymax{7}
        \draw[color=gray!50,dashed] (\xmin,-0.9) grid (\xmax,\ymax);
        \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
        \draw[->] (0,-0.9)--(0,\ymax) node [left]{$y$};
        \node at (0,0) [below left]{$O$};
        \clip (\xmin,-0.9) rectangle (\xmax-0.1,\ymax-0.1);
        \draw[smooth,samples=100] plot(\x,{2^(\x)});
        \draw[smooth,samples=100] plot(\x,{0.3^(\x)});
\end{tikzpicture}
\end{minipage}\hfill
\begin{minipage}[c]{0.52\textwidth}
\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.6,>=stealth,...]
  \def\xmin{-6} \def\xmax{6} \def\ymax{7}
  \draw[color=gray!50,dashed] (\xmin,-0.9) grid (\xmax,\ymax);
  \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
  \draw[->] (0,-0.9)--(0,\ymax) node [left]{$y$};
  \clip (\xmin,-0.9) rectangle (\xmax-0.1,\ymax-0.1);
  \draw[smooth,samples=100] plot(\x,{2^(\x)});
  \draw[smooth,samples=100] plot(\x,{0.3^(\x)});
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
\end{minipage}

\vspace{0.5cm}

\subsection*{F.8. Đồ thị hàm số Logarit ($\log_a x$)}
\noindent
\begin{minipage}[c]{0.45\textwidth}
\centering
\begin{tikzpicture}[scale=0.6,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \def\xmax{6} \def\ymin{-4} \def\ymax{4}
        \draw[color=gray!50,dashed] (-0.9,\ymin) grid (\xmax,\ymax);
        \draw[->] (-0.9,0)--(\xmax,0) node [below]{$x$};
        \draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
        \node at (0,0) [above left]{$O$};
        \clip (-0.9,\ymin) rectangle (\xmax-0.1,\ymax-0.1);
        \draw[smooth,samples=300,domain=0.01:\xmax] plot(\x,{ln(\x)/ln(2)});
        \draw[smooth,samples=300,domain=0.01:\xmax] plot(\x,{ln(\x)/ln(0.3)});
\end{tikzpicture}
\end{minipage}\hfill
\begin{minipage}[c]{0.52\textwidth}
\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.6,>=stealth,...]
  \def\xmax{6} \def\ymin{-4} \def\ymax{4}
  \draw[color=gray!50,dashed] (-0.9,\ymin) grid (\xmax,\ymax);
  \draw[->] (-0.9,0)--(\xmax,0) node [below]{$x$};
  \draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
  \clip (-0.9,\ymin) rectangle (\xmax-0.1,\ymax-0.1);
  \draw[smooth,samples=300,domain=0.01:\xmax] plot(\x,{ln(\x)/ln(2)});
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
\end{minipage}
"""
if "F.7. Đồ thị hàm số Mũ" not in text:
    target = r"\section*{G. NHÓM BẢNG BIẾN THIÊN"
    text = text.replace(target, ham_mu + "\n\n% -------------------------------------------------------------------------\n" + target)


with open(r"d:\vPT-LaTeX\LaTextoPic\Mau_codeLaTeX_Main_Lenh_Ve_Nhanh\KhoMau_LaTextoPic_Official.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Done")
