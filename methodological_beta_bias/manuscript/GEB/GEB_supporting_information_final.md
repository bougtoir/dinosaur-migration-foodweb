# Supporting information (Global Ecology and Biogeography)

**Table S1.** Simulation parameter registry: all scripts (01–06, 13),
site counts, range breadth, occupancy probability, replicate counts
and frozen seed sets 20260920–20260924; null-model definitions;
full seed list.

**Table S2.** Full sweep outputs: sim01 gamma sweep, sim02 dominance
sweep, sim03 lumping levels, sim04 temporal bins, sim06 factorial
grid (CSV exports, unchanged).

**Table S3.** Asymmetric-sampling sweep (sim05): Δβ_obs by sampling
multiplier 1–8×.

**Table S4.** Presence/collection model details: predictor set,
unpenalized pseudo-R² with convergence warning, L2-penalized refits
(C = 0.1, 1, 10) and coefficients.

**Table S5.** Taxonomic mapping: Maidment 2024 guild assignments
(predator/herbivore) and species-to-genus resolution list.

**Table S6.** Nemegt full decomposition including dominant-predator
(Tarbosaurus) diagnostics, downsampling and taphonomic tests.

**Table S7.** False-contrast threshold sensitivity (sim01 arm):
false-contrast rate at |Δβ_obs| > 0.05 / 0.10 / 0.20 for pool sizes
2, 4, 12, 26 (false_contrast_threshold_sensitivity.csv).

**Table S8.** Nonzero-contrast temporal-aggregation scenarios
(sim21): breadth parameters, thin-slice Δβ_true, per-bin Δβ_obs,
attenuation fractions.

**Figure S1.** Asymmetric-sampling effect on Δβ_obs (sim05).

**Figure S2.** Temporal-aggregation curves at alternative bin widths.

**Figure S3.** Morrison occurrence-locality map and collection
environment structure.

**Figure S4.** Presence-model robustness: unpenalized vs L2 fits.

**Figure S5.** Nemegt extended diagnostics (Tarbosaurus).

**Text S1.** Independent evidence audit (INDEPENDENT_EVIDENCE_AUDIT.md):
isotopes, trackways, feeding traces — classifications and citations.

**Table S9.** Two-dimensional robustness simulation details: lattice
geometry, disc-range generation, gamma-pool and temporal arms,
distance-decay slope estimation (binned beta-vs-distance curves).

**Table S10.** Species-resolution analysis: Δβ at genus and species
levels, Allosaurus-exclusion sensitivity, extent residual and
pseudo-R² with convergence status.

**Text S2.** Code provenance: sha256 checksums of raw inputs,
metadata/sources.csv, and the value-level traceability table
(results/manuscript_values.csv).

**Text S3.** Temporal-pooling saturation. For union pooling across k
time slices with per-slice presence probability p, pooled presence is
1 − (1 − p)^k; widespread taxa saturate first, so aggregation distorts
measured turnover asymmetrically depending on whether the contrast's
provenance is structural or ecological.
