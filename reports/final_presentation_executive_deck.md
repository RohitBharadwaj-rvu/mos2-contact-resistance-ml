# Executive Presentation Deck: $\text{MoS}_2$ Contact Resistance & Schottky Barrier Height ML Project

---

## Slide 1: Title & Executive Overview
### Decoupling and Predicting Contact Resistance in 2D $\text{MoS}_2$ Transistors via Physics-Informed Machine Learning and Symbolic Regression
- **Author:** Rohit Bharadwaj
- **Project Domain:** Semiconductor Physics, 2D Nanoelectronics, Interpretable ML
- **GitHub Repository:** [mos2-contact-resistance-ml](https://github.com/RohitBharadwaj-rvu/mos2-contact-resistance-ml)
- **Kaggle Benchmark Dataset:** [`rohitajitbharadwaj/mos2-contact-resistance-benchmark`](https://www.kaggle.com/datasets/rohitajitbharadwaj/mos2-contact-resistance-benchmark)
- **Key Target:** Bridge data-driven learning with solid-state transport physics to achieve the IRDS target: $R_c < 100\,\Omega\cdot\mu\text{m}$.

---

## Slide 2: The Core Technological Challenge
- **Silicon Scaling Wall:** Below $3\,\text{nm}$, Silicon suffers catastrophic quantum tunneling leakage and DIBL.
- **The 2D Promise:** Monolayer $\text{MoS}_2$ ($0.65\,\text{nm}$ body thickness) enables ultimate electrostatic channel control.
- **The Contact Bottleneck:**
  - Standard thermal evaporation causes severe kinetic damage, generating sulfur vacancies ($V_S$) and Metal-Induced Gap States (MIGS).
  - Strong Bardeen Fermi-level pinning ($S \approx 0.15 - 0.28$) keeps contact resistance high ($10^3 - 10^5\,\Omega\cdot\mu\text{m}$).
  - Literature data conflates work function, chemical reactivity, gating, and transfer techniques.

---

## Slide 3: Master Curated Benchmark Dataset
- **FAIR-Compliant Benchmark:** 20 experimental device instances extracted from 13 high-impact publications (Nature, Nature Materials, Nano Letters, ACS Nano).
- **Comprehensive Feature Vector:** 44 physically annotated descriptors:
  - Band alignment ($\Phi_B, W_M, \chi_{\text{MoS}_2}$, pinning index)
  - Electrostatic state ($n_{2D}$, gate oxide dielectric constant $\kappa$, thickness $t_{\text{ox}}$, EOT)
  - Interfacial chemistry ($\Delta H_f$ sulfide formation enthalpy, atomic bonding radii)
  - Deposition architecture (van der Waals lamination vs 3D thermal evaporation)
- **Open Access Release:** Published under CC-BY-4.0 with complete machine-readable ontology (`data_dictionary.json`).

---

## Slide 4: Rigorous Grouped Cross-Validation Protocol
- **The Leakage Danger:** Random train/test splits leak identical fabrication artifacts from the same research groups, yielding artificially inflated metrics.
- **Grouped Cross-Validation (`GroupKFold`, $k=5$):**
  - Grouped strictly by `source_uid` (paper origin).
  - Complete zero-leakage guarantee: test folds contain only unseen experimental papers.
- **Multi-Objective Composite Selection Score:**
  $$\text{Score} = 0.40(1 - \min(1, \text{RMSE})) + 0.35\max(0, \rho) + 0.25 C - 0.05\max(0, P - 4)$$
  Penalizes unnecessary feature complexity while rewarding rank preservation.

---

## Slide 5: Comprehensive Model Leaderboard & Performance
| Architecture | Out-of-Fold RMSE | Spearman $\rho$ | Kendall $\tau$ | Composite Score | Physical Monotonicity |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tuned Ridge Regression** | **0.2260 dex** | **0.9489** | **0.8316** | **0.8720** | **100% Monotonic** |
| **Tuned ElasticNet** | 0.2277 dex | 0.9489 | 0.8316 | 0.8710 | 100% Monotonic |
| **Gradient Boosting Regressor** | 0.3838 dex | 0.9023 | 0.7474 | 0.7870 | Constrained |
| **HistGradientBoosting (Constrained)** | 0.3871 dex | 0.9023 | 0.7474 | 0.7830 | 100% Monotonic |
| **Gaussian Process (Matérn 5/2)** | 0.3904 dex | 0.8872 | 0.7368 | 0.7781 | Smooth Kernel |
| **Discovered Closed-Form Law** | **0.3859 dex** | **0.8887** | **0.7444** | **0.7751** | **Analytical Physics** |

---

## Slide 6: Genetic Programming Discovered Physical Contact Law
- Using symbolic regression across 4 complexity tiers, we discovered a simple, elegant closed-form formula without human intervention:
  $$\log_{10}\left(R_c / [\Omega\cdot\mu\text{m}]\right) \approx \Phi_B / [\text{eV}] - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) + 3.660$$
  $$R_c \approx 4570 \cdot 10^{\Phi_B - (n_{2D}/10^{13})}\quad [\Omega\cdot\mu\text{m}]$$
- **Theoretical Validation:**
  - Conforms to monotonic physical laws: $\frac{\partial R_c}{\partial \Phi_B} > 0$, $\frac{\partial R_c}{\partial n_{2D}} < 0$.
  - At $\Phi_B = 0\,\text{eV}$ and $n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$, yields $R_c = 45.7\,\Omega\cdot\mu\text{m}$, respecting the Landauer-Sharvin quantum ballistic lower bound ($12.8\,\Omega\cdot\mu\text{m}$) with a $3.57\times$ phonon-scattering margin.

---

## Slide 7: Mechanism Decoupling & Explainability
- **Cross-Architecture SHAP Consensus:**
  - $\Phi_B$ and $n_{2D}$ account for **$84.9\%$** of predictive power.
  - 100% sign agreement across all 6 model architectures.
- **ANOVA Variance Decomposition:**
  - **Intrinsic Semiconductor Physics ($\Phi_B, n_{2D}$):** Explains **$87.1\%$** of total empirical variance.
  - **Extrinsic Fabrication Factors ($\delta_{\text{vdW}}, \Delta H_f$):** Explains **$6.0\%$**.
  - **Unexplained Noise:** Bounded at **$6.9\%$** ($\sigma \approx 0.18\,\text{dex} \approx 1.5\times$).
- **The vdW Multiplier:** Van der Waals transfer provides an intrinsic $10^{-0.366} \approx 0.43\times$ ($> 2.3\times$) resistance reduction independently of the metal chosen.

---

## Slide 8: Causal Mediation Analysis of Interfacial Chemistry
- **The Puzzle:** Why do reactive metals (Ti, Sc) with large sulfide formation enthalpy ($\Delta H_f$) exhibit lower contact resistance?
- **Causal Path Decomposition (Baron-Kenny / Preacher-Hayes):**
  - **Indirect Path (Barrier Reduction):** **$90.7\%$** ($a \cdot b = -0.4655$).
  - **Direct Path (Orbital Overlap):** **$9.3\%$** ($c' = -0.0478$).
- **Conclusion:** Reactive metals act primarily by forming conductive interfacial sub-sulfides that de-pin the Fermi level closer to the conduction band, rather than through direct wave-function overlap alone.

---

## Slide 9: 2D Transport Regime Phase Mapping
- **Four Delineated Operating Regimes:**
  1. *Regime I: Ballistic / Quantum-Limited ($R_c < 200\,\Omega\cdot\mu\text{m}$)* - Transferred semimetals (Bi, Sb), 1T homojunctions.
  2. *Regime II: Thermionic-Field Tunneling ($200 - 1500\,\Omega\cdot\mu\text{m}$)* - Evaporated and annealed Ti/Au, Sc, Ag.
  3. *Regime III: Thermionic Emission ($1500 - 15000\,\Omega\cdot\mu\text{m}$)* - Evaporated Au, Ni, Cr.
  4. *Regime IV: Defect-Pinned ($R_c > 15000\,\Omega\cdot\mu\text{m}$)* - High-damage unpassivated contacts (Pt, Pd).
- **White Space Identification:** Discovered experimental vacancy in high-accumulation p-type contacts and zero-barrier thick-substrate configurations.

---

## Slide 10: Quantitative Sub-100 $\Omega\cdot\mu\text{m}$ Design Rules
- Inverting the closed-form contact law yields the **Maximum Tolerable Schottky Barrier Height**:
  $$\Phi_{B,\max} = \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) - 1.660\quad [\text{eV}]$$
- **Technological Thresholds:**
  - Back-gated $\text{SiO}_2$ ($n_{2D} \le 1.0 \times 10^{13}\,\text{cm}^{-2}$): Sub-100 $\Omega\cdot\mu\text{m}$ is **physically impossible**.
  - High-$\kappa$ $\text{HfO}_2$ ($n_{2D} = 1.8 \times 10^{13}\,\text{cm}^{-2}$): Requires $\Phi_B \le 0.14\,\text{eV}$ (Achieved by Bi/Sb semimetals).
  - High-$\kappa$ $\text{HfO}_2$ ($n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$): Requires $\Phi_B \le 0.34\,\text{eV}$ (Achieved by annealed Ti/Au).

---

## Slide 11: Experimental Parameter Return-on-Investment (ROI)
- **Tier 1 (Top Priority):**
  - Gate Dielectric EOT Scaling ($\Delta \log_{10} R_c = 1.50\,\text{dex} = \mathbf{31.6\times\ \text{reduction}}$).
  - Schottky Barrier Height Engineering ($\Delta \log_{10} R_c = 0.85\,\text{dex} = \mathbf{7.1\times\ \text{reduction}}$).
- **Tier 2 (Major Enhancer):**
  - Van der Waals Transfer Lamination ($\mathbf{2.3\times\ \text{reduction}}$).
  - Interfacial Reaction Enthalpy & Annealing ($\mathbf{1.8\times\ \text{reduction}}$).
- **Tier 4 (Wasted Effort):**
  - Metal Pad Thickness ($> 20\,\text{nm}$) & Bulk Metal Resistivity ($\mathbf{< 1.05\times\ \text{effect}}$).

---

## Slide 12: Verified Live Interactive Dashboard & Summary
- **Full-Stack Application:** Python Flask + HTML5/CSS interactive dashboard (`src/dashboard/app.py`).
- **Live Verification:** Verified on `http://127.0.0.1:5050` with automated Playwright headless screenshot (`reports/figures/dashboard_live_screenshot.png`).
- **Complete Open-Source Ecosystem:**
  - 175+ automated unit tests across 38 modules with 100% green pass rate.
  - Reproducible CLI: `python -m src.pipeline.contact_predictor_pipeline --metal Bi --n2d 1.8e13 --vdw`.
  - Comprehensive reports, figures, and publication-ready artifacts archived in Git and Kaggle.
