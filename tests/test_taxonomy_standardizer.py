"""Tests for Categorical Taxonomy Standardizer."""

from src.features.taxonomy_standardizer import (
    load_categorical_taxonomies,
    standardize_deposition_method,
    standardize_contact_architecture,
    standardize_gate_dielectric,
    standardize_annealing_ambient
)


def test_load_taxonomies():
    tax = load_categorical_taxonomies()
    assert "deposition_method_mappings" in tax
    assert "architecture_mappings" in tax
    assert "dielectric_mappings" in tax


def test_standardize_deposition():
    assert standardize_deposition_method("e-beam") == "E_beam_Evaporation"
    assert standardize_deposition_method("dry transfer") == "Dry_Transfer"
    assert standardize_deposition_method("sputtering") == "Sputtering"


def test_standardize_architecture():
    assert standardize_contact_architecture("semimetal vdw") == "Semimetal_vdW"
    assert standardize_contact_architecture("1t phase") == "Phase_Engineered_1T"
    assert standardize_contact_architecture("top contact") == "Top_Contact"


def test_standardize_dielectric():
    assert standardize_gate_dielectric("SiO2/Si") == "SiO2"
    assert standardize_gate_dielectric("h-BN") == "hBN"
    assert standardize_gate_dielectric("Al2O3") == "Al2O3"


def test_standardize_anneal():
    assert standardize_annealing_ambient("forming gas") == "Ar/H2_Forming_Gas"
    assert standardize_annealing_ambient(None) == "None"
    assert standardize_annealing_ambient("vacuum") == "Vacuum"
