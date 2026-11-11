"""
Symbolic Regression Input Variable Selector (Sprint 4.d.1).
Selects and scales a compact set of 3-4 primary physical variables for equation discovery,
preventing combinatorial explosion and enforcing dimensional / numerical stability.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

SYMBOLIC_VARS_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "symbolic_input_variables.json"


def select_symbolic_input_variables(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Selects and normalizes the primary physical inputs for symbolic equation discovery:
    1. x1: Schottky Barrier Height (Phi_B, eV)
    2. x2: Gate Carrier Density normalized (n_2D / 1e13 cm^-2)
    3. x3: van der Waals / De-pinning binary indicator (0 or 1)
    4. x4: Interfacial Reactivity / Enthalpy normalized (-Delta H_f / 500 kJ/mol)
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    selected_variables = [
        {
            "symbol": "x_sbh",
            "feature_col": "physics_predicted_sbh_ev",
            "unit": "eV",
            "range": [float(df["physics_predicted_sbh_ev"].min()), float(df["physics_predicted_sbh_ev"].max())],
            "scaling": "identity",
            "physical_meaning": "Schottky barrier height governing thermionic injection barrier"
        },
        {
            "symbol": "x_n2d",
            "feature_col": "gate_carrier_density_cm2",
            "unit": "10^13 cm^-2",
            "range": [
                float((df["gate_carrier_density_cm2"] / 1e13).min()),
                float((df["gate_carrier_density_cm2"] / 1e13).max())
            ],
            "scaling": "divide_by_1e13",
            "physical_meaning": "Electrostatic gate-induced channel carrier density modulating barrier width and tunneling"
        },
        {
            "symbol": "x_vdw",
            "feature_col": "is_vdw_or_depinned_contact",
            "unit": "dimensionless {0, 1}",
            "range": [0.0, 1.0],
            "scaling": "identity",
            "physical_meaning": "De-pinning binary flag indicating pristine van der Waals interface"
        },
        {
            "symbol": "x_hf",
            "feature_col": "sulfide_formation_enthalpy_kj_mol",
            "unit": "dimensionless ratio (-Delta_Hf / 500 kJ/mol)",
            "range": [
                float((-df["sulfide_formation_enthalpy_kj_mol"] / 500.0).min()),
                float((-df["sulfide_formation_enthalpy_kj_mol"] / 500.0).max())
            ],
            "scaling": "neg_divide_by_500",
            "physical_meaning": "Thermodynamic metal sulfide formation enthalpy indicating interface chemical bond energy"
        }
    ]

    # Compute correlation with target
    correlations = {}
    X_scaled = pd.DataFrame()
    X_scaled["x_sbh"] = df["physics_predicted_sbh_ev"]
    X_scaled["x_n2d"] = df["gate_carrier_density_cm2"] / 1e13
    X_scaled["x_vdw"] = df["is_vdw_or_depinned_contact"]
    X_scaled["x_hf"] = -df["sulfide_formation_enthalpy_kj_mol"] / 500.0

    target = df["log10_rc"]
    for col in X_scaled.columns:
        correlations[col] = {
            "pearson_r": round(float(X_scaled[col].corr(target, method="pearson")), 4),
            "spearman_rho": round(float(X_scaled[col].corr(target, method="spearman")), 4)
        }

    spec = {
        "title": "Selected Physical Input Variables for Symbolic Regression Discovery",
        "rationale": (
            "Restricts equation search to 4 dimensionally well-scaled solid-state descriptors "
            "spanning barrier physics, electrostatic gating, interface de-pinning, and chemical bond formation. "
            "Prevents combinatorial explosion and division-by-zero or numerical underflow in genetic programming."
        ),
        "target_variable": "log10_rc",
        "variables": selected_variables,
        "correlations_with_target": correlations
    }

    SYMBOLIC_VARS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SYMBOLIC_VARS_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    return spec


def get_scaled_symbolic_dataset(df: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Returns (X_scaled, y) DataFrame and target array ready for symbolic regression engines.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    X = pd.DataFrame(index=df.index)
    X["x_sbh"] = df["physics_predicted_sbh_ev"]
    X["x_n2d"] = df["gate_carrier_density_cm2"] / 1e13
    X["x_vdw"] = df["is_vdw_or_depinned_contact"].astype(float)
    X["x_hf"] = -df["sulfide_formation_enthalpy_kj_mol"] / 500.0

    y = df["log10_rc"].values
    return X, y


if __name__ == "__main__":
    res = select_symbolic_input_variables()
    print("Symbolic regression input variables selected.")
    for v in res["variables"]:
        print(f"  - {v['symbol']}: {v['feature_col']} ({v['unit']})")
