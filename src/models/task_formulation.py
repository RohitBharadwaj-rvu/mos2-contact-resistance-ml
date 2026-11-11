"""
Target Formulation and Multi-Task Architecture Definition (Sprint 2.a.1).
Defines formal single-task, multi-task, and physics-chained regression learning tasks for MoS2 contact resistance and Schottky barrier height.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

TASK_SPEC_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "learning_task_specifications.json"


def evaluate_target_correlations(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Evaluates empirical and theoretical coupling between log10(Rc) and SBH."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    subset = df[["log10_rc", "schottky_barrier_height_ev"]].dropna()
    corr = float(subset["log10_rc"].corr(subset["schottky_barrier_height_ev"]))
    
    return {
        "n_samples": len(subset),
        "pearson_r": round(corr, 3),
        "covariance": round(float(np.cov(subset["log10_rc"], subset["schottky_barrier_height_ev"])[0, 1]), 3)
    }


def define_learning_task_specifications() -> Dict[str, Any]:
    """
    Formalizes the machine learning task architectures:
    1. Primary Single-Task: Directly predict log10(Rc) from material & process features.
    2. Auxiliary Single-Task: Predict Schottky barrier height Phi_B from work function & architecture.
    3. Multi-Output Joint Regression: Predict [log10(Rc), Phi_B] simultaneously sharing representation.
    4. Physics-Chained Hybrid: Model 1 predicts Phi_B; Model 2 predicts log10(Rc) conditioned on predicted Phi_B.
    """
    spec = {
        "primary_task": {
            "name": "log10_contact_resistance_regression",
            "target_variable": "log10_rc",
            "unit": "log10(Ohm*um)",
            "loss_function": "MSE",
            "metric": "RMSE",
            "physical_significance": "Represents orders-of-magnitude contact resistance scaling; 0.1 dex error = 26% error."
        },
        "auxiliary_task": {
            "name": "schottky_barrier_height_regression",
            "target_variable": "schottky_barrier_height_ev",
            "unit": "eV",
            "loss_function": "MSE",
            "metric": "MAE",
            "physical_significance": "Measures interfacial potential barrier governing thermionic carrier injection."
        },
        "formulations": {
            "independent_single_task": {
                "description": "Fit separate estimators for log10_rc and Phi_B. Maximizes parameter dedication and prevents negative transfer in small-N regime.",
                "recommended": True,
                "rationale": "Given N=20, independent models prevent cross-task parameter interference and allow distinct regularizers for each target."
            },
            "joint_multi_task": {
                "description": "Multi-output regressor optimizing shared loss: L = L(log10_rc) + lambda * L(Phi_B).",
                "recommended": False,
                "rationale": "High target correlation (r=0.816) theoretically aids joint learning, but small sample size risks joint optimization instabilities."
            },
            "physics_chained_hybrid": {
                "description": "Stage 1 predicts Phi_B; Stage 2 predicts log10_rc using Stage 1 prediction as a dynamic input feature alongside carrier density.",
                "recommended": True,
                "rationale": "Directly embodies the thermionic emission physics: Rc ~ exp(q * Phi_B / kT)."
            }
        }
    }
    
    TASK_SPEC_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TASK_SPEC_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    s = define_learning_task_specifications()
    print("Learning task specifications generated successfully.")
