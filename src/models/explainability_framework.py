"""
Post-Hoc Model Interpretability and Feature Attribution Framework (Sprint 2.e.1).
Defines SHAP (TreeSHAP/KernelSHAP), Permutation Importance, and Partial Dependence methodologies for dissecting MoS2 contact predictions.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.model_factory import instantiate_candidate_model
from src.models.sample_complexity_analyzer import select_parsimonious_features

EXPLAINABILITY_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "explainability_methodology.json"


def evaluate_post_hoc_explanation_frameworks() -> Dict[str, Any]:
    """
    Surveys and specifies the mathematical foundations of post-hoc attribution frameworks
    tailored to small-N semiconductor regression.
    """
    methods = [
        {
            "name": "TreeSHAP",
            "type": "exact_local_attribution",
            "algorithm": "Tree-traversal Shapley computation (Lundberg et al., 2020)",
            "applicable_models": ["Random_Forest", "Gradient_Boosting"],
            "strengths": [
                "Exact polynomial-time computation without sampling approximations",
                "Satisfies efficiency axiom: sum of attributions exactly equals f(x) - E[f(X)]",
                "Supports pairwise SHAP interaction matrices"
            ],
            "role": "Primary explainer for tree ensembles in Section 5"
        },
        {
            "name": "KernelSHAP",
            "type": "model_agnostic_local_attribution",
            "algorithm": "Weighted linear surrogate regression over coalitional subsets",
            "applicable_models": ["Gaussian_Process_Matern", "Ridge_Regression", "Support_Vector_Regression_RBF"],
            "strengths": [
                "Agnostic to model architecture; seamlessly explains Gaussian Processes and SVR",
                "Consistent baseline expectation"
            ],
            "role": "Primary explainer for Bayesian GPR and kernel models"
        },
        {
            "name": "Permutation_Feature_Importance",
            "type": "global_importance",
            "algorithm": "Out-of-fold feature shuffling measuring Delta RMSE",
            "applicable_models": ["All shortlisted models"],
            "strengths": [
                "Directly reflects generalization metric degradation",
                "Non-parametric and robust on small-N validation splits"
            ],
            "role": "Validation metric degradation benchmark across folds"
        },
        {
            "name": "Partial_Dependence_PDP",
            "type": "marginal_response_surfaces",
            "algorithm": "Grid-based marginal expectation E_{X_{-j}}[f(x_j, X_{-j})]",
            "applicable_models": ["All continuous regressors"],
            "strengths": [
                "Visually traces non-linear saturation curves (e.g. gate accumulation plateaus)",
                "Forms the mathematical engine for the 2D Interpretable Regime Map"
            ],
            "role": "Engine for 2D/3D Regime Mapping in Sprint 5.c"
        }
    ]
    
    spec = {
        "title": "Post-Hoc Feature Attribution Specification for MoS2 Contacts",
        "methods": methods,
        "selected_primary_pair": {
            "local_attribution": "SHAP (TreeSHAP for Ensembles, KernelSHAP for GPR)",
            "global_response": "Partial Dependence Profiling (PDP)"
        }
    }
    
    EXPLAINABILITY_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(EXPLAINABILITY_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


def compute_prototype_permutation_importance(model_name: str = "Gradient_Boosting", df: Optional[pd.DataFrame] = None) -> Dict[str, float]:
    """Computes empirical permutation feature importance for a specified candidate model."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values
    
    model = instantiate_candidate_model(model_name)
    model.fit(X, y)
    
    r = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    
    importances = {
        col: round(float(mean_imp), 4)
        for col, mean_imp in zip(feature_cols, r.importances_mean)
    }
    return importances


if __name__ == "__main__":
    s = evaluate_post_hoc_explanation_frameworks()
    print("Post-hoc explanation methodology defined.")
    imp = compute_prototype_permutation_importance()
    print("Permutation importances for Gradient Boosting:")
    print(json.dumps(imp, indent=2))
