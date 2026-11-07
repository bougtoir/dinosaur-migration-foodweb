"""Build results/manuscript_values.csv — every numeric value cited in the
manuscript, traced to its source script and output file."""
from __future__ import annotations

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"

ROWS = []


def add(vid, val, lo=None, hi=None, seed="", script="", out="", fig="",
        loc="", unit=None):
    if unit is None:
        unit = ("Δβ (mean-pairwise Jaccard)" if vid.startswith(("sim", "emp_db", "nem"))
                and "r2" not in vid.lower() and "falsecontrast" not in vid
                else "z-score" if "_z" in vid
                else "pseudo-R2" if "r2" in vid.lower()
                else "proportion" if "falsecontrast" in vid or "difference" in vid
                else "")
    ROWS.append(dict(value_id=vid, value=val, CI_lower=lo, CI_upper=hi,
                     unit=unit, simulation_seed_set=seed,
                     source_script=script, source_output=out, figure_panel=fig,
                     manuscript_location=loc))


def main() -> None:
    s1 = pd.read_csv(T / "sim01_gamma_bias.csv")
    r = s1[s1.n_pred_taxa == 2].iloc[0]
    add("sim01_bias_p2", r.bias_mean, r.lo95, r.hi95, "20260922",
        "01_gamma_diversity_bias.py", "sim01_gamma_bias.csv",
        "Fig.2a", "Results 1")
    r = s1[s1.n_pred_taxa == 4].iloc[0]
    add("sim01_bias_p4", r.bias_mean, r.lo95, r.hi95, "20260922",
        "01_gamma_diversity_bias.py", "sim01_gamma_bias.csv",
        "Fig.2a", "Results 1")
    add("sim01_falsecontrast_p4", r["prop_abs_gt_0.1"], seed="20260922",
        script="01_gamma_diversity_bias.py", out="sim01_gamma_bias.csv",
        fig="Fig.2a", loc="Results 1")
    r = s1[s1.n_pred_taxa == 26].iloc[0]
    add("sim01_bias_p26", r.bias_mean, r.lo95, r.hi95, "20260922",
        "01_gamma_diversity_bias.py", "sim01_gamma_bias.csv",
        "Fig.2a", "Results 1")

    s2 = pd.read_csv(T / "sim02_dominance_bias.csv")
    for p, vid in ((0.5, "sim02_bias_pD0.5_allolike"), (0.9, "sim02_bias_pD0.9")):
        r = s2[s2.p_dominant == p].iloc[0]
        add(vid, r.delta_beta_obs_mean, r.lo95, r.hi95, "20260922",
            "02_dominance_bias.py", "sim02_dominance_bias.csv",
            "Fig.2b", "Results 2")

    s3 = pd.read_csv(T / "sim03_taxonomic_lumping.csv")
    r = s3.iloc[-1]
    add("sim03_B_lumping_k6", r.B_lumping_mean, seed="20260922",
        script="03_taxonomic_lumping.py", out="sim03_taxonomic_lumping.csv",
        fig="Fig.4a", loc="Results 2")
    add("sim03_shift_genus_minus_species_k6", r.shift_genus_minus_species,
        seed="20260922", script="03_taxonomic_lumping.py",
        out="sim03_taxonomic_lumping.csv", fig="Fig.4a", loc="Results 2")

    s4 = pd.read_csv(T / "sim04_temporal_averaging.csv")
    for w, vid in ((1, "sim04_db_width1"), (8, "sim04_db_width8")):
        r = s4[s4.bin_width_slices == w].iloc[0]
        add(vid, r.delta_beta_obs_mean, r.lo95, r.hi95, "20260922",
            "04_temporal_averaging.py", "sim04_temporal_averaging.csv",
            "Fig.4b", "Results 2")

    s5 = pd.read_csv(T / "sim05_sampling_bias.csv")
    add("sim05_bias_range_min", s5.delta_beta_obs_mean.min(),
        s5.lo95.min(), s5.hi95.min(), "20260922", "05_sampling_bias.py",
        "sim05_sampling_bias.csv", "Table 2", "Results 2")
    add("sim05_bias_range_max", s5.delta_beta_obs_mean.max(),
        seed="20260922", script="05_sampling_bias.py",
        out="sim05_sampling_bias.csv", fig="Table 2", loc="Results 2")

    s6 = pd.read_csv(T / "sim06_factorial.csv")
    r = s6.loc[s6.bias.abs().idxmax()]
    add("sim06_max_abs_bias", r.bias, seed="20260923",
        script="06_combined_factorial_simulation.py",
        out="sim06_factorial.csv", fig="Fig.5",
        loc=f"Results 3 (cell n_pred={int(r.n_pred_taxa)}, p_D={r.p_dominant}, k={int(r.n_lumped)})")
    add("sim06_false_difference_max", s6.prop_false_difference.max(),
        seed="20260923", script="06_combined_factorial_simulation.py",
        out="sim06_factorial.csv", fig="Fig.5", loc="Results 3")

    # factorial: degenerate cells (k >= n_pred collapses the whole small
    # guild into one column, so its turnover is zero by construction)
    nd = s6[s6.n_lumped < s6.n_pred_taxa]
    r = nd.loc[nd.bias.abs().idxmax()]
    add("sim06_max_abs_bias_nondegenerate", r.bias, seed="20260923",
        script="06_combined_factorial_simulation.py",
        out="sim06_factorial.csv", fig="Fig.5",
        loc=f"Results 3 (cell n_pred={int(r.n_pred_taxa)}, p_D={r.p_dominant}, k={int(r.n_lumped)})")

    def b6(n, pd_, k):
        return s6[(s6.n_pred_taxa == n) & (s6.p_dominant == pd_)
                  & (s6.n_lumped == k)].bias.iloc[0]
    add("sim06_bias_p4_pd0.9_k3", b6(4, 0.9, 3), seed="20260923",
        script="06_combined_factorial_simulation.py",
        out="sim06_factorial.csv", fig="Fig.5", loc="Results 3")
    add("sim06_additive_p4_pd0.9_k3",
        b6(4, 0.0, 1) + (b6(26, 0.9, 1) - b6(26, 0.0, 1))
        + (b6(26, 0.0, 3) - b6(26, 0.0, 1)), seed="20260923",
        script="06_combined_factorial_simulation.py (sum of one-factor "
        "effects read from the grid)", out="sim06_factorial.csv",
        fig="Fig.5", loc="Results 3")

    dec = pd.read_csv(T / "morrison_decomposition.csv")
    lbl = dict(zip(dec.step, dec.label))
    d = dict(zip(dec.step, dec.delta_beta))
    lo = dict(zip(dec.step, dec.lo95)); hi = dict(zip(dec.step, dec.hi95))
    M07 = "07_morrison_empirical_decomposition.py"
    add("emp_db_naive", d[1], lo[1], hi[1], "20260924", M07,
        "morrison_decomposition.csv", "Fig.6", "Results 4")
    add("emp_gamma_null_interval", None, lo[2], hi[2], "20260924", M07,
        "morrison_decomposition.csv", "Fig.6", "Results 5")
    add("emp_freq_null_interval", None, lo[3], hi[3], "20260924", M07,
        "morrison_decomposition.csv", "Fig.6", "Results 5")
    add("emp_db_minus_allosaurus", d[4], lo[4], hi[4], "20260924", M07,
        "morrison_decomposition.csv", "Fig.6", "Results 5")
    add("emp_db_species", d[5], lo[5], hi[5], "20260924", M07,
        "morrison_decomposition.csv", "Fig.6", "Results 5")
    add("emp_allo_extent_z", d[6], seed="", script="01_allosaurus_mechanisms.py",
        out="morrison_decomposition.csv", fig="Fig.6", loc="Results 5")
    add("emp_presence_pseudoR2", d[7], seed="",
        script="01_allosaurus_mechanisms.py", out="morrison_decomposition.csv",
        fig="", loc="Results 5 (exploratory)")

    rob = pd.read_csv(T / "presence_model_robustness.csv")
    r = rob[rob.penalty_C == 1.0].iloc[0]
    add("emp_presence_pseudoR2_penalized", r.pseudo_r2_penalized,
        seed="", script="12_presence_model_robustness.py",
        out="presence_model_robustness.csv", fig="",
        loc="Results 5 (exploratory robustness)")

    s13g = pd.read_csv(T / "sim13_2d_gamma.csv")
    for np_, vid in ((4, "sim13_2d_bias_p4"), (2, "sim13_2d_bias_p2")):
        r = s13g[s13g.n_pred_taxa == np_].iloc[0]
        add(vid, r.delta_beta_mean, r.lo95, r.hi95, "20260924",
            "13_2d_robustness.py", "sim13_2d_gamma.csv", "Fig.3a",
            "Results 1 (2-D robustness)")
    r = s13g[s13g.n_pred_taxa == 4].iloc[0]
    add("sim13_2d_decayslope_diff_p4", r.decay_slope_diff, seed="20260924",
        script="13_2d_robustness.py", out="sim13_2d_gamma.csv",
        fig="Fig.3b", loc="Results 1")
    s13t = pd.read_csv(T / "sim13_2d_temporal.csv")
    add("sim13_2d_temporal_attenuation",
        s13t.iloc[-1].delta_beta_mean - s13t.iloc[0].delta_beta_mean,
        seed="20260924", script="13_2d_robustness.py",
        out="sim13_2d_temporal.csv", fig="Fig.4b", loc="Results 2")

    nem = pd.read_csv(T / "nemegt_comparator_decomposition.csv")
    nci = pd.read_csv(T.parents[2] / "results" / "tables"
                      / "nemegt_delta_beta.csv").iloc[0]
    add("nem_db_full", nem.iloc[0].delta_beta,
        round(float(nci.delta_beta_full_lo95), 3),
        round(float(nci.delta_beta_full_hi95), 3), "20260920",
        "11_nemegt_validation.py (CI); 08_optional_external_validation.py",
        "nemegt_comparator_decomposition.csv; nemegt_delta_beta.csv",
        "Fig.6 inset", "Results 6")

    # rows previously appended outside this script (values rounded to 4 dp
    # exactly as first registered)
    s21 = pd.read_csv(T / "sim21_temporal_attenuation.csv")
    for sc in ("weak", "moderate", "strong"):
        g = s21[s21.scenario == sc]
        for tag, nb in (("thin", 8), ("pooled", 1)):
            r = g[g.temporal_bins == nb].iloc[0]
            add(f"sim21_{sc}_{tag}", f"{r.delta_beta_mean:.4f}",
                f"{r.lo95:.4f}", f"{r.hi95:.4f}", "20260925",
                "analysis/21_temporal_false_negative.py",
                "results/tables/sim21_temporal_attenuation.csv", "Fig. 4b",
                "Results 2 (temporal); Discussion", unit="Δβ (mean-pairwise Jaccard)")
    fc = pd.read_csv(T / "false_contrast_threshold_sensitivity.csv")
    add("fc_thr_pool2_all", float(fc[fc.n_pred_taxa == 2].false_contrast_rate.min()),
        seed="20260922", script="analysis/22_false_contrast_threshold.py",
        out="results/tables/false_contrast_threshold_sensitivity.csv",
        fig="Table 1", loc="Results 1", unit="proportion")
    r = fc[(fc.n_pred_taxa == 4) & (fc.threshold == 0.20)].iloc[0]
    add("fc_thr_pool4_0.20", float(r.false_contrast_rate), seed="20260922",
        script="analysis/22_false_contrast_threshold.py",
        out="results/tables/false_contrast_threshold_sensitivity.csv",
        fig="Table 1", loc="Results 1", unit="proportion")

    # ---- additional manuscript numbers (ECOEVO registry extension) ----
    for _, r in fc.iterrows():
        add(f"fc_rate_pool{int(r.n_pred_taxa)}_thr{r.threshold:.2f}",
            float(r.false_contrast_rate), seed="20260922",
            script="22_false_contrast_threshold.py",
            out="false_contrast_threshold_sensitivity.csv", fig="Table 1",
            loc="Results 1; Table 1", unit="proportion")
    for npool in (12, 16, 20):
        r = s1[s1.n_pred_taxa == npool].iloc[0]
        add(f"sim01_propneg_p{npool}", float(r.prop_negative), seed="20260922",
            script="01_gamma_diversity_bias.py", out="sim01_gamma_bias.csv",
            fig="Fig.2a", loc="Results 1", unit="proportion")
    r = s3.iloc[-1]
    add("sim03_db_species_k6", r.delta_beta_species, seed="20260922",
        script="03_taxonomic_lumping.py", out="sim03_taxonomic_lumping.csv",
        fig="Fig.4a", loc="Results 2")
    add("sim03_db_genus_k6", r.delta_beta_genus, seed="20260922",
        script="03_taxonomic_lumping.py", out="sim03_taxonomic_lumping.csv",
        fig="Fig.4a", loc="Results 2")
    for _, r in s5.iterrows():
        add(f"sim05_db_mult{int(r.pred_sampling_ratio_A_vs_B)}",
            r.delta_beta_obs_mean, r.lo95, r.hi95, "20260922",
            "05_sampling_bias.py", "sim05_sampling_bias.csv", "Table 2",
            "Results 2; Table 2")
    r = s13g[s13g.n_pred_taxa == 4].iloc[0]
    add("sim13_2d_decayslope_small_p4", r.decay_slope_pred, seed="20260924",
        script="13_2d_robustness.py", out="sim13_2d_gamma.csv", fig="Fig.3b",
        loc="Abstract; Results 1; Discussion", unit="Jaccard per lattice unit")
    add("sim13_2d_decayslope_comparison_p4", r.decay_slope_herb,
        seed="20260924", script="13_2d_robustness.py",
        out="sim13_2d_gamma.csv", fig="Fig.3b",
        loc="Abstract; Results 1; Discussion", unit="Jaccard per lattice unit")
    add("sim13_2d_temporal_thin", s13t.iloc[0].delta_beta_mean,
        seed="20260924", script="13_2d_robustness.py",
        out="sim13_2d_temporal.csv", fig="Fig.4b", loc="Discussion")
    add("sim13_2d_temporal_pooled", s13t.iloc[-1].delta_beta_mean,
        seed="20260924", script="13_2d_robustness.py",
        out="sim13_2d_temporal.csv", fig="Fig.4b", loc="Discussion")
    for sc in ("weak", "moderate", "strong"):
        r = s21[(s21.scenario == sc) & (s21.temporal_bins == 1)].iloc[0]
        add(f"sim21_{sc}_attenuation_fraction", r.attenuation_fraction,
            seed="20260925", script="21_temporal_false_negative.py",
            out="sim21_temporal_attenuation.csv", fig="Fig.4b",
            loc="Results 2", unit="fraction")
        add(f"sim21_{sc}_fold", r.abs_vs_thin_fraction, seed="20260925",
            script="21_temporal_false_negative.py",
            out="sim21_temporal_attenuation.csv", fig="Fig.4b",
            loc="Abstract; Results 2; Discussion", unit="ratio")

    ALLO = T.parents[2] / "allosaurus_spatial_ecology" / "results" / "tables"
    at = pd.read_csv(ALLO / "allo_duration_model_taxa.csv")
    a = at[at.taxon == "Allosaurus"].iloc[0]
    add("emp_allo_extent_resid_km", a.extent_resid, script="01_allosaurus_mechanisms.py",
        out="allo_duration_model_taxa.csv", fig="Fig.6", loc="Results 5",
        unit="km")
    add("emp_allo_occupancy", a.occupancy, script="01_allosaurus_mechanisms.py",
        out="allo_duration_model_taxa.csv", fig="Fig.2b", loc="Results 2",
        unit="proportion of collections")
    lg = pd.read_csv(ALLO / "allo_presence_logit.csv")
    st = lg[lg.term.str.startswith("state_")].coef
    add("emp_presence_state_coef_min", st.min(), script="01_allosaurus_mechanisms.py",
        out="allo_presence_logit.csv", loc="Results 5 (exploratory)", unit="logit coefficient")
    add("emp_presence_state_coef_max", st.max(), script="01_allosaurus_mechanisms.py",
        out="allo_presence_logit.csv", loc="Results 5 (exploratory)", unit="logit coefficient")

    PROC = T.parents[2] / "data" / "processed"
    occ = pd.read_csv(PROC / "occurrences_clean.csv")
    add("emp_n_occurrences", len(occ), script="analysis/02_occurrence_cleaning.py",
        out="data/processed/occurrences_clean.csv", loc="Methods", unit="count")
    add("emp_n_collections", occ.collection_no.nunique(),
        script="analysis/02_occurrence_cleaning.py",
        out="data/processed/occurrences_clean.csv", loc="Methods", unit="count")
    add("emp_n_genera", occ.taxon.nunique(), script="analysis/02_occurrence_cleaning.py",
        out="data/processed/occurrences_clean.csv", loc="Methods", unit="count")
    for g in ("herbivore", "predator"):
        add(f"emp_n_genera_{g}", occ[occ.guild == g].taxon.nunique(),
            script="analysis/02_occurrence_cleaning.py",
            out="data/processed/occurrences_clean.csv", loc="Methods", unit="count")
    no = pd.read_csv(PROC / "nemegt_occurrences.csv")
    add("nem_n_occurrences", len(no), script="analysis/10_nemegt_prep.py",
        out="data/processed/nemegt_occurrences.csv", loc="Methods", unit="count")
    add("nem_n_collections", no.collection_no.nunique(), script="analysis/10_nemegt_prep.py",
        out="data/processed/nemegt_occurrences.csv", loc="Methods", unit="count")
    m = no.body_fossil.fillna(False).astype(bool) & ~no.is_ootaxon.fillna(False).astype(bool)
    sub = no[m & no.genus.notna()]
    add("nem_sub_n_collections", sub.collection_no.nunique(),
        script="analysis/11_nemegt_validation.py",
        out="data/processed/nemegt_occurrences.csv", loc="Methods", unit="count")
    for g in ("predator", "herbivore"):
        x = sub[sub.guild == g]
        add(f"nem_sub_n_occ_{g}", len(x), script="analysis/11_nemegt_validation.py",
            out="data/processed/nemegt_occurrences.csv", loc="Methods", unit="count")
        add(f"nem_sub_n_genera_{g}", x.genus.nunique(),
            script="analysis/11_nemegt_validation.py",
            out="data/processed/nemegt_occurrences.csv", loc="Methods", unit="count")

    out = pd.DataFrame(ROWS)
    out.to_csv(T.parent / "manuscript_values.csv", index=False)
    print(out[["value_id", "value"]].to_string(index=False))


if __name__ == "__main__":
    main()
