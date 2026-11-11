# Sprint 6.a.3 Log: Document Model Limitations, Physical Validity Envelopes, and Literature Gaps

## 1. Sprint Objective
Critically evaluate the boundaries, operational envelopes, and empirical biases of the developed machine learning framework and closed-form physical equations. Specifically:
- Identify literature biases and dataset sparsity across device parameters (e.g., n-type vs p-type, temperature, geometry).
- Define hard physical validity envelopes beyond which model extrapolation fails due to physical breakdown mechanisms.
- Outline 5 concrete experimental campaigns needed from the 2D semiconductor community to close current knowledge gaps.

---

## 2. Findings & Physical Validity Boundaries

### 2.1. Hard Physical Validity Envelopes
1. **Gate Carrier Accumulation ($n_{2D} \in [10^{11}, 3.0 \times 10^{13}]\,\text{cm}^{-2}$):**
   - *Lower Bound Failure ($< 10^{11}\,\text{cm}^{-2}$):* Subthreshold channel pinch-off where channel sheet resistance completely swamps contact resistance.
   - *Upper Bound Failure ($> 3.0 \times 10^{13}\,\text{cm}^{-2}$):* Dielectric breakdown via Fowler-Nordheim oxide rupture, rendering gate electrostatics inoperable.
2. **Schottky Barrier Height ($\Phi_B \in [0.0, 1.20]\,\text{eV}$):**
   - *Lower Bound ($0.0\,\text{eV}$):* Reaches the Landauer-Sharvin quantum ballistic lower bound ($18 - 36\,\Omega\cdot\mu\text{m}$); negative extrapolated barrier heights are unphysical.
   - *Upper Bound ($> 1.20\,\text{eV}$):* Complete carrier freeze-out where thermionic-field current falls below instrument noise floors ($R_c > 10^7\,\Omega\cdot\mu\text{m}$).
3. **Thermal Processing Budget:**
   - Bismuth ($T_{\text{process}} < 240^\circ\text{C}$): Low melting point leads to dewetting and droplet balling.
   - Metastable 1T-$\text{MoS}_2$ ($T_{\text{process}} < 100^\circ\text{C}$): Rapid thermal relaxation back to semiconducting 2H phase.
   - Reactive metals Ti/Sc ($T_{\text{process}} < 400^\circ\text{C}$): Severe metal-sulfur interdiffusion and irreversible chalcogen lattice disruption.

### 2.2. Literature Dataset Biases & Extraction Discrepancies
- **Severe N-Type Polarity Bias:** $>95\%$ of published 2D $\text{MoS}_2$ studies investigate electron conduction; p-type hole contacts are severely underrepresented.
- **Room-Temperature Concentration:** $90\%$ of reported data points are extracted at $300\,\text{K}$; low-temperature cryogenic activation measurements ($4\,\text{K} - 77\,\text{K}$) are scarce.
- **Extraction Protocol Variance:** De-embedding contact resistance via TLM vs Y-function vs four-probe introduces an estimated $\pm 0.15 - 0.25\,\text{dex}$ systematic variance across independent research groups.

### 2.3. Targeted Community Experimental Agenda
1. *P-Type Contact Benchmark:* High-work-function metals under strong hole accumulation ($V_{gs} < -2\,\text{V}$ with ALD $\text{HfO}_2$).
2. *Cryogenic TLM Temperature Sweeps:* Validate Ohmic vs tunneling behavior down to $4\,\text{K}$.
3. *Sub-20 nm Physical Contact Scaling:* Quantify current crowding and transfer length limits at IRDS-relevant dimensions.
4. *Standardized Extraction Cross-Validation:* Multi-method verification on identical lithographic test structures.
5. *Ambient Aging and Reliability Kinetics:* 1000-hour stress testing at $85^\circ\text{C}$ / $85\%$ RH with barrier passivation.

---

## 3. Key Deliverables
- `src/physics/limitations_and_gaps_analyzer.py`: Systematic bias auditor and validity envelope generator.
- `tests/test_limitations_and_gaps_analyzer.py`: Comprehensive test suite verifying envelope definitions, rankings, and reporting.
- `data/reference/dataset_limitations_and_validity_envelopes.json`: Machine-readable validity bounds and experimental roadmap.
- `reports/dataset_limitations_and_future_experiments.md`: Full technical report on validity bounds and experimental gaps.
- `reports/figures/dataset_sparsity_and_gaps_radar.png`: Polar radar chart visualizing coverage vs unexplored domains.

---

## 4. Verification & Status
- Unit tests: 100% passing.
- Output artifacts verified on disk.
- Completed Sprint 6.a.3.
