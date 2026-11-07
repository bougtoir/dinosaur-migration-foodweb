# Migration sustained dinosaur food webs

Tests whether Late Jurassic (Morrison Formation) dinosaur food webs were
spatially coupled by seasonal movement of large herbivorous dinosaurs, and
whether migratory prey bias fossil predator/prey ratios.

Full analysis plan: see `ANALYSIS_PLAN.md`. Data sources and provenance:
`DATA_SOURCES.md` and `metadata/sources.csv`.

## Reproduce

```bash
pip install -r requirements.txt
python3 src/download/fetch_data.py   # Dryad download requires Chrome via CDP
make stage1                         # data audit -> beta diversity -> sensitivity
make beta_bias                      # methodological beta-bias study (below)
```

### Methodological beta-bias study

`make beta_bias` reruns, from the archived inputs in `data/raw/` and
`data/processed/` (no network access needed), every simulation, the
Morrison sequential decomposition, the Nemegt comparator, the value
registry `methodological_beta_bias/results/manuscript_values.csv`, the
parameter/seed registry
`methodological_beta_bias/results/parameter_seed_registry.csv` and the
article figures (`methodological_beta_bias/figures/ecoevo/`). Seeds are
fixed in each script. Runtime is roughly 15 minutes on one CPU core.
The independent-evidence audit is
`methodological_beta_bias/INDEPENDENT_EVIDENCE_AUDIT.md`.

## Repository layout

```
data/{raw,interim,processed}   datasets (raw never overwritten; sha256 logged)
metadata/                      sources.csv, taxonomy_reconciliation.csv
src/download/                  data acquisition with provenance
analysis/                      numbered pipeline scripts (01-06 = Stage 1)
results/{tables,models,diagnostics}
figures/{main,extended_data}
manuscript/
tests/
```

## Stage 1 status

See `STATUS.md` and `results/stage1_report.md`.
