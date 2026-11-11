"""Tests for Extraction Schema and Row Validator."""

from src.data.extraction_schema import (
    load_extraction_schema,
    validate_extraction_row,
    create_empty_row_template
)


def test_load_schema():
    schema = load_extraction_schema()
    assert "properties" in schema
    assert "required" in schema
    assert "contact_metal" in schema["required"]
    assert "provenance_location" in schema["required"]


def test_valid_row():
    row = {
        "data_point_id": "DP-001",
        "source_uid": "SRC-EXP-2021-SHEN",
        "contact_metal": "Bi",
        "contact_architecture": "Semimetal_vdW",
        "layer_count": 1,
        "characterization_method": "TLM",
        "measurement_temperature_k": 300.0,
        "contact_resistance_rc_ohm_um": 123.0,
        "schottky_barrier_height_ev": 0.0,
        "provenance_location": "Figure 2c, page 213"
    }
    is_valid, errors = validate_extraction_row(row)
    assert is_valid is True
    assert len(errors) == 0


def test_invalid_row_missing_required():
    row = {
        "data_point_id": "DP-002",
        "contact_metal": "Ti"
        # Missing source_uid, provenance_location, etc.
    }
    is_valid, errors = validate_extraction_row(row)
    assert is_valid is False
    assert len(errors) >= 3


def test_create_template():
    template = create_empty_row_template()
    assert "data_point_id" in template
    assert "contact_resistance_rc_ohm_um" in template
    assert "provenance_location" in template
