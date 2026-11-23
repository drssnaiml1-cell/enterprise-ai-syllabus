"""Build programming-languages/README.md and data/lang_courses.json (used by the website)
from programming-languages/latex/lang-courses.tex.

Usage:  python3 scripts/make_lang_readme.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "programming-languages")
SRC = open(os.path.join(DIR, "latex", "lang-courses.tex"), encoding="utf-8").read()


def clean(t):
    """Turn a small LaTeX fragment into Markdown text."""
    t = t.replace("%\n", " ").replace("\n", " ")
    t = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", t)
    t = re.sub(r"\\emph\{([^}]*)\}", r"_\1_", t)
    t = t.replace(r"\&", "&").replace(r"\%", "%").replace(r"\#", "#")
    t = t.replace("---", "—").replace("--", "–").replace("``", "“").replace("''", "”")
    t = t.replace(r"\ ", " ")
    return re.sub(r"\s+", " ", t).strip()


def arg(s, i):
    """Return (content, end) of the brace group starting at s[i] == '{'."""
    assert s[i] == "{"
    depth, j = 0, i
    while True:
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1


def args(s, i, n):
    out = []
    for _ in range(n):
        while s[i] in " \n%":
            i += 1
        a, i = arg(s, i)
        out.append(a)
    return out, i


def table_rows(block):
    rows = []
    for line in block.strip().splitlines():
        line = line.strip()
        if line.endswith(r"\\"):
            rows.append([clean(c) for c in line[:-2].split(" & ")])
    return rows


courses = []
for part in re.split(r"\\course(?=\{)", SRC)[1:]:
    (num, code, title, ltpc, prereq, tagline), _ = args(part, 0, 6)
    units = []
    for m in re.finditer(r"\\unit(?=\{)", part):
        (roman, utitle, hours, topics, outcome), _ = args(part, m.end(), 5)
        units.append((roman, clean(utitle), clean(topics), clean(outcome)))
    cap = clean(args(part, part.index(r"\capstone") + len(r"\capstone"), 1)[0][0])
    roles = [clean(r) for r in re.findall(r"\\role\{([^}]*)\}", part)]
    certs = table_rows(re.search(r"\\begin\{certtable\}(.*?)\\end\{certtable\}", part, re.S).group(1))
    outlook = table_rows(re.search(r"\\begin\{outlooktable\}(.*?)\\end\{outlooktable\}", part, re.S).group(1))
    cos = table_rows(re.search(r"\\begin\{cotable\}(.*?)\\end\{cotable\}", part, re.S).group(1))
    courses.append(dict(num=num, code=code, title=clean(title), prereq=clean(prereq), tagline=clean(tagline),
                        units=units, capstone=cap, roles=roles, certs=certs, outlook=outlook, cos=cos))

o = []
w = o.append
w('<p align="center"><img src="../assets/algoprofessor-logo.svg" alt="AlgoProfessor logo" width="150"></p>\n')
w('<h1 align="center">Enterprise Programming Languages Curriculum</h1>\n')
w('<p align="center"><b>Python · Go · Rust · Scala · Java</b><br>Industry-aligned syllabus · Five courses · Five units each · Curriculum Edition 2026–27</p>\n')
w('<p align="center">\n  <a href="Programming_Languages_Syllabus.pdf"><img src="https://img.shields.io/badge/Download-Syllabus%20PDF-A8811C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Syllabus PDF"></a>\n'
  '  <a href="latex/"><img src="https://img.shields.io/badge/Source-LaTeX%20(XeLaTeX)-0B1F3A?style=for-the-badge&logo=latex&logoColor=C9A227" alt="LaTeX source"></a>\n'
  '  <a href="mailto:cto@algoprofessor.com"><img src="https://img.shields.io/badge/Partner-cto%40algoprofessor.com-138808?style=for-the-badge&logo=maildotru&logoColor=white" alt="Partnership email"></a>\n</p>\n')
w("Companion to the [Enterprise AI Product Development Curriculum](../README.md). Modern AI products are polyglot: "
  "Python for models and agents, Go and Java for services, Scala for large data pipelines and Rust for the fast, safe core. "
  "These five courses build engineers who can work across every layer.\n")
w("Every course has **five units**, each ending in a **hands-on outcome**; **45 lecture + 30 lab hours** (L–T–P–C 3–0–2–4) with "
  "**8 labs**; **five course outcomes mapped to Bloom levels** for OBE, NBA and NAAC; an **enterprise capstone**; "
  "**recommended industry certifications** (checked November 2026); and a **2026–2035 engineering outlook**.\n")

w("## Courses at a Glance\n")
w("| # | Code | Course | Focus | Capstone |\n|:-:|:--|:--|:--|:--|")
for c in courses:
    capname = re.match(r"\*\*(.*?):?\*\*", c["capstone"])
    w(f"| {c['num']} | `{c['code']}` | [{c['title']}](#course-{c['num']}) | {c['tagline']} | {capname.group(1).rstrip(':') if capname else ''} |")
w("")

for c in courses:
    w(f'<a id="course-{c["num"]}"></a>\n')
    w(f"## {c['num']}. {c['title']} (`{c['code']}`)\n")
    w(f"_{c['tagline']}_ · **Prerequisites:** {c['prereq']} · **Hours:** 45 L + 30 P\n")
    w("| Unit | Title | Hands-on outcome |\n|:-:|:--|:--|")
    for r, t, _, out in c["units"]:
        w(f"| {r} | **{t}** | {out} |")
    w("")
    w("<details><summary><b>Unit topics</b></summary>\n")
    for r, t, topics, _ in c["units"]:
        w(f"- **Unit {r}, {t}:** {topics}")
    w("\n</details>\n")
    w("**Course outcomes:** " + " · ".join(f"{co} ({lvl}) {txt}" for co, txt, lvl in c["cos"]) + "\n")
    w(f"**Capstone:** {c['capstone']}\n")
    w("**Careers:** " + ", ".join(c["roles"]) + "\n")
    w("| Certification | Issuer | Level | Units |\n|:--|:--|:--|:-:|")
    for name, issuer, level, units in c["certs"]:
        w(f"| {name} | {issuer} | {level} | {units} |")
    w("")
    w("**2026–2035 outlook:** " + " · ".join(f"**{d}:** {t}" for d, t in c["outlook"]) + "\n")

w("## Build the PDF\n")
w("```bash\ncd programming-languages/latex\nxelatex main.tex && xelatex main.tex\ncp main.pdf ../Programming_Languages_Syllabus.pdf\ncd ../.. && python3 scripts/make_lang_readme.py   # refresh this README\n```\n")
w("The book uses Times New Roman when installed (TeX Gyre Termes otherwise), a white Indian-tricolour cover and navy-and-gold pages.\n")
w("## For Universities\n")
w("AlgoProfessor helps institutions adopt this curriculum: syllabus customisation, faculty development programmes, programming and cloud labs, "
  "GitHub course repositories, industry capstones, certification readiness, accreditation support and placement readiness.\n")
w("**Vice-Chancellors, Deans and HoDs:** contact **[cto@algoprofessor.com](mailto:cto@algoprofessor.com)** · "
  "[www.algoprofessor.com](https://www.algoprofessor.com) · [campus.algoprofessor.com](https://campus.algoprofessor.com)\n")
w("---\n\n**Dr S Satyanarayana** Ph.D., PDF(AI), FARSC · Agentic AI Scientist · Founder & CEO, AlgoProfessor · Creator of AlgoLang · AlgoProfessor AI R&D Solutions, Hyderabad\n")
w('<p align="center"><sub>© 2026 Dr S Satyanarayana, AlgoProfessor AI R&amp;D Solutions. All rights reserved.</sub></p>')

open(os.path.join(DIR, "README.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
LANG = {"1": "Python", "2": "Go", "3": "Rust", "4": "Scala", "5": "Java"}
site = [dict(num=int(c["num"]), lang=LANG[c["num"]], code=c["code"], title=c["title"], tagline=c["tagline"],
             prereq=c["prereq"], units=[dict(r=r, t=t, topics=tp, out=out) for r, t, tp, out in c["units"]],
             capstone=c["capstone"].replace("**", ""), roles=c["roles"],
             certs=[dict(name=n, issuer=i, level=l, units=u) for n, i, l, u in c["certs"]],
             outlook=[dict(d=d, t=t) for d, t in c["outlook"]],
             cos=[dict(co=co, txt=t, lvl=l) for co, t, l in c["cos"]]) for c in courses]
json.dump(site, open(os.path.join(ROOT, "data", "lang_courses.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"programming-languages/README.md written: {len(courses)} courses, {sum(len(c['units']) for c in courses)} units; data/lang_courses.json written")
