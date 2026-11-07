# ECOEVO final handoff — methodological_beta_bias → Ecology and Evolution

Target: Ecology and Evolution (Wiley), Research Article, Wiley transfer from
Journal of Biogeography (no reviewer comments). Title and running title unchanged.

Rebuild:

    cd dinosaur_migration_foodweb && make beta_bias          # ~8–15 min, no network
    cd methodological_beta_bias
    python3 analysis/27_ecoevo_references.py                  # uses cached Crossref JSON
    python3 analysis/26_ecoevo_build.py
    python3 analysis/31_ecoevo_clean_clone_check.py <clone> <make log>
    python3 analysis/30_ecoevo_audits.py <clone>/methodological_beta_bias/results/manuscript_values.csv
    python3 analysis/26_ecoevo_build.py                       # repackage with final audits

Package: `manuscript/ECOEVO/build/submission/ECOEVO_submission_package.zip`.

## Final report (finalization pass)

SCIENTIFIC VALIDITY: PASS
ECOLOGY AND EVOLUTION SCOPE FIT: PASS
NOVELTY CLAIM CALIBRATION: PASS
MORRISON INTERPRETATION: PASS
NEMEGT COMPARATOR WORDING: PASS
FACTORIAL NON-DEGENERATE INTERACTION EVIDENCE: PASS
TEMPORAL AGGREGATION WORDING: PASS
NUMERICAL CONSISTENCY: PASS
REFERENCES: PASS
FIGURE/TABLE ORDER: PASS
DATA ACCESSIBILITY: PASS
PUBLIC REPOSITORY LINKS: PASS
REVIEWER-FILE / PUBLIC-REPOSITORY CONSISTENCY: PASS
OBSOLETE ANONYMITY WORDING REMOVED: PASS
OBSOLETE "NO SUPPORTING INFORMATION" WORDING REMOVED: PASS
SINGLE-AUTHOR LANGUAGE: PASS
COVER LETTER: PASS
CLEAN-CLONE REPRODUCIBILITY: PASS
TRANSFER / DIRECT-SUBMISSION DUAL READINESS: PASS
TITLE-PAGE AUTHOR PLACEHOLDERS: INTENTIONALLY LEFT FOR MANUAL AUTHOR COMPLETION
ANY SCIENTIFIC RESULT CHANGED: NO
ANY NEW ANALYSIS ADDED: NO
FINAL DECISION: SUBMISSION READY

Evidence: ECOEVO_NUMERICAL_AUDIT.md, ECOEVO_REFERENCE_AUDIT.md,
ECOEVO_FIGURE_TABLE_ORDER_AUDIT.md, ECOEVO_DATA_CODE_LINK_AUDIT.md,
ECOEVO_CLEAN_CLONE_REPRODUCIBILITY.md, ECOEVO_HOSTILE_REVIEW.md,
ECOEVO_SUBMISSION_CHECKLIST.md. The builder fails on stale journal,
anonymity or "no Supporting Information" wording, first-person plural,
uncited references and out-of-order display items.

## What changed relative to JBI (no new analyses; no frozen value changed)

- Framing, abstract (unstructured), keywords (6), single-blind statements, new cover letter.
- Wording corrections required by the code/registry: factorial grid {4, 12, 26}; −0.91 is a degenerate cell (whole small guild lumped); sign-proportion statement (83.5% negative at pool 20); finest-resolution temporal contrasts include the structural component; Morrison seed 20260924; 2-D thin-slice −0.046 (not −0.045).
- Registry: all JBI values unchanged; provenance columns corrected; previously hand-appended rows now generated; new rows for every number cited.
- Figures redrawn from frozen tables (Figure 5 unclipped scale and degenerate-cell labels; Figure 6 null intervals as bands).
- Public repository: `make beta_bias` target, README section, scikit-learn in requirements, `parameter_seed_registry.csv`, evidence-audit attribution fix (Foster 2015).
