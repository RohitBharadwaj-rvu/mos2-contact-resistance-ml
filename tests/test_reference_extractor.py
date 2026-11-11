"""Tests for Elemental and Material Reference Data Extractor."""

from src.data.reference_extractor import (
    export_reference_dataset,
    load_reference_dataframe,
    EXTENDED_ELEMENTAL_PROPERTIES
)


def test_export_and_load_reference():
    paths = export_reference_dataset()
    assert paths["csv"].exists()
    assert paths["json"].exists()

    df = load_reference_dataframe()
    assert len(df) == len(EXTENDED_ELEMENTAL_PROPERTIES)
    assert len(df) >= 15
    assert "work_function_ev" in df.columns
    assert "electronegativity_pauling" in df.columns
    assert "sulfide_formation_enthalpy_kj_per_mol_s" in df.columns
    assert "d_band_center_ev" in df.columns


def test_property_ranges():
    df = load_reference_dataframe()
    # Work function physically between 2.5 eV and 6.0 eV
    assert (df["work_function_ev"] >= 2.5).all()
    assert (df["work_function_ev"] <= 6.0).all()

    # Electronegativity physically between 1.0 and 3.0
    assert (df["electronegativity_pauling"] >= 1.0).all()
    assert (df["electronegativity_pauling"] <= 3.0).all()
