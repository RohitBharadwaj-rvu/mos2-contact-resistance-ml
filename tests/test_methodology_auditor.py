"""Tests for Methodological Quality Auditor."""

from src.data.methodology_auditor import (
    audit_full_text_methodology,
    load_methodology_audit,
    AUDIT_OUT_JSON,
    AUDIT_OUT_CSV
)


def test_audit_execution():
    records = audit_full_text_methodology()
    assert len(records) >= 15
    assert AUDIT_OUT_JSON.exists()
    assert AUDIT_OUT_CSV.exists()


def test_quality_tiers():
    records = load_methodology_audit()
    tiers = [r["quality_tier"] for r in records]
    assert "Tier_1_Exceptional" in tiers
    
    # shen_2021 and english_2016 should be Tier 1
    shen = next(r for r in records if r["id"] == "ref_001_shen_2021")
    assert shen["composite_quality_score"] >= 90
    assert shen["quality_tier"] == "Tier_1_Exceptional"

    # radisavljevic_2011 has two-probe extraction, should be lowest tier
    rad = next(r for r in records if r["id"] == "ref_008_radisavljevic_2011")
    assert rad["composite_quality_score"] < 70
