"""
Unit Standardization and Physical Conversion Engine.
Converts heterogeneous literature units (kOhm*um, Ohm*mm, Pa, mbar, eV, meV, C, K) to standardized SI/device units.
"""

from typing import Dict, Any, Optional
import math


def standardize_contact_resistance(value: float, input_unit: str = "Ohm*um", channel_width_um: Optional[float] = None) -> float:
    """
    Standardizes contact resistance into Ohm*um.
    Supported units: 'Ohm*um', 'kOhm*um', 'Ohm*mm', 'Ohm' (requires channel_width_um).
    """
    unit = input_unit.strip().lower()
    if unit in ["ohm*um", "ω*μm", "ohm*micron"]:
        return float(value)
    elif unit in ["kohm*um", "kω*μm"]:
        return float(value * 1000.0)
    elif unit in ["ohm*mm", "ω*mm"]:
        return float(value * 1000.0)
    elif unit in ["ohm", "ω"]:
        if channel_width_um is None or channel_width_um <= 0:
            raise ValueError("Absolute resistance in Ohms requires positive channel_width_um to normalize")
        return float(value * channel_width_um)
    else:
        raise ValueError(f"Unsupported contact resistance unit '{input_unit}'")


def standardize_barrier_height(value: float, input_unit: str = "eV") -> float:
    """
    Standardizes Schottky barrier height into eV.
    Supported units: 'eV', 'meV', 'Joules'.
    """
    unit = input_unit.strip().lower()
    if unit == "ev":
        return float(value)
    elif unit == "mev":
        return float(value / 1000.0)
    elif unit in ["joule", "joules", "j"]:
        return float(value / 1.602176634e-19)
    else:
        raise ValueError(f"Unsupported barrier height unit '{input_unit}'")


def standardize_temperature(value: float, input_unit: str = "K") -> float:
    """
    Standardizes temperature into Kelvin (K).
    Supported units: 'K', 'C', 'Celsius', 'F', 'Fahrenheit'.
    """
    unit = input_unit.strip().lower()
    if unit in ["k", "kelvin"]:
        return float(value)
    elif unit in ["c", "celsius"]:
        return float(value + 273.15)
    elif unit in ["f", "fahrenheit"]:
        return float((value - 32.0) * (5.0 / 9.0) + 273.15)
    else:
        raise ValueError(f"Unsupported temperature unit '{input_unit}'")


def standardize_pressure(value: float, input_unit: str = "Torr") -> float:
    """
    Standardizes vacuum chamber base pressure into Torr.
    Supported units: 'Torr', 'mbar', 'bar', 'Pa'.
    """
    unit = input_unit.strip().lower()
    if unit == "torr":
        return float(value)
    elif unit == "mbar":
        return float(value * 0.750062)
    elif unit == "bar":
        return float(value * 750.062)
    elif unit == "pa":
        return float(value * 0.00750062)
    else:
        raise ValueError(f"Unsupported pressure unit '{input_unit}'")


def standardize_thickness(value: float, input_unit: str = "nm", layer_count: Optional[int] = None) -> float:
    """
    Standardizes semiconductor thickness into nanometers (nm).
    Supported units: 'nm', 'angstrom', 'layer_count'.
    Monolayer MoS2 = 0.65 nm.
    """
    unit = input_unit.strip().lower()
    if unit == "nm":
        return float(value)
    elif unit in ["angstrom", "a", "å"]:
        return float(value * 0.1)
    elif unit in ["layer_count", "layers"]:
        count = layer_count if layer_count is not None else int(value)
        return float(count * 0.65)
    else:
        raise ValueError(f"Unsupported thickness unit '{input_unit}'")


def compute_carrier_density_from_gate(
    v_gs: float,
    v_th: float,
    dielectric_thickness_nm: float = 300.0,
    dielectric_rel_permittivity: float = 3.9
) -> float:
    """
    Computes 2D carrier density n_2D (cm^-2) from gate overdrive (V_gs - V_th):
    C_ox = eps_0 * eps_r / t_ox (F/cm^2)
    n_2D = C_ox * (V_gs - V_th) / q
    """
    eps_0 = 8.854187817e-14  # F/cm
    q = 1.602176634e-19      # Coulombs
    t_ox_cm = dielectric_thickness_nm * 1e-7
    c_ox = (eps_0 * dielectric_rel_permittivity) / t_ox_cm
    
    overdrive = max(0.0, v_gs - v_th)
    n_2d = (c_ox * overdrive) / q
    return float(f"{n_2d:.2e}")
