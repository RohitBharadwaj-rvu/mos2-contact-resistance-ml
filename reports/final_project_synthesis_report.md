# Physical Machine Learning and Closed-Form Decoupling of Contact Resistance and Schottky Barrier Height in Two-Dimensional $\text{MoS}_2$ Field-Effect Transistors

**Author:** Rohit Bharadwaj  
**Project GitHub Repository:** [mos2-contact-resistance-ml](https://github.com/RohitBharadwaj-rvu/mos2-contact-resistance-ml)  
**Kaggle Benchmark Dataset:** [`rohitajitbharadwaj/mos2-contact-resistance-benchmark`](https://www.kaggle.com/datasets/rohitajitbharadwaj/mos2-contact-resistance-benchmark)  
**Date:** November 2026  

---

## Abstract
Contact resistance ($R_c$) at metal–semiconductor interfaces remains the primary bottleneck hindering two-dimensional (2D) molybdenum disulfide ($\text{MoS}_2$) field-effect transistors (FETs) from reaching the International Roadmap for Devices and Systems (IRDS) target of $R_c < 100\,\Omega\cdot\mu\text{m}$ for sub-1nm logic nodes. In this project, we construct an end-to-end, physics-informed machine learning (ML) and symbolic regression framework to predict, decouple, and optimize contact resistance across 20 rigorously curated experimental devices spanning 13 landmark literature publications. Using paper-grouped cross-validation (`GroupKFold`, $k=5$) to prevent data leakage, we benchmark 9 model families, finding that tuned regularized linear models (Ridge/ElasticNet) achieve state-of-the-art predictive accuracy ($\text{RMSE} = 0.2260\,\text{dex}$, Spearman $\rho = 0.9489$, Kendall $\tau = 0.8316$). Through multi-tier genetic programming, we discover an analytical, closed-form scaling law:
$$R_c \approx 4570 \cdot 10^{\Phi_B - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right)}\quad [\Omega\cdot\mu\text{m}]$$
which maintains a physically realistic margin over the theoretical Landauer-Sharvin ballistic quantum lower bound ($12.8 - 18.1\,\Omega\cdot\mu\text{m}$). Variance decomposition via ANOVA reveals that intrinsic semiconductor electrostatics ($\Phi_B, n_{2D}$) account for **$87.1\%$** of empirical variance, while extrinsic processing factors ($\delta_{\text{vdW}}, \Delta H_f$) explain **$6.0\%$**, with unexplained noise bounded at **$6.9\%$**. Causal mediation path analysis further establishes that **$90.7\%$** of the contact enhancement provided by high-formation-enthalpy reactive metals is mediated indirectly through Schottky barrier height ($\Phi_B$) reduction rather than direct orbital hybridization. Finally, we establish a 4-regime transport taxonomy, delineate a 2D phase diagram, and invert the discovered scaling law to provide actionable quantitative design rules for experimentalists.

---

## 1. Introduction & Physical Motivation
Silicon CMOS scaling faces severe short-channel effects below the $3\,\text{nm}$ gate length node. Monolayer transition metal dichalcogenides (TMDs), particularly $\text{MoS}_2$, possess atomic sub-nanometer body thickness, an absence of dangling bonds, a pristine bandgap ($1.8\,\text{eV}$ for monolayer, $1.3\,\text{eV}$ for few-layer), and high immunity to drain-induced barrier lowering (DIBL).

However, the practical application of 2D $\text{MoS}_2$ in high-performance computing is severely throttled by parasitics:
1. **Fermi-Level Pinning:** Conventional thermal and e-beam evaporation of 3D metals creates high kinetic damage, inducing sulfur vacancies ($V_S$) and Metal-Induced Gap States (MIGS) that pin the Fermi level near $0.35 - 0.70\,\text{eV}$ below the conduction band edge ($S = d\Phi_B / dW_M \approx 0.15 - 0.28 \ll 1.0$).
2. **Contact Resistance Scaling:** Contact resistance in conventional back-gated devices remains $10^3 - 10^5\,\Omega\cdot\mu\text{m}$, orders of magnitude above the IRDS requirement of $R_c < 100\,\Omega\cdot\mu\text{m}$.
3. **Decoupling Challenge:** In laboratory literature, interfacial chemistry (formation enthalpy $\Delta H_f$), dielectric gating ($n_{2D}$), deposition method (van der Waals lamination vs evaporation), and metal work function ($W_M$) are conflated, obscuring the primary governing levers.

---

## 2. Master Curated Dataset & FAIR Packaging
A standardized, literature-curated benchmark dataset was assembled across 13 landmark peer-reviewed publications:
- Total Curated Devices: 20 experimental FET instances.
- Feature Dimensionality: 44 physically annotated and engineered columns.
- Metal Systems Covered: $\text{Bi}$, $\text{Sb}$, $\text{Ti}$, $\text{Sc}$, $\text{Ag}$, $\text{Au}$, $\text{Pt}$, $\text{Pd}$, $\text{Ni}$, and phase-engineered $1\text{T}-\text{MoS}_2$.
- Target Variables: $\log_{10}(R_c / [\Omega\cdot\mu\text{m}])$ and width-normalized $R_c$ ($\Omega\cdot\mu\text{m}$).
- FAIR Packaging: Completely packaged with machine-readable schemas (`data_dictionary.json`, `data_dictionary.md`), source citation registers (`source_provenance_registry.json`), and published openly to Kaggle under CC-BY-4.0: [`rohitajitbharadwaj/mos2-contact-resistance-benchmark`](https://www.kaggle.com/datasets/rohitajitbharadwaj/mos2-contact-resistance-benchmark).

---

## 3. Validation Strategy & Benchmark Model Leaderboard
To eliminate inter-paper contamination and over-optimistic cross-validation, models were evaluated strictly using **Grouped 5-Fold Cross-Validation (`GroupKFold`, $k=5$) grouped by `source_uid`**.

Models were ranked using a multi-objective composite fitness score balancing root mean square error (RMSE), rank correlation (Spearman $\rho$), concordance (Kendall $\tau$), and feature complexity penalties:
$$\text{Score} = 0.40(1 - \min(1, \text{RMSE})) + 0.35\max(0, \rho) + 0.25 C - 0.05\max(0, P - 4)$$

### Definitive Cross-Validated Model Leaderboard
| Rank | Model Architecture | CV RMSE (dex) | Spearman $\rho$ | Kendall $\tau$ | Composite Score | Physical Consistency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | **Tuned Ridge Regression** | **0.2260** | **0.9489** | **0.8316** | **0.8720** | **100% Monotonic** |
| **2** | **Tuned ElasticNet** | 0.2277 | 0.9489 | 0.8316 | 0.8710 | 100% Monotonic |
| **3** | **Gradient Boosting Regressor** | 0.3838 | 0.9023 | 0.7474 | 0.7870 | Constrained |
| **4** | **HistGradientBoosting (Constrained)** | 0.3871 | 0.9023 | 0.7474 | 0.7830 | 100% Monotonic |
| **5** | **Gaussian Process (Matérn 5/2)** | 0.3904 | 0.8872 | 0.7368 | 0.7781 | Smooth Kernel |
| **6** | **Discovered Closed-Form Law** | **0.3859** | **0.8887** | **0.7444** | **0.7751** | **Analytical Physics** |
| **7** | LightGBM (Monotonic) | 0.4083 | 0.8647 | 0.7158 | 0.7556 | Constrained |
| **8** | Tuned Random Forest | 0.4187 | 0.8722 | 0.7263 | 0.7535 | Unconstrained Trees |
| **9** | Support Vector Regression (SVR) | 0.4172 | 0.8647 | 0.7053 | 0.7508 | RBF Kernel |

---

## 4. Discovered Closed-Form Physical Contact Law
Multi-objective symbolic regression across 4 complexity tiers generated a Pareto frontier balancing mathematical complexity against predictive accuracy.

The optimal formula on the Pareto frontier discovered without human bias is:
$$\log_{10}\left(R_c / [\Omega\cdot\mu\text{m}]\right) \approx \Phi_B / [\text{eV}] - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) + 3.660$$
$$R_c \approx 4570 \cdot 10^{\Phi_B - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right)}\quad [\Omega\cdot\mu\text{m}]$$

