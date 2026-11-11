"""
Unit tests for Sprint 5.c.1: Physical Transport Regime Definitions and Dataset Classification.
"""

import pytest
import json
from pathlib import Path
from src.interpretability.regime_definitions import (
    define_contact_transport_regimes,
    classify_device_regime,
    classify_dataset_regimes,
    REGIMES_JSON_PATH
)


def test_define_contact_transport_regimes():
    regimes = define_contact_transport_regimes()
    assert len(regimes) == 4
    assert "Regime_I_Quantum_Limited" in regimes
    assert "Regime_II_Thermionic_Field_Tunneling" in regimes
    assert "Regime_III_Thermionic_Emission" in regimes
    assert "Regime_IV_Defect_Dominated_Pinned" in regimes


def test_classify_device_regime():
    # Test Quantum-limited regime (e.g. Bi vdW)
    r1 = classify_device_regime(log10_rc=2.1, sbh_ev=0.05, n2d_cm2=1.5e13, is_vdw=True)
    assert r1 == "Regime_I_Quantum_Limited"

    # Test Tunneling regime (e.g. Ti)
    r2 = classify_device_regime(log10_rc=2.7, sbh_ev=0.30, n2d_cm2=1.0e13, is_vdw=False)
    assert r2 == "Regime_II_Thermionic_Field_Tunneling"

    # Test Thermionic regime (e.g. Au)
    r3 = classify_device_regime(log10_rc=3.5, sbh_ev=0.60, n2d_cm2=5.0e12, is_vdw=False)
    assert r3 == "Regime_III_Thermionic_Emission"

    # Test Defect / pinned regime (e.g. Pt)
    r4 = classify_device_regime(log10_rc=4.8, sbh_ev=1.35, n2d_cm2=3.0e12, is_vdw=False)
    assert r4 == "Regime_IV_Defect_Dominated_Pinned"


def test_classify_dataset_regimes():
    res = classify_dataset_regimes()
    assert "regime_distribution" in res
    assert "classified_devices" in res
    assert len(res["classified_devices"]) == 20

    dist = res["regime_distribution"]
    assert sum(dist.values()) == 20
    assert dist["Regime_I_Quantum_Limited"] >= 1
    assert dist["Regime_II_Thermionic_Field_Tunneling"] >= 1
    assert dist["Regime_IV_Defect_Dominated_Pinned"] >= 1

    assert REGIMES_JSON_PATH.exists()
    with open(REGIMES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["classified_devices"]) == 20
