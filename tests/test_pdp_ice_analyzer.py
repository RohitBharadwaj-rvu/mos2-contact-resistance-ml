"""
Unit tests for Sprint 5.a.2: Permutation Importance, PDP, and ICE Curves.
"""

import pytest
import json
from pathlib import Path
from src.interpretability.pdp_ice_analyzer import (
    compute_oof_permutation_importance,
    compute_pdp_and_ice,
    compute_2d_pdp_surface,
    run_full_pdp_and_permutation_analysis,
    PDP_JSON_PATH,
    PDP_ICE_PNG_PATH,
    PDP_2D_PNG_PATH,
    PERM_IMP_PNG_PATH
)


def test_compute_oof_permutation_importance():
    res = compute_oof_permutation_importance(n_repeats=3)
    assert "permutation_importance" in res
    assert "base_oof_rmse_dex" in res
    perm = res["permutation_importance"]
    assert len(perm) == 4
    for f, d in perm.items():
        assert "mean_delta_rmse_dex" in d
        assert "relative_importance_pct" in d


def test_compute_pdp_and_ice():
    pdp = compute_pdp_and_ice(grid_points=10)
    assert "gate_carrier_density_cm2" in pdp
    assert "physics_predicted_sbh_ev" in pdp
    for f, d in pdp.items():
        assert len(d["grid"]) == 10
        assert len(d["pdp_mean_curve"]) == 10
        assert len(d["ice_curves"]) == 20


def test_run_full_pdp_and_permutation_analysis():
    res = run_full_pdp_and_permutation_analysis()
    assert "permutation_importance" in res
    assert "pdp_1d_curves" in res

    assert PDP_JSON_PATH.exists()
    assert PDP_ICE_PNG_PATH.exists()
    assert PDP_2D_PNG_PATH.exists()
    assert PERM_IMP_PNG_PATH.exists()
    assert PDP_ICE_PNG_PATH.stat().st_size > 50000
    assert PDP_2D_PNG_PATH.stat().st_size > 50000
    assert PERM_IMP_PNG_PATH.stat().st_size > 50000