### Physical Validation of Discovered Equation:
1. **Schottky Barrier Sensitivity:** $\frac{\partial \log_{10} R_c}{\partial \Phi_B} = +1.00\,\text{dex/eV} > 0$ (Monotonically increasing resistance with barrier height).
2. **Electrostatic Gate Sensitivity:** $\frac{\partial \log_{10} R_c}{\partial (n_{2D}/10^{13})} = -1.00\,\text{dex} < 0$ (Every $10^{13}\,\text{cm}^{-2}$ accumulation cuts resistance by exactly $10\times$).
3. **Quantum Ballistic Floor Alignment:** At zero barrier ($\Phi_B = 0\,\text{eV}$) and peak gate accumulation ($n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$), the equation yields:
   $$R_c = 4570 \cdot 10^{-2.0} = 45.7\,\Omega\cdot\mu\text{m}$$
   This sits comfortably above the theoretical single-contact Landauer-Sharvin quantum ballistic lower bound ($12.8\,\Omega\cdot\mu\text{m}$), maintaining an ideal physical margin factor of $3.57\times$ to account for finite acoustic/optical phonon scattering.

---

## 5. Interpretability & Mechanism Decoupling

### 5.1. Cross-Architecture Feature Attributions (SHAP)
Cross-architecture SHAP analysis across linear, tree, and kernel models revealed unanimous agreement:
- **Schottky Barrier Height ($\Phi_B$):** Accounts for **$54.2\%$** of predictive attribution.
- **Gate Carrier Density ($n_{2D}$):** Accounts for **$30.7\%$** of predictive attribution.
- **Van der Waals Transfer Indicator ($\delta_{\text{vdW}}$):** Accounts for **$8.6\%$** of predictive attribution.
- **Interfacial Formation Enthalpy ($\Delta H_f$):** Accounts for **$6.5\%$** of predictive attribution.

