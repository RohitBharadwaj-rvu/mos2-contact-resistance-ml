# Sprint 5.c.2 Log: Generate 2D/3D Regime Phase Diagrams

## 1. Objectives & Visualization Framework
- Construct a continuous 2D contour phase diagram mapping predicted contact resistance $R_c$ across the primary physical space: Gate Carrier Density $n_{2D}$ ($1.0 \times 10^{12} - 2.5 \times 10^{13}\,\text{cm}^{-2}$) $\times$ Schottky Barrier Height $\Phi_B$ ($0.0 - 1.3\,\text{eV}$).
- Overlay discrete solid-state transport regime boundaries:
  - **Boundary I/II:** $R_c = 200\,\Omega\cdot\mu\text{m}$ ($2.30\,\text{dex}$) [Ballistic / Quantum-limited threshold].
  - **Boundary II/III:** $R_c = 1,500\,\Omega\cdot\mu\text{m}$ ($3.18\,\text{dex}$) [Tunneling vs Thermionic boundary].
  - **Boundary III/IV:** $R_c = 15,000\,\Omega\cdot\mu\text{m}$ ($4.18\,\text{dex}$) [Thermionic vs Defect-pinned threshold].
- Overlay all 20 curated historical benchmark devices from the literature, color-coded by fabrication architecture (vdW transferred vs 3D evaporated).
- Map unexplored experimental white space and technological opportunity zones.
- Generate secondary phase map: Metal Work Function $\Phi_m$ vs Contact Resistance, contrasting unpinned Schottky-Mott scaling with the Fermi-level pinning plateau.

## 2. Phase Diagram Architecture & Regime Boundaries

| Regime | Visual Domain in Phase Space | Border Contour | Technological Anchor |
| :--- | :--- | :--- | :--- |
| **Regime I (Quantum-Limited)** | Bottom-Right ($\Phi_B < 0.2\,\text{eV}$, $n_{2D} > 1.2 \times 10^{13}\,\text{cm}^{-2}$) | Cyan Dashed ($R_c = 200\,\Omega\cdot\mu\text{m}$) | Bi(0001) vdW, 1T-MoS2 homojunction |
| **Regime II (Tunneling)** | Center-Right ($0.2 \le \Phi_B \le 0.5\,\text{eV}$, $n_{2D} > 8 \times 10^{12}\,\text{cm}^{-2}$) | Yellow Solid ($R_c = 1,500\,\Omega\cdot\mu\text{m}$) | Ti/Au annealed, Sc, In, Ag |
| **Regime III (Thermionic)** | Top-Left ($0.5 < \Phi_B \le 0.8\,\text{eV}$, $n_{2D} < 10^{13}\,\text{cm}^{-2}$) | White Dash-Dot ($R_c = 15\,\text{k}\Omega\cdot\mu\text{m}$) | Au, Ni, Cr, Mo |
| **Regime IV (Defect Pinned)** | Extreme Top-Left ($\Phi_B > 0.8\,\text{eV}$, low gating) | Outer Bounds ($R_c > 15\,\text{k}\Omega\cdot\mu\text{m}$) | High-work-function Pt |

## 3. Identified Technological White Space
1. **Ultra-High Electrostatic Gating Regime ($n_{2D} > 2.0 \times 10^{13}\,\text{cm}^{-2}$ with moderate $\Phi_B \approx 0.3 - 0.5\,\text{eV}$):**
   - High-$\kappa$ top-gate integration ($\text{HfO}_2$, $\text{Al}_2\text{O}_3$, or solid polymer electrolytes) compresses depletion width sufficiently to push conventional CMOS metals (Ti, Ag) across the Boundary I/II threshold into the sub-$200\,\Omega\cdot\mu\text{m}$ regime.
2. **P-Type Hole Injection White Space ($\Phi_B < 0.2\,\text{eV}$ for valence band):**
   - High work-function 2D layered metals (e.g., $\text{NbS}_2$, $\text{TaS}_2$) free of high-energy evaporation damage can unlock complementary p-channel 2D logic.

## 4. Implemented Deliverables
- `src/visualization/regime_map_visualizer.py`: 2D phase diagram and work-function mapping visualizer.
- `tests/test_regime_map_visualizer.py`: Unit test suite testing grid generation, boundary tracking, and figure persistence.
- `data/processed/regime_phase_diagram_data.json`: Serialized phase map coordinates and white space catalog.
- `reports/figures/regime_phase_diagram_2d.png`: 2D contour phase diagram with regime boundaries and literature overlays.
- `reports/figures/regime_phase_diagram_workfunction.png`: Contact resistance vs metal work function plot.

## 5. Verification
- `python -m pytest tests/test_regime_map_visualizer.py` passed (1/1 green).
