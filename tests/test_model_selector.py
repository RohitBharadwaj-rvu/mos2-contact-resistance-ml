"""
Tests for Final Candidate Model Selector (Sprint 2.c.3).
"""

from pathlib import Path
import json
import pytest
from src.models.model_selector import (
    generate_candidate_architecture_matrix,
    get_shortlisted_architectures,
    SHORTLIST_JSON_PATH
)


def test_generate_candidate_architecture_matrix():
    """Verify multi-criteria decision matrix scoring and shortlisted selections."""
    matrix = generate_candidate_architecture_matrix()
    
    assert "weights" in matrix
    assert abs(sum(matrix["weights"].values()) - 1.0) < 1e-4
    
    evals = matrix["candidate_evaluations"]
    assert len(evals) >= 6
    
    # Verify composite scores are between 0 and 10
    for cand in evals:
        assert 0.0 <= cand["composite_score"] <= 10.0
        
    shortlisted = matrix["shortlisted_models"]
    assert len(shortlisted) >= 4
    assert "Gaussian_Process_Matern" in shortlisted
    assert "Gradient_Boosting" in shortlisted
    assert "Ridge_Regression" in shortlisted
    assert "Unregularized_OLS" not in shortlisted, "Unregularized OLS must not be shortlisted"
    
    assert SHORTLIST_JSON_PATH.exists()
    with open(SHORTLIST_JSON_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["shortlisted_models"]) == len(shortlisted)


def test_get_shortlisted_architectures():
    """Verify getter returns consistent list of shortlisted model names."""
    names = get_shortlisted_architectures()
    assert isinstance(names, list)
    assert len(names) >= 4
