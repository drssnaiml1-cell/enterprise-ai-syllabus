"""Generate the presentation (LaTeX Beamer, 16:9) from the data files.

Usage:
    python3 scripts/make_slides.py      # writes slides/Enterprise_AI_Curriculum_Slides.tex
    cd slides && xelatex Enterprise_AI_Curriculum_Slides.tex && xelatex Enterprise_AI_Curriculum_Slides.tex
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda f: json.load(open(os.path.join(ROOT, "data", f), encoding="utf-8"))
C = J("courses.json") + J("extra_courses.json")
for c in C:
    c.setdefault("track", "core" if c["num"] <= 10 else "em")
K, P, U = J("careers.json"), J("products.json"), J("unicorn.json")
N = len(C)


def e(s):
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(rep.get(ch, ch) for ch in str(s))


TCOL = {"core": "navy", "em": "igreen", "fde": "gold"}
TNAME = {"core": "Core AI Track", "em": "Emerging Technologies Track", "fde": "Industry Practice Track"}
LV = {"Entry": ("saffron", "Fresher"), "Mid": ("chakra", "Mid 3--5 yrs"), "Senior": ("igreen", "Senior 6+ yrs")}
n_units = sum(len(c["units"]) for c in C)
n_labs = sum(len(c["labs"]) for c in C)
n_cert = sum(len(c["certs"]) for c in C)
n_jobs = len({j["title"] for k in K["courses"].values() for j in k["jobs"]})


def rng(s):
    """'6–15' / '30–60+' -> (6, 15, plus)"""
    m = re.findall(r"\d+", s)
    return float(m[0]), float(m[-1]), s.strip().endswith("+")


o = []
w = o.append
w(r"""\documentclass[aspectratio=169,10pt]{beamer}
\usepackage{fontspec}\setmainfont{FreeSerif}\setsansfont{FreeSerif}
\usepackage{tikz,tabularx,booktabs,colortbl,array}
\usetikzlibrary{shapes.geometric,shapes.symbols,arrows.meta,positioning,calc,shadows}
\definecolor{navy}{HTML}{0B1F3A}\definecolor{navy2}{HTML}{1E3A6E}
\definecolor{gold}{HTML}{A8811C}\definecolor{goldl}{HTML}{C9A227}\definecolor{goldbg}{HTML}{FBF6E9}
\definecolor{saffron}{HTML}{FF9933}\definecolor{saffront}{HTML}{B35400}
\definecolor{chakra}{HTML}{000080}\definecolor{igreen}{HTML}{138808}\definecolor{igreent}{HTML}{0E6B06}
\definecolor{l1bg}{HTML}{FFF4E8}\definecolor{l2bg}{HTML}{EEF0FF}\definecolor{l3bg}{HTML}{EEF8EC}
\definecolor{rowbg}{HTML}{F5F7FA}\definecolor{muted}{HTML}{5B6678}\definecolor{line}{HTML}{E6E2D6}
\definecolor{lay0}{HTML}{0B1F3A}\definecolor{lay1}{HTML}{16305A}\definecolor{lay2}{HTML}{1E3A6E}\definecolor{lay3}{HTML}{2B4B8A}\definecolor{lay4}{HTML}{0F5E5A}\definecolor{lay5}{HTML}{138808}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{normal text}{fg=navy}\setbeamercolor{structure}{fg=gold}
\setbeamercolor{frametitle}{fg=navy}\setbeamerfont{frametitle}{size=\Large,series=\bfseries}
\setbeamertemplate{frametitle}{\vspace{6pt}\insertframetitle\par\vspace{-2pt}{\color{goldl}\rule{2.2cm}{1.4pt}}}
\setbeamertemplate{itemize item}{\color{goldl}\small$\blacktriangleright$}
\setbeamertemplate{headline}{\begin{tikzpicture}[remember picture,overlay]
\fill[saffron] (current page.north west) rectangle ([xshift=5.333cm,yshift=-0.12cm]current page.north west);
\fill[white] ([xshift=5.333cm]current page.north west) rectangle ([xshift=10.667cm,yshift=-0.12cm]current page.north west);
\fill[igreen] ([xshift=10.667cm]current page.north west) rectangle ([yshift=-0.12cm]current page.north east);
\end{tikzpicture}}
\setbeamertemplate{footline}{\begin{beamercolorbox}[wd=\paperwidth,ht=2.4ex,dp=1ex]{}\hspace{0.4cm}{\tiny\color{muted}Enterprise AI Product Development Curriculum \;|\; Dr S Satyanarayana Ph.D., PDF(AI), FARSC \;|\; AlgoProfessor AI R\&D Solutions}\hfill{\tiny\bfseries\color{gold}\insertframenumber\,/\,\inserttotalframenumber}\hspace{0.4cm}\end{beamercolorbox}}
\newcommand{\pill}[2]{\tikz[baseline=(t.base)]\node[fill=#1,rounded corners=2pt,inner sep=2pt,text=white,font=\tiny\bfseries](t){#2};}
\newcommand{\chakra}[2]{\begin{scope}[shift={#1}]\draw[chakra,line width=1.4pt] (0,0) circle (#2);\fill[chakra] (0,0) circle (0.13*#2);\foreach \a in {0,15,...,345}{\draw[chakra,line width=0.4pt] (0,0) -- (\a:#2);}\end{scope}}
\renewcommand{\arraystretch}{1.18}
\begin{document}
""")

# 1 title
w(r"""{\setbeamertemplate{footline}{}
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
\fill[saffron] (current page.north west) rectangle ([yshift=-0.55cm]current page.north east);
\fill[igreen] (current page.south west) rectangle ([yshift=0.55cm]current page.south east);
\chakra{([xshift=-3.2cm,yshift=0.55cm]current page.east)}{1.9cm}
\node[anchor=south] at ([xshift=-3.2cm,yshift=-3.05cm]current page.east) {\includegraphics[width=1.9cm]{algoprofessor-logo.pdf}};
\node[anchor=west,align=left,text width=10.2cm] at ([xshift=0.8cm,yshift=0.0cm]current page.west) {\raggedright
{\scriptsize\bfseries\color{gold}INDUSTRY-ALIGNED COURSE SYLLABUS \;\textbullet\; 2026--27}\\[6pt]
{\fontsize{27}{31}\selectfont\bfseries\color{navy}Enterprise AI\\Product Development}\\[8pt]
{\normalsize\color{navy2}""" + str(N) + r""" courses \textbullet{} 3 tracks \textbullet{} skills, jobs \& salaries \textbullet{} 20 products}\\[12pt]
{\small\bfseries Dr S Satyanarayana Ph.D., PDF(AI), FARSC}\\
{\scriptsize Founder, CEO \& Chief Agentic AI Scientist, AlgoProfessor AI R\&D Solutions, Hyderabad}\\[6pt]
{\scriptsize\color{gold}\bfseries cto@algoprofessor.com \;|\; drssnaiml1-cell.github.io/enterprise-ai-syllabus}};
\end{tikzpicture}
\end{frame}}
""")

# 2 problem
w(r"""\begin{frame}{The gap every university must close by 2035}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{tikzpicture}
\node[draw=line,fill=rowbg,rounded corners=4pt,text width=5.6cm,align=center,inner sep=8pt] (a) {{\small\color{muted}Employers used to ask}\\[2pt]{\large\bfseries ``Did you \emph{study} AI?''}};
\node[draw=goldl,fill=goldbg,rounded corners=4pt,text width=5.6cm,align=center,inner sep=8pt,below=0.55cm of a] (b) {{\small\color{gold}Employers now ask}\\[2pt]{\large\bfseries ``What AI product have you \emph{built, deployed and governed}?''}};
\draw[-{Latex[length=3mm]},line width=1.5pt,goldl] (a) -- (b);
\end{tikzpicture}
\end{column}
\begin{column}{0.48\textwidth}
\small
\begin{itemize}\setlength\itemsep{6pt}
\item Every graduate in engineering, science and management will \textbf{work beside AI}; many will \textbf{build it}.
\item Universities that close the gap first lead in \textbf{placements, research, accreditation and rankings}.
\item This curriculum turns every unit into a \textbf{working artefact} and every course into a \textbf{deployable product}.
\item Aligned to \textbf{NEP 2020, OBE, NBA and NAAC} with CO--Bloom mapping.
\end{itemize}
\end{column}
\end{columns}
\end{frame}
""")

# 3 at a glance
stats = [(N, "Courses", "saffron"), (n_units, "Units", "chakra"), (N * 75, "Contact hours", "igreen"),
         (n_labs, "Hands-on labs", "saffron"), (n_cert, "Certifications mapped", "chakra"), (n_jobs, "Job roles", "igreen"),
         (len(P), "Enterprise products", "saffron"), (len(U["products"]), "Unicorn-track products", "chakra"), (len(K["pathways"]), "Career pathways", "igreen")]
w(r"\begin{frame}{The curriculum at a glance}\centering\begin{tikzpicture}")
for i, (n, lab, col) in enumerate(stats):
    x, y = (i % 3) * 4.6, -(i // 3) * 2.05
    tc = {"saffron": "saffront", "chakra": "chakra", "igreen": "igreent"}[col]
    w(rf"\node[draw=line,fill=white,rounded corners=5pt,minimum width=4.2cm,minimum height=1.75cm,drop shadow={{opacity=0.12}}] (s{i}) at ({x},{y}) {{}};\fill[{col}] ([xshift=2pt]s{i}.north west) rectangle ([xshift=-2pt,yshift=-4pt]s{i}.north east);")
    w(rf"\node[font=\fontsize{{24}}{{26}}\selectfont\bfseries,text={tc}] at ([yshift=0.12cm]s{i}.center) {{{n:,}}};\node[font=\small,text=muted] at ([yshift=-0.52cm]s{i}.center) {{{lab}}};")
w(r"\end{tikzpicture}\end{frame}")

# 4 three tracks
w(r"\begin{frame}{Three tracks, one product-engineering mindset}\centering\begin{tikzpicture}")
for i, tr in enumerate(["core", "em", "fde"]):
    cs = [c for c in C if c["track"] == tr]
    x = i * 5.1
    col = TCOL[tr]
    w(rf"\node[fill={col},rounded corners=4pt,minimum width=4.8cm,minimum height=0.9cm,text=white,font=\bfseries] at ({x},0) {{{TNAME[tr]}}};")
    w(rf"\node[font=\scriptsize\color{{muted}}] at ({x},-0.65) {{{len(cs)} course{'s' if len(cs) > 1 else ''}}};")
    for j, c in enumerate(cs):
        w(rf"\node[draw={col},fill=white,rounded corners=2pt,minimum width=4.8cm,minimum height=0.42cm,font=\scriptsize,anchor=center] at ({x},{-1.08 - j * 0.48}) {{\textbf{{\color{{{col}}}{c['num']}}}\; {e(c['title'])}}};")
w(r"""\node[text width=4.8cm,font=\scriptsize,align=left,anchor=north] at (10.2,-1.9) {Learners embed with a real or simulated client to \textbf{discover, prototype, deploy and scale} AI, combining the other fifteen courses.\\[4pt]{\color{gold}\bfseries The fastest-growing AI role of 2026.}};
\end{tikzpicture}\end{frame}""")

# 5 five-unit arc
arc = ["Foundations", "Core methods", "Advanced methods", "Production engineering", "Deployment, governance \\& capstone"]
w(r"\begin{frame}{Every course follows the same five-unit arc}\centering\begin{tikzpicture}")
cols5 = ["saffron", "goldl", "chakra", "navy2", "igreen"]
for i, a in enumerate(arc):
    w(rf"\node[signal,signal to=east,fill={cols5[i]},text=white,font=\small\bfseries,minimum height=1.3cm,minimum width=2.85cm,text width=2.3cm,align=center] at ({i * 2.95},0) {{Unit {['I','II','III','IV','V'][i]}\\{{\scriptsize {a}}}}};")
w(r"""\end{tikzpicture}\\[0.6cm]
\begin{tikzpicture}
\foreach \x/\t/\d in {0/45 lecture hours/L--T--P--C 3--0--2--4, 3.7/30 lab hours/8 tool-driven labs per course, 7.4/1 hands-on outcome/per unit: a working artefact, 11.1/1 capstone/a deployable enterprise product}{
\node[draw=line,fill=goldbg,rounded corners=4pt,minimum width=3.4cm,minimum height=1.4cm,align=center] at (\x,0) {{\bfseries\color{navy}\t}\\{\scriptsize\color{muted}\d}};}
\end{tikzpicture}\\[0.4cm]
{\scriptsize\color{muted}Five course outcomes per course mapped to Bloom levels L2 Understand to L6 Create, ready for CO--PO--PSO attainment.}
\end{frame}""")

# 6 course map
w(r"\begin{frame}{The " + str(N) + r" courses}\centering\begin{tikzpicture}")
for i, c in enumerate(C):
    x, y = (i % 4) * 3.75, -(i // 4) * 1.55
    col = TCOL[c["track"]]
    w(rf"\node[draw={col},line width=0.8pt,fill=white,rounded corners=4pt,minimum width=3.55cm,minimum height=1.38cm,text width=3.3cm,align=left] at ({x},{y}) {{{{\tiny\bfseries\color{{{col}}}{e(c['code'])}}}\\{{\scriptsize\bfseries {e(c['title'])}}}\\{{\tiny\color{{muted}}{e(', '.join(c['languages']))}}}}};")
    w(rf"\fill[{col}] ({x - 1.775 + 0.04},{y + 0.69}) rectangle ({x + 1.775 - 0.04},{y + 0.62});")
w(r"\end{tikzpicture}\\[2pt]{\tiny\pill{navy}{Core AI} \pill{igreen}{Emerging Technologies} \pill{gold}{Industry Practice (FDE)} \quad\color{muted} Each tile lists the course's top-3 programming languages.}\end{frame}")

# course slides
for c in C:
    k = K["courses"][str(c["num"])]
    col = TCOL[c["track"]]
    s = k["salary"]
    w(r"\begin{frame}")
    w(r"\begin{tikzpicture}[remember picture,overlay]\fill[" + col + r"] ([yshift=-0.12cm]current page.north west) rectangle ([yshift=-1.55cm]current page.north east);")
    w(r"\node[anchor=west,text=white,align=left] at ([xshift=0.5cm,yshift=-0.85cm]current page.north west) {{\tiny\bfseries\color{" + ("goldl" if col != "gold" else "white") + "}COURSE " + str(c["num"]) + r" \,|\, " + e(c["code"]) + r" \,|\, " + TNAME[c["track"]].upper() + r"}\\{\Large\bfseries " + e(c["title"]) + r"}\\[-1pt]{\scriptsize\itshape\color{white!85!" + col + r"}" + e(c["tagline"]) + r"}};\end{tikzpicture}")
    w(r"\vspace{0.72cm}")
    w(r"\begin{columns}[T]\begin{column}{0.53\textwidth}{\scriptsize\bfseries\color{gold}FIVE-UNIT CURRICULUM}\par\vspace{2pt}")
    for u in c["units"]:
        w(r"\begin{tikzpicture}\node[fill=" + col + r",text=white,font=\scriptsize\bfseries,minimum width=0.62cm,minimum height=0.62cm,rounded corners=2pt] (n) {" + u["n"] + r"};\node[right=3pt of n.east,anchor=west,text width=7.1cm,font=\scriptsize,align=left] {\textbf{" + e(u["title"]) + r"}\\{\color{muted}" + e(u["outcome"]) + r"}};\end{tikzpicture}\par\vspace{1pt}")
    w(r"\vspace{2pt}\begin{tikzpicture}\node[fill=goldbg,draw=goldl,rounded corners=3pt,text width=7.6cm,font=\scriptsize,align=left,inner sep=4pt] {{\bfseries\color{gold}Capstone:} \textbf{" + e(c["capstone"]["name"]) + r"}};\end{tikzpicture}")
    w(r"\end{column}\begin{column}{0.45\textwidth}{\scriptsize\bfseries\color{gold}SKILLS YOU WILL GAIN}\par\vspace{1pt}{\scriptsize\raggedright")
    for x in k["skills"][:4]:
        w(r"\textcolor{saffron}{$\star$} " + e(x) + r"\\")
    w(r"\par}\vspace{4pt}{\scriptsize\bfseries\color{gold}JOBS}\par\vspace{1pt}{\scriptsize")
    for j in k["jobs"][:4]:
        lc, lt = LV[j["level"]]
        w(r"\pill{" + lc + "}{" + lt + r"} \textbf{" + e(j["title"]) + r"}\\[1pt]")
    w(r"}\vspace{3pt}{\scriptsize\bfseries\color{gold}INDICATIVE SALARY IN INDIA (₹ LPA)}\par\vspace{2pt}\begin{tikzpicture}")
    for i, (bg, fc, lab, val) in enumerate((("l1bg", "saffront", "Fresher", s["entry"]), ("l2bg", "chakra", "Mid", s["mid"]), ("l3bg", "igreent", "Senior", s["senior"]))):
        bc = ["saffron", "chakra", "igreen"][i]
        w(rf"\node[fill={bg},minimum width=2.05cm,minimum height=0.95cm,rounded corners=2pt,align=center] (v{i}) at ({i * 2.1},0) {{{{\tiny\color{{muted}}{lab}}}\\{{\small\bfseries\color{{{fc}}}₹{e(val)}}}}};\fill[{bc}] ([xshift=1pt]v{i}.north west) rectangle ([xshift=-1pt,yshift=-2.5pt]v{i}.north east);")
    w(r"\end{tikzpicture}\par\vspace{2pt}{\tiny\color{muted}\textbf{Hiring:} " + e(", ".join(k["companies"][:6])) + r"}")
    w(r"\end{column}\end{columns}\end{frame}")

# salary range chart
w(r"\begin{frame}{Salary outlook: fresher to senior, by course}")
w(r"{\scriptsize\color{muted}Indicative annual CTC in India (₹ lakh per annum), compiled November 2026 from published 2026 salary reports. Bars run from the bottom of the fresher band to the top of the senior band.}\par\vspace{2pt}\centering\begin{tikzpicture}[x=0.066cm,y=0.37cm]")
w(r"\foreach \v in {0,20,...,160}{\draw[line] (\v,0.4) -- (\v,-" + str(N) + r".4);\node[font=\tiny,text=muted] at (\v,1.0) {\v};}")
for i, c in enumerate(C):
    s = K["courses"][str(c["num"])]["salary"]
    e0, e1, _ = rng(s["entry"]); m0, m1, _ = rng(s["mid"]); s0, s1, sp = rng(s["senior"])
    y = -i
    col = TCOL[c["track"]]
    w(rf"\node[anchor=east,font=\tiny,text={col}] at (-2,{y}) {{\textbf{{{c['num']}}} {e(c['title'])}}};")
    w(rf"\fill[saffron] ({e0},{y - 0.28}) rectangle ({e1},{y + 0.28});\fill[chakra,opacity=0.85] ({m0},{y - 0.28}) rectangle ({m1},{y + 0.28});\fill[igreen] ({max(s0, m1)},{y - 0.28}) rectangle ({s1},{y + 0.28});")
    w(rf"\node[anchor=west,font=\tiny,text=igreent] at ({s1 + 1},{y}) {{₹{e(s['entry']).split('–')[0]}--{e(s['senior'])}}};")
w(r"\node[font=\tiny,text=muted] at (80,-" + str(N) + r".2) {₹ lakh per annum};")
w(r"\end{tikzpicture}\\{\tiny\pill{saffron}{Fresher (0--2 yrs)} \pill{chakra}{Mid (3--5 yrs)} \pill{igreen}{Senior (6+ yrs)}\quad\color{muted}Ranges overlap where sources disagree; IT services pay at the lower end, product companies, GCCs and AI-first start-ups at the upper end.}\end{frame}")

# career matrix
w(r"\begin{frame}{Course-to-career matrix}\centering{\tiny\setlength{\tabcolsep}{1.6pt}\renewcommand{\arraystretch}{1.3}\begin{tabular}{@{}>{\raggedright\arraybackslash}p{3.6cm}" + "".join(r">{\centering\arraybackslash}p{0.42cm}" for _ in C) + r"@{}}")
w(r"\rowcolor{navy}\textcolor{white}{\bfseries Career role}" + "".join(r"&\textcolor{" + ("white" if c["track"] == "core" else ("green!40!white" if c["track"] == "em" else "goldl")) + r"}{\bfseries " + str(c["num"]) + "}" for c in C) + r"\\")
for i, p in enumerate(K["pathways"]):
    row = (r"\rowcolor{rowbg}" if i % 2 else "") + r"\textbf{" + e(p["role"]) + "}"
    for c in C:
        if c["num"] in p["courses"]:
            row += r"&\cellcolor{goldl!60}\leavevmode{\color{navy}●}"
        elif c["num"] in p["plus"]:
            row += r"&\cellcolor{goldbg}\leavevmode{\color{gold}○}"
        else:
            row += "&"
    w(row + r"\\")
w(r"\end{tabular}}\\[3pt]{\tiny\colorbox{goldl!60}{\color{navy}●} core course \quad \colorbox{goldbg}{\color{gold}○} recommended extra \quad column numbers = course numbers}\end{frame}")

# language strategy
w(r"""\begin{frame}{Programming language strategy 2026--2035}
\centering\begin{tikzpicture}
\node[fill=igreen,text=white,minimum width=11cm,minimum height=0.95cm,rounded corners=3pt,font=\small\bfseries] (d) at (0,2.2) {Delivery layer \;$\cdot$\; TypeScript / JavaScript \;$\cdot$\; Go \;$\cdot$\; Java / Scala};
\node[fill=goldl,text=white,minimum width=11cm,minimum height=0.95cm,rounded corners=3pt,font=\small\bfseries] (i) at (0,1.05) {Intelligence layer \;$\cdot$\; Python \;$\cdot$\; SQL \;$\cdot$\; R \;$\cdot$\; Julia};
\node[fill=chakra,text=white,minimum width=11cm,minimum height=0.95cm,rounded corners=3pt,font=\small\bfseries] (p) at (0,-0.1) {Performance \& safety layer \;$\cdot$\; C++ / CUDA \;$\cdot$\; Rust \;$\cdot$\; Mojo};
\node[fill=navy,text=white,minimum width=11cm,minimum height=0.95cm,rounded corners=3pt,font=\small\bfseries] (s) at (0,-1.25) {Specialist \;$\cdot$\; OpenQASM 3 (quantum) \;$\cdot$\; Solidity (smart contracts)};
\node[text width=3.4cm,font=\scriptsize,align=left,anchor=west] at (5.9,0.5) {\textbf{Python for intelligence, a systems language for performance, a delivery language for users.}\\[4pt]{\color{muted}Graduates who work across all three layers build complete AI products, not just models.}};
\end{tikzpicture}\\[0.35cm]
{\scriptsize\textbf{By 2030--2035:} AI-assisted engineering is the norm \textbullet{} polyglot by default \textbullet{} memory safety by design \textbullet{} performance engineering as a core skill \textbullet{} specification and verification}
\end{frame}""")

# enterprise products
w(r"\begin{frame}{Top 10 real-time enterprise products}{\scriptsize\color{muted}One flagship product per industry, each combining several courses into a real-time system students build as a capstone.}\par\vspace{3pt}\centering\begin{tikzpicture}")
for i, p in enumerate(P):
    x, y = (i % 5) * 3.0, -(i // 5) * 2.55
    w(rf"\node[draw=line,fill=white,rounded corners=4pt,minimum width=2.85cm,minimum height=2.4cm,text width=2.6cm,align=left,anchor=north] (p{i}) at ({x},{y}) {{\raggedright{{\fontsize{{14}}{{14}}\selectfont\bfseries\color{{goldl}}{p['id']:02d}}}\\{{\tiny\bfseries\color{{gold}}{e(p['domain'])}}}\\[1pt]{{\scriptsize\bfseries {e(p['name'])}}}\\[1pt]{{\tiny\color{{muted}}Courses {', '.join(map(str, p['courses']))}}}}};")
    w(rf"\fill[saffron] ([xshift=2pt]p{i}.north west) rectangle ([xshift=-2pt,yshift=-3pt]p{i}.north east);")
w(r"\end{tikzpicture}\end{frame}")

# example product deep dive: product 1
p = P[0]
w(r"\begin{frame}{Inside a product: " + e(p["name"]) + r"}")
w(r"\begin{columns}[T]\begin{column}{0.5\textwidth}\scriptsize")
w(r"\begin{tikzpicture}\node[fill=l1bg,text width=6.6cm,rounded corners=3pt,inner sep=5pt,align=left] {\textbf{Business problem:} " + e(p["problem"]) + r"};\end{tikzpicture}\par\vspace{3pt}")
w(r"\begin{tikzpicture}\node[fill=l3bg,text width=6.6cm,rounded corners=3pt,inner sep=5pt,align=left] {\textbf{In real time:} " + e(p["realtime"]) + r"};\end{tikzpicture}\par\vspace{4pt}")
w(r"\textbf{KPIs it moves:} " + e(", ".join(p["kpis"])) + r"\\[2pt]\textbf{Stack:} " + e(", ".join(p["stack"])))
w(r"\end{column}\begin{column}{0.47\textwidth}{\scriptsize\bfseries\color{gold}PRODUCT MODULES $\rightarrow$ COURSES}\par\vspace{3pt}")
for i, m in enumerate(p["modules"]):
    w(r"\begin{tikzpicture}\node[fill=lay" + str(i % 6) + r",text=white,text width=6.0cm,rounded corners=2pt,font=\tiny,inner sep=4pt,align=left] {\textbf{" + str(i + 1) + ".} " + e(m) + r"};\end{tikzpicture}\par\vspace{1pt}")
w(r"\vspace{2pt}{\tiny\textbf{Courses:} " + e(", ".join(f"{n}. {C[n-1]['title']}" for n in p["courses"])) + r"}\end{column}\end{columns}\end{frame}")

# unicorn grid
w(r"\begin{frame}{Unicorn track: 10 frontier products}{\scriptsize\color{muted}Each starts as a 12-week team MVP and grows into a venture-scale platform. Company names show market categories, not partners or endorsements.}\par\vspace{3pt}\centering\begin{tikzpicture}")
for i, u in enumerate(U["products"]):
    x, y = (i % 5) * 3.0, -(i // 5) * 3.1
    stars = "★" * u["complexity"] + "☆" * (5 - u["complexity"])
    w(rf"\node[fill=navy,rounded corners=4pt,minimum width=2.85cm,minimum height=2.95cm,text width=2.6cm,align=left,anchor=north,text=white] (u{i}) at ({x},{y}) {{\raggedright{{\tiny\bfseries\color{{goldl}}{e(u['category'])}}}\\[2pt]{{\scriptsize\bfseries {e(u['name'])}}}\\[3pt]{{\small\color{{goldl}}{stars}}}\\{{\tiny\color{{white!75!navy}}{len(u['courses'])} courses}}}};")
w(r"\end{tikzpicture}\end{frame}")

# unicorn architecture example: sovereign indic
u = U["products"][2]
w(r"\begin{frame}{Inside a unicorn-track product: " + e(u["name"]) + r"}\begin{columns}[T]\begin{column}{0.55\textwidth}{\scriptsize\bfseries\color{gold}SYSTEM ARCHITECTURE (TOP TO BOTTOM)}\par\vspace{3pt}")
for i, l in enumerate(u["layers"]):
    h, r = l.split(":", 1)
    w(r"\begin{tikzpicture}\node[fill=lay" + str(i % 6) + r",text=white,text width=7.6cm,rounded corners=2pt,font=\tiny,inner sep=4pt,align=left] {{\color{goldl}\bfseries " + e(h) + ":}" + e(r) + r"};\end{tikzpicture}\par\vspace{1pt}")
w(r"\end{column}\begin{column}{0.42\textwidth}\scriptsize\textbf{Why now:} " + e(u["signal"]) + r"\par\vspace{4pt}\textbf{The moat:}\begin{itemize}\setlength\itemsep{0pt}")
for m in u["moats"]:
    w(r"\item " + e(m))
w(r"\end{itemize}\vspace{3pt}\begin{tikzpicture}\node[fill=l1bg,text width=5.3cm,rounded corners=3pt,inner sep=4pt,align=left,font=\tiny] (a) {\textbf{12-week MVP:} " + e(u["mvp"]) + r"};\node[fill=l3bg,text width=5.3cm,rounded corners=3pt,inner sep=4pt,align=left,font=\tiny,below=3pt of a] {\textbf{Venture scale:} " + e(u["scale"]) + r"};\end{tikzpicture}\end{column}\end{columns}\end{frame}")

# FDE spotlight
fde = [c for c in C if c["track"] == "fde"][0]
kf = K["courses"][str(fde["num"])]
w(r"\begin{frame}{Spotlight: Forward Deployed Engineering (Course " + str(fde["num"]) + r")}\begin{columns}[T]\begin{column}{0.5\textwidth}\centering\begin{tikzpicture}")
steps = ["Discover", "Prototype", "Deploy", "Adopt", "Prove value"]
for i, st in enumerate(steps):
    ang = 90 - i * 72
    w(rf"\node[circle,fill={['saffron','goldl','chakra','navy2','igreen'][i]},text=white,minimum size=1.35cm,font=\scriptsize\bfseries,align=center] (f{i}) at ({ang}:2.0) {{{st}}};")
for i in range(5):
    w(rf"\draw[-{{Latex[length=2mm]}},gold,line width=1pt] (f{i}) to[bend left=18] (f{(i + 1) % 5});")
w(r"\node[font=\scriptsize\bfseries,text=gold,align=center] at (0,0) {Client-\\embedded\\loop};\end{tikzpicture}\end{column}\begin{column}{0.48\textwidth}\scriptsize")
w(r"\textbf{Engineers who embed with a client} to turn AI products into working, measured deployments: part engineer, part consultant, part product translator.\par\vspace{4pt}{\bfseries\color{gold}Jobs}\\")
for j in kf["jobs"]:
    lc, lt = LV[j["level"]]
    w(r"{\tiny\pill{" + lc + "}{" + lt + r"} " + e(j["title"]) + r"}\\")
s = kf["salary"]
w(r"\vspace{3pt}{\bfseries\color{gold}Salary in India:} {\color{saffront}₹" + e(s["entry"]) + r"} $\rightarrow$ {\color{chakra}₹" + e(s["mid"]) + r"} $\rightarrow$ {\color{igreent}₹" + e(s["senior"]) + r" LPA}\\[2pt]{\bfseries\color{gold}Hiring:} " + e(", ".join(kf["companies"][:7])) + r"\\[2pt]{\tiny\color{muted}FDE postings in India grew nearly 19-fold between June 2025 and June 2026 (Indeed data, reported by CXOToday).}")
w(r"\end{column}\end{columns}\end{frame}")

# consultancy
svc = ["Curriculum adoption \\& customisation", "Faculty development programmes", "AI \\& emerging-tech labs", "GitHub course repositories", "Industry capstones \\& live projects",
       "Certification readiness", "Centre of Excellence in AI", "Research, patents \\& Q1 papers", "Accreditation \\& ranking support", "Placement \\& career readiness"]
w(r"\begin{frame}{AlgoProfessor consultancy: from syllabus to industry-ready graduates}\centering\begin{tikzpicture}")
for i, t in enumerate(svc):
    x, y = (i % 5) * 3.0, -(i // 5) * 1.5
    col = ["saffron", "chakra", "igreen"][i % 3]
    w(rf"\node[draw=line,fill=white,rounded corners=4pt,minimum width=2.85cm,minimum height=1.3cm,text width=2.55cm,align=center,font=\scriptsize\bfseries] (c{i}) at ({x},{y}) {{{{\fontsize{{13}}{{13}}\selectfont\color{{goldl}}{i + 1:02d}}}\\{t}}};\fill[{col}] ([xshift=2pt]c{i}.north west) rectangle ([xshift=-2pt,yshift=-3pt]c{i}.north east);")
w(r"\end{tikzpicture}\\[0.35cm]\begin{tikzpicture}")
for i, (m, d) in enumerate((("Pilot", "1--2 courses, FDP, lab manual, GitHub repo"), ("Department Programme", "Core AI track + FDE, labs, capstones, certification prep"), ("University Transformation", f"All {N} courses, CoE, research and accreditation support"))):
    col = ["saffron", "chakra", "igreen"][i]
    w(rf"\node[fill={col},text=white,rounded corners=3pt,minimum width=4.7cm,minimum height=1.05cm,text width=4.4cm,align=center] at ({i * 4.95},0) {{{{\small\bfseries {m}}}\\{{\tiny {d}}}}};")
w(r"\end{tikzpicture}\\[0.2cm]{\scriptsize\textbf{How it runs:} {\color{saffront}\bfseries Discover} $\rightarrow$ {\color{chakra}\bfseries Design} $\rightarrow$ {\color{igreent}\bfseries Deliver} $\rightarrow$ {\color{gold}\bfseries Measure}, reviewed every semester}\end{frame}")

# assessment pie
w(r"""\begin{frame}{Assessment and outcome-based education}\begin{columns}[c]\begin{column}{0.45\textwidth}\centering\begin{tikzpicture}
\def\R{2.1}
\fill[saffron] (0,0) -- (90:\R) arc (90:18:\R) -- cycle;
\fill[chakra] (0,0) -- (18:\R) arc (18:-54:\R) -- cycle;
\fill[igreen] (0,0) -- (-54:\R) arc (-54:-126:\R) -- cycle;
\fill[goldl] (0,0) -- (-126:\R) arc (-126:-270:\R) -- cycle;
\fill[white] (0,0) circle (1.0);
\node[font=\small\bfseries,align=center] at (0,0) {Per\\course};
\node[font=\tiny\bfseries,text=white] at (54:1.55) {20\%};\node[font=\tiny\bfseries,text=white] at (-18:1.55) {20\%};\node[font=\tiny\bfseries,text=white] at (-90:1.55) {20\%};\node[font=\tiny\bfseries,text=white] at (162:1.55) {40\%};
\end{tikzpicture}\end{column}\begin{column}{0.52\textwidth}\small
\pill{saffron}{20\%} Continuous lab work \& notebooks\\[3pt]
\pill{chakra}{20\%} Two mid-term evaluations\\[3pt]
\pill{igreen}{20\%} Mini-project / sprint reviews\\[3pt]
\pill{goldl}{40\%} Enterprise capstone (demo + report)\\[8pt]
\begin{itemize}\scriptsize\setlength\itemsep{2pt}
\item Five COs per course mapped to Bloom levels L2--L6
\item Git, code review and CI/CD on every lab
\item Model cards, data sheets and risk register per product
\item Evidence ready for NBA, NAAC and NIRF
\end{itemize}\end{column}\end{columns}\end{frame}""")

# closing
w(r"""{\setbeamertemplate{footline}{}
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
\fill[saffron] (current page.north west) rectangle ([yshift=-0.55cm]current page.north east);
\fill[igreen] (current page.south west) rectangle ([yshift=0.55cm]current page.south east);
\chakra{([yshift=2.75cm]current page.center)}{0.7cm}
\node[align=center] at ([yshift=-0.15cm]current page.center) {
{\scriptsize\bfseries\color{gold}PARTNER WITH ALGOPROFESSOR}\\[4pt]
{\fontsize{22}{26}\selectfont\bfseries\color{navy}Build an AI-Ready University}\\[2pt]{\fontsize{22}{26}\selectfont\bfseries\color{navy}for 2026--2035}\\[8pt]
{\small Vice-Chancellors, Deans and HoDs: let's schedule a curriculum consultation.}\\[8pt]
{\large\bfseries\color{gold}cto@algoprofessor.com}\\[2pt]
{\small www.algoprofessor.com \;|\; campus.algoprofessor.com}\\[2pt]
{\scriptsize\color{muted}Explore in 3D: drssnaiml1-cell.github.io/enterprise-ai-syllabus \;|\; Syllabus book and slides on GitHub}};
\node at ([yshift=-3.05cm]current page.center) {\includegraphics[width=1.3cm]{algoprofessor-logo.pdf}};
\end{tikzpicture}
\end{frame}}
\end{document}""")

os.makedirs(os.path.join(ROOT, "slides"), exist_ok=True)
open(os.path.join(ROOT, "slides", "Enterprise_AI_Curriculum_Slides.tex"), "w", encoding="utf-8").write("\n".join(o))
print("slides/Enterprise_AI_Curriculum_Slides.tex written")
