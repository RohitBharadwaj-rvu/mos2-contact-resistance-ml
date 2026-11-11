# Sprint 1.e.2: Establish Categorical Taxonomies

## Objective
Normalize and standardize the unstructured, heterogeneous free-text descriptions of contact deposition methods, device architectures, gate dielectrics, and post-annealing ambients into consistent categorical taxonomies.

## Canonical Taxonomies
1. **Deposition Methods:**
   - `E_beam_Evaporation` (electron beam evaporation)
   - `Thermal_Evaporation` (resistive boat thermal evaporation)
   - `Sputtering` (DC/RF magnetron sputtering)
   - `Dry_Transfer` (clean mechanical transfer of pre-patterned vdW metal pads)
   - `Chemical_Treatment` (n-butyl lithium phase transformation)
2. **Contact Architectures:**
   - `Top_Contact` (conventional surface contact)
   - `vdW_Laminated` (transferred metal with pristine vdW interface)
   - `Semimetal_vdW` (Bi 0001, Sb semimetal contacts)
   - `Phase_Engineered_1T` (locally transformed metallic 1T phase)
   - `Interlayer_Buffer` (monolayer graphene, hBN, or thin sub-oxide interlayer)
   - `Edge_Contact` (1D covalent edge contact)
3. **Gate Dielectric:** `SiO2`, `hBN`, `Al2O3`, `HfO2`.
4. **Post-Annealing Gas Ambient:** `None`, `Vacuum`, `Ar`, `Ar/H2_Forming_Gas`, `N2`.

## Deliverables
- `data/reference/categorical_taxonomies.json`: Formal synonym mapping dictionary.
- `src/features/taxonomy_standardizer.py`: Automated parsing and normalization module.
- `tests/test_taxonomy_standardizer.py`: Test suite validating fuzzy synonym resolution.
