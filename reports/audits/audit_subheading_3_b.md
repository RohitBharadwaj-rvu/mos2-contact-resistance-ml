# Subheading 3.b Audit: Evaluation Metrics & Model Selection Criteria

## 1. Scope & Objectives
Subheading 3.b defines the formal regression error metrics, rank correlation metrics, and multi-objective model selection criteria:
- **Sprint 3.b.1:** Scale-invariant error metrics ($\text{RMSE}_{\text{dex}}$, $\text{MAE}_{\text{dex}}$, geometric factor error, linear $\text{MedAPE}$).
- **Sprint 3.b.2:** Rank and monotonic trend metrics (Spearman $\rho$, Kendall $\tau$, pairwise Concordance Index $C$).
- **Sprint 3.b.3:** Multi-objective composite model selection formula ($\mathcal{S}_{\text{selection}}$) and deployment qualification thresholds.

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Standalone Cross-Validation Model Scorer
- **Issue:** Section 4 hyperparameter optimization and benchmarking required a single reusable function to run any estimator over CV splits and directly return the multi-objective selection report with out-of-fold metrics.
- **Resolution:** Implemented `evaluate_model_cv(model, X, y, splits=None)` in `src/validation/selection_criteria.py`. It automatically clones estimators, trains on training folds, aggregates out-of-fold predictions, and computes the composite selection score along with fold-level RMSE and MAE.

---

## 3. Verification & Compliance
- Serialized reference specifications in `data/reference/regression_error_metrics.json`, `data/reference/rank_trend_metrics_spec.json`, and `data/reference/model_selection_criteria.json`.
- 100% passing tests across `tests/test_regression_metrics.py`, `tests/test_rank_trend_metrics.py`, and `tests/test_selection_criteria.py`.

Subheading 3.b is certified and ready to advance to the Heading 3 Major Milestone Review.
