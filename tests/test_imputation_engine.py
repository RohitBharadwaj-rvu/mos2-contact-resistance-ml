"""Tests for Imputation Engine."""

import pandas as pd
from src.features.imputation_engine import (
    analyze_missingness,
    apply_domain_inferred_imputation
)


def test_analyze_missingness():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": ["x", "y", "z"],
        "c": [None, None, None]
    })
    stats = analyze_missingness(df)
    assert stats["total_rows"] == 3
    assert stats["missing_statistics"]["a"]["null_count"] == 1
    assert stats["missing_statistics"]["b"]["null_count"] == 0
    assert stats["missing_statistics"]["c"]["null_count"] == 3


def test_domain_inferred_imputation():
    df = pd.DataFrame([
        {
            "deposition_method": "E_beam_Evaporation",
            "post_annealing_temperature_c": None,
            "gate_carrier_density_cm2": None,
            "vacuum_base_pressure_torr": None,
            "adhesion_layer": None
        }
    ])
    df_imp = apply_domain_inferred_imputation(df)
    
    # Assert defaults applied
    assert df_imp["post_annealing_temperature_c"].iloc[0] == 20.0
    assert df_imp["gate_carrier_density_cm2"].iloc[0] == 1.0e13
    assert df_imp["vacuum_base_pressure_torr"].iloc[0] == 1.0e-6
    assert df_imp["adhesion_layer"].iloc[0] == "None"
    
    # Assert missingness indicators tracked
    assert df_imp["anneal_temp_was_missing"].iloc[0] == 1
    assert df_imp["carrier_density_was_missing"].iloc[0] == 1
