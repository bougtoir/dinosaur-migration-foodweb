"""Build the Ecology and Evolution submission package.

Sources: manuscript/ECOEVO/*_ecoevo.md (numbers written as [[value_id|fmt]]
tokens resolved from results/manuscript_values.csv), bibliography_ecoevo.md
(from 27_ecoevo_references.py), figures/ecoevo/ (from 28_ecoevo_figures.py).

Outputs (manuscript/ECOEVO/build/):
  ECOEVO_main_manuscript.docx   submission main document (tables after
                                references, figure legends, no embedded figures,
                                continuous line numbers, page numbers)
  ECOEVO_main_manuscript_inline.docx   same text with figures/tables inline
  ECOEVO_title_page.docx, ECOEVO_cover_letter.docx, ECOEVO_tables.docx
  ECOEVO_figures.pptx           one editable slide per figure
  ECOEVO_main_resolved.md, token_log.csv
  submission/ECOEVO_submission_package.zip
Fails loudly on: unresolved tokens, uncited/missing references, figures or
tables first cited out of order, first-person plural, stale journal or
supplement wording, literal markdown in docx, line breaks inside runs.
"""
import csv
import re
import shutil
import sys
import zipfile
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "manuscript" / "ECOEVO"
B = E / "build"
FIG = ROOT / "figures" / "ecoevo"
B.mkdir(exist_ok=True)
(B / "submission").mkdir(exist_ok=True)

TITLE = "Assemblage structure distorts beta diversity and distance decay"
RUNNING = "Bias in spatial turnover inference"
KEYWORDS = (E / "keywords_ecoevo.md").read_text().strip()
MINUS = "\u2212"
ERRORS = []

# ---------------------------------------------------------------- tokens
REG = pd.read_csv(ROOT / "results" / "manuscript_values.csv", dtype=str)
REG = REG.set_index("value_id")
TOKEN_LOG = []
TOK = re.compile(r"\[\[([^\]\[:]+?)\]\]")


def fmt_num(v, spec):
    if spec == "int":
        return f"{int(round(v)):,}".replace(",", ",")
    if spec.startswith("pct"):
        s = f"{v * 100:.{int(spec[3:])}f}"
    else:
        plus = spec.startswith("+")
        d = int(spec.lstrip("+"))
        s = f"{v:.{d}f}"
        if plus and not s.startswith("-") and float(s) != 0:
            s = "+" + s
    return s.replace("-", MINUS)


def resolve(text, where):
    def rep(m):
        body = m.group(1)
        if body.startswith(("EQ", "TABLE", "INCLUDE")):
            return m.group(0)
        key, _, spec = body.partition("|")
        spec = spec or "3"
        field = "value"
        if key.endswith(".lo"):
            key, field = key[:-3], "CI_lower"
        elif key.endswith(".hi"):
            key, field = key[:-3], "CI_upper"
        if key not in REG.index or pd.isna(REG.loc[key, field]):
            ERRORS.append(f"unresolved token {body} in {where}")
            return "??"
        raw = float(REG.loc[key, field])
        out = fmt_num(raw, spec)
        TOKEN_LOG.append({"file": where, "value_id": key, "field": field,
                          "format": spec, "rendered": out, "registry_value": raw,
                          "source_script": REG.loc[key, "source_script"],
                          "source_output": REG.loc[key, "source_output"]})
        return out
    return TOK.sub(rep, text)


def src(name):
    t = (E / name).read_text()
    t = re.sub(r"\[\[INCLUDE:([^\]]+)\]\]",
               lambda m: (E / m.group(1)).read_text().strip(), t)
    return resolve(t, name)


