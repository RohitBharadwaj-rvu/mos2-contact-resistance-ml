"""Tests for Completeness and Consistency Auditor."""

from src.data.completeness_auditor import (
    audit_source_completeness,
    execute_completeness_audit,
    get_curated_modeling_dataset_sources,
    COMPLETENESS_AUDIT_PATH
)


def test_execute_audit():
    results = execute_completeness_audit()
    assert len(results) >= 15
    assert COMPLETENESS_AUDIT_PATH.exists()


def test_quarantine_two_probe():
    paper = {
        "id": "ref_008_radisavljevic_2011",
        "contact_metal": "Au",
        "contact_type": "Evaporated",
        "carrier_type": "n-type",
        "temperature_k": 300,
        "characterization_method": "Two-probe extracted",
        "reported_rc_ohm_um": 8500.0,
        "reported_sbh_ev": 0.55
    }
    method_record = {"composite_quality_score": 64}
    res = audit_source_completeness(paper, method_record)
    assert res["curation_decision"] == "QUARANTINED_AUXILIARY"
    assert "Two-probe" in res["quarantine_reason"] or "Suboptimal metrology" in res["quarantine_reason"]


def test_accept_high_quality_tlm():
    paper = {
        "id": "ref_001_shen_2021",
        "contact_metal": "Bi",
        "contact_type": "Semimetal vdW",
        "carrier_type": "n-type",
        "temperature_k": 300,
        "characterization_method": "TLM",
        "reported_rc_ohm_um": 123.0,
        "reported_sbh_ev": 0.0
    }
    method_record = {"composite_quality_score": 100}
    res = audit_source_completeness(paper, method_record)
    assert res["curation_decision"] == "ACCEPTED_PRIMARY_MODELING"
    assert res["quarantine_reason"] is None


def test_curated_dataset_sources():
    sources = get_curated_modeling_dataset_sources()
    assert len(sources) >= 12
    assert "ref_001_shen_2021" in sources
    assert "ref_008_radisavljevic_2011" not in sources  # Quarantined
