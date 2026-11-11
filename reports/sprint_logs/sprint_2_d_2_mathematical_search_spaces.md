# Sprint 2.d.2: Determine Mathematical Search Spaces and Physical Constraints

## Sprint Metadata
- **Sprint ID:** Sprint-2.d.2
- **Objective:** Establish primitive mathematical operator sets, numerical protection mechanisms, complexity penalties, and physical inductive constraints for symbolic regression equation discovery.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Protected Mathematical Operator Primitives

Standard symbolic evolution frequently encounters singularities (division by zero, negative logarithms, exponential overflows). We formulated numerically protected versions:
1. **Protected Division ($\text{div}(x_1, x_2)$):** Returns $1.0$ when $|x_2| < 10^{-6}$.
2. **Protected Exponential ($\text{exp}(x)$):** Clips exponent at $[-20.0, +15.0]$ to prevent IEEE-754 overflow.
3. **Protected Logarithm ($\text{log}(x)$):** Clips argument at $[10^{-6}, 10^{12}]$ with absolute value protection.
4. **Protected Reciprocal ($\text{inv}(x)$):** Returns $0.0$ when $|x| < 10^{-6}$.

---

## 2. Complexity Budgets and Genetic Hyperparameters

To prevent equation bloat and ensure human-interpretable formulas:
- **Maximum Syntax Tree Depth:** $\le 4$ levels.
- **Maximum Node Count:** $\le 12$ operators/terminals.
- **Parsimony Penalty:** $\lambda = 0.035$, penalizing redundant terms in the fitness function.
- **Population & Generations:** 1,000 individuals over 50 generations with tournament size 20.

---

## 3. Solid-State Physical Inductive Constraints

Any discovered candidate formula must obey foundational semiconductor physics:
1. **Barrier Monotonicity:**
   $$\frac{\partial \log_{10} R_c}{\partial \Phi_B} \ge 0$$
   An increase in the interfacial Schottky barrier cannot decrease contact resistance.
2. **Gate Density Monotonicity:**
   $$\frac{\partial \log_{10} R_c}{\partial n_{2D}} \le 0$$
   Electrostatic carrier accumulation compresses the tunneling barrier and must decrease contact resistance.
3. **Ballistic Asymptote Bound:**
   $$\lim_{n_{2D} \to \infty, \Phi_B \to 0} R_c \ge R_{\text{quantum}} \approx \frac{h}{2 e^2 M} \sim 10 - 100\,\Omega\cdot\mu\text{m}$$
   The formula cannot predict unphysical sub-quantum zero contact resistance.

---

## 4. Deliverables Produced
- `src/models/symbolic_search_space.py`: Protected math operators and search space definition.
- `tests/test_symbolic_search_space.py`: Unit tests for operator stability and constraint definitions.
- `data/reference/symbolic_search_space_config.json`: Machine-readable search space specification.
