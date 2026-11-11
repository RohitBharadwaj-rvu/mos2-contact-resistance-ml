"""
Tests for Tree-Based Ensemble Models (Sprint 2.c.1).
"""

from pathlib import Path
import json
import pytest
from src.models.tree_ensembles import (
    build_tree_model,
    evaluate_tree_ensembles,
    TREE_EVAL_JSON
)


def test_build_tree_model():
    """Verify initialization and parameter constraints for tree ensembles."""
    for model_name in ["random_forest", "gradient_boosting", "extra_trees"]:
        m = build_tree_model(model_name, max_depth=2, n_estimators=20)
        assert m.max_depth == 2
        assert m.n_estimators == 20
        
    with pytest.raises(ValueError):
        build_tree_model("unknown_ensemble")


def test_evaluate_tree_ensembles():
    """Verify performance metrics and feature importances of tree ensembles on real data."""
    res = evaluate_tree_ensembles()
    
    assert res["n_samples"] >= 20
    assert len(res["features_used"]) <= 4
    
    models = res["models"]
    for m in ["random_forest", "gradient_boosting", "extra_trees"]:
        assert m in models
        m_res = models[m]
        assert m_res["rmse_log10_rc"] > 0.0
        assert m_res["mae_log10_rc"] > 0.0
        assert m_res["r2_score"] > 0.5, "Constrained tree ensembles should achieve high in-sample explanation"
        assert len(m_res["feature_importances"]) == len(res["features_used"])
        # Sum of feature importances should be approximately 1.0
        assert abs(sum(m_res["feature_importances"].values()) - 1.0) < 0.05
        
    assert TREE_EVAL_JSON.exists()
