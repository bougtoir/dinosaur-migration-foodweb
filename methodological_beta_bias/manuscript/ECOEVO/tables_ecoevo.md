<!-- TABLE:1 -->
**Table 1.** False-contrast rate (proportion of replicates in which the absolute value of Δβ_obs exceeds the threshold) by small-guild pool size and threshold, with Δβ_true = 0; comparison guild 26 taxa; 200 replicates per cell (seed 20260922).

| Small-guild pool size | Threshold 0.05 | Threshold 0.10 | Threshold 0.20 |
|---|---|---|---|
| 2 | [[fc_rate_pool2_thr0.05|2]] | [[fc_rate_pool2_thr0.10|2]] | [[fc_rate_pool2_thr0.20|2]] |
| 4 | [[fc_rate_pool4_thr0.05|2]] | [[fc_rate_pool4_thr0.10|2]] | [[fc_rate_pool4_thr0.20|2]] |
| 12 | [[fc_rate_pool12_thr0.05|2]] | [[fc_rate_pool12_thr0.10|2]] | [[fc_rate_pool12_thr0.20|2]] |
| 26 | [[fc_rate_pool26_thr0.05|2]] | [[fc_rate_pool26_thr0.10|2]] | [[fc_rate_pool26_thr0.20|2]] |

<!-- TABLE:2 -->
**Table 2.** Apparent guild contrast Δβ_obs under predator-sampling asymmetry between alternating environmental blocks, with Δβ_true = 0 (pool sizes 26 and 12 taxa; 200 replicates per cell; seed 20260922).

| Predator sampling multiplier (block A relative to block B) | Mean Δβ_obs | 95% replicate interval |
|---|---|---|
| 1 | [[sim05_db_mult1]] | [[sim05_db_mult1.lo]] to [[sim05_db_mult1.hi]] |
| 2 | [[sim05_db_mult2]] | [[sim05_db_mult2.lo]] to [[sim05_db_mult2.hi]] |
| 4 | [[sim05_db_mult4]] | [[sim05_db_mult4.lo]] to [[sim05_db_mult4.hi]] |
| 8 | [[sim05_db_mult8]] | [[sim05_db_mult8.lo]] to [[sim05_db_mult8.hi]] |

<!-- TABLE:3 -->
**Table 3.** Recommended diagnostic sequence for guild-level beta-diversity contrasts. Each row pairs a structural mechanism examined in this study with a diagnostic recommended, where the data allow, before an observed contrast is interpreted ecologically; the sequence is not a validated decision rule.

| Structural mechanism | Failure mode | Recommended diagnostic | Evidence in this study |
|---|---|---|---|
| Unequal regional pool (gamma imbalance) | False differentiation | Pool-size-matched null model | Simulation 1; Fig. 2a; Table 1 |
| Dominant taxon | False differentiation | Occupancy inspection; leave-one-dominant analysis | Simulation 2; Fig. 2b |
| Taxonomic lumping | False differentiation (apparent continuity) | Cross-resolution sensitivity test | Simulation 3; Fig. 4a |
| Temporal aggregation | Erasure of a structural contrast; amplification of an ecological contrast (source-dependent) | Re-analysis at the finest available temporal bins; aggregation survival not treated as robustness | Simulations 4 and 4b; Fig. 4b |
| Asymmetric sampling | Small bias under the tested parameters; parameter-dependent in general | Inspection of collection-effort and detection structure | Simulation 5; Table 2 |
| Distance-decay geometry | Distorted apparent decay slope | Decay-slope comparison under structural controls | Two-dimensional simulation; Fig. 3b |
| Joint structural factors | Non-additive combined bias; extreme false differences | Factorial or multi-factor robustness check | Simulation 6; Fig. 5 |
