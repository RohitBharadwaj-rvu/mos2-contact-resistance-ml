"""
Unit tests for Experimental Feature Engineer & Dual-Task Formulation (Sprint 7.3).
"""

import pytest
import pandas as pd
from pathlib import Path

from src.features.experimental_feature_engineer import (
    get_raw_experimental_dataset,
    engineer_experimental_features,
    get_task1_rc_feature_names,
    get_task2_sbh_feature_names,
    export_master_features_dataset,
    MASTER_FEATURES_CSV
)


def test_get_raw_experimental_dataset():
    df = get_raw_experimental_dataset()
    assert len(df) >= 25
    assert "source_uid" in df.columns
    assert "contact_metal" in df.columns
    assert "work_function_ev" in df.columns


def test_engineer_experimental_features():
    df_feat = engineer_experimental_features()
    assert len(df_feat) >= 25
    assert "log_vacuum_pressure" in df_feat.columns
    assert "is_annealed" in df_feat.columns
    assert "thermal_budget_k_min" in df_feat.columns
    assert "n2d_norm_1e13" in df_feat.columns
    assert "work_function_offset_cbm_ev" in df_feat.columns

    # Verify Task 1 does NOT contain baked-in pinning factor
    task1_cols = get_task1_rc_feature_names()
    assert "work_function_ev" in task1_cols
    assert "physics_predicted_sbh_ev" not in task1_cols
    assert "is_vdw_or_depinned_contact" in task1_cols

    # Verify Task 2 features
    task2_cols = get_task2_sbh_feature_names()
    assert "work_function_ev" in task2_cols
    assert "work_function_offset_cbm_ev" in task2_cols


def test_export_master_features_dataset():
    df_exported = export_master_features_dataset()
    assert MASTER_FEATURES_CSV.exists()
    assert len(df_exported) >= 25
    df_read = pd.read_csv(MASTER_FEATURES_CSV)
    assert len(df_read) == len(df_exported)
