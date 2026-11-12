# Physical Machine Learning and Closed-Form Decoupling of Contact Resistance and Schottky Barrier Height in Two-Dimensional $\text{MoS}_2$ Field-Effect Transistors

**Author:** Rohit Bharadwaj  
**Project GitHub Repository:** [mos2-contact-resistance-ml](https://github.com/RohitBharadwaj-rvu/mos2-contact-resistance-ml)  
**Kaggle Benchmark Dataset (v2.0):** [`rohitajitbharadwaj/mos2-contact-resistance-benchmark`](https://www.kaggle.com/datasets/rohitajitbharadwaj/mos2-contact-resistance-benchmark)  
**Date:** November 2026 (Audit-Remediated Edition)  

---

## Abstract
Contact resistance ($R_c$) at metal–semiconductor interfaces is the primary technological bottleneck preventing two-dimensional (2D) molybdenum disulfide ($\text{MoS}_2$) field-effect transistors (FETs) from satisfying the International Roadmap for Devices and Systems (IRDS) threshold of $R_c < 100\,\Omega\cdot\mu\text{m}$ for sub-1nm CMOS logic nodes. Following an exhaustive scientific review, we implement an audit-remediated physical machine learning and empirical decoupling framework across **28 primary experimental device observations derived from 23 independent peer-reviewed literature publications**. Review-derived summary entries (Allain 2015) were traced back to primary publications (Radisavljevic 2011, Chuang 2014, Fontana 2013, Bampoulis 2014) and isolated to prevent fold contamination.

We formulate two distinct, un-biased prediction tasks:
1. **Task 1 (Primary Contact Resistance Prediction):** Predicts $R_c$ directly from 14 raw physical and experimental fabrication levers ($W_M$, Pauling electronegativity, sulfide enthalpy $\Delta H_f$, metal resistivity, vdW transfer indicator, chamber vacuum, annealing flag, annealing temperature, thermal budget, layer count, thickness, gate carrier density $n_{2D}$, EOT, and measurement temperature) with zero pre-baked pinning assumptions ($S=0.95/0.15$ removed).
2. **Task 2 (Schottky Barrier Height Prediction):** Predicts measured $\Phi_B$ from 8 interface and materials descriptors.

To eliminate hyperparameter selection optimism, all models are evaluated under **Nested GroupKFold-5** (outer 5 folds for unseen literature generalizability, inner 3 folds for hyperparameter tuning) and headline **Leave-One-Group-Out (LOGO across 23 independent sources)**. Tree ensembles demonstrate superior out-of-distribution generalization: **Random Forest** achieves an out-of-fold Nested CV RMSE of **0.3666 dex** and LOGO RMSE of **0.3884 dex** ($\rho = 0.7699$), followed closely by **LightGBM** (Nested RMSE: **0.3775 dex**, LOGO RMSE: **0.4116 dex**, $\rho = 0.8850$) and **Support Vector Regression** (Nested RMSE: **0.3984 dex**, LOGO RMSE: **0.4038 dex**, $\rho = 0.8539$). For Task 2, **Gaussian Process Regressor (Matérn 5/2)** achieves a LOGO RMSE of **0.1152 eV** ($\rho = 0.8997$).

Evaluating closed-form symbolic scaling equations strictly out-of-fold across unseen publications, we validate a compact scaling law:
$$\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}]) \approx 1.399 + 0.312 \frac{W_M}{\sqrt{n_{2D}/10^{13}}} - 0.344 (\mathbb{I}_{\text{vdW}} \sqrt{n_{2D}/10^{13}}) + 0.405 \frac{|\Delta H_f|}{300}$$
which achieves an out-of-fold LOGO RMSE of **0.3269 dex** and Spearman rank correlation $\rho = \mathbf{0.9163}$ across 23 primary independent publications.

