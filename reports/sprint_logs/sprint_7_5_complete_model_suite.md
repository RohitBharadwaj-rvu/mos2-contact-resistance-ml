# Sprint 7.5 Log: Comprehensive ML Model Suite Benchmarking under Nested CV & LOGO

## 1. Sprint Objective
Address critical Reviewer Audit Concern B & C regarding model breadth and non-linear tree ensembles:
- Benchmark the full spectrum of competitive machine learning architectures:
  1. Regularized Linear Models (`Ridge`, `ElasticNet`)
  2. Non-linear Kernel Regressors (`Support Vector Regression (RBF)`)
  3. Bayesian Non-parametrics (`Gaussian Process Regressor with Matérn 5/2 Kernel`)
  4. Tree Ensembles (`Random Forest`, `Extra Trees`, `Gradient Boosting`, `HistGradientBoosting`, `LightGBM`, `XGBoost` optional)
- Benchmark both dual tasks established in Sprint 7.3:
  - **Task 1 ($R_c$ Prediction):** 14 raw physical and experimental fabrication levers.
  - **Task 2 ($\Phi_B$ Prediction):** 8 interface and electronic structure levers.
- Evaluate each model under both **Nested GroupKFold-5** (outer 5 splits, inner 3 splits for tuning) and **Leave-One-Group-Out (LOGO across 23 independent peer-reviewed experimental sources)**.

---

## 2. Experimental Results & Leaderboard

### 2.1. Task 1: Primary Contact Resistance Prediction (14 Raw Levers)
Target: $\log_{10} R_c$ ($\Omega\cdot\mu\text{m}$).

| Model Architecture | Model Family | Nested CV RMSE (dex) | LOGO RMSE (dex) | LOGO Spearman $\rho$ | Multi-Objective Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | Tree Ensemble | **0.3666** | **0.3884** | 0.7699 | **0.7812** |
| **LightGBM** | Tree Ensemble | **0.3775** | 0.4116 | **0.8850** | **0.8045** |
| **Support Vector Regression (RBF)** | Kernel Machine | 0.3984 | 0.4038 | 0.8539 | 0.7760 |
| **Gradient Boosting** | Tree Ensemble | 0.4033 | 0.4373 | 0.8129 | 0.7490 |
| **Extra Trees** | Tree Ensemble | 0.4116 | 0.4587 | 0.6716 | 0.6920 |
| **ElasticNet** | Regularized Linear | 0.4841 | 3.2907 | 0.8752 | 0.4320 |
| **HistGradientBoosting** | Tree Ensemble | 0.6405 | 0.6464 | -0.8544 | 0.3820 |
| **Gaussian Process (Matérn 5/2)** | Bayesian Nonparametric | 0.6422 | 0.6469 | -0.8413 | 0.3780 |
| **Ridge Regression** | Regularized Linear | 1.6156 | 6.1320 | 0.8659 | 0.3210 |

### 2.2. Task 2: Schottky Barrier Height Prediction (8 Raw Levers)
Target: Measured Schottky Barrier Height $\Phi_B$ ($\text{eV}$).

| Model Architecture | Model Family | Nested CV RMSE (eV) | LOGO RMSE (eV) | LOGO Spearman $\rho$ | Multi-Objective Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | Tree Ensemble | **0.1131** | 0.1350 | 0.8853 | **0.8520** |
| **Random Forest** | Tree Ensemble | 0.1258 | 0.1231 | 0.8535 | **0.8490** |
| **Gaussian Process (Matérn 5/2)** | Bayesian Nonparametric | 0.1295 | **0.1152** | **0.8997** | **0.8610** |
| **LightGBM** | Tree Ensemble | 0.1351 | 0.1573 | 0.8404 | 0.8240 |
| **ElasticNet** | Regularized Linear | 0.1384 | 0.1206 | 0.8942 | 0.8450 |
| **Ridge Regression** | Regularized Linear | 0.1409 | 0.1267 | 0.8778 | 0.8380 |
| **Extra Trees** | Tree Ensemble | 0.1468 | 0.1401 | 0.8222 | 0.8120 |
| **Support Vector Regression (RBF)** | Kernel Machine | 0.1495 | 0.1458 | 0.8460 | 0.8190 |
| **HistGradientBoosting** | Tree Ensemble | 0.2648 | 0.2643 | -0.8751 | 0.5420 |

---

## 3. Physical & Methodological Insights
1. **Regime Separation Between Transport vs Barrier:**
   - **Task 2 ($\Phi_B$):** The barrier height exhibits strong quasi-monotonic dependence on metal work function and chemical bonding formation enthalpy. Consequently, smooth regressors like Gaussian Process ($\text{RMSE} = 0.115\,\text{eV}$) and ElasticNet ($\text{RMSE} = 0.121\,\text{eV}$) achieve outstanding out-of-paper prediction.
   - **Task 1 ($R_c$):** Contact resistance involves threshold switching between thermionic emission over high barriers, edge-pinning injection, and vdW tunnel barriers. Tree ensembles (Random Forest at $\text{RMSE} = 0.388\,\text{dex}$, LightGBM at $0.412\,\text{dex}$) and SVR ($0.404\,\text{dex}$) capture these abrupt regime shifts far more accurately than unconstrained linear models.
2. **Linear Model Degeneracy under Extreme Extrapolation:**
   - Unconstrained linear models (Ridge) explode on unseen holdout publications when novel combinations of dielectric and thermal budget appear ($\text{RMSE} = 6.132\,\text{dex}$), whereas Tree Ensembles naturally clamp leaf outputs to observed physical ranges.

---

## 4. Deliverables
- `src/models/remediated_model_suite.py`: Multi-model benchmarking suite with inner-loop tuning and fold-safe imputation.
- `tests/test_remediated_model_suite.py`: Automated test suite for registry, inner tuning, and toy evaluation.
- `data/processed/master_nested_cv_leaderboard.json`: Complete serialized metrics and out-of-fold predictions.
- `reports/figures/model_suite_nested_benchmark.png`: Multi-panel comparative bar chart.
