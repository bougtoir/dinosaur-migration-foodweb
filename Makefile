PY ?= python3

.PHONY: all data stage1 beta_bias figures clean

data:
	$(PY) src/download/fetch_data.py

stage1:
	$(PY) analysis/01_data_audit.py
	$(PY) analysis/02_occurrence_cleaning.py
	$(PY) analysis/03_taxonomy.py
	$(PY) analysis/04_spatial_occupancy.py
	$(PY) analysis/05_beta_diversity.py
	$(PY) analysis/06_sampling_bias.py

# Methodological beta-bias study (simulations, Morrison decomposition,
# Nemegt comparator, value registry, figures). Requires stage1 outputs.
MBB = methodological_beta_bias/analysis
beta_bias: stage1
	$(PY) analysis/07_exploratory_reverse_signal.py
	$(PY) analysis/10_nemegt_prep.py
	$(PY) analysis/11_nemegt_validation.py
	$(PY) allosaurus_spatial_ecology/analysis/01_allosaurus_mechanisms.py
	$(PY) $(MBB)/01_gamma_diversity_bias.py
	$(PY) $(MBB)/02_dominance_bias.py
	$(PY) $(MBB)/03_taxonomic_lumping.py
	$(PY) $(MBB)/04_temporal_averaging.py
	$(PY) $(MBB)/05_sampling_bias.py
	$(PY) $(MBB)/06_combined_factorial_simulation.py
	$(PY) $(MBB)/07_morrison_empirical_decomposition.py
	$(PY) $(MBB)/08_optional_external_validation.py
	$(PY) $(MBB)/12_presence_model_robustness.py
	$(PY) $(MBB)/13_2d_robustness.py
	$(PY) $(MBB)/21_temporal_false_negative.py
	$(PY) $(MBB)/22_false_contrast_threshold.py
	$(PY) $(MBB)/11_manuscript_values.py
	$(PY) $(MBB)/29_parameter_seed_registry.py
	$(PY) $(MBB)/28_ecoevo_figures.py

all: stage1

clean:
	rm -f results/tables/*.csv results/diagnostics/*.txt
	rm -f figures/main/*.png figures/extended_data/*.png
