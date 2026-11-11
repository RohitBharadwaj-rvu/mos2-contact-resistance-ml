# Sprint 5.a.2 Log: Permutation Importance, Partial Dependence (PDP), and ICE Curves

## 1. Objectives & Methodological Framework
- Compute model-agnostic out-of-fold permutation feature importance across paper-grouped 5-fold cross-validation (`GroupKFold(n_splits=5, groups=source_uid)`).
- Generate 1D Partial Dependence Plots (PDP) paired with Individual Conditional Expectation (ICE) curves for continuous descriptors ($n_{2D}$, $\Phi_B$, $\Delta H_f$).
- Map the 2D Partial Dependence interaction surface across the carrier density $\times$ Schottky barrier height space ($n_{2D} \times \Phi_B$).
- Output publication-quality diagnostic graphics:
  1. `reports/figures/permutation_importance_oof.png`
  2. `reports/figures/pdp_ice_curves.png`
  3. `reports/figures/pdp_2d_interaction_surface.png`

## 2. Permutation Feature Importance Results (Grouped Out-of-Fold)

| Feature | Solid-State Role | Mean $\Delta\text{RMSE}$ (dex) | Std $\Delta\text{RMSE}$ | Relative Importance |
| :--- | :--- | :--- | :--- | :--- |
| **`physics_predicted_sbh_ev`** | Schottky Barrier Height ($\Phi_B$) | **$+0.2747$** | $0.1420$ | **$55.6\%$** |
| **`gate_carrier_density_cm2`** | Gate Carrier Density ($n_{2D}$) | **$+0.1449$** | $0.0803$ | **$29.3\%$** |
| **`is_vdw_or_depinned_contact`** | van der Waals / De-pinning ($\delta_{\text{vdW}}$) | **$+0.0612$** | $0.0301$ | **$12.4\%$** |
| **`sulfide_formation_enthalpy_kj_mol`** | Interfacial Reactivity ($\Delta H_f$) | **$+0.0137$** | $0.0052$ | **$2.8\%$** |

## 3. Physical Insights from PDP and ICE Analysis
1. **Model-Agnostic Validation of Primary Drivers:**
   - Scrambling $\Phi_B$ on unseen validation papers causes out-of-fold RMSE to jump from $0.226\,\text{dex}$ to $> 0.501\,\text{dex}$ (more than doubling prediction error). This confirms that barrier height is the single most critical governing descriptor.
   - Gating ($n_{2D}$) provides the secondary stabilizing control ($29.3\%$), capable of compressing contact resistance by over an order of magnitude across the achievable gating window.
2. **Individual Conditional Expectation (ICE) Homogeneity:**
   - Across all 20 devices, the ICE response trajectories for both $n_{2D}$ and $\Phi_B$ are parallel and strictly monotonic, demonstrating absence of hidden pathological interactions or localized counter-physical gradient inversions.
3. **2D Interaction Surface Dynamics:**
   - In the $n_{2D} \times \Phi_B$ contour space, low contact resistance ($R_c < 100\,\Omega\cdot\mu\text{m}$, or $< 2.0\,\text{dex}$) is confined strictly to the high-density ($n_{2D} > 1.2 \times 10^{13}\,\text{cm}^{-2}$), low-barrier ($\Phi_B < 0.2\,\text{eV}$) quadrant.

## 4. Implemented Deliverables
- `src/interpretability/pdp_ice_analyzer.py`: Complete permutation importance, 1D PDP+ICE, and 2D interaction engine.
- `tests/test_pdp_ice_analyzer.py`: Unit test suite covering permutation calculations, grid evaluations, and figure persistence.
- `data/processed/pdp_and_permutation_importance.json`: Full numerical dataset of permutation impacts and PDP coordinates.
- Figures: `permutation_importance_oof.png`, `pdp_ice_curves.png`, `pdp_2d_interaction_surface.png`.

## 5. Verification
- `python -m pytest tests/test_pdp_ice_analyzer.py` passed (3/3 green).
