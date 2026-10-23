"""Build the JBI submission package from JBI component sources.

Assembles JBI_main_blinded_final.md, then builds:
- JBI_main_blinded_final.docx (title + running title + abstract +
  keywords + body + references + data accessibility + embedded figures)
- JBI_title_page_final.docx
- JBI_cover_letter_final.docx
- JBI_supporting_information_final.docx
- submission/JBI_submission_package_final.zip

Frozen analysis results are not touched.
"""
import re
import zipfile
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "manuscript"
JBI = M / "JBI"
FIGDIR = ROOT / "figures"
SUB = JBI / "submission"
SUB.mkdir(exist_ok=True)

TITLE = "Assemblage structure distorts beta diversity and distance decay"
RUNNING = "Bias in spatial turnover inference"
KEYWORDS = ("assemblage structure; beta diversity; biogeography; "
            "distance decay; gamma diversity; spatial turnover; "
            "taxonomic aggregation; temporal aggregation")

FIGMAP = {
    "Figure 1": "fig_geb1_conceptual.png",
    "Figure 2": "fig_geb2_gamma_dominance.png",
    "Figure 3": "fig_geb3_2d_decay.png",
    "Figure 4": "fig_geb4_lumping_temporal.png",
    "Figure 5": "fig3_bias_heatmap.png",
    "Figure 6": "fig_geb6_empirical.png",
}
INSERT_AFTER = {
    "Figure 1": "Our objectives are",
    "Figure 2": "(Fig. 2a)",
    "Figure 3": "(Fig. 3)",
    "Figure 4": "Fig. 4b)",
    "Figure 5": "(Fig. 5)",
    "Figure 6": "(Fig. 6)",
}
EQUATIONS = {
    "Δβ = β_P − β_H",
    "Bias = Δβ_obs − Δβ_true.",
    "Δβ_obs = Δβ_eco + B_γ + B_D + B_T + B_L + B_S + ε",
}


