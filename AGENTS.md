# Project Agent Guidelines: $\text{MoS}_2$ Contact Resistance & Schottky Barrier Height ML Project

## 1. Project Context & Objectives
This project implements a rigorous, end-to-end Machine Learning and Physical Characterization framework for predicting and decoupling contact resistance ($R_c$) and Schottky barrier height ($\Phi_B$) in monolayer and few-layer molybdenum disulfide ($\text{MoS}_2$) field-effect transistors (FETs).

The master plan for the project is documented in [`mos2_contact_resistance_ml_execution_roadmap.md`](file:///c:/Users/rohit/.gemini/antigravity/playground/semicon%20charecterization/mos2_contact_resistance_ml_execution_roadmap.md).

---

## 2. Sprint Execution Rules & Workflow

1. **Deepest Point as an Individual Sprint:**
   - Every lowest-level numbered bullet in `mos2_contact_resistance_ml_execution_roadmap.md` constitutes an entire, self-contained sprint.
   - Sprints must be executed rigorously, producing tangible scripts, datasets, validation reports, evaluation metrics, equations, and documentation.
   - Sequence is strictly sequential from Sprint 1.a.1 to Sprint 6.b.3.

2. **Git & GitHub Integration:**
   - After **each sprint**, all new code, data, logs, and artifacts must be staged and committed with a clear, informative commit message (e.g., `feat(sprint-1.a.1): Survey scientific literature indexes and build index registry`).
   - Immediately push the commit to GitHub (`origin main`).

3. **Subheading and Heading Review Breaks (Audit & Gap Closure):**
   - **Subheading Review:** Upon completing all sprints under any subheading (e.g., after 1.a, 1.b, 1.c, etc.), halt new feature work to conduct an audit:
     - Check for errors, edge cases, missing data, and suboptimal implementations.
     - Identify scientific and computational gaps.
     - Implement fixes and refinements before advancing to the next subheading.
     - Commit and push the review & improvement deliverables.
   - **Heading Milestone Review:** Upon completing all subheadings under a major heading (e.g., Section 1, Section 2, etc.), conduct an overarching milestone audit and integration verification before proceeding to the subsequent major heading.

4. **Kaggle Compute & Storage Access:**
   - The environment has access to Kaggle CLI authenticated as `rohitajitbharadwaj`.
   - Utilize Kaggle for dataset sharing, benchmark hosting, and heavy GPU/CPU training whenever advantageous.

5. **Goal-Driven Unbroken Execution:**
   - Under the `/goal` execution mode, execution proceeds autonomously without stopping until all sprints, review breaks, models, interpretable regime maps, and final deliverables across the entire roadmap are 100% complete.

---

## 3. Scientific Audit Remediation Sprints (Section 7)
Following the expert scientific validation audit, the project executes 8 dedicated remediation sprints addressing all identified concerns:
1. **Sprint 7.1: Primary Data Provenance Disentanglement & Literature Expansion:**
   - Trace review-derived observations (DP-017 through DP-020) back to primary experimental publications.
   - Separate review-derived data into a secondary dataset; exclude from primary benchmark.
   - Expand primary experimental corpus to 35+ device observations across 18+ independent peer-reviewed experimental papers.
2. **Sprint 7.2: Missing-Value Scientific Rigor & Granular Measurement Provenance:**
   - Track measurement quality (`measured`, `calculated_from_reported`, `as_fabricated_unannealed`, `not_reported`).
   - Remove naive hardcoded default imputations (e.g., 20°C annealing, 1e13 carrier density).
   - Generate explicit missingness indicators and missingness-aware modeling.
3. **Sprint 7.3: Full Experimental Feature Space & De-Biased SBH Prediction:**
   - Un-bake assumed pinning factors ($S=0.95/0.15$) from model inputs; supply raw physical inputs ($W_M$, deposition method, annealing temp/atmosphere, layer count/thickness, dielectric stack/EOT, measurement temp).
   - Establish two distinct prediction tasks: Task 1 ($R_c$ prediction from raw experimental inputs) and Task 2 (Schottky barrier height $\Phi_B$ prediction).
4. **Sprint 7.4: Nested Paper-Wise Cross-Validation & Headline LOGO Benchmark:**
   - Implement nested cross-validation: outer GroupKFold for generalisation, inner GroupKFold strictly on training folds for tuning/feature selection.
   - Implement Leave-One-Group-Out (LOGO) across all independent primary paper groups as the headline external benchmark.
5. **Sprint 7.5: Complete ML Model Suite (including XGBoost & Tree Regularization):**
   - Add `xgboost` as a candidate model alongside Ridge, ElasticNet, Random Forest, HistGradientBoosting, LightGBM, and GP.
   - Benchmark all candidate models under Nested GroupKFold and LOGO.
6. **Sprint 7.6: Cross-Validated Symbolic Regression & Held-Out Law Evaluation:**
   - Evaluate symbolic regression candidate equations on genuinely held-out publications under cross-validation.
7. **Sprint 7.7: Out-of-Fold Explainability & Nuanced Decoupling Analysis:**
   - Compute SHAP values out-of-fold using fold-specific models.
   - Reframe causal claims as empirical associations and observational path analysis with bootstrap confidence intervals.
8. **Sprint 7.8: Full Pipeline Refactoring, Dashboard Sync, Verified Screenshots & Kaggle Update:**
   - Update `contact_predictor_pipeline.py`, Flask dashboard (`src/dashboard/app.py`), verified Playwright screenshot, Kaggle dataset sync, and final thesis/presentation documents.
