"""
Mathematical Search Space and Physical Constraints for Symbolic Regression (Sprint 2.d.2).
Defines protected mathematical primitives, parsimony penalties, and solid-state physical inductive constraints for equation discovery.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Callable
import numpy as np

SEARCH_SPACE_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "symbolic_search_space_config.json"


def protected_div(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    """Protected division avoiding zero-division singularities."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(np.abs(x2) > 1e-6, x1 / x2, 1.0)


def protected_exp(x: np.ndarray) -> np.ndarray:
    """Protected exponential clipping at +15.0 to prevent floating-point overflow."""
    with np.errstate(over="ignore", under="ignore"):
        return np.exp(np.clip(x, -20.0, 15.0))


def protected_log(x: np.ndarray) -> np.ndarray:
    """Protected natural logarithm avoiding negative and zero arguments."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(np.clip(np.abs(x), 1e-6, 1e12))


def protected_inv(x: np.ndarray) -> np.ndarray:
    """Protected reciprocal operation."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(np.abs(x) > 1e-6, 1.0 / x, 0.0)


def define_symbolic_search_space() -> Dict[str, Any]:
    """
    Defines the complete mathematical search configuration for equation discovery:
    1. Allowed primitives and protected transcendental functions.
    2. Parsimony penalties and tree structural limits.
    3. Physical inductive constraints (monotonicity, asymptotic limits).
    """
    config = {
        "primitive_operators": [
            {"name": "add", "symbol": "+", "arity": 2},
            {"name": "sub", "symbol": "-", "arity": 2},
            {"name": "mul", "symbol": "*", "arity": 2},
            {"name": "div", "symbol": "/", "arity": 2, "protected": True},
            {"name": "exp", "symbol": "exp", "arity": 1, "protected": True, "rationale": "Models thermionic exp(q*Phi / kT)"},
            {"name": "log", "symbol": "log", "arity": 1, "protected": True, "rationale": "Models logarithmic target and scaling"},
            {"name": "inv", "symbol": "1/x", "arity": 1, "protected": True, "rationale": "Models reciprocal density scaling"}
        ],
        "complexity_constraints": {
            "max_tree_depth": 4,
            "max_nodes": 12,
            "parsimony_coefficient": 0.035,
            "tournament_size": 20,
            "generations": 50,
            "population_size": 1000
        },
        "physical_inductive_constraints": [
            {
                "constraint": "positive_schottky_monotonicity",
                "formulation": "d(log10_rc) / d(Phi_B) >= 0",
                "physical_meaning": "Increasing barrier height must monotonically increase contact resistance."
            },
            {
                "constraint": "negative_gate_monotonicity",
                "formulation": "d(log10_rc) / d(n_2D) <= 0",
                "physical_meaning": "Electrostatic carrier accumulation must monotonically compress depletion width and decrease contact resistance."
            },
            {
                "constraint": "asymptotic_quantum_limit",
                "formulation": "lim_{n_2D -> inf, Phi_B -> 0} Rc >= R_quantum ~ 10-100 Ohm*um",
                "physical_meaning": "Contact resistance cannot drop below the Landauer-Sharvin ballistic quantum resistance limit."
            }
        ]
    }
    
    SEARCH_SPACE_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SEARCH_SPACE_JSON, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        
    return config


if __name__ == "__main__":
    cfg = define_symbolic_search_space()
    print("Symbolic search space defined successfully:")
    print(json.dumps(cfg, indent=2))
