# Sprint 1.d.2: Extract Tabular and Textual Values

## Objective
Extract explicitly stated numerical values and categorical descriptions from accepted primary papers, landmark benchmark reviews, and supplementary information tables into the validated schema format.

## Extracted Dataset Summary
- **Volume:** 20 verified experimental device configurations.
- **Contact Materials Represented:**
  - Semimetals: Bi (monolayer exfoliated & CVD), Sb
  - Transferred vdW: Ag, In, Pt
  - Conventional Evaporated: Ti, Au, Sc, Ni, Cr, Mo, Pd
  - Phase Engineered: $1\text{T}\text{-}\text{MoS}_2$
  - Interlayers: Monolayer Graphene, $\text{MoO}_x$
  - Annealed Contacts: Forming gas annealed Ti at $300^\circ\text{C}$
- **Target Distributions:**
  - Width-normalized contact resistance $R_c$: spanning from $123\,\Omega\cdot\mu\text{m}$ (Bi) to $65,000\,\Omega\cdot\mu\text{m}$ (Pt).
  - Schottky barrier height $\Phi_B$: spanning from $0.0\,\text{eV}$ (Bi semimetal) to $1.45\,\text{eV}$ (Pt electron barrier).

## Deliverables
- `data/raw/extracted_tabular_literature_dataset.csv` & `.json`: Schema-validated primary experimental dataset.
- `src/data/tabular_extractor.py`: Extraction loader and validator.
- `tests/test_tabular_extractor.py`: Test suite validating absence of null critical targets and unique IDs.