def blocks(md):
    """Normalise markdown into blocks (no hard wraps survive)."""
    out, buf, tbl = [], [], []

    def fb():
        if buf:
            out.append(("p", " ".join(x.strip() for x in buf)))
            buf.clear()

    def ft():
        if tbl:
            rows = [[c.strip() for c in ln.strip().strip("|").split("|")]
                    for ln in tbl]
            rows = [r for r in rows if not set("".join(r)) <= set("-: ")]
            out.append(("tbl", rows))
            tbl.clear()
    for line in md.split("\n"):
        s = line.strip()
        if s.startswith("<!--"):
            fb(); ft(); continue
        if s.startswith("|") and s.endswith("|"):
            fb(); tbl.append(s); continue
        ft()
        if not s:
            fb(); continue
        if s.startswith("#"):
            fb(); lvl = len(s) - len(s.lstrip("#"))
            out.append((f"h{lvl}", s.lstrip("#").strip())); continue
        m = re.fullmatch(r"\[\[(EQ|TABLE):([^\]]+)\]\]", s)
        if m:
            fb(); out.append((m.group(1).lower(), m.group(2))); continue
        buf.append(s)
    fb(); ft()
    return out


ABSTRACT = blocks(src("abstract_ecoevo.md"))
INTRO = blocks(src("introduction_ecoevo.md"))
METHODS = blocks(src("methods_ecoevo.md"))
RESULTS = blocks(src("results_ecoevo.md"))
DISC = blocks(src("discussion_ecoevo.md"))
TITLEPAGE = blocks(src("title_page_ecoevo.md"))
COVER = blocks(src("cover_letter_ecoevo.md"))
COVER_DIRECT = blocks(src("cover_letter_direct_ecoevo.md"))
LEGENDS = [b for b in blocks(src("figure_legends_ecoevo.md")) if b[0] == "p"]
TABLES_MD = src("tables_ecoevo.md")
TABLES = {}
for part in re.split(r"<!-- TABLE:(\d) -->", TABLES_MD)[1:]:
    pass
for num, body in re.findall(r"<!-- TABLE:(\d) -->(.*?)(?=<!-- TABLE:|\Z)",
                            TABLES_MD, re.S):
    bl = blocks(body)
    TABLES[num] = (bl[0][1], bl[1][1])
BIB = [re.match(r"- \*\*(\S+)\*\* — (.*)", ln).groups()
       for ln in (E / "bibliography_ecoevo.md").read_text().splitlines()
       if ln.startswith("- **")]

EQUATIONS = {
    "delta": [("sub", "Δβ", ""), ("op", "="), ("sub", "β", "P"), ("op", "−"),
              ("sub", "β", "H")],
    "bias": [("t", "Bias"), ("op", "="), ("sub", "Δβ", "obs"), ("op", "−"),
             ("sub", "Δβ", "true")],
    "lumping": [("sub", "B", "lumping"), ("op", "="), ("sub", "β", "species"),
                ("op", "−"), ("sub", "β", "genus")],
    "decomp": [("sub", "Δβ", "obs"), ("op", "="), ("sub", "Δβ", "eco"),
               ("op", "+"), ("sub", "B", "γ"), ("op", "+"), ("sub", "B", "D"),
               ("op", "+"), ("sub", "B", "T"), ("op", "+"), ("sub", "B", "L"),
               ("op", "+"), ("sub", "B", "S"), ("op", "+"), ("t", "ε")],
    "atten": [("t", "A"), ("op", "="), ("t", "1"), ("op", "−"),
              ("frac", [("abs", [("sub", "Δβ", "pooled")])],
               [("abs", [("sub", "Δβ", "thin")])])],
    "union": [("sub", "p", "k"), ("op", "="), ("t", "1"), ("op", "−"),
              ("sup", "(1 − p)", "k")],
}

# ---------------------------------------------------------------- checks
BODY_TEXT = "\n".join(t for bl in (ABSTRACT, INTRO, METHODS, RESULTS, DISC)
                      for k, t in bl if k == "p")
ALL_TEXT = BODY_TEXT + "\n".join(t for k, t in LEGENDS) + TABLES_MD


def first_cites(pattern, text):
    order = []
    for m in re.finditer(pattern, text):
        for n in re.findall(r"\d", m.group(0)):
            if n not in order:
                order.append(n)
    return order


fig_order = first_cites(r"Figs?\. \d[a-z]?(?:(?:, | and |–)\d[a-z]?)*", BODY_TEXT)
tab_order = first_cites(r"Tables? \d(?:(?:, | and |–)\d)*", BODY_TEXT)
if fig_order != [str(i) for i in range(1, 7)]:
    ERRORS.append(f"figure first-citation order {fig_order}")
