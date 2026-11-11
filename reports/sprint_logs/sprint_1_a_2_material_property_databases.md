# Sprint 1.a.2: Investigate Existing Material Property Databases

## Objective
Search for and systematically index open-access computational and experimental materials databases that contain baseline elemental, physical, and electronic properties for contact metals and 2D semiconductors ($\text{MoS}_2$).

## Key Findings & Property Catalog
1. **Curated Primary Databases:**
   - **Materials Project:** Provides DFT band structures, formation enthalpies, density of states, and bulk work functions.
   - **Computational 2D Materials Database (C2DB - DTU):** Monolayer-specific electronic properties (PBE/HSE06 bandgaps: ~1.80 eV direct, $m_e^* \approx 0.48 m_0$, out-of-plane dielectric constants).
   - **NIST Chemistry WebBook / Standard Reference Data:** Precision experimental work functions for polycrystalline and crystal-oriented metals.
   - **CRC Handbook of Chemistry & Physics:** Pauling electronegativities, atomic radii, melting temperatures, and electrical resistivities.
   - **OQMD (Open Quantum Materials Database):** Metal-sulfide formation enthalpies ($\Delta H_f$) to model contact interfacial chemical reactivity (e.g., Ti-S reactivity vs noble Au unreactivity).

2. **Extracted Intrinsic Descriptors Table:**
   - Built intrinsic property profiles for 12 key contact metals: Ti, Sc, Au, Pd, Pt, Ni, Cr, Bi, Sb, In, Ag, Mo.
   - Implemented baseline calculation of ideal Schottky-Mott barrier heights: $\Phi_{Bn} = \Phi_M - \chi_s$.

## Deliverables
- `data/reference/material_property_databases.json`: External materials databases registry with API endpoints and priority ratings.
- `src/data/material_databases.py`: Python module containing database registry access, physical property tables, and electronic parameter extractors.
- `tests/test_material_databases.py`: Automated test suite verifying properties and Schottky-Mott calculations.
