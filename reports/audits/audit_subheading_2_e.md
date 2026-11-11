# Subheading 2.e Audit: Interpretability & Decoupling Analysis Frameworks

## 1. Scope & Objectives
Subheading 2.e establishes the mathematical and physical methodologies for model interpretability and domain decoupling:
- **Sprint 2.e.1:** Post-hoc explanation methods (TreeSHAP, KernelSHAP, Permutation Feature Importance, Partial Dependence Plots).
- **Sprint 2.e.2:** Intrinsic metal vs extrinsic processing decoupling framework, domain attribution shares, and actionable experimental bounds.

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Ill-Conditioned Feature Covariance in Decoupling Unit Test
- **Issue:** Test matrix featured unscaled gate carrier density values ($10^{12}\,\text{cm}^{-2}$) alongside work function ($4.0\,\text{eV}$), causing numerical ill-conditioning in unscaled Ridge regression tests.
- **Resolution:** Added `StandardScaler()` into the test pipeline, eliminating `LinAlgWarning` and ensuring numerical stability.

### Gap 2: End-to-End Prediction Decoupler
- **Issue:** Downstream modules in Section 5 needed a single callable function that takes any trained estimator, computes feature attributions, and directly maps them into the 3 physical domain shares.
- **Resolution:** Implemented `decouple_model_predictions(model, X, y)` in `src/models/decoupling_framework.py`, returning both granular feature importances and aggregated domain percentages (`intrinsic_share_pct`, `extrinsic_share_pct`, `electrostatic_share_pct`).

---

## 3. Verification & Compliance
- Serialized specifications in `data/reference/explainability_methodology.json` and `data/reference/decoupling_framework_spec.json`.
- 100% passing tests across `tests/test_explainability_framework.py` and `tests/test_decoupling_framework.py`.

Subheading 2.e is certified and approved to advance to the Heading 2 Major Milestone Review.