### 5.2. Intrinsic Transport vs Extrinsic Processing Decoupling
Using ANOVA sum-of-squares decomposition on the total empirical log-variance ($\sigma^2_{\log_{10} R_c} = 0.4759\,\text{dex}^2$):
- **Intrinsic Physics ($\Phi_B, n_{2D}$):** Explains **$87.1\%$** ($0.4148\,\text{dex}^2$).
- **Extrinsic Fabrication ($\delta_{\text{vdW}}, \Delta H_f$):** Explains **$6.0\%$** ($0.0285\,\text{dex}^2$).
- **Unexplained Noise / Measurement Variability:** **$6.9\%$** ($0.0326\,\text{dex}^2$).
- **Key Insight:** Van der Waals transfer provides an intrinsic $10^{-0.366} \approx 0.43\times$ ($> 2.3\times$) resistance reduction across all metals, independent of metal work function.

### 5.3. Causal Mediation Path Analysis
Baron-Kenny / Preacher-Hayes mediation analysis decomposed the total causal effect of reactive metal formation enthalpy ($\Delta H_f$):
- Indirect path mediated through Schottky barrier reduction: **$90.7\%$** ($a \cdot b = -0.4655$).
- Direct path via orbital hybridization / tunnel barrier thinning: **$9.3\%$** ($c' = -0.0478$).
- **Scientific Conclusion:** Reactive metals like Ti and Sc do not lower contact resistance primarily through direct chemical bonding; rather, their chemical reaction consumes interfacial chalcogens, de-pinning the Fermi level closer to the conduction band.

---

## 6. Physical Transport Regimes & 2D Phase Diagrams
Devices in the 2D parameter space $(\Phi_B, n_{2D})$ are partitioned into four distinct physical transport regimes:
1. **Regime I: Ballistic / Quantum-Limited Regime ($R_c < 200\,\Omega\cdot\mu\text{m}$):**
   Governed by Landauer-Sharvin quantum transmission. Satisfied by transferred semimetals (Bi, Sb) and 1T metallic phase homojunctions with $\Phi_B < 0.15\,\text{eV}$ and $n_{2D} \ge 1.0 \times 10^{13}\,\text{cm}^{-2}$.
2. **Regime II: Thermionic-Field / Tunneling Regime ($200 - 1500\,\Omega\cdot\mu\text{m}$):**
   Governed by field-emission tunneling through an electrostatically compressed depletion width. Satisfied by annealed Ti/Au, Sc, Ag, and In.
3. **Regime III: Thermionic Emission Regime ($1500 - 15000\,\Omega\cdot\mu\text{m}$):**
   Governed by Richardson thermal activation over the barrier. Common in evaporated Au, Ni, Cr on back-gated $\text{SiO}_2$.
4. **Regime IV: Defect-Dominated / Fermi-Level Pinned Regime ($R_c > 15000\,\Omega\cdot\mu\text{m}$):**
   Severe Fermi-level pinning near mid-gap and defect hopping. Observed in unpassivated Pt, Pd, and damaged evaporates.

---

## 7. Quantitative Design Rules for Sub-100 $\Omega\cdot\mu\text{m}$ Contacts
Inverting the validated closed-form law gives the **Maximum Tolerable Schottky Barrier Height**:
$$\Phi_{B,\max} = \log_{10}(R_c^*) + \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) - 3.660\quad [\text{eV}]$$

