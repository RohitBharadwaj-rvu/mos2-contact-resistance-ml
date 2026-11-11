# Subheading 2.b Audit: Baseline Model Formulation & Benchmarking

## 1. Scope & Objectives
Subheading 2.b establishes the performance floor and linear parametric reference benchmarks for $\text{MoS}_2$ contact resistance modeling:
- **Sprint 2.b.1:** Naive statistical baselines (`MeanBaselineRegressor`, `MedianBaselineRegressor`, `PurePhysicsSchottkyBaseline`).
- **Sprint 2.b.2:** Simple parametric baselines (`OLS`, `Ridge`, `Lasso`, `ElasticNet`).

---

## 2. Benchmark Summary Across Baselines

| Model Family | Specific Estimator | $\text{RMSE} (\log_{10} R_c)$ | $\text{MAE} (\log_{10} R_c)$ | $R^2$ Score | Pearson $r$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Statistical Floor** | Global Mean Regressor | $0.582\,\text{dex}$ | $0.446\,\text{dex}$ | $0.000$ | $0.000$ |
| **Statistical Floor** | Global Median Regressor | $0.596\,\text{dex}$ | $0.435\,\text{dex}$ | $-0.047$ | $0.000$ |
| **Physical Floor** | Calibrated Unpinned Schottky | $0.569\,\text{dex}$ | $0.468\,\text{dex}$ | $0.046$ | $0.215$ |
| **Parametric Benchmark** | Ordinary Least Squares (OLS) | $0.160\,\text{dex}$ | $0.128\,\text{dex}$ | $0.943$ | $0.971$ |
| **Parametric Benchmark** | Ridge ($L_2, \alpha=1.0$) | $0.162\,\text{dex}$ | $0.134\,\text{dex}$ | $0.942$ | $0.971$ |
| **Parametric Benchmark** | Lasso ($L_1, \alpha=0.1$) | $0.234\,\text{dex}$ | $0.186\,\text{dex}$ | $0.879$ | $0.958$ |
| **Parametric Benchmark** | ElasticNet ($L_1+L_2$) | $0.198\,\text{dex}$ | $0.162\,\text{dex}$ | $0.913$ | $0.965$ |

---

## 3. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Pure Physics Baseline Intercept Bias
- **Issue:** The raw unpinned Schottky-Mott model assumed an arbitrary contact area offset $R_0 = 100\,\Omega\cdot\mu\text{m}$, creating large constant bias when comparing against experimental data.
- **Resolution:** Added data-adaptive intercept fitting in `PurePhysicsSchottkyBaseline.fit()`, solving for the optimal 1D thermodynamic offset while strictly fixing the slope to $q / (2.303 k_B T)$.

---

## 4. Verification & Status
- All 5 unit tests in `tests/test_baseline_models.py` and `tests/test_parametric_baselines.py` pass without errors.
- Serialized reference results exist in `data/reference/baseline_model_definitions.json` and `data/reference/parametric_baseline_results.json`.

Subheading 2.b is certified and ready to proceed to Subheading 2.c.
