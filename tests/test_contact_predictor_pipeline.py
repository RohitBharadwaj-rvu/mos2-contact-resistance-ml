"""
Unit tests for end-to-end contact predictor inference pipeline (Sprint 6.b.2).
"""

import pytest
from src.pipeline.contact_predictor_pipeline import MoS2ContactPredictor, METAL_DATABASE


@pytest.fixture(scope="module")
def predictor():
    return MoS2ContactPredictor()


def test_mos2_contact_predictor_init(predictor):
    assert predictor.ml_model is not None
    assert predictor.symbolic_model is not None
    assert len(predictor.feature_cols) == 4


def test_mos2_contact_predictor_bi_vdw(predictor):
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=1.8e13, is_vdw_transferred=True)
    assert res["inputs"]["metal"] == "Bi"
    assert res["inputs"]["is_vdw_transferred"] is True
    # Predicted Rc should achieve ultra-low regime (< 150 Ohm*um)
    rc_ml = res["predicted_contact_resistance"]["ml_model_ridge"]["rc_ohm_um"]
    assert rc_ml < 150.0
    assert res["transport_regime"]["regime_id"] == "Regime_I_Quantum_Limited"
    assert any("Target achieved" in g for g in res["engineering_guidance"])


def test_mos2_contact_predictor_ti_backgated(predictor):
    res = predictor.predict(metal="Ti", gate_carrier_density_cm2=5.0e12, is_vdw_transferred=False)
    assert res["inputs"]["metal"] == "Ti"
    rc_ml = res["predicted_contact_resistance"]["ml_model_ridge"]["rc_ohm_um"]
    assert rc_ml > 1000.0
    assert any("gate carrier density must be boosted" in g for g in res["engineering_guidance"])


def test_mos2_contact_predictor_validity_warnings(predictor):
    # Extreme carrier density risking oxide breakdown
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=4.0e13, is_vdw_transferred=True)
    assert any("dielectric rupture" in w for w in res["validity_warnings"])

    # High barrier metal
    res_pt = predictor.predict(metal="Pt", gate_carrier_density_cm2=1.0e13, schottky_barrier_height_ev=0.95)
    assert any("freeze-out" in w for w in res_pt["validity_warnings"])


def test_mos2_contact_predictor_respects_quantum_limit(predictor):
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=2.5e13, schottky_barrier_height_ev=0.0)
    rc_ml = res["predicted_contact_resistance"]["ml_model_ridge"]["rc_ohm_um"]
    rc_quantum = res["physical_limits"]["landauer_quantum_floor_ohm_um"]
    assert rc_ml >= rc_quantum
