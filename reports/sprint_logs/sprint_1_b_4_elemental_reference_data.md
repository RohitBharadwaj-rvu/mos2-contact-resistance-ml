# Sprint 1.b.4: Extract Elemental & Material Reference Data

## Objective
Extract and structure a unified high-precision dataset of fundamental physical, electronic, thermodynamic, and mechanical constants for all candidate contact metals (Ti, Sc, Au, Pd, Pt, Ni, Cr, Bi, Sb, In, Ag, Mo, W, Cu, Al, Y) and $\text{MoS}_2$ layers.

## Extracted Material Properties
1. **Physical Constants:**
   - Work function ($\Phi_M$ in eV)
   - Pauling electronegativity ($\chi_P$)
   - Atomic and covalent radii ($r_{atom}, r_{cov}$ in pm)
   - Bulk electrical resistivity ($\rho$ in $\Omega\cdot\text{cm}$)
   - Melting point ($T_m$ in K)
   - First ionization energy ($IE_1$ in eV)
2. **Interface & Reactivity Descriptors:**
   - Standard sulfide formation enthalpy ($\Delta H_f^\circ$ in kJ/mol per S atom) representing chemical reactivity with sulfur atoms.
   - d-band center position relative to $E_F$ ($\epsilon_d - E_F$ in eV) controlling hybridization with Mo $4d$ and S $3p$ orbitals.
   - Crystal structure (HCP, FCC, BCC, Rhombohedral, Tetragonal).
   - Qualitative interface adhesion and contact classifications.

## Deliverables
- `data/processed/elemental_material_reference.csv`: Tabular CSV of all 16 contact elements.
- `data/processed/elemental_material_reference.json`: Structured JSON catalog.
- `src/data/reference_extractor.py`: Extraction and loading module.
- `tests/test_reference_extractor.py`: Test suite validating physical boundaries and format consistency.
