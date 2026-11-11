"""Tests for Material Property Databases and Baseline Physical Constants."""

from src.data.material_databases import (
    load_material_databases,
    get_metal_properties,
    get_mos2_properties,
    compute_schottky_mott_barrier,
    BASELINE_METAL_PROPERTIES
)


def test_load_material_databases():
    dbs = load_material_databases()
    assert len(dbs) >= 5
    ids = [d["id"] for d in dbs]
    assert "materials_project" in ids
    assert "c2db" in ids
    assert "nist_srd" in ids


def test_get_metal_properties():
    ti = get_metal_properties("Ti")
    assert ti is not None
    assert ti["work_function_ev"] == 4.33
    assert ti["contact_class"] == "reactive_3d_metal"
    
    bi = get_metal_properties("Bi")
    assert bi is not None
    assert bi["contact_class"] == "semimetal_vdw_gapless"

    w = get_metal_properties("W")
    assert w is not None
    assert w["contact_class"] == "refractory_metal"

    graphene = get_metal_properties("Graphene")
    assert graphene is not None
    assert graphene["contact_class"] == "2d_vdw_interlayer"


def test_fermi_shift():
    from src.data.material_databases import compute_gate_modulated_fermi_shift
    shift_zero = compute_gate_modulated_fermi_shift(0)
    assert shift_zero == 0.0

    shift_high_n = compute_gate_modulated_fermi_shift(1e13)
    # At 10^13 cm^-2, Fermi level shifts into conduction band by ~25-50 meV
    assert 0.02 <= shift_high_n <= 0.15


def test_get_mos2_properties():
    mono = get_mos2_properties("monolayer")
    assert mono is not None
    assert mono["bandgap_direct_ev"] == 1.80
    assert mono["electron_affinity_ev"] == 4.20


def test_compute_schottky_mott_barrier():
    # Ti: 4.33 - 4.20 = 0.13 eV
    sb_ti = compute_schottky_mott_barrier("Ti", "monolayer")
    assert abs(sb_ti - 0.13) < 1e-4

    # Au: 5.10 - 4.20 = 0.90 eV
    sb_au = compute_schottky_mott_barrier("Au", "monolayer")
    assert abs(sb_au - 0.90) < 1e-4
