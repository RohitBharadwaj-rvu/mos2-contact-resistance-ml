# Sprint 1.b.1: Develop and Test Search Taxonomies

## Objective
Design, calibrate, and test structured keyword taxonomies, boolean operators, synonym expansions, and noise exclusion rules to systematically mine the semiconductor characterization literature for $\text{MoS}_2$ contact resistance and Schottky barrier measurements.

## Taxonomy Architecture
1. **Material Synonyms:** Captures chemical names, acronyms, and thickness dimensions (`"MoS2"`, `"molybdenum disulfide"`, `"monolayer MoS2"`, `"few-layer MoS2"`).
2. **Contact Performance Targets:**
   - Contact resistance & resistivity: `"contact resistance"`, `"specific contact resistivity"`, `"TLM"`, `"transfer length method"`.
   - Schottky barrier & pinning: `"Schottky barrier height"`, `"SBH"`, `"Fermi level pinning"`, `"Schottky-Mott"`, `"thermionic emission"`.
3. **Contact Fabrication & Interface Variables:**
   - Deposition techniques (`"e-beam evaporation"`, `"sputtering"`, `"thermal evaporation"`).
   - Advanced architectures (`"van der Waals contact"`, `"semimetal contact"`, `"1T phase"`, `"transferred contact"`).
   - Post-processing (`"annealing"`, `"forming gas"`).
4. **Noise Filtering:**
   - Eliminates non-device and electrochemical domains: `"photocatalysis"`, `"hydrogen evolution reaction"`, `"solid lubricant"`, `"battery anode"`.

## Deliverables
- `data/reference/search_taxonomies.json`: Formal keyword clusters and tested boolean queries.
- `src/data/search_taxonomies.py`: Query builder with automated syntax validation and balanced parenthetical verification.
- `tests/test_search_taxonomies.py`: Test suite validating boolean composition and syntax integrity.
