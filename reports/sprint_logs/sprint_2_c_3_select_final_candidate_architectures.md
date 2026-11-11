# Sprint 2.c.3: Select Final Candidate Architectures

## Sprint Metadata
- **Sprint ID:** Sprint-2.c.3
- **Objective:** Compare the strengths, empirical benchmarks, and theoretical properties of all researched models against EDA findings; construct a multi-criteria decision matrix and shortlist the final candidate algorithms for implementation and optimization.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Multi-Criteria Architecture Decision Matrix

Candidates were evaluated across five weighted axes tailored to small-$N$ 2D semiconductor modeling:
1. **Small-$N$ Generalization & Parsimony ($25\%$):** Resistance to overfitting and high variance under $N=20$.
2. **Physical Interpretability & Attribution ($25\%$):** Direct connection between learned parameters and solid-state transport physics.
3. **Non-Linear Interactions & Saturation ($20\%$):** Ability to capture gating thresholds, Fermi shifts, and semimetal de-pinning steps.
4. **Uncertainty Quantification ($20\%$):** Capability to provide calibrated confidence bounds for unmeasured metals and process recipes.
5. **Optimization Stability ($10\%$):** Deterministic convex or closed-form solutions with minimal hyperparameter fragility.

### Summary Scores

| Architecture | Model Family | Composite Score (0–10) | Decision | Architectural Role |
| :--- | :--- | :--- | :--- | :--- |
| **Gaussian Process (Matérn 5/2)** | Bayesian Non-Parametric | **8.78** | **SHORTLISTED (Champion)** | Closed-form Bayesian uncertainty, experimental noise estimation, non-linear kernel smoothness. |
| **Ridge Regression** | Regularized Linear | **8.38** | **SHORTLISTED (Baseline)** | Robust parsimonious linear benchmark with direct sign/magnitude coefficient verification. |
| **Random Forest** | Tree Bagging | **8.18** | **SHORTLISTED (Ensemble)** | Subsampling variance reduction, non-linear gating threshold splits. |
| **ElasticNet** | Sparse Regularized Linear | **8.12** | **SHORTLISTED (Baseline)** | Automated feature zeroing and convex feature selection. |
| **Gradient Boosting** | Gradient Boosted Trees | **8.08** | **SHORTLISTED (Ensemble)** | Highly expressive non-linear champion capturing complex interaction terms. |
| **SVR (RBF)** | Kernel Support Vector | **7.78** | **SHORTLISTED (Kernel)** | $\epsilon$-insensitive margin regressor immune to minor experimental noise. |
| **Unregularized OLS** | Ordinary Least Squares | **6.40** | **REJECTED** | Severe risk of multicollinearity variance explosion in small-$N$ regime. |

---

## 2. Selected Shortlist Strategy for Section 4 Training

The shortlisted models span three complementary philosophical paradigms:
1. **Parsimonious Linear Regularized:** Ridge and ElasticNet.
2. **Non-Linear Tabular Ensembles:** Gradient Boosting and Random Forest.
3. **Continuous Bayesian / Kernel:** Gaussian Process (Matérn 5/2) and SVR.

---

## 3. Deliverables Produced
- `src/models/model_selector.py`: Decision matrix synthesizer and official architecture shortlist retriever.
- `tests/test_model_selector.py`: Verification suite confirming weights, composite scores, and shortlisting rules.
- `data/reference/shortlisted_architectures.json`: Serialized decision matrix.