Out-of-fold variance decomposition with 1,000 bootstrap iterations demonstrates that intrinsic electronic transport ($W_M, n_{2D}, T$) accounts for **$63.4\%$** [95% CI: $38.4\% - 75.9\%$] of observed variance, extrinsic fabrication modifiers explain **$10.6\%$** [95% CI: $0.0\% - 37.4\%$], and laboratory/device variability accounts for **$26.6\%$** [95% CI: $11.8\% - 42.2\%$]. Observational path analysis indicates that **$94.7\%$** [95% CI: $48.4\% - 100.0\%$] of the contact resistance reduction in de-pinned van der Waals contacts is statistically mediated through Schottky barrier height reduction.

---

## 1. Primary Data Provenance & Disentangled Corpus
The primary experimental corpus comprises 28 independently characterized $\text{MoS}_2$ FET devices spanning 23 peer-reviewed experimental publications:
- **Disentangled Review Provenance:** 4 review-derived rows in earlier compilations were traced back to original primary literature:
  - DP-017 (Ti) $\to$ Radisavljevic et al., *Nature Nanotechnology* 6, 147 (2011).
  - DP-018 (Mo) $\to$ Chuang et al., *Nano Letters* 14, 1337 (2014).
  - DP-019 (Ni) $\to$ Fontana et al., *Scientific Reports* 3, 1629 (2013).
  - DP-020 (Au) $\to$ Bampoulis et al., *J. Phys. Chem. C* 118, 20459 (2014).
- **Secondary Review Isolation:** Review-level summaries are quarantined into `data/raw/secondary_review_literature_dataset.csv` and excluded from primary training and cross-validation splits.
- **Granular Missingness Tracking:** Missing values explicitly differentiate intentional fabrication choices (`as_fabricated_unannealed`, $\mathbb{I}_{\text{annealed}}=0$) from truly unmeasured parameters (`unreported`). Imputation is strictly executed fold-by-fold without data leakage.

---

## 2. Headline Cross-Validation Benchmarks

### 2.1. Task 1: Primary Contact Resistance Prediction (14 Raw Levers)
Target: $\log_{10} R_c$ ($\Omega\cdot\mu\text{m}$).

| Model Architecture | Model Family | Nested CV-5 RMSE (dex) | LOGO RMSE (dex) | LOGO Spearman $\rho$ | Multi-Objective Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Random Forest** | Tree Ensemble | **0.3666** | **0.3884** | 0.7699 | **0.7812** |
| **LightGBM** | Tree Ensemble | **0.3775** | 0.4116 | **0.8850** | **0.8045** |
| **Support Vector Regression (RBF)** | Kernel Machine | 0.3984 | 0.4038 | 0.8539 | 0.7760 |
| **Gradient Boosting** | Tree Ensemble | 0.4033 | 0.4373 | 0.8129 | 0.7490 |
| **Extra Trees** | Tree Ensemble | 0.4116 | 0.4587 | 0.6716 | 0.6920 |
| **ElasticNet** | Regularized Linear | 0.4841 | 3.2907 | 0.8752 | 0.4320 |
| **HistGradientBoosting** | Tree Ensemble | 0.6405 | 0.6464 | -0.8544 | 0.3820 |
| **Gaussian Process (Matérn 5/2)** | Bayesian Nonparametric | 0.6422 | 0.6469 | -0.8413 | 0.3780 |
| **Ridge Regression** | Regularized Linear | 1.6156 | 6.1320 | 0.8659 | 0.3210 |

### 2.2. Task 2: Schottky Barrier Height Prediction (8 Raw Levers)
Target: Measured Schottky Barrier Height $\Phi_B$ ($\text{eV}$).

| Model Architecture | Model Family | Nested CV-5 RMSE (eV) | LOGO RMSE (eV) | LOGO Spearman $\rho$ | Multi-Objective Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Gaussian Process (Matérn 5/2)** | Bayesian Nonparametric | 0.1295 | **0.1152** | **0.8997** | **0.8610** |
| **ElasticNet** | Regularized Linear | 0.1384 | 0.1206 | 0.8942 | 0.8450 |
| **Random Forest** | Tree Ensemble | 0.1258 | 0.1231 | 0.8535 | 0.8490 |
| **Ridge Regression** | Regularized Linear | 0.1409 | 0.1267 | 0.8778 | 0.8380 |
| **Gradient Boosting** | Tree Ensemble | **0.1131** | 0.1350 | 0.8853 | 0.8520 |
| **Extra Trees** | Tree Ensemble | 0.1468 | 0.1401 | 0.8222 | 0.8120 |
| **Support Vector Regression (RBF)** | Kernel Machine | 0.1495 | 0.1458 | 0.8460 | 0.8190 |
| **LightGBM** | Tree Ensemble | 0.1351 | 0.1573 | 0.8404 | 0.8240 |

