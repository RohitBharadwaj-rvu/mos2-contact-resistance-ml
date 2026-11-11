# Subheading 4.b Audit: Baseline and Non-Linear Model Training

## 1. Scope & Objectives
Subheading 4.b executes the first systematic out-of-fold training runs across both baseline and candidate non-linear architectures:
- **Sprint 4.b.1:** Baseline cross-validation runs under `GroupKFold(n_splits=5)` for naive statistical baselines (Mean, Median, Pure Physics Schottky) and simple parametric linear models (OLS, Ridge, Lasso, ElasticNet).
- **Sprint 4.b.2:** Default non-linear candidate cross-validation runs under `GroupKFold(n_splits=5)` for Random Forest, Gradient Boosting, GPR (Matérn 5/2), and SVR (RBF).

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Integrated Benchmark Leaderboard
- **Issue:** Baseline scores and non-linear candidate scores were isolated in separate JSON files without a unified competitive ranking.
- **Resolution:** Implemented `compile_master_benchmark_leaderboard()` in `src/models/model_benchmark_aggregator.py`, compiling all 11 evaluated estimators, ranking them strictly by composite selection score, and exporting `data/processed/master_model_benchmark_leaderboard.json`.

---

## 3. Comprehensive Leaderboard Pre-Tuning

| Rank | Model Architecture | Category | $\text{RMSE}_{\text{oof}} (\text{dex})$ | Spearman $\rho_{\text{oof}}$ | Concordance Index $C$ | Composite Score $\mathcal{S}$ | Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `elastic_net` | Regularized Linear | $0.2509$ | $+0.9504$ | $0.9211$ | **0.8626** | Qualified |
| **2** | `ridge_regression` | Regularized Linear | $0.2306$ | $+0.9338$ | $0.9000$ | **0.8596** | Qualified |
| **3** | `ordinary_least_squares` | Linear | $0.2514$ | $+0.9293$ | $0.9000$ | **0.8497** | Qualified |
| **4** | `lasso_regression` | Regularized Linear | $0.3185$ | $+0.9188$ | $0.8789$ | **0.8139** | Qualified |
| **5** | `Gradient_Boosting` | Non-Linear Ensemble | $0.4098$ | $+0.8868$ | $0.8500$ | **0.7590** | Qualified |
| **6** | `Random_Forest` | Non-Linear Ensemble | $0.4098$ | $+0.8612$ | $0.8237$ | **0.7434** | Qualified |
| **7** | `Gaussian_Process_Matern` | Bayesian Kernel | $0.4518$ | $+0.8647$ | $0.8579$ | **0.7364** | Borderline |
| **8** | `Support_Vector_Regression` | Kernel Margin | $0.5337$ | $+0.7053$ | $0.7632$ | **0.6242** | Unqualified |
| **9** | `pure_physics_schottky` | Pure Physics | $1.9687$ | $+0.5518$ | $0.7026$ | **0.3688** | Floor Fail |
| **10**| `mean_baseline` | Naive Statistical | $0.7294$ | $-0.5764$ | $0.3000$ | **0.1832** | Floor Fail |
| **11**| `median_baseline` | Naive Statistical | $0.7661$ | $-0.5504$ | $0.3211$ | **0.1738** | Floor Fail |

---

## 4. Verification & Status
- All 11 models execute successfully under zero-leakage paper-grouped splits.
- All unit tests in `tests/test_baseline_runner.py`, `tests/test_nonlinear_runner.py`, and `tests/test_model_benchmark_aggregator.py` pass cleanly.

Subheading 4.b is certified and ready to advance to Subheading 4.c.
