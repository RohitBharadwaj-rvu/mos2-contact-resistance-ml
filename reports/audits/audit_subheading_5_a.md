# Subheading 5.a Audit: Global & Local Feature Attribution

## 1. Executive Summary & Review Scope
This audit reviews Subheading 5.a across Sprints 5.a.1 and 5.a.2:
- **Sprint 5.a.1:** Exact, Tree, and Kernel SHAP attributions, beeswarm plotting, and physical directionality audit across 6 model architectures (`src/interpretability/shap_analyzer.py`).
- **Sprint 5.a.2:** Model-agnostic out-of-fold permutation importance, 1D Partial Dependence (PDP) with ICE curves, and 2D interaction surfaces (`src/interpretability/pdp_ice_analyzer.py`).

## 2. Audit Findings & Convergence Analysis

### 2.1 Consensus Between SHAP and Permutation Importance
- **SHAP Perspective (Local Derivative / Marginal Attribution):** Across all 6 candidate architectures, $n_{2D}$ produces the highest mean absolute SHAP value ($|\text{SHAP}| \approx 0.25 - 0.44\,\text{dex}$), closely followed by $\Phi_B$ ($0.17 - 0.20\,\text{dex}$) and $\delta_{\text{vdW}}$ ($0.11 - 0.22\,\text{dex}$).
- **Permutation Importance Perspective (Out-of-Fold Variance Destruction):** Scrambling $\Phi_B$ on unseen validation papers induces the single largest error surge ($\Delta\text{RMSE} = +0.2747\,\text{dex}$, accounting for **$55.6\%$** of total permutation impact), followed by $n_{2D}$ ($+0.1449\,\text{dex}$, **$29.3\%$**).
- **Consensus:** Together, barrier height ($\Phi_B$) and carrier density ($n_{2D}$) account for **$84.9\%$** of predictive variance in contact resistance, while van der Waals de-pinning contributes **$12.4\%$**.

### 2.2 Physical Sanity & ICE Homogeneity
- **Strict Directionality Match:** Every evaluated architecture confirmed 100% adherence to physical directionality:
  - $\frac{\partial R_c}{\partial \Phi_B} > 0$ (exponential barrier suppression).
  - $\frac{\partial R_c}{\partial n_{2D}} < 0$ (depletion barrier compression).
  - $\frac{\partial R_c}{\partial (\text{vdW})} < 0$ (Fermi-level de-pinning).
- **ICE Curve Parallelism:** Individual conditional expectation trajectories are monotonic and parallel across all 20 devices, demonstrating that the learned response is globally stable and free of spurious regional inversions.

## 3. Subheading 5.a Sign-Off
All attribution engines, unit tests, and publication visual assets (`shap_summary_beeswarm.png`, `shap_cross_architecture_comparison.png`, `permutation_importance_oof.png`, `pdp_ice_curves.png`, `pdp_2d_interaction_surface.png`) are verified and audited.
Subheading 5.a is approved. The project is cleared to proceed to **Subheading 5.b: Decoupling Analysis: Disentangling Confounded Mechanisms**.
