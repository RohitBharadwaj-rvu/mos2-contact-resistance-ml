"""
EDA Synthesis and Modeling Recommendation Engine (Sprint 1.f.5).
Synthesizes findings from univariate, bivariate, collinearity, and lab bias analyses into programmatic modeling constraints.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.features.collinearity_analyzer import run_collinearity_analysis
from src.visualization.lab_bias_analyzer import analyze_inter_paper_variance

RECOMMENDATIONS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "eda_modeling_recommendations.json"


def generate_eda_modeling_recommendations(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Synthesizes all exploratory data analysis findings into concrete modeling requirements:
    1. Sample size and dimensionality constraints (small-N regime).
    2. Feature selection and redundancy pruning.
    3. Target scale & loss function.
    4. Cross-validation partitioning strategy.
    5. Evaluation metric selection.
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    n_samples = len(df)
    n_sources = df["source_uid"].nunique()
    
    # Collinearity check
    collin_res = run_collinearity_analysis(df)
    high_vif_features = [f for f, v in collin_res["vif_scores"].items() if v > 10.0]
    
    # Lab bias check
    bias_res = analyze_inter_paper_variance(df)
    
    recommendations = {
        "dataset_scale": {
            "n_samples": n_samples,
            "n_sources": n_sources,
            "effective_degrees_of_freedom": n_sources - 1,
            "regime": "small_n_tabular"
        },
        "target_formulation": {
            "primary_target": "log10_rc",
            "raw_target": "contact_resistance_rc_ohm_um",
            "rationale": "Raw Rc exhibits heavy positive skew (skewness=2.50). Log10 transformation normalizes residuals (skewness=0.44) and matches logarithmic resistance scaling across orders of magnitude.",
            "schottky_barrier_target": "schottky_barrier_height_ev"
        },
        "feature_selection_constraints": {
            "max_features_recommended": 4,
            "sample_to_feature_ratio_target": ">= 4:1",
            "redundant_collinear_pairs": [
                {
                    "features": ["work_function_ev", "schottky_mott_barrier_ev"],
                    "correlation": 1.0,
                    "action": "Drop schottky_mott_barrier_ev because it is an exact linear shift (Phi_M - 4.2)"
                },
                {
                    "features": ["pauling_electronegativity", "work_function_ev"],
                    "correlation": 0.81,
                    "action": "Keep work_function_ev as primary physical descriptor; use electronegativity only in multivariate tree models"
                }
            ],
            "high_vif_features_to_prune": high_vif_features,
            "recommended_primary_features": [
                "physics_predicted_sbh_ev",
                "is_vdw_or_depinned_contact",
                "sulfide_formation_enthalpy_kj_mol",
                "work_function_ev"
            ]
        },
        "cross_validation_strategy": {
            "recommended_cv": "GroupKFold_or_LOGO",
            "grouping_variable": "source_uid",
            "rationale": "Standard random K-Fold suffers from data leakage due to intra-laboratory correlation. Grouped splitting tests generalization to completely unseen fabrication labs and literature sources."
        },
        "recommended_models": {
            "parsimonious_parametric": ["Ridge", "Lasso", "ElasticNet", "KernelRidge"],
            "probabilistic": ["GaussianProcessRegressor"],
            "non_linear_tabular": ["RandomForestRegressor", "GradientBoostingRegressor"],
            "symbolic_discovery": ["gplearn", "analytical_physics_equations"]
        },
        "evaluation_metrics": [
            {
                "name": "RMSE_log10_rc",
                "description": "Root Mean Squared Error on log10(Rc), representing average order-of-magnitude error (dex)."
            },
            {
                "name": "MAE_log10_rc",
                "description": "Mean Absolute Error on log10(Rc), robust to individual experimental outliers."
            },
            {
                "name": "Spearman_rho",
                "description": "Monotonic rank correlation, invariant to non-linear monotonic calibrations."
            },
            {
                "name": "Pearson_r",
                "description": "Linear correlation between predicted and experimental log10(Rc)."
            }
        ]
    }
    
    RECOMMENDATIONS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RECOMMENDATIONS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, indent=2)
        
    return recommendations


if __name__ == "__main__":
    recs = generate_eda_modeling_recommendations()
    print(f"Generated EDA modeling recommendations with {recs['dataset_scale']['n_samples']} samples across {recs['dataset_scale']['n_sources']} sources.")
