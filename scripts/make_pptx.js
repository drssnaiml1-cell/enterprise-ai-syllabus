// Build the PowerPoint deck from the data files.
// Usage: node scripts/make_pptx.js   ->  slides/Enterprise_AI_Curriculum.pptx
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const FA = require("react-icons/fa");

const ROOT = path.join(__dirname, "..");
const J = (f) => JSON.parse(fs.readFileSync(path.join(ROOT, "data", f), "utf8"));
const C = J("courses.json").concat(J("extra_courses.json"));
C.forEach((c) => { if (!c.track) c.track = c.num <= 10 ? "core" : "em"; });
const K = J("careers.json"), P = J("products.json"), U = J("unicorn.json");
const N = C.length;
const SKILL = process.env.PPTX_SKILL_DIR;

// ---------------------------------------------------------------- palette
const HEX = { navy: "0B1F3A", navy2: "1E3A6E", gold: "C9A227", goldDk: "A8811C", saffron: "FF9933", saffronDk: "B35400",
  chakra: "1A2F8F", green: "138808", greenDk: "0E6B06", ink: "1E293B", muted: "5B6678", line: "E3E7EE", panel: "F5F7FA", white: "FFFFFF",
  goldTint: "F7EFD8", saffTint: "FFF1E3", chakTint: "E9ECF8", greenTint: "E8F5E6", navyTint: "E8ECF3", navyMid: "16305A" };
const THEME = { name: "AlgoProfessor Tricolour", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: HEX.navy, lt1: HEX.white, dk2: HEX.navy2, lt2: HEX.panel, accent1: HEX.gold, accent2: HEX.saffron, accent3: HEX.green,
    accent4: HEX.chakra, accent5: HEX.goldDk, accent6: HEX.muted, hlink: HEX.chakra, folHlink: HEX.navy2 } };
const TR = { core: { name: "Core AI Track", col: HEX.navy, tint: HEX.navyTint }, em: { name: "Emerging Technologies Track", col: HEX.green, tint: HEX.greenTint },
  fde: { name: "Industry Practice Track", col: HEX.goldDk, tint: HEX.goldTint } };
const LV = { Entry: { t: "Fresher", c: HEX.saffron, tc: HEX.saffronDk, tint: HEX.saffTint }, Mid: { t: "Mid 3–5 yrs", c: HEX.chakra, tc: HEX.chakra, tint: HEX.chakTint },
  Senior: { t: "Senior 6+ yrs", c: HEX.green, tc: HEX.greenDk, tint: HEX.greenTint } };
const COURSE_ICON = ["FaBrain", "FaChartLine", "FaProjectDiagram", "FaChessKnight", "FaEye", "FaComments", "FaRobot", "FaMagic", "FaDatabase", "FaShieldAlt",
  "FaAtom", "FaMicrochip", "FaCogs", "FaUserShield", "FaLink", "FaHandshake"];
const PROD_ICON = ["FaUniversity", "FaHospital", "FaIndustry", "FaShoppingCart", "FaTruck", "FaBroadcastTower", "FaBolt", "FaSeedling", "FaLandmark", "FaGraduationCap"];
const UNI_ICON = ["FaCode", "FaHeadset", "FaFlag", "FaServer", "FaStethoscope", "FaRobot", "FaCreditCard", "FaShieldAlt", "FaSatellite", "FaFlask"];
const SVC = [["FaBook", "Curriculum adoption & customisation"], ["FaChalkboardTeacher", "Faculty development programmes"], ["FaFlask", "AI & emerging-tech labs"],
  ["FaGithub", "GitHub course repositories"], ["FaProjectDiagram", "Industry capstones & live projects"], ["FaCertificate", "Certification readiness"],
  ["FaLightbulb", "Centre of Excellence in AI"], ["FaPenFancy", "Research, patents & Q1 papers"], ["FaAward", "Accreditation & ranking support"], ["FaBriefcase", "Placement & career readiness"]];

