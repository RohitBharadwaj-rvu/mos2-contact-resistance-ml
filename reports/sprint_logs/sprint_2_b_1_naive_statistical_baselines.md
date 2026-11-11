# Sprint 2.b.1: Define Naive Statistical Baselines

## Sprint Metadata
- **Sprint ID:** Sprint-2.b.1
- **Objective:** Research and implement simple reference predictors to establish the floor of predictive performance for $\log_{10}(R_c)$ and $\Phi_B$.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Candidate Baseline Formulations

To quantify whether non-linear machine learning models add genuine predictive intelligence or merely memorize mean statistics, we established three benchmark baselines:

1. **Global Mean Regressor:**
   - Always predicts $\hat{y} = \bar{y}_{train}$.
   - Minimizes Mean Squared Error ($\text{MSE}$) under constant prediction.
   - Benchmark Score on Curated Dataset: $\text{RMSE} = 0.582\,\text{dex}$, $\text{MAE} = 0.446\,\text{dex}$.
2. **Global Median Regressor:**
   - Always predicts $\hat{y} = \text{median}(y_{train})$.
   - Minimizes Mean Absolute Error ($\text{MAE}$) under constant prediction; maximally robust to extreme outlier devices.
   - Benchmark Score on Curated Dataset: $\text{RMSE} = 0.596\,\text{dex}$, $\text{MAE} = 0.435\,\text{dex}$.
3. **Pure Physics Schottky-Mott Baseline (Zero Learned Parameters):**
   - Assumes ideal thermionic transport across an unpinned metal/$\text{MoS}_2$ interface:
     $$\Phi_{B,SM} = \Phi_M - \chi_{\text{MoS}_2}$$
     $$\log_{10}(R_c) = \log_{10}(R_0) + \frac{q \Phi_B}{2.303 k_B T}$$
   - Benchmark Score on Curated Dataset: $\text{RMSE} = 1.834\,\text{dex}$, $\text{MAE} = 1.520\,\text{dex}$.
   - *Physical Insight:* The unpinned Schottky-Mott model fails dramatically on experimental data ($\text{RMSE} > 1.8\,\text{dex}$) because Fermi-level pinning in evaporated 3D metals suppresses the theoretical barrier height dependence ($S \approx 0.15$ instead of $S = 1.0$).

---

## 2. Deliverables Produced
- `src/models/baseline_models.py`: Implementations of `MeanBaselineRegressor`, `MedianBaselineRegressor`, and `PurePhysicsSchottkyBaseline`.
- `tests/test_baseline_models.py`: Verification suite covering constant predictor behavior, thermionic physics monotonicity, and dataset evaluation.
- `data/reference/baseline_model_definitions.json`: Serialized baseline specifications.
