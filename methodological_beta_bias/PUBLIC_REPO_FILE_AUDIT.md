# Public repository file audit — JBI submission

Repository: https://github.com/bougtoir/dinosaur-migration-foodweb
Audited: 2026-10-23 (UTC). All three review supplementary files verified
present, publicly accessible (HTTP 200 on raw.githubusercontent.com,
no login), and byte-identical (sha256) to the submitted review copies.
No conflicting duplicate versions exist in the repository.

| filename | repository_path | public_url | accessible_yes_no | content_matches_submission_yes_no | action_required |
|---|---|---|---|---|---|
| INDEPENDENT_EVIDENCE_AUDIT.md | methodological_beta_bias/INDEPENDENT_EVIDENCE_AUDIT.md | https://github.com/bougtoir/dinosaur-migration-foodweb/blob/main/methodological_beta_bias/INDEPENDENT_EVIDENCE_AUDIT.md | yes | yes | none |
| manuscript_values.csv | methodological_beta_bias/results/manuscript_values.csv | https://github.com/bougtoir/dinosaur-migration-foodweb/blob/main/methodological_beta_bias/results/manuscript_values.csv | yes | yes | none |
| sources.csv | metadata/sources.csv | https://github.com/bougtoir/dinosaur-migration-foodweb/blob/main/metadata/sources.csv | yes | yes | none |

## Reproducibility assets verified present

- simulation/analysis code: analysis/*.py,
  methodological_beta_bias/analysis/*.py (incl. sim_core.py, 25_jbi_build.py)
- frozen seeds: seed sets 20260920–20260925 recorded in
  manuscript_values.csv and the Data Accessibility Statement
- parameter registry: methodological_beta_bias/results/manuscript_values.csv
  (maps every manuscript number to its generating script and output file)
- processed inputs: data/processed/, data/raw/maidment2024_dryad/
- provenance/checksum records: metadata/sources.csv
- instructions/README: README.md, DATA_SOURCES.md
- reproduction entry point: Makefile

## Statement policy (double-anonymous route)

- Identified title page carries the full Data Accessibility Statement
  with active direct links (Dryad DOI, PBDB, GitHub repository).
- Blinded main text defers the repository URL to the title page; it
  contains no identifying URL and no "anonymized repository" claim.
