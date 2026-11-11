"""
Regression Error Metrics Evaluator for Nanoscale Contacts (Sprint 3.b.1).
Implements order-of-magnitude metrics (RMSE/MAE in dex), geometric factor errors, and scale-invariant percentage errors.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np

METRICS_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "regression_error_metrics.json"


def compute_log_rmse(y_true_log: np.ndarray, y_pred_log: np.ndarray) -> float:
    """Computes Root Mean Squared Error on log10 target (units: dex)."""
    return float(np.sqrt(np.mean((y_true_log - y_pred_log) ** 2)))


def compute_log_mae(y_true_log: np.ndarray, y_pred_log: np.ndarray) -> float:
    """Computes Mean Absolute Error on log10 target (units: dex)."""
    return float(np.mean(np.abs(y_true_log - y_pred_log)))


def compute_geometric_factor_error(y_true_log: np.ndarray, y_pred_log: np.ndarray) -> float:
    """
    Computes the geometric multiplicative factor error:
    Factor = 10^(MAE(log10))
    e.g., MAE = 0.15 dex -> Factor = 10^0.15 = 1.41x (predictions within 41% on average).
    """
    mae = compute_log_mae(y_true_log, y_pred_log)
    return float(10.0 ** mae)


def compute_linear_medape(y_true_linear: np.ndarray, y_pred_linear: np.ndarray) -> float:
    """Computes Median Absolute Percentage Error (MedAPE) in linear space (percentage)."""
    ratios = np.abs(y_true_linear - y_pred_linear) / (np.abs(y_true_linear) + 1e-12)
    return float(np.median(ratios) * 100.0)


def evaluate_regression_metrics(y_true_log: np.ndarray, y_pred_log: np.ndarray) -> Dict[str, float]:
    """Computes comprehensive regression error metrics across logarithmic and linear spaces."""
    rmse_dex = compute_log_rmse(y_true_log, y_pred_log)
    mae_dex = compute_log_mae(y_true_log, y_pred_log)
    geom_factor = compute_geometric_factor_error(y_true_log, y_pred_log)
    
    y_true_lin = 10.0 ** y_true_log
    y_pred_lin = 10.0 ** y_pred_log
    medape_pct = compute_linear_medape(y_true_lin, y_pred_lin)
    
    # R2 on log10 target
    ss_tot = np.sum((y_true_log - np.mean(y_true_log)) ** 2)
    ss_res = np.sum((y_true_log - y_pred_log) ** 2)
    r2_log = float(1.0 - (ss_res / (ss_tot + 1e-12)))
    
    return {
        "rmse_log10_dex": round(rmse_dex, 4),
        "mae_log10_dex": round(mae_dex, 4),
        "geometric_factor_error": round(geom_factor, 3),
        "medape_linear_pct": round(medape_pct, 2),
        "r2_log10": round(r2_log, 4)
    }


def define_regression_error_metrics_spec() -> Dict[str, Any]:
    """Catalog of regression metrics and physical interpretation."""
    spec = {
        "title": "Regression Error Metrics Specification for MoS2 Contact Resistance",
        "metrics": [
            {
                "name": "RMSE_log10_dex",
                "unit": "dex (decades)",
                "formula": "sqrt(mean((log10(Rc_true) - log10(Rc_pred))^2))",
                "physical_meaning": "Penalizes large order-of-magnitude prediction errors; standard optimization loss."
            },
            {
                "name": "MAE_log10_dex",
                "unit": "dex (decades)",
                "formula": "mean(|log10(Rc_true) - log10(Rc_pred)|)",
                "physical_meaning": "Robust average decade discrepancy; immune to isolated outlier characterization noise."
            },
            {
                "name": "geometric_factor_error",
                "unit": "multiplicative factor (X-fold)",
                "formula": "10^(MAE_log10)",
                "physical_meaning": "Direct physical interpretability: factor of 1.4x means predictions are within 40% of measured values."
            },
            {
                "name": "medape_linear_pct",
                "unit": "%",
                "formula": "median(|Rc_true - Rc_pred| / Rc_true) * 100",
                "physical_meaning": "Scale-invariant median relative percentage error across linear resistance ranges."
            }
        ]
    }
    
    METRICS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    s = define_regression_error_metrics_spec()
    print("Regression metrics specification serialized.")
    # Example test
    y_t = np.array([2.5, 3.0, 4.0])
    y_p = np.array([2.6, 2.9, 4.2])
    print("Example metric computation:", evaluate_regression_metrics(y_t, y_p))
