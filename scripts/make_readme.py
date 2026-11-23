"""Generate README.md from the data files (same source as the website).

Usage:  python3 scripts/make_readme.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda f: json.load(open(os.path.join(ROOT, "data", f), encoding="utf-8"))
C = D("courses.json")
xp = os.path.join(ROOT, "data", "extra_courses.json")
if os.path.exists(xp):
    C += json.load(open(xp, encoding="utf-8"))
for c in C:
    c.setdefault("track", "core" if c["num"] <= 10 else "em")
K, P, U = D("careers.json"), D("products.json"), D("unicorn.json")
SITE = "https://drssnaiml1-cell.github.io/enterprise-ai-syllabus/"
LV = {"Entry": "🟠 Fresher / Entry", "Mid": "🔵 Mid (3–5 yrs)", "Senior": "🟢 Senior (6+ yrs)"}
KEY = "**Colour code:** 🟠 Saffron = Fresher / Entry (0–2 yrs) · 🔵 Chakra navy = Mid-level (3–5 yrs) · 🟢 Green = Senior (6+ yrs)"
TITLE = lambda n: C[n - 1]["title"]

n_c = len(C)
n_u = sum(len(c["units"]) for c in C)
n_l = sum(len(c["labs"]) for c in C)
n_h = n_c * 75
n_cert = sum(len(c["certs"]) for c in C)
WORDS = {15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen"}

o = []
w = o.append
w('<p align="center">\n  <img src="assets/algoprofessor-logo.svg" alt="AlgoProfessor logo" width="170">\n</p>\n')
w('<h1 align="center">Enterprise AI Product Development Curriculum</h1>\n')
w(f'<p align="center"><b>Industry-aligned syllabus · {WORDS.get(n_c, n_c)} courses · Five units each · Curriculum Edition 2026–27</b></p>\n')
w('<p align="center">')
w(f'  <a href="{SITE}"><img src="https://img.shields.io/badge/Website-3D%20Live%20Syllabus-0B1F3A?style=for-the-badge&logo=googlechrome&logoColor=C9A227" alt="Live website"></a>')
w('  <a href="Enterprise_AI_Syllabus.pdf"><img src="https://img.shields.io/badge/Download-Syllabus%20PDF-A8811C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Syllabus PDF"></a>')
w('  <a href="mailto:cto@algoprofessor.com"><img src="https://img.shields.io/badge/Partner-cto%40algoprofessor.com-138808?style=for-the-badge&logo=maildotru&logoColor=white" alt="Partnership email"></a>')
w('</p>\n\n<p align="center">')
w(f'  <img src="https://img.shields.io/badge/Courses-{n_c}-FF9933?style=flat-square" alt="{n_c} courses">')
w(f'  <img src="https://img.shields.io/badge/Units-{n_u}-000080?style=flat-square" alt="{n_u} units">')
w(f'  <img src="https://img.shields.io/badge/Labs-{n_l}-138808?style=flat-square" alt="{n_l} labs">')
hrs = f"{n_h:,}"
w(f'  <img src="https://img.shields.io/badge/Contact%20hours-{hrs.replace(",", "%2C")}-A8811C?style=flat-square" alt="{hrs} contact hours">')
w(f'  <img src="https://img.shields.io/badge/Certifications-{n_cert}-FF9933?style=flat-square" alt="{n_cert} certifications">')
w('  <img src="https://img.shields.io/badge/NEP%202020-OBE%20%C2%B7%20NBA%20%C2%B7%20NAAC-0B1F3A?style=flat-square" alt="NEP 2020, OBE, NBA, NAAC">')
w('</p>\n\n---\n')

w("## About\n")
w("This curriculum prepares learners to **design, build, deploy and govern AI products at enterprise scale**. Ten core AI courses are complemented by a five-course **Emerging Technologies Track** and an **Industry Practice Track** in **Forward Deployed Engineering (FDE)**, where learners embed with real clients to deploy AI that delivers measured business value. Every course:\n")
w("- has **five units**, each ending in a concrete **hands-on outcome** (a working artefact the learner builds);")
w("- pairs **45 lecture hours with 30 hours of tool-driven lab work** (L–T–P–C 3–0–2–4) and **8 labs**;")
w("- maps **five course outcomes to Bloom levels** for OBE, NBA and NAAC documentation;")
w("- ends in an **enterprise capstone product**, with **recommended industry certifications**, skills, jobs, salary bands and the **top three programming languages** for 2026–2035.\n")
w("Every course follows one arc: **foundations → core methods → advanced methods → production engineering → enterprise deployment, governance and capstone.**\n")
w("**🎞️ Presentation:** [Enterprise_AI_Curriculum_Slides.pdf](slides/Enterprise_AI_Curriculum_Slides.pdf) (33 slides, 16:9, LaTeX Beamer source in [`slides/`](slides/)): curriculum at a glance, three tracks, five-unit arc, all 16 courses with skills, jobs and salaries, salary range chart, career matrix, language strategy, enterprise and unicorn-track products, FDE spotlight and consultancy.\n")
w("**📊 PowerPoint deck:** [Enterprise_AI_Curriculum.pptx](slides/Enterprise_AI_Curriculum.pptx) (37 editable slides with speaker notes, Indian-tricolour colour code, track-coloured course-to-career matrix) · [PDF preview](slides/Enterprise_AI_Curriculum_PowerPoint.pdf) · generator [`scripts/make_pptx.js`](scripts/make_pptx.js).\n")
w("**📘 Syllabus book:** [Enterprise_AI_Syllabus.pdf](Enterprise_AI_Syllabus.pdf) (updated edition, November 2026: all 16 courses plus skills, jobs, salaries, career pathways, 10 enterprise products and 10 unicorn-track products), with its LaTeX source in [`latex/`](latex/).\n")
w(f"**🌐 Explore it as a 3D interactive website:** **{SITE}** (click any course in the 3D orbit to see its units, labs, outcomes, skills, jobs, salaries and the products it builds).\n")
w(f"**💻 Companion syllabus, Enterprise Programming Languages:** [Programming_Languages_Syllabus.pdf](programming-languages/Programming_Languages_Syllabus.pdf) (23 pages): five courses in **Python, Go, Rust, Scala and Java**, each with five units and hands-on outcomes, industry tools, 8 labs, CO–Bloom mapping, an enterprise capstone, certifications and a 2026–2035 outlook. Course-by-course summary in [`programming-languages/`](programming-languages/), LaTeX source in [`programming-languages/latex/`](programming-languages/latex/), and all five courses on the website at [#proglang]({SITE}#proglang).\n")


def course_table(track):
    rows = [c for c in C if c["track"] == track]
    w("| # | Code | Course | Product focus | Top 3 languages |\n|:-:|:--|:--|:--|:--|")
    for c in rows:
        w(f"| {c['num']} | `{c['code']}` | [{c['title']}]({SITE}#course-{c['num']}) | {c['tagline']} | {', '.join(c['languages'])} |")
    w("")


w("## Core AI Track\n"); course_table("core")
w("## Emerging Technologies Track\n"); course_table("em")
w("## Industry Practice Track: Forward Deployed Engineering\n")
w("Forward Deployed Engineering is the delivery layer of enterprise AI: engineers embed with a client, find the problem worth solving, build on the client's own data and systems, and stay until the solution is adopted and its value is measured. This course turns the rest of the curriculum into client-ready practice.\n")
course_table("fde")
for c in [c for c in C if c["track"] == "fde"]:
    w(f"**Prerequisites:** {c['prereq']} · **Hours:** {c['hours']}\n")
    w("| Unit | Title | Hands-on outcome |\n|:-:|:--|:--|")
    for u in c["units"]:
        w(f"| {u['n']} | **{u['title']}** | {u['outcome']} |")
    w(f"\n**Capstone, {c['capstone']['name']}:** {c['capstone']['desc'][0].upper() + c['capstone']['desc'][1:]}\n")
    w("**Course outcomes:** " + " · ".join(f"{x['co']} ({x['bloom']}) {x['text']}" for x in c["cos"]) + "\n")
    w("**Recommended certifications:** " + "; ".join(f"{x['name']} ({x['issuer']}, {x['level']})" for x in c["certs"]) + "\n")

w("## Top 10 Real-Time Enterprise Products\n")
w(f"One flagship product per industry domain. Each combines several courses into a real-time, production-grade system that student teams build as a capstone and enterprises actually run. [Explore the product blueprints on the website]({SITE}#products).\n")
w("| # | Domain | Enterprise product | What happens in real time | Courses |\n|:-:|:--|:--|:--|:--|")
for p in P:
    w(f"| {p['id']} | {p['icon']} {p['domain']} | [**{p['name']}**]({SITE}#product-{p['id']}) | {p['realtime']} | {', '.join(map(str, p['courses']))} |")
w("")
for p in P:
    w(f"<details>\n<summary><b>{p['icon']} {p['id']}. {p['name']}</b> ({p['domain']})</summary>\n")
    w(f"**Business problem:** {p['problem']}\n\n**Modules**\n")
    w("\n".join(f"{i+1}. {m}" for i, m in enumerate(p["modules"])) + "\n")
    w(f"**Courses that build it:** {', '.join(f'{n}. ' + TITLE(n) for n in p['courses'])}\n")
    w(f"**Technology stack:** {', '.join(p['stack'])}\n\n**Business KPIs:** {', '.join(p['kpis'])}\n")
    w(f"**Job roles it showcases:** {', '.join(p['roles'])}\n\n**Context:** {p['context']}\n\n</details>\n")

w("## Unicorn Track: 10 Frontier Products Inspired by 2026's Unicorn Categories\n")
w(f"{U['intro']} [Explore the venture blueprints on the website]({SITE}#unicorn).\n")
w("| # | Unicorn category | Frontier product | Complexity | Courses |\n|:-:|:--|:--|:-:|:--|")
for u in U["products"]:
    w(f"| {u['id']} | {u['icon']} {u['category']} | [**{u['name']}**]({SITE}#unicorn-{u['id']}) | {'★' * u['complexity']}{'☆' * (5 - u['complexity'])} | {', '.join(map(str, u['courses']))} |")
w("")
for u in U["products"]:
    layers = "\n".join(f"{i+1}. **{l.split(':', 1)[0]}:**{l.split(':', 1)[1]}" for i, l in enumerate(u["layers"]))
    w(f"<details>\n<summary><b>{u['icon']} {u['id']}. {u['name']}</b> ({u['category']})</summary>\n")
    w(f"**Why now:** {u['signal']} _Category examples: {', '.join(u['refs'])}._\n\n**What it does:** {u['what']}\n")
    w(f"**System architecture**\n\n{layers}\n\n**Hard problems (the moat):** {'; '.join(u['moats'])}\n")
    w(f"**12-week team MVP:** {u['mvp']}\n\n**Venture-scale platform:** {u['scale']}\n\n**Business model:** {u['business']}\n")
    w(f"**Courses:** {', '.join(f'{n}. ' + TITLE(n) for n in u['courses'])}\n\n**Stack:** {', '.join(u['stack'])}\n\n**Roles:** {', '.join(u['roles'])}\n\n</details>\n")
w("Company names show the market category each idea comes from; they are not partners or endorsements of AlgoProfessor.\n")
w("<details><summary><b>Market sources</b></summary>\n\n" + "\n".join(f"- [{a}]({b})" for a, b in U["sources"]) + "\n\n</details>\n")

w("## Skills & Jobs by Course\n")
w(KEY + "\n")
w("Every course ends with job-ready skills and a GitHub portfolio (five unit artefacts, eight lab projects and an enterprise capstone).\n")
for c in C:
    k = K["courses"][str(c["num"])]
    w(f"<details>\n<summary><b>{c['num']}. {c['title']}</b> ({c['code']}): {', '.join(j['title'] for j in k['jobs'][:3])} …</summary>\n")
    w("**Skills you will gain**\n\n" + "\n".join(f"- {s}" for s in k["skills"]) + "\n")
    w("**Jobs you can apply for**\n\n| Job role | Level | What the role does |\n|:--|:--|:--|")
    w("\n".join(f"| **{j['title']}** | {LV[j['level']]} | {j['what']} |" for j in k["jobs"]) + "\n")
    w(f"**Industries hiring:** {k['hiring']}\n\n**Top companies hiring these skills:** {', '.join(k['companies'])}\n")
    s = k["salary"]
    w(f"**Indicative salary in India (CTC):** 🟠 Fresher ₹{s['entry']} LPA · 🔵 Mid (3–5 yrs) ₹{s['mid']} LPA · 🟢 Senior (6+ yrs) ₹{s['senior']} LPA\n")
    w(f"**Capstone for your portfolio:** {c['capstone']['name']}\n\n</details>\n")

w("## Salary Guide by Course\n")
w(KEY + "\n\n_" + K["salary_note"] + "_\n")
w("| # | Course | 🟠 Fresher / Entry | 🔵 Mid (3–5 yrs) | 🟢 Senior (6+ yrs) | Top companies hiring |\n|:-:|:--|:-:|:-:|:-:|:--|")
for c in C:
    k = K["courses"][str(c["num"])]; s = k["salary"]
    w(f"| {c['num']} | {c['title']} | ₹{s['entry']} LPA | ₹{s['mid']} LPA | ₹{s['senior']} LPA | {', '.join(k['companies'][:5])} |")
w("\n<details><summary><b>Salary sources</b></summary>\n\n" + "\n".join(f"- [{a}]({b})" for a, b in K["salary_sources"]) + "\n\n</details>\n")

w("## Career Pathways\n\nWhich courses make a learner job-ready for each role (core courses, plus recommended extras):\n")
w("| Target role | Core courses | Recommended extras | |\n|:--|:--|:--|:--|")
for p in K["pathways"]:
    w(f"| **{p['role']}** | {', '.join(f'{n}. ' + TITLE(n) for n in p['courses'])} | {', '.join(TITLE(n) for n in p['plus'])} | {p['note']} |")
w("")

w("## Assessment Scheme (per course)\n\n| Component | Weight |\n|:--|:-:|\n| Continuous lab work & notebooks | 20% |\n| Two mid-term evaluations | 20% |\n| Mini-project / sprint reviews | 20% |\n| Enterprise capstone (demo + report) | 40% |\n")
w("## For Universities: AlgoProfessor Consultancy\n")
w("AlgoProfessor supports institutions from adoption to industry-ready graduates: curriculum customisation, faculty development programmes, AI and emerging-tech lab set-up, GitHub course repositories, industry capstones and forward-deployed client projects, certification readiness, a Centre of Excellence in AI, research and Q1 publications, accreditation and ranking support, and placement readiness.\n")
w("| Engagement model | Scope | Best suited for |\n|:--|:--|:--|")
w("| **Pilot** | One or two courses, FDP, lab manual and GitHub repository for one department | Departments starting their AI journey |")
w("| **Department Programme** | Full core AI track (10 courses) plus Forward Deployed Engineering, with labs, capstones and certification preparation | AI & DS, CSE and allied departments |")
w(f"| **University Transformation** | All {n_c} courses, Centre of Excellence, research and accreditation support across schools | Universities aiming for AI leadership |\n")
w("**Vice-Chancellors, Deans and HoDs:** contact **[cto@algoprofessor.com](mailto:cto@algoprofessor.com)** to schedule a curriculum consultation · [www.algoprofessor.com](https://www.algoprofessor.com) · [campus.algoprofessor.com](https://campus.algoprofessor.com)\n")

w("## Repository Layout\n\n```")
w("index.html                  the 3D website (GitHub Pages)")
w("Enterprise_AI_Syllabus.pdf  the full syllabus PDF, updated edition (16 courses, 75 pages)")
w("data/courses.json           structured data for courses 1–15 (extracted from the first edition)")
w("data/course_details.json    industry tools, language tables and references for courses 1–15")
w("data/extra_courses.json     course 16: Forward Deployed Engineering")
w("data/careers.json           skills, jobs, companies, salaries and career pathways")
w("data/products.json          10 real-time enterprise product blueprints")
w("data/unicorn.json           10 unicorn-track frontier product blueprints")
w("data/lang_courses.json      Python, Go, Rust, Scala, Java courses for the website (from the LaTeX source)")
w("src/template.html           website template")
w("scripts/parse.py            extracts course data from the syllabus text")
w("scripts/build.py            builds index.html from the template and data")
w("scripts/make_readme.py      builds this README from the data")
w("scripts/make_latex.py       builds the LaTeX source of the syllabus from the data")
w("latex/                      LaTeX source (XeLaTeX) and compiled PDF of the syllabus")
w("slides/                     Beamer source + PDF, and the PowerPoint deck (.pptx + PDF preview)")
w("scripts/make_slides.py      builds the Beamer presentation source from the data")
w("scripts/make_pptx.js        builds the PowerPoint deck (pptxgenjs)")
w("programming-languages/      companion syllabus: Python, Go, Rust, Scala, Java (PDF, README, latex/ source)")
w("scripts/make_lang_readme.py builds programming-languages/README.md and data/lang_courses.json from its LaTeX source")
w("assets/                     AlgoProfessor logo")
w("assets/vendor/              Three.js 0.187 (MIT) for the 3D hero, bundled so the site needs no CDN")
w("```\n\nTo rebuild the website and this README after editing any file in `data/` or the template:\n")
w("```bash\npython3 scripts/make_lang_readme.py\npython3 scripts/build.py data/courses.json src/template.html index.html\npython3 scripts/make_readme.py\npython3 scripts/make_latex.py\ncd latex && xelatex Enterprise_AI_Syllabus.tex && xelatex Enterprise_AI_Syllabus.tex\ncp Enterprise_AI_Syllabus.pdf ../Enterprise_AI_Syllabus.pdf && cd ..\npython3 scripts/make_slides.py\ncd slides && xelatex Enterprise_AI_Curriculum_Slides.tex && xelatex Enterprise_AI_Curriculum_Slides.tex && cd ..\nnode scripts/make_pptx.js   # needs pptxgenjs, react-icons, react-dom, sharp\n```\n")
w("## Author\n\n**Dr S Satyanarayana** Ph.D., PDF(AI), FARSC  \nFounder, CEO & Chief Agentic AI Scientist, AlgoProfessor AI R&D Solutions, Hyderabad  \nInternational Postdoctoral Research Co-Supervisor, NYUST (YunTech) & NKUST, Taiwan  \n[GitHub](https://github.com/drssnaiml1-cell) · [ceo@algoprofessor.com](mailto:ceo@algoprofessor.com)\n")
w('---\n\n<p align="center"><sub>© 2026 Dr S Satyanarayana, AlgoProfessor AI R&amp;D Solutions. All rights reserved.</sub></p>')

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
print(f"README.md written: {n_c} courses, {n_u} units, {n_l} labs, {n_h} hours, {n_cert} certifications")
