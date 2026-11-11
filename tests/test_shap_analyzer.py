"""
Unit tests for Sprint 5.a.1: SHAP Feature Attribution Engine.
"""

import pytest
import json
from pathlib import Path
from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.interpretability.shap_analyzer import (
    compute_model_shap,
    run_full_shap_attribution_analysis,
    SHAP_JSON_PATH,
    BEESWARM_PNG_PATH,
    COMPARISON_PNG_PATH
)


def test_compute_model_shap():
    df = get_cleaned_and_engineered_dataset()
    features = select_parsimonious_features(df, max_features=4)
    X = df[features].copy()
    y = df["log10_rc"].values

    res = compute_model_shap("Ridge_Regression", X, y)
    assert res["model_name"] == "Ridge_Regression"
    assert "mean_abs_shap" in res
    assert len(res["mean_abs_shap"]) == 4
    assert "directionality_audit" in res

    # Verify physical directionality for key features
    assert res["directionality_audit"]["physics_predicted_sbh_ev"]["effect_sign"].startswith("positive")
    assert res["directionality_audit"]["gate_carrier_density_cm2"]["effect_sign"].startswith("negative")


def test_run_full_shap_attribution_analysis():
    res = run_full_shap_attribution_analysis()
    assert "model_attributions" in res
    assert len(res["model_attributions"]) == 6
    assert "Ridge_Regression" in res["model_attributions"]
    assert "Gradient_Boosting" in res["model_attributions"]

    assert SHAP_JSON_PATH.exists()
    assert BEESWARM_PNG_PATH.exists()
    assert COMPARISON_PNG_PATH.exists()
    assert BEESWARM_PNG_PATH.stat().st_size > 50000
    assert COMPARISON_PNG_PATH.stat().st_size > 50000
