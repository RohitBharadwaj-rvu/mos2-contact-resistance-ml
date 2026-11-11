"""
Material Property Database Registry and Baseline Physical Property Extractors.
Provides physical, thermodynamic, and electronic constants for candidate contact metals and MoS2.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "material_property_databases.json"

# Curated reference physical properties from NIST / CRC / Materials Project / C2DB
# Properties:
# - work_function_ev: Experimental work function (eV)
# - electronegativity_pauling: Pauling electronegativity
# - atomic_radius_pm: Empirical atomic radius in picometers
# - resistivity_ohm_cm: Bulk electrical resistivity (Ohm*cm) at 293K
# - melting_point_k: Melting temperature (K)
# - standard_sulfide_enthalpy_kj_mol: Enthalpy of formation for the most stable metal sulfide (kJ/mol per S)
# - d_band_center_ev: Approximate d-band center relative to Fermi level (eV)
BASELINE_METAL_PROPERTIES = {
    "Ti": {
        "atomic_number": 22,
        "work_function_ev": 4.33,
        "electronegativity_pauling": 1.54,
        "atomic_radius_pm": 140,
        "resistivity_ohm_cm": 4.2e-5,
        "melting_point_k": 1941,
        "standard_sulfide_enthalpy_kj_mol": -270.0,  # TiS2 formation per mol S
        "d_band_center_ev": -1.2,
        "crystal_structure": "HCP",
        "contact_class": "reactive_3d_metal"
    },
    "Sc": {
        "atomic_number": 21,
        "work_function_ev": 3.50,
        "electronegativity_pauling": 1.36,
        "atomic_radius_pm": 160,
        "resistivity_ohm_cm": 5.6e-5,
        "melting_point_k": 1814,
        "standard_sulfide_enthalpy_kj_mol": -340.0,
        "d_band_center_ev": -1.0,
        "crystal_structure": "HCP",
        "contact_class": "low_workfunction_reactive"
    },
    "Au": {
        "atomic_number": 79,
        "work_function_ev": 5.10,
        "electronegativity_pauling": 2.54,
        "atomic_radius_pm": 135,
        "resistivity_ohm_cm": 2.2e-6,
        "melting_point_k": 1337,
        "standard_sulfide_enthalpy_kj_mol": -15.0,  # weakly reactive
        "d_band_center_ev": -3.5,
        "crystal_structure": "FCC",
        "contact_class": "noble_metal"
    },
    "Pd": {
        "atomic_number": 46,
        "work_function_ev": 5.22,
        "electronegativity_pauling": 2.20,
        "atomic_radius_pm": 137,
        "resistivity_ohm_cm": 1.05e-5,
        "melting_point_k": 1828,
        "standard_sulfide_enthalpy_kj_mol": -85.0,
        "d_band_center_ev": -2.1,
        "crystal_structure": "FCC",
        "contact_class": "high_workfunction_p_type"
    },
    "Pt": {
        "atomic_number": 78,
        "work_function_ev": 5.65,
        "electronegativity_pauling": 2.28,
        "atomic_radius_pm": 135,
        "resistivity_ohm_cm": 1.06e-5,
        "melting_point_k": 2041,
        "standard_sulfide_enthalpy_kj_mol": -60.0,
        "d_band_center_ev": -2.4,
        "crystal_structure": "FCC",
        "contact_class": "high_workfunction_noble"
    },
    "Ni": {
        "atomic_number": 28,
        "work_function_ev": 5.15,
        "electronegativity_pauling": 1.91,
        "atomic_radius_pm": 124,
        "resistivity_ohm_cm": 6.9e-6,
        "melting_point_k": 1728,
        "standard_sulfide_enthalpy_kj_mol": -82.0,
        "d_band_center_ev": -1.8,
        "crystal_structure": "FCC",
        "contact_class": "reactive_3d_metal"
    },
    "Cr": {
        "atomic_number": 24,
        "work_function_ev": 4.50,
        "electronegativity_pauling": 1.66,
        "atomic_radius_pm": 128,
        "resistivity_ohm_cm": 1.25e-5,
        "melting_point_k": 2180,
        "standard_sulfide_enthalpy_kj_mol": -130.0,
        "d_band_center_ev": -1.5,
        "crystal_structure": "BCC",
        "contact_class": "adhesion_layer"
    },
    "Bi": {
        "atomic_number": 83,
        "work_function_ev": 4.22,
        "electronegativity_pauling": 2.02,
        "atomic_radius_pm": 156,
        "resistivity_ohm_cm": 1.07e-4,
        "melting_point_k": 544,
        "standard_sulfide_enthalpy_kj_mol": -70.0,
        "d_band_center_ev": -6.0,  # Semimetal, p-band density at Fermi level
        "crystal_structure": "Rhombohedral",
        "contact_class": "semimetal_vdw_gapless"
    },
    "Sb": {
        "atomic_number": 51,
        "work_function_ev": 4.55,
        "electronegativity_pauling": 2.05,
        "atomic_radius_pm": 140,
        "resistivity_ohm_cm": 4.17e-5,
        "melting_point_k": 904,
        "standard_sulfide_enthalpy_kj_mol": -80.0,
        "d_band_center_ev": -5.2,
        "crystal_structure": "Rhombohedral",
        "contact_class": "semimetal_vdw_gapless"
    },
    "In": {
        "atomic_number": 49,
        "work_function_ev": 4.12,
        "electronegativity_pauling": 1.78,
        "atomic_radius_pm": 167,
        "resistivity_ohm_cm": 8.37e-6,
        "melting_point_k": 430,
        "standard_sulfide_enthalpy_kj_mol": -110.0,
        "d_band_center_ev": -5.5,
        "crystal_structure": "Tetragonal",
        "contact_class": "low_melting_vdw"
    },
    "Ag": {
        "atomic_number": 47,
        "work_function_ev": 4.26,
        "electronegativity_pauling": 1.93,
        "atomic_radius_pm": 145,
        "resistivity_ohm_cm": 1.59e-6,
        "melting_point_k": 1235,
        "standard_sulfide_enthalpy_kj_mol": -32.0,
        "d_band_center_ev": -4.2,
        "crystal_structure": "FCC",
        "contact_class": "noble_metal"
    },
    "Mo": {
        "atomic_number": 42,
        "work_function_ev": 4.60,
        "electronegativity_pauling": 2.16,
        "atomic_radius_pm": 139,
        "resistivity_ohm_cm": 5.2e-6,
        "melting_point_k": 2896,
        "standard_sulfide_enthalpy_kj_mol": -145.0,
        "d_band_center_ev": -1.9,
        "crystal_structure": "BCC",
        "contact_class": "refractory_metal"
    },
    "W": {
        "atomic_number": 74,
        "work_function_ev": 4.55,
        "electronegativity_pauling": 2.36,
        "atomic_radius_pm": 139,
        "resistivity_ohm_cm": 5.28e-6,
        "melting_point_k": 3695,
        "standard_sulfide_enthalpy_kj_mol": -130.0,
        "d_band_center_ev": -2.2,
        "crystal_structure": "BCC",
        "contact_class": "refractory_metal"
    },
    "Cu": {
        "atomic_number": 29,
        "work_function_ev": 4.65,
        "electronegativity_pauling": 1.90,
        "atomic_radius_pm": 128,
        "resistivity_ohm_cm": 1.68e-6,
        "melting_point_k": 1358,
        "standard_sulfide_enthalpy_kj_mol": -40.0,
        "d_band_center_ev": -2.7,
        "crystal_structure": "FCC",
        "contact_class": "noble_metal"
    },
    "Al": {
        "atomic_number": 13,
        "work_function_ev": 4.28,
        "electronegativity_pauling": 1.61,
        "atomic_radius_pm": 143,
        "resistivity_ohm_cm": 2.65e-6,
        "melting_point_k": 933,
        "standard_sulfide_enthalpy_kj_mol": -170.0,
        "d_band_center_ev": -6.5,
        "crystal_structure": "FCC",
        "contact_class": "reactive_low_wf"
    },
    "Y": {
        "atomic_number": 39,
        "work_function_ev": 3.10,
        "electronegativity_pauling": 1.22,
        "atomic_radius_pm": 180,
        "resistivity_ohm_cm": 5.96e-5,
        "melting_point_k": 1799,
        "standard_sulfide_enthalpy_kj_mol": -350.0,
        "d_band_center_ev": -0.8,
        "crystal_structure": "HCP",
        "contact_class": "low_workfunction_reactive"
    },
    "Graphene": {
        "atomic_number": 6,
        "work_function_ev": 4.50,
        "electronegativity_pauling": 2.55,
        "atomic_radius_pm": 77,
        "resistivity_ohm_cm": 1.0e-5,
        "melting_point_k": 3800,
        "standard_sulfide_enthalpy_kj_mol": 0.0,
        "d_band_center_ev": -4.5,
        "crystal_structure": "2D_Hexagonal",
        "contact_class": "2d_vdw_interlayer"
    }
}

MOS2_BASELINE_PROPERTIES = {
    "monolayer": {
        "bandgap_direct_ev": 1.80,
        "electron_affinity_ev": 4.20,
        "work_function_ev": 5.25,
        "effective_mass_electrons_m0": 0.48,
        "effective_mass_holes_m0": 0.60,
        "thickness_nm": 0.65,
        "dielectric_constant_in_plane": 4.8,
        "dielectric_constant_out_of_plane": 3.0
    },
    "bilayer": {
        "bandgap_indirect_ev": 1.60,
        "electron_affinity_ev": 4.25,
        "work_function_ev": 5.15,
        "effective_mass_electrons_m0": 0.52,
        "thickness_nm": 1.30
    },
    "few_layer_3_to_5": {
        "bandgap_indirect_ev": 1.40,
        "electron_affinity_ev": 4.30,
        "work_function_ev": 5.05,
        "effective_mass_electrons_m0": 0.55,
        "thickness_nm": 2.60
    },
    "bulk": {
        "bandgap_indirect_ev": 1.23,
        "electron_affinity_ev": 4.35,
        "work_function_ev": 4.90,
        "effective_mass_electrons_m0": 0.58,
        "thickness_nm": 10.0
    }
}


def load_material_databases() -> List[Dict[str, Any]]:
    """Loads the catalog of external material property databases."""
    if not DB_REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Database registry not found at {DB_REGISTRY_PATH}")
    with open(DB_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_metal_properties(metal_symbol: str) -> Optional[Dict[str, Any]]:
    """Retrieves physical constants for a given contact metal."""
    return BASELINE_METAL_PROPERTIES.get(metal_symbol)


def get_mos2_properties(thickness_category: str = "monolayer") -> Optional[Dict[str, Any]]:
    """Retrieves electronic properties for MoS2 by thickness category."""
    return MOS2_BASELINE_PROPERTIES.get(thickness_category)


def compute_schottky_mott_barrier(metal_symbol: str, thickness_category: str = "monolayer") -> Optional[float]:
    """
    Computes theoretical n-type Schottky barrier height under the Schottky-Mott limit:
    Phi_Bn_theoretical = Phi_M - Chi_semiconductor
    """
    metal = get_metal_properties(metal_symbol)
    mos2 = get_mos2_properties(thickness_category)
    if not metal or not mos2:
        return None
    phi_m = metal["work_function_ev"]
    chi_s = mos2["electron_affinity_ev"]
    return round(phi_m - chi_s, 3)


def compute_gate_modulated_fermi_shift(carrier_density_cm2: float, effective_mass_m0: float = 0.48) -> float:
    """
    Computes the 2D degenerate Fermi level shift relative to the conduction band minimum (E_F - E_C):
    Delta_E_F = (pi * hbar^2 / m*) * n_2D
    For monolayer MoS2 with g_v = 2, g_s = 2 (valley and spin degeneracy = 4, but strong spin-orbit split):
    m* = effective_mass_m0 * m_e (where m_e = 9.109e-31 kg).
    Returns shift in eV (positive means E_F is above conduction band edge).
    """
    import math
    if carrier_density_cm2 <= 0:
        return 0.0
    hbar = 1.054571817e-34  # J*s
    m_e = 9.1093837e-31     # kg
    q = 1.602176634e-19     # C (eV conversion)
    m_star = effective_mass_m0 * m_e
    n_m2 = carrier_density_cm2 * 1e4
    # 2D DOS g_2d = g_v * g_s * m* / (2 * pi * hbar^2) = 2 * m* / (pi * hbar^2) with g_v=1, g_s=2
    # n_2d = g_2d * Delta_E
    # Delta_E = n_2d / g_2d = (pi * hbar^2 / (2 * m*)) * n_2d
    delta_e_joules = (math.pi * (hbar ** 2) / (2.0 * m_star)) * n_m2
    delta_e_ev = delta_e_joules / q
    return round(delta_e_ev, 4)

