# Sprint 5.c.3 Log: Quantitative Design Rules for Sub-100 $\Omega\cdot\mu\text{m}$ $\text{MoS}_2$ Contacts

## 1. Sprint Objective
Identify quantitative design rules, operational boundaries, and material/engineering guidelines (required gate carrier accumulation $n_{2D}$, maximum tolerable Schottky barrier height $\Phi_B$, van der Waals transfer requirements, dielectric specifications) necessary to break the sub-$100\,\Omega\cdot\mu\text{m}$ contact resistance barrier in 2D $\text{MoS}_2$ field-effect transistors.

---

## 2. Methodology & Implementation
1. **Mathematical Inversion of Discovered Closed-Form Law:**
   Utilizing the validated Pareto-optimal analytical contact resistance equation:
   $$\log_{10}(R_c / [\Omega\cdot\mu\text{m}]) \approx \Phi_B / [\text{eV}] - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) + 3.660$$
   We derive the closed-form threshold for maximum tolerable Schottky barrier height $\Phi_{B,\max}$ as a function of target resistance $R_c^*$ and gate carrier density:
   $$\Phi_{B,\max} = \log_{10}(R_c^*) + \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) - 3.660\quad [\text{eV}]$$

2. **Gating Regime Feasibility Evaluation:**
   Evaluated feasibility across 5 realistic electrostatic gating architectures:
   - Back-gate ($90\,\text{nm}\ \text{SiO}_2$, $n_{2D} = 5.0 \times 10^{12}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -1.16\,\text{eV}$ (Mathematically impossible; dielectric breakdown occurs before reaching sub-100 $\Omega\cdot\mu\text{m}$).
   - Back-gate ($90\,\text{nm}\ \text{SiO}_2$, $n_{2D} = 1.0 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -0.66\,\text{eV}$ (Impossible without aggressive chemical doping).
   - High-$\kappa$ Top-gate ($5\,\text{nm}\ \text{HfO}_2$, $n_{2D} = 1.5 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -0.16\,\text{eV}$ (Borderline quantum regime).
   - Peak High-$\kappa$ Top-gate ($3\,\text{nm}\ \text{HfO}_2$, $n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = \mathbf{0.34\,\text{eV}}$ (Fully achievable with van der Waals semimetals Bi or Sb).
   - Ionic Liquid / Electrolyte ($n_{2D} = 2.5 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = \mathbf{0.84\,\text{eV}}$ (Achievable even with conventional transition metals Ti/Au).

3. **Multi-Scenario Technology Playbook:**
   Structured 4 distinct technology matrices for experimentalists:
   - Scenario 1: Sub-1nm CMOS Node Ultra-High-Performance Logic (van der Waals Bi/Sb semimetals).
   - Scenario 2: Standard Foundry CMOS Fab-Line Compatible Integration (Ti/Sc reactive interfaces).
   - Scenario 3: Cryogenic Quantum Computing Readout (1T-metallic MoS2 / superconducting Nb).
   - Scenario 4: Flexible / Transparent Electronics (Graphene / Ag nanowires).

---

## 3. Key Deliverables
- `src/interpretability/design_rules_extractor.py`: Quantitative design rule threshold evaluator and recommendation generator.
- `tests/test_design_rules_extractor.py`: Comprehensive test suite verifying threshold logic, edge conditions, and reporting.
- `data/reference/design_rules_ultra_low_contact_resistance.json`: Machine-readable parameters, threshold tables, and scenario configs.
- `reports/design_rules_sub_100_ohm_um.md`: Standalone technical report detailing experimental checklists and technology strategies.

---

## 4. Verification & Status
- Unit tests: 100% passing.
- Output artifacts verified on disk.
- Completed Sprint 5.c.3.
