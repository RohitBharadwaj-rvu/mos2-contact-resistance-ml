# Sprint 1.e.1: Audit and Standardize Units

## Objective
Inspect and resolve all unit discrepancies across literature sources, establishing mathematically rigorous conversion functions to bring contact resistance, barrier heights, temperatures, pressures, thicknesses, and carrier densities into uniform standard units.

## Standardized Dimensions & Conversions
1. **Contact Resistance ($R_c$):** Standardized to $\Omega\cdot\mu\text{m}$.
   - $1\,\text{k}\Omega\cdot\mu\text{m} \to 1000\,\Omega\cdot\mu\text{m}$
   - $1\,\Omega\cdot\text{mm} \to 1000\,\Omega\cdot\mu\text{m}$
   - Absolute $R_{c,abs}\,[\Omega] \times W\,[\mu\text{m}] \to \Omega\cdot\mu\text{m}$
2. **Schottky Barrier Height ($\Phi_B$):** Standardized to $\text{eV}$.
   - $1\,\text{meV} \to 10^{-3}\,\text{eV}$
3. **Temperature ($T$):** Standardized to $\text{K}$.
   - $T[^\circ\text{C}] + 273.15 \to T[\text{K}]$
4. **Vacuum Chamber Pressure ($P$):** Standardized to $\text{Torr}$.
   - $1\,\text{mbar} \to 0.750062\,\text{Torr}$; $1\,\text{Pa} \to 0.00750062\,\text{Torr}$
5. **Semiconductor Thickness ($t$):** Standardized to $\text{nm}$.
   - Monolayer $\text{MoS}_2 = 0.65\,\text{nm}$; $1\,\text{\AA} = 0.1\,\text{nm}$
6. **Electrostatic Carrier Density ($n_{2D}$):** Standardized to $\text{cm}^{-2}$.
   - Calculated via capacitive overdrive: $n_{2D} = \frac{\varepsilon_0 \varepsilon_r}{q t_{ox}} (V_{gs} - V_{th})$.

## Deliverables
- `src/features/unit_standardizer.py`: Conversion and unit audit module.
- `tests/test_unit_standardizer.py`: Unit tests validating mathematical conversions.
