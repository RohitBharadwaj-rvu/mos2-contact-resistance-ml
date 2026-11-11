"""Tests for Data Provenance Tracker."""

from src.data.provenance_tracker import (
    build_provenance_ledger,
    load_provenance_ledger,
    find_provenance_by_datapoint,
    generate_record_hash,
    PROVENANCE_JSON_PATH,
    PROVENANCE_CSV_PATH
)


def test_build_and_load_provenance():
    records = build_provenance_ledger()
    assert len(records) >= 20
    assert PROVENANCE_JSON_PATH.exists()
    assert PROVENANCE_CSV_PATH.exists()


def test_provenance_lookup():
    prov = find_provenance_by_datapoint("DP-001")
    assert prov is not None
    assert prov["source_uid"] == "SRC-EXP-2021-SHEN"
    assert "Figure 2c" in prov["provenance_location"]
    assert prov["verification_status"] == "Verified_Against_Primary_Source"
    assert len(prov["verification_hash"]) == 16


def test_hash_determinism():
    rec = {
        "data_point_id": "DP-TEST",
        "source_uid": "SRC-TEST",
        "contact_metal": "Au",
        "contact_resistance_rc_ohm_um": 500.0,
        "schottky_barrier_height_ev": 0.4,
        "provenance_location": "Fig 1"
    }
    h1 = generate_record_hash(rec)
    h2 = generate_record_hash(rec)
    assert h1 == h2
