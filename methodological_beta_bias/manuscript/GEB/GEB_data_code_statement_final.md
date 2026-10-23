# Data and code availability

All occurrence data derive from published public sources: the
Maidment et al. (2024) Dryad package (DOI 10.5061/dryad.6m905qg77,
CC0) and the Paleobiology Database (public API; download parameters
and sha256 checksums recorded in `metadata/sources.csv`). All analysis
and simulation code, frozen random seeds and the value registry
(`results/manuscript_values.csv`) are available in a public repository
[repo URL — to be anonymized for double-anonymous review if required
by GEB, then restored]. The full pipeline reproduces with the Makefile
entry points documented in README.


Exact code version: commit 4794c1ef (branch devin/1790067066-geb-submission,
repository bougtoir/wip; a public/anonymized mirror will be provided at
submission as required). Frozen seed sets: 20260920–20260925 across
simulation arms; sim21 seed 20260925; sim22 seed 20260922 (recorded
per-script and in results/manuscript_values.csv). Reproducibility entry
point: Makefile in dinosaur_migration_foodweb/methodological_beta_bias/.
