"""
Tests for EDA Synthesis and Modeling Recommendations (Sprint 1.f.5).
"""

from pathlib import Path
import json
import pytest
from src.visualization.eda_synthesis import (
    generate_eda_modeling_recommendations,
    RECOMMENDATIONS_JSON_PATH
)


def test_generate_eda_modeling_recommendations():
    """Verify synthesized modeling recommendations match empirical data distributions."""
    recs = generate_eda_modeling_recommendations()
    
    assert recs["dataset_scale"]["n_samples"] >= 20
    assert recs["dataset_scale"]["n_sources"] >= 10
    assert recs["dataset_scale"]["regime"] == "small_n_tabular"
    
    # Target formulation
    assert recs["target_formulation"]["primary_target"] == "log10_rc"
    
    # Feature constraints
    feat_cons = recs["feature_selection_constraints"]
    assert feat_cons["max_features_recommended"] <= 5
    assert len(feat_cons["recommended_primary_features"]) >= 3
    
    # Cross validation strategy
    assert recs["cross_validation_strategy"]["grouping_variable"] == "source_uid"
    
    # Check output JSON
    assert RECOMMENDATIONS_JSON_PATH.exists()
    with open(RECOMMENDATIONS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["dataset_scale"]["n_samples"] == recs["dataset_scale"]["n_samples"]
