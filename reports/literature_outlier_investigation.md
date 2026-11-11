# Literature Outlier Investigation: High-Error Residual Case Studies

## 1. Overview & Forensic Objective
In small-sample solid-state machine learning, outliers represent invaluable physical signatures rather than mere noise. This investigation traces every test device exhibiting an out-of-fold residual $|e_i| \ge 0.35\,\text{dex}$ ($> 2.2\times$ multiplicative factor error) back to primary experimental literature.

## 2. Detailed Case Studies

### Case Study 1: 1T-MoS2 Contact (SRC-EXP-2014-KAPPERA)
- **Citation:** Kappera et al., Nature Materials 13, 1128–1134 (2014)
- **Paper Title:** *Phase-engineered low-resistance contacts to monolayer 2D semiconductors*
- **DOI:** [10.1038/nmat4080](https://doi.org/10.1038/nmat4080)
- **Observed $R_c$:** $240.0\ \Omega\cdot\mu\mathrm{m}$
- **Predicted $R_c$:** $616.2\ \Omega\cdot\mu\mathrm{m}$
- **Residual:** `$-0.4095\ \mathrm{dex}$ (Multiplicative error: $2.57\times$)
- **Fabrication Process:** Chemical phase transition via n-butyl lithium immersion converting 2H semiconducting MoS2 into metallic 1T phase
- **Contact Geometry:** 1T-metallic/2H-semiconducting atomically continuous 2D planar homojunction
- **Extraction Method:** Transfer Length Method (TLM) with varied contact spacings (0.5 - 5 um)
- **Characterization Environment:** Room temperature ambient and vacuum probe station
- **Physical Root Cause:** The 1T metallic phase homojunction eliminates the van der Waals tunnel barrier entirely, providing an atomically seamless covalent transition with near-unity carrier transmission. Standard regularized models predict Rc ~ 616 Ohm*um, but the seamless atomic transition achieves 240 Ohm*um, resulting in a negative residual (-0.41 dex, model overprediction).
- **Classification:** `Uncaptured atomic interface physics (covalent 2D homojunction vs 3D/2D heterojunction)`
- **Recommended Future Feature:** `Binary feature: 'is_phase_engineered_homojunction'`

### Case Study 2: Pt Contact (SRC-EXP-2018-LIU)
- **Citation:** Liu et al., Nature 557, 696–700 (2018)
- **Paper Title:** *Approaching the Schottky-Mott limit in van der Waals metal-semiconductor junctions*
- **DOI:** [10.1038/s41586-018-0129-8](https://doi.org/10.1038/s41586-018-0129-8)
- **Observed $R_c$:** $64998.0\ \Omega\cdot\mu\mathrm{m}$
- **Predicted $R_c$:** $25995.6\ \Omega\cdot\mu\mathrm{m}$
- **Residual:** `$0.398\ \mathrm{dex}$ (Multiplicative error: $2.5\times$)
- **Fabrication Process:** Mechanical transfer of pre-fabricated, ultra-flat Pt contact stripes onto monolayer MoS2 without high-energy evaporation damage
- **Contact Geometry:** Top-contact pristine van der Waals interface
- **Extraction Method:** Four-probe Transfer Length Method (TLM) as a function of temperature (77K - 300K) and gate bias
- **Characterization Environment:** High vacuum cryostat (~10^-6 Torr)
- **Physical Root Cause:** Pt has a very high work function (~5.65 eV). In unpinned vdW junctions, this induces a massive electron Schottky barrier (Phi_B ~ 1.38 eV), driving the contact into extreme thermionic suppression. The model predicted 26.0 kOhm*um, but the measured resistance reached 65.0 kOhm*um (+0.40 dex underprediction). The discrepancy stems from high-field barrier lowering saturation and heavy effective mass of hole carriers.
- **Classification:** `Non-linear extreme barrier saturation (thermionic freeze-out)`
- **Recommended Future Feature:** `Non-linear barrier transmission term: exp(q*Phi_B / k_B*T)`

### Case Study 3: Pd Contact (SRC-EXP-2014-MCDONNELL)
- **Citation:** McDonnell et al., ACS Nano 8, 2880–2888 (2014)
- **Paper Title:** *Defect-dominated doping and contact resistance in MoS2*
- **DOI:** [10.1021/nn500044q](https://doi.org/10.1021/nn500044q)
- **Observed $R_c$:** $12000.5\ \Omega\cdot\mu\mathrm{m}$
- **Predicted $R_c$:** $4998.0\ \Omega\cdot\mu\mathrm{m}$
- **Residual:** `$0.3804\ \mathrm{dex}$ (Multiplicative error: $2.4\times$)
- **Fabrication Process:** Direct thermal evaporation of Pd onto mechanically exfoliated MoS2 flakes without chemical passivation
- **Contact Geometry:** Conventional 3D evaporated top contact
- **Extraction Method:** In-situ X-ray Photoelectron Spectroscopy (XPS) coupled with 2-terminal/TLM electrical transport
- **Characterization Environment:** Ultra-High Vacuum (UHV, ~10^-10 Torr) and ambient re-exposure
- **Physical Root Cause:** Evaporating high-melting-point Pd directly onto unpassivated MoS2 generates substantial sulfur vacancy defect clusters. These mid-gap defects pin the Fermi level rigidly near 0.35 eV below the conduction band and create high localized scattering centers. The model predicted 5.0 kOhm*um based on ideal Pd work function, whereas experimental defect generation degraded Rc to 12.0 kOhm*um (+0.38 dex underprediction).
- **Classification:** `Defect-induced interfacial disorder (evaporation energy damage)`
- **Recommended Future Feature:** `Deposition method indicator ('evaporation' vs 'transfer')`

## 3. Synthesis: Model Shortcomings vs Uncaptured Experimental Degrees of Freedom
1. **Covalent 2D Homojunctions vs Heterojunctions:** Phase-engineered 1T-MoS2 contacts achieve lower resistance than any standard metal due to zero van der Waals gap and atomic continuity.
2. **Evaporation Damage & Defect Generation:** High-energy thermal deposition creates sulfur vacancy pinning centers that increase contact resistance by 2-3x relative to transferred pristine metals.
3. **Extreme Barrier Saturation:** High work-function metals (Pt) exhibit non-linear thermionic freeze-out that slightly exceeds linear log-scale models.
