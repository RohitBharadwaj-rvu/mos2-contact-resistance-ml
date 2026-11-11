# Sprint 4.d.1 Log: Select Input Variables for Equation Search

## 1. Objectives & Selection Criteria
- Identify a compact set of 3 to 4 primary solid-state physical descriptors for symbolic regression equation discovery.
- Prevent combinatorial explosion during genetic tree mutation/crossover.
- Scale variables into well-conditioned, dimensionless $O(1)$ numerical domains to prevent arithmetic underflow/overflow or genetic algorithm stalling on extreme scale discrepancies.

## 2. Selected Descriptors & Dimensional Scaling

1. **$x_{\text{sbh}}$ (Schottky Barrier Height, $\Phi_B$):**
   - Source feature: `physics_predicted_sbh_ev`
   - Range: $[0.0, 1.38]\,\text{eV}$
   - Scaling: Identity ($\Phi_B / 1\,\text{eV}$)
   - Correlation: $r = +0.7630$, $\rho = +0.7542$. Strongest positive physical driver of contact resistance.

2. **$x_{\text{n2d}}$ (Normalized Gate Carrier Density, $\tilde{n}_{2D}$):**
   - Source feature: `gate_carrier_density_cm2`
   - Raw range: $3.0 \times 10^{12} - 1.5 \times 10^{13}\,\text{cm}^{-2}$
   - Scaling: $\tilde{n}_{2D} = n_{2D} / 10^{13}\,\text{cm}^{-2} \in [0.3, 1.5]$
   - Correlation: $r = -0.7862$, $\rho = -0.8243$. Dominant electrostatic gate modulation.

3. **$x_{\text{vdw}}$ (Interface De-pinning Flag, $\delta_{\text{vdW}}$):**
   - Source feature: `is_vdw_or_depinned_contact`
   - Range: $\{0.0, 1.0\}$
   - Scaling: Identity
   - Correlation: $r = -0.3725$, $\rho = -0.5316$. Captures clean van der Waals contact interfaces free of Fermi-level pinning.

4. **$x_{\text{hf}}$ (Normalized Metal Sulfide Enthalpy, $\Delta \tilde{H}_f$):**
   - Source feature: `sulfide_formation_enthalpy_kj_mol`
   - Range: $[0.0, 0.68]$
   - Scaling: $\Delta \tilde{H}_f = -\Delta H_f / 500\,\text{kJ/mol}$
   - Correlation: $r = -0.0933$, $\rho = +0.0483$. Interfacial chemical reaction affinity.

## 3. Implemented Deliverables
- `src/models/symbolic_variable_selector.py`: Feature selection, normalization engine, and target correlation computation.
- `tests/test_symbolic_variable_selector.py`: Verification tests for definitions, scaling bounds, and dataset shapes.
- `data/reference/symbolic_input_variables.json`: Structured variable specifications and correlations.

## 4. Verification & Validation
- Ran `python -m pytest tests/test_symbolic_variable_selector.py` — 2/2 passed (100% green).
