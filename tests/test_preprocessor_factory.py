"""
Tests for Preprocessor Factory (Sprint 4.a.2).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd
from src.features.preprocessor_factory import (
    build_family_preprocessor,
    define_preprocessor_spec,
    PREPROCESSOR_SPEC_JSON
)


def test_build_family_preprocessor():
    """Verify preprocessor construction, imputation, and scaling across families."""
    df = pd.DataFrame({
        "physics_predicted_sbh_ev": [0.4, np.nan, 0.6],
        "is_vdw_or_depinned_contact": [1.0, 0.0, 0.0],
        "sulfide_formation_enthalpy_kj_mol": [-100.0, -150.0, np.nan],
        "gate_carrier_density_cm2": [1e12, 5e12, 1e13]
    })
    
    for family in ["linear", "kernel", "bayesian_non_parametric", "tree_ensemble", "symbolic"]:
        pipe = build_family_preprocessor(family)
        res = pipe.fit_transform(df)
        assert res.shape == (3, 4)
        assert not np.isnan(res).any(), f"NaNs remained after preprocessing for family {family}"
        
        if family == "symbolic":
            # Values should be within (0.1, 1.0)
            assert (res >= 0.09).all() and (res <= 1.01).all()
            
    with pytest.raises(ValueError):
        build_family_preprocessor("unknown_family")


def test_define_preprocessor_spec():
    """Verify specification JSON output."""
    spec = define_preprocessor_spec()
    assert "families" in spec
    assert len(spec["families"]) == 4
    
    assert PREPROCESSOR_SPEC_JSON.exists()
    with open(PREPROCESSOR_SPEC_JSON, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["families"]) == len(spec["families"])
