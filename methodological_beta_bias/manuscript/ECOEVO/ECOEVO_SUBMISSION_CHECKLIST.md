# ECOEVO submission checklist — Ecology and Evolution, Research Article

Guidelines source: E&E Author Guidelines (Wayback snapshot 2024-11-09; live page
blocked to automated access) and Product Information (snapshot 2025-02-14),
archived privately in `wip/journal_guidelines_archive/ecology_and_evolution/`
with a SHA-256 ledger. Re-check the live page in the submission system.

## Journal requirements

| Requirement (E&E) | Status | Where |
|---|---|---|
| Single-blind review | Done: author information is on the title page and in the main document; the repository URL is given directly | main docx, title page |
| Title page: title, author, affiliation, contact details | Title, running title, author done; affiliation, postal address, e-mail and ORCID intentionally left for manual completion by the author (not a HOLD) | title page, main docx |
| Abstract (any format) | Unstructured, 273 words | main docx |
| 4–6 keywords | 6: assemblage structure; beta diversity; community ecology; distance decay; spatial turnover; temporal aggregation | main docx, title page |
| Concise cover letter focused on the question | Author-supplied final text, first person singular; transfer-route and direct-submission versions | ECOEVO_cover_letter.docx; ECOEVO_cover_letter_direct_submission.docx |
| Text: Introduction, Methods, Results, Discussion | Done (about 4,900 words; E&E has no word limit) | main docx |
| Literature cited, consistent style, DOIs | 55 references, Harvard author–year, all DOIs Crossref/DataCite-verified | main docx; ECOEVO_REFERENCE_AUDIT.md |
| Tables on separate pages after the references, cited in order | Tables 1–3 each on a new page after the references; also supplied as editable `tables/ECOEVO_tables.docx` | main docx |
| Figure legends | After the tables | main docx |
| Figures uploaded as separate files (EPS/TIFF preferred, ≥300 dpi) and cited in order | Figure1–6.tif at 300 dpi (LZW), plus PNG copies and an editable pptx; not embedded in the main document | figures/ |
| Data Accessibility Statement (data archived publicly; links active) | Done; all links return HTTP 200 | main docx; ECOEVO_DATA_CODE_LINK_AUDIT.md |
| Competing interests statement | "The author declares no competing interests." | main docx, title page, cover letter |
| Author contributions (CRediT) | Single author, CRediT roles | main docx, title page |
| Acknowledgements incl. funding | Bakker acknowledgement (cautious wording; no review, endorsement, data or analysis implied); "No external funding was received for this work." | main docx, title page |
| Ethics / consent | Not required: public non-human fossil occurrence data and simulated data only; consent not applicable | main docx, title page |
| Supplementary material discouraged | No supplementary or S-numbered items. The three reviewer files are copies of canonical repository files, supplied for convenience only | reviewer_files/ |
| Page and continuous line numbers | Present in the main document | main docx |
| Data and code provided at submission (minimum standards, Jenkins et al. 2023) | Public repository with code, inputs, seeds, registry, Makefile and README | ECOEVO_CLEAN_CLONE_REPRODUCIBILITY.md |

## Route A / Route B readiness

- Route A (Wiley transfer restored): use `ECOEVO_cover_letter.docx`; replace transferred metadata and files as below.
- Route B (direct new submission because the transfer link remains broken): use `ECOEVO_cover_letter_direct_submission.docx`, which adds the sentence about the non-functional transfer link and the Wiley Author Services ticket (e1434765-ba23-499f-8edd-b2092cf12e3c). All other files are identical. Do not use this letter if the transfer succeeds.
- Global Ecology and Biogeography is not mentioned in either letter (disclose only if the submission system asks).

## Transfer metadata (Route A: Wiley transfer from Journal of Biogeography)

Check every field the system carries over from the JBI submission and replace it:

| Field | Value to use |
|---|---|
| Article type | Research Article |
| Title | Assemblage structure distorts beta diversity and distance decay |
| Running title | Bias in spatial turnover inference |
| Abstract | From ECOEVO_main_manuscript.docx (unstructured; replace the JBI structured abstract) |
| Keywords | The 6 above (replace the JBI list, which contained "biogeography") |
| Author / corresponding author | Tatsuki Onishi; enter affiliation, address, e-mail and ORCID |
| Funding | No external funding |
| Conflicts | None |
| Data availability | Paste the Data Accessibility Statement from the main document (the JBI version deferred the URL to the title page for double-anonymous review; do not reuse it) |
| Ethics | Not applicable (public non-human fossil occurrence data and simulations) |
| Files | Delete all transferred JBI files (blinded main, JBI title page, JBI cover letter, JBI figures). Upload: main document, title page, cover letter, Figures 1–6, tables file, and the 3 reviewer files. Do not upload a response to reviewers (none were received). |

## Package contents (`ECOEVO_submission_package.zip`)

- ECOEVO_main_manuscript.docx (submission main document)
- ECOEVO_main_manuscript_inline.docx (reading copy with figures and tables inline)
- ECOEVO_title_page.docx, ECOEVO_cover_letter.docx
- tables/ECOEVO_tables.docx
- figures/Figure1–6.tif and .png; figures/ECOEVO_figures_editable.pptx
- reviewer_files/ (sources.csv, manuscript_values.csv, INDEPENDENT_EVIDENCE_AUDIT.md)
- audits/ (this checklist and the ECOEVO_* audit reports)

## Author actions before submitting

1. Enter affiliation, full postal address, e-mail and ORCID manually (title page and main-document title block; intentionally not completed by the build).
2. Ecology and Evolution is fully open access: an article publication charge applies on acceptance (check the current amount and any institutional or waiver arrangements in the Wiley system).
3. Replace all transferred JBI files and metadata (table above).
