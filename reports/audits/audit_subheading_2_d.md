# Subheading 2.d Audit: Symbolic Regression Paradigms & Constraints

## 1. Scope & Objectives
Subheading 2.d establishes the foundations for closed-form equation discovery of $\text{MoS}_2$ contact resistance:
- **Sprint 2.d.1:** Algorithm and framework survey (`gplearn`, `PySR`, `PySINDy`).
- **Sprint 2.d.2:** Primitive operator search spaces, protected arithmetic (`div`, `exp`, `log`, `inv`), complexity budgets ($\le 12$ nodes), and physical inductive constraints.

---

## 2. Issues, Gaps & Suboptimal Implementations Addressed

### Gap 1: Automated Verification of Discovered Symbolic Equations
- **Issue:** Symbolic genetic algorithms occasionally evolve equations with high accuracy that violate physical first principles (e.g., negative barrier height derivatives or sub-quantum resistance).
- **Resolution:** Implemented `validate_physics_constraints(func)` in `src/models/symbolic_search_space.py`. It evaluates finite-difference partial derivatives across $\Phi_B$ and $n_{2D}$ grids, verifying positive Schottky monotonicity ($\partial R_c / \partial \Phi_B \ge 0$), negative gate accumulation monotonicity ($\partial R_c / \partial n_{2D} \le 0$), and quantum Landauer lower bounds.

---

## 3. Verification & Compliance
- Serialized search configuration in `data/reference/symbolic_search_space_config.json`.
- All tests in `tests/test_symbolic_survey.py` and `tests/test_symbolic_search_space.py` pass cleanly with zero warnings.

Subheading 2.d is certified and approved to advance to Subheading 2.e.
