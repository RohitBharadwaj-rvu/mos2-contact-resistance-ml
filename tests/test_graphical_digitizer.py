"""Tests for Graphical Data Digitizer."""

from src.data.graphical_digitizer import (
    save_digitized_dataset,
    load_digitized_curves,
    transform_pixel_to_physical,
    get_pinning_factor_from_digitized_sbh,
    DIGITIZED_DATA_PATH
)


def test_save_and_load_digitized():
    path = save_digitized_dataset()
    assert path.exists()
    curves = load_digitized_curves()
    assert len(curves) >= 3
    assert DIGITIZED_DATA_PATH.exists()


def test_pixel_transformation_linear():
    # 0 to 100 px maps to 0 to 10 eV
    x_val, y_val = transform_pixel_to_physical(
        px=50.0, py=50.0,
        ref_x_px=(0.0, 100.0), ref_x_val=(0.0, 10.0),
        ref_y_px=(100.0, 0.0), ref_y_val=(0.0, 10.0),
        log_x=False, log_y=False
    )
    assert abs(x_val - 5.0) < 1e-4
    assert abs(y_val - 5.0) < 1e-4


def test_pixel_transformation_log():
    # 0 to 100 px maps to 10^1 to 10^3 (10 to 1000)
    x_val, y_val = transform_pixel_to_physical(
        px=50.0, py=50.0,
        ref_x_px=(0.0, 100.0), ref_x_val=(10.0, 1000.0),
        ref_y_px=(100.0, 0.0), ref_y_val=(10.0, 1000.0),
        log_x=True, log_y=True
    )
    # Log midpoint between 1 and 3 is 2 -> 10^2 = 100
    assert abs(x_val - 100.0) < 1e-3
    assert abs(y_val - 100.0) < 1e-3


def test_pinning_factor_calculation():
    s_factor = get_pinning_factor_from_digitized_sbh()
    # In Allain et al. 2015, Fermi-level pinning factor S ~ 0.1 - 0.25
    assert 0.10 <= s_factor <= 0.30