For the IRDS target $R_c^* = 100\,\Omega\cdot\mu\text{m}$ ($\log_{10}(100) = 2.0$):
$$\Phi_{B,\max} = \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) - 1.660\quad [\text{eV}]$$

### Feasibility by Electrostatic Gating Geometry:
- Standard Back-Gate ($90\,\text{nm}\ \text{SiO}_2$, $n_{2D} = 5 \times 10^{12}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -1.16\,\text{eV}$ (**Physically Impossible**).
- Strong Back-Gate ($90\,\text{nm}\ \text{SiO}_2$, $n_{2D} = 1.0 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -0.66\,\text{eV}$ (**Physically Impossible**).
- High-$\kappa$ Top-Gate ($5\,\text{nm}\ \text{HfO}_2$, $n_{2D} = 1.5 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = -0.16\,\text{eV}$ (**Impossible without degenerate chemical doping**).
- Peak High-$\kappa$ Top-Gate ($3\,\text{nm}\ \text{HfO}_2$, $n_{2D} = 1.8 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = \mathbf{0.14\,\text{eV}}$ (**Achieved with Bi/Sb semimetals**).
- Peak High-$\kappa$ Top-Gate ($3\,\text{nm}\ \text{HfO}_2$, $n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$): $\Phi_{B,\max} = \mathbf{0.34\,\text{eV}}$ (**Achieved with annealed Ti/Au**).

### Laboratory Parameter Return-on-Investment (ROI) Hierarchy:
- **Tier 1 (Essential Priority, $> 5\times$ impact):** Gate dielectric EOT scaling ($31.6\times$ reduction) and Schottky barrier elimination ($7.1\times$ reduction).
- **Tier 2 (Major Enhancer, $1.5\times - 5\times$ impact):** Van der Waals lamination ($2.3\times$ reduction) and reactive vacuum annealing ($1.8\times$ reduction).
- **Tier 3 (Minor Modulator, $1.1\times - 1.5\times$ impact):** Flake thickness ($1.3\times$ reduction).
- **Tier 4 (Ineffective / Wasted Effort, $< 1.1\times$ impact):** Metal pad thickness ($> 20\,\text{nm}$) and bulk metal electrical resistivity.

---

## 8. Verified Interactive Web Dashboard
An interactive Flask/HTML5 dashboard was developed in `src/dashboard/app.py`, allowing experimentalists to dynamically evaluate contact performance, inspect Landauer bounds, and verify transport regimes.

The live dashboard was verified on `http://127.0.0.1:5050` with automated Playwright headless browser capture, producing verified live screenshot: `reports/figures/dashboard_live_screenshot.png` and artifact `dashboard_live_verification.png`.

---

## 9. Conclusion
This project successfully bridges data-driven machine learning with fundamental semiconductor physics. By rigorously enforcing grouped cross-validation, discovering closed-form Pareto-optimal scaling laws, and performing causal mediation analysis, we provide the 2D semiconductor community with a definitive, reproducible, and actionable roadmap for achieving sub-$100\,\Omega\cdot\mu\text{m}$ contacts for future sub-1nm CMOS technologies.
