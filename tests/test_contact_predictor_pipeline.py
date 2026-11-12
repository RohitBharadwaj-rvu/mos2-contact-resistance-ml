"""
Unit tests for end-to-end contact predictor inference pipeline (Sprint 7.8).
"""

import pytest
from src.pipeline.contact_predictor_pipeline import MoS2ContactPredictor, METAL_DATABASE


@pytest.fixture(scope="module")
def predictor():
    return MoS2ContactPredictor()


def test_mos2_contact_predictor_init(predictor):
    assert predictor.rc_model is not None
    assert predictor.sbh_model is not None
    assert len(predictor.task1_cols) == 14
    assert len(predictor.task2_cols) == 8


def test_mos2_contact_predictor_bi_vdw(predictor):
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=1.8e13, is_vdw_transferred=True)
    assert res["inputs"]["metal"] == "Bi"
    assert res["inputs"]["is_vdw_or_depinned"] is True
    # Predicted SBH should be low (< 0.25 eV)
    assert res["predicted_schottky_barrier"]["sbh_ev"] < 0.25
    # Predicted Rc from RF
    rc_ml = res["predicted_contact_resistance"]["task1_random_forest"]["rc_ohm_um"]
    assert rc_ml > 0
    assert "Regime_I_Quantum_Limited" in res["transport_regime"]["regime_id"]


def test_mos2_contact_predictor_ti_reactive(predictor):
    res = predictor.predict(metal="Ti", gate_carrier_density_cm2=5.0e12, is_vdw_transferred=False)
    assert res["inputs"]["metal"] == "Ti"
    rc_ml = res["predicted_contact_resistance"]["task1_random_forest"]["rc_ohm_um"]
    assert rc_ml > 500.0


def test_mos2_contact_predictor_validity_warnings(predictor):
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=4.0e13, is_vdw_transferred=True)
    assert any("oxide breakdown" in w for w in res["warnings"])

    res_pt = predictor.predict(metal="Pt", gate_carrier_density_cm2=1.0e13, schottky_barrier_height_ev=0.85)
    assert any("thermionic emission" in w for w in res_pt["warnings"])


def test_mos2_contact_predictor_respects_quantum_limit(predictor):
    res = predictor.predict(metal="Bi", gate_carrier_density_cm2=2.5e13, schottky_barrier_height_ev=0.0)
    rc_ml = res["predicted_contact_resistance"]["task1_random_forest"]["rc_ohm_um"]
    rc_quantum = res["physical_limits"]["landauer_quantum_floor_ohm_um"]
    assert rc_ml >= rc_quantum
