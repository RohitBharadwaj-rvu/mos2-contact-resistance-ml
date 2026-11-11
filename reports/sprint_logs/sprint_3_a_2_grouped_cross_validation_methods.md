# Sprint 3.a.2: Research and Benchmark Grouped Cross-Validation Methods

## Sprint Metadata
- **Sprint ID:** Sprint-3.a.2
- **Objective:** Implement and benchmark GroupKFold and Leave-One-Group-Out (LOGO) cross-validation schemes grouped strictly by source paper UID; quantify the out-of-distribution generalization performance and optimism penalty of random splits.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Cross-Validation Schemes Evaluated

To prevent intra-laboratory leakage and benchmark true out-of-distribution transferability to unseen experimental cleanrooms, we compared three cross-validation protocols:
1. **Random 5-Fold (Unconstrained Baseline):** Standard random partitioning; vulnerable to intra-paper leakage.
2. **Grouped 5-Fold (`GroupKFold(n_splits=5)`):** Partitions the 13 literature clusters across 5 folds such that all devices from any single paper reside exclusively in either the training or validation fold ($0\%$ overlap).
3. **Leave-One-Group-Out (`LeaveOneGroupOut`):** Iterates over all 13 distinct publication sources, holding out one full study per fold and training on the remaining 12.

---

## 2. Empirical Cross-Validation Results

| Architecture | Metric | Random 5-Fold | Grouped 5-Fold | LOGO (13 Folds) | Optimism Penalty ($\Delta \text{RMSE}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ridge Regression** | $\text{RMSE} (\log_{10} R_c)$ | $0.219\,\text{dex}$ | $0.231\,\text{dex}$ | $0.240\,\text{dex}$ | $+0.012\,\text{dex}$ |
| | $\text{MAE} (\log_{10} R_c)$ | $0.182\,\text{dex}$ | $0.196\,\text{dex}$ | $0.206\,\text{dex}$ | |
| | Pearson $r$ | $0.946$ | $0.942$ | $0.936$ | |
| **Gradient Boosting** | $\text{RMSE} (\log_{10} R_c)$ | $0.420\,\text{dex}$ | $0.410\,\text{dex}$ | $0.415\,\text{dex}$ | $-0.010\,\text{dex}$ |
| | $\text{MAE} (\log_{10} R_c)$ | $0.313\,\text{dex}$ | $0.290\,\text{dex}$ | $0.300\,\text{dex}$ | |
| | Pearson $r$ | $0.784$ | $0.796$ | $0.790$ | |
| **GPR (Matérn 5/2)** | $\text{RMSE} (\log_{10} R_c)$ | $0.417\,\text{dex}$ | $0.452\,\text{dex}$ | $0.433\,\text{dex}$ | $+0.035\,\text{dex}$ |
| | $\text{MAE} (\log_{10} R_c)$ | $0.246\,\text{dex}$ | $0.250\,\text{dex}$ | $0.252\,\text{dex}$ | |
| | Pearson $r$ | $0.794$ | $0.756$ | $0.780$ | |

---

## 3. Methodological Decisions
- **Standard Protocol:** Grouped 5-Fold is selected for fast hyperparameter tuning in Section 4.
- **Final Benchmark:** Leave-One-Group-Out (LOGO) is selected as the primary certification metric for final model comparisons, as it precisely models deploying the trained model to predict results from a brand-new, unseen research group.

---

## 4. Deliverables Produced
- `src/validation/grouped_cv_evaluator.py`: Split generators and comparative validation evaluator.
- `tests/test_grouped_cv_evaluator.py`: Automated verification suite for zero-leakage splits and LOGO fold counts.
- `data/reference/grouped_cv_comparison.json`: Serialized empirical cross-validation benchmarks.
