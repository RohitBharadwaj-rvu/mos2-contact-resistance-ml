# Sprint 5.b.1 Log: Quantify Inter-Feature Confounding and Collinearity

## 1. Objectives & Methodological Protocol
- Quantify empirical collinearity, covariance, and confounding among key solid-state descriptors ($\Phi_B$, $n_{2D}$, $\delta_{\text{vdW}}$, $\Delta H_f$).
- Compute both raw (Pearson, Spearman) and conditioned partial correlation matrices using precision matrix pseudo-inverses.
- Compute Variance Inflation Factors (VIF) to assess multi-collinearity inflation risks.
- Identify the most entangled pairs of physical mechanisms in historical literature datasets.
- Produce comparative dual heatmap publication graphic (`reports/figures/confounding_partial_correlation_matrix.png`).

## 2. Statistical Collinearity & VIF Results

| Feature Descriptor | Solid-State Role | Variance Inflation Factor (VIF) | Collinearity Status |
| :--- | :--- | :--- | :--- |
| **`physics_predicted_sbh_ev`** | Schottky Barrier Height ($\Phi_B$) | **$1.295$** | Low / Well-conditioned |
| **`is_vdw_or_depinned_contact`** | van der Waals / De-pinning ($\delta_{\text{vdW}}$) | **$1.472$** | Low / Well-conditioned |
| **`sulfide_formation_enthalpy_kj_mol`** | Interfacial Sulfide Enthalpy ($\Delta H_f$) | **$1.273$** | Low / Well-conditioned |
| **`gate_carrier_density_cm2`** | Gate Carrier Accumulation ($n_{2D}$) | **$1.438$** | Low / Well-conditioned |

**Finding:** All VIF values are $< 1.50$ (far below the conservative danger threshold of $5.0$). This confirms that the 4-feature parsimonious descriptor subset selected in Section 2 mathematically eliminates severe multicollinearity while retaining full physical coverage.

## 3. Disentangling Entangled Mechanisms (Raw vs Partial Correlation)

| Feature Pair | Raw Pearson $r$ | Partial Correlation $r_{\text{cond}}$ | Confounding Delta $|\Delta r|$ | Physical Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **`vdW Flag` $\leftrightarrow$ `Sulfide Enthalpy`** | $+0.4282$ | $+0.4260$ | $0.0022$ | vdW contact metals (Bi, Sb, graphene) historically exhibit higher (less negative) formation enthalpies than 3D reactive transition metals (Ti, Sc). |
| **`Schottky Barrier` $\leftrightarrow$ `Gate Carrier Density`** | $-0.3777$ | $-0.3837$ | $0.0060$ | Experimental sampling bias: devices with high barrier heights were frequently measured under elevated back-gate bias to turn on channel conduction. |
| **`vdW Flag` $\leftrightarrow$ `Gate Carrier Density`** | $+0.3626$ | $+0.4357$ | $0.0731$ | Transferred vdW devices utilized thin high-$\kappa$ or clean $\text{SiO}_2$ substrates allowing higher gate induction before dielectric breakdown. |
| **`Schottky Barrier` $\leftrightarrow$ `Sulfide Enthalpy`** | $+0.2160$ | $+0.0401$ | **$0.1759$** | **Major Decoupling Result:** When conditioned on carrier density and vdW structure, the direct correlation between $\Phi_B$ and $\Delta H_f$ drops to near zero ($+0.04$). |

## 4. Implemented Deliverables
- `src/interpretability/confounding_analyzer.py`: Precision matrix computation, VIF evaluation, and comparative heatmap plotting.
- `tests/test_confounding_analyzer.py`: Unit test suite testing partial correlation bounds and VIF calculations.
- `data/processed/inter_feature_confounding_analysis.json`: Full numerical record of VIFs and correlation matrices.
- `reports/figures/confounding_partial_correlation_matrix.png`: Publication-grade dual correlation heatmap.

## 5. Verification
- `python -m pytest tests/test_confounding_analyzer.py` passed (2/2 green).
