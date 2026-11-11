# Subheading 3.a Audit: Paper-Wise Validation Scheme & Splitting Protocol

## 1. Scope & Objectives
Subheading 3.a establishes the data leakage protection and cross-validation splitting protocols for the project:
- **Sprint 3.a.1:** Data leakage risk analysis, identifying multi-device paper vulnerabilities ($55\%$ of records) and proving that random K-fold splits suffer from $> 60\%$ fold contamination.
- **Sprint 3.a.2:** Grouped cross-validation scheme benchmarking (`GroupKFold` vs `LeaveOneGroupOut`), establishing baseline out-of-fold metrics and measuring optimism penalties.
- **Sprint 3.a.3:** Configuration and distribution audit of the official splitting protocol, verifying fold balance and target range coverage.

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Reusable Cross-Validation Split Generator
- **Issue:** Models in Section 4 required disparate initialization for `GroupKFold` vs `LeaveOneGroupOut` indexing arrays.
- **Resolution:** Implemented `get_cv_splits(df=None, scheme="grouped_5fold")` in `src/validation/splitting_protocol.py`, providing a drop-in split provider supporting `"grouped_5fold"`, `"logo"`, and `"random_5fold"`.

---

## 3. Verification & Compliance
- Serialized specifications in `data/reference/data_leakage_risk_analysis.json`, `data/reference/grouped_cv_comparison.json`, and `data/reference/official_validation_protocol.json`.
- 100% passing tests across `tests/test_leakage_analyzer.py`, `tests/test_grouped_cv_evaluator.py`, and `tests/test_splitting_protocol.py`.

Subheading 3.a is certified and approved to advance to Subheading 3.b.