if tab_order != ["1", "2", "3"]:
    ERRORS.append(f"table first-citation order {tab_order}")
pos_tab = {n: BODY_TEXT.find(f"Table {n}") for n in "123"}

# references <-> citations
flat = re.sub(r"\s+", " ", BODY_TEXT)


def fams(entry):
    head = entry.split(" (")[0]
    names = [n.strip() for n in re.split(r",\s*(?=[A-Z][^,]*,\s*[A-Z]\.)|, & | & ", head)]
    return [n.split(",")[0].strip() for n in names if n], re.search(r"\((\d{4})\)", entry).group(1)


cite_audit = []
for key, entry in BIB:
    fl, yr = fams(entry)
    if len(fl) == 1:
        stem = re.escape(fl[0])
    elif len(fl) == 2:
        stem = re.escape(fl[0]) + " & " + re.escape(fl[1])
    else:
        stem = re.escape(fl[0]) + " et al\\."
    pat = stem + r"(?:,| \()(?: \d{4}[a-z]?,)* ?" + yr
    hits = len(re.findall(pat, flat))
    cite_audit.append({"key": key, "cite_as": re.sub(r"\\", "", stem) + ", " + yr,
                       "in_text_hits": hits})
    if hits == 0:
        ERRORS.append(f"reference not cited: {key} ({stem} {yr})")
known = {(c["cite_as"].rsplit(", ", 1)[0], c["cite_as"].rsplit(", ", 1)[1])
         for c in cite_audit}
for m in re.finditer(r"([A-Z][A-Za-zÀ-ž’'\-]+(?: et al\.| & [A-Z][A-Za-zÀ-ž’'\-]+)?)"
                     r"(?:,| \()((?: \d{4}[a-z]?,)* ?\d{4})", flat):
    for yr in re.findall(r"\d{4}", m.group(2)):
        if (m.group(1), yr) not in known:
            ERRORS.append(f"citation without reference: {m.group(1)} {yr}")

STALE = [r"\bwe\b", r"\bWe\b", r"\bour\b", r"\bOur\b", r"\bus\b", r"\bJBI\b",
         r"\bGEB\b", "Journal of Biogeography", "Global Ecology and Biogeography",
         "Supporting Information", "Supplementary Information",
         "Supplementary Figure", r"Figure S\d", r"Table S\d", r"Appendix S",
         "dispensing", "double-anonymous", "anonymi[sz]ed", "blinded",
         "title page", r"\binside\b the gamma", "sign reversal",
         "true ecological beta", "anonymous repository", "replaced on acceptance",
         "on acceptance", "double-blind", "No journal Supporting Information",
         "Supporting Information is required"]
for pat in STALE:
    for name, txt in (("body", ALL_TEXT),
                      ("title page", "\n".join(t for _, t in TITLEPAGE))):
        if re.search(pat, txt):
            ERRORS.append(f"stale/forbidden wording '{pat}' in {name}")
cover_txt = "\n".join(t for _, t in COVER + COVER_DIRECT)
for pat in [r"\bwe\b", r"\bWe\b", r"\bour\b", r"\bOur\b", r"\bGEB\b",
            "Global Ecology and Biogeography", "anonymi[sz]ed", "anonymous",
            "double-blind", "double-anonymous", "No journal Supporting Information"]:
    if re.search(pat, cover_txt):
        ERRORS.append(f"forbidden wording '{pat}' in cover letter")

# ---------------------------------------------------------------- docx helpers
SUBPAT = re.compile(r"(Δβ|β|B|p|N|A|R)_(obs|true|eco|P|H|species|genus|lumping|"
                    r"D|γ|T|L|S|thin|pooled|k)\b")
INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+`)")


def normalise_styles(doc, size=12):
    st = doc.styles
    for s in st:
        try:
            f = s.font
        except AttributeError:
            continue
        rpr = s.element.find(qn("w:rPr"))
        if rpr is not None:
            rf = rpr.find(qn("w:rFonts"))
            if rf is not None:
                for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme",
                          "w:cstheme"):
                    rf.attrib.pop(qn(a), None)
            col = rpr.find(qn("w:color"))
            if col is not None:
                for a in ("w:themeColor", "w:themeShade", "w:themeTint"):
                    col.attrib.pop(qn(a), None)
        f.name = "Times New Roman"
        f.color.rgb = RGBColor(0, 0, 0)
        rpr = s.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts"); rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), "Times New Roman")
    st["Normal"].font.size = Pt(size)
    for lvl, sz in ((1, 14), (2, 12), (3, 12)):
        h = st[f"Heading {lvl}"]
        h.font.size = Pt(sz); h.font.bold = True; h.font.italic = (lvl == 3)
    st["Title"].font.size = Pt(16); st["Title"].font.bold = True
    tppr = st["Title"].element.find(qn("w:pPr"))
    if tppr is not None:
        for bd in tppr.findall(qn("w:pBdr")):
            tppr.remove(bd)
    pf = st["Normal"].paragraph_format
    pf.line_spacing = 2.0
    pf.space_after = Pt(0)


def add_runs(par, text, size=None, italic=False):
    for piece in INLINE.split(text):
        if not piece:
            continue
        bold = ital = False
        if piece.startswith("**"):
            piece, bold = piece[2:-2], True
        elif piece.startswith("`"):
            piece = piece[1:-1]
        elif piece.startswith("*"):
            piece, ital = piece[1:-1], True
        pos = 0
        for m in SUBPAT.finditer(piece):
            if m.start() > pos:
                r = par.add_run(piece[pos:m.start()])
                r.bold, r.italic = bold, ital or italic
                if size: r.font.size = Pt(size)
            r = par.add_run(m.group(1)); r.bold, r.italic = bold, ital or italic
            if size: r.font.size = Pt(size)
            r = par.add_run(m.group(2)); r.font.subscript = True
            r.bold, r.italic = bold, ital or italic
            if size: r.font.size = Pt(size)
            pos = m.end()
        if pos < len(piece):
            r = par.add_run(piece[pos:]); r.bold, r.italic = bold, ital or italic
            if size: r.font.size = Pt(size)


def m_r(text, plain=False):
    r = OxmlElement("m:r")
    if plain:
        rp = OxmlElement("m:rPr"); sty = OxmlElement("m:sty")
        sty.set(qn("m:val"), "p"); rp.append(sty); r.append(rp)
    t = OxmlElement("m:t"); t.set(qn("xml:space"), "preserve"); t.text = text
    r.append(t)
    return r


def m_elems(parts):
    out = []
    for p in parts:
        if p[0] == "t":
            out.append(m_r(p[1], plain=len(p[1]) > 1 and p[1].isalpha()))
        elif p[0] == "abs":
            d = OxmlElement("m:d"); dpr = OxmlElement("m:dPr")
            for tag in ("m:begChr", "m:endChr"):
                c = OxmlElement(tag); c.set(qn("m:val"), "|"); dpr.append(c)
            d.append(dpr); e = OxmlElement("m:e")
            for x in m_elems(p[1]): e.append(x)
            d.append(e); out.append(d)
        elif p[0] == "op":
            out.append(m_r(f" {p[1]} ", plain=True))
        elif p[0] in ("sub", "sup"):
            if p[0] == "sub" and not p[2]:
                out.append(m_r(p[1])); continue
            tag = "m:sSub" if p[0] == "sub" else "m:sSup"
            s = OxmlElement(tag); e = OxmlElement("m:e")
            e.append(m_r(p[1]))
            sc = OxmlElement("m:sub" if p[0] == "sub" else "m:sup")
            sc.append(m_r(p[2], plain=len(p[2]) > 1))
            s.append(e); s.append(sc); out.append(s)
        elif p[0] == "frac":
            f = OxmlElement("m:f"); num = OxmlElement("m:num")
            den = OxmlElement("m:den")
            for x in m_elems(p[1]): num.append(x)
            for x in m_elems(p[2]): den.append(x)
            f.append(num); f.append(den); out.append(f)
    return out


