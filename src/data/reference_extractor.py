"""
Unified Elemental and Material Reference Data Extractor.
Extracts, structures, and exports intrinsic physical and electronic constants for candidate contact metals and MoS2.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

CSV_OUT_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "elemental_material_reference.csv"
JSON_OUT_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "elemental_material_reference.json"

EXTENDED_ELEMENTAL_PROPERTIES = [
    {
        "element": "Ti",
        "symbol": "Ti",
        "atomic_number": 22,
        "atomic_weight_amu": 47.867,
        "work_function_ev": 4.33,
        "electronegativity_pauling": 1.54,
        "atomic_radius_pm": 140,
        "covalent_radius_pm": 160,
        "bulk_resistivity_ohm_cm": 4.2e-5,
        "melting_point_k": 1941,
        "first_ionization_energy_ev": 6.828,
        "sulfide_formation_enthalpy_kj_per_mol_s": -270.0,
        "d_band_center_ev": -1.2,
        "crystal_structure": "HCP",
        "metal_type": "Reactive 3d Transition Metal",
        "adhesion_quality": "Excellent"
    },
    {
        "element": "Sc",
        "symbol": "Sc",
        "atomic_number": 21,
        "atomic_weight_amu": 44.956,
        "work_function_ev": 3.50,
        "electronegativity_pauling": 1.36,
        "atomic_radius_pm": 160,
        "covalent_radius_pm": 170,
        "bulk_resistivity_ohm_cm": 5.6e-5,
        "melting_point_k": 1814,
        "first_ionization_energy_ev": 6.561,
        "sulfide_formation_enthalpy_kj_per_mol_s": -340.0,
        "d_band_center_ev": -1.0,
        "crystal_structure": "HCP",
        "metal_type": "Low Work Function Transition Metal",
        "adhesion_quality": "High"
    },
    {
        "element": "Au",
        "symbol": "Au",
        "atomic_number": 79,
        "atomic_weight_amu": 196.967,
        "work_function_ev": 5.10,
        "electronegativity_pauling": 2.54,
        "atomic_radius_pm": 135,
        "covalent_radius_pm": 136,
        "bulk_resistivity_ohm_cm": 2.2e-6,
        "melting_point_k": 1337,
        "first_ionization_energy_ev": 9.225,
        "sulfide_formation_enthalpy_kj_per_mol_s": -15.0,
        "d_band_center_ev": -3.5,
        "crystal_structure": "FCC",
        "metal_type": "Noble Metal",
        "adhesion_quality": "Poor (requires adhesion layer)"
    },
    {
        "element": "Pd",
        "symbol": "Pd",
        "atomic_number": 46,
        "atomic_weight_amu": 106.42,
        "work_function_ev": 5.22,
        "electronegativity_pauling": 2.20,
        "atomic_radius_pm": 137,
        "covalent_radius_pm": 139,
        "bulk_resistivity_ohm_cm": 1.05e-5,
        "melting_point_k": 1828,
        "first_ionization_energy_ev": 8.337,
        "sulfide_formation_enthalpy_kj_per_mol_s": -85.0,
        "d_band_center_ev": -2.1,
        "crystal_structure": "FCC",
        "metal_type": "High Work Function Noble Metal",
        "adhesion_quality": "Moderate"
    },
    {
        "element": "Pt",
        "symbol": "Pt",
        "atomic_number": 78,
        "atomic_weight_amu": 195.084,
        "work_function_ev": 5.65,
        "electronegativity_pauling": 2.28,
        "atomic_radius_pm": 135,
        "covalent_radius_pm": 136,
        "bulk_resistivity_ohm_cm": 1.06e-5,
        "melting_point_k": 2041,
        "first_ionization_energy_ev": 8.959,
        "sulfide_formation_enthalpy_kj_per_mol_s": -60.0,
        "d_band_center_ev": -2.4,
        "crystal_structure": "FCC",
        "metal_type": "High Work Function Refractory Noble",
        "adhesion_quality": "Moderate"
    },
    {
        "element": "Ni",
        "symbol": "Ni",
        "atomic_number": 28,
        "atomic_weight_amu": 58.693,
        "work_function_ev": 5.15,
        "electronegativity_pauling": 1.91,
        "atomic_radius_pm": 124,
        "covalent_radius_pm": 124,
        "bulk_resistivity_ohm_cm": 6.9e-6,
        "melting_point_k": 1728,
        "first_ionization_energy_ev": 7.639,
        "sulfide_formation_enthalpy_kj_per_mol_s": -82.0,
        "d_band_center_ev": -1.8,
        "crystal_structure": "FCC",
        "metal_type": "Ferromagnetic 3d Metal",
        "adhesion_quality": "Good"
    },
    {
        "element": "Cr",
        "symbol": "Cr",
        "atomic_number": 24,
        "atomic_weight_amu": 51.996,
        "work_function_ev": 4.50,
        "electronegativity_pauling": 1.66,
        "atomic_radius_pm": 128,
        "covalent_radius_pm": 139,
        "bulk_resistivity_ohm_cm": 1.25e-5,
        "melting_point_k": 2180,
        "first_ionization_energy_ev": 6.766,
        "sulfide_formation_enthalpy_kj_per_mol_s": -130.0,
        "d_band_center_ev": -1.5,
        "crystal_structure": "BCC",
        "metal_type": "Reactive Adhesion Layer",
        "adhesion_quality": "Very High"
    },
    {
        "element": "Bi",
        "symbol": "Bi",
        "atomic_number": 83,
        "atomic_weight_amu": 208.980,
        "work_function_ev": 4.22,
        "electronegativity_pauling": 2.02,
        "atomic_radius_pm": 156,
        "covalent_radius_pm": 148,
        "bulk_resistivity_ohm_cm": 1.07e-4,
        "melting_point_k": 544,
        "first_ionization_energy_ev": 7.289,
        "sulfide_formation_enthalpy_kj_per_mol_s": -70.0,
        "d_band_center_ev": -6.0,
        "crystal_structure": "Rhombohedral",
        "metal_type": "Semimetal (Zero DOS at Fermi Level)",
        "adhesion_quality": "vdW Clean Interface"
    },
    {
        "element": "Sb",
        "symbol": "Sb",
        "atomic_number": 51,
        "atomic_weight_amu": 121.760,
        "work_function_ev": 4.55,
        "electronegativity_pauling": 2.05,
        "atomic_radius_pm": 140,
        "covalent_radius_pm": 139,
        "bulk_resistivity_ohm_cm": 4.17e-5,
        "melting_point_k": 904,
        "first_ionization_energy_ev": 8.608,
        "sulfide_formation_enthalpy_kj_per_mol_s": -80.0,
        "d_band_center_ev": -5.2,
        "crystal_structure": "Rhombohedral",
        "metal_type": "Semimetal (vdW Gapless)",
        "adhesion_quality": "vdW Clean Interface"
    },
    {
        "element": "In",
        "symbol": "In",
        "atomic_number": 49,
        "atomic_weight_amu": 114.818,
        "work_function_ev": 4.12,
        "electronegativity_pauling": 1.78,
        "atomic_radius_pm": 167,
        "covalent_radius_pm": 142,
        "bulk_resistivity_ohm_cm": 8.37e-6,
        "melting_point_k": 430,
        "first_ionization_energy_ev": 5.786,
        "sulfide_formation_enthalpy_kj_per_mol_s": -110.0,
        "d_band_center_ev": -5.5,
        "crystal_structure": "Tetragonal",
        "metal_type": "Post-transition Low-Melting Metal",
        "adhesion_quality": "Moderate"
    },
    {
        "element": "Ag",
        "symbol": "Ag",
        "atomic_number": 47,
        "atomic_weight_amu": 107.868,
        "work_function_ev": 4.26,
        "electronegativity_pauling": 1.93,
        "atomic_radius_pm": 145,
        "covalent_radius_pm": 145,
        "bulk_resistivity_ohm_cm": 1.59e-6,
        "melting_point_k": 1235,
        "first_ionization_energy_ev": 7.576,
        "sulfide_formation_enthalpy_kj_per_mol_s": -32.0,
        "d_band_center_ev": -4.2,
        "crystal_structure": "FCC",
        "metal_type": "High-Conductivity Noble Metal",
        "adhesion_quality": "Moderate"
    },
    {
        "element": "Mo",
        "symbol": "Mo",
        "atomic_number": 42,
        "atomic_weight_amu": 95.95,
        "work_function_ev": 4.60,
        "electronegativity_pauling": 2.16,
        "atomic_radius_pm": 139,
        "covalent_radius_pm": 154,
        "bulk_resistivity_ohm_cm": 5.2e-6,
        "melting_point_k": 2896,
        "first_ionization_energy_ev": 7.092,
        "sulfide_formation_enthalpy_kj_per_mol_s": -145.0,
        "d_band_center_ev": -1.9,
        "crystal_structure": "BCC",
        "metal_type": "Refractory Transition Metal",
        "adhesion_quality": "High"
    },
    {
        "element": "W",
        "symbol": "W",
        "atomic_number": 74,
        "atomic_weight_amu": 183.84,
        "work_function_ev": 4.55,
        "electronegativity_pauling": 2.36,
        "atomic_radius_pm": 139,
        "covalent_radius_pm": 162,
        "bulk_resistivity_ohm_cm": 5.28e-6,
        "melting_point_k": 3695,
        "first_ionization_energy_ev": 7.864,
        "sulfide_formation_enthalpy_kj_per_mol_s": -130.0,
        "d_band_center_ev": -2.2,
        "crystal_structure": "BCC",
        "metal_type": "Ultra-Refractory Metal",
        "adhesion_quality": "High"
    },
    {
        "element": "Cu",
        "symbol": "Cu",
        "atomic_number": 29,
        "atomic_weight_amu": 63.546,
        "work_function_ev": 4.65,
        "electronegativity_pauling": 1.90,
        "atomic_radius_pm": 128,
        "covalent_radius_pm": 132,
        "bulk_resistivity_ohm_cm": 1.68e-6,
        "melting_point_k": 1358,
        "first_ionization_energy_ev": 7.726,
        "sulfide_formation_enthalpy_kj_per_mol_s": -40.0,
        "d_band_center_ev": -2.7,
        "crystal_structure": "FCC",
        "metal_type": "Interconnect Noble Metal",
        "adhesion_quality": "Moderate"
    },
    {
        "element": "Al",
        "symbol": "Al",
        "atomic_number": 13,
        "atomic_weight_amu": 26.982,
        "work_function_ev": 4.28,
        "electronegativity_pauling": 1.61,
        "atomic_radius_pm": 143,
        "covalent_radius_pm": 121,
        "bulk_resistivity_ohm_cm": 2.65e-6,
        "melting_point_k": 933,
        "first_ionization_energy_ev": 5.986,
        "sulfide_formation_enthalpy_kj_per_mol_s": -170.0,
        "d_band_center_ev": -6.5,
        "crystal_structure": "FCC",
        "metal_type": "Post-transition Reactive Metal",
        "adhesion_quality": "High (Forms native oxide)"
    },
    {
        "element": "Y",
        "symbol": "Y",
        "atomic_number": 39,
        "atomic_weight_amu": 88.906,
        "work_function_ev": 3.10,
        "electronegativity_pauling": 1.22,
        "atomic_radius_pm": 180,
        "covalent_radius_pm": 190,
        "bulk_resistivity_ohm_cm": 5.96e-5,
        "melting_point_k": 1799,
        "first_ionization_energy_ev": 6.217,
        "sulfide_formation_enthalpy_kj_per_mol_s": -350.0,
        "d_band_center_ev": -0.8,
        "crystal_structure": "HCP",
        "metal_type": "Rare-earth Low-WF Metal",
        "adhesion_quality": "High"
    }
]


def export_reference_dataset() -> Dict[str, Path]:
    """Exports reference data to both CSV and JSON."""
    CSV_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(EXTENDED_ELEMENTAL_PROPERTIES)
    df.to_csv(CSV_OUT_PATH, index=False)
    
    with open(JSON_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(EXTENDED_ELEMENTAL_PROPERTIES, f, indent=2)
        
    return {"csv": CSV_OUT_PATH, "json": JSON_OUT_PATH}


def load_reference_dataframe() -> pd.DataFrame:
    """Loads the reference dataset as a Pandas DataFrame."""
    if not CSV_OUT_PATH.exists():
        export_reference_dataset()
    return pd.read_csv(CSV_OUT_PATH)
