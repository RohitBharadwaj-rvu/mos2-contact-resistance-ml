# Sprint 2.a.1: Define Target Formulations

## Sprint Metadata
- **Sprint ID:** Sprint-2.a.1
- **Objective:** Decide how to structure the prediction tasks for target variables ($\log_{10}(R_c)$ and $\Phi_B$), evaluate empirical and theoretical coupling, and determine single-task vs multi-task vs physics-chained regression formulations.
- **Date:** 2026-11-12
- **Status:** COMPLETED

---

## 1. Analysis of Target Variables

The curated $\text{MoS}_2$ contact dataset features two central continuous targets:
1. **Contact Resistance ($R_c$, continuous $\Omega\cdot\mu\text{m}$):** Formulated as $\log_{10}(R_c)$ to achieve skewness normality ($0.44$) and capture orders-of-magnitude transport scaling.
2. **Schottky Barrier Height ($\Phi_B$, continuous $\text{eV}$):** Measures interfacial potential barrier for thermionic and field emission.

### Statistical & Physical Coupling
- Empirical correlation across all experimental devices: $r = 0.816$ ($p = 1.34 \times 10^{-5}$), Spearman $\rho = 0.842$.
- Physical mechanism: According to thermionic emission theory across a 2D/3D semiconductor interface:
  $$J = A^* T^{3/2} \exp\left(-\frac{q \Phi_B}{k_B T}\right) \implies R_c \propto \frac{k_B T}{q A^* T^{3/2}} \exp\left(\frac{q \Phi_B}{k_B T}\right)$$
  Taking the logarithm:
  $$\log_{10}(R_c) = \text{const} + \frac{q \Phi_B}{2.303 k_B T} - \log_{10}(n_{2D})$$
  Therefore, $\log_{10}(R_c)$ scales linearly with $\Phi_B$ at constant temperature and gate density.

---

## 2. Selected Task Architectures

We evaluated three candidate learning formulations:
1. **Independent Single-Task Regression (Recommended Primary):**
   - Separate estimators for $\log_{10}(R_c)$ and $\Phi_B$.
   - *Rationale:* With $N = 20$, multi-output joint networks suffer from optimization interference. Independent estimators allow separate $L_1/L_2$ regularization parameters tuned to each physical target.
2. **Joint Multi-Task Regression (Evaluated Benchmark):**
   - Multi-output regressor optimizing $L = L(\log_{10} R_c) + \lambda L(\Phi_B)$.
3. **Physics-Chained Hybrid Pipeline (Recommended Innovation):**
   - Stage 1 predicts effective Schottky barrier height $\hat{\Phi}_B$ from intrinsic metal work function, semimetal pinning factor, and sulfur chemical enthalpy.
   - Stage 2 predicts $\log_{10}(R_c)$ using $\hat{\Phi}_B$ alongside extrinsic processing variables (gate carrier density $n_{2D}$, post-annealing temperature $T_{anneal}$, and dielectric permittivity $\kappa$).
   - This explicitly decouples the electronic barrier formation from the electrostatic gating and fabrication quality.

---

## 3. Deliverables Produced
- `src/models/task_formulation.py`: Module defining target correlation evaluation and learning task specifications.
- `tests/test_task_formulation.py`: Test suite verifying correlation bounds and task specifications.
- `data/reference/learning_task_specifications.json`: Serialized schema for downstream models.