def body(p):
    t = Path(p).read_text().strip()
    lines = t.split("\n")
    while lines and re.match(r"^#{1,3}\s", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip()


# ---------------- assemble main md ----------------
parts = [
    f"# {TITLE}",
    "*(blinded main text — double-anonymous review)*",
    "",
    f"**Running title:** {RUNNING}",
    "",
    "## Abstract",
    "",
    body(JBI / "JBI_structured_abstract.md"),
    "",
    f"**Keywords:** {KEYWORDS}",
    "",
    "## Introduction",
    body(JBI / "introduction_jbi.md"),
    "",
    "## Methods",
    body(JBI / "methods_jbi.md"),
    "",
    "## Results",
    body(JBI / "results_jbi.md"),
    "",
    "## Discussion",
    body(JBI / "discussion_jbi.md"),
    "",
    "## References",
    "",
    "See bibliography.md (55 DOI-verified entries; reference_audit.csv).",
    "",
    "## Data Accessibility Statement",
    "",
    body(JBI / "JBI_data_accessibility_statement.md"),
    "",
]
(JBI / "JBI_main_blinded_final.md").write_text("\n".join(parts))
print("rebuilt JBI_main_blinded_final.md")


def newdoc():
    d = Document()
    d.styles["Normal"].font.name = "Times New Roman"
    d.styles["Normal"].font.size = Pt(11)
    return d


# ---------------- blinded main docx ----------------
CAPTIONS = (JBI / "JBI_figure_captions.md").read_text()
cap = {}
for m in re.finditer(r"\*\*Figure (\d)\.\s*(.*?)\*\*\s*(.*?)(?=\n\*\*Figure|\Z)",
                     CAPTIONS, re.S):
    cap[f"Figure {m.group(1)}"] = (
        f"Figure {m.group(1)}. {m.group(2)} {m.group(3).strip()}")

doc = newdoc()


def omml_run(text, italic=True):
    r = OxmlElement("m:r")
    if italic:
        stl = OxmlElement("m:sty")
        stl.set(qn("m:val"), "i")
        r.append(stl)
    t = OxmlElement("m:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    return r


def omml_ssub(base, sub):
    s = OxmlElement("m:sSub")
    e = OxmlElement("m:e")
    e.append(omml_run(base))
    sb = OxmlElement("m:sub")
    sb.append(omml_run(sub))
    s.append(e)
    s.append(sb)
    return s


def add_equation(text):
    p = doc.add_paragraph()
    p.alignment = 1
    omath = OxmlElement("m:oMathPara")
    om = OxmlElement("m:oMath")
    for tok in text.rstrip(".").split(" "):
        if "_" in tok:
            base, sub = tok.split("_", 1)
            om.append(omml_ssub(base, sub))
        elif tok in {"=", "+", "−", "-"}:
            om.append(omml_run(f" {tok} ", italic=False))
        else:
            om.append(omml_run(tok))
    omath.append(om)
    p._p.append(omath)


def add_fig(key):
    doc.add_picture(str(FIGDIR / FIGMAP[key]), width=Inches(6.0))
    doc.paragraphs[-1].alignment = 1
    p = doc.add_paragraph(cap.get(key, key))
    p.runs[0].font.size = Pt(9)


def add_md_table(rows):
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = "Table Grid"
    for i, row in enumerate(rows):
        for j, celltxt in enumerate(row):
            c = tbl.cell(i, j)
            c.text = celltxt.strip()
            if i == 0:
                c.paragraphs[0].runs[0].bold = True
            for pr in c.paragraphs:
                for rn in pr.runs:
                    rn.font.size = Pt(9)


doc.add_heading(TITLE, 0)
p = doc.add_paragraph()
p.add_run(f"Running title: {RUNNING}").italic = True
doc.add_paragraph("Blinded main text (double-anonymous).").italic = True

lines = (JBI / "JBI_main_blinded_final.md").read_text().split("\n")
blocks = []
buf = []
tbl = []


def flush_buf():
    if buf:
        blocks.append(("p", " ".join(buf)))
        buf.clear()


def flush_tbl():
    if tbl:
        rows = []
        for ln in tbl:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if set("".join(cells)) <= {"-", ":"}:
                continue
            rows.append(cells)
        if rows:
            blocks.append(("tbl", rows))
        tbl.clear()


for line in lines:
    s = line.strip()
    if s.startswith("|") and s.endswith("|"):
        flush_buf()
        tbl.append(s)
        continue
    flush_tbl()
    if not s:
        flush_buf()
        continue
    if s.startswith("#"):
        flush_buf()
        blocks.append(("h", s))
        continue
    if s in EQUATIONS:
        flush_buf()
        blocks.append(("eq", s))
        continue
    buf.append(s)
flush_buf()
flush_tbl()

inserted = set()
for kind, s in blocks:
    if kind == "h":
        if s.startswith("# ") or s.startswith("*(blinded"):
            continue
        level = 1 if s.startswith("## ") else 2
        doc.add_heading(s.lstrip("#").strip(), level)
        continue
    if kind == "eq":
        add_equation(s)
        continue
    if kind == "tbl":
        add_md_table(s)
        continue
    if s.startswith("See bibliography.md"):
        continue
    s2 = s.replace("**", "")
    doc.add_paragraph(s2)
    for key, marker in INSERT_AFTER.items():
        if key not in inserted and marker in s2:
            add_fig(key)
            inserted.add(key)

doc.add_page_break()
doc.add_heading("References", 1)
for ln in (JBI / "bibliography.md").read_text().splitlines():
    ln = ln.strip()
    if ln.startswith("- **"):
        m = re.match(r"- \*\*(.+?)\*\* — (.*)", ln)
        doc.add_paragraph(m.group(2) if m else ln[2:])

doc.save(JBI / "JBI_main_blinded_final.docx")
print("built JBI_main_blinded_final.docx; figures inserted:",
      sorted(inserted))

# ---------------- title page docx ----------------
d = newdoc()
d.add_heading(TITLE, 0)
for t in (JBI / "JBI_title_page_final.md").read_text().split("\n"):
    s = t.strip()
    if not s or s.startswith("#") or s == TITLE:
        continue
    d.add_paragraph(s.replace("**", ""))
d.save(JBI / "JBI_title_page_final.docx")

# ---------------- cover letter docx ----------------
d = newdoc()
d.add_heading("Cover letter — Journal of Biogeography", 0)
for t in (JBI / "JBI_cover_letter_final.md").read_text().split("\n"):
    s = t.strip()
    if not s or s.startswith("#"):
        continue
    d.add_paragraph(s.replace("**", "").replace("“", "“").replace("”", "”"))
d.save(JBI / "JBI_cover_letter_final.docx")

# ---------------- zip ----------------
figs = {k: FIGDIR / v for k, v in FIGMAP.items()}
zpath = SUB / "JBI_submission_package_final.zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for f in ["JBI_main_blinded_final.docx", "JBI_main_blinded_final.md",
              "JBI_title_page_final.docx", "JBI_title_page_final.md",
              "JBI_structured_abstract_final.md",
              "JBI_cover_letter_final.docx", "JBI_cover_letter_final.md",
              "JBI_biosketch.md", "JBI_data_accessibility_statement.md",
              "JBI_author_contributions.md", "JBI_keywords.md",
              "JBI_figure_captions_final.md",
              "JBI_bibliography_final.md",
              "JBI_CITATION_ECOLOGY_AUDIT.md",
              "JBI_EDITORIAL_FIT_AUDIT.md",
              "JBI_TRANSFER_DECISION.md",
              "JBI_SI_INVENTORY.md",
              "JBI_SI_CITATION_AUDIT.md",
              "JBI_DISPLAY_ITEM_ORDER_AUDIT.md",
              "JBI_submission_checklist_final.md",
              "title_candidates_JBI.md"]:
        z.write(JBI / f, f)
    for key, fp in figs.items():
        zname = fp.name.replace("fig_geb", "fig_jbi").replace(
            "fig3_", "fig_jbi5_")
        z.write(fp, f"figures/{zname}")
    z.write(JBI / "bibliography.md", "references.md")
    z.write(ROOT / "results" / "manuscript_values.csv",
            "manuscript_values.csv")
print("wrote", zpath)
