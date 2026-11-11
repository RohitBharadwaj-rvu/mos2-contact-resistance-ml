# Sprint 5.c.1 Log: Define Physical Regimes in Contact Behavior

## 1. Objectives & Theoretical Framework
- Formalize the four canonical transport regimes governing carrier injection in nanoscale monolayer and few-layer $\text{MoS}_2$ field-effect transistors.
- Establish quantitative criteria for barrier height ($\Phi_B$), gate carrier density ($n_{2D}$), contact architecture (vdW vs evaporated 3D), and target contact resistance ($R_c$).
- Classify all 20 historical benchmark devices in the master curated database into their physical regimes.

## 2. Definitive Contact Transport Regimes

| Regime | Transport Mechanism | Target $R_c$ Range | $\Phi_B$ Criterion | $n_{2D}$ Criterion | Representative Technologies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Regime I: Quantum-Limited** | Ballistic Landauer-Sharvin transmission; zero tunnel barrier | $\le 200\,\Omega\cdot\mu\text{m}$ ($\le 2.30\,\text{dex}$) | $\Phi_B < 0.15\,\text{eV}$ | $\ge 1.0 \times 10^{13}\,\text{cm}^{-2}$ | Bi(0001) transferred vdW, 1T-MoS2 homojunction, Sb(0001) |
| **Regime II: Thermionic-Field Tunneling** | Fowler-Nordheim / direct tunneling through gate-compressed barrier | $200 - 1,500\,\Omega\cdot\mu\text{m}$ ($2.30 - 3.18\,\text{dex}$) | $\Phi_B \le 0.45\,\text{eV}$ | $\ge 8.0 \times 10^{12}\,\text{cm}^{-2}$ | Ti/Au evaporated + annealed, Ag, In, Sc |
| **Regime III: Thermionic Emission** | Classical Richardson-Dushman thermal emission over barrier | $1,500 - 15,000\,\Omega\cdot\mu\text{m}$ ($3.18 - 4.18\,\text{dex}$) | $\Phi_B \le 0.70\,\text{eV}$ | $\ge 3.0 \times 10^{12}\,\text{cm}^{-2}$ | Au evaporated, Ni, Cr, Mo |
| **Regime IV: Defect Pinned / Freeze-Out** | Metal-induced gap states, vacancy hopping, thermionic freeze-out | $> 15,000\,\Omega\cdot\mu\text{m}$ ($> 4.18\,\text{dex}$) | $\Phi_B > 0.70\,\text{eV}$ | Any | Pt, direct unpassivated evaporated Pd |

## 3. Dataset Distribution & Mapping Results
- **Regime I (Quantum-Limited):** 2 devices ($10\%$). Includes Bi at peak gating ($123\,\Omega\cdot\mu\text{m}$) and 1T metallic phase ($240\,\Omega\cdot\mu\text{m}$).
- **Regime II (Tunneling):** 10 devices ($50\%$). The dominant operating mode of state-of-the-art literature FETs.
- **Regime III (Thermionic):** 7 devices ($35\%$). Typical for standard un-passivated 3D metals (Au, Ni).
- **Regime IV (Defect Pinned):** 1 device ($5\%$). Unpassivated high work-function Pt ($65\,\text{k}\Omega\cdot\mu\text{m}$).

## 4. Implemented Deliverables
- `src/interpretability/regime_definitions.py`: Formal regime catalog and programmatic classifier.
- `tests/test_regime_definitions.py`: Unit test suite testing classification logic and dataset integrity.
- `data/reference/contact_transport_regimes.json`: Serialized catalog and device classifications.

## 5. Verification
- `python -m pytest tests/test_regime_definitions.py` passed (3/3 green).
