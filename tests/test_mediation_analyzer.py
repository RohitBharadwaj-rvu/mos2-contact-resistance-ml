"""
Unit tests for Sprint 5.b.3: Interfacial Chemistry vs Barrier Height Mediation Analysis.
"""

import pytest
import json
from pathlib import Path
from src.interpretability.mediation_analyzer import (
    run_mediation_analysis,
    MEDIATION_JSON_PATH,
    MEDIATION_PNG_PATH
)


def test_run_mediation_analysis():
    res = run_mediation_analysis(n_bootstraps=100)
    assert "path_coefficients" in res
    assert "indirect_effect" in res
    assert "variance_share" in res
    assert "physical_conclusion" in res

    paths = res["path_coefficients"]
    assert "path_a_enthalpy_to_sbh" in paths
    assert "path_b_sbh_to_log10_rc" in paths
    assert "path_c_prime_direct_enthalpy_to_log10_rc" in paths
    assert "total_effect_c" in paths

    ind = res["indirect_effect"]
    assert "value" in ind
    assert "bootstrap_95_ci" in ind
    assert len(ind["bootstrap_95_ci"]) == 2

    v_share = res["variance_share"]
    assert "pct_direct_orbital_bonding" in v_share
    assert "pct_indirect_barrier_doping" in v_share

    assert MEDIATION_JSON_PATH.exists()
    assert MEDIATION_PNG_PATH.exists()
    assert MEDIATION_PNG_PATH.stat().st_size > 40000
