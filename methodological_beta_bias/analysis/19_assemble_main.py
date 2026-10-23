"""Assemble GEB_main_blinded.md from component drafts.
Deterministic concatenation — run after editing any component file.
Leading heading lines of component files are stripped; the assembly
owns section headings."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "manuscript"
GEB = M / "GEB"


def body(p):
    t = Path(p).read_text().strip()
    # drop leading standalone heading lines (# ... or ## ... (suffix))
    lines = t.split("\n")
    while lines and re.match(r"^#{1,3}\s", lines[0]) and \
            lines[0].strip().rstrip().endswith((")", "abstract", "Results",
                                                "Methods", "Introduction",
                                                "Discussion")):
        lines.pop(0)
    return "\n".join(lines).strip()


parts = [
    "# Structural asymmetries distort guild-level beta-diversity contrasts",
    "*(blinded main text — double-anonymous review)*",
    "",
    "## Abstract",
    "",
    body(GEB / "GEB_structured_abstract.md"),
    "",
    "## Introduction",
    body(GEB / "introduction_geb.md"),
    "",
    "## Methods",
    body(M / "methods.md"),
    "",
    "## Results",
    body(M / "results.md"),
    "",
    "## Discussion",
    body(GEB / "discussion_geb.md"),
    "",
    "## References",
    "",
    "See bibliography.md (52 DOI-verified entries; reference_audit.csv).",
    "",
]
(GEB / "GEB_main_blinded.md").write_text("\n".join(parts))
print("rebuilt GEB_main_blinded.md")
