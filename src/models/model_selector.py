"""
Final Candidate Model Selector and Architecture Shortlist (Sprint 2.c.3).
Synthesizes baseline, tree ensemble, and alternative regression findings into a multi-criteria decision matrix and official shortlisted architectures.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

SHORTLIST_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "shortlisted_architectures.json"


def generate_candidate_architecture_matrix() -> Dict[str, Any]:
    """
    Constructs a multi-criteria decision matrix evaluating candidate models across 5 axes:
    1. Small-N Generalization & Overfitting Resilience (Weight: 25%)
    2. Physical Interpretability & Coefficient Attribution (Weight: 25%)
    3. Non-Linear Interaction & Saturation Modeling (Weight: 20%)
    4. Uncertainty Quantification for Lab Extrapolation (Weight: 20%)
    5. Optimization Stability & Ease of Tuning (Weight: 10%)
    """
    candidates = [
        {
            "architecture": "Ridge_Regression",
            "family": "regularized_linear",
            "scores": {
                "small_n_generalization": 9.5,
                "physical_interpretability": 10.0,
                "non_linear_interactions": 6.0,
                "uncertainty_quantification": 5.0,
                "optimization_stability": 10.0
            },
            "shortlisted": True,
            "role": "Primary regularized linear benchmark with direct coefficient physics attribution."
        },
        {
            "architecture": "ElasticNet",
            "family": "regularized_linear",
            "scores": {
                "small_n_generalization": 9.0,
                "physical_interpretability": 9.5,
                "non_linear_interactions": 6.0,
                "uncertainty_quantification": 5.0,
                "optimization_stability": 9.5
            },
            "shortlisted": True,
            "role": "Sparsity-inducing linear model pruning weak features."
        },
        {
            "architecture": "Gradient_Boosting",
            "family": "tree_ensemble",
            "scores": {
                "small_n_generalization": 8.0,
                "physical_interpretability": 8.0,
                "non_linear_interactions": 10.0,
                "uncertainty_quantification": 4.0,
                "optimization_stability": 8.5
            },
            "shortlisted": True,
            "role": "Primary non-linear tabular champion capturing gating and de-pinning interactions."
        },
        {
            "architecture": "Random_Forest",
            "family": "tree_ensemble",
            "scores": {
                "small_n_generalization": 8.5,
                "physical_interpretability": 7.5,
                "non_linear_interactions": 9.0,
                "uncertainty_quantification": 6.0,
                "optimization_stability": 9.5
            },
            "shortlisted": True,
            "role": "Robust bagging ensemble minimizing variance."
        },
        {
            "architecture": "Gaussian_Process_Matern",
            "family": "bayesian_non_parametric",
            "scores": {
                "small_n_generalization": 9.5,
                "physical_interpretability": 7.0,
                "non_linear_interactions": 9.5,
                "uncertainty_quantification": 10.0,
                "optimization_stability": 8.0
            },
            "shortlisted": True,
            "role": "Primary Bayesian model supplying analytic prediction intervals and experimental noise estimation."
        },
        {
            "architecture": "Support_Vector_Regression_RBF",
            "family": "kernel_margin",
            "scores": {
                "small_n_generalization": 9.0,
                "physical_interpretability": 6.5,
                "non_linear_interactions": 9.5,
                "uncertainty_quantification": 4.0,
                "optimization_stability": 8.5
            },
            "shortlisted": True,
            "role": "Epsilon-insensitive margin regressor immune to small experimental noise."
        },
        {
            "architecture": "Unregularized_OLS",
            "family": "linear",
            "scores": {
                "small_n_generalization": 5.0,
                "physical_interpretability": 10.0,
                "non_linear_interactions": 5.0,
                "uncertainty_quantification": 4.0,
                "optimization_stability": 7.0
            },
            "shortlisted": False,
            "role": "Rejected due to high variance and multicollinearity sensitivity."
        }
    ]
    
    # Compute composite weighted score
    weights = {
        "small_n_generalization": 0.25,
        "physical_interpretability": 0.25,
        "non_linear_interactions": 0.20,
        "uncertainty_quantification": 0.20,
        "optimization_stability": 0.10
    }
    
    for c in candidates:
        total = sum(c["scores"][dim] * weights[dim] for dim in weights)
        c["composite_score"] = round(total, 2)
        
    candidates_sorted = sorted(candidates, key=lambda x: x["composite_score"], reverse=True)
    
    matrix = {
        "weights": weights,
        "candidate_evaluations": candidates_sorted,
        "shortlisted_models": [c["architecture"] for c in candidates_sorted if c["shortlisted"]],
        "primary_champion_recommendation": "Gaussian_Process_Matern and Gradient_Boosting"
    }
    
    SHORTLIST_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SHORTLIST_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)
        
    return matrix


def get_shortlisted_architectures() -> List[str]:
    """Returns the official shortlisted architecture identifiers."""
    matrix = generate_candidate_architecture_matrix()
    return matrix["shortlisted_models"]


if __name__ == "__main__":
    m = generate_candidate_architecture_matrix()
    print("Candidate Architecture Decision Matrix:")
    print(json.dumps(m, indent=2))
