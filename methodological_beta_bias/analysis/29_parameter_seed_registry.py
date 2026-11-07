"""Write results/parameter_seed_registry.csv: every module-level constant
(seeds, replicate counts, grid sizes, default parameters) and every
literal parameter grid in the simulation and empirical scripts, read
statically with `ast` (scripts are not executed)."""
import ast
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT.parent
SCRIPTS = sorted((ROOT / "analysis").glob("0[1-8]_*.py")) + [
    ROOT / "analysis" / n for n in ("12_presence_model_robustness.py",
                                    "13_2d_robustness.py",
                                    "21_temporal_false_negative.py",
                                    "22_false_contrast_threshold.py",
                                    "sim_core.py")] + [
    PROJ / "analysis" / "05_beta_diversity.py",
    PROJ / "analysis" / "07_exploratory_reverse_signal.py",
    PROJ / "analysis" / "11_nemegt_validation.py"]

rows = []
for p in SCRIPTS:
    tree = ast.parse(p.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id.isupper():
            try:
                val = ast.literal_eval(node.value)
            except Exception:
                continue
            rows.append({"script": str(p.relative_to(PROJ)),
                         "name": node.targets[0].id, "value": repr(val),
                         "kind": "module constant", "line": node.lineno})
    for node in ast.walk(tree):
        if isinstance(node, ast.For) and isinstance(node.iter, (ast.Tuple, ast.List)):
            try:
                val = ast.literal_eval(node.iter)
            except Exception:
                continue
            tgt = ast.unparse(node.target)
            rows.append({"script": str(p.relative_to(PROJ)), "name": tgt,
                         "value": repr(val), "kind": "loop grid",
                         "line": node.lineno})
out = ROOT / "results" / "parameter_seed_registry.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["script", "name", "value", "kind", "line"])
    w.writeheader()
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
