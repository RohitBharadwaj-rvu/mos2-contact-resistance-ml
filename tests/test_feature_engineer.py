"""Tests for Physics-Informed Feature Engineering Pipeline."""

import pandas as pd
from src.features.feature_engineer import enrich_dataset_with_physics_features
from src.data.tabular_extractor import load_tabular_dataset


def test_enrich_dataset():
    df_raw = load_tabular_dataset()
    df_enriched = enrich_dataset_with_physics_features(df_raw)
    
    # Assert newly engineered features exist
    expected_cols = [
        "schottky_mott_barrier_ev",
        "delta_cnl_ev",
        "electronegativity_diff_sulfur",
        "is_vdw_or_depinned_contact",
        "effective_pinning_factor_s",
        "fermi_level_shift_ev",
        "physics_predicted_sbh_ev",
        "thermal_energy_kbt_ev",
        "log_vacuum_pressure"
    ]
    for col in expected_cols:
        assert col in df_enriched.columns, f"Missing feature {col}"
        assert df_enriched[col].notnull().all(), f"NaN in feature {col}"


def test_physical_consistency_of_features():
    df_raw = load_tabular_dataset()
    df_enriched = enrich_dataset_with_physics_features(df_raw)
    
    # Ti Schottky-Mott barrier: 4.33 - 4.20 = 0.13 eV
    ti_row = df_enriched[df_enriched["contact_metal"] == "Ti"].iloc[0]
    assert abs(ti_row["schottky_mott_barrier_ev"] - 0.13) < 0.05
    
    # Bi semimetal is depinned vdW contact (S = 0.95)
    bi_row = df_enriched[df_enriched["contact_metal"] == "Bi"].iloc[0]
    assert bi_row["is_vdw_or_depinned_contact"] == 1.0
    assert bi_row["effective_pinning_factor_s"] == 0.95
    
    # Evaporated Au has strong pinning (S = 0.15)
    au_row = df_enriched[(df_enriched["contact_metal"] == "Au") & (df_enriched["contact_architecture"] == "Top_Contact")].iloc[0]
    assert au_row["is_vdw_or_depinned_contact"] == 0.0
    assert au_row["effective_pinning_factor_s"] == 0.15
