# Sprint 4.b.2: Train Default Candidate Non-Linear Models

## Sprint Metadata
- **Sprint ID:** Sprint-4.b.2
- **Objective:** Train shortlisted non-linear models (Random Forest, Gradient Boosting, GPR Matérn 5/2, SVR) with default capacity-constrained settings across official `GroupKFold(n_splits=5)` splits; verify pipeline functionality and record initial out-of-fold benchmarks.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Out-of-Fold Performance Comparison (Default Hyperparameters)

| Model Architecture | Default Hyperparameters | $\text{RMSE}_{\text{oof}} (\text{dex})$ | Spearman $\rho_{\text{oof}}$ | Concordance $C_{\text{oof}}$ | Composite Score $\mathcal{S}$ | Qualification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting** | $\text{depth}=3, N=50, lr=0.05$ | **$0.4098\,\text{dex}$** | **$+0.8868$** | **$0.8500$** | **$0.7590$** | **PASS (Non-Linear Leader)** |
| **Random Forest** | $\text{depth}=3, N=50, \text{leaf}=2$ | $0.4098\,\text{dex}$ | $+0.8612$ | $0.8237$ | $0.7434$ | **PASS** |
| **GPR (Matérn 5/2)** | $C \times \text{Matérn}(l=2.0) + \text{White}$ | $0.4518\,\text{dex}$ | $+0.8647$ | $0.8579$ | $0.7364$ | Borderline ($0.4518 > 0.45$) |
| **SVR (RBF)** | $C=5.0, \epsilon=0.10$ | $0.5337\,\text{dex}$ | $+0.7053$ | $0.7632$ | $0.6242$ | Fail (Requires $C/\gamma$ tuning) |

---

## 2. Key Diagnostic Findings
1. **Tree Ensembles Achieve Robust Rank Correlation:** Both Gradient Boosting and Random Forest achieve $\rho > 0.86$ out-of-fold, demonstrating that even with default parameters, tree splits effectively capture the primary ordering between semimetal/vdW contacts and evaporated pinned contacts.
2. **Identification of Tuning Opportunities for Subheading 4.c:**
   - Default GPR with fixed length-scale $2.0$ produces fold-1 outlier error ($0.916\,\text{dex}$) because fold 1 contains McDonnell et al. high-barrier evaporated Au/Pt contacts. Tuning the noise prior $\sigma_{noise}^2$ and length-scale bounds will regularize these predictions.
   - SVR with unoptimized $C=5.0$ and default scale gamma underfits fold 1, highlighting the necessity of systematic grid search over $C \in [0.1, 100]$ and $\epsilon \in [0.01, 0.5]$.

---

## 3. Deliverables Produced
- `src/models/nonlinear_runner.py`: Cross-validation execution suite for default non-linear models.
- `tests/test_nonlinear_runner.py`: Verification tests for out-of-fold execution and metric validity.
- `data/processed/default_nonlinear_cross_validation_results.json`: Serialized out-of-fold predictions, fold metrics, and composite scores.
