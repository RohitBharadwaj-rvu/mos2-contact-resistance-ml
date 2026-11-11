# Subheading 2.a Audit: Formulation of the Learning Tasks & Capacity Constraints

## 1. Scope & Objectives
Subheading 2.a defines the structural foundation of the machine learning tasks:
- **Sprint 2.a.1:** Target formulations ($\log_{10}(R_c)$ and $\Phi_B$), evaluation of empirical/theoretical correlations ($r = 0.816$), and recommendation of independent and physics-chained regression formulations.
- **Sprint 2.a.2:** Sample-to-feature ratio analysis ($N = 20, df = 12$), establishing mathematical capacity bounds ($P \le 4$, tree depth $\le 3$, equation length $\le 12$).

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Automated Parsimonious Feature Selection Seam
- **Issue:** While mathematical bounds ($P \le 4$) were defined, downstream models lacked a reusable, programmatic function to retrieve the optimal non-collinear feature subset.
- **Resolution:** Implemented `select_parsimonious_features(df, max_features=4)` in `src/models/sample_complexity_analyzer.py` which dynamically enforces $|r| < 0.85$ between selected inputs, prioritizing `physics_predicted_sbh_ev`, `is_vdw_or_depinned_contact`, and `sulfide_formation_enthalpy_kj_mol`.

---

## 3. Verification & Compliance
- `src/models/task_formulation.py`: All target formulations verified against thermionic transport theory.
- `src/models/sample_complexity_analyzer.py`: Capacity boundaries serialized to `data/reference/model_complexity_constraints.json`.
- `tests/test_task_formulation.py` & `tests/test_sample_complexity_analyzer.py`: 100% passing tests.

Subheading 2.a is certified and approved to advance to Subheading 2.b.
