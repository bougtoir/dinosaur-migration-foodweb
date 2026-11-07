# ECOEVO hostile review (simulated sceptical Ecology and Evolution reviewer)

Scope: manuscript as built by `analysis/26_ecoevo_build.py`. Each objection is
rated for severity (desk-reject / major / minor), whether it is legitimate,
and what was done. Only legitimate weaknesses were repaired; no new analyses
or unsupported claims were added.

## Priority 1 — must be fixed before submission (all resolved)

| # | Objection | Legitimate? | Action |
|---|---|---|---|
| 1 | Factorial "Bias = −0.91" is presented as an interaction result, but at pool 4 with k = 6 the lumping step collapses the whole four-taxon guild into one column, so β_P = 0 by construction and Δβ_obs = −β_H. | Yes (found in this audit: `06_combined_factorial_simulation.py` uses `kk = min(k, n_p)`). | −0.91 retained but explicitly identified as a degenerate boundary cell (Results, Discussion, Fig. 5 legend and in-panel label). Non-degenerate maximum (−0.76; pool 4, p_D = 0.9, k = 3) and the summed single-factor expectation for the same cell (−0.28) added to the registry (`sim06_max_abs_bias_nondegenerate`, `sim06_bias_p4_pd0.9_k3`, `sim06_additive_p4_pd0.9_k3`) and used as the non-additivity evidence. |
| 2 | Methods state the factorial pool axis is 2–26; code uses {4, 12, 26}. | Yes. | Methods corrected to the implemented grid. |
| 3 | "All-negative-sign rate persisted through pools of 20" — registry shows 83.5% negative at pool 20 (100% only up to pool 12). | Yes (prose overstated). | Rewritten: all replicates negative up to pool 12; 83.5% at pool 20 (`sim01_propneg_p20`). |
| 4 | Imposed-contrast temporal arm: the finest-resolution "Δβ_true ≈ −0.05/−0.10/−0.17" values also contain the pool-asymmetry component (pools 26 vs 12 retained). | Yes. | Methods/Results now call them finest-resolution contrasts and state that they combine the imposed ecological difference with the structural component quantified in Simulation 4. |
| 5 | Seed provenance: Methods said the Morrison bootstrap used seed 20260920; the decomposition script uses 20260924. | Yes. | Methods corrected; registry provenance columns corrected (values unchanged). |
| 6 | Citation errors: "Kidwell & Behrensmeyer, 1991" has no matching reference (the entry is Kidwell & Bosence 1991); "Kowalewski, 1999" is a chapter in Martin (1999), a single-author book; Whittaker (1960) DOI pointed to a one-page item in issue 4; Hispanosauropus paper attributed to "Lockley et al." in the evidence audit but its sole author is Foster (2015); Maidment (2024) Dryad dataset has a single creator but was cited as "et al."; two references (Baselga 2012; Noto & Grossman 2010) were listed but never cited. | Yes. | All corrected; Baselga (2012) now cited for the replacement/richness-difference point in the Discussion, Noto & Grossman (2010) for prior Morrison palaeoecology in Methods. Builder fails on any uncited reference or unmatched citation. |
| 7 | Figure 6 drew null intervals as error bars anchored at the observed value (visually implying a CI from −0.55 to −0.23). | Yes. | Figure redrawn: null intervals as shaded bands with the observed value as an open circle; bootstrap CIs as error bars. |
| 8 | Figure 5 colour scale clipped at ±0.5 while bias reached −0.91; embedded stale "Fig.3" title; colour bar overlapping a panel. | Yes. | Redrawn with symmetric unclipped scale, cell values, false-difference outlines and degenerate-cell labels; no embedded title. |

## Priority 2 — high (addressed in text)

