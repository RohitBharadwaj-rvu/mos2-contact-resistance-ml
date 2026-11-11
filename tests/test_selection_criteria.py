"""
Tests for Model Selection Criteria (Sprint 3.b.3).
"""

from pathlib import Path
import json
import pytest
import numpy as np
from src.validation.selection_criteria import (
    compute_composite_selection_score,
    define_model_selection_criteria_spec,
    evaluate_model_cv,
    SELECTION_JSON_PATH
)


def test_compute_composite_selection_score():
    """Verify composite scoring under high-performing, degraded, and penalized models."""
    # High-performing model (RMSE ~0.20, high rank correlation)
    y_true = np.array([2.0, 2.5, 3.0, 3.5, 4.0])
    y_pred_good = np.array([2.1, 2.4, 3.1, 3.4, 4.1])
    
    res_good = compute_composite_selection_score(y_true, y_pred_good, feature_count=4)
    assert res_good["composite_selection_score"] > 0.80
    assert res_good["is_qualified_for_deployment"] is True
    assert res_good["parsimony_penalty"] == 0.0
    
    # Degraded model (RMSE ~0.90, poor rank correlation)
    y_pred_bad = np.array([4.0, 3.5, 3.0, 2.5, 2.0])
    res_bad = compute_composite_selection_score(y_true, y_pred_bad, feature_count=4)
    assert res_bad["composite_selection_score"] < 0.40
    assert res_bad["is_qualified_for_deployment"] is False
    
    # Model penalized for excess features (feature_count = 8)
    res_penalized = compute_composite_selection_score(y_true, y_pred_good, feature_count=8)
    assert res_penalized["parsimony_penalty"] == 0.20
    assert res_penalized["composite_selection_score"] < res_good["composite_selection_score"]


def test_define_model_selection_criteria_spec():
    """Verify specification JSON output."""
    spec = define_model_selection_criteria_spec()
    assert "hard_qualification_thresholds" in spec
    assert spec["hard_qualification_thresholds"]["max_grouped_rmse_dex"] <= 0.45
    
    assert SELECTION_JSON_PATH.exists()
    with open(SELECTION_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["title"] == spec["title"]


def test_evaluate_model_cv():
    """Verify that evaluate_model_cv executes cross-validation and returns full score report."""
    from src.features.feature_engineer import get_cleaned_and_engineered_dataset
    from src.models.model_factory import instantiate_candidate_model
    from src.models.sample_complexity_analyzer import select_parsimonious_features
    
    df = get_cleaned_and_engineered_dataset()
    features = select_parsimonious_features(df, max_features=4)
    X = df[features]
    y = df["log10_rc"].values
    
    model = instantiate_candidate_model("Ridge_Regression")
    report = evaluate_model_cv(model, X, y)
    
    assert "composite_selection_score" in report
    assert "fold_metrics" in report
    assert len(report["fold_metrics"]) == 5
    assert len(report["oof_predictions"]) == len(y)
    assert report["is_qualified_for_deployment"] is True

