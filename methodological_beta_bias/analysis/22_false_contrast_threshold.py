"""False-contrast threshold sensitivity for Simulation 1.

Replicates the sim01 gamma-imbalance setting (frozen seed 20260922,
identical generator) and reports the false-contrast rate under three
operational thresholds: |delta_beta| > 0.05, 0.10, 0.20, for pool
sizes 2, 4, 12, 26.

Output: results/tables/false_contrast_threshold_sensitivity.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sim_core import gen_guild, delta_beta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "tables"

RNG_SEED = 20260922
N_LOC = 200
BREADTH = 0.45
OCC_P = 0.35
N_H = 26
REPS = 200
THRESHOLDS = (0.05, 0.10, 0.20)


def main() -> None:
    rng = np.random.default_rng(RNG_SEED)
    rows = []
    for n_p in (2, 4, 12, 26):
        vals = []
        for _ in range(REPS):
            mh = gen_guild(N_LOC, N_H, BREADTH, OCC_P, rng)
            mp = gen_guild(N_LOC, n_p, BREADTH, OCC_P, rng)
            vals.append(delta_beta(mh, mp))
        v = np.asarray(vals)
        for thr in THRESHOLDS:
            rows.append({
                "n_pred_taxa": n_p,
                "threshold": thr,
                "false_contrast_rate": float(np.mean(np.abs(v) > thr)),
                "replicates": REPS,
            })
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "false_contrast_threshold_sensitivity.csv",
              index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
