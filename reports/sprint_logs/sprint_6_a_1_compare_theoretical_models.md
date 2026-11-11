# Sprint 6.a.1 Log: Compare ML Trends Against Semiconductor Physics and Theoretical Models

## 1. Sprint Objective
Connect machine learning empirical trends, feature attributions, and discovered closed-form equations directly to foundational solid-state semiconductor contact physics. Specifically evaluate:
1. **Schottky-Mott Rule vs Bardeen Fermi-Level Pinning:** Quantify the pinning parameter $S = d\Phi_B / dW_M$ across evaporated 3D interfaces vs van der Waals transferred contacts.
2. **Landauer-Sharvin Ballistic Quantum Limit:** Derive the theoretical lower bound on contact resistance for 2D $\text{MoS}_2$ and verify that ML predictions respect this quantum mechanical ceiling.
3. **Thermionic vs Field-Emission Tunneling Scaling:** Contrast the empirical activation sensitivity $\partial \log_{10} R_c / \partial \Phi_B$ against Richardson thermionic emission to identify the true microscopic injection mechanism.

---

## 2. Theoretical Analysis & Key Findings

### 2.1. Landauer-Sharvin Quantum Ballistic Contact Limit
For monolayer $\text{MoS}_2$ with conduction band valley degeneracy $g_v = 2$, spin degeneracy $g_s = 2$, and effective mass $m^* = 0.55\,m_0$:
$$k_F = \sqrt{\pi n_{2D}},\quad \frac{M}{W} = \frac{2 k_F}{\pi} = 2 \sqrt{\frac{n_{2D}}{\pi}}$$
The Landauer-Sharvin quantum contact resistance floor for a single contact is:
$$R_{c,\min} = \frac{h}{4 e^2 \sqrt{n_{2D}/\pi}}$$
- At $n_{2D} = 1.0 \times 10^{13}\,\text{cm}^{-2}$: $R_{c,\min} \approx 18.1\,\Omega\cdot\mu\text{m}$ ($36.2\,\Omega\cdot\mu\text{m}$ for contact pair).
- At $n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$: $R_{c,\min} \approx 12.8\,\Omega\cdot\mu\text{m}$ ($25.6\,\Omega\cdot\mu\text{m}$ for contact pair).
- The discovered closed-form ML equation predicts $R_c = 45.7\,\Omega\cdot\mu\text{m}$ at $\Phi_B = 0\,\text{eV}$ and $n_{2D} = 2.0 \times 10^{13}\,\text{cm}^{-2}$, maintaining a physically sound margin factor of $3.57\times$ over the ideal ballistic single-contact limit (accounting for non-ideal acoustic and optical phonon scattering in realistic devices).

### 2.2. Fermi-Level Pinning & MIGS Suppression
- Conventional Evaporated Metals ($3D$ deposition): $S \approx 0.15 - 0.28$, reflecting severe Metal-Induced Gap States (MIGS) and defect pinning near the charge neutrality level ($\Phi_{\text{CNL}} \approx 4.5\,\text{eV}$).
- Van der Waals Transferred Interfaces (Bi, Sb, Graphene): $S \to 0.95 - 1.0$, approaching the ideal unpinned Schottky-Mott limit ($S = 1.0$) with pristine, dangling-bond-free interfaces.

### 2.3. Transport Mechanism: Thermionic vs Field-Emission Tunneling
- Pure Richardson thermionic emission at $T = 300\,\text{K}$ predicts:
  $$\frac{\partial \log_{10} R_c}{\partial \Phi_B} = \frac{q}{\ln(10) k_B T} \approx 16.8\,\text{dex/eV}$$
- Machine learning models and symbolic regression discover an empirical slope of $\mathbf{1.00 - 1.30\,\text{dex/eV}}$ (a $16.8\times$ shallower slope).
- **Physical Deduction:** Contact injection in practical 2D $\text{MoS}_2$ FETs is **not** pure thermionic emission over the barrier. Rather, it is dominated by **Thermionic-Field Emission (TFE) and Fowler-Nordheim tunneling**, where gate electrostatic band-bending thins the tunneling barrier width ($W_{\text{dep}} \propto \sqrt{\epsilon / n_{2D}}$), allowing carriers to tunnel through rather than thermally surmount the barrier.

---

## 3. Key Deliverables
- `src/physics/theoretical_models_comparator.py`: Physics comparator pipeline and Landauer limit calculator.
- `tests/test_theoretical_models_comparator.py`: Comprehensive test suite verifying quantum bounds, pinning analysis, and scaling.
- `data/processed/theoretical_physics_comparison.json`: Processed numerical comparisons, physical parameters, and margin factors.
- `reports/figures/ml_vs_theoretical_models.png`: Two-panel publication graphic showing (a) Ballistic quantum floor vs ML predictions and (b) Schottky-Mott vs Bardeen pinning curves.

---

## 4. Verification & Status
- Unit tests: 100% passing.
- Outputs verified.
- Completed Sprint 6.a.1.
