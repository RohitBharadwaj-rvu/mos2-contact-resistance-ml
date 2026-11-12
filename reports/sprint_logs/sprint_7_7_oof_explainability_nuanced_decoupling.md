# Sprint 7.7 Log: Out-of-Fold Explainability & Nuanced Decoupling Analysis

## 1. Sprint Objective
Address critical Reviewer Audit Concern E regarding over-claiming and methodological leakage in interpretability:
- **Out-of-Fold SHAP Attributions:** Replace in-sample SHAP calculations with out-of-fold TreeSHAP attributions computed strictly on validation folds using models trained on separate literature splits.
- **Out-of-Fold Variance Decomposition with Bootstrap CIs:** Replace sequential in-sample OLS regressions with out-of-fold GroupKFold predictions and 1,000-iteration bootstrap 95% confidence intervals.
- **Reframing Causal Claims to Observational Path Analysis:** Explicitly re-state mediation analyses as empirical path associations with bootstrap confidence intervals, acknowledging observational limitations rather than asserting dogmatic causal proof.

---

## 2. Quantitative Results & Findings

### 2.1. Out-of-Fold SHAP Feature Attributions (Task 1: Raw Physical Levers)
Computed via fold-isolated Random Forest models on held-out literature splits across 28 primary devices:

| Feature | Mean Absolute Out-of-Fold SHAP (|dex|) | Relative Importance (%) | Physical Role |
| :--- | :---: | :---: | :--- |
| `work_function_ev` ($W_M$) | **0.2786** | **43.09%** | Primary electronic band alignment / Schottky barrier control |
| `n2d_norm_1e13` ($n_{2D}$) | **0.1886** | **29.16%** | Electrostatic band-bending and tunnel barrier thinning |
| `is_vdw_or_depinned_contact` ($\mathbb{I}_{\text{vdW}}$) | 0.0628 | 9.71% | Interface defect/pinning suppression |
| `sulfide_formation_enthalpy_kj_mol` ($\Delta H_f$) | 0.0583 | 9.01% | Chemical reactivity and interfacial compound formation |
| `post_annealing_temperature_c` | 0.0318 | 4.92% | Thermal activation and contact interface remodeling |

### 2.2. Out-of-Fold Intrinsic vs Extrinsic Variance Decomposition (1,000 Bootstrap CIs)
Evaluating hierarchical regression out-of-fold across 5 paper-isolated splits:

| Component | Point Estimate (Median) | 95% Bootstrap Confidence Interval |
| :--- | :---: | :---: |
| **Intrinsic Transport Factors** ($W_M$, $n_{2D}$, $T_{\text{meas}}$) | **63.4%** | [38.4%, 75.9%] |
| **Extrinsic Fabrication Modifiers** (vdW transfer, $\Delta H_f$, $T_{\text{anneal}}$) | **10.6%** | [0.0%, 37.4%] |
| **Device/Lab Experimental Variability (Noise)** | **26.6%** | [11.8%, 42.2%] |

### 2.3. Observational Path Analysis (Empirical Mediation with 1,000 Bootstrap Resamples)
Evaluating how de-pinned / vdW transfer architecture relates to contact resistance through Schottky barrier reduction ($\Phi_B$):
- **Total Empirical Association:** $\beta_{\text{total}} = -0.555$ [95% CI: -0.892, -0.015]
- **Indirect Path via $\Phi_B$ Reduction:** $\beta_{\text{indirect}} = -0.539$ [95% CI: -0.886, -0.022]
- **Direct Path (Unmediated):** $\beta_{\text{direct}} = -0.016$ [95% CI: -0.276, +0.162] (statistically indistinguishable from 0)
- **Mediation Proportion:** **94.7%** [95% CI: 48.4%, 100.0%]

---

## 3. Scientific Qualification Statement
> **Observational Path Modeling vs Causal Claims:** Because the published literature dataset is observational rather than derived from randomized controlled trials, path coefficients reflect empirical associations and mediation hypotheses rather than conclusive proof of fundamental causality. The data strongly indicate that barrier height reduction statistically mediates virtually the entirety of the contact resistance improvement in de-pinned van der Waals contacts, while direct tunneling modification contributes minimally.

---

## 4. Deliverables
- `src/interpretability/oof_explainability_engine.py`: Out-of-fold SHAP, bootstrap variance decomposition, and observational path analysis.
- `tests/test_oof_explainability.py`: Automated test suite for OOF SHAP, bootstrap variance shares, and path modeling.
- `data/processed/oof_explainability_and_decoupling_benchmarks.json`: Serialized metrics, rankings, and bootstrap intervals.
- `reports/figures/oof_shap_summary.png`: Horizontal bar chart of out-of-fold SHAP attributions.
- `reports/figures/oof_variance_decomposition_bootstrap.png`: Bar chart with 95% bootstrap error bars for variance shares.
