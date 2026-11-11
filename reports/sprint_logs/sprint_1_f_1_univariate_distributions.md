# Sprint 1.f.1: Analyze Univariate Distributions

## Objective
Analyze statistical moments, quantiles, skewness, kurtosis, and categorical distributions across all input features and target variables in the curated $\text{MoS}_2$ contact dataset, and detect potential outliers.

## Univariate Statistical Summary
1. **Target Variables:**
   - **$\log_{10}(R_c)$:** Mean: $3.12$, Median: $3.08$ (corresponding to $R_c \approx 1200\,\Omega\cdot\mu\text{m}$), IQR: $0.98$, Skewness: $0.44$, Kurtosis: $-0.28$. The logarithmic transform exhibits clean quasi-normal characteristics suitable for regression.
   - **Schottky Barrier Height ($\Phi_B$):** Mean: $0.34\,\text{eV}$, Median: $0.28\,\text{eV}$, Min: $0.0\,\text{eV}$ (Bi semimetal), Max: $1.45\,\text{eV}$ (Pt vdW), Skewness: $1.41$.
2. **Key Input Features:**
   - **Metal Work Function ($\Phi_M$):** Spans $3.50\,\text{eV}$ (Sc) to $5.65\,\text{eV}$ (Pt), with mean $4.62\,\text{eV}$ and median $4.50\,\text{eV}$.
   - **Contact Architecture Representation:** Dominated by `Top_Contact` (evaporated) and `vdW_Laminated`/`Semimetal_vdW`, providing balanced coverage between Fermi-pinned and de-pinned contacts.
3. **Outlier Detection:**
   - No catastrophic outliers detected in the log-transformed space; all points lie within physical device bounds ($10^2 - 10^5\,\Omega\cdot\mu\text{m}$).

## Deliverables
- `data/processed/univariate_distribution_summary.json`: Detailed statistical moment summary.
- `reports/figures/univariate_distributions.png`: 4-panel publication-grade distribution figure.
- `src/visualization/univariate_distributions.py`: Analysis and visualization module.
- `tests/test_univariate_eda.py`: Automated test suite.
