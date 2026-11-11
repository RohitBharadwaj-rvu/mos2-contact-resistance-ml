"""
Unit tests for Sprint 5.b.1: Inter-Feature Confounding Analysis.
"""

import pytest
import json
import numpy as np
from pathlib import Path
from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.interpretability.confounding_analyzer import (
    compute_partial_correlation_matrix,
    analyze_inter_feature_confounding,
    CONFOUNDING_JSON_PATH,
    CONFOUNDING_PNG_PATH
)


def test_compute_partial_correlation_matrix():
    df = get_cleaned_and_engineered_dataset()
    cols = [
        "physics_predicted_sbh_ev",
        "is_vdw_or_depinned_contact",
        "sulfide_formation_enthalpy_kj_mol",
        "gate_carrier_density_cm2"
    ]
    part_corr = compute_partial_correlation_matrix(df, cols)
    assert part_corr.shape == (4, 4)
    # Diagonals should be 1.0
    for i in range(4):
        assert np.isclose(part_corr[i, i], 1.0)
    # Off-diagonals bounded in [-1, 1]
    assert np.all(part_corr >= -1.0)
    assert np.all(part_corr <= 1.0)


def test_analyze_inter_feature_confounding():
    res = analyze_inter_feature_confounding()
    assert "variance_inflation_factors" in res
    assert "partial_correlation_matrix" in res
    assert "entangled_feature_pairs" in res
    assert len(res["entangled_feature_pairs"]) == 6

    # VIFs should be well conditioned (all < 5.0)
    for feat, vif in res["variance_inflation_factors"].items():
        assert vif < 5.0

    assert CONFOUNDING_JSON_PATH.exists()
    assert CONFOUNDING_PNG_PATH.exists()
    assert CONFOUNDING_PNG_PATH.stat().st_size > 50000
