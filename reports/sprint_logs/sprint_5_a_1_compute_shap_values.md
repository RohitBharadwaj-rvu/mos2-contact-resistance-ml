# Sprint 5.a.1 Log: Compute SHAP Values and Audit Physical Directionality

## 1. Objectives & Algorithmic Scope
- Compute exact, Tree, and Kernel SHAP values across all 6 shortlisted model architectures (`Ridge_Regression`, `ElasticNet`, `Gradient_Boosting`, `Random_Forest`, `Gaussian_Process_Matern`, `Support_Vector_Regression_RBF`).
- Audit the physical directionality of each solid-state descriptor against fundamental semiconductor physics.
- Compare SHAP feature importance hierarchies across linear, tree ensemble, and kernel paradigms.
- Generate publication figures:
  1. Multi-panel beeswarm summary plot (`reports/figures/shap_summary_beeswarm.png`).
  2. Clustered bar chart comparing feature attribution consensus (`reports/figures/shap_cross_architecture_comparison.png`).

## 2. Cross-Architecture SHAP Attribution Results

| Architecture | 1st Ranked Feature ($|\text{SHAP}|$) | 2nd Ranked Feature ($|\text{SHAP}|$) | 3rd Ranked Feature ($|\text{SHAP}|$) | 4th Ranked Feature ($|\text{SHAP}|$) |
| :--- | :--- | :--- | :--- | :--- |
| **Ridge Regression** | $n_{2D}$ ($0.2478\,\text{dex}$) | $\Phi_B$ ($0.1796\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.1671\,\text{dex}$) | $\Delta H_f$ ($0.0512\,\text{dex}$) |
| **ElasticNet** | $n_{2D}$ ($0.2611\,\text{dex}$) | $\Phi_B$ ($0.1989\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.1806\,\text{dex}$) | $\Delta H_f$ ($0.0509\,\text{dex}$) |
| **Gradient Boosting** | $n_{2D}$ ($0.3553\,\text{dex}$) | $\Phi_B$ ($0.1713\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.1649\,\text{dex}$) | $\Delta H_f$ ($0.1163\,\text{dex}$) |
| **Random Forest** | $n_{2D}$ ($0.4441\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.1092\,\text{dex}$) | $\Phi_B$ ($0.0753\,\text{dex}$) | $\Delta H_f$ ($0.0548\,\text{dex}$) |
| **Gaussian Process (Matérn)** | $n_{2D}$ ($0.2861\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.2183\,\text{dex}$) | $\Phi_B$ ($0.1882\,\text{dex}$) | $\Delta H_f$ ($0.0633\,\text{dex}$) |
| **Support Vector Regression** | $n_{2D}$ ($0.2921\,\text{dex}$) | $\Phi_B$ ($0.1582\,\text{dex}$) | $\delta_{\text{vdW}}$ ($0.1419\,\text{dex}$) | $\Delta H_f$ ($0.0594\,\text{dex}$) |

## 3. Physical Directionality Audit
Every single architecture yields 100% physically consistent directionalities:
1. **Gate Carrier Density ($n_{2D}$):** Consistently negative ($r < -0.80$). Electrostatic carrier accumulation thins the Schottky depletion barrier and enhances quantum tunneling.
2. **Schottky Barrier Height ($\Phi_B$):** Consistently positive ($r > +0.70$). Higher barrier height exponentially suppresses thermionic-field injection.
3. **van der Waals / De-pinning ($\delta_{\text{vdW}}$):** Consistently negative ($r < -0.50$). Pristine vdW contacts suppress Fermi-level pinning and decrease contact resistance.
4. **Sulfide Enthalpy ($\Delta H_f$):** Modest positive attribution ($r \sim +0.20$), indicating that highly reactive metals requiring large formation enthalpy produce localized defect pin-down unless passivated.

## 4. Implemented Deliverables
- `src/interpretability/shap_analyzer.py`: Multi-model SHAP attribution engine.
- `tests/test_shap_analyzer.py`: Unit test suite testing explainers and physical directionality checks.
- `data/processed/shap_feature_attribution_analysis.json`: Serialized SHAP values matrix and cross-architecture summaries.
- `reports/figures/shap_summary_beeswarm.png`: Multi-panel beeswarm plot.
- `reports/figures/shap_cross_architecture_comparison.png`: Clustered consensus attribution bar chart.

## 5. Verification
- `python -m pytest tests/test_shap_analyzer.py` passed (2/2 green).
