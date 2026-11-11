"""
Systematic Hyperparameter Tuner for Small-N Grouped CV (Sprint 4.c.2).
Conducts leakage-free grid search over candidate architectures using GroupKFold(n_splits=5, groups=source_uid),
optimizing the composite multi-objective selection score.
"""

import json
from itertools import product
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.sample_complexity_analyzer import select_parsimonious_features
from src.validation.splitting_protocol import get_cv_splits
from src.validation.selection_criteria import evaluate_model_cv
from src.models.model_factory import instantiate_candidate_model

TUNED_HYPERPARAMS_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "tuned_hyperparameters_and_scores.json"


def get_tuning_grid(model_name: str) -> List[Dict[str, Any]]:
    """
    Returns list of parameter dictionary combinations for systematic search.
    """
    if model_name == "Ridge_Regression":
        alphas = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
        return [{"alpha": a} for a in alphas]

    elif model_name == "ElasticNet":
        alphas = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
        l1_ratios = [0.1, 0.3, 0.5, 0.7, 0.9]
        return [{"alpha": a, "l1_ratio": r} for a, r in product(alphas, l1_ratios)]

    elif model_name == "Gradient_Boosting":
        n_estimators = [20, 30, 50, 75]
        learning_rates = [0.01, 0.03, 0.05, 0.1]
        max_depths = [2, 3]
        subsamples = [0.7, 0.8, 1.0]
        return [
            {"n_estimators": n, "learning_rate": lr, "max_depth": d, "subsample": s}
            for n, lr, d, s in product(n_estimators, learning_rates, max_depths, subsamples)
        ]

    elif model_name == "Random_Forest":
        n_estimators = [30, 50, 80]
        max_depths = [2, 3]
        min_samples_splits = [3, 4, 6]
        min_samples_leafs = [2, 3]
        return [
            {"n_estimators": n, "max_depth": d, "min_samples_split": s, "min_samples_leaf": l}
            for n, d, s, l in product(n_estimators, max_depths, min_samples_splits, min_samples_leafs)
        ]

    elif model_name == "Gaussian_Process_Matern":
        length_scales = [0.5, 1.0, 2.0, 5.0]
        noise_levels = [0.01, 0.05, 0.1, 0.2]
        nus = [1.5, 2.5]
        return [
            {"length_scale": ls, "noise_level": nl, "nu": nu}
            for ls, nl, nu in product(length_scales, noise_levels, nus)
        ]

    elif model_name == "Support_Vector_Regression_RBF":
        Cs = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
        epsilons = [0.02, 0.05, 0.1, 0.2]
        gammas = ["scale", 0.05, 0.1, 0.2]
        return [
            {"C": c, "epsilon": ep, "gamma": g}
            for c, ep, g in product(Cs, epsilons, gammas)
        ]

    else:
        raise ValueError(f"No tuning grid defined for model: {model_name}")


def tune_single_architecture(
    model_name: str,
    X: pd.DataFrame,
    y: np.ndarray,
    splits: List[Tuple[np.ndarray, np.ndarray]]
) -> Dict[str, Any]:
    """
    Evaluates all parameter configurations for an architecture across splits,
    identifying the best parameters by composite_selection_score.
    """
    param_grid = get_tuning_grid(model_name)
    best_score = -float("inf")
    best_params = None
    best_metrics = None
    all_runs = []

    for params in param_grid:
        try:
            model = instantiate_candidate_model(model_name, **params)
            res = evaluate_model_cv(model, X, y, splits=splits)
            score = res["composite_selection_score"]
            all_runs.append({
                "params": params,
                "composite_score": score,
                "rmse": res["underlying_metrics"]["rmse_log10_dex"],
                "spearman_rho": res["underlying_metrics"]["spearman_rho"],
                "concordance_index": res["underlying_metrics"]["concordance_index"],
                "is_qualified": res["is_qualified_for_deployment"]
            })
            if score > best_score:
                best_score = score
                best_params = params
                best_metrics = res
        except Exception as e:
            continue

    # Compute parameter sensitivity: range of scores
    scores = [r["composite_score"] for r in all_runs]
    sensitivity = {
        "min_score": round(float(np.min(scores)), 4) if scores else None,
        "max_score": round(float(np.max(scores)), 4) if scores else None,
        "mean_score": round(float(np.mean(scores)), 4) if scores else None,
        "std_score": round(float(np.std(scores)), 4) if scores else None,
        "total_combinations_tested": len(all_runs)
    }

    return {
        "model_name": model_name,
        "best_params": best_params,
        "best_composite_score": best_score,
        "best_metrics": best_metrics,
        "sensitivity_analysis": sensitivity,
        "top_5_configurations": sorted(all_runs, key=lambda x: x["composite_score"], reverse=True)[:5]
    }


def run_systematic_hyperparameter_tuning(
    df: Optional[pd.DataFrame] = None,
    scheme: str = "grouped_5fold"
) -> Dict[str, Any]:
    """
    Runs systematic hyperparameter optimization across all shortlisted model architectures:
    1. Ridge_Regression
    2. ElasticNet
    3. Gradient_Boosting
    4. Random_Forest
    5. Gaussian_Process_Matern
    6. Support_Vector_Regression_RBF
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    splits = get_cv_splits(df, scheme=scheme)
    feature_cols = select_parsimonious_features(df, max_features=4)
    X = df[feature_cols].copy()
    y = df["log10_rc"].values

    models = [
        "Ridge_Regression",
        "ElasticNet",
        "Gradient_Boosting",
        "Random_Forest",
        "Gaussian_Process_Matern",
        "Support_Vector_Regression_RBF"
    ]

    tuning_results = {}
    for name in models:
        res = tune_single_architecture(name, X, y, splits)
        tuning_results[name] = res

    output = {
        "validation_scheme": scheme,
        "n_samples": len(df),
        "features_used": feature_cols,
        "models_tuned": tuning_results
    }

    TUNED_HYPERPARAMS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TUNED_HYPERPARAMS_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output


if __name__ == "__main__":
    results = run_systematic_hyperparameter_tuning()
    print("Systematic hyperparameter tuning complete.")
    for name, r in results["models_tuned"].items():
        print(f"[{name}] Best Score: {r['best_composite_score']} | Best Params: {r['best_params']}")
