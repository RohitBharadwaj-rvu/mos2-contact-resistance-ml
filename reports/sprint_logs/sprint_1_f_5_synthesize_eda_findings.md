# Sprint 1.f.5: Synthesize EDA Findings to Guide Downstream Modeling

## Sprint Metadata
- **Sprint ID:** Sprint-1.f.5
- **Objective:** Synthesize EDA findings to guide downstream modeling decisions (sample size constraints, feature dimensionality vs. sample size risks, need for regularized/parsimonious models, choice of evaluation metrics robust to small-N settings).
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Synthesis of Empirical Findings

Across Sprints 1.f.1 through 1.f.4, rigorous statistical exploration uncovered five foundational realities of the 2D $\text{MoS}_2$ contact resistance literature:

### 1. Small-$N$ Data Regime ($N = 20$, 13 Distinct Papers)
- The experimentally verified dataset comprises 20 rigorous primary device records from 13 independent peer-reviewed literature sources.
- With 13 distinct papers, the effective degrees of freedom across independent research environments is $df \approx 12$.
- **Downstream Implication:** Complex high-capacity models (e.g. unregularized deep neural networks) will instantly overfit. We must enforce strict parsimony: maximum of 3–5 effective input features, strong $L_1/L_2$ regularization, shallow tree depths ($\text{max\_depth} \le 3$), or analytical symbolic formulas.

### 2. Log-Normal Distribution of Contact Resistance
- Raw $R_c$ values span four orders of magnitude ($123$ to $65,000\,\Omega\cdot\mu\text{m}$) with a severe right-skew ($2.50$).
- Taking $\log_{10}(R_c)$ normalizes the skewness to $0.44$, aligning target residuals with standard Gaussian assumptions.
- **Downstream Implication:** All regression models must formulate $\log_{10}(R_c)$ as the primary continuous target variable.

### 3. Severe Multicollinearity Among Physical Descriptors
- Classical Schottky-Mott barrier $\Delta \Phi_{SM} = \Phi_M - \chi$ is perfectly collinear ($r = 1.0$) with metal work function $\Phi_M$.
- Pauling electronegativity $\chi_P$ correlates heavily with $\Phi_M$ ($r = 0.812$).
- Calculating Variance Inflation Factors (VIF) confirms VIF values $> 100$ when all elemental descriptors are included simultaneously.
- **Downstream Implication:** Prune redundant linear descriptors. Use physics-informed compound descriptors (e.g. `physics_predicted_sbh_ev` which accounts for partial pinning $S=0.15$ in evaporated vs $S=0.95$ in vdW contacts).

### 4. Lab Bias vs Material Physics
- Between-paper ANOVA yields $F = 1.711$ ($p = 0.251$).
- Benchmarking identical $\text{Ti}$ contacts across three independent laboratories (English 2016, Liu 2020, Allain 2015) reveals an inter-lab variability factor of $\approx 3.6\times$ ($550$ to $2000\,\Omega\cdot\mu\text{m}$).
- In comparison, selecting semimetal de-pinned contacts ($\text{Bi}$, $R_c = 123\,\Omega\cdot\mu\text{m}$) vs pinned high-$\Phi$ contacts ($\text{Pt}$, $R_c = 65,000\,\Omega\cdot\mu\text{m}$) produces a $> 500\times$ difference.
- **Downstream Implication:** Physical contact descriptors dominate the experimental variance by over two orders of magnitude, validating the feasibility of machine learning modeling despite inter-laboratory noise.

### 5. Evaluation Strategy & Metrics
- Random cross-validation risks severe optimistic bias due to intra-study clustering.
- **CV Strategy:** Must employ **GroupKFold** or **Leave-One-Group-Out (LOGO)** cross-validation grouped strictly by `source_uid`.
- **Metrics:**
  1. $\text{RMSE}(\log_{10} R_c)$: directly interpretable as average order-of-magnitude error (dex).
  2. $\text{MAE}(\log_{10} R_c)$: robust to isolated experimental outliers.
  3. $\text{Spearman's } \rho$: assesses monotonic ranking fidelity between contact strategies.
  4. $\text{Pearson's } r$: assesses linear calibration quality.

---

## 2. Deliverables Produced
- `src/visualization/eda_synthesis.py`: Programmatic synthesizer outputting concrete modeling constraints.
- `tests/test_eda_synthesis.py`: Verification suite confirming constraints and thresholds.
- `data/processed/eda_modeling_recommendations.json`: Machine-readable specification consumed by Section 2 (Model Formulation & Selection).
