"""Tests for Unit Standardization Engine."""

import pytest
from src.features.unit_standardizer import (
    standardize_contact_resistance,
    standardize_barrier_height,
    standardize_temperature,
    standardize_pressure,
    standardize_thickness,
    compute_carrier_density_from_gate
)


def test_standardize_rc():
    # 1.2 kOhm*um -> 1200 Ohm*um
    assert standardize_contact_resistance(1.2, "kOhm*um") == 1200.0
    # 0.5 Ohm*mm -> 500 Ohm*um
    assert standardize_contact_resistance(0.5, "Ohm*mm") == 500.0
    # 100 Ohm absolute on 5 um wide channel -> 500 Ohm*um
    assert standardize_contact_resistance(100.0, "Ohm", channel_width_um=5.0) == 500.0


def test_standardize_barrier():
    assert standardize_barrier_height(250.0, "meV") == 0.25
    assert standardize_barrier_height(0.35, "eV") == 0.35


def test_standardize_temp():
    assert standardize_temperature(25.0, "C") == 298.15
    assert standardize_temperature(300.0, "K") == 300.0


def test_standardize_pressure():
    # 1.33e-4 mbar ~ 1e-4 Torr
    torr = standardize_pressure(1.33322e-4, "mbar")
    assert abs(torr - 1.0e-4) < 1e-6


def test_standardize_thickness():
    # Monolayer
    assert standardize_thickness(1, "layer_count") == 0.65
    # 6.5 Angstroms -> 0.65 nm
    assert abs(standardize_thickness(6.5, "angstrom") - 0.65) < 1e-4


def test_compute_carrier_density():
    # 300 nm SiO2 (eps=3.9), 40 V overdrive: n_2D ~ 2.9e12 cm^-2
    n_2d = compute_carrier_density_from_gate(50.0, 10.0, 300.0, 3.9)
    assert 2.5e12 <= n_2d <= 3.2e12
