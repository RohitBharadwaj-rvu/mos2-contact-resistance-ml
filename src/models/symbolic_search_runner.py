"""
Symbolic Regression Discovery Runner (Sprint 4.d.2).
Runs genetic programming searches across complexity levels using gplearn, converts expressions
via sympy to mathematical notation, evaluates paper-grouped CV performance, and maps the Pareto frontier.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import pandas as pd
import sympy as sp
from gplearn.genetic import SymbolicRegressor

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.models.symbolic_variable_selector import get_scaled_symbolic_dataset
from src.validation.splitting_protocol import get_cv_splits
from src.validation.regression_metrics import evaluate_regression_metrics
from src.validation.rank_trend_metrics import evaluate_rank_and_trend_metrics
from src.validation.selection_criteria import compute_composite_selection_score

PARETO_FRONTIER_JSON = Path(__file__).resolve().parents[2] / "data" / "processed" / "symbolic_regression_pareto_frontier.json"


def program_to_sympy_str(program_str: str) -> str:
    """
    Translates gplearn prefix function syntax into a standard algebraic sympy expression string.
    Replaces X0, X1, X2, X3 with x_sbh, x_n2d, x_vdw, x_hf.
    """
    s = str(program_str)
    # Define sympy symbols
    x_sbh, x_n2d, x_vdw, x_hf = sp.symbols("x_sbh x_n2d x_vdw x_hf")
    
    # Custom protected functions in sympy
    local_dict = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
        "div": lambda a, b: a / sp.Piecewise((b, sp.Abs(b) > 1e-4), (1e-4, True)),
        "inv": lambda a: 1 / sp.Piecewise((a, sp.Abs(a) > 1e-4), (1e-4, True)),
        "sqrt": lambda a: sp.sqrt(sp.Abs(a)),
        "log": lambda a: sp.log(sp.Abs(a) + 1e-4),
        "X0": x_sbh,
        "X1": x_n2d,
        "X2": x_vdw,
        "X3": x_hf
    }
    
    try:
        expr = sp.sympify(s, locals=local_dict)
        simplified = sp.simplify(expr)
        return str(simplified)
    except Exception:
        # Fallback string replace
        s = s.replace("X0", "x_sbh").replace("X1", "x_n2d").replace("X2", "x_vdw").replace("X3", "x_hf")
        return s


def evaluate_symbolic_expression_cv(
    sr_model_factory,
    X: pd.DataFrame,
    y: np.ndarray,
    splits: List[Tuple[np.ndarray, np.ndarray]]
) -> Dict[str, Any]:
    """
    Evaluates a symbolic regressor configuration strictly on out-of-fold predictions
    across paper-grouped folds.
    """
    oof_preds = np.zeros(len(y))
    
    for train_idx, val_idx in splits:
        X_train, y_train = X.iloc[train_idx], y[train_idx]
        X_val = X.iloc[val_idx]
        
        fold_model = sr_model_factory()
        fold_model.fit(X_train, y_train)
        oof_preds[val_idx] = fold_model.predict(X_val)
        
    composite = compute_composite_selection_score(y, oof_preds, feature_count=4)
    rmse = composite["underlying_metrics"]["rmse_log10_dex"]
    mae = float(np.mean(np.abs(y - oof_preds)))
    
    return {
        "oof_rmse": rmse,
        "oof_mae": round(mae, 4),
        "spearman_rho": composite["underlying_metrics"]["spearman_rho"],
        "concordance_index": composite["underlying_metrics"]["concordance_index"],
        "composite_score": composite["composite_selection_score"],
        "oof_predictions": [round(float(p), 4) for p in oof_preds]
    }


def run_symbolic_search_across_complexity_levels(
    df: Optional[pd.DataFrame] = None,
    scheme: str = "grouped_5fold",
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Runs genetic programming searches across 4 complexity tiers:
    1. Low Complexity (parsimony=0.05, max_length <= 7)
    2. Medium Complexity (parsimony=0.01, length ~ 8-12)
    3. High Complexity (parsimony=0.003, length ~ 13-18)
    4. Very High Complexity (parsimony=0.0005, length ~ 19-25)
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()

    X, y = get_scaled_symbolic_dataset(df)
    splits = get_cv_splits(df, scheme=scheme)

    complexity_configs = [
        {
            "tier": "tier_1_ultra_compact",
            "parsimony_coefficient": 0.05,
            "generations": 15,
            "population_size": 400,
            "init_depth": (1, 2)
        },
        {
            "tier": "tier_2_compact",
            "parsimony_coefficient": 0.01,
            "generations": 20,
            "population_size": 500,
            "init_depth": (2, 3)
        },
        {
            "tier": "tier_3_intermediate",
            "parsimony_coefficient": 0.003,
            "generations": 25,
            "population_size": 600,
            "init_depth": (2, 4)
        },
        {
            "tier": "tier_4_expressive",
            "parsimony_coefficient": 0.0005,
            "generations": 25,
            "population_size": 700,
            "init_depth": (3, 5)
        }
    ]

    discovered_equations = []

    for cfg in complexity_configs:
        parsimony = cfg["parsimony_coefficient"]
        gens = cfg["generations"]
        pop = cfg["population_size"]
        depth = cfg["init_depth"]

        def make_model():
            return SymbolicRegressor(
                population_size=pop,
                generations=gens,
                tournament_size=20,
                init_depth=depth,
                function_set=("add", "sub", "mul", "div", "inv"),
                metric="rmse",
                parsimony_coefficient=parsimony,
                random_state=random_state,
                verbose=0
            )

        # Fit full model to extract candidate mathematical program
        sr_full = make_model()
        sr_full.fit(X, y)

        raw_program = str(sr_full._program)
        clean_algebraic = program_to_sympy_str(raw_program)
        tree_length = sr_full._program.length_

        # In-sample performance
        in_sample_preds = sr_full.predict(X)
        in_sample_rmse = round(float(np.sqrt(np.mean((in_sample_preds - y) ** 2))), 4)

        # Out-of-fold paper-grouped cross validation
        cv_eval = evaluate_symbolic_expression_cv(make_model, X, y, splits)

        discovered_equations.append({
            "tier": cfg["tier"],
            "complexity_length": tree_length,
            "parsimony_coefficient": parsimony,
            "raw_program": raw_program,
            "clean_algebraic_expression": clean_algebraic,
            "in_sample_rmse": in_sample_rmse,
            "oof_rmse": cv_eval["oof_rmse"],
            "spearman_rho": cv_eval["spearman_rho"],
            "concordance_index": cv_eval["concordance_index"],
            "composite_score": cv_eval["composite_score"],
            "oof_predictions": cv_eval["oof_predictions"]
        })

    # Determine Pareto frontier (non-dominated points in complexity vs oof_rmse)
    # A point is Pareto optimal if no other point has both lower complexity and lower RMSE
    pareto_frontier = []
    sorted_by_length = sorted(discovered_equations, key=lambda x: (x["complexity_length"], x["oof_rmse"]))
    
    best_rmse_so_far = float("inf")
    for eq in sorted_by_length:
        if eq["oof_rmse"] < best_rmse_so_far:
            best_rmse_so_far = eq["oof_rmse"]
            pareto_frontier.append(eq)

    output = {
        "title": "Symbolic Regression Discovery Across Complexity Levels",
        "validation_scheme": scheme,
        "n_samples": len(df),
        "input_variables": list(X.columns),
        "discovered_equations": discovered_equations,
        "pareto_frontier": pareto_frontier
    }

    PARETO_FRONTIER_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(PARETO_FRONTIER_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output


if __name__ == "__main__":
    res = run_symbolic_search_across_complexity_levels()
    print("Symbolic search complete.")
    for eq in res["discovered_equations"]:
        print(f"[{eq['tier']}] Complexity: {eq['complexity_length']} | OOF RMSE: {eq['oof_rmse']} dex | Score: {eq['composite_score']}")
        print(f"  Expr: {eq['clean_algebraic_expression']}")