def add_equation(doc, name):
    p = doc.add_paragraph(); p.alignment = 1
    mp = OxmlElement("m:oMathPara"); om = OxmlElement("m:oMath")
    for x in m_elems(EQUATIONS[name]): om.append(x)
    mp.append(om); p._p.append(mp)


def add_table(doc, num, single=False):
    cap, rows = TABLES[num]
    p = doc.add_paragraph(); add_runs(p, cap, size=11)
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    for i, row in enumerate(rows):
        if len(row) != len(rows[0]):
            ERRORS.append(f"Table {num} row {i} has {len(row)} cells")
        for j, cell in enumerate(row):
            c = t.cell(i, j); c.text = ""
            par = c.paragraphs[0]
            par.paragraph_format.line_spacing = 1.0
            add_runs(par, cell, size=10)
            if i == 0:
                for r in par.runs: r.bold = True
    return t


def line_numbers_and_footer(doc):
    for sec in doc.sections:
        ln = OxmlElement("w:lnNumType")
        ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
        ln.set(qn("w:distance"), "283")
        sec._sectPr.append(ln)
        p = sec.footer.paragraphs[0]; p.alignment = 1
        r = p.add_run()
        for typ, txt in (("begin", None), (None, "PAGE"), ("end", None)):
            if typ:
                fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), typ)
                r._r.append(fc)
            else:
                it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
                it.text = txt; r._r.append(it)


def newdoc(numbered=True):
    d = Document()
    normalise_styles(d)
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(1)
        s.top_margin = s.bottom_margin = Inches(1)
    if numbered:
        line_numbers_and_footer(d)
    return d


def emit(doc, bl, inline=False, placed=None):
    for kind, val in bl:
        if kind.startswith("h"):
            lvl = {1: 1, 2: 1, 3: 2, 4: 3}[int(kind[1])]
            doc.add_heading(val, lvl)
        elif kind == "eq":
            add_equation(doc, val)
        elif kind == "table":
            if inline:
                add_table(doc, val); placed.add(f"T{val}")
        elif kind == "tbl":
            ERRORS.append("stray table in body")
        else:
            p = doc.add_paragraph(); add_runs(p, val)
            if inline:
                for m in re.finditer(r"Figs?\. (\d)", val):
                    n = m.group(1)
                    if f"F{n}" not in placed:
                        doc.add_picture(str(FIG / f"Figure{n}.png"), width=Inches(6.3))
                        doc.paragraphs[-1].alignment = 1
                        lg = doc.add_paragraph(); add_runs(lg, LEGENDS[int(n) - 1][1], size=10)
                        placed.add(f"F{n}")


def title_block(doc):
    doc.add_paragraph(TITLE, style="Title")
    for t in ("Running title: " + RUNNING, "Article type: Research Article",
              "Author: Tatsuki Onishi",
              "Affiliation: [affiliation to be entered by the author at submission]",
              "Corresponding author: Tatsuki Onishi, [full postal address, e-mail "
              "address and ORCID to be entered by the author at submission]"):
        doc.add_paragraph(t)


def statements(doc):
    keep = False
    for kind, val in TITLEPAGE:
        if kind == "h2":
            keep = True
            doc.add_heading(val, 1)
        elif keep and kind == "p":
            p = doc.add_paragraph(); add_runs(p, val)


def references(doc):
    doc.add_heading("References", 1)
    for _, entry in BIB:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        add_runs(p, entry)


def build_main(inline):
    doc = newdoc()
    placed = set()
    title_block(doc)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    emit(doc, ABSTRACT)
    p = doc.add_paragraph(); r = p.add_run("Keywords: "); r.bold = True
    p.add_run(KEYWORDS)
    for bl in (INTRO, METHODS, RESULTS, DISC):
        emit(doc, bl, inline, placed)
    statements(doc)
    references(doc)
    if not inline:
        for n in ("1", "2", "3"):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            add_table(doc, n)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        doc.add_heading("Figure legends", 1)
        for _, lg in LEGENDS:
            p = doc.add_paragraph(); add_runs(p, lg)
    else:
        missing = {f"F{i}" for i in range(1, 7)} | {"T1", "T2", "T3"}
        if missing - placed:
            ERRORS.append(f"inline build missing {sorted(missing - placed)}")
    return doc


