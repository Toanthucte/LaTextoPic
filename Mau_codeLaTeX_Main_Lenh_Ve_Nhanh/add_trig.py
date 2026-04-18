import json, re

with open(r"d:\vPT-LaTeX\LaTextoPic\Mau_codeLaTeX_Main_Lenh_Ve_Nhanh\KhoMau_LaTextoPic_Official.tex", "r", encoding="utf-8") as f:
    text = f.read()

cos_str = r"""
\vspace{0.5cm}

\subsection*{F.9. Đồ thị hàm lượng giác (Cosin)}
\begin{center}
\begin{tikzpicture}[scale=0.7,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \def\xmin{-7} \def\xmax{7} \def\ymin{-1.5} \def\ymax{1.8}
        \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
        \draw[->] (0,\ymin)--(0,\ymax) node [right]{$y$};
        \node at (0,0) [below right]{$O$};
        \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
        \draw[smooth,samples=200,domain=\xmin:\xmax] plot(\x,{cos(\x r)});
        \draw[dashed] (\xmin,1)--(\xmax,1) (\xmin,-1)--(\xmax,-1);
        \foreach \x in {-2*pi,-1.5*pi,-pi,-0.5*pi,0}
        {\draw[fill=black] (\x,cos \x*180/pi) circle (1pt);
                \draw[dashed] (\x,cos \x*180/pi)--(\x,0);
                \draw[fill=black] (-\x,cos -\x*180/pi) circle (1pt);
                \draw[dashed] (-\x,cos \x*180/pi)--(-\x,0);}
        \node at (0,1.3) [left]{$1$};
        \node at (0,-1.3) [left]{$-1$};
        \node at (-2*pi-0.15,0) [below]{$-2\pi$};
        \node at (-1.5*pi-0.2,0) [below]{$-\frac{3\pi}{2}$};
        \node at (-pi-0.15,0) [above]{$-\pi$};
        \node at (-0.5*pi-0.15,0) [above]{$-\frac{\pi}{2}$};
        \node at (0.5*pi+0.1,0) [above]{$\frac{\pi}{2}$};
        \node at (pi-0.1,0) [above]{$\pi$};
        \node at (1.5*pi,0) [above]{$\frac{3\pi}{2}$};
        \node at (2*pi+0.2,0) [below]{$2\pi$};
\end{tikzpicture}
\end{center}

\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.7,>=stealth,...]
  \def\xmin{-7} \def\xmax{7} \def\ymin{-1.5} \def\ymax{1.8}
  \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
  \draw[->] (0,\ymin)--(0,\ymax) node [right]{$y$};
  \node at (0,0) [below right]{$O$};
  \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
  \draw[smooth,samples=200,domain=\xmin:\xmax] plot(\x,{cos(\x r)});
  \draw[dashed] (\xmin,1)--(\xmax,1) (\xmin,-1)--(\xmax,-1);
  % Vẽ các điểm đặc biệt
  \foreach \x in {-2*pi,-1.5*pi,-pi,-0.5*pi,0}
  {\draw[fill=black] (\x,cos \x*180/pi) circle (1pt);
   \draw[dashed] (\x,cos \x*180/pi)--(\x,0);
   \draw[fill=black] (-\x,cos -\x*180/pi) circle (1pt);
   \draw[dashed] (-\x,cos \x*180/pi)--(-\x,0);}
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
"""

