"""
Tests for Leakage-Free Categorical Encoders (Sprint 4.a.1).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd
from src.features.categorical_encoders import (
    build_categorical_preprocessor,
    define_categorical_encoding_spec,
    ENCODING_SPEC_JSON
)


def test_one_hot_preprocessor_leakage_resilience():
    """Verify that OneHot preprocessor ignores unseen categories without throwing errors."""
    train_df = pd.DataFrame({
        "contact_architecture": ["top_contact", "transferred_vdw"],
        "deposition_method": ["e_beam_evaporation", "mechanical_transfer"],
        "work_function_ev": [4.5, 4.2]
    })
    
    # Test fold has an unseen category 'edge_contact'
    test_df = pd.DataFrame({
        "contact_architecture": ["edge_contact"],
        "deposition_method": ["e_beam_evaporation"],
        "work_function_ev": [5.1]
    })
    
    preprocessor = build_categorical_preprocessor(strategy="one_hot")
    X_train_trans = preprocessor.fit_transform(train_df)
    assert X_train_trans.shape[0] == 2
    
    # Transform unseen test data without errors
    X_test_trans = preprocessor.transform(test_df)
    assert X_test_trans.shape[0] == 1
    assert np.isfinite(X_test_trans).all()


def test_physics_ordinal_preprocessor():
    """Verify physics-ranked ordinal encoder preserves expected interface hierarchy."""
    df = pd.DataFrame({
        "contact_architecture": ["top_contact", "edge_contact", "transferred_vdw"],
        "deposition_method": ["thermal_evaporation", "e_beam_evaporation", "mechanical_transfer"],
        "num_val": [1.0, 2.0, 3.0]
    })
    
    preprocessor = build_categorical_preprocessor(strategy="physics_ordinal")
    trans = preprocessor.fit_transform(df)
    
    # Check architecture monotonic ranking: top (0) < edge (1) < vdw (2)
    assert trans[0, 0] < trans[1, 0] < trans[2, 0]
    assert trans[0, 1] < trans[1, 1] < trans[2, 1]


def test_define_categorical_encoding_spec():
    """Verify specification JSON output."""
    spec = define_categorical_encoding_spec()
    assert "categorical_variables" in spec
    assert "recommended_strategy" in spec
    
    assert ENCODING_SPEC_JSON.exists()
    with open(ENCODING_SPEC_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["title"] == spec["title"]
