"""
Physics-Informed Domain Feature Engineering Pipeline for MoS2 Contacts.
Computes Schottky-Mott mismatch, Fermi pinning descriptors, chemical reactivity, and degenerate gate factors.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

from src.data.material_databases import BASELINE_METAL_PROPERTIES, MOS2_BASELINE_PROPERTIES, compute_gate_modulated_fermi_shift


def enrich_dataset_with_physics_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches tabular contact dataset with domain-specific physical descriptors.
    """
    df_feat = df.copy()
    
    # Fundamental semiconductor reference values
    chi_s = MOS2_BASELINE_PROPERTIES["monolayer"]["electron_affinity_ev"]  # 4.20 eV
    e_cnl_ev = 4.42  # Charge Neutrality Level relative to vacuum (0.22 eV below Ec)
    chi_sulfur = 2.58  # Pauling electronegativity of Sulfur
    
    # 1. Merge baseline elemental constants if missing
    def get_metal_prop(row, prop_name, default_val=None):
        metal = row.get("contact_metal")
        if metal in BASELINE_METAL_PROPERTIES and prop_name in BASELINE_METAL_PROPERTIES[metal]:
            return BASELINE_METAL_PROPERTIES[metal][prop_name]
        return default_val

    if "work_function_ev" not in df_feat.columns or df_feat["work_function_ev"].isnull().any():
        df_feat["work_function_ev"] = df_feat.apply(
            lambda r: r["work_function_ev"] if pd.notnull(r.get("work_function_ev")) else get_metal_prop(r, "work_function_ev", 4.5),
            axis=1
        )
        
    if "pauling_electronegativity" not in df_feat.columns or df_feat["pauling_electronegativity"].isnull().any():
        df_feat["pauling_electronegativity"] = df_feat.apply(
            lambda r: r["pauling_electronegativity"] if pd.notnull(r.get("pauling_electronegativity")) else get_metal_prop(r, "electronegativity_pauling", 2.0),
            axis=1
        )
        
    # Sulfide formation enthalpy and d-band center
    df_feat["sulfide_formation_enthalpy_kj_mol"] = df_feat.apply(
        lambda r: get_metal_prop(r, "standard_sulfide_enthalpy_kj_mol", -100.0),
        axis=1
    )
    df_feat["d_band_center_ev"] = df_feat.apply(
        lambda r: get_metal_prop(r, "d_band_center_ev", -2.0),
        axis=1
    )
    df_feat["metal_resistivity_ohm_cm"] = df_feat.apply(
        lambda r: get_metal_prop(r, "resistivity_ohm_cm", 1.0e-5),
        axis=1
    )

    # 2. Physics Descriptors:
    # A. Schottky-Mott ideal barrier: Phi_M - Chi_S
    df_feat["schottky_mott_barrier_ev"] = df_feat["work_function_ev"] - chi_s
    
    # B. Distance of metal work function from MoS2 Charge Neutrality Level (CNL)
    df_feat["delta_cnl_ev"] = df_feat["work_function_ev"] - e_cnl_ev
    
    # C. Electronegativity difference with Sulfur (chemical reaction driving force)
    df_feat["electronegativity_diff_sulfur"] = np.abs(df_feat["pauling_electronegativity"] - chi_sulfur)
    
    # D. vdW / Clean interface indicator
    # 1 for Semimetal_vdW, vdW_Laminated, Phase_Engineered_1T, Interlayer_Buffer
    vdw_architectures = ["Semimetal_vdW", "vdW_Laminated", "Phase_Engineered_1T", "Interlayer_Buffer"]
    df_feat["is_vdw_or_depinned_contact"] = df_feat["contact_architecture"].apply(
        lambda arch: 1.0 if arch in vdw_architectures else 0.0
    )
    
    # E. Fermi-level pinning factor estimate S:
    # Unpinned vdW contacts: S ~ 0.95; Evaporated 3D contacts: S ~ 0.15
    df_feat["effective_pinning_factor_s"] = df_feat["is_vdw_or_depinned_contact"].apply(
        lambda is_vdw: 0.95 if is_vdw == 1.0 else 0.15
    )
    
    # F. Gate-modulated Fermi level degenerate shift Delta_E_F
    carrier_densities = df_feat["gate_carrier_density_cm2"].fillna(1.0e13)
    df_feat["fermi_level_shift_ev"] = carrier_densities.apply(
        lambda n: compute_gate_modulated_fermi_shift(float(n))
    )
    
    # G. Theoretical pinned Schottky barrier height model:
    # Phi_B_theory = S * (Phi_M - Chi_S) + (1 - S) * (E_C - E_CNL) - Delta_E_F
    e_c_minus_cnl = 0.22  # eV
    df_feat["physics_predicted_sbh_ev"] = (
        df_feat["effective_pinning_factor_s"] * df_feat["schottky_mott_barrier_ev"]
        + (1.0 - df_feat["effective_pinning_factor_s"]) * e_c_minus_cnl
        - df_feat["fermi_level_shift_ev"]
    ).clip(lower=0.0)
    
    # H. Thermal energy ratio k_B * T (eV)
    k_b = 8.617333262e-5
    df_feat["thermal_energy_kbt_ev"] = df_feat["measurement_temperature_k"] * k_b
    
    # I. Logarithm of vacuum base pressure (vacuum quality index)
    pressures = df_feat["vacuum_base_pressure_torr"].replace(0, np.nan).fillna(1.0e-6)
    df_feat["log_vacuum_pressure"] = np.log10(pressures)
    
    return df_feat