tan_str = r"""
\vspace{0.5cm}

\subsection*{F.10. Đồ thị hàm lượng giác (Tan)}
\begin{center}
\begin{tikzpicture}[scale=0.7,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \def\xmin{-7} \def\xmax{7} \def\ymin{-4} \def\ymax{4}
        \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
        \draw[->] (0,\ymin)--(0,\ymax) node [right]{$y$};
        \node at (0,0) [below right]{$O$};
        \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
        \draw[smooth,samples=300,domain=\xmin:\xmax] plot(\x,{tan(\x r)});
        \node at (-2*pi-0.2,0) [above]{$-2\pi$};
        \node at (-1.5*pi-0.4,0) [below]{$-\frac{3\pi}{2}$};
        \node at (-pi-0.2,0) [above]{$-\pi$};
        \node at (-0.5*pi-0.4,0) [below]{$-\frac{\pi}{2}$};
        \node at (0.5*pi-0.2,0) [below]{$\frac{\pi}{2}$};
        \node at (pi-0.1,0) [above]{$\pi$};
        \node at (1.5*pi-0.3,0) [below]{$\frac{3\pi}{2}$};
        \node at (2*pi+0.2,0) [below]{$2\pi$};
\end{tikzpicture}
\end{center}

\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.7,>=stealth,...]
  \def\xmin{-7} \def\xmax{7} \def\ymin{-4} \def\ymax{4}
  \draw[->] ((\xmin,0)--(\xmax,0) node [below]{$x$};
  \draw[->] (0,\ymin)--(0,\ymax) node [right]{$y$};
  \node at (0,0) [below right]{$O$};
  \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
  \draw[smooth,samples=300,domain=\xmin:\xmax] plot(\x,{tan(\x r)});
  % Điền text lên trục
  \node at (-0.5*pi-0.4,0) [below]{$-\frac{\pi}{2}$};
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
"""

cotan_str = r"""
\vspace{0.5cm}

\subsection*{F.11. Đồ thị hàm lượng giác (Cotan)}
\begin{center}
\begin{tikzpicture}[scale=0.7,>=stealth, font=\footnotesize, line join=round, line cap=round]
        \def\xmin{-7} \def\xmax{7} \def\ymin{-4} \def\ymax{4}
        \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
        \draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
        \node at (0,0) [above left]{$O$};
        \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
        \foreach \n in {-2,-1,0,1}
        {\draw[smooth,samples=200,domain=(\n+0.05)*pi:(\n+0.95)*pi] plot(\x,{1/tan(\x r)});
                \draw[dashed] (\n*pi,\ymin)--(\n*pi,\ymax);}
        \node at (-2*pi-0.4,0) [below]{$-2\pi$};
        \node at (-1.5*pi-0.3,0) [below]{$-\frac{3\pi}{2}$};
        \node at (-pi-0.3,0) [below]{$-\pi$};
        \node at (-0.5*pi-0.3,0) [below]{$-\frac{\pi}{2}$};
        \node at (0.5*pi-0.1,0) [below]{$\frac{\pi}{2}$};
        \node at (pi-0.2,0) [below]{$\pi$};
        \node at (1.5*pi-0.2,0) [below]{$\frac{3\pi}{2}$};
\end{tikzpicture}
\end{center}

\begin{tcolorbox}[codebox]
\begin{verbatim}
\begin{tikzpicture}[scale=0.7,>=stealth,...]
  \def\xmin{-7} \def\xmax{7} \def\ymin{-4} \def\ymax{4}
  \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
  \draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
  \node at (0,0) [above left]{$O$};
  \clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
  \foreach \n in {-2,-1,0,1}
  {\draw[smooth,samples=200,domain=(\n+0.05)*pi:(\n+0.95)*pi] 
          plot(\x,{1/tan(\x r)});
   \draw[dashed] (\n*pi,\ymin)--(\n*pi,\ymax);}
  % Điền text lên trục
\end{tikzpicture}
\end{verbatim}
\end{tcolorbox}
"""

if "F.9. Đồ thị hàm lượng giác (Cosin)" not in text:
    target = r"\section*{G. NHÓM BẢNG BIẾN THIÊN \& BẢNG XÉT DẤU (TKZ-TAB)}"
    pos = text.find(target)
    if pos != -1:
        text = text[:pos] + cos_str + "\n" + tan_str + "\n" + cotan_str + "\n\n% -------------------------------------------------------------------------\n" + text[pos:]
    else:
        print("Target 'NHÓM BẢNG BIẾN THIÊN' not found")

with open(r"d:\vPT-LaTeX\LaTextoPic\Mau_codeLaTeX_Main_Lenh_Ve_Nhanh\KhoMau_LaTextoPic_Official.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Add Trig Done")
