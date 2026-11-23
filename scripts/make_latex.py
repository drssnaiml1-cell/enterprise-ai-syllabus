"""Generate the full syllabus as LaTeX (XeLaTeX) from the data files.

Usage:
    python3 scripts/make_latex.py            # writes latex/Enterprise_AI_Syllabus.tex
    cd latex && xelatex Enterprise_AI_Syllabus.tex && xelatex Enterprise_AI_Syllabus.tex
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
J = lambda f: json.load(open(os.path.join(DATA, f), encoding="utf-8"))

C = J("courses.json") + J("extra_courses.json")
DET = J("course_details.json")
for c in C:
    c.setdefault("track", "core" if c["num"] <= 10 else "em")
    d = DET.get(str(c["num"]))
    if d:
        for k in ("tools", "langs", "refs"):
            c.setdefault(k, d[k])
K, P, U = J("careers.json"), J("products.json"), J("unicorn.json")
N = len(C)
WORD = {15: "Fifteen", 16: "Sixteen", 17: "Seventeen"}[N]
word = WORD.lower()


def e(s):
    """Escape plain text for LaTeX."""
    s = str(s)
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(rep.get(ch, ch) for ch in s)


def title_of(n):
    return C[n - 1]["title"]


TRACK = {"core": "Core AI Track", "em": "Emerging Technologies Track", "fde": "Industry Practice Track"}
LVL = {"Entry": ("l1", "Fresher / Entry"), "Mid": ("l2", "Mid (3--5 yrs)"), "Senior": ("l3", "Senior (6+ yrs)")}

out = []
w = out.append

# ------------------------------------------------------------------ preamble
w(r"""\documentclass[10pt,a4paper]{article}
\usepackage[a4paper,top=2.1cm,bottom=2.0cm,left=2.0cm,right=2.0cm,headheight=14pt]{geometry}
\usepackage{fontspec}
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}[Ligatures={NoCommon}]}{\setmainfont{FreeSerif}}
\newfontfamily\fbfont{FreeSerif}\usepackage{newunicodechar}\newunicodechar{₹}{{\fbfont ₹}}\newunicodechar{★}{{\fbfont ★}}\newunicodechar{☆}{{\fbfont ☆}}\newunicodechar{▶}{{\fbfont ▶}}\newunicodechar{ﬀ}{ff}\newunicodechar{ﬁ}{fi}\newunicodechar{ﬂ}{fl}\newunicodechar{ﬃ}{ffi}\newunicodechar{ﬄ}{ffl}
\usepackage{xcolor}
\definecolor{navy}{HTML}{0B1F3A}\definecolor{navy2}{HTML}{1E3A6E}
\definecolor{gold}{HTML}{A8811C}\definecolor{goldl}{HTML}{C9A227}\definecolor{goldbg}{HTML}{FBF6E9}
\definecolor{saffron}{HTML}{FF9933}\definecolor{saffront}{HTML}{B35400}
\definecolor{chakra}{HTML}{000080}\definecolor{igreen}{HTML}{138808}\definecolor{igreent}{HTML}{0E6B06}
\definecolor{l1bg}{HTML}{FFF4E8}\definecolor{l2bg}{HTML}{EEF0FF}\definecolor{l3bg}{HTML}{EEF8EC}
\definecolor{unitline}{HTML}{9FB0CC}\definecolor{unitbg}{HTML}{EEF2F9}\definecolor{rowbg}{HTML}{F5F7FA}
\definecolor{muted}{HTML}{5B6678}
\definecolor{lay0}{HTML}{0B1F3A}\definecolor{lay1}{HTML}{16305A}\definecolor{lay2}{HTML}{1E3A6E}\definecolor{lay3}{HTML}{2B4B8A}\definecolor{lay4}{HTML}{0F5E5A}\definecolor{lay5}{HTML}{138808}
\usepackage{amssymb}\usepackage{graphicx,tabularx,longtable,booktabs,colortbl,array,multicol,enumitem,fancyhdr,titlesec,tikz}
\usepackage[most]{tcolorbox}
\usepackage[hidelinks]{hyperref}\usepackage{xurl}
\hypersetup{pdftitle={Enterprise AI Product Development Curriculum 2026-27},pdfauthor={Dr S Satyanarayana},pdfsubject={Industry-aligned syllabus: """ + str(N) + r""" courses}}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\renewcommand{\arraystretch}{1.25}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\scriptsize\color{navy}\textsc{Enterprise AI Product Development Curriculum}}
\fancyhead[R]{\scriptsize\bfseries\color{gold}Industry-Aligned Syllabus}
\fancyfoot[L]{\scriptsize\color{navy}Dr S Satyanarayana Ph.D., PDF(AI), FARSC}
\fancyfoot[R]{\scriptsize\color{navy}\thepage}
\renewcommand{\headrule}{\color{goldl}\hrule height 0.8pt}
\titleformat{\section}{\Large\bfseries\color{navy}}{}{0pt}{}[\vspace{-2pt}{\color{goldl}\titlerule[0.8pt]}]
\titleformat{\subsection}{\large\bfseries\color{navy}}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{9pt}{3pt}
\setlist[itemize]{leftmargin=14pt,itemsep=1pt,topsep=2pt,label={\color{goldl}\small$\blacktriangleright$}}
\setlist[enumerate]{leftmargin=18pt,itemsep=1pt,topsep=2pt}
\newcommand{\chip}[1]{\tcbox[on line,colback=goldbg,colframe=goldl!70,boxrule=0.5pt,arc=2pt,boxsep=0pt,left=3pt,right=3pt,top=1.5pt,bottom=1.5pt,fontupper=\scriptsize\bfseries\color{navy}]{#1}\hspace{1pt}\allowbreak}
\newcommand{\cnum}[2]{\tcbox[on line,colback=#1,colframe=#1,arc=2pt,boxsep=0pt,left=3pt,right=3pt,top=1pt,bottom=1pt,fontupper=\scriptsize\bfseries\color{white}]{#2}\hspace{1pt}}
\newcommand{\hdr}{\rowcolor{navy}}
\newcommand{\hw}[1]{\textcolor{white}{\bfseries #1}}
\tcbset{unitbox/.style={enhanced,breakable,colback=white,colframe=unitline,boxrule=0.6pt,arc=2pt,left=6pt,right=6pt,top=4pt,bottom=4pt,colbacktitle=unitbg,coltitle=navy,fonttitle=\small\bfseries,toptitle=1pt,bottomtitle=1pt}}
\begin{document}
""")

# ------------------------------------------------------------------ cover
tracks_core = " \\textbullet{} ".join(e(c["title"]) for c in C if c["track"] == "core")
tracks_em = " \\textbullet{} ".join(e(c["title"]) for c in C if c["track"] == "em")
w(r"""\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
\fill[saffron] (current page.north west) rectangle ([yshift=-1.3cm]current page.north east);
\fill[white] ([yshift=-1.3cm]current page.north west) rectangle ([yshift=-1.45cm]current page.north east);
\fill[igreen] (current page.south west) rectangle ([yshift=1.3cm]current page.south east);
\begin{scope}[shift={([yshift=-6.3cm]current page.north)}]
\draw[chakra,line width=2.2pt] (0,0) circle (2.1cm);\fill[chakra] (0,0) circle (0.28cm);
\foreach \a in {0,15,...,345}{\draw[chakra,line width=0.7pt] (0,0) -- (\a:2.1cm);\fill[chakra] (\a+7.5:2.1cm) circle (1.2pt);}
\end{scope}
\node[anchor=north west] at ([xshift=1.6cm,yshift=-1.9cm]current page.north west) {\includegraphics[width=2.8cm]{algoprofessor-logo.pdf}};
\end{tikzpicture}
\vspace*{8.2cm}
\begin{center}
{\small\bfseries\color{gold}\textsc{Industry-Aligned Course Syllabus}}\\[10pt]
{\fontsize{34}{40}\selectfont\bfseries\color{navy}Enterprise AI\\Product Development}\\[12pt]
{\large\color{navy2}""" + WORD + r""" Courses \quad$\cdot$\quad Five Units Each \quad$\cdot$\quad Three Tracks}\\[14pt]
{\bfseries\color{gold}Core AI Track}\\[2pt]
\begin{minipage}{0.86\textwidth}\centering\small """ + tracks_core + r"""\end{minipage}\\[8pt]
{\bfseries\color{igreen}Emerging Technologies Track}\\[2pt]
\begin{minipage}{0.86\textwidth}\centering\small """ + tracks_em + r"""\end{minipage}\\[8pt]
{\bfseries\color{gold}Industry Practice Track}\\[2pt]
{\small Forward Deployed Engineering (FDE)}\\[12pt]
{\small\bfseries\color{navy2}Core Competencies \;|\; Five-Unit Curriculum \;|\; Industry Tools \& Hands-on Outcomes\\[2pt]
\color{gold}Skills, Jobs \& Salaries \;|\; 10 Enterprise Products \;|\; 10 Unicorn-Track Products}\\[18pt]
{\large\bfseries\color{navy}Dr S Satyanarayana Ph.D., PDF(AI), FARSC}\\[2pt]
{\small\color{navy2}AlgoProfessor AI R\&D Solutions, Hyderabad}\\[6pt]
{\footnotesize\color{gold}Curriculum Edition 2026--27 \;$\cdot$\; Updated Edition, November 2026}\\[4pt]
{\footnotesize\color{muted}Interactive 3D edition: \href{https://drssnaiml1-cell.github.io/enterprise-ai-syllabus/}{drssnaiml1-cell.github.io/enterprise-ai-syllabus}}
\end{center}
\newpage
""")

# ------------------------------------------------------------------ letter
w(r"""\begin{tcolorbox}[colback=white,colframe=goldl,boxrule=0.8pt,arc=0pt,borderline south={2.5pt}{0pt}{igreen},borderline north={2.5pt}{0pt}{saffron},halign=center]
{\Large\bfseries\color{navy}A Message to Vice-Chancellors, Deans and Heads of Department}\\[2pt]
{\small\bfseries\color{gold}AlgoProfessor AI R\&D Solutions, Hyderabad}
\end{tcolorbox}
\hfill{\small November 2026}

Respected Vice-Chancellors, Deans and Heads of Department,

Between now and 2035, every graduate in engineering, science and management will work beside AI systems, and many will build them. Employers no longer ask whether a student has studied AI; they ask whether the student has \textbf{built, deployed and governed an AI product}. Universities that close this gap first will lead in placements, research output, accreditation outcomes and rankings.

This syllabus was written to close that gap. It offers \textbf{""" + word + r""" industry-aligned courses}: ten in core AI, five in emerging technologies and a capstone practice course in \textbf{Forward Deployed Engineering}, the fastest-growing AI role of 2026. Every course has five units, a hands-on outcome for every unit, current industry tools, an enterprise capstone, recommended industry certifications, the skills, jobs and salary outlook it leads to, and the programming languages that will matter through 2035. Ten real-time enterprise products and ten unicorn-track products show how the courses combine into systems that industry runs. It fits NEP 2020's emphasis on multidisciplinary, skill-based and outcome-based learning, and its CO--Bloom mapping supports OBE documentation for NBA and NAAC.

A strong syllabus is only the first step. Results come from trained faculty, working laboratories, real projects and steady review. \textbf{AlgoProfessor AI R\&D Solutions} offers end-to-end consultancy so your institution can adopt this curriculum quickly and deliver it with industry quality:

\begin{tcolorbox}[colback=goldbg,colframe=goldbg,arc=2pt,left=4pt,right=4pt,borderline west={3pt}{0pt}{chakra}]
\small\begin{tabularx}{\linewidth}{@{}>{\leavevmode\bfseries\color{chakra}}p{3.3cm}Y@{}}
For Vice-Chancellors & A future-ready academic brand, higher placements and rankings, research and patent output, and a centre of excellence that attracts students, industry partners and funding.\\
For Deans & A board-of-studies-ready curriculum across departments, OBE and accreditation evidence, and a measurable plan for faculty capability.\\
For Heads of Department & Course files, lab manuals, GitHub repositories, trained faculty, live student projects and certification-ready students from the first semester of adoption.\\
\end{tabularx}
\end{tcolorbox}

I invite you to partner with us to make your institution a model of AI-ready higher education for India. Together we can prepare graduates who do not just use AI, but lead it.

With regards,\\[2pt]
{\bfseries\color{navy}Dr S Satyanarayana Ph.D., PDF(AI), FARSC}\\
{\small Agentic AI Scientist $\cdot$ Founder \& CEO, AlgoProfessor $\cdot$ Creator of AlgoLang\\AlgoProfessor AI R\&D Solutions, Hyderabad\\Editor-in-Chief, IJCMI\\
{\color{gold}\bfseries Partnership enquiries: cto@algoprofessor.com \quad|\quad www.algoprofessor.com}}
\newpage
""")

# ------------------------------------------------------------------ consultancy
SVC = [("Curriculum Adoption \\& Customisation", f"Adapt these {N} courses to your regulations, credit structure and semester plan; Board of Studies documents, course files and CO--PO--PSO mapping."),
       ("Faculty Development Programmes", "Hands-on FDPs and train-the-trainer bootcamps for every course, taught by practitioners, with teaching kits, slides and assessment banks."),
       ("AI \\& Emerging-Tech Laboratory Set-up", "Design of GPU, edge, robotics, quantum-simulation and SOC labs; software stacks, cloud credits guidance and complete lab manuals."),
       ("GitHub Course Repositories", "Complete, version-controlled course repositories with notebooks, code, datasets and solutions for all units and labs, ready for students from day one."),
       ("Industry Capstones \\& Live Projects", "``One Student, One Project'': real enterprise problems, weekly milestones, forward-deployed client projects and GitHub portfolios for UG, PG and Ph.D. scholars."),
       ("Certification Readiness", "Preparation tracks mapped to each course's recommended certifications (AWS, Microsoft, Google Cloud, NVIDIA, Databricks, IBM, CompTIA and others)."),
       ("Centre of Excellence in AI", "Set up and run a university AI Centre of Excellence with research themes, industry partnerships, hackathons and incubation for student start-ups."),
       ("Research, Patents \\& Q1 Publications", "Research mentoring, sponsored projects, patent drafting support and Q1/SCI paper development for faculty and doctoral scholars."),
       ("Accreditation \\& Ranking Support", "OBE evidence, outcome attainment and documentation for NBA, NAAC, NIRF and international rankings built from this curriculum."),
       ("Placement \\& Career Readiness", "Role-based training for AI Engineer, Agentic AI, Forward Deployed, Data, Cybersecurity and Physical AI careers; interview preparation and industry connect.")]
w(r"\section*{AlgoProfessor Consultancy Services for this Curriculum}\addcontentsline{toc}{section}{AlgoProfessor Consultancy Services}")
w("AlgoProfessor supports universities at every stage, from adopting the syllabus to producing industry-ready graduates, for all " + word + " courses: " + ", ".join(e(c["title"]) for c in C[:-1]) + ", and " + e(C[-1]["title"]) + ".\n")
w(r"\begin{tcbraster}[raster columns=2,raster equal height=rows,raster column skip=8pt,raster row skip=6pt]")
for i, (t, d) in enumerate(SVC):
    col = ["saffron", "chakra", "igreen"][i % 3]
    w(r"\begin{tcolorbox}[colback=white,colframe=" + col + r"!60,boxrule=0.6pt,arc=2pt,left=5pt,right=5pt,top=3pt,bottom=3pt,borderline north={2.5pt}{0pt}{" + col + r"}]{\small\bfseries\color{navy}" + f"{i+1}. {t}" + r"}\\[1pt]{\footnotesize " + d + r"}\end{tcolorbox}")
w(r"\end{tcbraster}")
w(r"\subsection*{Engagement Models}")
w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\bfseries}p{2.9cm}Y>{\raggedright\arraybackslash}p{4.2cm}@{}}\hdr\hw{Model}&\hw{Scope}&\hw{Best suited for}\\")
w(r"Pilot & One or two courses, FDP, lab manual and GitHub repository for one department & Departments starting their AI journey\\\rowcolor{rowbg}")
w(r"Department Programme & The full core AI track (10 courses) plus Forward Deployed Engineering, with labs, capstones and certification preparation & AI \& DS, CSE and allied departments\\")
w(r"University Transformation & All " + str(N) + r" courses, Centre of Excellence, research and accreditation support across schools & Universities aiming for AI leadership\\\bottomrule\end{tabularx}}")
w(r"\subsection*{How an Engagement Runs}")
w(r"{\small{\color{saffront}\bfseries Step 1 -- Discover:} meeting with leadership, gap analysis of current syllabus, labs and faculty. {\color{chakra}\bfseries Step 2 -- Design:} customised curriculum, lab plan and faculty roadmap. {\color{igreent}\bfseries Step 3 -- Deliver:} FDPs, lab set-up, GitHub repositories, live projects. {\color{gold}\bfseries Step 4 -- Measure:} outcome attainment, certifications earned, placements and research output, reviewed each semester.}")
w(r"\newpage")

# ------------------------------------------------------------------ contents
w(r"""{\renewcommand{\contentsname}{Contents}\setcounter{tocdepth}{1}\small\tableofcontents}\newpage""")

# ------------------------------------------------------------------ overview
w(r"\section*{Programme Overview}\addcontentsline{toc}{section}{Programme Overview}")
w(r"This curriculum prepares learners to \textbf{design, build, deploy and govern AI products at enterprise scale}. Every course names its top three programming languages with a 2026--2035 outlook. Every unit ends with a concrete \textbf{hands-on outcome} (a working artefact the learner builds), and every course follows the same five-unit arc: \emph{foundations $\rightarrow$ core methods $\rightarrow$ advanced methods $\rightarrow$ engineering for production $\rightarrow$ enterprise deployment, governance and capstone}. Ten core AI courses are complemented by a five-course \textbf{Emerging Technologies Track} and an \textbf{Industry Practice Track} in Forward Deployed Engineering. Each course pairs 45 lecture hours with 30 hours of tool-driven laboratory work and ends with a capstone that produces a deployable product increment.")
w(r"{\small\begin{longtable}{@{}p{0.7cm}p{5.0cm}p{1.5cm}p{1.4cm}p{6.3cm}@{}}\hdr\hw{No.}&\hw{Course}&\hw{Code}&\hw{L--T--P--C}&\hw{Product Focus}\\\endhead")
last = None
for c in C:
    if c["track"] != last and c["track"] != "core":
        col = "igreen" if c["track"] == "em" else "gold"
        w(r"\multicolumn{5}{@{}c@{}}{\cellcolor{" + col + r"}\color{white}\bfseries " + TRACK[c["track"]] + r"}\\")
    last = c["track"]
    w(f"{c['num']} & \\textbf{{{e(c['title'])}}} & {e(c['code'])} & 3--0--2--4 & {e(c['tagline'])}\\\\")
w(r"\bottomrule\end{longtable}}")
w(r"\newpage")

# ------------------------------------------------------------------ assessment + standards
w(r"""\begin{multicols}{2}
\subsection*{Assessment Scheme (per course)}
{\small\begin{tabularx}{\linewidth}{@{}Yr@{}}Continuous lab work \& notebooks & 20\%\\Two mid-term evaluations & 20\%\\Mini-project / sprint reviews & 20\%\\Enterprise capstone (demo + report) & 40\%\\\end{tabularx}}
\subsection*{Bloom's Taxonomy Legend}
{\small L1 Remember \quad L2 Understand \quad L3 Apply\\ L4 Analyse \quad L5 Evaluate \quad L6 Create}
\subsection*{Colour Code for Careers}
{\small\cnum{saffron}{\phantom{0}} Fresher / Entry (0--2 yrs)\\ \cnum{chakra}{\phantom{0}} Mid-level (3--5 yrs)\\ \cnum{igreen}{\phantom{0}} Senior (6+ yrs)}
\columnbreak
\subsection*{Common Product-Engineering Standards}
\begin{itemize}\small
\item Git-based version control, code review and CI/CD on every lab
\item Containerised delivery with Docker; Kubernetes for capstones
\item Experiment tracking, model registry and reproducible environments
\item Model cards, data sheets and risk register for each product
\item Cloud parity: AWS, Azure or GCP; on-prem GPU where available
\item Each course maps to current industry certifications (checked November 2026)
\end{itemize}
\end{multicols}
\subsection*{Industry Certification Policy}
{\small Every course lists industry certifications that match its units, from AWS, Microsoft, Google Cloud, NVIDIA, Databricks, IBM, CompTIA, ISACA, IAPP, the Linux Foundation and others, plus NPTEL/SWAYAM where it fits. Names and exam codes were checked in November 2026. Several well-known exams were retired in 2026 (AWS Machine Learning -- Specialty; Microsoft AI-102, DP-100 and AI-900), so their current replacements are listed instead. Vendors change exams often, so learners should confirm the exam code on the issuer's website before registering. Course certificates (Coursera, edX, NVIDIA DLI) are listed as useful extras, not as replacements for proctored exams.}
\subsection*{Learning Pathway}
{\small{\color{gold}\bfseries Foundation track:} AI $\rightarrow$ ML $\rightarrow$ Data Engineering \quad {\color{gold}\bfseries Model track:} DL $\rightarrow$ CV / RL \quad {\color{gold}\bfseries Frontier track:} LLM $\rightarrow$ Generative AI $\rightarrow$ Agentic AI \quad {\color{gold}\bfseries Cross-cutting:} Trustworthy AI is taken alongside or after any frontier course.\\
{\color{igreent}\bfseries Emerging track:} DL $\rightarrow$ Edge AI / Physical AI \quad ML $\rightarrow$ Quantum AI \quad ML $\rightarrow$ AI Cybersecurity $\rightarrow$ Blockchain \& Decentralised AI\\
{\color{gold}\bfseries Practice track:} LLM + Agentic AI + Data Engineering $\rightarrow$ Forward Deployed Engineering, taken in the final year as the client-embedded capstone of the programme.}
\newpage
""")

# ------------------------------------------------------------------ language strategy
LANGS = [("Python", "1--14, 16", "The working language of AI: models, agents, data and evaluation. AI coding assistants make it even more productive."),
         ("C++ / CUDA", "1, 3, 4, 5, 8, 11, 12, 13", "The performance layer: GPU kernels, inference engines, simulators, robots and edge devices. Demand rises with compute cost."),
         ("Rust", "6, 10, 12, 13, 14, 15", "Memory-safe systems language for AI infrastructure, security, embedded and blockchain; fastest-rising systems language."),
         ("SQL", "2, 9, 16", "The most durable data skill; every AI product depends on well-modelled data."),
         ("TypeScript / JavaScript", "6, 7, 8, 16", "Delivers AI to users: web apps, chat interfaces, MCP servers and agent SDKs."),
         ("Go", "7, 14, 15", "Cloud-native services, agent platforms, security tools and enterprise blockchain."),
         ("Java / Scala", "1, 9", "JVM backbone of enterprise systems and big-data streaming engines."),
         ("Domain languages", "R (2, 10), Julia (4), OpenQASM 3 (11), Solidity (15), Mojo (3, emerging)", "Specialist languages for statistics, scientific computing, quantum circuits, smart contracts and next-generation AI performance.")]
w(r"\section*{Programming Language Strategy 2026--2035}\addcontentsline{toc}{section}{Programming Language Strategy 2026--2035}")
w(r"Every course lists the three programming languages that matter most for building its products, with an outlook to 2035. The plan follows one principle: \emph{Python for intelligence, a systems language for performance and safety, and a delivery language for users and platforms}. Graduates who can work across all three layers can build complete AI products, not just models.")
w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\bfseries}p{3.0cm}>{\raggedright\arraybackslash}p{4.2cm}Y@{}}\hdr\hw{Language}&\hw{Courses (top-3)}&\hw{Why it matters for 2026--2035 engineering}\\")
for i, (a, b, d) in enumerate(LANGS):
    w(("\\rowcolor{rowbg}" if i % 2 else "") + f"{e(a)} & {b} & {e(d)}\\\\")
w(r"\bottomrule\end{tabularx}}")
w(r"""\subsection*{Engineering Outcomes Expected by 2030--2035}
\begin{itemize}\small
\item \textbf{AI-assisted software engineering is the norm:} engineers direct coding agents, so code review, testing, specification and system design matter more than typing code.
\item \textbf{Polyglot by default:} a Python model is served by C++/Rust engines, reached through TypeScript or Go services, and fed by SQL pipelines; graduates must read and reason across these layers.
\item \textbf{Memory safety and security by design:} security guidance increasingly favours memory-safe languages such as Rust for new critical systems.
\item \textbf{Performance engineering is a core skill:} GPU, edge and quantum hardware reward engineers who can optimise below the Python layer.
\item \textbf{Specification and verification:} formal contracts, typed interfaces and evaluation suites become the way humans control AI-written code.
\end{itemize}
{\footnotesize\itshape\color{muted} The 2026--2035 outlook reflects current industry direction and is a planning guide, not a forecast guarantee; review it every academic year.}
\newpage""")

# ------------------------------------------------------------------ courses
def products_for(n):
    a = [p["name"] for p in P if n in p["courses"]]
    b = [u["name"] for u in U["products"] if n in u["courses"]]
    return a, b


last = None
for c in C:
    if c["track"] != last:
        col = {"core": "navy", "em": "igreen", "fde": "gold"}[c["track"]]
        intro = {"core": "Ten courses that take a learner from intelligent decision systems to trustworthy, production-grade AI.",
                 "em": "Five courses on the technologies reshaping AI between 2026 and 2035: quantum, edge, physical AI, security and decentralised trust.",
                 "fde": "The client-embedded capstone course: learners combine the other fifteen courses to discover, build, deploy and scale AI with real enterprises."}[c["track"]]
        if c["track"] != "core":
            w(r"\newpage")
        w(r"\begin{tcolorbox}[colback=" + col + r",colframe=" + col + r",arc=2pt,halign=center,top=6pt,bottom=6pt]{\Large\bfseries\color{white}" + TRACK[c["track"]] + r"}\\[2pt]{\small\color{white}" + intro + r"}\end{tcolorbox}")
        w(r"\addcontentsline{toc}{section}{\textcolor{" + ("gold" if c["track"] != "em" else "igreen") + "}{" + TRACK[c["track"]] + "}}")
        last = c["track"]
    else:
        w(r"\newpage")
    k = K["courses"][str(c["num"])]
    w(r"\phantomsection\addcontentsline{toc}{section}{Course " + str(c["num"]) + r"\quad " + e(c["title"]) + "}")
    w(r"\begin{tcolorbox}[colback=navy,colframe=navy,arc=2pt,left=8pt,top=5pt,bottom=5pt]{\small\bfseries\color{goldl}COURSE " + str(c["num"]) + r" \;|\; " + e(c["code"]) + (r" \;|\; " + TRACK[c["track"]].upper() if c["track"] != "core" else "") + r"}\\[1pt]{\LARGE\bfseries\color{white}" + e(c["title"]) + r"}\\[2pt]{\small\itshape\color{goldl}" + e(c["tagline"]) + r"}\end{tcolorbox}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\bfseries\cellcolor{rowbg}}p{2.3cm}Y>{\bfseries\cellcolor{rowbg}}p{2.3cm}p{2.6cm}@{}}Course Code & " + e(c["code"]) + r" & L--T--P--C & 3--0--2--4\\Prerequisites & " + e(c["prereq"]) + r" & Contact Hours & " + e(c["hours"]) + r"\\\end{tabularx}}")
    w(r"\subsection*{Core Competencies}\begin{itemize}\small")
    for x in c["competencies"]:
        w(r"\item " + e(x))
    w(r"\end{itemize}")
    w(r"\subsection*{Five-Unit Curriculum}")
    for u in c["units"]:
        w(r"\begin{tcolorbox}[unitbox,title={{\color{gold}UNIT " + u["n"] + r"}\quad " + e(u["title"]) + r"\hfill{\color{gold}" + str(u["hours"]) + r" Hours}}]\small " + e(u["topics"]) + r"\par\vspace{2pt}{\color{unitline}\hdashrule}\par\textbf{Hands-on Outcome:} " + e(u["outcome"]) + r"\end{tcolorbox}")
    w(r"\subsection*{Industry Tools \& Platforms}")
    if c["track"] == "fde":
        w(r"{\footnotesize\itshape\color{muted}Course 16 is new in this updated edition (November 2026).}\par")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\leavevmode\bfseries\color{navy}}p{3.6cm}Y@{}}")
    for i, (a, b) in enumerate(c["tools"]):
        w(("\\rowcolor{rowbg}" if i % 2 == 0 else "") + f"{e(a)} & {e(b)}\\\\")
    w(r"\end{tabularx}}")
    w(r"\subsection*{Hands-on Laboratory (30 Hours)}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\leavevmode\bfseries\color{gold}}p{0.6cm}Y>{\leavevmode\bfseries\color{gold}}p{0.6cm}Y@{}}")
    labs = c["labs"]; h = (len(labs) + 1) // 2
    for i in range(h):
        r = labs[i + h] if i + h < len(labs) else ""
        w(("\\rowcolor{rowbg}" if i % 2 == 0 else "") + f"L{i+1} & {e(labs[i])} & {'L'+str(i+h+1) if r else ''} & {e(r)}\\\\")
    w(r"\end{tabularx}}")
    w(r"\subsection*{Course Outcomes}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\bfseries}p{0.9cm}Y>{\raggedright\arraybackslash}p{2.3cm}@{}}\hdr\hw{CO}&\hw{On completion, the learner will be able to}&\hw{Bloom Level}\\")
    for i, x in enumerate(c["cos"]):
        w(("\\rowcolor{rowbg}" if i % 2 else "") + f"{x['co']} & {e(x['text'])} & {e(x['bloom'])}\\\\")
    w(r"\bottomrule\end{tabularx}}")
    w(r"\begin{tcolorbox}[colback=goldbg,colframe=goldl,boxrule=0.7pt,arc=2pt,title={Enterprise Capstone Product},colbacktitle=goldl!35,coltitle=navy,fonttitle=\small\bfseries]\small\textbf{" + e(c["capstone"]["name"]) + r":} " + e(c["capstone"]["desc"]) + r"\end{tcolorbox}")
    # NEW: skills, jobs and salary
    w(r"\subsection*{Skills You Will Gain}\begin{multicols}{2}\begin{itemize}\small")
    for x in k["skills"]:
        w(r"\item " + e(x))
    w(r"\end{itemize}\end{multicols}")
    w(r"\subsection*{Jobs You Can Apply For}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash}p{4.6cm}>{\raggedright\arraybackslash}p{2.5cm}Y@{}}\hdr\hw{Job role}&\hw{Level}&\hw{What the role does}\\")
    for i, j in enumerate(k["jobs"]):
        lc, lt = LVL[j["level"]]
        w(r"\rowcolor{" + lc + "bg}" + r"\textbf{" + e(j["title"]) + r"} & \leavevmode{\color{" + {"l1": "saffront", "l2": "chakra", "l3": "igreent"}[lc] + r"}\bfseries " + lt + r"} & " + e(j["what"]) + r"\\")
    w(r"\end{tabularx}}")
    w(r"{\small\textbf{Industries hiring:} " + e(k["hiring"]) + r"\\[2pt]\textbf{Top companies hiring these skills:} " + e(", ".join(k["companies"])) + "}")
    s = k["salary"]
    w(r"\begin{tcbraster}[raster columns=3,raster column skip=6pt,raster equal height]")
    for col, bg, lab, val in (("saffron", "l1bg", "Fresher / Entry (0--2 yrs)", s["entry"]), ("chakra", "l2bg", "Mid-level (3--5 yrs)", s["mid"]), ("igreen", "l3bg", "Senior (6+ yrs)", s["senior"])):
        tcol = {"saffron": "saffront", "chakra": "chakra", "igreen": "igreent"}[col]
        w(r"\begin{tcolorbox}[colback=" + bg + r",colframe=" + bg + r",arc=2pt,halign=center,borderline north={2.5pt}{0pt}{" + col + r"},top=3pt,bottom=3pt]{\scriptsize\color{muted}" + lab + r"}\\{\large\bfseries\color{" + tcol + r"}₹" + e(val) + r" LPA}\end{tcolorbox}")
    w(r"\end{tcbraster}")
    w(r"{\footnotesize\itshape\color{muted}Indicative annual CTC in India, based on " + e(s["basis"]) + r". See the Salary Guide for sources and caveats.}")
    a, b = products_for(c["num"])
    w(r"\subsection*{Aligned Careers}")
    w(r"{\raggedright " + " ".join(r"\chip{" + e(x) + "}" for x in c["careers"]) + r"\par}")
    if a or b:
        w(r"\par{\small\textbf{Enterprise products using this course:} " + (e("; ".join(a)) if a else "--") + r"\\\textbf{Unicorn-track products using this course:} " + (e("; ".join(b)) if b else "--") + "}")
    w(r"\subsection*{Top 3 Programming Languages (2026--2035 Outlook)}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}p{0.8cm}>{\bfseries}p{2.6cm}YY@{}}\hdr\hw{Rank}&\hw{Language}&\hw{Use in this course}&\hw{2026--2035 engineering outlook}\\")
    for i, (r1, l, use, ol) in enumerate(c["langs"]):
        w(("\\rowcolor{rowbg}" if i % 2 else "") + r"\leavevmode{\color{gold}\bfseries " + e(r1) + "} & " + f"{e(l)} & {e(use)} & {e(ol)}\\\\")
    w(r"\bottomrule\end{tabularx}}")
    w(r"\subsection*{Recommended Industry Certifications}")
    w(r"{\small\begin{tabularx}{\linewidth}{@{}Y>{\raggedright\arraybackslash}p{3.0cm}>{\raggedright\arraybackslash}p{2.2cm}p{1.3cm}@{}}\hdr\hw{Certification}&\hw{Issuer}&\hw{Level}&\hw{Units}\\")
    for i, x in enumerate(c["certs"]):
        w(("\\rowcolor{rowbg}" if i % 2 else "") + f"{e(x['name'])} & {e(x['issuer'])} & {e(x['level'])} & {e(x['units'])}\\\\")
    w(r"\bottomrule\end{tabularx}}")
    w(r"\subsection*{Text \& Reference Books}{\footnotesize\begin{enumerate}[label={[\arabic*]}]")
    for x in c["refs"]:
        w(r"\item " + e(x))
    w(r"\end{enumerate}}")

# ------------------------------------------------------------------ career pathways + matrix
w(r"\newpage\section*{Career Pathways}\addcontentsline{toc}{section}{Career Pathways and Course-to-Career Matrix}")
w(r"Which courses make a learner job-ready for each role. Core courses are essential; recommended extras deepen the profile.")
w(r"{\small\begin{longtable}{@{}>{\raggedright\arraybackslash}p{3.3cm}>{\raggedright\arraybackslash}p{4.8cm}>{\raggedright\arraybackslash}p{2.8cm}>{\raggedright\arraybackslash}p{4.6cm}@{}}\hdr\hw{Target role}&\hw{Core courses}&\hw{Recommended extras}&\hw{Why it matters}\\\endhead")
for i, p in enumerate(K["pathways"]):
    w(("\\rowcolor{rowbg}" if i % 2 else "") + r"\textbf{" + e(p["role"]) + "} & " + e(", ".join(f"{n}. {title_of(n)}" for n in p["courses"])) + " & " + e(", ".join(title_of(n) for n in p["plus"])) + " & " + e(p["note"]) + r"\\")
w(r"\bottomrule\end{longtable}}")
w(r"\newpage\subsection*{Course-to-Career Alignment Matrix}")
cols = "".join("c" for _ in C)
cols = "".join(r">{\centering\arraybackslash}p{0.52cm}" for _ in C)
w(r"{\footnotesize\setlength{\tabcolsep}{2pt}\renewcommand{\arraystretch}{1.55}\begin{tabular}{@{}>{\raggedright\arraybackslash}p{5.0cm}" + cols + r"@{}}\hdr\hw{Career role}" + "".join(r"&\hw{" + str(c["num"]) + "}" for c in C) + r"\\")
for i, p in enumerate(K["pathways"]):
    row = (r"\rowcolor{rowbg}" if i % 2 else "") + r"\textbf{" + e(p["role"]) + "}"
    for c in C:
        n = c["num"]
        if n in p["courses"]:
            row += r"&\cellcolor{goldl!55}\leavevmode{\color{navy}●}"
        elif n in p["plus"]:
            row += r"&\cellcolor{goldbg}\leavevmode{\color{gold}○}"
        else:
            row += "&"
    w(row + r"\\")
w(r"\end{tabular}}")
w(r"\par{\footnotesize\colorbox{goldl!55}{\color{navy}●} Core course for the role \quad \colorbox{goldbg}{\color{gold}○} Recommended extra \quad Courses: " + e("; ".join(f"{c['num']} {c['title']}" for c in C)) + "}")
w(r"\begin{tcolorbox}[colback=goldbg,colframe=goldl,arc=2pt,boxrule=0.6pt]\small\textbf{Graduate profile.} A learner who completes the ten core courses, at least one emerging-track course and Forward Deployed Engineering can take an enterprise problem from data acquisition through model or agent design, production deployment, monitoring and regulatory sign-off, and can lead it inside a client organisation to measured, auditable business impact.\end{tcolorbox}")

# ------------------------------------------------------------------ salary guide
w(r"\newpage\section*{Salary Guide by Course}\addcontentsline{toc}{section}{Salary Guide by Course}")
w(r"{\small\itshape " + e(K["salary_note"]) + "}\n")
w(r"{\small\begin{longtable}{@{}p{0.4cm}>{\raggedright\arraybackslash}p{4.0cm}>{\centering\arraybackslash}p{1.8cm}>{\centering\arraybackslash}p{1.8cm}>{\centering\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{4.9cm}@{}}\hdr\hw{\#}&\hw{Course}&\cellcolor{saffron}\hw{Fresher}&\cellcolor{chakra}\hw{Mid (3--5)}&\cellcolor{igreen}\hw{Senior (6+)}&\hw{Top companies hiring}\\\endhead")
for c in C:
    s = K["courses"][str(c["num"])]["salary"]
    co = K["courses"][str(c["num"])]["companies"][:5]
    w(f"{c['num']} & \\textbf{{{e(c['title'])}}} & \\cellcolor{{l1bg}}\\leavevmode{{\\color{{saffront}}\\bfseries ₹{e(s['entry'])}}} & \\cellcolor{{l2bg}}\\leavevmode{{\\color{{chakra}}\\bfseries ₹{e(s['mid'])}}} & \\cellcolor{{l3bg}}\\leavevmode{{\\color{{igreent}}\\bfseries ₹{e(s['senior'])}}} & {e(', '.join(co))}\\\\")
w(r"\bottomrule\end{longtable}}")
w(r"{\footnotesize Figures in ₹ lakh per annum (LPA). Company names are examples of employers that hire for these skill sets, not current openings or endorsements.}")
w(r"\subsection*{Salary Sources}{\scriptsize\begin{enumerate}[label={[\arabic*]},itemsep=0pt]")
for a, b in K["salary_sources"]:
    w(r"\item " + e(a) + r". \url{" + b.replace("%", r"\%").replace("#", r"\#") + "}")
w(r"\end{enumerate}}")

# ------------------------------------------------------------------ enterprise products
w(r"\newpage\section*{Top 10 Real-Time Enterprise Products}\addcontentsline{toc}{section}{Top 10 Real-Time Enterprise Products}")
w(r"One flagship product per industry domain. Each combines several courses into a real-time, production-grade system that student teams can build as a capstone and that enterprises actually run. The KPIs are the measures each product improves, not promised results.")
w(r"{\small\begin{tabularx}{\linewidth}{@{}p{0.5cm}>{\raggedright\arraybackslash}p{3.6cm}Y>{\raggedright\arraybackslash}p{2.6cm}@{}}\hdr\hw{\#}&\hw{Domain}&\hw{Enterprise product}&\hw{Courses}\\")
for i, p in enumerate(P):
    w(("\\rowcolor{rowbg}" if i % 2 else "") + f"{p['id']} & {e(p['domain'])} & \\textbf{{{e(p['name'])}}} & {', '.join(map(str, p['courses']))}\\\\")
w(r"\bottomrule\end{tabularx}}")
for p in P:
    w(r"\begin{tcolorbox}[enhanced,breakable,colback=white,colframe=navy,boxrule=0.6pt,arc=2pt,title={\color{goldl}PRODUCT " + str(p["id"]) + r" \;|\; " + e(p["domain"]).upper() + r"\\\color{white}\large " + e(p["name"]) + r"},colbacktitle=navy,fonttitle=\small\bfseries]")
    w(r"{\small\itshape\color{muted}" + e(p["tagline"]) + r"}\par")
    w(r"\begin{tcolorbox}[colback=l1bg,colframe=l1bg,arc=2pt,borderline west={3pt}{0pt}{saffron},top=2pt,bottom=2pt]\small\textbf{Business problem:} " + e(p["problem"]) + r"\end{tcolorbox}")
    w(r"\begin{tcolorbox}[colback=l3bg,colframe=l3bg,arc=2pt,borderline west={3pt}{0pt}{igreen},top=2pt,bottom=2pt]\small\textbf{What happens in real time:} " + e(p["realtime"]) + r"\end{tcolorbox}")
    w(r"{\small\textbf{Product modules}}\begin{enumerate}\small")
    for m in p["modules"]:
        w(r"\item " + e(m))
    w(r"\end{enumerate}")
    w(r"{\small\textbf{Courses that build it:} " + e(", ".join(f"{n}. {title_of(n)}" for n in p["courses"])) + r"\\\textbf{Technology stack:} " + e(", ".join(p["stack"])) + r"\\\textbf{Business KPIs it moves:} " + e(", ".join(p["kpis"])) + r"\\\textbf{Job roles it showcases:} " + e(", ".join(p["roles"])) + r"\\\textbf{Context:} " + e(p["context"]) + "}")
    w(r"\end{tcolorbox}")

# ------------------------------------------------------------------ unicorn track
w(r"\newpage\section*{Unicorn Track: 10 Frontier Products}\addcontentsline{toc}{section}{Unicorn Track: 10 Frontier Products}")
w(e(U["intro"]))
w(r"{\small\begin{tabularx}{\linewidth}{@{}p{0.4cm}>{\raggedright\arraybackslash}p{3.6cm}Y>{\centering\arraybackslash}p{1.8cm}>{\raggedright\arraybackslash}p{2.3cm}@{}}\hdr\hw{\#}&\hw{2026 unicorn category}&\hw{Frontier product}&\hw{Complexity}&\hw{Courses}\\")
for i, u in enumerate(U["products"]):
    w(("\\rowcolor{rowbg}" if i % 2 else "") + f"{u['id']} & {e(u['category'])} & \\textbf{{{e(u['name'])}}} & \\leavevmode{{\\color{{gold}}{'★' * u['complexity']}{'☆' * (5 - u['complexity'])}}} & {', '.join(map(str, u['courses']))}\\\\")
w(r"\bottomrule\end{tabularx}}")
w(r"{\footnotesize\itshape\color{muted}Company names show the market category each idea comes from. They are not partners or endorsements of AlgoProfessor.}")
LCOL = ["0B1F3A", "16305A", "1E3A6E", "2B4B8A", "0F5E5A", "138808"]
for u in U["products"]:
    w(r"\newpage")
    w(r"\begin{tcolorbox}[colback=navy,colframe=navy,arc=2pt,left=8pt,top=5pt,bottom=5pt]{\small\bfseries\color{goldl}UNICORN TRACK " + str(u["id"]) + r" \;|\; " + e(u["category"]).upper() + r"}\\[1pt]{\LARGE\bfseries\color{white}" + e(u["name"]) + r"}\\[2pt]{\small\itshape\color{goldl}" + e(u["tagline"]) + r"}\\[2pt]{\small\color{white}Complexity {\color{goldl}" + "★" * u["complexity"] + "☆" * (5 - u["complexity"]) + r"} \;$\cdot$\; " + str(len(u["courses"])) + r" courses \;$\cdot$\; " + str(len(u["layers"])) + r" system layers}\end{tcolorbox}")
    w(r"\begin{tcolorbox}[colback=l1bg,colframe=l1bg,arc=2pt,borderline west={3pt}{0pt}{saffron},top=2pt,bottom=2pt]\small\textbf{Why now:} " + e(u["signal"]) + r" {\color{muted}Category examples: " + e(", ".join(u["refs"])) + r".}\end{tcolorbox}")
    w(r"\begin{tcolorbox}[colback=l3bg,colframe=l3bg,arc=2pt,borderline west={3pt}{0pt}{igreen},top=2pt,bottom=2pt]\small\textbf{What the product does:} " + e(u["what"]) + r"\end{tcolorbox}")
    w(r"\subsection*{System Architecture (top to bottom)}")
    for i, l in enumerate(u["layers"]):
        hname, rest = l.split(":", 1)
        w(r"\begin{tcolorbox}[colback=lay" + str(i % 6) + r",colframe=lay" + str(i % 6) + r",arc=2pt,top=1.5pt,bottom=1.5pt,left=6pt,before skip=2pt,after skip=2pt]\small\color{white}{\color{goldl}\bfseries " + str(i + 1) + ". " + e(hname) + ":}" + e(rest) + r"\end{tcolorbox}")
    w(r"\subsection*{Hard Problems: The Moat}\begin{itemize}\small")
    for m in u["moats"]:
        w(r"\item " + e(m))
    w(r"\end{itemize}")
    w(r"\subsection*{From Capstone to Company}")
    w(r"\begin{tcbraster}[raster columns=2,raster equal height,raster column skip=8pt]\begin{tcolorbox}[colback=l1bg,colframe=l1bg,arc=2pt,borderline north={2.5pt}{0pt}{saffron}]{\scriptsize\bfseries\color{muted}12-WEEK TEAM MVP}\\\small " + e(u["mvp"]) + r"\end{tcolorbox}\begin{tcolorbox}[colback=l3bg,colframe=l3bg,arc=2pt,borderline north={2.5pt}{0pt}{igreen}]{\scriptsize\bfseries\color{muted}VENTURE-SCALE PLATFORM}\\\small " + e(u["scale"]) + r"\end{tcolorbox}\end{tcbraster}")
    w(r"{\small\textbf{Business model:} " + e(u["business"]) + r"\\\textbf{Courses that build it:} " + e(", ".join(f"{n}. {title_of(n)}" for n in u["courses"])) + r"\\\textbf{Technology stack:} " + e(", ".join(u["stack"])) + r"\\\textbf{Roles it prepares you for:} " + e(", ".join(u["roles"])) + "}")
w(r"\subsection*{Market Sources for the Unicorn Track}{\scriptsize\begin{enumerate}[label={[\arabic*]},itemsep=0pt]")
for a, b in U["sources"]:
    w(r"\item " + e(a) + r". \url{" + b.replace("%", r"\%").replace("#", r"\#") + "}")
w(r"\end{enumerate}}")

# ------------------------------------------------------------------ back cover
w(r"""\newpage\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
\fill[saffron] (current page.north west) rectangle ([yshift=-1.3cm]current page.north east);
\fill[igreen] (current page.south west) rectangle ([yshift=1.3cm]current page.south east);
\begin{scope}[shift={([yshift=-5.6cm]current page.north)}]
\draw[chakra,line width=1.8pt] (0,0) circle (1.6cm);\fill[chakra] (0,0) circle (0.22cm);
\foreach \a in {0,15,...,345}{\draw[chakra,line width=0.6pt] (0,0) -- (\a:1.6cm);}
\end{scope}
\end{tikzpicture}
\vspace*{6.6cm}
\begin{center}
{\small\bfseries\color{gold}\textsc{Partner with AlgoProfessor}}\\[8pt]
{\fontsize{26}{32}\selectfont\bfseries\color{navy}Build an AI-Ready University\\for 2026--2035}\\[10pt]
{\color{goldl}\rule{4cm}{1pt}}\\[8pt]
\begin{minipage}{0.8\textwidth}\centering
Curriculum adoption \textbullet{} Faculty development \textbullet{} AI \& emerging-tech labs \textbullet{} GitHub course repositories \textbullet{} Industry capstones \textbullet{} Forward-deployed client projects \textbullet{} Certification readiness \textbullet{} Centre of Excellence \textbullet{} Research \& Q1 publications \textbullet{} Accreditation \& ranking support \textbullet{} Placement \& career readiness
\end{minipage}\\[16pt]
\begin{tcolorbox}[width=0.62\textwidth,colback=white,colframe=goldl,arc=2pt,halign=center,borderline north={2.5pt}{0pt}{saffron},borderline south={2.5pt}{0pt}{igreen}]
{\bfseries\color{chakra}Vice-Chancellors, Deans and HoDs: contact us to schedule a curriculum consultation}\\[6pt]
{\large\bfseries\color{gold}cto@algoprofessor.com}\\[2pt]
www.algoprofessor.com\\
{\small University partnerships: campus.algoprofessor.com}\\
{\small Explore in 3D: drssnaiml1-cell.github.io/enterprise-ai-syllabus}
\end{tcolorbox}
\vspace{12pt}
\includegraphics[width=3.4cm]{algoprofessor-logo.pdf}\\[4pt]
{\bfseries\color{navy}AlgoProfessor AI R\&D Solutions}\\
{\small Hyderabad, India}\\[4pt]
{\small\itshape\color{igreent}Design \textbullet{} Training \textbullet{} Research \textbullet{} Innovation \textbullet{} Consultancy}
\end{center}
\end{document}""")

tex = "\n".join(out)
tex = tex.replace("\n{\\small\\begin{tabularx}", "\n\\par{\\small\\begin{tabularx}")
tex = tex.replace(r"{\color{unitline}\hdashrule}", r"\noindent{\color{unitline}\leaders\hbox to 4pt{\hss\rule[0.6ex]{2pt}{0.4pt}\hss}\hfill\kern0pt}")
os.makedirs(os.path.join(ROOT, "latex"), exist_ok=True)
open(os.path.join(ROOT, "latex", "Enterprise_AI_Syllabus.tex"), "w", encoding="utf-8").write(tex)
print(f"latex/Enterprise_AI_Syllabus.tex written: {N} courses, {len(tex):,} characters")
