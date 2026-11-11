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


def validate_physics_constraints(func: Callable[[np.ndarray, np.ndarray], np.ndarray],
                                 phi_bounds: tuple = (0.1, 1.2),
                                 n2d_bounds: tuple = (1e11, 1e13)) -> Dict[str, Any]:
    """
    Numerically audits a candidate symbolic function f(Phi_B, n_2D) -> log10(Rc)
    against solid-state physical constraints using finite-difference partial derivatives.
    """
    phi_grid = np.linspace(phi_bounds[0], phi_bounds[1], 20)
    n2d_grid = np.logspace(np.log10(n2d_bounds[0]), np.log10(n2d_bounds[1]), 20)
    
    # 1. Monotonicity in Phi_B (at fixed median n_2D)
    median_n2d = np.full_like(phi_grid, 1e12)
    rc_vs_phi = func(phi_grid, median_n2d)
    diff_phi = np.diff(rc_vs_phi)
    phi_monotonic = bool(np.all(diff_phi >= -1e-4))
    
    # 2. Negative monotonicity in n_2D (at fixed median Phi_B)
    median_phi = np.full_like(n2d_grid, 0.4)
    rc_vs_n2d = func(median_phi, n2d_grid)
    diff_n2d = np.diff(rc_vs_n2d)
    n2d_monotonic = bool(np.all(diff_n2d <= 1e-4))
    
    # 3. Quantum lower bound (log10(Rc) >= log10(10 Ohm*um) = 1.0)
    min_predicted_rc = float(np.min(func(np.array([phi_bounds[0]]), np.array([n2d_bounds[1]]))))
    quantum_valid = bool(min_predicted_rc >= 0.8)
    
    all_passed = phi_monotonic and n2d_monotonic and quantum_valid
    
    return {
        "passed_all_constraints": all_passed,
        "schottky_monotonicity": phi_monotonic,
        "gate_monotonicity": n2d_monotonic,
        "quantum_limit_valid": quantum_valid,
        "min_predicted_log10_rc": round(min_predicted_rc, 3)
    }


if __name__ == "__main__":
    cfg = define_symbolic_search_space()
    print("Symbolic search space defined successfully:")
    print(json.dumps(cfg, indent=2))
