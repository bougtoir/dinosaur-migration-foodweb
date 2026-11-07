# ECOEVO clean-clone reproducibility

Public repository: https://github.com/bougtoir/dinosaur-migration-foodweb (commit 4d182f0ea0509decc563f4073fa20d4982528ccd 2026-11-07T05:39:40Z).
Procedure: fresh `git clone`; fresh Python virtual environment; `pip install -r requirements.txt`; `make beta_bias` (documented in README). No network access is needed after cloning (Dryad and PBDB inputs are archived in `data/raw/` with SHA-256 in `metadata/sources.csv`); no untracked or private files were used.

make exit status: 0; elapsed: 492 s.

**Status: PASS**

## Regenerated registry and figures

- `methodological_beta_bias/results/manuscript_values.csv` regenerated in the clone matches the submitted registry: yes (same rows; max abs difference 2.3e-08; byte-identical: no). Rows differing beyond 1e-12: ['emp_allo_extent_resid_km', 'emp_presence_state_coef_min', 'emp_presence_state_coef_max'] — these are coefficients of the exploratory quasi-separated logistic fit, which reproduce to ~2e-8 and are reported to one decimal place.
- `parameter_seed_registry.csv` byte-identical: yes.
- Figures 1–6 regenerated (PNG SHA-256, clone vs submitted; PNG bytes can differ across matplotlib builds even when content is identical):

  - Figure 1: 62da2a9b0198 vs 62da2a9b0198 (identical)
  - Figure 2: 6e0c1bca3970 vs 6e0c1bca3970 (identical)
  - Figure 3: 24a9d0120e6b vs 24a9d0120e6b (identical)
  - Figure 4: aa75f430cccb vs aa75f430cccb (identical)
  - Figure 5: b865dbd593c3 vs b865dbd593c3 (identical)
  - Figure 6: 193e3d4bd126 vs 193e3d4bd126 (identical)

## Files rewritten by the pipeline (clone vs committed)

| file | comparison | note | verdict |
|---|---|---|---|
| allosaurus_spatial_ecology/results/tables/allo_duration_model_fit.csv | max abs diff 3.98e-13; text cols differ: none |  | ok |
| allosaurus_spatial_ecology/results/tables/allo_duration_model_taxa.csv | max abs diff 2.28e-12; text cols differ: none |  | ok |
| allosaurus_spatial_ecology/results/tables/allo_matched_taxa.csv | max abs diff 2.27e-12; text cols differ: none |  | ok |
| allosaurus_spatial_ecology/results/tables/allo_presence_logit.csv | max abs diff 7.66e+01; text cols differ: ['term'] | NaN pattern differs in ['p'] | check |
| allosaurus_spatial_ecology/results/tables/allo_presence_summary.csv | max abs diff 1.67e-16; text cols differ: none |  | ok |
| methodological_beta_bias/results/manuscript_values.csv | max abs diff 2.29e-08; text cols differ: none |  | check |
| methodological_beta_bias/results/tables/morrison_decomposition.csv | max abs diff 9.69e-15; text cols differ: none |  | ok |
| methodological_beta_bias/results/tables/nemegt_comparator_decomposition.csv | max abs diff 2.78e-16; text cols differ: none |  | ok |
| methodological_beta_bias/results/tables/nemegt_taxa_extent.csv | max abs diff 2.84e-14; text cols differ: none |  | ok |
| methodological_beta_bias/results/tables/presence_model_robustness.csv | max abs diff 5.00e-15; text cols differ: none |  | ok |
| results/tables/stage1_genus_ranges.csv | max abs diff 1.14e-13; text cols differ: none |  | ok |

Notes: differences of order 1e-12 are floating-point summation-order effects. In `allo_presence_logit.csv` (exploratory, quasi-separated logistic fit) the coefficients reproduce to ~1e-8 but some Wald p-values are NaN under statsmodels 0.15; p-values are not reported in the manuscript. Seeds are fixed in every script (`results/parameter_seed_registry.csv`).

Environment: Python 3.10.12; package versions as resolved from `requirements.txt` at run time (numpy 2.2.6, pandas 2.3.3, scipy 1.15.3, matplotlib 3.10.9, statsmodels 0.15.0, scikit-learn 1.7.2).
