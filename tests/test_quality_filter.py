"""Tests for Inclusion/Exclusion Quality Filter."""

from src.data.quality_filter import (
    load_inclusion_exclusion_criteria,
    audit_candidate_record
)


def test_load_criteria():
    criteria = load_inclusion_exclusion_criteria()
    assert "inclusion_rules" in criteria
    assert "exclusion_rules" in criteria
    assert len(criteria["inclusion_rules"]) >= 5
    assert len(criteria["exclusion_rules"]) >= 5


def test_valid_record_accepted():
    record = {
        "title": "Ultralow contact resistance in MoS2 using Bi semimetal",
        "contact_metal": "Bi",
        "reported_rc_ohm_um": 123.0,
        "reported_sbh_ev": 0.0,
        "characterization_method": "TLM",
        "abstract": "TLM measurements demonstrate low resistance on MoS2 FETs."
    }
    accepted, passed, rejections = audit_candidate_record(record)
    assert accepted is True
    assert len(rejections) == 0
    assert len(passed) >= 3


def test_off_topic_rejected():
    record = {
        "title": "MoS2 nanosheets for hydrogen evolution reaction and photocatalysis",
        "contact_metal": "Pt",
        "reported_rc_ohm_um": 100.0,
        "characterization_method": "TLM",
        "abstract": "We evaluate photocatalytic water splitting."
    }
    accepted, passed, rejections = audit_candidate_record(record)
    assert accepted is False
    assert any("EXC-03" in r for r in rejections)


def test_two_probe_rejected():
    record = {
        "title": "Electrical transport in MoS2",
        "contact_metal": "Au",
        "reported_rc_ohm_um": 8000.0,
        "characterization_method": "Two-probe extracted",
        "abstract": "Two-probe measurement of MoS2."
    }
    accepted, passed, rejections = audit_candidate_record(record)
    assert accepted is False
    assert any("EXC-02" in r for r in rejections)


def test_unphysical_sbh_rejected():
    record = {
        "title": "Metal contact on MoS2",
        "contact_metal": "Pt",
        "reported_sbh_ev": 3.5,  # Exceeds bandgap!
        "characterization_method": "TLM",
        "abstract": "MoS2 contact."
    }
    accepted, passed, rejections = audit_candidate_record(record)
    assert accepted is False
    assert any("EXC-04" in r for r in rejections)
