"""
Missing Data Pattern Auditor and Physics-Informed Imputation Engine.
Analyzes missing value rates, validates domain default inferences, and generates imputed feature matrices.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from src.data.tabular_extractor import load_tabular_dataset


def analyze_missingness(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes column-wise missingness count and percentage."""
    total_rows = len(df)
    missing_stats = {}
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        missing_stats[col] = {
            "null_count": null_count,
            "null_percentage": round((null_count / total_rows) * 100.0, 2)
        }
    return {
        "total_rows": total_rows,
        "columns_analyzed": len(df.columns),
        "missing_statistics": missing_stats
    }


def apply_domain_inferred_imputation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies physics-informed domain defaults to safely infer missing experimental parameters
    while tracking provenance with boolean missingness indicator columns.
    """
    df_imputed = df.copy()
    
    # 1. Post-annealing temperature and ambient defaults (20 C, None if unmentioned)
    if "post_annealing_temperature_c" in df_imputed.columns:
        df_imputed["anneal_temp_was_missing"] = df_imputed["post_annealing_temperature_c"].isnull().astype(int)
        df_imputed["post_annealing_temperature_c"] = pd.to_numeric(
            df_imputed["post_annealing_temperature_c"], errors="coerce"
        ).fillna(20.0)
        
    if "post_annealing_gas_ambient" in df_imputed.columns:
        df_imputed["post_annealing_gas_ambient"] = df_imputed["post_annealing_gas_ambient"].fillna("None").astype(str)
        
    # 2. Adhesion layer default (None if unspecified)
    if "adhesion_layer" in df_imputed.columns:
        df_imputed["adhesion_layer"] = df_imputed["adhesion_layer"].fillna("None").astype(str)
        
    # 3. Flake synthesis method default
    if "flake_synthesis_method" in df_imputed.columns:
        df_imputed["flake_synthesis_method"] = df_imputed["flake_synthesis_method"].fillna("Mechanical_Exfoliation").astype(str)
        
    # 4. Vacuum pressure default based on deposition method
    if "vacuum_base_pressure_torr" in df_imputed.columns:
        df_imputed["vacuum_pressure_was_missing"] = df_imputed["vacuum_base_pressure_torr"].isnull().astype(int)
        default_pressures = {
            "E_beam_Evaporation": 1e-6,
            "Thermal_Evaporation": 1e-6,
            "Sputtering": 1e-6,
            "Dry_Transfer": 1e-7,
            "Chemical_Treatment": 1e-6
        }
        dep_col = df_imputed["deposition_method"].map(default_pressures).fillna(1e-6)
        num_pressure = pd.to_numeric(df_imputed["vacuum_base_pressure_torr"], errors="coerce")
        df_imputed["vacuum_base_pressure_torr"] = num_pressure.fillna(dep_col)
        
    # 5. Carrier density default for ON-state contact resistance measurements (1.0e13 cm^-2)
    if "gate_carrier_density_cm2" in df_imputed.columns:
        df_imputed["carrier_density_was_missing"] = df_imputed["gate_carrier_density_cm2"].isnull().astype(int)
        num_density = pd.to_numeric(df_imputed["gate_carrier_density_cm2"], errors="coerce")
        df_imputed["gate_carrier_density_cm2"] = num_density.fillna(1.0e13)
        
    return df_imputed
