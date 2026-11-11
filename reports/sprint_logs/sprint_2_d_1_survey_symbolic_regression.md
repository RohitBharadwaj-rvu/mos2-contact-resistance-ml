# Sprint 2.d.1: Survey Symbolic Regression Algorithms and Tools

## Sprint Metadata
- **Sprint ID:** Sprint-2.d.1
- **Objective:** Research how symbolic regression algorithms operate, evaluate available open-source software libraries, and determine the optimal toolchain for extracting analytical formulas from $\text{MoS}_2$ contact data.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Algorithmic Paradigms for Symbolic Discovery

Symbolic regression discovers mathematical models directly from data without prescribing an arbitrary model structure:
1. **Genetic Programming (Tree Evolution):**
   - Syntax trees representing equations evolve via crossover, point mutation, and subtree hoist mutations.
   - Objective: $\min \text{Fitness} = \text{MSE} + \lambda \times \text{Length}(\text{Tree})$.
   - Parsimony coefficient $\lambda$ penalizes bloat.
2. **Multi-Population Pareto Search (PySR):**
   - Evolves islands of equations and computes continuous non-dominated Pareto frontiers comparing loss against string complexity.
   - Refines constant real coefficients via BFGS gradient descent.
3. **Dictionary Sparse Regression (SINDy):**
   - Formulates equation discovery as sparse linear selection over a candidate basis library: $\dot{x} = \Theta(X) \Xi$.

---

## 2. Framework Comparison & Selection

| Framework | Engine & API | Strengths | Limitations | Decision |
| :--- | :--- | :--- | :--- | :--- |
| **`gplearn`** | Pure Python, Scikit-Learn | Seamless integration with Scikit-Learn `Pipeline`, native parsimony penalty, zero foreign C++/Julia dependencies, lightweight. | Requires multiple random seeds to avoid local tree minima. | **PRIMARY SELECTION (Production Tool)** |
| **`PySR`** | Julia (`SymbolicRegression.jl`) | Full Pareto frontier generation, constant BFGS refinement. | Requires external Julia runtime and JIT compilation overhead. | **SECONDARY / BENCHMARK** |
| **`PySINDy`** | NumPy / Scipy | Deterministic, fast convex STLSQ. | Cannot discover nested exponential compositions easily. | **BENCHMARK** |

---

## 3. Deliverables Produced
- `src/models/symbolic_survey.py`: Software evaluation matrix and architecture survey.
- `tests/test_symbolic_survey.py`: Automated verification tests.
- `data/reference/symbolic_regression_survey.json`: Serialized evaluation scores.
