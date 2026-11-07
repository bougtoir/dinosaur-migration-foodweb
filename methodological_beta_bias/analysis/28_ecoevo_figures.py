"""Ecology and Evolution figure set (Figures 1-6) redrawn from the frozen
results tables. No simulation or estimate is recomputed here; the script
only changes layout and notation (consistent mathtext symbols, no stale
panel numbering, unclipped colour scale, null intervals drawn as bands).

Outputs: figures/ecoevo/Figure{1..6}.png (300 dpi) and .tif (300 dpi, LZW).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT.parent
T = ROOT / "results" / "tables"
F = ROOT / "figures" / "ecoevo"
F.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "mathtext.default": "regular", "pdf.fonttype": 42})
DOBS = r"$\Delta\beta_{\mathrm{obs}}$"
DTRUE = r"$\Delta\beta_{\mathrm{true}}$"


def save(fig, n):
    png = F / f"Figure{n}.png"
    fig.savefig(png, dpi=300)
    plt.close(fig)
    Image.open(png).convert("RGB").save(F / f"Figure{n}.tif",
                                        compression="tiff_lzw", dpi=(300, 300))


def box(ax, x, y, w, h, text, fc, ec, fs=9):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.01", fc=fc, ec=ec, lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


def arrow(ax, x0, y0, x1, y1, c="k"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2))


# ---- Figure 1: conceptual framework ----
fig, ax = plt.subplots(figsize=(8.5, 3.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
box(ax, 0.11, 0.55, 0.19, 0.20,
    "Generative\ncontrast\n" + r"$\Delta\beta_{\mathrm{eco}}$", "#dbeafe", "#1e40af", 10)
ax.add_patch(plt.Rectangle((0.24, 0.30), 0.53, 0.50, fc="#f3f4f6",
                           ec="#6b7280", ls="--"))
ax.text(0.505, 0.74, "Assemblage structure (non-independent, interacting)",
        ha="center", fontsize=9, color="#374151")
steps = ["Regional\npool size", "Dominance", "Taxonomic\naggregation",
         "Temporal\naggregation", "Sampling\nasymmetry"]
for x, s in zip(np.linspace(0.295, 0.715, 5), steps):
    box(ax, x, 0.52, 0.090, 0.20, s, "#fef3c7", "#b45309", 7)
box(ax, 0.89, 0.55, 0.17, 0.20, "Observed\ncontrast\n" + DOBS,
    "#fee2e2", "#b91c1c", 10)
arrow(ax, 0.205, 0.55, 0.24, 0.55)
arrow(ax, 0.77, 0.55, 0.805, 0.55, "#b91c1c")
ax.text(0.5, 0.17,
        "False differentiation: " + DTRUE + r" = 0 but " + DOBS + r" $\neq$ 0;   "
        "lost or exaggerated differentiation: " + DTRUE + r" $\neq$ 0 but "
        + DOBS + r" $\neq$ " + DTRUE, ha="center", fontsize=8.5)
ax.text(0.5, 0.06, DOBS + r" $\neq$ " + r"$\Delta\beta_{\mathrm{eco}}$"
        " whenever the compared assemblages differ in structure",
        ha="center", fontsize=8.5)
fig.tight_layout()
save(fig, 1)

# ---- Figure 2: pool size + dominance ----
g = pd.read_csv(T / "sim01_gamma_bias.csv")
d = pd.read_csv(T / "sim02_dominance_bias.csv")
fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
ax[0].errorbar(g.n_pred_taxa, g.delta_beta_obs_mean,
               yerr=[g.delta_beta_obs_mean - g.lo95, g.hi95 - g.delta_beta_obs_mean],
               marker="o", capsize=3, color="#1f77b4")
ax[0].axhline(0, color="k", lw=0.8, ls=":")
ax[0].axvspan(3, 5, alpha=0.15, color="green")
v4 = g.loc[g.n_pred_taxa == 4, "delta_beta_obs_mean"].iloc[0]
v2 = g.loc[g.n_pred_taxa == 2, "delta_beta_obs_mean"].iloc[0]
ax[0].annotate("pool 4 (representative)", xy=(4, v4), fontsize=8,
               xytext=(8, -0.28), arrowprops=dict(arrowstyle="->"))
ax[0].annotate("pool 2 (extreme)", xy=(2, v2), fontsize=8,
               xytext=(6, -0.40), arrowprops=dict(arrowstyle="->"))
ax[0].set_xlabel("Small-guild regional pool size (comparison guild = 26 taxa)")
ax[0].set_ylabel(DOBS)
ax[0].set_title("(a) Pool-size imbalance (" + DTRUE + " = 0)")
ax[1].errorbar(d.p_dominant, d.delta_beta_obs_mean,
               yerr=[d.delta_beta_obs_mean - d.lo95, d.hi95 - d.delta_beta_obs_mean],
               marker="s", capsize=3, color="#b45309")
ax[1].axhline(0, color="k", lw=0.8, ls=":")
allo = pd.read_csv(PROJ / "allosaurus_spatial_ecology" / "results" / "tables"
                   / "allo_duration_model_taxa.csv")
occ_allo = float(allo.loc[allo.taxon == "Allosaurus", "occupancy"].iloc[0])
ax[1].axvline(occ_allo, color="#7c3aed", ls="--", lw=1)
ax[1].text(occ_allo + 0.02, ax[1].get_ylim()[0] + 0.01,
           "Morrison dominant\npredator occupancy", fontsize=7, color="#7c3aed")
ax[1].set_xlabel(r"Dominant-taxon prevalence $p_D$")
ax[1].set_ylabel(DOBS)
ax[1].set_title("(b) Dominant-taxon effect (" + DTRUE + " = 0)")
fig.tight_layout()
save(fig, 2)

# ---- Figure 3: 2-D replication + distance decay ----
g13 = pd.read_csv(T / "sim13_2d_gamma.csv")
dc = pd.read_csv(T / "sim13_2d_decay_curves.csv")
fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
ax[0].errorbar(g13.n_pred_taxa, g13.delta_beta_mean,
               yerr=[g13.delta_beta_mean - g13.lo95, g13.hi95 - g13.delta_beta_mean],
               marker="o", capsize=3, color="#0369a1")
ax[0].axhline(0, color="k", lw=0.8, ls=":")
ax[0].set_xlabel("Small-guild pool size (2-D lattice)")
ax[0].set_ylabel(DOBS)
ax[0].set_title("(a) 2-D replication of pool-size bias")
dcc = dc[dc.dist_bin_center <= 30]
ax[1].plot(dcc.dist_bin_center, dcc.dissim_smallpool, "o-",
           label="small pool (4 taxa)", color="#0369a1")
ax[1].plot(dcc.dist_bin_center, dcc.dissim_comparison, "s-",
           label="comparison guild (26 taxa)", color="#b45309")
row4 = g13[g13.n_pred_taxa == 4].iloc[0]
for col, c, s in [("dissim_smallpool", "#0369a1", row4.decay_slope_pred),
                  ("dissim_comparison", "#b45309", row4.decay_slope_herb)]:
    ok = dcc[col].notna()
    b0 = dcc[col][ok].mean() - s * dcc.dist_bin_center[ok].mean()
    ax[1].plot(dcc.dist_bin_center[ok], b0 + s * dcc.dist_bin_center[ok],
               "--", color=c, lw=1)
ax[1].text(1, 1.07, f"fitted slopes: {row4.decay_slope_pred:.3f} vs "
           f"{row4.decay_slope_herb:.3f}", fontsize=8)
ax[1].set_xlim(0, 30); ax[1].set_ylim(0.2, 1.12)
ax[1].set_xlabel("Pairwise distance (lattice units)")
ax[1].set_ylabel("Mean pairwise Jaccard dissimilarity")
ax[1].set_title("(b) Distance-decay distortion (pool 4)")
ax[1].legend(fontsize=8, loc="lower right")
fig.tight_layout()
save(fig, 3)

# ---- Figure 4: taxonomic + temporal aggregation ----
l = pd.read_csv(T / "sim03_taxonomic_lumping.csv")
t = pd.read_csv(T / "sim04_temporal_averaging.csv")
t13 = pd.read_csv(T / "sim13_2d_temporal.csv")
t21 = pd.read_csv(T / "sim21_temporal_attenuation.csv")
fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
ax[0].plot(l.n_lumped_species, l.B_lumping_mean, "o-", color="#15803d")
ax[0].axhline(0, color="k", lw=0.8, ls=":")
ax[0].set_xlabel("Species pooled per genus ($k$)")
ax[0].set_ylabel(r"$B_{\mathrm{lumping}} = \beta_{\mathrm{species}} - \beta_{\mathrm{genus}}$")
ax[0].set_title("(a) Taxonomic aggregation")
ax[1].plot(t.temporal_bins, t.delta_beta_obs_mean, "o-",
           label="structural only (1-D)", color="#0369a1")
ax[1].plot(t13.temporal_bins, t13.delta_beta_mean, "s--",
           label="structural only (2-D)", color="#b45309")
for scen, c in [("weak", "#7c3aed"), ("moderate", "#c026d3"), ("strong", "#db2777")]:
    s = t21[t21.scenario == scen]
    ax[1].plot(s.temporal_bins, s.delta_beta_mean, "v--", color=c,
               label=f"imposed ecological contrast, {scen}")
ax[1].axhline(0, color="k", lw=0.8, ls=":")
ax[1].invert_xaxis()
ax[1].set_xlabel("Temporal bins (8 = finest; 1 = fully pooled)")
ax[1].set_ylabel(DOBS)
ax[1].set_title("(b) Temporal aggregation (source-dependent)")
ax[1].legend(fontsize=7, loc="lower left")
fig.tight_layout()
save(fig, 4)

# ---- Figure 5: factorial bias map ----
s6 = pd.read_csv(T / "sim06_factorial.csv")
vmax = float(np.ceil(s6.bias.abs().max() * 10) / 10)
fig, axes = plt.subplots(1, 3, figsize=(9, 3.3), sharey=True)
for ax, k in zip(axes, sorted(s6.n_lumped.unique())):
    sub = s6[s6.n_lumped == k]
    piv = sub.pivot(index="n_pred_taxa", columns="p_dominant", values="bias")
    im = ax.imshow(piv.values, cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                   origin="lower", aspect="auto")
    ax.set_xticks(range(piv.shape[1]))
    ax.set_xticklabels([f"{c:g}" for c in piv.columns])
    ax.set_yticks(range(piv.shape[0]))
    ax.set_yticklabels([str(i) for i in piv.index])
    ax.set_xlabel(r"Dominant-taxon prevalence $p_D$")
    ax.set_title(f"$k$ = {k} species lumped")
    pfd = sub.pivot(index="n_pred_taxa", columns="p_dominant",
                    values="prop_false_difference")
    for i, npool in enumerate(piv.index):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6.5,
                    color="white" if abs(v) > 0.45 * vmax else "black")
            if pfd.values[i, j] >= 0.95:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                           ec="k", lw=0.8))
        if k >= npool:
            ax.text(piv.shape[1] - 0.5, i + 0.42, "whole guild lumped",
                    ha="right", va="top", fontsize=6, color="white", style="italic")
axes[0].set_ylabel("Small-guild pool size")
fig.subplots_adjust(left=0.07, right=0.88, bottom=0.18, top=0.88, wspace=0.08)
cax = fig.add_axes([0.90, 0.18, 0.015, 0.70])
cb = fig.colorbar(im, cax=cax)
cb.set_label("Bias = " + DOBS + r" $-$ " + DTRUE + " (" + DTRUE + " = 0)")
save(fig, 5)

# ---- Figure 6: Morrison sequential decomposition + Nemegt comparator ----
dec = pd.read_csv(T / "morrison_decomposition.csv").set_index("step")
nci = pd.read_csv(PROJ / "results" / "tables" / "nemegt_delta_beta.csv").iloc[0]
fig, ax = plt.subplots(figsize=(7.5, 3.9))
rows = [("Nemegt comparator (naive)", None),
        ("Morrison: naive genus-level contrast", 1),
        ("Morrison: gamma-matched null interval", 2),
        ("Morrison: frequency-matched null interval", 3),
        ("Morrison: dominant predator excluded", 4),
        ("Morrison: species-level resolution", 5)]
ys = np.arange(len(rows))[::-1]
for (lab, st), y in zip(rows, ys):
    if st is None:
        v, lo, hi = nci.delta_beta_full, nci.delta_beta_full_lo95, nci.delta_beta_full_hi95
        ax.errorbar([v], [y], xerr=[[v - lo], [hi - v]], fmt="s", color="#0369a1",
                    capsize=3)
    elif st in (2, 3):
        r = dec.loc[st]
        ax.fill_betweenx([y - 0.3, y + 0.3], r.lo95, r.hi95,
                         color="#3498db" if st == 2 else "#27ae60", alpha=0.35, lw=0)
        ax.plot([r.delta_beta], [y], marker="o", mfc="white", mec="#b91c1c",
                ls="none")
    else:
        r = dec.loc[st]
        ax.errorbar([r.delta_beta], [y], xerr=[[r.delta_beta - r.lo95],
                    [r.hi95 - r.delta_beta]], fmt="o", color="#b91c1c", capsize=3)
ax.axvline(0, color="k", lw=0.8)
ax.axhline(ys[0] - 0.5, color="#9ca3af", lw=0.6)
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=8)
ax.set_xlabel(r"$\Delta\beta = \beta_P - \beta_H$ (mean pairwise Jaccard)")
fig.tight_layout()
save(fig, 6)
print("wrote", sorted(p.name for p in F.iterdir()))
