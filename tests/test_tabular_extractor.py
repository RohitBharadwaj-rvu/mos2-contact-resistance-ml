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


def test_transfer_length_and_resistivity():
    from src.data.tabular_extractor import compute_transfer_length_um, convert_rc_to_specific_resistivity
    # Rc = 500 Ohm*um, R_sh = 10,000 Ohm/sq -> L_T = 0.05 um
    lt = compute_transfer_length_um(500.0, 10000.0)
    assert lt == 0.05

    # rho_c = (500 * 1e-4)^2 / 10000 = (0.05)^2 / 10000 = 2.5e-7 Ohm*cm^2
    rho_c = convert_rc_to_specific_resistivity(500.0, 10000.0)
    assert abs(rho_c - 2.5e-7) < 1e-9
