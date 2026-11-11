# Sprint 4.c.2 Log: Design and Run Systematic Tuning Search

## 1. Objectives & Search Protocol
- Execute systematic hyperparameter optimization across all 6 shortlisted model families.
- Guarantee leakage-free evaluation by optimizing strictly within paper-grouped 5-fold cross-validation (`GroupKFold(n_splits=5, groups=source_uid)`).
- Maximize the official multi-objective composite selection score:
  $$\text{Score} = 0.35 \cdot S_{\text{RMSE}} + 0.35 \cdot S_{\text{Spearman}} + 0.30 \cdot S_{\text{Concordance}} - P_{\text{complexity}}$$
- Analyze parameter sensitivity, variance, and optimal capacity regimes.

## 2. Tuning Results and Comparative Performance

| Architecture | Default Score | Tuned Score | Tuned RMSE (dex) | Tuned $\rho$ | Tuned $C$ | Optimal Hyperparameters |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Ridge Regression** | 0.8596 | **0.8720** | **0.2260** | **0.9489** | **0.9211** | `alpha: 5.0` |
| **ElasticNet** | 0.8626 | **0.8710** | **0.2277** | **0.9489** | **0.9211** | `alpha: 0.1, l1_ratio: 0.1` |
| **Gradient Boosting** | 0.7590 | **0.7870** | **0.3838** | **0.9023** | **0.8737** | `n_estimators: 75, lr: 0.1, max_depth: 3, subsample: 0.8` |
| **Gaussian Process (Matérn)** | 0.7364 | **0.7781** | **0.3904** | **0.8872** | **0.8789** | `length_scale: 0.5, noise_level: 0.01, nu: 1.5` |
| **Random Forest** | 0.7434 | **0.7535** | **0.4187** | **0.8718** | **0.8368** | `n_estimators: 30, max_depth: 3, min_samples_split: 3, min_leaf: 2` |
| **SVR (RBF)** | 0.6970 | **0.7508** | **0.4172** | **0.8632** | **0.8474** | `C: 20.0, epsilon: 0.02, gamma: 0.05` |

## 3. Key Physical & Algorithmic Insights
1. **L2 Shrinkage Sweet Spot:** Ridge optimal `alpha` increased from 1.0 to 5.0, reflecting the benefit of stronger shrinkage when learning over collinear solid-state descriptors ($n_{2D}$, $\Phi_B$, $\Delta H_f$).
2. **Gradient Boosting Capacity:** Adding shallow depth (`max_depth=3`) with moderate bagging (`subsample=0.8`) and 75 iterations drove out-of-fold RMSE from 0.4098 down to 0.3838 dex without over-fitting.
3. **SVR Qualification:** The default SVR previously failed the qualification threshold ($\text{Score} = 0.6970 < 0.70$). Narrowing the margin to $\epsilon = 0.02$ and expanding $C$ to $20.0$ elevated SVR into qualified status ($\text{Score} = 0.7508$).
4. **Gaussian Process Noise Filtering:** Lowering noise level to $0.01$ and using $\nu=1.5$ (Matérn with lower differentiability) improved modeling of steep contact resistance transitions at the de-pinning threshold.

## 4. Implemented Deliverables
- `src/models/hyperparameter_tuner.py`: Grid search engine across grouped folds.
- `tests/test_hyperparameter_tuner.py`: Verification tests for grids, single architecture tuning, and full search pipeline.
- `data/processed/tuned_hyperparameters_and_scores.json`: Complete parameter logs, top-5 configurations, and sensitivity statistics.

## 5. Verification & Validation
- Ran `python -m pytest tests/test_hyperparameter_tuner.py` — 3/3 passed in 105s.
