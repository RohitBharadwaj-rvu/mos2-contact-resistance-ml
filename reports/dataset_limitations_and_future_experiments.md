# Model Validity Envelopes, Dataset Limitations, and Future Experimental Roadmap

## 1. Executive Summary
While the machine learning models and discovered closed-form physical equations provide unprecedented accuracy ($\text{RMSE} = 0.226\,\text{dex}$) across curated literature benchmarks, their domain of validity is strictly bounded by the underlying physics and empirical sampling coverage of published 2D semiconductor literature.

## 2. Hard Physical Validity Envelopes

| Physical Parameter | Valid Model Envelope | Lower Bound Failure Mode | Upper Bound Failure Mode |
| :--- | :--- | :--- | :--- |
| **Gate Carrier Density ($n_{2D}$)** | $10^{11} - 3 \times 10^{13}\,\mathrm{cm}^{-2}$ | Subthreshold regime where current is dominated by channel thermionic barrier rather than contact resistance. | Dielectric breakdown (Fowler-Nordheim leakage and oxide rupture) in thin high-k gate stacks. |
| **Schottky Barrier Height ($\Phi_B$)** | $0.0 - 1.20\,\mathrm{eV}$ | Ohmic degenerate state bounded strictly by the Landauer-Sharvin quantum ballistic limit (~ 18-36 Ohm*um). | Complete carrier freeze-out where current drops below noise floor (Rc > 1e7 Ohm*um). |

### Thermal Budget Limits
- **Bismuth Semimetal:** T_process < 240 deg C (Bismuth dewetting and balling threshold).
- **1T Phase Mos2:** T_process < 100 deg C (Metastable 1T to 2H relaxation threshold).
- **Reactive Metals Ti Sc:** T_process < 400 deg C (Excessive metal-sulfur interdiffusion leading to MoS2 lattice destruction).

## 3. Literature Dataset Biases & Extraction Discrepancies
- Severe n-type bias: >95% of published 2D MoS2 studies investigate electron injection; p-type contacts remain severely under-characterized.
- Room-temperature bias: 90% of extracted Rc values are reported at 300 K; temperature-dependent activation curves (4 K - 300 K) are sparse.
- Contact geometry bias: Overwhelming focus on top-contact geometries; 1D edge contacts (e.g., via etched h-BN/graphene trenches) are rarely tabulated.
- Publication bias toward low Rc: Studies achieving poor contact (> 1e5 Ohm*um) frequently omit TLM de-embedding, skewing literature toward best-case devices.

## 4. Priority Roadmap for Future Laboratory Experiments

### Priority 1: Systematic P-Type Contact Benchmark on 2D MoS2
- **Scientific Rationale:** Complementary CMOS logic strictly requires high-performance p-FETs. Experimental validation with high work-function metals (Pt, Pd, Au) under high-k hole accumulation is essential.
- **Target Measurement Protocol:** TLM de-embedded Rc and Richardson activation SBH under hole accumulation (Vgs < -2 V with thin HfO2).

### Priority 2: Cryogenic Temperature-Dependent TLM (4 K - 300 K)
- **Scientific Rationale:** Decouple tunneling vs thermionic emission across the full temperature range. Freeze-out measurements will verify if zero-barrier Bi contacts remain Ohmic at 4 K.
- **Target Measurement Protocol:** Four-probe TLM contact resistance vs 1000/T to extract true zero-bias barrier height.

### Priority 3: Contact Scaling Down to Sub-20 nm Contact Length (Lc)
- **Scientific Rationale:** IRDS roadmap requires physical contact pitch < 40 nm. Characterize current crowding and transfer length scaling limits at ultra-scaled dimensions.
- **Target Measurement Protocol:** Rc vs Lc scaling from 10 nm to 500 nm to measure transmission length LT.

### Priority 4: Standardized Extraction Protocol Benchmark (TLM vs Y-Function)
- **Scientific Rationale:** Eliminate inter-lab extraction variance by conducting cross-methodology comparisons on the same identical physical device.
- **Target Measurement Protocol:** Simultaneous TLM, Y-function, and gated four-probe extraction on identical lithographic patterns.

### Priority 5: Air-Stability and Accelerated Lifetime Aging Analysis
- **Scientific Rationale:** Semimetal and 1T contacts degrade rapidly in ambient humidity. Quantify degradation kinetics and capping layer (ALD Al2O3, h-BN) effectiveness over 1000+ hours.
- **Target Measurement Protocol:** Time-dependent Rc drift under 85 deg C / 85% relative humidity stress testing.
