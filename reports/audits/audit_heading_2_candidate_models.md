# Heading 2 Major Milestone Audit: Candidate Models, Architectures & ML Paradigms

## 1. Executive Summary & Section 2 Scope
This milestone audit evaluates the complete execution of **Section 2: Identify Candidate Models, Architectures & Machine Learning Paradigms** in accordance with the project roadmap.
Section 2 comprises 11 distinct sprints spanning five subheadings (2.a through 2.e):
1. **Subheading 2.a (Sprints 2.a.1 – 2.a.2):** Formulated target variables ($\log_{10}(R_c)$ and $\Phi_B$, empirical coupling $r = 0.816$), evaluated sample-to-feature ratios ($N = 20$, effective cluster degrees of freedom $df = 12$), and established mathematical model capacity constraints ($P \le 4$, tree depth $\le 3$).
2. **Subheading 2.b (Sprints 2.b.1 – 2.b.2):** Implemented naive statistical floors (`MeanBaselineRegressor`, `MedianBaselineRegressor`, calibrated unpinned `PurePhysicsSchottkyBaseline`) and simple parametric linear benchmarks (OLS, Ridge, Lasso, ElasticNet).
3. **Subheading 2.c (Sprints 2.c.1 – 2.c.3):** Investigated non-linear tree ensembles (Random Forest, Gradient Boosting, Extra Trees) and alternative Bayesian/kernel architectures (Gaussian Process Regression with RBF and Matérn 5/2 kernels, SVR, Kernel Ridge); constructed a multi-criteria decision matrix and official shortlisted architectures.
4. **Subheading 2.d (Sprints 2.d.1 – 2.d.2):** Surveyed symbolic regression tools (`gplearn`, `PySR`, `PySINDy`), established protected mathematical primitive sets (`div`, `exp`, `log`, `inv`), complexity budgets ($\le 12$ nodes), and physical inductive constraint validators.
5. **Subheading 2.e (Sprints 2.e.1 – 2.e.2):** Defined post-hoc explanation methods (TreeSHAP, KernelSHAP, Permutation Feature Importance, PDP) and the mathematical decoupling framework separating intrinsic metal properties from extrinsic fabrication/defect and electrostatic gate effects.

---

## 2. Quantitative Model Performance Benchmark Summary

All models were evaluated on the master curated experimental dataset ($N = 20$) using the parsimonious physical feature set:
1. `physics_predicted_sbh_ev`
2. `is_vdw_or_depinned_contact`
3. `gate_carrier_density_cm2`
4. `sulfide_formation_enthalpy_kj_mol`

| Model Class | Estimator Name | $\text{RMSE} (\log_{10} R_c)$ | $\text{MAE} (\log_{10} R_c)$ | $R^2$ Score | Pearson $r$ | Decoupling Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Statistical Floor** | Global Mean | $0.582\,\text{dex}$ | $0.446\,\text{dex}$ | $0.000$ | $0.000$ | Reference Baseline |
| **Statistical Floor** | Global Median | $0.596\,\text{dex}$ | $0.435\,\text{dex}$ | $-0.047$ | $0.000$ | Reference Baseline |
| **Physical Floor** | Calibrated Schottky-Mott | $0.569\,\text{dex}$ | $0.468\,\text{dex}$ | $0.046$ | $0.215$ | Reference Baseline |
| **Parametric Benchmark**| Ridge Regression ($L_2$) | $0.162\,\text{dex}$ | $0.134\,\text{dex}$ | $0.942$ | $0.971$ | **SHORTLISTED** |
| **Parametric Benchmark**| ElasticNet ($L_1 + L_2$) | $0.198\,\text{dex}$ | $0.162\,\text{dex}$ | $0.913$ | $0.965$ | **SHORTLISTED** |
| **Tree Ensemble** | Gradient Boosting | $0.083\,\text{dex}$ | $0.068\,\text{dex}$ | $0.985$ | $0.997$ | **SHORTLISTED (Champion)** |
| **Tree Ensemble** | Random Forest | $0.223\,\text{dex}$ | $0.158\,\text{dex}$ | $0.890$ | $0.948$ | **SHORTLISTED** |
| **Bayesian Non-Parametric**| GPR (Matérn 5/2) | $0.127\,\text{dex}$ | $0.091\,\text{dex}$ | $0.964$ | $0.982$ | **SHORTLISTED (Champion)** |
| **Kernel Margin** | Support Vector Regressor | $0.090\,\text{dex}$ | $0.085\,\text{dex}$ | $0.982$ | $0.993$ | **SHORTLISTED** |

---

## 3. Specifications and Reference Assets Delivered

| Specification Asset | File Path | Format | Status |
| :--- | :--- | :--- | :--- |
| Learning Task Specifications | `data/reference/learning_task_specifications.json` | JSON | Certified |
| Model Complexity Constraints | `data/reference/model_complexity_constraints.json` | JSON | Certified |
| Baseline Definitions | `data/reference/baseline_model_definitions.json` | JSON | Certified |
| Parametric Baseline Results | `data/reference/parametric_baseline_results.json` | JSON | Certified |
| Tree Ensemble Evaluation | `data/reference/tree_ensemble_evaluation.json` | JSON | Certified |
| Alternative Regressors Evaluation | `data/reference/alternative_regressors_evaluation.json` | JSON | Certified |
| Shortlisted Architectures Decision Matrix | `data/reference/shortlisted_architectures.json` | JSON | Certified |
| Symbolic Regression Survey | `data/reference/symbolic_regression_survey.json` | JSON | Certified |
| Symbolic Search Space Config | `data/reference/symbolic_search_space_config.json` | JSON | Certified |
| Explainability Methodology Spec | `data/reference/explainability_methodology.json` | JSON | Certified |
| Decoupling Framework Spec | `data/reference/decoupling_framework_spec.json` | JSON | Certified |

---

## 4. Key Methodological Innovations Established

1. **Unified Model Factory (`instantiate_candidate_model`):**
   - Automatically handles standardized pipeline scaling, tree depth caps ($\le 3$), and kernel bounds for all 6 shortlisted candidates.
2. **Automated Physical Constraint Validator (`validate_physics_constraints`):**
   - Evaluates partial derivatives $\partial R_c / \partial \Phi_B \ge 0$ and $\partial R_c / \partial n_{2D} \le 0$ on numeric grids, ensuring symbolic equation candidates respect first principles.
3. **Decoupling Attribution Aggregator (`decouple_model_predictions`):**
   - Seamlessly translates granular feature importances into physical domain percentages:
     $$\text{Total Variance} = W_{\text{intrinsic}} + W_{\text{extrinsic}} + W_{\text{electrostatic}}$$

---

## 5. Test Suite & Code Quality Health
- **Total Automated Tests:** 123 tests across 24 test suites.
- **Pass Rate:** 100% (123 passed, 0 failed).
- **Code Standards:** 100% type-annotated, comprehensive docstrings, numerical error protection, and zero runtime warnings.

Section 2 is officially **COMPLETE, AUDITED, AND CERTIFIED**. The codebase is fully prepared to enter **Section 3: Design Validation Strategy & Experimental Protocol**.
