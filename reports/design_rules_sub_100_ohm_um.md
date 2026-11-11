# Quantitative Design Rules for Sub-100 $\Omega\cdot\mu\mathrm{m}$ $\text{MoS}_2$ Contacts

## 1. Executive Summary & Governing Physical Design Equation
Based on systematic machine learning synthesis and validated symbolic discovery, contact resistance in monolayer and few-layer $\text{MoS}_2$ field-effect transistors is strictly bounded by the closed-form physical equation:

$$\log_{10}\left(R_c\ [\Omega\cdot\mu\mathrm{m}]\right) \approx \Phi_B\ [\mathrm{eV}] - \left(\frac{n_{2D}}{10^{13}\ \mathrm{cm}^{-2}}\right) + 3.660$$

Inverting this relationship yields the **Maximum Tolerable Schottky Barrier Height ($\Phi_{B,\max}$)** required to meet any target contact resistance $R_c^*$ at gate carrier accumulation $n_{2D}$:

$$\Phi_{B,\max} = \log_{10}\left(R_c^*\right) + \left(\frac{n_{2D}}{10^{13}\ \mathrm{cm}^{-2}}\right) - 3.660\quad [\mathrm{eV}]$$

## 2. Quantitative Threshold Matrix for Target $R_c < 100\ \Omega\cdot\mu\mathrm{m}$

| Electrostatic Gating Scenario | Carrier Density $n_{2D}$ | Max Tolerable $\Phi_B$ | Feasibility Status | Technological Solution |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Back-Gate (SiO2 90nm, Vgs=30V)** | $5.0e+12\ \mathrm{cm}^{-2}$ | **$0.00\ \mathrm{eV}$** | `IMPOSSIBLE` | Dielectric breakdown limit |
| **Strong Back-Gate (SiO2 90nm, Vgs=60V)** | $1.0e+13\ \mathrm{cm}^{-2}$ | **$0.00\ \mathrm{eV}$** | `IMPOSSIBLE` | Dielectric breakdown limit |
| **Thin High-k Top-Gate (HfO2 5nm, Vgs=2V)** | $1.5e+13\ \mathrm{cm}^{-2}$ | **$0.00\ \mathrm{eV}$** | `IMPOSSIBLE` | Dielectric breakdown limit |
| **Peak High-k Gating (HfO2 3nm, Vgs=3V)** | $2.0e+13\ \mathrm{cm}^{-2}$ | **$0.34\ \mathrm{eV}$** | `ACHIEVABLE` | Bi(0001) or 1T-MoS2 |
| **Ionic Liquid / Solid Electrolyte** | $2.5e+13\ \mathrm{cm}^{-2}$ | **$0.84\ \mathrm{eV}$** | `ACHIEVABLE` | Bi(0001) or 1T-MoS2 |

## 3. Technology Strategy Matrix by Operational Constraints

### Sub-1nm CMOS Node Ultra-High-Performance Logic (IRDS Target) (`< 100 Ohm*um`)
- **Recommended Contact Strategy:** Van der Waals transferred semimetal: Bismuth Bi(0001) or Antimony Sb(0001)
- **Interface Engineering:** Pristine physical transfer in inert glovebox (< 0.1 ppm O2/H2O) to prevent surface oxidation.
- **Gate Dielectric Stack:** Dual-gated geometry with high-k HfO2 or ZrO2 (EOT < 0.8 nm), providing n_2D >= 1.8e13 cm^-2.
- **Thermal Budget Limit:** Maintain T_processing < 240 deg C to prevent bismuth balling/dewetting.

### Standard Foundry CMOS Fab-Line Compatible Integration (`200 - 400 Ohm*um`)
- **Recommended Contact Strategy:** Low-work-function reactive transition metal: Titanium (Ti) or Scandium (Sc) with Au/Pt cap
- **Interface Engineering:** Ultra-high vacuum e-beam evaporation (< 10^-8 Torr) with slow initial deposition rate (0.1 A/s) to minimize kinetic impact damage.
- **Gate Dielectric Stack:** Back-gated SiO2 (30-50 nm) or Al2O3 top-gate, operating at n_2D >= 1.0e13 cm^-2.
- **Thermal Budget Limit:** Post-metal vacuum annealing at 250 - 300 deg C in Ar/H2 forming gas to induce mild interfacial sulfur reaction and reduce pinning.

### Cryogenic 2D Superconducting / Quantum Readout Electronics (4 K - 77 K) (`< 200 Ohm*um at 4 K`)
- **Recommended Contact Strategy:** Chemically converted 1T metallic phase MoS2 homojunction or Nb/MoS2 superconducting contact
- **Interface Engineering:** Local n-butyl lithium or laser-assisted phase transformation to eliminate Schottky barrier freeze-out entirely (Phi_B ~ 0 eV).
- **Gate Dielectric Stack:** h-BN encapsulated gate stack to suppress cryogenic charged impurity scattering.
- **Thermal Budget Limit:** Metastable 1T phase requires T < 100 deg C after chemical conversion to prevent relaxation back to 2H phase.

### Low-Temperature Flexible Polymer Substrates (PET, Polyimide) (`< 500 Ohm*um`)
- **Recommended Contact Strategy:** Transferred monolayer graphene or low-temperature silver Ag nanowires
- **Interface Engineering:** Dry stamping van der Waals lamination at room temperature.
- **Gate Dielectric Stack:** High-capacitance ion gel or ALD Al2O3 deposited at 120 deg C.
- **Thermal Budget Limit:** Strict limit T < 150 deg C to preserve organic substrate dimensional stability.

## 4. Key Experimental Checklist for Breaking $100\ \Omega\cdot\mu\mathrm{m}$
1. **Dielectric Thinning:** Replace $90\,\text{nm}\ \text{SiO}_2$ with high-$\kappa$ dielectric (e.g., $3\,\text{nm}\ \text{HfO}_2$ with $\text{EOT} < 1\,\text{nm}$) to induce $n_{2D} > 1.8 \times 10^{13}\,\text{cm}^{-2}$.
2. **Damage-Free Interface:** Abandon high-energy thermal/e-beam evaporation of 3D metals; deploy transfer-laminated semimetals (Bi, Sb) or chemical 1T phase transition.
3. **Atmospheric Exclusion:** Perform all transfer and characterization in UHV or sub-ppm inert environments to prevent moisture-induced sulfur vacancy defect creation.