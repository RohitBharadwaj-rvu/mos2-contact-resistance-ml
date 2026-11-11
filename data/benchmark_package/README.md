# MoS2 Contact Resistance & Schottky Barrier Height Benchmark Dataset

## FAIR-Compliant 2D Semiconductor Electronics Benchmark

- **Findable:** Published openly with standard JSON metadata, DOI citations, and Kaggle integration.
- **Accessible:** Plain-text CSV and JSON formats with no proprietary binary dependencies.
- **Interoperable:** Standardized SI/engineering units and full ontology mapping in `data_dictionary.json`.
- **Reusable:** Licensed under Creative Commons Attribution 4.0 International (CC-BY-4.0).

### Key Target Variables
- `log10_contact_resistance_ohm_um`: Base-10 logarithm of width-normalized contact resistance (ML regression target).
- `physics_predicted_sbh_ev`: Effective Schottky barrier height (eV).
- `gate_carrier_density_cm2`: Gate-induced sheet carrier density beneath the contact pad (cm^-2).

### Benchmark Baseline Performance (Grouped 5-Fold CV)
- **Best Machine Learning Model:** Tuned Ridge Regression (RMSE = 0.226 dex, Spearman rho = 0.949, Score = 0.872)
- **Discovered Closed-Form Law:** $R_c \approx 4570 \cdot 10^{\Phi_B - (n_{2D}/10^{13})}\,\Omega\cdot\mu\mathrm{m}$ (RMSE = 0.386 dex)