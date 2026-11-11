"""Tests for Tabular Literature Data Extractor."""

from src.data.tabular_extractor import (
    export_tabular_dataset,
    load_tabular_dataset,
    VERIFIED_LITERATURE_DATA_POINTS,
    TABULAR_CSV_PATH,
    TABULAR_JSON_PATH
)


def test_export_and_load_tabular():
    paths = export_tabular_dataset()
    assert paths["csv"].exists()
    assert paths["json"].exists()

    df = load_tabular_dataset()
    assert len(df) == len(VERIFIED_LITERATURE_DATA_POINTS)
    assert len(df) >= 20
    assert "contact_resistance_rc_ohm_um" in df.columns
    assert "schottky_barrier_height_ev" in df.columns


def test_no_null_critical_targets():
    df = load_tabular_dataset()
    # Every row must have at least one valid target (Rc or SBH)
    has_target = df["contact_resistance_rc_ohm_um"].notnull() | df["schottky_barrier_height_ev"].notnull()
    assert has_target.all()


def test_unique_datapoint_ids():
    df = load_tabular_dataset()
    assert len(df["data_point_id"].unique()) == len(df)