| # | Objection | Response |
|---|---|---|
| 9 | Novelty: pool size, dominance, lumping, time averaging and sampling effects are all known. | Agreed and stated in Introduction, Discussion and cover letter. The contribution is framed as controlled magnitude, interaction, distance-decay distortion, source-dependent aggregation, an empirical decomposition and a workflow. No novelty claim for individual mechanisms. |
| 10 | Overgeneralisation from simplified 1-D/2-D simulators. | Magnitudes are described as scenario-specific demonstrations of sufficiency throughout (Abstract, Discussion, Limitations); conceptual applicability is separated from quantitative transferability. |
| 11 | Palaeontology-specificity. | Framing rebuilt around general ecological inference; fossil data presented as stress tests; keywords non-palaeontological; applicability paragraph lists museum, herbarium, monitoring and multi-source data with the explicit caveat that direct tests are needed. |
| 12 | Circular inference: simulations designed to produce bias then "find" it. | The simulations are not used as evidence that bias occurs in nature, only to quantify how large it can be under stated conditions; the Morrison analysis is presented as a worked example, and "structural sufficiency is not causal attribution" is stated in Results, Discussion and Limitations. |
| 13 | Inadequate empirical validation (one formation). | Stated as a limitation; Nemegt is explicitly a structural comparator, not a replication. |
| 14 | Metric dependence (Jaccard only). | Added to Limitations, citing Baselga (2010) and Legendre (2014) on replacement versus richness-difference components; no new metric analyses claimed. |
| 15 | Temporal aggregation operator. | Conclusions explicitly restricted to union pooling; other operators named as untested. |
| 16 | Sampling design (small effect may be parameter-specific). | Stated in Results, Discussion and Table 3 ("small bias under the tested parameters; parameter-dependent in general"). |
| 17 | Taxonomic-resolution assumptions in the Morrison species-level step. | Limitations note dependence on identification completeness. |
| 18 | Presence model non-convergence. | Reported as exploratory only, with the penalised refit and quasi-separation diagnostics. |

## Priority 3 — medium / optional

| # | Objection | Response |
|---|---|---|
| 19 | Distance-decay result rests on one lattice configuration (pool 4). | Reported as a demonstration under identical generative processes; the text explicitly denies that empirical decay differences are generally artefacts. |
| 20 | Gamma-matched null: observed value lies outside the null interval. | Wording fixed as "close to, but marginally more negative than, the lower bound"; never "inside". |
| 21 | Allosaurus behavioural inference. | Discussion explicitly does not claim sedentariness, non-migration or falsified mobility. |
| 22 | Reference to "true ecological beta diversity". | Not used; Δβ_true defined as the simulation-defined contrast. |

## Verdict

No remaining issue is expected to cause desk rejection on scientific grounds.
The remaining risks are judgement calls a reviewer may still raise (simulator
simplicity, single empirical case, Jaccard-only), all disclosed as limitations.

## Final adversarial pass (finalization round)

| # | Rejection attempt | Classification | Basis |
|---|---|---|---|
| 1 | Known mechanisms / weak novelty | Resolved | Novelty explicitly not claimed for any mechanism; contribution stated as magnitude, interaction, distance-decay distortion, source-dependent aggregation, empirical decomposition and workflow (Introduction, Discussion, cover letter) |
| 2 | Excessive palaeontological specificity | Resolved | General ecological-inference framing; fossil data as stress tests; non-palaeontological keywords; applicability to museum, herbarium, monitoring, archaeological and multi-source data without quantitative transport |
| 3 | Oversimplified simulation geometry | Transparently limited | 1-D plus 2-D replication; magnitudes called scenario-specific demonstrations of sufficiency (Abstract, Limitations) |
| 4 | Metric dependence (Jaccard only) | Transparently limited | Stated in Limitations with Baselga (2010) and Legendre (2014) |
| 5 | One empirical worked example | Transparently limited | Morrison described as one worked case; Nemegt as structural comparator only |
| 6 | Causal overinterpretation | Resolved | "Structural sufficiency is not causal attribution"; no claims about Allosaurus behaviour or falsified mobility |
| 7 | Temporal aggregation operator dependence | Transparently limited | Conclusions restricted to union pooling; finest-resolution imposed-arm values described as combining ecological and structural components |
| 8 | Degenerate factorial cells | Resolved | −0.91 labelled degenerate (text, Fig. 5 legend and panel label); non-additivity evidence is the non-degenerate −0.76 versus summed −0.28 |
| 9 | Insufficient external validation | Transparently limited | Limitations: conclusions for other domains require direct tests |
| 10 | Taxonomic-resolution dependence | Transparently limited | Species-level Morrison step depends on identification completeness (Limitations) |
| 11 | Sampling model simplification | Transparently limited | Small sampling effect restricted to tested parameterisation (Results, Discussion, Table 3) |
| 12 | Repository claims vs actual assets | Resolved | Every path named in the Data Accessibility Statement returns HTTP 200; public registry byte-identical to the reviewer copy; clean public clone reproduces the registry and figures (ECOEVO_DATA_CODE_LINK_AUDIT.md, ECOEVO_CLEAN_CLONE_REPRODUCIBILITY.md) |

Unresolved HOLD items: none.
