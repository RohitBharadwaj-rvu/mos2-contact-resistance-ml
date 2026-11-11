# Sprint 4.d.3 Log: Evaluate Discovered Equations for Accuracy-Complexity Trade-Off

## 1. Objectives & Physical Audit Framework
- Evaluate discovered equations from genetic programming against solid-state physical requirements and dimensional consistency.
- Enforce three fundamental physical sanity tests:
  1. **Barrier Monotonicity:** $\frac{\partial \log_{10} R_c}{\partial \Phi_B} \ge 0$ (Thermionic emission decreases exponentially with barrier height).
  2. **Carrier Monotonicity:** $\frac{\partial \log_{10} R_c}{\partial n_{2D}} \le 0$ (Electrostatic gate doping thins the depletion region and accelerates tunneling).
  3. **Quantum Asymptotic Floor:** As $\Phi_B \to 0$ and $n_{2D} \to 2 \times 10^{13}\,\text{cm}^{-2}$, $R_c$ must converge above the ballistic Landauer quantum limit ($R_Q \approx 25 - 50\,\Omega\cdot\mu\text{m}$, or $\log_{10} R_c \approx 1.4 - 1.7\,\text{dex}$).
- Classify equations into Pareto-optimal, physically valid, or degenerate, and select the optimal symbolic surrogate.

## 2. Audited Equations & Physical Classification

| Tier | Discovered Symbolic Form | OOF RMSE (dex) | Spearman $\rho$ | C-index | Composite Score | Physics Audit | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Ultra Compact)** | $\log_{10} R_c \approx \frac{1}{\tilde{n}_{2D}} + 1.647$ | 0.5200 | 0.7276 | 0.7711 | 0.6394 | Passes ($\Phi_B$ neutral, $n_{2D}$ monotonic, floor $1.85\,\text{dex}$) | Valid (Suboptimal) |
| **Tier 2 (Compact)** | $\log_{10} R_c \approx \frac{0.679}{\tilde{n}_{2D}} + 2.268$ | 0.5520 | 0.7033 | 0.7553 | 0.6142 | Passes | Valid (Suboptimal) |
| **Tier 3 (Intermediate)** | $\log_{10} R_c \approx \tilde{n} + \Phi_B + \frac{0.35 \Phi_B}{\delta_{\text{vdW}}} + \frac{1}{\tilde{n}} + 0.396$ | 0.4981 | 0.8211 | 0.8263 | 0.6947 | Fails ($\frac{\partial R_c}{\partial \tilde{n}} > 0$ at high doping) | Unphysical |
| **Tier 4 (Pareto Optimal)** | **$\log_{10} R_c \approx \Phi_B - \tilde{n}_{2D} + 3.660$** | **0.3859** | **0.8887** | **0.8737** | **0.7751** | **Passes All Constraints** | **PHYSICALLY VALID & PARETO OPTIMAL** |

## 3. Recommended Closed-Form Physical Surrogate
The Tier 4 relationship represents an extraordinary physical distillation:
$$\log_{10}\left(R_c / [\Omega\cdot\mu\text{m}]\right) \approx \Phi_B / [\text{eV}] - \left(\frac{n_{2D}}{10^{13}\,\text{cm}^{-2}}\right) + 3.660$$
In linear resistance units:
$$R_c \approx 4570 \cdot 10^{\Phi_B - \left(\frac{n_{2D}}{10^{13}}\right)}\;\Omega\cdot\mu\text{m}$$
- **Physical Verification:**
  - Zero barrier ($\Phi_B = 0\,\text{eV}$) at maximum practical gate induction ($n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$):
    $$R_c = 4570 \cdot 10^{0 - 2} = 45.7\,\Omega\cdot\mu\text{m}$$
    This matches within $< 10\%$ the theoretical Landauer-Sharvin 2D quantum resistance limit for monolayer $\text{MoS}_2$ ($R_Q = \frac{h}{4 e^2 k_F} \approx 25 - 50\,\Omega\cdot\mu\text{m}$)!
  - High barrier ($\Phi_B = 0.8\,\text{eV}$) at weak gating ($n_{2D} = 3 \times 10^{12}\,\text{cm}^{-2}$):
    $$R_c = 4570 \cdot 10^{0.8 - 0.3} = 4570 \cdot 10^{0.5} \approx 14.5\,\text{k}\Omega\cdot\mu\text{m}$$
    Consistent with pinned unpassivated high-barrier literature contacts.

## 4. Implemented Deliverables
- `src/models/symbolic_evaluator.py`: Finite-difference gradient verifier, quantum floor checker, and accuracy-complexity Pareto analyzer.
- `tests/test_symbolic_evaluator.py`: Unit test suite testing valid and invalid symbolic models.
- `data/processed/symbolic_equations_audited.json`: Comprehensive report containing all equation audits and the recommended formula.

## 5. Verification & Validation
- Ran `python -m pytest tests/test_symbolic_evaluator.py` — Passed (3/3 green).
