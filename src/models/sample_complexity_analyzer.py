"""
Sample-to-Feature Ratio and Model Complexity Constraint Analyzer (Sprint 2.a.2).
Evaluates dataset degrees of freedom, sample-to-feature ratios, and establishes strict mathematical bounds on model capacity to prevent overfitting in small-N tabular regimes.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

COMPLEXITY_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "model_complexity_constraints.json"


def compute_sample_complexity_constraints(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Computes rigorous capacity limits and feature budgets for the N=20 MoS2 contact dataset.
    Follows Harrell's heuristic and Vapnik-Chervonenkis (VC) generalization bounds.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    n_samples = len(df)
    n_groups = df["source_uid"].nunique()
    
    # Harrell's guideline: N / P >= 5 to 10
    # For N=20: P_max = 20 / 5 = 4 features
    max_features_parsimonious = max(1, int(n_samples / 5))
    max_features_strict = max(1, int(n_samples / 10))
    
    constraints = {
        "dataset_dimensions": {
            "n_samples": n_samples,
            "n_literature_clusters": n_groups,
            "effective_dof_cluster": n_groups - 1
        },
        "feature_budgets": {
            "unregularized_linear_max_features": max_features_strict,
            "regularized_linear_max_features": max_features_parsimonious,
            "recommended_active_features": 4,
            "minimum_sample_to_feature_ratio": "5:1"
        },
        "model_architecture_constraints": {
            "linear_models": {
                "regularization": "MANDATORY (L1 Lasso, L2 Ridge, or ElasticNet)",
                "max_active_weights": 4,
                "alpha_tuning_range": [1e-3, 1e2]
            },
            "decision_tree_ensembles": {
                "max_depth": 3,
                "min_samples_split": 4,
                "min_samples_leaf": 2,
                "n_estimators": 50,
                "max_features": "sqrt",
                "rationale": "Deep trees will isolate single data points and memorize noise; shallow depth prevents sample fragmentation."
            },
            "gaussian_processes": {
                "kernel_families": ["RBF", "Matern52", "DotProduct"],
                "length_scale_bounds": [0.1, 10.0],
                "noise_level_alpha": ">= 0.05",
                "rationale": "Gaussian processes provide closed-form Bayesian uncertainty estimation naturally robust to small N."
            },
            "symbolic_regression": {
                "max_equation_length_nodes": 12,
                "parsimony_coefficient": 0.05,
                "allowed_operators": ["add", "sub", "mul", "div", "exp", "log"],
                "rationale": "High node complexity results in non-physical polynomial fitting."
            }
        },
        "overfitting_risk_assessment": {
            "risk_level": "HIGH_IF_UNCONSTRAINED",
            "mitigation_protocol": [
                "Strict feature selection to top 3-4 physical descriptors",
                "Paper-wise GroupKFold cross-validation",
                "Regularization penalties on all parametric models",
                "Ensemble averaging and Bayesian shrinkage"
            ]
        }
    }
    
    COMPLEXITY_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLEXITY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(constraints, f, indent=2)
        
    return constraints


if __name__ == "__main__":
    c = compute_sample_complexity_constraints()
    print("Computed model complexity constraints:")
    print(json.dumps(c, indent=2))
