"""
Semiconductor Characterization Standards and Metrology Evaluator.
Defines reliability criteria, 2D thermionic models, and measurement quality metrics for Rc and SBH.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

STANDARDS_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "characterization_standards.json"


def load_characterization_standards() -> Dict[str, Any]:
    """Loads semiconductor characterization standards and error bounds."""
    if not STANDARDS_PATH.exists():
        raise FileNotFoundError(f"Standards file not found at {STANDARDS_PATH}")
    with open(STANDARDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_rc_method_reliability(method_name: str) -> Dict[str, Any]:
    """
    Evaluates reliability tier, score, and error characteristics for contact resistance extraction method.
    """
    standards = load_characterization_standards()
    methods = standards.get("contact_resistance_methods", {})
    
    # Fuzzy match method key
    for key, val in methods.items():
        if key.lower() in method_name.lower() or method_name.lower() in val["name"].lower():
            return val
            
    return {
        "name": method_name,
        "reliability_tier": "Unrecognized",
        "reliability_score": 0.0,
        "typical_uncertainty_percent": 50.0,
        "decouples_channel_resistance": False
    }


def evaluate_sbh_method_reliability(method_name: str) -> Dict[str, Any]:
    """
    Evaluates reliability tier, score, and error characteristics for Schottky barrier extraction method.
    """
    standards = load_characterization_standards()
    methods = standards.get("schottky_barrier_methods", {})
    
    for key, val in methods.items():
        if key.lower() in method_name.lower() or method_name.lower() in val["name"].lower():
            return val
            
    return {
        "name": method_name,
        "reliability_tier": "Unrecognized",
        "reliability_score": 0.0,
        "typical_uncertainty_ev": 0.25,
        "flatband_extrapolation_required": True
    }


def compute_2d_thermionic_current(
    temperature_k: float,
    barrier_height_ev: float,
    richardson_constant_a_cm2_k1p5: float = 30.0,
    area_cm2: float = 1e-8
) -> float:
    """
    Computes 2D thermionic emission current according to:
    I_2D = A * A_2D^* * T^(3/2) * exp(-q * Phi_B / (k_B * T))
    Note the T^(3/2) temperature scaling derived from 2D density of states.
    """
    import math
    if temperature_k <= 0:
        return 0.0
    k_b = 8.617333262e-5  # eV/K
    exponent = -barrier_height_ev / (k_b * temperature_k)
    # Numerical protection against underflow
    if exponent < -80:
        return 0.0
    i_2d = area_cm2 * richardson_constant_a_cm2_k1p5 * (temperature_k ** 1.5) * math.exp(exponent)
    return i_2d
