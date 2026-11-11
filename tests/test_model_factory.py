"""
Tests for Unified Model Factory (Subheading 2.c Audit).
"""

import pytest
from src.models.model_factory import instantiate_candidate_model
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