---

## 3. Discovered Closed-Form Empirical Scaling Law
Evaluated strictly out-of-fold across 23 independent primary literature sources:
$$\log_{10}(R_c\ [\Omega\cdot\mu\mathrm{m}]) \approx 1.399 + 0.312 \frac{W_M}{\sqrt{n_{2D}/10^{13}}} - 0.344 (\mathbb{I}_{\text{vdW}} \sqrt{n_{2D}/10^{13}}) + 0.405 \frac{|\Delta H_f|}{300}$$
- **GroupKFold-5 OOF RMSE:** **0.3438 dex**
- **LOGO Held-Out RMSE across 23 Publications:** **0.3269 dex**
- **LOGO Spearman Rank Correlation ($\rho$):** **0.9163**
- **Physical Interpretation:** Captures barrier-mediated tunneling, gate carrier accumulation, chemical reactivity, and vdW de-pinning as an interpretable semi-empirical parametric heuristic.

---

## 4. Out-of-Fold Explainability & Nuanced Decoupling
1. **Out-of-Fold TreeSHAP Attributions (Task 1):**
   - Metal Work Function ($W_M$): **0.2786 dex** (43.1% relative attribution)
   - Gate Carrier Density ($n_{2D}$): **0.1886 dex** (29.2% relative attribution)
   - Interface Architecture ($\mathbb{I}_{\text{vdW}}$): **0.0628 dex** (9.7% relative attribution)
   - Interfacial Formation Enthalpy ($\Delta H_f$): **0.0583 dex** (9.0% relative attribution)
   - Post-Annealing Temperature ($T_{\text{anneal}}$): **0.0318 dex** (4.9% relative attribution)
2. **Out-of-Fold Variance Decomposition (1,000 Bootstrap 95% CIs):**
   - Intrinsic Transport Factors ($W_M, n_{2D}, T$): **63.4%** [95% CI: 38.4%, 75.9%]
   - Extrinsic Fabrication Modifiers (vdW transfer, chemistry, annealing): **10.6%** [95% CI: 0.0%, 37.4%]
   - Experimental Variability / Device Noise: **26.6%** [95% CI: 11.8%, 42.2%]
3. **Observational Path Analysis:**
   - Evaluates empirical mediation of vdW de-pinning via Schottky barrier reduction.
   - Indirect Mediated Path: $\beta_{\text{indirect}} = -0.539$ [95% CI: -0.886, -0.022]
   - Direct Unmediated Path: $\beta_{\text{direct}} = -0.016$ [95% CI: -0.276, +0.162] (statistically indistinguishable from zero)
   - Mediation Proportion: **94.7%** [95% CI: 48.4%, 100.0%]

---

## 5. Summary & Engineering Deliverables
- **Live Interactive Dashboard:** Full-stack Flask app (`src/dashboard/app.py`) deployed on `http://127.0.0.1:5050` with live Playwright screenshot verification.
- **Kaggle Benchmark Dataset (v2.0):** Publicly published to [`rohitajitbharadwaj/mos2-contact-resistance-benchmark`](https://www.kaggle.com/datasets/rohitajitbharadwaj/mos2-contact-resistance-benchmark).
- **Automated Test Suite:** 231 passed unit tests covering data curation, provenance, nested cross-validation, model suite, symbolic search, interpretability, and web dashboard.
- **GitHub Repository:** Open-source release at [https://github.com/RohitBharadwaj-rvu/mos2-contact-resistance-ml](https://github.com/RohitBharadwaj-rvu/mos2-contact-resistance-ml).
