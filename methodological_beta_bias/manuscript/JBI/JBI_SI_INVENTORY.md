# JBI Supporting Information inventory and disposition

Every former SI item classified A (must move) / B (should move) /
C (can remain) / D (redundant-delete). Final disposition chosen:
integrate essential items into the main manuscript; move low-level
reproducibility material to the public repository; eliminate the journal
SI entirely (Option A).

| Item | Cited in main? / where | Role | Required for main claim? | Required for reproduction? | Action | Rationale |
|---|---|---|---|---|---|---|
| Table S1 parameter+seed registry | yes, Methods | reproducibility | no | yes | DELETE→repo | low-level registry; belongs to repository |
| Table S2 full sweep outputs | yes, Methods | exhaustive outputs | no | yes | DELETE→repo | CSVs already in repo (`results/tables/`) |
| Table S3 sampling sweep | yes, Results 2 + workflow table | robustness of sampling result | yes (supports "small bias" claim) | yes | MAIN → Table 2 | affects interpretation of a headline robustness result |
| Table S4 presence-model details | yes, Methods | exploratory model diagnostics | no (exploratory, already summarised) | yes | DELETE→repo | low-level diagnostics; main text keeps convergence caveat |
| Table S5 taxonomic mapping | yes, Methods | guild assignment data | no | yes | DELETE→repo | full reconciliation table is repository data |
| Table S6 Nemegt extended diagnostics | yes, Methods/Results 6 | extended comparator | no | yes | DELETE→repo | extended Tarbosaurus diagnostics are secondary |
| Table S7 threshold sensitivity | yes, Results 1 | justifies |Δβ|>0.1 threshold | yes | MAIN → Table 1 | required to evaluate the operational threshold |
| Table S8 sim21 scenario outputs | yes, Methods | supports "four-fold" claim | key values already in text | yes | values in main; full table → repo | headline values integrated; full grid is repo material |
| Table S9 2-D robustness details | yes, Methods | parameter grid detail | no | yes | DELETE→repo | 2-D results stay in main text/Fig. 3 |
| Table S10 species-resolution detail | yes, Methods | sensitivity detail | no | yes | DELETE→repo | main keeps the −0.322 attenuation value |
| Figure S1 sampling curve | yes, Results 2 | secondary visual | no | no | DELETE (content → Table 2) | same data now shown as main table |
| Figure S2 temporal curves (alt bins) | yes, Results 2 | redundant sensitivity | no | no | DELETE→repo | Fig. 4b already shows the scenarios |
| Figure S3 Morrison locality map | yes, Methods | context map | no | yes | DELETE→repo | helpful but not interpretive |
| Figure S4 presence-model robustness | yes, Methods | exploratory diagnostics | no | no | DELETE→repo | follows Table S4 |
| Figure S5 Nemegt extended diagnostics | yes, Methods/Results 6 | extended comparator | no | no | DELETE→repo | follows Table S6 |
| Text S1 independent evidence audit | yes, Methods/Results 7 | evidence context | key conclusion in main | yes | conclusion in main; full matrix → repo | already a repo file (INDEPENDENT_EVIDENCE_AUDIT.md) |
| Text S2 code provenance | yes, Methods | provenance/checksums | no | yes | DELETE→repo | metadata/sources.csv already in repo |
| Text S3 temporal-pooling mechanism | yes, Discussion | mechanism explanation | yes | no | MAIN (mechanism sentence inlined in Discussion) | one-sentence mechanism now in main text |
