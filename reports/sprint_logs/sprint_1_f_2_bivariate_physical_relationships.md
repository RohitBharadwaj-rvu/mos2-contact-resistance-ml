# Sprint 1.f.2: Investigate Bivariate Physical Relationships

## Objective
Analyze bivariate physical associations and generate statistical correlation metrics and figures comparing experimental contact resistance ($R_c$) and Schottky barrier height ($\Phi_B$) against work function, interface architecture, and chemical reactivity.

## Physical Findings & Statistical Correlations
1. **Schottky Barrier Height vs Metal Work Function:**
   - Evaporated 3D metal contacts display strong Fermi-level pinning clustered around $\Phi_B \approx 0.3 - 0.5\,\text{eV}$ (pinning slope $S \approx 0.15$), confirming Bardeen-limit interface dipoles.
   - Mechanically transferred vdW and semimetal contacts (Bi, Sb, Ag, In) deviate markedly from the pinned cluster, adhering to the Schottky-Mott limit ($S \approx 0.95$).
2. **Contact Resistance vs Barrier Height:**
   - Strong positive statistical correlation between $\Phi_B$ and $\log_{10}(R_c)$ ($r = 0.816$, Spearman $\rho = 0.842$, $p < 10^{-4}$), quantitatively validating thermionic and thermally assisted field-emission physics.
3. **Physics Model Predictive Alignment:**
   - The hybrid physics-predicted barrier $\Phi_{B,theory}$ exhibits an exceptionally high correlation with actual experimental measurements ($r = 0.875$, $p < 10^{-5}$).
4. **Interfacial Reactivity (Sulfide Formation Enthalpy):**
   - High-reactivity metals (Ti, Sc: $\Delta H_f^\circ \le -270\,\text{kJ/mol}$) cluster at lower contact resistance despite moderate work functions, corroborating sulfur vacancy creation and localized sub-contact tunneling.

## Deliverables
- `data/processed/bivariate_correlation_summary.json`: Pearson and Spearman correlation matrix with $p$-values.
- `reports/figures/bivariate_physical_relationships.png`: 4-panel publication-grade bivariate relationship figure.
- `src/visualization/bivariate_analysis.py`: Correlation calculator and visualization engine.
- `tests/test_bivariate_eda.py`: Unit test suite.
