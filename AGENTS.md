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
