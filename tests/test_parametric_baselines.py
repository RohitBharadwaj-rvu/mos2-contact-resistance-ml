"""
Tests for Simple Parametric Baselines (Sprint 2.b.2).
"""

from pathlib import Path
import json
import pytest
from src.models.parametric_baselines import (
    build_parametric_pipeline,
    evaluate_parametric_baselines,
    PARAMETRIC_JSON_PATH
)


def test_build_parametric_pipeline():
    """Verify construction and validation of scikit-learn linear pipelines."""
    for model_name in ["ols", "ridge", "lasso", "elastic_net"]:
        pipe = build_parametric_pipeline(model_name)
        assert "scaler" in pipe.named_steps
        assert "regressor" in pipe.named_steps
        
    with pytest.raises(ValueError):
        build_parametric_pipeline("nonexistent_model")


def test_evaluate_parametric_baselines():
    """Verify evaluation metrics and coefficient extraction for linear baselines."""
    res = evaluate_parametric_baselines()
    
    assert res["n_samples"] >= 20
    assert len(res["features_used"]) <= 4
    
    models = res["models"]
    for m in ["ordinary_least_squares", "ridge_regression", "lasso_regression", "elastic_net"]:
        assert m in models
        m_res = models[m]
        assert m_res["rmse_log10_rc"] > 0.0
        assert m_res["mae_log10_rc"] > 0.0
        assert m_res["r2_score"] > 0.0, "Parametric models should explain positive variance over mean baseline"
        assert len(m_res["coefficients"]) == len(res["features_used"])
        
    assert PARAMETRIC_JSON_PATH.exists()
