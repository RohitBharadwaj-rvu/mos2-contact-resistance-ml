"""
Tests for Unified Model Factory (Subheading 2.c Audit).
"""

import pytest
from src.models.model_factory import instantiate_candidate_model, instantiate_tuned_candidate_model
from src.models.model_selector import get_shortlisted_architectures


def test_instantiate_candidate_model():
    """Verify that every shortlisted architecture can be instantiated and configured."""
    shortlisted = get_shortlisted_architectures()
    
    for name in shortlisted:
        model = instantiate_candidate_model(name)
        assert model is not None
        assert hasattr(model, "fit")
        assert hasattr(model, "predict")
        
    with pytest.raises(ValueError):
        instantiate_candidate_model("Nonexistent_Model")

    # Verify discovered symbolic model instantiation
    sym_model = instantiate_candidate_model("Discovered_Symbolic")
    assert sym_model is not None
    assert hasattr(sym_model, "fit")
    assert hasattr(sym_model, "predict")


def test_instantiate_tuned_candidate_model():
    """Verify that every shortlisted architecture can be instantiated in its optimal tuned configuration."""
    shortlisted = get_shortlisted_architectures()
    for name in shortlisted:
        tuned_model = instantiate_tuned_candidate_model(name)
        assert tuned_model is not None
        assert hasattr(tuned_model, "fit")
        assert hasattr(tuned_model, "predict")
