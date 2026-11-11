# Sprint 6.a.2 Log: Actionable Laboratory Recommendations and Parameter ROI Ranking

## 1. Sprint Objective
Translate machine learning feature attributions, causal path coefficients, and regime phase diagrams into concrete, actionable engineering guidelines for experimentalists. Specifically:
- Rank materials and fabrication parameters by their true Return-on-Investment (ROI) in reducing contact resistance.
- Distinguish high-impact fabrication levers from common laboratory practices that produce negligible return.
- Formulate a 4-step decision hierarchy for designing sub-$100\,\Omega\cdot\mu\text{m}$ contacts.

---

## 2. Experimental Parameter Return-on-Investment (ROI) Hierarchy

| Tier | Parameter | Typical Laboratory Variation | Max Resistance Impact | Practical Engineering Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Essential Priority** | **Gate Dielectric EOT / Capacitance** | $90\,\text{nm}\ \text{SiO}_2 \to 3\,\text{nm}\ \text{HfO}_2$ | **$1.50\,\text{dex}$ ($31.6\times$)** | **Top Priority:** Replace thick thermal oxide with high-$\kappa$ ALD dielectrics. Increasing carrier accumulation to $n_{2D} > 1.8 \times 10^{13}\,\text{cm}^{-2}$ is essential to achieve low $R_c$. |
| **Tier 1: Essential Priority** | **Schottky Barrier Height ($\Phi_B$)** | $\text{Pt/Au}\ (0.7\,\text{eV}) \to \text{Bi}\ (0.05\,\text{eV})$ | **$0.85\,\text{dex}$ ($7.1\times$)** | Select semimetals (Bi, Sb) or reactive low-work-function metals (Sc) to eliminate the thermal activation barrier. |
| **Tier 2: Major Enhancer** | **Deposition Damage / vdW Transfer** | E-beam evaporation $\to$ vdW lamination | **$0.37\,\text{dex}$ ($2.3\times$)** | Eliminate energetic metal ion bombardment. Dry-transfer laminated pads preserve the chalcogen lattice and prevent deep defect states. |
| **Tier 2: Major Enhancer** | **Interfacial Enthalpy / Annealing** | Noble Au $\to$ Reactive Ti/Sc with anneal | **$0.25\,\text{dex}$ ($1.8\times$)** | For evaporated contacts, deploy vacuum forming gas annealing ($250-300^\circ\text{C}$) to induce conductive sub-sulfide de-pinning layers. |
| **Tier 3: Minor Modulator** | **Flake Layer Thickness** | $1\text{L}\ \text{monolayer} \to 3-5\text{L}\ \text{few-layer}$ | **$0.12\,\text{dex}$ ($1.3\times$)** | Few-layer flakes offer slightly narrower bandgaps and multiple subbands, but cannot compensate for poor gate electrostatics. |
| **Tier 4: Ineffective / Wasted Effort** | **Metal Pad Thickness ($> 20\,\text{nm}$)** | $20\,\text{nm} \to 100\,\text{nm}$ | **$0.02\,\text{dex}$ ($1.05\times$)** | **Do not waste material:** Beyond the continuous percolation threshold ($\sim 15\,\text{nm}$), pad sheet resistance is negligible compared to interfacial contact resistance. |
| **Tier 4: Ineffective / Wasted Effort** | **Bulk Metal Resistivity** | $\text{Ag}\ (1.6\,\mu\Omega\cdot\text{cm}) \to \text{Bi}\ (100\,\mu\Omega\cdot\text{cm})$ | **$0.01\,\text{dex}$ ($1.02\times$)** | Semimetals have $50\times$ higher bulk resistivity than silver, yet yield $10\times$ lower contact resistance due to interface de-pinning. Ignore bulk resistivity. |

---

## 3. Four-Step Laboratory Decision Hierarchy
1. **Step 1 (Dielectric Selection):** Choose thin high-$\kappa$ gate dielectric ($\text{HfO}_2, \text{ZrO}_2$ with $\text{EOT} < 1\,\text{nm}$) to enable electrostatic band-bending.
2. **Step 2 (Contact Material Selection):** Target zero-barrier semimetals (Bi, Sb) for lowest $R_c$, or reactive transition metals (Ti, Sc) for CMOS foundry compatibility.
3. **Step 3 (Deposition Process):** Use dry mechanical van der Waals stamping or low-energy UHV evaporation ($< 0.1\,\text{\AA/s}$) to suppress defect generation.
4. **Step 4 (Post-Metal Treatment):** Vacuum anneal reactive metals at $250-300^\circ\text{C}$ in $\text{Ar/H}_2$; immediately passivate semimetals with $10\,\text{nm}\ \text{Al}_2\text{O}_3$ to prevent ambient oxidation.

---

## 4. Key Deliverables
- `src/physics/experimental_recommendations_engine.py`: ROI calculator and decision tree synthesizer.
- `tests/test_experimental_recommendations_engine.py`: Unit test suite verifying ranking order, thresholds, and data export.
- `data/reference/experimental_optimization_matrix.json`: Machine-readable optimization matrix.
- `reports/figures/experimental_parameter_roi_ranking.png`: Horizontal bar chart illustrating return-on-investment across all fabrication levers.

---

## 5. Verification & Status
- Unit tests: 100% passing.
- Output artifacts verified.
- Completed Sprint 6.a.2.
