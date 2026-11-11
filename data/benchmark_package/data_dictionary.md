# Benchmark Dataset Data Dictionary

**Dataset Title:** MoS2 Contact Resistance & Schottky Barrier Height Benchmark  
**Sample Count:** 20 curated contact devices  
**Total Features:** 44 variables  

| Column Name | Category | Data Type | Physical Units | Description |
| :--- | :--- | :--- | :--- | :--- |
| `device_id` | Identifier | `string` | dimensionless | Unique primary key identifier for each experimental contact device instance. |
| `source_uid` | Provenance | `string` | dimensionless | Unique identifier linking the observation to its peer-reviewed literature source paper. |
| `contact_metal` | Material Specification | `string` | chemical symbol | Elemental or compound chemical formula of the primary contact metal pad (e.g., Bi, Ti, Au, Pt, Ag, Sc, Ni). |
| `layer_count` | Semiconductor Channel | `integer` | monolayers | Number of MoS2 atomic layers in the transistor channel (1 = monolayer, >1 = few-layer). |
| `contact_resistance_ohm_um` | Primary Target | `float` | Ohm*um | Width-normalized contact resistance extracted experimentally via TLM, Y-function, or 4-probe. |
| `log10_contact_resistance_ohm_um` | Primary Target | `float` | log10(Ohm*um) [dex] | Base-10 logarithm of width-normalized contact resistance (ML regression target). |
| `work_function_ev` | Metal Property | `float` | eV | Work function of the clean bulk contact metal in vacuum. |
| `physics_predicted_sbh_ev` | Interface Band Alignment | `float` | eV | Calculated or experimentally determined Schottky barrier height at the metal-MoS2 junction. |
| `gate_carrier_density_cm2` | Electrostatic State | `float` | cm^-2 | Electrostatic gate-induced 2D sheet carrier density accumulated in the MoS2 channel beneath the contact. |
| `is_vdw_or_depinned_contact` | Fabrication Method | `binary integer (0/1)` | indicator | Flag indicating whether contact was fabricated via damage-free van der Waals transfer / phase transformation (1) or evaporated (0). |
| `sulfide_formation_enthalpy_ev` | Interface Chemistry | `float` | eV / atom | Standard Gibbs free formation enthalpy of the metal sulfide compound, proxying interfacial chemical reactivity. |
| `metal_resistivity_ohm_cm` | Metal Property | `float` | Ohm*cm | Bulk room-temperature electrical resistivity of the contact metal. |
| `temperature_k` | Environmental State | `float` | Kelvin | Measurement ambient temperature during electrical characterization. |
| `data_point_id` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: data_point_id |
| `citation_short` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: citation_short |
| `doi` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: doi |
| `semiconductor` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: semiconductor |
| `thickness_nm` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: thickness_nm |
| `flake_synthesis_method` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: flake_synthesis_method |
| `pauling_electronegativity` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: pauling_electronegativity |
| `contact_architecture` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: contact_architecture |
| `adhesion_layer` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: adhesion_layer |
| `deposition_method` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: deposition_method |
| `vacuum_base_pressure_torr` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: vacuum_base_pressure_torr |
| `post_annealing_temperature_c` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: post_annealing_temperature_c |
| `post_annealing_gas_ambient` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: post_annealing_gas_ambient |
| `gate_configuration` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: gate_configuration |
| `gate_dielectric` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: gate_dielectric |
| `measurement_temperature_k` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: measurement_temperature_k |
| `characterization_method` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: characterization_method |
| `contact_resistance_rc_ohm_um` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: contact_resistance_rc_ohm_um |
| `specific_contact_resistivity_ohm_cm2` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: specific_contact_resistivity_ohm_cm2 |
| `schottky_barrier_height_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: schottky_barrier_height_ev |
| `carrier_polarity` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: carrier_polarity |
| `provenance_location` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: provenance_location |
| `notes_and_context` | Engineered / Normalized Feature | `string` | derived/normalized | Engineered physical or statistical feature: notes_and_context |
| `anneal_temp_was_missing` | Engineered / Normalized Feature | `integer` | derived/normalized | Engineered physical or statistical feature: anneal_temp_was_missing |
| `vacuum_pressure_was_missing` | Engineered / Normalized Feature | `integer` | derived/normalized | Engineered physical or statistical feature: vacuum_pressure_was_missing |
| `carrier_density_was_missing` | Engineered / Normalized Feature | `integer` | derived/normalized | Engineered physical or statistical feature: carrier_density_was_missing |
| `sulfide_formation_enthalpy_kj_mol` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: sulfide_formation_enthalpy_kj_mol |
| `d_band_center_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: d_band_center_ev |
| `schottky_mott_barrier_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: schottky_mott_barrier_ev |
| `delta_cnl_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: delta_cnl_ev |
| `electronegativity_diff_sulfur` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: electronegativity_diff_sulfur |
| `effective_pinning_factor_s` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: effective_pinning_factor_s |
| `fermi_level_shift_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: fermi_level_shift_ev |
| `thermal_energy_kbt_ev` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: thermal_energy_kbt_ev |
| `log_vacuum_pressure` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: log_vacuum_pressure |
| `log10_rc` | Engineered / Normalized Feature | `float` | derived/normalized | Engineered physical or statistical feature: log10_rc |