const iconCache = {};
async function icon(name, color = "FFFFFF", size = 256) {
  const key = name + color;
  if (iconCache[key]) return iconCache[key];
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(FA[name], { color: "#" + color, size: String(size) }));
  const png = await sharp(Buffer.from(svg)).resize(size, size).png().toBuffer();
  return (iconCache[key] = "image/png;base64," + png.toString("base64"));
}
const shadow = () => ({ type: "outer", color: "0B1F3A", opacity: 0.14, blur: 6, offset: 2, angle: 90 });
const rng = (s) => { const m = String(s).match(/\d+/g).map(Number); return [m[0], m[m.length - 1]]; };

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
  pres.author = "Dr S Satyanarayana";
  pres.company = "AlgoProfessor AI R&amp;D Solutions";
  pres.title = "Enterprise AI Product Development Curriculum 2026-27";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const S = pres.shapes;

  // ------------------------------------------------------------ layouts
  const FOOT = "Enterprise AI Product Development Curriculum  ·  Dr S Satyanarayana Ph.D., PDF(AI), FARSC  ·  AlgoProfessor AI R&D Solutions";
  pres.defineSlideMaster({ title: "CONTENT", background: { color: HEX.white },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.32, w: 11.4, h: 0.8, fontSize: 30, bold: true, color: HEX.navy, valign: "middle", align: "left", margin: 0, fit: "shrink" }, text: "" } },
      { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10.5, h: 0.3, fontSize: 10, color: HEX.muted, margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: HEX.goldDk, bold: true, align: "right" } });
  pres.defineSlideMaster({ title: "COURSE", background: { color: HEX.white },
    objects: [
      { placeholder: { options: { name: "kicker", type: "body", x: 0.6, y: 0.28, w: 10.6, h: 0.32, fontSize: 12, bold: true, color: HEX.goldDk, margin: 0, charSpacing: 1 }, text: "" } },
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.58, w: 10.6, h: 0.7, fontSize: 32, bold: true, color: HEX.navy, margin: 0, valign: "middle", align: "left" }, text: "" } },
      { placeholder: { options: { name: "tagline", type: "body", x: 0.6, y: 1.26, w: 10.6, h: 0.36, fontSize: 14, italic: true, color: HEX.muted, margin: 0 }, text: "" } },
      { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10.5, h: 0.3, fontSize: 10, color: HEX.muted, margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: HEX.goldDk, bold: true, align: "right" } });
  pres.defineSlideMaster({ title: "SECTION", background: { color: HEX.navy },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.35, w: 8.2, h: 1.2, fontSize: 44, bold: true, color: HEX.white, margin: 0, valign: "bottom", align: "left" }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.7, w: 8.2, h: 1.0, fontSize: 18, color: "D9DFEA", margin: 0, valign: "top" }, text: "" } },
    ] });
  pres.defineSlideMaster({ title: "DARK", background: { color: HEX.navy }, objects: [] });

  const content = (sec) => pres.addSlide({ masterName: "CONTENT", sectionTitle: sec });
  const circleIcon = async (sl, x, y, d, fill, name, nm) => {
    sl.addShape(S.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: nm || "icon circle" });
    sl.addImage({ data: await icon(name), x: x + d * 0.24, y: y + d * 0.24, w: d * 0.52, h: d * 0.52, altText: name.replace("Fa", "") + " icon" });
  };
  const ribbon = (sl, x, y) => { [HEX.saffron, HEX.white, HEX.green].forEach((c, i) => sl.addShape(S.ROUNDED_RECTANGLE, { x: x + i * 0.62, y, w: 0.56, h: 0.12, rectRadius: 0.06, fill: { color: c }, line: { color: c }, objectName: "tricolour ribbon" })); };
  const chakra = (sl, cx, cy, r, col, lw) => {
    sl.addShape(S.OVAL, { x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, fill: { type: "none" }, line: { color: col, width: lw * 2.2 }, objectName: "Ashoka Chakra" });
    sl.addShape(S.OVAL, { x: cx - r * 0.14, y: cy - r * 0.14, w: r * 0.28, h: r * 0.28, fill: { color: col }, line: { color: col } });
    for (let i = 0; i < 24; i++) {
      const a = (i * 15 * Math.PI) / 180, dx = Math.cos(a) * r, dy = Math.sin(a) * r;
      if (Math.abs(dx) < 1e-6 && dy < 0) continue;
      const x = Math.min(cx, cx + dx), y = Math.min(cy, cy + dy);
      sl.addShape(S.LINE, { x, y, w: Math.max(Math.abs(dx), 0.001), h: Math.max(Math.abs(dy), 0.001), flipH: (dx < 0) !== (dy < 0), line: { color: col, width: lw } });
    }
  };
  const logo = (sl, x, y, w) => sl.addImage({ path: path.join(ROOT, "slides", "algoprofessor-logo.png"), x, y, w, h: w * 534 / 900, altText: "AlgoProfessor logo" });

  // ================================================================ 1 title
  pres.addSection({ title: "Introduction" });
  let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Introduction" });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 0.5, w: 1.9, h: 1.2, rectRadius: 0.12, fill: { color: HEX.white }, line: { color: HEX.white }, objectName: "logo badge" });
  logo(s, 0.72, 0.58, 1.66);
  s.addText("INDUSTRY-ALIGNED COURSE SYLLABUS  ·  2026–27", { x: 0.6, y: 2.05, w: 7.6, h: 0.35, fontSize: 14, bold: true, color: HEX.gold, charSpacing: 2, margin: 0, isTextBox: true });
  s.addText("Enterprise AI Product Development", { x: 0.6, y: 2.45, w: 7.9, h: 1.9, fontFace: "Cambria", fontSize: 50, bold: true, color: HEX.white, margin: 0, valign: "top", isTextBox: true });
  s.addText(`${N} courses  ·  3 tracks  ·  skills, jobs & salaries  ·  20 products`, { x: 0.6, y: 4.4, w: 7.8, h: 0.45, fontSize: 20, color: "D9DFEA", margin: 0, isTextBox: true });
  ribbon(s, 0.6, 5.12);
  s.addText([{ text: "Dr S Satyanarayana Ph.D., PDF(AI), FARSC", options: { bold: true, fontSize: 18, color: HEX.white, breakLine: true } },
    { text: "Founder, CEO & Chief Agentic AI Scientist · AlgoProfessor AI R&D Solutions, Hyderabad", options: { fontSize: 13, color: "C9D3E3" } }],
    { x: 0.6, y: 5.45, w: 8.0, h: 0.8, margin: 0, isTextBox: true });
  s.addText("cto@algoprofessor.com   ·   drssnaiml1-cell.github.io/enterprise-ai-syllabus", { x: 0.6, y: 6.45, w: 8.0, h: 0.35, fontSize: 13, bold: true, color: HEX.gold, margin: 0, isTextBox: true });
  chakra(s, 10.55, 3.75, 2.15, "3E5BD8", 1.1);
  s.addShape(S.OVAL, { x: 10.55 - 2.55, y: 3.75 - 2.55, w: 5.1, h: 5.1, fill: { type: "none" }, line: { color: HEX.gold, width: 1, dashType: "dash" }, objectName: "orbit" });
  s.addNotes("Introduce the curriculum: sixteen industry-aligned courses across Core AI, Emerging Technologies and an Industry Practice track in Forward Deployed Engineering, mapped to skills, jobs, salaries and twenty enterprise and unicorn-track products.");

  // ================================================================ 2 gap
  s = content("Introduction");
  s.addText("The gap every university must close by 2035", { placeholder: "title" });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 1.55, w: 5.6, h: 1.55, rectRadius: 0.12, fill: { color: HEX.panel }, line: { color: HEX.line }, objectName: "then card" });
  s.addText([{ text: "Employers used to ask", options: { fontSize: 14, color: HEX.muted, breakLine: true } }, { text: "“Did you study AI?”", options: { fontFace: "Cambria", fontSize: 26, bold: true, color: HEX.navy } }],
    { x: 0.6, y: 1.55, w: 5.6, h: 1.55, align: "center", valign: "middle", isTextBox: true });
  s.addShape(S.DOWN_ARROW, { x: 3.05, y: 3.25, w: 0.7, h: 0.65, fill: { color: HEX.gold }, line: { color: HEX.gold }, objectName: "shift arrow" });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 4.05, w: 5.6, h: 2.3, rectRadius: 0.12, fill: { color: HEX.navy }, line: { color: HEX.navy }, shadow: shadow(), objectName: "now card" });
  s.addText([{ text: "Employers now ask", options: { fontSize: 14, color: HEX.gold, bold: true, breakLine: true } },
    { text: "“What AI product have you built, deployed and governed?”", options: { fontFace: "Cambria", fontSize: 26, bold: true, color: HEX.white } }],
    { x: 0.85, y: 4.05, w: 5.1, h: 2.3, align: "center", valign: "middle", isTextBox: true });
  const gap = [["FaUsers", "Every graduate will work beside AI", "Engineering, science and management graduates will use AI daily; many will build it."],
    ["FaChartBar", "First movers lead", "Universities that close the gap first lead in placements, research, accreditation and rankings."],
    ["FaTools", "Artefacts, not just exams", "Every unit ends in a working artefact; every course in a deployable product."],
    ["FaCheckCircle", "Accreditation-ready", "Aligned to NEP 2020, OBE, NBA and NAAC with CO–Bloom mapping."]];
  for (let i = 0; i < gap.length; i++) {
    const y = 1.55 + i * 1.22;
    await circleIcon(s, 6.9, y + 0.05, 0.62, [HEX.saffron, HEX.chakra, HEX.green, HEX.goldDk][i], gap[i][0]);
    s.addText([{ text: gap[i][1], options: { bold: true, fontSize: 17, color: HEX.navy, breakLine: true } }, { text: gap[i][2], options: { fontSize: 14, color: HEX.muted } }],
      { x: 7.75, y, w: 5.0, h: 1.05, margin: 0, valign: "top", isTextBox: true });
  }
  s.addNotes("Frame the problem: the market now hires for shipped AI products, not course completion. The curriculum is designed so every unit and course produces evidence of building.");

  // ================================================================ 3 at a glance
  s = content("Introduction");
  s.addText("The curriculum at a glance", { placeholder: "title" });
  const nUnits = C.reduce((a, c) => a + c.units.length, 0), nLabs = C.reduce((a, c) => a + c.labs.length, 0), nCert = C.reduce((a, c) => a + c.certs.length, 0);
  const nJobs = new Set(Object.values(K.courses).flatMap((k) => k.jobs.map((j) => j.title))).size;
  const stats = [[N, "Courses", "FaLayerGroup"], [nUnits, "Units", "FaBook"], [(N * 75).toLocaleString("en-IN"), "Contact hours", "FaChalkboardTeacher"],
    [nLabs, "Hands-on labs", "FaFlask"], [nCert, "Certifications mapped", "FaCertificate"], [nJobs, "Job roles", "FaBriefcase"],
    [P.length, "Enterprise products", "FaIndustry"], [U.products.length, "Unicorn-track products", "FaRocket"], [K.pathways.length, "Career pathways", "FaRoute" in FA ? "FaRoute" : "FaProjectDiagram"]];
  for (let i = 0; i < stats.length; i++) {
    const x = 0.6 + (i % 3) * 4.1, y = 1.45 + Math.floor(i / 3) * 1.85;
    const col = [HEX.saffron, HEX.chakra, HEX.green][i % 3], tc = [HEX.saffronDk, HEX.chakra, HEX.greenDk][i % 3];
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 3.9, h: 1.65, rectRadius: 0.1, fill: { color: HEX.white }, line: { color: HEX.line }, shadow: shadow(), objectName: "stat card" });
    await circleIcon(s, x + 0.3, y + 0.5, 0.65, col, stats[i][2]);
    s.addText(String(stats[i][0]), { x: x + 1.15, y: y + 0.2, w: 2.6, h: 0.85, fontFace: "Cambria", fontSize: 44, bold: true, color: tc, margin: 0, valign: "middle", isTextBox: true });
    s.addText(stats[i][1], { x: x + 1.15, y: y + 1.05, w: 2.6, h: 0.4, fontSize: 15, color: HEX.muted, margin: 0, isTextBox: true });
  }
  s.addNotes("Headline numbers. Each course is 45 lecture plus 30 lab hours with eight labs and five Bloom-mapped course outcomes.");

  // ================================================================ 4 three tracks
  s = content("Introduction");
  s.addText("Three tracks, one product-engineering mindset", { placeholder: "title" });
  const trIcon = { core: "FaBrain", em: "FaAtom", fde: "FaHandshake" };
  for (const [i, tr] of ["core", "em", "fde"].entries()) {
    const x = 0.6 + i * 4.1, cs = C.filter((c) => c.track === tr), col = TR[tr].col;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y: 1.45, w: 3.9, h: 5.35, rectRadius: 0.12, fill: { color: TR[tr].tint }, line: { color: TR[tr].tint }, objectName: "track panel" });
    await circleIcon(s, x + 0.25, y0(1.65), 0.7, col, trIcon[tr]);
    s.addText([{ text: TR[tr].name, options: { bold: true, fontSize: 17, color: col, breakLine: true } }, { text: `${cs.length} course${cs.length > 1 ? "s" : ""}`, options: { fontSize: 13, color: HEX.muted } }],
      { x: x + 1.1, y: 1.6, w: 2.7, h: 0.8, margin: 0, valign: "middle", isTextBox: true });
    if (tr === "fde") {
      const c = cs[0];
      s.addText([{ text: `${c.num}  `, options: { bold: true, color: col } }, { text: c.title, options: { bold: true, color: HEX.navy } }], { x: x + 0.3, y: 2.65, w: 3.4, h: 0.6, fontSize: 15, margin: 0, isTextBox: true });
      s.addText("Learners embed with a real or simulated client to discover, prototype, deploy and scale AI, combining the other fifteen courses.", { x: x + 0.3, y: 3.3, w: 3.35, h: 1.5, fontSize: 14, color: HEX.ink, margin: 0, valign: "top", isTextBox: true });
      s.addText("The fastest-growing AI role of 2026", { x: x + 0.3, y: 4.9, w: 3.35, h: 0.5, fontSize: 15, bold: true, italic: true, color: HEX.goldDk, margin: 0, isTextBox: true });
    } else {
      s.addText(cs.map((c, j) => ({ text: `${c.num}  ${c.title}`, options: { breakLine: j < cs.length - 1, color: HEX.navy } })),
        { x: x + 0.3, y: 2.6, w: 3.45, h: 4.0, fontSize: 14, margin: 0, valign: "top", paraSpaceAfter: 5, isTextBox: true });
    }
  }
  function y0(v) { return v; }
  s.addNotes("Ten core AI courses, five emerging-technology courses and the Forward Deployed Engineering practice course that turns the rest into client-ready delivery.");

  // ================================================================ 5 five-unit arc
  s = content("Introduction");
  s.addText("Every course follows the same five-unit arc", { placeholder: "title" });
  const arc = [["I", "Foundations"], ["II", "Core methods"], ["III", "Advanced methods"], ["IV", "Production engineering"], ["V", "Deployment, governance & capstone"]];
  const arcCol = [HEX.saffron, HEX.gold, HEX.chakra, HEX.navy2, HEX.green];
  arc.forEach(([n, t], i) => {
    s.addShape(S.CHEVRON, { x: 0.6 + i * 2.45, y: 1.7, w: 2.6, h: 1.55, fill: { color: arcCol[i] }, line: { color: arcCol[i] }, objectName: "arc chevron" });
    s.addText([{ text: `Unit ${n}`, options: { bold: true, fontSize: 18, breakLine: true } }, { text: t, options: { fontSize: 13 } }],
      { x: 0.6 + i * 2.45 + 0.55, y: 1.7, w: 1.6, h: 1.55, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  const arcStats = [["45", "lecture hours", "L–T–P–C 3–0–2–4"], ["30", "lab hours", "8 tool-driven labs"], ["5", "hands-on outcomes", "one working artefact per unit"], ["1", "capstone", "a deployable enterprise product"]];
  arcStats.forEach(([n, a, b], i) => {
    const x = 0.6 + i * 3.08;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y: 3.85, w: 2.88, h: 2.0, rectRadius: 0.1, fill: { color: HEX.white }, line: { color: HEX.line }, shadow: shadow(), objectName: "arc stat" });
    s.addText(n, { x, y: 4.0, w: 2.88, h: 0.85, fontFace: "Cambria", fontSize: 44, bold: true, color: HEX.goldDk, align: "center", margin: 0, isTextBox: true });
    s.addText([{ text: a, options: { bold: true, fontSize: 16, color: HEX.navy, breakLine: true } }, { text: b, options: { fontSize: 13, color: HEX.muted } }],
      { x: x + 0.15, y: 4.9, w: 2.58, h: 0.8, align: "center", margin: 0, isTextBox: true });
  });
  s.addText("Five course outcomes per course, mapped to Bloom levels L2 Understand to L6 Create, ready for CO–PO–PSO attainment.", { x: 0.6, y: 6.15, w: 12.1, h: 0.4, fontSize: 14, italic: true, color: HEX.muted, margin: 0, isTextBox: true });
  s.addNotes("The common arc makes courses easy to adopt and assess: foundations, core methods, advanced methods, production engineering, then deployment, governance and a capstone.");

  // ================================================================ 6 course map
  s = content("Introduction");
  s.addText(`The ${N} courses`, { placeholder: "title" });
  for (const [i, c] of C.entries()) {
    const x = 0.6 + (i % 4) * 3.07, y = 1.4 + Math.floor(i / 4) * 1.3, col = TR[c.track].col;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 2.92, h: 1.16, rectRadius: 0.1, fill: { color: TR[c.track].tint }, line: { color: TR[c.track].tint }, objectName: "course tile" });
    await circleIcon(s, x + 0.15, y + 0.28, 0.6, col, COURSE_ICON[i]);
    s.addText([{ text: c.code, options: { fontSize: 10, bold: true, color: col, breakLine: true } }, { text: c.title, options: { fontSize: 13, bold: true, color: HEX.navy } }],
      { x: x + 0.88, y: y + 0.08, w: 1.96, h: 1.0, margin: 0, valign: "middle", isTextBox: true });
  }
  const legend = (sl, x, y, items) => items.forEach(([t, c], i) => {
    sl.addShape(S.OVAL, { x: x + i * 3.0, y: y + 0.07, w: 0.2, h: 0.2, fill: { color: c }, line: { color: c } });
    sl.addText(t, { x: x + i * 3.0 + 0.28, y, w: 2.65, h: 0.34, fontSize: 12, color: HEX.ink, margin: 0, valign: "middle", isTextBox: true });
  });
  legend(s, 0.6, 6.6, [["Core AI Track", HEX.navy], ["Emerging Technologies", HEX.green], ["Industry Practice (FDE)", HEX.goldDk]]);
  s.addNotes("The full course map, colour-coded by track.");

  // ================================================================ course slides
  let lastTrack = null;
  for (const [i, c] of C.entries()) {
    const k = K.courses[String(c.num)], col = TR[c.track].col;
    if (c.track !== lastTrack) {
      pres.addSection({ title: TR[c.track].name });
      const cs = C.filter((x) => x.track === c.track);
      const d = pres.addSlide({ masterName: "SECTION", sectionTitle: TR[c.track].name });
      d.addText(TR[c.track].name, { placeholder: "title" });
      d.addText({ core: "Ten courses from intelligent decision systems to trustworthy, production-grade AI.", em: "Five courses on the technologies reshaping AI between 2026 and 2035.", fde: "The client-embedded capstone: discover, build, deploy and scale AI with real enterprises." }[c.track], { placeholder: "body" });
      d.addShape(S.OVAL, { x: 9.55, y: 1.45, w: 3.0, h: 3.0, fill: { color: c.track === "core" ? HEX.navyMid : col }, line: { color: HEX.gold, width: 2 }, objectName: "section icon circle" });
      d.addImage({ data: await icon(trIcon[c.track]), x: 10.3, y: 2.2, w: 1.5, h: 1.5, altText: "track icon" });
      d.addText(cs.map((x, j) => ({ text: `${x.num}   ${x.title}`, options: { breakLine: j < cs.length - 1 } })), { x: 0.8, y: 4.85, w: 11.8, h: 1.9, fontSize: 14, color: "C9D3E3", margin: 0, valign: "top", isTextBox: true, ...(cs.length > 5 ? { columns: 2 } : {}) });
      ribbon(d, 0.8, 2.05);
      d.addNotes(`Section: ${TR[c.track].name} (${cs.length} course${cs.length > 1 ? "s" : ""}).`);
      lastTrack = c.track;
    }
    s = pres.addSlide({ masterName: "COURSE", sectionTitle: TR[c.track].name });
    s.addText(`COURSE ${c.num}  ·  ${c.code}  ·  ${TR[c.track].name.toUpperCase()}`, { placeholder: "kicker" });
    s.addText(c.title, { placeholder: "title" });
    s.addText(c.tagline, { placeholder: "tagline" });
    await circleIcon(s, 11.75, 0.35, 1.0, col, COURSE_ICON[i]);
    // units
    s.addText("FIVE-UNIT CURRICULUM", { x: 0.6, y: 1.8, w: 6.6, h: 0.3, fontSize: 13, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
    c.units.forEach((u, j) => {
      const y = 2.15 + j * 0.84;
      s.addShape(S.OVAL, { x: 0.6, y: y + 0.05, w: 0.5, h: 0.5, fill: { color: col }, line: { color: col }, objectName: "unit number" });
      s.addText(u.n, { x: 0.6, y: y + 0.05, w: 0.5, h: 0.5, fontSize: 12, bold: true, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText([{ text: u.title, options: { bold: true, fontSize: 14, color: HEX.navy, breakLine: true } }, { text: u.outcome, options: { fontSize: 10.5, color: HEX.muted } }],
        { x: 1.25, y, w: 5.95, h: 0.8, margin: 0, valign: "top", isTextBox: true });
    });
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 6.37, w: 6.6, h: 0.55, rectRadius: 0.08, fill: { color: HEX.goldTint }, line: { color: HEX.gold, width: 0.75 }, objectName: "capstone" });
    s.addText([{ text: "Capstone:  ", options: { bold: true, color: HEX.goldDk } }, { text: c.capstone.name, options: { bold: true, color: HEX.navy } }],
      { x: 0.75, y: 6.37, w: 6.35, h: 0.55, fontSize: 13, valign: "middle", margin: 0, isTextBox: true });
    // right panel
    s.addShape(S.ROUNDED_RECTANGLE, { x: 7.55, y: 1.75, w: 5.2, h: 5.17, rectRadius: 0.1, fill: { color: HEX.panel }, line: { color: HEX.panel }, objectName: "career panel" });
    s.addText("SKILLS YOU WILL GAIN", { x: 7.8, y: 1.88, w: 4.8, h: 0.28, fontSize: 12, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
    s.addText(k.skills.slice(0, 3).map((x, j) => ({ text: x, options: { bullet: { code: "25B8" }, breakLine: j < 2 } })),
      { x: 7.8, y: 2.18, w: 4.75, h: 1.3, fontSize: 11.5, color: HEX.ink, margin: 0, valign: "top", paraSpaceAfter: 3, isTextBox: true });
    s.addText("JOBS", { x: 7.8, y: 3.55, w: 4.8, h: 0.28, fontSize: 12, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
    k.jobs.slice(0, 4).forEach((jb, j) => {
      const L = LV[jb.level], y = 3.88 + j * 0.37;
      s.addShape(S.ROUNDED_RECTANGLE, { x: 7.8, y: y + 0.03, w: 1.25, h: 0.27, rectRadius: 0.06, fill: { color: L.c }, line: { color: L.c }, objectName: "level pill" });
      s.addText(L.t, { x: 7.8, y: y + 0.03, w: 1.25, h: 0.27, fontSize: 10, bold: true, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText(jb.title, { x: 9.15, y, w: 3.45, h: 0.33, fontSize: 12.5, bold: true, color: HEX.navy, valign: "middle", margin: 0, isTextBox: true });
    });
    s.addText("INDICATIVE SALARY IN INDIA (₹ LPA)", { x: 7.8, y: 5.4, w: 4.8, h: 0.28, fontSize: 12, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
    [["Fresher", k.salary.entry, LV.Entry], ["Mid", k.salary.mid, LV.Mid], ["Senior", k.salary.senior, LV.Senior]].forEach(([lab, val, L], j) => {
      const x = 7.8 + j * 1.6;
      s.addShape(S.ROUNDED_RECTANGLE, { x, y: 5.72, w: 1.5, h: 0.78, rectRadius: 0.08, fill: { color: L.tint }, line: { color: L.c, width: 1 }, objectName: "salary tile" });
      s.addText([{ text: lab, options: { fontSize: 10, color: HEX.muted, breakLine: true } }, { text: "₹" + val, options: { fontSize: 18, bold: true, color: L.tc } }],
        { x, y: 5.72, w: 1.5, h: 0.78, align: "center", valign: "middle", margin: 0, isTextBox: true });
    });
    s.addText([{ text: "Hiring: ", options: { bold: true, color: HEX.navy } }, { text: k.companies.slice(0, 5).join(", "), options: { color: HEX.muted } }],
      { x: 7.8, y: 6.55, w: 4.8, h: 0.3, fontSize: 10, fit: "shrink", margin: 0, valign: "top", isTextBox: true });
    s.addNotes(`${c.title} (${c.code}). Prerequisites: ${c.prereq}. Capstone: ${c.capstone.name} – ${c.capstone.desc} Jobs: ${k.jobs.map((j) => j.title).join(", ")}. Top languages: ${c.languages.join(", ")}.`);
  }

  // ================================================================ careers section
  pres.addSection({ title: "Careers & Salaries" });
  s = content("Careers & Salaries");
  s.addText("Salary outlook: fresher to senior, by course", { placeholder: "title" });
  const X0 = 4.75, XW = 7.35, MAXV = 160, Y0 = 1.62, RH = 0.305, sx = (v) => X0 + (v / MAXV) * XW;
  for (let v = 0; v <= MAXV; v += 20) {
    s.addShape(S.LINE, { x: sx(v), y: Y0 - 0.1, w: 0, h: N * RH + 0.05, line: { color: HEX.line, width: 0.75 } });
    s.addText(String(v), { x: sx(v) - 0.3, y: Y0 - 0.42, w: 0.6, h: 0.28, fontSize: 10, color: HEX.muted, align: "center", margin: 0, isTextBox: true });
  }
  C.forEach((c, i) => {
    const sv = K.courses[String(c.num)].salary, y = Y0 + i * RH, [e0, e1] = rng(sv.entry), [m0, m1] = rng(sv.mid), [s0, s1] = rng(sv.senior);
    s.addText(`${c.num}  ${c.title}`, { x: 0.6, y, w: 4.0, h: RH, fontSize: 10.5, bold: true, color: TR[c.track].col, align: "right", valign: "middle", margin: 0, isTextBox: true });
    const bar = (a, b, col) => s.addShape(S.RECTANGLE, { x: sx(a), y: y + 0.05, w: Math.max(sx(b) - sx(a), 0.02), h: RH - 0.1, fill: { color: col }, line: { color: col }, objectName: "salary bar" });
    bar(e0, e1, HEX.saffron); bar(m0, m1, HEX.chakra); bar(Math.max(s0, m1), s1, HEX.green);
    s.addText(`₹${e0}–${sv.senior}`, { x: sx(s1) + 0.08, y, w: 1.2, h: RH, fontSize: 10, color: HEX.greenDk, bold: true, valign: "middle", margin: 0, isTextBox: true });
  });
  legend(s, 4.75, 6.6, [["Fresher (0–2 yrs)", HEX.saffron], ["Mid-level (3–5 yrs)", HEX.chakra], ["Senior (6+ yrs)", HEX.green]]);
  s.addText("₹ lakh per annum · indicative, Nov 2026", { x: 0.6, y: 6.6, w: 4.0, h: 0.34, fontSize: 10, italic: true, color: HEX.muted, align: "right", margin: 0, valign: "middle", isTextBox: true });
  s.addNotes("Indicative annual CTC in India compiled in November 2026 from published salary reports; IT services pay at the lower end, product companies, GCCs and AI-first start-ups at the upper end. Ranges overlap where sources disagree.");

  // matrix
  s = content("Careers & Salaries");
  s.addText("Course-to-career matrix", { placeholder: "title" });
  const hdrColor = (c) => TR[c.track].col;
  const rows = [[{ text: "Career role", options: { bold: true, color: HEX.white, fill: { color: HEX.navy }, fontSize: 12 } },
    ...C.map((c) => ({ text: String(c.num), options: { bold: true, color: HEX.white, fill: { color: hdrColor(c) }, align: "center", fontSize: 12 } }))]];
  K.pathways.forEach((p, r) => {
    const band = r % 2 ? HEX.panel : HEX.white;
    rows.push([{ text: p.role, options: { bold: true, color: HEX.navy, fill: { color: band }, fontSize: 11.5 } },
      ...C.map((c) => p.courses.includes(c.num) ? { text: "●", options: { color: HEX.white, fill: { color: hdrColor(c) }, align: "center", fontSize: 13, bold: true } }
        : p.plus.includes(c.num) ? { text: "○", options: { color: hdrColor(c), fill: { color: TR[c.track].tint }, align: "center", fontSize: 13, bold: true } }
          : { text: "", options: { fill: { color: band } } })]);
  });
  s.addTable(rows, { x: 0.6, y: 1.35, w: 12.13, colW: [3.65].concat(Array(N).fill((12.13 - 3.65) / N)), rowH: 0.355, border: { type: "solid", pt: 0.75, color: "FFFFFF" }, valign: "middle", fontFace: "Calibri", margin: [0.02, 0.06, 0.02, 0.06] });
  const mLeg = [["●  Core course", HEX.navy], ["○  Recommended extra", HEX.muted]];
  s.addText([{ text: "●", options: { color: HEX.navy, bold: true } }, { text: " core course (cell coloured by track)     ", options: { color: HEX.ink } },
    { text: "○", options: { color: HEX.goldDk, bold: true } }, { text: " recommended extra     ", options: { color: HEX.ink } },
    { text: "■", options: { color: HEX.navy } }, { text: " Core AI   ", options: { color: HEX.ink } }, { text: "■", options: { color: HEX.green } }, { text: " Emerging   ", options: { color: HEX.ink } },
    { text: "■", options: { color: HEX.goldDk } }, { text: " FDE", options: { color: HEX.ink } }], { x: 0.6, y: 6.5, w: 12.1, h: 0.35, fontSize: 12, margin: 0, isTextBox: true });
  s.addNotes("Read across a row to see which courses make a learner job-ready for that role; column numbers are course numbers and colours show the track.");

  // top pathways
  s = content("Careers & Salaries");
  s.addText("Six high-demand career pathways", { placeholder: "title" });
  const pick = ["Forward Deployed Engineer", "Agentic AI Engineer", "LLM & Generative AI Engineer", "AI / ML Engineer", "Data Scientist", "AI Security Engineer"];
  const picons = ["FaHandshake", "FaRobot", "FaComments", "FaBrain", "FaChartLine", "FaUserShield"];
  for (const [i, role] of pick.entries()) {
    const p = K.pathways.find((x) => x.role === role); if (!p) continue;
    const x = 0.6 + (i % 3) * 4.1, y = 1.45 + Math.floor(i / 3) * 2.75;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 3.9, h: 2.55, rectRadius: 0.1, fill: { color: HEX.white }, line: { color: HEX.line }, shadow: shadow(), objectName: "pathway card" });
    await circleIcon(s, x + 0.25, y + 0.25, 0.65, [HEX.goldDk, HEX.navy, HEX.chakra, HEX.saffron, HEX.green, HEX.navy2][i], picons[i]);
    s.addText(p.role, { x: x + 1.05, y: y + 0.25, w: 2.7, h: 0.65, fontSize: 16, bold: true, color: HEX.navy, valign: "middle", margin: 0, isTextBox: true });
    s.addText(p.note, { x: x + 0.25, y: y + 1.0, w: 3.45, h: 0.75, fontSize: 12, color: HEX.muted, margin: 0, valign: "top", isTextBox: true });
    s.addText([{ text: "Core: ", options: { bold: true, color: HEX.goldDk } }, { text: p.courses.map((n) => C[n - 1].title).join(" · "), options: { color: HEX.navy } }],
      { x: x + 0.25, y: y + 1.75, w: 3.45, h: 0.7, fontSize: 11, margin: 0, valign: "top", isTextBox: true });
  }
  s.addNotes("Six of the thirteen pathways; the matrix on the previous slide shows them all.");

  // language strategy
  s = content("Careers & Salaries");
  s.addText("Programming language strategy 2026–2035", { placeholder: "title" });
  const layers = [["Delivery layer", "TypeScript / JavaScript · Go · Java / Scala", HEX.green, "FaGlobe"], ["Intelligence layer", "Python · SQL · R · Julia", HEX.goldDk, "FaBrain"],
    ["Performance & safety layer", "C++ / CUDA · Rust · Mojo", HEX.chakra, "FaMicrochip"], ["Specialist layer", "OpenQASM 3 (quantum) · Solidity (smart contracts)", HEX.navy, "FaAtom"]];
  for (const [i, [a, b, col, ic]] of layers.entries()) {
    const y = 1.55 + i * 1.18;
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6 + i * 0.25, y, w: 7.9 - i * 0.5, h: 1.0, rectRadius: 0.1, fill: { color: col }, line: { color: col }, objectName: "language layer" });
    s.addImage({ data: await icon(ic), x: 0.85 + i * 0.25, y: y + 0.25, w: 0.5, h: 0.5, altText: a });
    s.addText([{ text: a, options: { bold: true, fontSize: 17, breakLine: true } }, { text: b, options: { fontSize: 14 } }], { x: 1.55 + i * 0.25, y, w: 6.6 - i * 0.5, h: 1.0, color: HEX.white, valign: "middle", margin: 0, isTextBox: true });
  }
  s.addText([{ text: "Python for intelligence, a systems language for performance, a delivery language for users.", options: { bold: true, fontSize: 17, color: HEX.navy, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "By 2030–2035: AI-assisted engineering is the norm; graduates must be polyglot, design for memory safety, optimise below the Python layer, and control AI-written code with specifications and evaluation suites.", options: { fontSize: 14, color: HEX.muted } }],
    { x: 8.9, y: 1.6, w: 3.85, h: 4.6, margin: 0, valign: "top", isTextBox: true });
  s.addNotes("Every course names its top three languages. Graduates who can work across all three layers build complete AI products, not just models.");

  // ================================================================ products section
  pres.addSection({ title: "Products" });
  s = content("Products");
  s.addText("Top 10 real-time enterprise products", { placeholder: "title" });
  for (const [i, p] of P.entries()) {
    const x = 0.6 + (i % 5) * 2.47, y = 1.4 + Math.floor(i / 5) * 2.72;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 2.3, h: 2.55, rectRadius: 0.1, fill: { color: HEX.white }, line: { color: HEX.line }, shadow: shadow(), objectName: "product card" });
    await circleIcon(s, x + 0.18, y + 0.18, 0.6, [HEX.saffron, HEX.chakra, HEX.green][i % 3], PROD_ICON[i]);
    s.addText(String(p.id).padStart(2, "0"), { x: x + 1.3, y: y + 0.12, w: 0.85, h: 0.6, fontFace: "Cambria", fontSize: 26, bold: true, color: HEX.gold, align: "right", margin: 0, isTextBox: true });
    s.addText(p.domain, { x: x + 0.18, y: y + 0.85, w: 1.98, h: 0.45, fontSize: 10, bold: true, color: HEX.goldDk, margin: 0, valign: "top", isTextBox: true });
    s.addText(p.name, { x: x + 0.18, y: y + 1.3, w: 1.98, h: 0.9, fontSize: 12.5, bold: true, color: HEX.navy, margin: 0, valign: "top", isTextBox: true });
    s.addText("Courses " + p.courses.join(", "), { x: x + 0.18, y: y + 2.18, w: 1.98, h: 0.3, fontSize: 10, color: HEX.muted, margin: 0, isTextBox: true });
  }
  s.addNotes("One flagship real-time product per industry; each combines several courses and makes a strong team capstone.");

  const p0 = P[0];
  s = content("Products");
  s.addText("Product deep dive: Real-Time Fraud & Risk Platform", { placeholder: "title" });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 1.45, w: 5.9, h: 1.55, rectRadius: 0.1, fill: { color: HEX.saffTint }, line: { color: HEX.saffTint }, objectName: "problem" });
  s.addText([{ text: "Business problem", options: { bold: true, color: HEX.saffronDk, fontSize: 14, breakLine: true } }, { text: p0.problem, options: { fontSize: 13, color: HEX.ink } }], { x: 0.8, y: 1.5, w: 5.5, h: 1.45, margin: 0, valign: "middle", isTextBox: true });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y: 3.15, w: 5.9, h: 1.55, rectRadius: 0.1, fill: { color: HEX.greenTint }, line: { color: HEX.greenTint }, objectName: "realtime" });
  s.addText([{ text: "What happens in real time", options: { bold: true, color: HEX.greenDk, fontSize: 14, breakLine: true } }, { text: p0.realtime, options: { fontSize: 13, color: HEX.ink } }], { x: 0.8, y: 3.2, w: 5.5, h: 1.45, margin: 0, valign: "middle", isTextBox: true });
  s.addText([{ text: "KPIs it moves: ", options: { bold: true, color: HEX.navy } }, { text: p0.kpis.join(" · "), options: { color: HEX.muted, breakLine: true } },
    { text: "Stack: ", options: { bold: true, color: HEX.navy } }, { text: p0.stack.join(" · "), options: { color: HEX.muted } }], { x: 0.6, y: 4.9, w: 5.9, h: 1.5, fontSize: 13, margin: 0, valign: "top", isTextBox: true });
  s.addText("PRODUCT MODULES", { x: 6.95, y: 1.45, w: 5.8, h: 0.3, fontSize: 12, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
  const modCol = [HEX.navy, HEX.navyMid, HEX.navy2, HEX.chakra, HEX.green];
  p0.modules.forEach((m, j) => {
    const y = 1.85 + j * 0.86;
    s.addShape(S.ROUNDED_RECTANGLE, { x: 6.95, y, w: 5.8, h: 0.74, rectRadius: 0.08, fill: { color: modCol[j] }, line: { color: modCol[j] }, objectName: "module" });
    s.addText([{ text: `${j + 1}  `, options: { bold: true, color: HEX.gold } }, { text: m, options: { color: HEX.white } }], { x: 7.1, y, w: 5.5, h: 0.74, fontSize: 13, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("Courses: " + p0.courses.map((n) => `${n} ${C[n - 1].title}`).join(" · "), { x: 6.95, y: 6.25, w: 5.8, h: 0.6, fontSize: 10.5, color: HEX.muted, margin: 0, valign: "top", isTextBox: true });
  s.addNotes(p0.tagline);

  // unicorn grid (dark)
  s = pres.addSlide({ masterName: "DARK", sectionTitle: "Products" });
  s.addText("Unicorn track: 10 frontier products", { x: 0.6, y: 0.32, w: 11.4, h: 0.8, fontFace: "Cambria", fontSize: 30, bold: true, color: HEX.white, margin: 0, valign: "middle", isTextBox: true });
  s.addText("Modelled on 2026's unicorn categories. Each starts as a 12-week team MVP and grows into a venture-scale platform.", { x: 0.6, y: 1.05, w: 12.1, h: 0.35, fontSize: 14, color: "C9D3E3", margin: 0, isTextBox: true });
  for (const [i, u] of U.products.entries()) {
    const x = 0.6 + (i % 5) * 2.47, y = 1.6 + Math.floor(i / 5) * 2.65;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 2.3, h: 2.48, rectRadius: 0.1, fill: { color: HEX.navyMid }, line: { color: "2B4B8A" }, objectName: "unicorn card" });
    await circleIcon(s, x + 0.18, y + 0.18, 0.58, HEX.gold, UNI_ICON[i]);
    s.addText("★".repeat(u.complexity) + "☆".repeat(5 - u.complexity), { x: x + 0.85, y: y + 0.28, w: 1.35, h: 0.38, fontSize: 13, color: HEX.gold, align: "right", margin: 0, isTextBox: true });
    s.addText(u.category, { x: x + 0.18, y: y + 0.88, w: 1.98, h: 0.45, fontSize: 10, bold: true, color: HEX.gold, margin: 0, valign: "top", isTextBox: true });
    s.addText(u.name, { x: x + 0.18, y: y + 1.33, w: 1.98, h: 0.85, fontSize: 12.5, bold: true, color: HEX.white, margin: 0, valign: "top", isTextBox: true });
    s.addText(`${u.courses.length} courses · ${u.layers.length} layers`, { x: x + 0.18, y: y + 2.12, w: 1.98, h: 0.28, fontSize: 10, color: "9FB0CC", margin: 0, isTextBox: true });
  }
  s.addText("Company names in the speaker notes show market categories, not partners or endorsements.", { x: 0.6, y: 7.0, w: 12.1, h: 0.3, fontSize: 10, color: "9FB0CC", margin: 0, isTextBox: true });
  s.addNotes(U.products.map((u) => `${u.id}. ${u.name}: ${u.signal} (category examples: ${u.refs.join(", ")})`).join("\n"));

  const u3 = U.products[2];
  s = content("Products");
  s.addText("Unicorn deep dive: Sovereign Indic Foundation Model", { placeholder: "title" });
  s.addText("SYSTEM ARCHITECTURE (TOP TO BOTTOM)", { x: 0.6, y: 1.45, w: 7.0, h: 0.3, fontSize: 12, bold: true, color: HEX.goldDk, charSpacing: 1, margin: 0, isTextBox: true });
  const layCol = [HEX.navy, HEX.navyMid, HEX.navy2, "2B4B8A", "0F5E5A", HEX.green];
  u3.layers.forEach((l, j) => {
    const [h, ...r] = l.split(":"), y = 1.85 + j * 0.8;
    s.addShape(S.ROUNDED_RECTANGLE, { x: 0.6, y, w: 7.0, h: 0.68, rectRadius: 0.08, fill: { color: layCol[j % 6] }, line: { color: layCol[j % 6] }, objectName: "arch layer" });
    s.addText([{ text: h + ": ", options: { bold: true, color: HEX.gold } }, { text: r.join(":").trim(), options: { color: HEX.white } }], { x: 0.78, y, w: 6.7, h: 0.68, fontSize: 12.5, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText([{ text: "Why now", options: { bold: true, color: HEX.navy, fontSize: 15, breakLine: true } }, { text: u3.signal, options: { fontSize: 13, color: HEX.muted, breakLine: true } },
    { text: " ", options: { fontSize: 6, breakLine: true } }, { text: "The moat", options: { bold: true, color: HEX.navy, fontSize: 15, breakLine: true } },
    ...u3.moats.map((m, j) => ({ text: m, options: { bullet: { code: "25B8" }, fontSize: 13, color: HEX.ink, breakLine: j < u3.moats.length - 1 } }))], { x: 8.0, y: 1.45, w: 4.75, h: 3.2, margin: 0, valign: "top", isTextBox: true });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 8.0, y: 4.85, w: 4.75, h: 0.95, rectRadius: 0.08, fill: { color: HEX.saffTint }, line: { color: HEX.saffTint }, objectName: "mvp" });
  s.addText([{ text: "12-week MVP: ", options: { bold: true, color: HEX.saffronDk } }, { text: u3.mvp, options: { color: HEX.ink } }], { x: 8.15, y: 4.85, w: 4.5, h: 0.95, fontSize: 12, valign: "middle", margin: 0, isTextBox: true });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 8.0, y: 5.9, w: 4.75, h: 0.95, rectRadius: 0.08, fill: { color: HEX.greenTint }, line: { color: HEX.greenTint }, objectName: "scale" });
  s.addText([{ text: "Venture scale: ", options: { bold: true, color: HEX.greenDk } }, { text: u3.scale, options: { color: HEX.ink } }], { x: 8.15, y: 5.9, w: 4.5, h: 0.95, fontSize: 12, valign: "middle", margin: 0, isTextBox: true });
  s.addNotes(u3.what);

  // FDE spotlight
  const fde = C.find((c) => c.track === "fde"), kf = K.courses[String(fde.num)];
  s = content("Products");
  s.addText(`Spotlight: Forward Deployed Engineering (Course ${fde.num})`, { placeholder: "title" });
  const loop = [["Discover", "FaSearch"], ["Prototype", "FaTools"], ["Deploy", "FaRocket"], ["Adopt", "FaUsers"], ["Prove value", "FaChartBar"]];
  const lc = [HEX.saffron, HEX.gold, HEX.chakra, HEX.navy2, HEX.green], CX = 3.35, CY = 4.2, R = 1.95;
  for (const [j, [t, ic]] of loop.entries()) {
    const a = (-90 + j * 72) * Math.PI / 180, x = CX + R * Math.cos(a) - 0.6, y = CY + R * Math.sin(a) - 0.6;
    s.addShape(S.OVAL, { x, y, w: 1.2, h: 1.2, fill: { color: lc[j] }, line: { color: HEX.white, width: 2 }, shadow: shadow(), objectName: "loop step" });
    s.addImage({ data: await icon(ic), x: x + 0.4, y: y + 0.18, w: 0.4, h: 0.4, altText: t });
    s.addText(t, { x: x - 0.1, y: y + 0.6, w: 1.4, h: 0.4, fontSize: 12, bold: true, color: HEX.white, align: "center", margin: 0, isTextBox: true });
  }
  s.addShape(S.OVAL, { x: CX - 0.85, y: CY - 0.85, w: 1.7, h: 1.7, fill: { color: HEX.goldTint }, line: { color: HEX.gold, width: 1.5, dashType: "dash" }, objectName: "loop centre" });
  s.addText("Client-embedded loop", { x: CX - 0.8, y: CY - 0.5, w: 1.6, h: 1.0, fontSize: 14, bold: true, color: HEX.goldDk, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Engineers who embed with a client to turn AI products into working, measured deployments: part engineer, part consultant, part product translator.", { x: 6.9, y: 1.5, w: 5.85, h: 1.0, fontSize: 15, color: HEX.navy, margin: 0, valign: "top", isTextBox: true });
  kf.jobs.forEach((jb, j) => {
    const L = LV[jb.level], y = 2.65 + j * 0.42;
    s.addShape(S.ROUNDED_RECTANGLE, { x: 6.9, y: y + 0.04, w: 1.35, h: 0.3, rectRadius: 0.06, fill: { color: L.c }, line: { color: L.c }, objectName: "level pill" });
    s.addText(L.t, { x: 6.9, y: y + 0.04, w: 1.35, h: 0.3, fontSize: 10, bold: true, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(jb.title, { x: 8.35, y, w: 4.4, h: 0.38, fontSize: 13, bold: true, color: HEX.navy, valign: "middle", margin: 0, isTextBox: true });
  });
  [["Fresher", kf.salary.entry, LV.Entry], ["Mid", kf.salary.mid, LV.Mid], ["Senior", kf.salary.senior, LV.Senior]].forEach(([lab, val, L], j) => {
    const x = 6.9 + j * 1.98;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y: 5.3, w: 1.85, h: 0.9, rectRadius: 0.08, fill: { color: L.tint }, line: { color: L.c, width: 1 }, objectName: "salary tile" });
    s.addText([{ text: lab, options: { fontSize: 11, color: HEX.muted, breakLine: true } }, { text: "₹" + val + " LPA", options: { fontSize: 17, bold: true, color: L.tc } }], { x, y: 5.3, w: 1.85, h: 0.9, align: "center", valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText("FDE postings in India grew nearly 19-fold between June 2025 and June 2026 (Indeed data reported by CXOToday). Hiring: " + kf.companies.slice(0, 6).join(", ") + ".", { x: 6.9, y: 6.3, w: 5.85, h: 0.6, fontSize: 10.5, italic: true, color: HEX.muted, margin: 0, valign: "top", isTextBox: true });
  s.addNotes(fde.tagline);

  // ================================================================ partnership section
  pres.addSection({ title: "Partnership" });
  s = content("Partnership");
  s.addText("AlgoProfessor consultancy: syllabus to job-ready", { placeholder: "title" });
  for (const [i, [ic, t]] of SVC.entries()) {
    const x = 0.6 + (i % 5) * 2.47, y = 1.45 + Math.floor(i / 5) * 1.75;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y, w: 2.3, h: 1.55, rectRadius: 0.1, fill: { color: HEX.white }, line: { color: HEX.line }, shadow: shadow(), objectName: "service card" });
    await circleIcon(s, x + 0.18, y + 0.2, 0.55, [HEX.saffron, HEX.chakra, HEX.green][i % 3], ic);
    s.addText(String(i + 1).padStart(2, "0"), { x: x + 1.4, y: y + 0.15, w: 0.75, h: 0.5, fontFace: "Cambria", fontSize: 22, bold: true, color: HEX.gold, align: "right", margin: 0, isTextBox: true });
    s.addText(t, { x: x + 0.18, y: y + 0.85, w: 1.98, h: 0.62, fontSize: 12.5, bold: true, color: HEX.navy, margin: 0, valign: "top", isTextBox: true });
  }
  const em = [["Pilot", "1–2 courses, FDP, lab manual and GitHub repository for one department", HEX.saffron],
    ["Department Programme", "Core AI track plus FDE, with labs, capstones and certification preparation", HEX.chakra],
    ["University Transformation", `All ${N} courses, Centre of Excellence, research and accreditation support`, HEX.green]];
  em.forEach(([t, d, col], j) => {
    const x = 0.6 + j * 4.1;
    s.addShape(S.ROUNDED_RECTANGLE, { x, y: 5.15, w: 3.9, h: 1.3, rectRadius: 0.1, fill: { color: col }, line: { color: col }, objectName: "engagement model" });
    s.addText([{ text: t, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 12 } }], { x: x + 0.2, y: 5.15, w: 3.5, h: 1.3, color: HEX.white, valign: "middle", margin: 0, isTextBox: true });
  });
  s.addText([{ text: "How it runs: ", options: { bold: true, color: HEX.navy } }, { text: "Discover", options: { bold: true, color: HEX.saffronDk } }, { text: "  →  ", options: { color: HEX.muted } },
    { text: "Design", options: { bold: true, color: HEX.chakra } }, { text: "  →  ", options: { color: HEX.muted } }, { text: "Deliver", options: { bold: true, color: HEX.greenDk } },
    { text: "  →  ", options: { color: HEX.muted } }, { text: "Measure", options: { bold: true, color: HEX.goldDk } }, { text: ", reviewed every semester", options: { color: HEX.muted } }],
    { x: 0.6, y: 6.55, w: 12.1, h: 0.38, fontSize: 14, margin: 0, isTextBox: true });
  s.addNotes("Ten services and three engagement models, from a one-department pilot to university-wide transformation.");

  // assessment donut
  s = content("Partnership");
  s.addText("Assessment and outcome-based education", { placeholder: "title" });
  s.addChart(pres.charts.DOUGHNUT, [{ name: "Assessment", labels: ["Continuous lab work & notebooks", "Two mid-term evaluations", "Mini-project / sprint reviews", "Enterprise capstone (demo + report)"], values: [20, 20, 20, 40] }],
    { x: 0.6, y: 1.4, w: 5.6, h: 5.3, holeSize: 55, chartColors: [HEX.saffron, HEX.chakra, HEX.green, HEX.gold], showValue: false, showPercent: true, showLegend: false,
      dataLabelColor: HEX.white, dataLabelFontSize: 14, dataLabelFontBold: true, dataLabelFontFace: "+mn-lt", showTitle: false, objectName: "assessment doughnut" });
  const al = [["Continuous lab work & notebooks", "20%", HEX.saffron], ["Two mid-term evaluations", "20%", HEX.chakra], ["Mini-project / sprint reviews", "20%", HEX.green], ["Enterprise capstone (demo + report)", "40%", HEX.gold]];
  al.forEach(([t, v, col], j) => {
    const y = 1.6 + j * 0.62;
    s.addShape(S.ROUNDED_RECTANGLE, { x: 6.7, y: y + 0.06, w: 0.8, h: 0.4, rectRadius: 0.08, fill: { color: col }, line: { color: col } });
    s.addText(v, { x: 6.7, y: y + 0.06, w: 0.8, h: 0.4, fontSize: 13, bold: true, color: HEX.white, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(t, { x: 7.65, y, w: 5.1, h: 0.52, fontSize: 16, color: HEX.navy, valign: "middle", margin: 0, isTextBox: true });
  });
  const obe = ["Five COs per course mapped to Bloom levels L2–L6", "Git, code review and CI/CD on every lab", "Model cards, data sheets and a risk register per product", "Evidence ready for NBA, NAAC and NIRF"];
  for (const [j, t] of obe.entries()) {
    const y = 4.3 + j * 0.58;
    s.addImage({ data: await icon("FaCheckCircle", HEX.green), x: 6.7, y: y + 0.08, w: 0.32, h: 0.32, altText: "check" });
    s.addText(t, { x: 7.15, y, w: 5.6, h: 0.5, fontSize: 15, color: HEX.ink, valign: "middle", margin: 0, isTextBox: true });
  }
  s.addNotes("Forty percent of each course grade comes from the enterprise capstone, so assessment rewards building and shipping.");

  // closing
  s = pres.addSlide({ masterName: "DARK", sectionTitle: "Partnership" });
  chakra(s, 6.667, 1.35, 0.72, "3E5BD8", 0.8);
  s.addText("PARTNER WITH ALGOPROFESSOR", { x: 1.0, y: 2.3, w: 11.33, h: 0.4, fontSize: 15, bold: true, color: HEX.gold, align: "center", charSpacing: 2, margin: 0, isTextBox: true });
  s.addText("Build an AI-Ready University for 2026–2035", { x: 1.0, y: 2.75, w: 11.33, h: 1.0, fontFace: "Cambria", fontSize: 40, bold: true, color: HEX.white, align: "center", margin: 0, isTextBox: true });
  s.addText("Vice-Chancellors, Deans and HoDs: let's schedule a curriculum consultation.", { x: 1.0, y: 3.8, w: 11.33, h: 0.45, fontSize: 18, color: "D9DFEA", align: "center", margin: 0, isTextBox: true });
  s.addShape(S.ROUNDED_RECTANGLE, { x: 3.67, y: 4.5, w: 6.0, h: 1.3, rectRadius: 0.12, fill: { color: HEX.navyMid }, line: { color: HEX.gold, width: 1.5 }, objectName: "contact card" });
  s.addText([{ text: "cto@algoprofessor.com", options: { fontSize: 24, bold: true, color: HEX.gold, breakLine: true } }, { text: "www.algoprofessor.com   ·   campus.algoprofessor.com", options: { fontSize: 15, color: HEX.white } }],
    { x: 3.67, y: 4.5, w: 6.0, h: 1.3, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Explore in 3D: drssnaiml1-cell.github.io/enterprise-ai-syllabus", { x: 1.0, y: 6.0, w: 11.33, h: 0.35, fontSize: 13, color: "C9D3E3", align: "center", margin: 0, isTextBox: true });
  ribbon(s, 5.74, 6.6);
  s.addNotes("Close with the invitation to partner and the contact details.");

  const out = path.join(ROOT, "slides", "Enterprise_AI_Curriculum.pptx");
  await pres.writeFile({ fileName: out });
  if (SKILL) { const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js")); await applyTheme(out, THEME); }
  console.log("written", out);
})().catch((e) => { console.error(e); process.exit(1); });
