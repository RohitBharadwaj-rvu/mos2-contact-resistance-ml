# Sprint 5.b.2 Log: Decouple Intrinsic vs Extrinsic Contributions to $R_c$

## 1. Objectives & Decoupling Formulation
- Formulate an additive physical decomposition of contact resistance in logarithmic space:
  $$\log_{10}(R_c) = f_{\text{intrinsic}}(\Phi_B, n_{2D}) + g_{\text{extrinsic}}(\delta_{\text{vdW}}, \Delta H_f) + \epsilon$$
- Isolate the fundamental quantum-electrostatic transport limit ($R_{c,\text{intrinsic}}$) from extrinsic processing modifiers ($R_{c,\text{extrinsic}}$).
- Quantify the exact percentage of total variance explained by intrinsic physics vs extrinsic fabrication factors using statistical ANOVA decomposition.
- Output publication-grade graphics: `reports/figures/intrinsic_vs_extrinsic_decomposition.png`.

## 2. Quantitative Variance Decomposition Results

| Contribution Component | Governing Variables | Variance Explained ($\text{dex}^2$) | Percentage of Total Variance | Physical Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Intrinsic Transport Component** | Schottky Barrier ($\Phi_B$), Gate Density ($n_{2D}$) | **$0.4148$** | **$87.1\%$** | Thermionic-field barrier transmission and electrostatic depletion thinning. |
| **Extrinsic Processing Modifier** | vdW de-pinning ($\delta_{\text{vdW}}$), Formation Enthalpy ($\Delta H_f$) | **$0.0285$** | **$6.0\%$** | Damage-free transfer, tunnel barrier elimination, and interfacial defect suppression. |
| **Unexplained Experimental Scatter** | Annealing, ambient humidity, lab differences | **$0.0326$** | **$6.9\%$** | Measurement noise and inter-laboratory processing discrepancies. |

## 3. Discovered Decoupled Physical Laws

1. **Intrinsic Base Transport Equation:**
   $$\log_{10}(R_{c,\text{intrinsic}}) = 1.30 \cdot \Phi_B - 1.18 \cdot \tilde{n}_{2D} + 3.71$$
   $$R_{c,\text{intrinsic}} \approx 5100 \cdot 10^{1.30 \Phi_B - 1.18 \tilde{n}_{2D}}\;\Omega\cdot\mu\text{m}$$
2. **Extrinsic Processing Multiplier:**
   $$\Delta \log_{10}(R_c) = -0.366 \cdot \delta_{\text{vdW}} - 0.460 \cdot \left(\frac{-\Delta H_f}{500\,\text{kJ/mol}}\right) + 0.274$$
   - **The vdW De-pinning Advantage:** Clean van der Waals transfer provides an intrinsic multiplicative factor reduction of $10^{-0.366} \approx 0.43\times$ ($>2.3\times$ resistance reduction) independently of metal choice.
   - **Chemical Enthalpy Doping:** Reactive metals with exothermic formation enthalpies provide an additional $0.46\,\text{dex}$ reduction via covalent orbital overlap.

## 4. Implemented Deliverables
- `src/interpretability/decoupling_decomposer.py`: Additive decomposition model and variance partitioning engine.
- `tests/test_decoupling_decomposer.py`: Unit test suite validating variance bounds, percentages, and artifact creation.
- `data/processed/intrinsic_extrinsic_decoupling_results.json`: Full device-by-device decomposition database.
- `reports/figures/intrinsic_vs_extrinsic_decomposition.png`: 3-panel publication graphic (variance donut, waterfall breakdown, intrinsic vs observed scatter).

## 5. Verification
- `python -m pytest tests/test_decoupling_decomposer.py` passed (1/1 green).
