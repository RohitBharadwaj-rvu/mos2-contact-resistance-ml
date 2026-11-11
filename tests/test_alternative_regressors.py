"""
Tests for Alternative Regression Architectures (Sprint 2.c.2).
"""

from pathlib import Path
import json
import pytest
from src.models.alternative_regressors import (
    build_alternative_model,
    evaluate_alternative_regressors,
    ALT_EVAL_JSON
)


def test_build_alternative_model():
    """Verify initialization of GPR, SVR, and Kernel Ridge pipelines."""
    for model_name in ["gaussian_process_rbf", "gaussian_process_matern", "svr_rbf", "kernel_ridge"]:
        pipe = build_alternative_model(model_name)
        assert "scaler" in pipe.named_steps
        assert "regressor" in pipe.named_steps
        
    with pytest.raises(ValueError):
        build_alternative_model("unknown_paradigm")


def test_evaluate_alternative_regressors():
    """Verify performance metrics and Bayesian uncertainty quantification of alternative models."""
    res = evaluate_alternative_regressors()
    
    assert res["n_samples"] >= 20
    assert len(res["features_used"]) <= 4
    
    models = res["models"]
    for m in ["gaussian_process_rbf", "gaussian_process_matern", "svr_rbf", "kernel_ridge"]:
        assert m in models
        m_res = models[m]
        assert m_res["rmse_log10_rc"] > 0.0
        assert m_res["mae_log10_rc"] > 0.0
        assert m_res["r2_score"] > 0.85, "Alternative kernel/Bayesian models should achieve strong fit"
        
    # Check GPR uncertainty
    assert "mean_uncertainty_sigma" in models["gaussian_process_rbf"]
    assert models["gaussian_process_rbf"]["mean_uncertainty_sigma"] > 0.0
    assert "optimized_kernel" in models["gaussian_process_rbf"]
    
    assert ALT_EVAL_JSON.exists()
