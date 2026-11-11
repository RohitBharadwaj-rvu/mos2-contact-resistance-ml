# Sprint 1.d.1: Design the Raw Data Extraction Schema

## Objective
Design and implement a structured, physics-informed data extraction schema and validation protocol capturing all necessary semiconductor properties, contact architectures, fabrication recipes, environmental conditions, and target metrics.

## Schema Architecture & Key Attributes
1. **Source & Provenance Attributes:**
   - `data_point_id`, `source_uid`, `citation_short`, `doi`, `provenance_location` (exact figure/table/page).
2. **Semiconductor & Flake Descriptors:**
   - `semiconductor` (default `MoS2`), `layer_count` (1 for monolayer, 2 for bilayer, integer or `bulk`), `thickness_nm`, `flake_synthesis_method` (`Mechanical_Exfoliation`, `CVD`, etc.).
3. **Contact Metal & Interface Engineering:**
   - `contact_metal` (Ti, Bi, Sc, Au, Pd, etc.), `work_function_ev`, `pauling_electronegativity`, `contact_architecture` (`Top_Contact`, `Semimetal_vdW`, `Phase_Engineered_1T`, `vdW_Laminated`, etc.), `deposition_method` (`E_beam_Evaporation`, `Thermal_Evaporation`, `Dry_Transfer`), `adhesion_layer`.
4. **Processing & Geometry Parameters:**
   - `post_annealing_temperature_c`, `post_annealing_gas_ambient`, `gate_configuration`, `gate_dielectric`, `gate_carrier_density_cm2`.
5. **Characterization Metrology & Targets:**
   - `measurement_temperature_k`, `characterization_method` (`TLM`, `Four_Probe_Hall`, `Richardson_Arrhenius`), `contact_resistance_rc_ohm_um`, `specific_contact_resistivity_ohm_cm2`, `schottky_barrier_height_ev`, `carrier_polarity` (`n_type`, `p_type`).

## Deliverables
- `data/reference/extraction_schema.json`: Formal JSON Schema declaring rules, enums, boundaries, and required keys.
- `src/data/extraction_schema.py`: Python module providing validation, template generation, and constraint enforcement.
- `tests/test_extraction_schema.py`: Test suite validating schema integrity and constraint bounds.
