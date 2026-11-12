# Sprint 7.2 Log: Scientific Missing-Value Handling & Granular Provenance Tracking

## 1. Sprint Objective
Address critical Audit Concern C:
- Eliminate crude hardcoded default substitutions (e.g., assuming unreported annealing implies 20°C annealing, or assuming unreported carrier density is $10^{13}\,\text{cm}^{-2}$).
- Explicitly differentiate between a physical zero-treatment state (`as_fabricated_unannealed`) and an unmeasured/unreported parameter (`unreported`).
- Develop a scikit-learn compatible `ScientificMissingnessHandler` that preserves `NaN` values natively for tree-based architectures (XGBoost, HistGradientBoosting) and applies fold-safe median imputation strictly within training folds for linear/regularized models.

---

## 2. Methodology & Scientific Justification

### 2.1. The Conflation of Physical State and Missingness
In previous iterations, missing annealing temperatures were filled with 20°C. In physical device characterization, an experimentalist who does not perform thermal annealing produces an *as-fabricated* contact. This is not missing data; it is an active physical state (`is_annealed = 0`, duration = 0). Conversely, if a study reports that annealing was performed in Ar but fails to state the temperature, the temperature is genuinely *unreported*. Conflating these two conditions introduces artificial clustering into small-sample datasets.

### 2.2. Rigorous Handling Architecture
1. **Explicit Physical Flags:**
   - `post_annealing_status`: Explicitly partitioned into `performed` (14 devices) and `as_fabricated_unannealed` (14 devices).
   - `is_annealed`: Binary indicator ($1$ if annealed, $0$ if as-fabricated).
2. **Missingness Preservation for Tree Models:**
   Modern gradient boosting frameworks (XGBoost, HistGradientBoosting, LightGBM) natively support missing values by learning default branching directions at split nodes. The handler preserves `NaN` values directly in `native_nan` mode.
3. **Leakage-Free Fold Imputation for Linear Models:**
   In `fold_imputed` mode, medians are computed *strictly* on training folds during cross-validation, guaranteeing zero look-ahead leakage. Every imputed feature receives an accompanying binary missingness mask (`feature_is_missing`).

---

## 3. Key Deliverables
- `src/features/scientific_imputation_engine.py`: Transformer handling native NaNs, fold-safe imputations, and missingness masks.
- `tests/test_scientific_imputation_engine.py`: Comprehensive test suite verifying fold-safe medians and NaN preservation.
- `data/processed/missingness_provenance_audit.json`: Complete dataset missingness audit report.

---

## 4. Verification & Status
- Unit tests: 100% passing.
- Leakage-free fold imputation validated.
- Completed Sprint 7.2.
