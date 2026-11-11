"""
Master Model Benchmark Leaderboard Aggregator (Subheading 4.b Audit Enhancement).
Aggregates out-of-fold cross-validation scores across all baselines and default non-linear models into a unified competitive leaderboard.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from src.models.baseline_runner import BASELINE_RUNS_JSON, run_all_baseline_models_cv
from src.models.nonlinear_runner import NONLINEAR_RUNS_JSON, run_all_default_nonlinear_models_cv

LEADERBOARD_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "master_model_benchmark_leaderboard.json"


def compile_master_benchmark_leaderboard() -> Dict[str, Any]:
    """
    Compiles results from baseline runs and default non-linear runs,
    ranks models by composite selection score, and identifies top candidates.
    """
    if not BASELINE_RUNS_JSON.exists():
        run_all_baseline_models_cv()
    if not NONLINEAR_RUNS_JSON.exists():
        run_all_default_nonlinear_models_cv()
        
    with open(BASELINE_RUNS_JSON, "r", encoding="utf-8") as f:
        base_data = json.load(f)
    with open(NONLINEAR_RUNS_JSON, "r", encoding="utf-8") as f:
        nonlin_data = json.load(f)
        
    all_models = []
    
    # Process baselines
    for name, data in base_data["baseline_models"].items():
        all_models.append({
            "model_name": name,
            "category": "baseline_parametric" if "regression" in name or "least" in name else "naive_statistical",
            "composite_score": data["composite_selection_score"],
            "rmse_log10_dex": data["underlying_metrics"]["rmse_log10_dex"],
            "spearman_rho": data["underlying_metrics"]["spearman_rho"],
            "concordance_index": data["underlying_metrics"]["concordance_index"],
            "is_qualified": data["is_qualified_for_deployment"]
        })
        
    # Process non-linear models
    for name, data in nonlin_data["default_nonlinear_models"].items():
        all_models.append({
            "model_name": name,
            "category": "non_linear_ml",
            "composite_score": data["composite_selection_score"],
            "rmse_log10_dex": data["underlying_metrics"]["rmse_log10_dex"],
            "spearman_rho": data["underlying_metrics"]["spearman_rho"],
            "concordance_index": data["underlying_metrics"]["concordance_index"],
            "is_qualified": data["is_qualified_for_deployment"]
        })
        
    # Rank models by composite score descending
    ranked_models = sorted(all_models, key=lambda x: x["composite_score"], reverse=True)
    
    leaderboard = {
        "title": "Master MoS2 Contact Resistance ML Benchmark Leaderboard (Default Settings)",
        "validation_scheme": "GroupKFold(n_splits=5, groups=source_uid)",
        "n_models_evaluated": len(ranked_models),
        "leaderboard": ranked_models,
        "champion_model_pre_tuning": ranked_models[0]["model_name"],
        "top_score_pre_tuning": ranked_models[0]["composite_score"]
    }
    
    LEADERBOARD_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEADERBOARD_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=2)
        
    return leaderboard


if __name__ == "__main__":
    board = compile_master_benchmark_leaderboard()
    print("Master Leaderboard compiled successfully:")
    for rank, m in enumerate(board["leaderboard"], 1):
        print(f"  #{rank}: {m['model_name']} - Score: {m['composite_score']}, RMSE: {m['rmse_log10_dex']} dex, Qualified: {m['is_qualified']}")
