# Sprint 2.b.2: Define Simple Parametric Baselines

## Sprint Metadata
- **Sprint ID:** Sprint-2.b.2
- **Objective:** Implement and benchmark standard low-complexity linear regression models (OLS, Ridge, Lasso, ElasticNet) as parametric benchmarks using the parsimonious feature subset.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Parametric Benchmark Results

We evaluated four linear parametric models trained on the standardized 4-feature parsimonious subset:
1. `physics_predicted_sbh_ev`
2. `is_vdw_or_depinned_contact`
3. `gate_carrier_density_cm2`
4. `sulfide_formation_enthalpy_kj_mol`

| Model Architecture | Regularization | $\text{RMSE} (\log_{10} R_c)$ | $\text{MAE} (\log_{10} R_c)$ | $R^2$ Score | Pearson $r$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OLS (Unregularized)** | None | $0.160\,\text{dex}$ | $0.128\,\text{dex}$ | $0.943$ | $0.971$ |
| **Ridge Regression** | $L_2$ ($\alpha = 1.0$) | $0.162\,\text{dex}$ | $0.134\,\text{dex}$ | $0.942$ | $0.971$ |
| **Lasso Regression** | $L_1$ ($\alpha = 0.1$) | $0.234\,\text{dex}$ | $0.186\,\text{dex}$ | $0.879$ | $0.958$ |
| **ElasticNet** | $L_1 + L_2$ ($\alpha=0.1, l_1=0.5$) | $0.198\,\text{dex}$ | $0.162\,\text{dex}$ | $0.913$ | $0.965$ |

---

## 2. Physical Consistency of Learned Weights

Examining the standardized weights reveals remarkable alignment with physical transport theory:
- **$\hat{\Phi}_B$ Coefficient ($+0.401$ to $+0.315$):** Positive weight confirms higher interfacial barrier increases $R_c$.
- **v体制/De-pinning Flag ($-0.218$ to $-0.080$):** Negative weight indicates semimetals and transfer contacts sharply lower $R_c$.
- **Gate Density $n_{2D}$ ($-0.304$ to $-0.281$):** Negative weight confirms electrostatic gate modulation compresses the depletion width and lowers tunneling resistance.
- **Sulfide Enthalpy ($+0.089$):** Modest positive weight aligns with chemical reactivity altering local interface quality.

---

## 3. Deliverables Produced
- `src/models/parametric_baselines.py`: Implementation of parametric pipeline builders and benchmark evaluations.
- `tests/test_parametric_baselines.py`: Automated unit tests verifying pipeline behavior and metrics.
- `data/reference/parametric_baseline_results.json`: Serialized benchmark scores and model weights.
