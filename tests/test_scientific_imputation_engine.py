"""
Unit tests for Scientific Imputation & Missingness Provenance Engine (Sprint 7.2).
"""

import json
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

from src.features.scientific_imputation_engine import (
    ScientificMissingnessHandler,
    audit_dataset_missingness_provenance,
    AUDIT_JSON_PATH
)


def test_audit_dataset_missingness_provenance():
    summary = audit_dataset_missingness_provenance()
    assert summary["total_primary_observations"] >= 25
    assert "annealing_provenance" in summary
    assert "carrier_density_provenance" in summary
    assert "schottky_barrier_measurements" in summary

    # Verify audit JSON exists
    assert AUDIT_JSON_PATH.exists()
    with open(AUDIT_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["total_primary_observations"] == summary["total_primary_observations"]


def test_scientific_missingness_handler_native_nan():
    df = pd.DataFrame({
        "num_feature": [1.0, 2.0, np.nan, 4.0],
        "complete_feature": [10.0, 20.0, 30.0, 40.0]
    })
    handler = ScientificMissingnessHandler(mode="native_nan")
    df_trans = handler.fit_transform(df)

    assert "num_feature_is_missing" in df_trans.columns
    assert "complete_feature_is_missing" not in df_trans.columns
    # NaN is preserved in native mode
    assert df_trans["num_feature"].isna().sum() == 1
    assert df_trans["num_feature_is_missing"].tolist() == [0.0, 0.0, 1.0, 0.0]


def test_scientific_missingness_handler_fold_imputed():
    train_df = pd.DataFrame({
        "num_feature": [10.0, 20.0, np.nan, 30.0]
    })
    test_df = pd.DataFrame({
        "num_feature": [np.nan, 40.0]
    })

    handler = ScientificMissingnessHandler(mode="fold_imputed")
    handler.fit(train_df)

    # Median of valid values in train [10, 20, 30] is 20.0
    assert handler.train_medians_["num_feature"] == 20.0

    test_trans = handler.transform(test_df)
    assert test_trans["num_feature"].isna().sum() == 0
    # Imputed with train median 20.0
    assert test_trans["num_feature"].iloc[0] == 20.0
    assert test_trans["num_feature_is_missing"].iloc[0] == 1.0
