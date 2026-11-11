"""Tests for Semiconductor Characterization Standards."""

from src.data.characterization_standards import (
    load_characterization_standards,
    evaluate_rc_method_reliability,
    evaluate_sbh_method_reliability,
    compute_2d_thermionic_current
)


def test_load_standards():
    standards = load_characterization_standards()
    assert "contact_resistance_methods" in standards
    assert "schottky_barrier_methods" in standards


def test_evaluate_rc_method():
    tlm = evaluate_rc_method_reliability("TLM")
    assert tlm["reliability_tier"] == "Gold_Standard"
    assert tlm["reliability_score"] == 10.0
    assert tlm["decouples_channel_resistance"] is True

    two_probe = evaluate_rc_method_reliability("Two_Probe_Extraction")
    assert two_probe["reliability_tier"] == "Error_Prone"
    assert two_probe["decouples_channel_resistance"] is False


def test_evaluate_sbh_method():
    richardson = evaluate_sbh_method_reliability("Modified_Richardson_Arrhenius")
    assert richardson["reliability_tier"] == "Gold_Standard"
    assert richardson["thermionic_scaling_power"] == 1.5

    single_iv = evaluate_sbh_method_reliability("Room_Temp_IV_Fitting")
    assert single_iv["reliability_tier"] == "Error_Prone"


def test_2d_thermionic_current():
    # Room temp (300 K), moderate barrier 0.2 eV
    curr_300 = compute_2d_thermionic_current(300, 0.2)
    assert curr_300 > 0.0

    # Lower temp (77 K), current drops exponentially
    curr_77 = compute_2d_thermionic_current(77, 0.2)
    assert 0.0 <= curr_77 < curr_300
