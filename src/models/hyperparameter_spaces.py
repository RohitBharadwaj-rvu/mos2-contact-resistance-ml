"""
Hyperparameter Space and Capacity Control Catalog (Sprint 4.c.1).
Defines systematic hyperparameter search grids, capacity controls, and regularization mechanisms tailored to small-N Grouped CV.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

HYPERPARAMS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "hyperparameter_search_spaces.json"


def define_hyperparameter_search_spaces() -> Dict[str, Any]:
    """
    Catalogues the exact hyperparameter search spaces for each shortlisted architecture,
    explaining the regularizing mechanism of each parameter.
    """
    spaces = {
        "Ridge_Regression": {
            "family": "linear_regularized",
            "search_grid": {
                "regressor__alpha": [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0]
            },
            "regularization_mechanism": "L2 penalty shrinks feature weights toward zero, stabilizing matrix inversion under collinear physical inputs."
        },
        "ElasticNet": {
            "family": "linear_regularized",
            "search_grid": {
                "regressor__alpha": [0.01, 0.05, 0.1, 0.2, 0.5, 1.0],
                "regressor__l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9]
            },
            "regularization_mechanism": "Convex mixture of L1 sparsity (feature elimination) and L2 ridge shrinkage."
        },
        "Gradient_Boosting": {
            "family": "tree_ensemble",
            "search_grid": {
                "n_estimators": [20, 30, 50, 75],
                "learning_rate": [0.01, 0.03, 0.05, 0.1],
                "max_depth": [2, 3],
                "subsample": [0.7, 0.8, 1.0],
                "min_samples_leaf": [2, 3]
            },
            "regularization_mechanism": "Shallow max_depth (<=3) prevents leaf fragmentation; low learning_rate slows gradient steps; subsample adds stochastic bagging."
        },
        "Random_Forest": {
            "family": "tree_ensemble",
            "search_grid": {
                "n_estimators": [30, 50, 80],
                "max_depth": [2, 3],
                "min_samples_split": [3, 4, 6],
                "min_samples_leaf": [2, 3]
            },
            "regularization_mechanism": "Random feature subsampling at splits combined with leaf-size thresholds prevents isolating single literature records."
        },
        "Gaussian_Process_Matern": {
            "family": "bayesian_kernel",
            "search_grid": {
                "length_scale_init": [0.5, 1.0, 2.0, 5.0],
                "noise_level_init": [0.01, 0.05, 0.1, 0.2],
                "nu": [1.5, 2.5]
            },
            "regularization_mechanism": "WhiteKernel noise parameter absorbs experimental measurement scatter without distorting underlying solid-state curves."
        },
        "Support_Vector_Regression_RBF": {
            "family": "kernel_margin",
            "search_grid": {
                "regressor__C": [0.5, 1.0, 2.0, 5.0, 10.0, 20.0],
                "regressor__epsilon": [0.02, 0.05, 0.1, 0.2],
                "regressor__gamma": ["scale", 0.05, 0.1, 0.2, 0.5]
            },
            "regularization_mechanism": "Epsilon-insensitive tube ignores minor characterization noise; C restricts dual weight magnitude."
        }
    }
    
    spec = {
        "title": "Hyperparameter Search Space and Capacity Catalog for MoS2 ML",
        "guidelines": "Evaluated strictly via GroupKFold(n_splits=5, groups=source_uid) using composite selection score",
        "search_spaces": spaces
    }
    
    HYPERPARAMS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HYPERPARAMS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    s = define_hyperparameter_search_spaces()
    print("Hyperparameter search spaces defined successfully.")
