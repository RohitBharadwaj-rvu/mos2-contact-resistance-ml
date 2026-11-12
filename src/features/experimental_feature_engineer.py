"""
Experimental Feature Engineer & Dual-Task Formulation (Sprint 7.3).
Eliminates artificial circular assumptions by:
1. Providing raw experimental parameters as model inputs:
   - Metal work function, electronegativity, formation enthalpy, bulk resistivity.
   - Deposition method, vdW status, vacuum pressure.
   - Annealing temperature, gas ambient, duration.
   - MoS2 layer count, thickness.
   - Gate dielectric material, EOT, carrier density.
   - Measurement temperature.
2. Un-baking assumed pinning factors: does NOT pre-calculate SBH with hardcoded 0.95/0.15 pinning.
3. Formulating two distinct prediction tasks:
   - Task 1: Primary Contact Resistance (Rc) prediction directly from raw fabrication & materials levers.
   - Task 2: Schottky Barrier Height (Phi_B) prediction from metal properties and interface chemistry.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_PRIMARY_CSV = ROOT_DIR / "data" / "raw" / "primary_experimental_literature_dataset.csv"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
MASTER_FEATURES_CSV = PROCESSED_DATA_DIR / "master_experimental_features_dataset.csv"


def get_raw_experimental_dataset() -> pd.DataFrame:
    """Loads the primary experimental dataset without any review entries."""
    return pd.read_csv(RAW_PRIMARY_CSV)


def engineer_experimental_features(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Transforms raw primary experimental literature data into clean, machine-learning-ready
    feature vectors with zero baked-in pinning assumptions.
    """
    if df is None:
        df = get_raw_experimental_dataset()

    df_feat = df.copy()

    # 1. Vacuum base pressure log transform
    df_feat["log_vacuum_pressure"] = np.round(np.log10(df_feat["vacuum_base_pressure_torr"]), 3)

    # 2. Annealing physical indicators
    df_feat["is_annealed"] = (df_feat["post_annealing_status"] == "performed").astype(int)
    # Effective annealing thermal budget in Kelvin * minutes
    t_kelvin = df_feat["post_annealing_temperature_c"] + 273.15
    df_feat["thermal_budget_k_min"] = np.round(t_kelvin * df_feat["post_annealing_duration_min"], 1)

    # 3. Electrostatic gating features
    # Normalized carrier density (per 1e13 cm^-2)
    df_feat["n2d_norm_1e13"] = np.round(df_feat["gate_carrier_density_cm2"] / 1.0e13, 4)
    # Log carrier density
    df_feat["log10_n2d"] = np.round(np.log10(df_feat["gate_carrier_density_cm2"]), 3)
    # Log EOT (nm)
    df_feat["log10_eot_nm"] = np.round(np.log10(df_feat["equivalent_oxide_thickness_nm"]), 3)

    # 4. Metal property features
    # Metal chemical reactivity indicator (negative enthalpy magnitude)
    df_feat["abs_sulfide_enthalpy"] = np.abs(df_feat["sulfide_formation_enthalpy_kj_mol"])
    # Metal work function offset from ideal MoS2 conduction band minimum (chi_MoS2 ~ 4.2 eV)
    df_feat["work_function_offset_cbm_ev"] = np.round(df_feat["work_function_ev"] - 4.20, 3)

    # 5. One-hot encodings for categorical fabrication variables
    # Deposition method encoding
    depo_dummies = pd.get_dummies(df_feat["deposition_method"], prefix="depo", dtype=int)
    df_feat = pd.concat([df_feat, depo_dummies], axis=1)

    # Annealing ambient encoding
    gas_dummies = pd.get_dummies(df_feat["post_annealing_gas_ambient"], prefix="ambient", dtype=int)
    df_feat = pd.concat([df_feat, gas_dummies], axis=1)

    # Gate dielectric encoding
    diel_dummies = pd.get_dummies(df_feat["gate_dielectric_material"], prefix="dielectric", dtype=int)
    df_feat = pd.concat([df_feat, diel_dummies], axis=1)

    # 6. Ensure log10_rc is clean target
    df_feat["log10_rc"] = np.round(np.log10(df_feat["contact_resistance_rc_ohm_um"]), 4)

    return df_feat


def get_task1_rc_feature_names() -> List[str]:
    """
    Returns the feature list for Task 1 (Contact Resistance Prediction).
    Notice: uses ONLY raw fabrication and material inputs; does NOT use measured SBH or hardcoded SBH!
    """
    return [
        "work_function_ev",
        "pauling_electronegativity",
        "sulfide_formation_enthalpy_kj_mol",
        "metal_resistivity_ohm_cm",
        "is_vdw_or_depinned_contact",
        "log_vacuum_pressure",
        "is_annealed",
        "post_annealing_temperature_c",
        "thermal_budget_k_min",
        "layer_count",
        "thickness_nm",
        "n2d_norm_1e13",
        "log10_eot_nm",
        "measurement_temperature_k"
    ]


def get_task2_sbh_feature_names() -> List[str]:
    """
    Returns the feature list for Task 2 (Schottky Barrier Height Prediction).
    Predicts measured SBH from metal work function, chemical reactivity, and deposition architecture.
    """
    return [
        "work_function_ev",
        "work_function_offset_cbm_ev",
        "pauling_electronegativity",
        "sulfide_formation_enthalpy_kj_mol",
        "is_vdw_or_depinned_contact",
        "log_vacuum_pressure",
        "is_annealed",
        "post_annealing_temperature_c"
    ]


def export_master_features_dataset() -> pd.DataFrame:
    """Exports processed master experimental features dataset."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df_feat = engineer_experimental_features()
    df_feat.to_csv(MASTER_FEATURES_CSV, index=False)
    return df_feat


if __name__ == "__main__":
    df_out = export_master_features_dataset()
    print("Master experimental feature dataset exported successfully.")
    print(f"Dataset shape: {df_out.shape}")
    print(f"Task 1 Features ({len(get_task1_rc_feature_names())}): {get_task1_rc_feature_names()}")
    print(f"Task 2 Features ({len(get_task2_sbh_feature_names())}): {get_task2_sbh_feature_names()}")
