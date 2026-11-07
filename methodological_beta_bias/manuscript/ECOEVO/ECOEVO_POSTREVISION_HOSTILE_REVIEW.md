# ECOEVO post-revision hostile review

Package reviewed: build from `analysis/26_ecoevo_build.py` after the finalization pass; registry `results/manuscript_values.csv`; public repository https://github.com/bougtoir/dinosaur-migration-foodweb (clean clone reproduced; see ECOEVO_CLEAN_CLONE_REPRODUCIBILITY.md). Author affiliation/contact placeholders are intentional and not assessed.

## A. Strongest possible rejection argument
The quantitative results come from deliberately simple 1-D/2-D presence–absence simulators with Jaccard dissimilarity only, and the single empirical decomposition (Morrison) cannot establish how often these distortions matter in real ecological comparisons. Classification: B, transparently acknowledged (magnitudes framed as scenario-specific demonstrations of sufficiency; metric, geometry, single-case and external-validity limits stated in Limitations). It is a scope limitation, not an error.

## B. Desk-rejection risk
LOW. The paper fits E&E's stated scope (methodological and conceptually useful work), the contribution is calibrated (component mechanisms explicitly not claimed as new), framing is general-ecological, and data/code are public and reproducible.

## C. Major-revision risk
MODERATE. A reviewer may still request a second metric (e.g. Simpson turnover) or an abundance-based check, or a second empirical system. These requests would extend scope rather than correct an error; the manuscript discloses both.

## D. Scientific claim calibration
No sentence presents pool-size, dominance, lumping, time-averaging or sampling effects as novel (Introduction states "What is missing from the literature is not awareness that these biases exist but their magnitudes under controlled conditions"). Sufficiency is distinguished from calibrated effect size in Abstract, Discussion and Limitations. PASS.

## E. Simulation validity
Geometry, parameterisation, guild construction and occupancy process limit transportability of magnitudes, not the qualitative claims (a structural difference alone suffices to create, erase or reshape a contrast). Pool sizes and thresholds are swept; the 0.1 false-contrast threshold is operational with sensitivity reported (Table 1). Mechanically induced outcomes are explained (e.g. union-pooling saturation; degenerate lumping cells). PASS.

## F. Factorial / non-additivity
−0.91 occurs only in cells where k = 6 lumps the whole four-taxon guild; labelled degenerate in Results, Discussion, Figure 5 legend and panel. Main evidence: combined bias −0.76 versus additive expectation −0.28 (pool 4, p_D = 0.9, k = 3). Repair: the additive expectation is now defined explicitly (pool-only bias plus dominance-only and lumping-only increments from the 26-taxon row), and the text states that this is a descriptive comparison of replicate means with no inferential interaction term; "interaction" wording replaced by "non-additive combined effect" where an inferential reading was possible. PASS.

## G. Distance decay
Methods define the slope as OLS of pairwise Jaccard dissimilarity on Euclidean distance. Repair: Results now state the slope is of Jaccard dissimilarity against distance, with positive values indicating dissimilarity increasing with distance (distance decay of similarity). One 2-D configuration (pool 4) supports a sufficiency claim only; the Discussion explicitly says empirical decay differences are not generally artefacts. PASS.

## H. Temporal aggregation
Text states source-dependent distortion under union pooling only; finest-resolution imposed-arm contrasts are described as combining the imposed ecological difference with the structural pool component. Fold values from the registry: 3.75 and 4.07 (rendered 3.8–4.1); "approximately four-fold" in the cover letter is an acceptable rounded summary. PASS.

## I. Morrison interpretation
Sequence: strong naive pattern → structural diagnostics → attenuation and non-uniqueness → strong biological explanation no longer required. "Structural sufficiency is not causal attribution" appears in Discussion and Limitations; no claims about sedentariness, non-migration or falsified mobility. Gamma-matched null wording: "close to, but marginally more negative than, the lower bound"; frequency-matched null explicitly does not reproduce the signal. Repair: dominant-taxon exclusion and species-level resolution are now introduced as dominance-sensitivity and taxonomic-grain sensitivity diagnostics, not preferred representations. PASS.

## J. Nemegt interpretation
Described only as a structural comparator with reversed pool structure showing that the Morrison direction is not universal; "not a biological replication" stated in Methods, Results and Limitations. PASS.

## K. Metric dependence
Limitations state that Jaccard combines replacement and richness difference, that turnover-only and abundance-based metrics differ in sensitivity and were not evaluated systematically (Baselga 2010; Legendre 2014). Acceptable as a disclosed limitation. PASS.

## L. Reproducibility / data access
All Data Accessibility paths return HTTP 200; public `manuscript_values.csv` is byte-identical to the reviewer copy; `make beta_bias` in a fresh public clone completes and reproduces the registry (non-converged logistic coefficients to ~2e-8, reported to 1 dp) and Figures 1–6. Reviewer files are described as convenience copies of canonical repository files. PASS.

## M. Figures / tables
Figures 1–6 and Tables 1–3 cited in order; Figure 5 full colour range, cell values and outlines (not colour-only), degenerate cells labelled; Figure 6 null bands versus bootstrap error bars, open versus filled symbols; Figure 3 axis labels state dissimilarity and lattice units. Table 1 calls 0.05/0.10/0.20 thresholds; Table 3 now titled "Recommended diagnostic sequence" and explicitly not a validated decision rule. PASS.

## N. References
55 references DOI-verified; coverage enforced both ways. Spot-checks: Kraft et al. 2011 / Chase et al. 2011 (pool dependence), Lennon et al. 2004 / Hillebrand et al. 2008 (commonness/dominance), Bertrand et al. 2006 / Bevilacqua et al. 2009 (taxonomic surrogacy), Olszewski 1999 / Tomašových & Kidwell 2010 (time averaging), Nekola & White 1999 / Soininen et al. 2007 (distance decay), Gotelli & Colwell 2001 / Chao et al. 2014 (sampling), Shaffer et al. 1998 / Pyke & Ehrlich 2010 (collections) support the claims they are attached to. Foster (2015) is cited only as non-diagnostic trackway evidence. Mild stretch noted but acceptable: Badgley (2010) and Alroy (2008) are general palaeo-sampling context citations. PASS.

## O. Cover letter
Both versions: first person singular, contribution stated as quantitative/integrative, no novelty claim for mechanisms, Morrison framed as sufficiency, broad E&E relevance explained, not defensive. Direct-submission version states the broken transfer link factually with ticket e1434765-ba23-499f-8edd-b2092cf12e3c and implies no guarantee of acceptance. PASS.

## P. Repairs made (wording only; regenerated through the builder)
1. Factorial: explicit definition of the additive expectation; statement that no inferential interaction term was estimated; "interaction" → "non-additive combined effect" in Results, Discussion heading/text, Abstract, Table 3.
2. Distance decay: Results specify slope of Jaccard dissimilarity against distance and sign convention.
3. Morrison: dominant-taxon exclusion and species-level resolution framed as sensitivity diagnostics.
4. Workflow: "recommended diagnostic sequence", applied as far as data allow, not a validated decision rule; step 9 no longer categorical; Table 3 title/header updated.

## Q. Remaining non-fatal limitations
Simple simulator geometry; Jaccard only; union pooling only; one empirical worked case; species-level step depends on identification completeness; sampling effect specific to tested parameters; magnitudes not transportable.

## R. Final editor decision
SEND TO REVIEW.

## S. Final reviewer recommendation
MINOR REVISION — strongest remaining concern: generality beyond Jaccard and beyond one empirical system (disclosed).
