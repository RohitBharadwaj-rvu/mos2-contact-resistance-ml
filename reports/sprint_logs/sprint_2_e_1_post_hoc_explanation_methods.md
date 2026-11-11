# Sprint 2.e.1: Study Post-Hoc Explanation Methods

## Sprint Metadata
- **Sprint ID:** Sprint-2.e.1
- **Objective:** Research post-hoc feature attribution and model explanation frameworks (SHAP, Permutation Feature Importance, Partial Dependence Profiling) to understand how they compute feature contributions, quantify interaction effects, and explain non-linear semiconductor predictions.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Theoretical Foundations of Post-Hoc Attribution

To unpack the physical predictions of non-linear tree ensembles, kernel models, and Gaussian Processes, we evaluated four explanation methodologies:
1. **Shapley Additive exPlanations (SHAP):**
   - Anchored in cooperative game theory (Shapley, 1953; Lundberg & Lee, 2017).
   - Uniquely satisfies four fundamental axioms:
     - **Efficiency:** $\sum_{i=1}^M \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
     - **Symmetry:** If features $i$ and $j$ contribute equally to all subsets, $\phi_i = \phi_j$.
     - **Dummy:** A feature with no effect receives $\phi_i = 0$.
     - **Additivity:** Attributions across ensemble trees sum linearly.
   - **TreeSHAP:** Runs in polynomial time $O(T L D^2)$, computing exact Shapley values for Gradient Boosting and Random Forest without sampling approximations.
   - **KernelSHAP:** Uses weighted linear surrogate regression for model-agnostic attribution across GPR and SVR.
2. **Permutation Feature Importance:**
   - Shuffles input columns on held-out validation folds and measures degradation in $\text{RMSE}(\log_{10} R_c)$.
   - Prototype execution on Gradient Boosting reveals `gate_carrier_density_cm2` ($\Delta \text{MSE} \approx 0.60$) and `physics_predicted_sbh_ev` ($\Delta \text{MSE} \approx 0.17$) as the primary drivers of model performance.
3. **Partial Dependence Profiling (PDP):**
   - Traces the marginal response surface $\mathbb{E}_{X_{-j}}[f(x_j, X_{-j})]$, visualizing non-linear gating thresholds and Fermi-level pinning asymptotes.

---

## 2. Deliverables Produced
- `src/models/explainability_framework.py`: Mathematical specification and prototype permutation importance evaluator.
- `tests/test_explainability_framework.py`: Automated verification suite.
- `data/reference/explainability_methodology.json`: Serialized methodology specification.