main = build_main(False)
inl = build_main(True)
main.save(B / "ECOEVO_main_manuscript.docx")
inl.save(B / "ECOEVO_main_manuscript_inline.docx")

tp = newdoc(numbered=False)
for kind, val in TITLEPAGE:
    if kind == "h1":
        tp.add_paragraph(val, style="Title")
    elif kind.startswith("h"):
        tp.add_heading(val, 1)
    else:
        p = tp.add_paragraph(); add_runs(p, val)
tp.save(B / "ECOEVO_title_page.docx")

cl = newdoc(numbered=False)
cl.styles["Normal"].paragraph_format.line_spacing = 1.15
for kind, val in COVER:
    p = cl.add_paragraph(); add_runs(p, val)
    p.paragraph_format.space_after = Pt(10)
cl.save(B / "ECOEVO_cover_letter.docx")
cld = newdoc(numbered=False)
cld.styles["Normal"].paragraph_format.line_spacing = 1.15
for kind, val in COVER_DIRECT:
    p = cld.add_paragraph(); add_runs(p, val)
    p.paragraph_format.space_after = Pt(10)
cld.save(B / "ECOEVO_cover_letter_direct_submission.docx")

tb = newdoc(numbered=False)
for i, n in enumerate(("1", "2", "3")):
    if i:
        tb.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    add_table(tb, n)
tb.save(B / "ECOEVO_tables.docx")

# editable figure deck
prs = Presentation(); prs.slide_width = PInches(13.333); prs.slide_height = PInches(7.5)
for i, (_, lg) in enumerate(LEGENDS, 1):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    tx = s.shapes.add_textbox(PInches(0.4), PInches(0.2), PInches(12.5), PInches(0.6))
    tx.text_frame.text = f"Figure {i}"; tx.text_frame.paragraphs[0].runs[0].font.size = PPt(24)
    s.shapes.add_picture(str(FIG / f"Figure{i}.png"), PInches(0.9), PInches(0.9),
                         height=PInches(4.9))
    cb = s.shapes.add_textbox(PInches(0.4), PInches(5.9), PInches(12.5), PInches(1.5))
    cb.text_frame.word_wrap = True
    cb.text_frame.text = re.sub(r"\*\*|\*|_", "", lg)
    for para in cb.text_frame.paragraphs:
        for r in para.runs: r.font.size = PPt(11)
prs.save(B / "ECOEVO_figures.pptx")

# resolved markdown + token log
md = [f"# {TITLE}", "", f"Running title: {RUNNING}", ""]
for bl in (ABSTRACT, INTRO, METHODS, RESULTS, DISC):
    for k, v in bl:
        md.append(("#" * int(k[1]) + " " + v) if k.startswith("h") else
                  (f"[equation: {v}]" if k == "eq" else
                   (f"[Table {v}]" if k == "table" else v)))
        md.append("")
