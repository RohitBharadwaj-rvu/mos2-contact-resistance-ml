# Sprint 1.f.3: Assess Feature Collinearity and Redundancy

## Objective
Compute statistical correlation matrices, identify pairwise collinearity ($|r| \ge 0.75$), calculate Variance Inflation Factors (VIF), and detect categorical co-occurrence across all input variables to guide dimensionality selection.

## Collinearity Findings & Multicollinearity Matrix
1. **Deterministic Linear Redundancies:**
   - $\Phi_M$ and $\Delta \Phi_{SM} = \Phi_M - 4.20$ have an exact linear correlation $r = 1.0$, which inflates VIF if included simultaneously in unregularized linear models.
   - `effective_pinning_factor_s` and `is_vdw_or_depinned_contact` have $r = 1.0$ (by definition).
2. **Physical Correlations:**
   - Pauling electronegativity $\chi_P$ strongly correlates with work function $\Phi_M$ ($r = 0.812$), conforming to Mulliken electronegativity theory ($\chi_M \propto \Phi_M + EA$).
   - Sulfide formation enthalpy $\Delta H_f^\circ$ correlates with d-band center position $\epsilon_d - E_F$ ($r = 0.768$), matching Hammer-Nørskov chemical bonding principles where d-band position controls reactivity.
3. **Modeling Strategy for Multicollinearity:**
   - For tree-based models (Gradient Boosting, LightGBM, Random Forest), colinear features do not degrade prediction accuracy.
   - For linear baselines and symbolic regression, we prioritize orthogonal descriptors: `work_function_ev`, `is_vdw_or_depinned_contact`, `sulfide_formation_enthalpy_kj_mol`, and `fermi_level_shift_ev`.

## Deliverables
- `data/processed/collinearity_vif_report.json`: VIF scores and pairwise high-correlation catalog.
- `reports/figures/feature_correlation_heatmap.png`: High-resolution annotated correlation heatmap.
- `src/features/collinearity_analyzer.py`: VIF and collinearity engine.
- `tests/test_collinearity_analyzer.py`: Unit test suite.
