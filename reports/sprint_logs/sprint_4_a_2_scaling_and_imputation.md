# Sprint 4.a.2: Implement Model Family-Specific Scaling and Imputation

## Sprint Metadata
- **Sprint ID:** Sprint-4.a.2
- **Objective:** Construct an integrated preprocessing pipeline that adapts missing value imputation and feature scaling rules specifically to the mathematical requirements of each model family (Linear, Kernel/Bayesian, Tree Ensembles, Symbolic Regression).
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Family-Specific Preprocessing Strategy

1. **Regularized Linear & Parametric (Ridge, Lasso, ElasticNet):**
   - Imputer: Median imputation on training split.
   - Scaler: `StandardScaler()`.
   - *Rationale:* Features range from $4.0\,\text{eV}$ (work function) to $10^{13}\,\text{cm}^{-2}$ (gate carrier density). Without standardization, the $L_1/L_2$ regularization penalty penalizes coefficients on tiny scales unfairly.
2. **Kernel & Bayesian Non-Parametric (GPR, SVR, Kernel Ridge):**
   - Imputer: Median imputation.
   - Scaler: `StandardScaler()`.
   - *Rationale:* RBF and Matérn distance metrics $\exp(-\|x_i - x_j\|^2 / 2l^2)$ require equalized coordinate variances to prevent single raw features from dominating distance calculations.
3. **Tree-Based Ensembles (Random Forest, Gradient Boosting):**
   - Imputer: Median imputation.
   - Scaler: `StandardScaler()` (or passthrough).
   - *Rationale:* Ensures zero `NaN` occurrences across all fold splits while preserving rank invariants.
4. **Symbolic Regression (`gplearn`):**
   - Imputer: Median imputation.
   - Scaler: `MinMaxScaler(feature_range=(0.1, 1.0))`.
   - *Rationale:* Ensures strictly positive input features, completely preventing division-by-zero singularities and negative logarithm crashes during evolutionary tree evaluations.

---

## 2. Deliverables Produced
- `src/features/preprocessor_factory.py`: Family-adaptive preprocessing factory `build_family_preprocessor()`.
- `tests/test_preprocessor_factory.py`: Unit tests verifying zero residual NaNs and positive value bounds for symbolic regression.
- `data/reference/preprocessor_pipeline_spec.json`: Machine-readable specification.