(B / "ECOEVO_main_resolved.md").write_text("\n".join(md))
with open(B / "token_log.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(TOKEN_LOG[0]))
    w.writeheader(); w.writerows(TOKEN_LOG)
with open(B / "citation_audit.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(cite_audit[0]))
    w.writeheader(); w.writerows(cite_audit)

# docx integrity
for f in ("ECOEVO_main_manuscript.docx", "ECOEVO_main_manuscript_inline.docx",
          "ECOEVO_title_page.docx", "ECOEVO_cover_letter.docx",
          "ECOEVO_cover_letter_direct_submission.docx", "ECOEVO_tables.docx"):
    d = Document(B / f)
    texts = [p.text for p in d.paragraphs] + [c.text for t in d.tables
                                              for row in t.rows for c in row.cells]
    for p in d.paragraphs:
        for r in p.runs:
            if "\n" in r.text or "\r" in r.text:
                ERRORS.append(f"line break inside run in {f}")
    for t in texts:
        for bad in ("**", "`", "[[", "]]", "##", "??"):
            if bad in t:
                ERRORS.append(f"literal markup {bad!r} in {f}: {t[:60]}")
    if "Times New Roman" not in (d.styles["Normal"].font.name or ""):
        ERRORS.append(f"font not TNR in {f}")

words = len(re.findall(r"\S+", "\n".join(t for bl in (INTRO, METHODS, RESULTS, DISC)
                                         for k, t in bl if k == "p")))
abs_words = len(re.findall(r"\S+", ABSTRACT[-1][1]))
print(f"main text words (Introduction–Discussion paragraphs): {words}")
print(f"abstract words: {abs_words}")
print(f"tokens resolved: {len(TOKEN_LOG)}; references: {len(BIB)}")

if ERRORS:
    print("BUILD FAILED:")
    for e in dict.fromkeys(ERRORS):
        print("  -", e)
    sys.exit(1)

# ---------------------------------------------------------------- package
SUB = B / "submission"
zpath = SUB / "ECOEVO_submission_package.zip"
MBB = ROOT
PROJ = ROOT.parent
items = [(B / "ECOEVO_main_manuscript.docx", "ECOEVO_main_manuscript.docx"),
         (B / "ECOEVO_main_manuscript_inline.docx", "ECOEVO_main_manuscript_inline.docx"),
         (B / "ECOEVO_title_page.docx", "ECOEVO_title_page.docx"),
         (B / "ECOEVO_cover_letter.docx", "ECOEVO_cover_letter.docx"),
         (B / "ECOEVO_cover_letter_direct_submission.docx",
          "ECOEVO_cover_letter_direct_submission.docx"),
         (B / "ECOEVO_tables.docx", "tables/ECOEVO_tables.docx"),
         (B / "ECOEVO_figures.pptx", "figures/ECOEVO_figures_editable.pptx")]
for i in range(1, 7):
    items += [(FIG / f"Figure{i}.tif", f"figures/Figure{i}.tif"),
              (FIG / f"Figure{i}.png", f"figures/Figure{i}.png")]
items += [(MBB / "INDEPENDENT_EVIDENCE_AUDIT.md",
           "reviewer_files/INDEPENDENT_EVIDENCE_AUDIT.md"),
          (MBB / "results" / "manuscript_values.csv", "reviewer_files/manuscript_values.csv"),
          (PROJ / "metadata" / "sources.csv", "reviewer_files/sources.csv")]
for a in sorted(E.glob("ECOEVO_*.md")):
    items.append((a, f"audits/{a.name}"))
readme = B / "README_package.md"
readme.write_text(
    "# Ecology and Evolution submission package\n\n"
    "- `ECOEVO_main_manuscript.docx`: main document for upload (title page block, "
    "abstract, text, statements, references, Tables 1–3 on separate pages, figure "
    "legends; continuous line numbers).\n"
    "- `ECOEVO_main_manuscript_inline.docx`: identical text with figures and tables "
    "placed after their first citation (reading copy).\n"
    "- `ECOEVO_title_page.docx`; `ECOEVO_cover_letter.docx` (Wiley transfer route); "
    "`ECOEVO_cover_letter_direct_submission.docx` (direct new submission if the transfer "
    "link stays broken; adds the transfer-ticket sentence).\n"
    "- `tables/ECOEVO_tables.docx`: Tables 1–3 (editable).\n"
    "- `figures/Figure1–6.tif` (300 dpi, upload as Figures), `.png` copies, and "
    "`ECOEVO_figures_editable.pptx`.\n"
    "- `reviewer_files/`: source-data registry, manuscript value registry and "
    "independent-evidence audit (canonical copies in the public repository).\n"
    "- `audits/`: pre-submission audit reports.\n")
items.append((readme, "README.md"))
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for p, arc in items:
        if not p.exists():
            sys.exit(f"missing package item {p}")
        assert not arc.startswith(("/", "..")), arc
        z.write(p, arc)
print("wrote", zpath, len(items), "items")
