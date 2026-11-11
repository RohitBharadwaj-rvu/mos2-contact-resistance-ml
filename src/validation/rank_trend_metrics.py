"""
Rank and Monotonic Trend Metrics Engine (Sprint 3.b.2).
Evaluates Spearman rank correlation, Kendall tau pairwise concordance, and ranking fidelity invariant to inter-laboratory offset shifts.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
from scipy import stats

RANK_METRICS_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "rank_trend_metrics_spec.json"


def compute_spearman_rho(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, float]:
    """Computes Spearman's rank correlation coefficient and p-value."""
    rho, pval = stats.spearmanr(y_true, y_pred)
    return float(rho), float(pval)


def compute_kendall_tau(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, float]:
    """Computes Kendall's tau-b rank correlation coefficient and p-value."""
    tau, pval = stats.kendalltau(y_true, y_pred)
    return float(tau), float(pval)


def compute_concordance_index(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes pairwise concordance index (fraction of pairs correctly ordered):
    C-index = concordant_pairs / total_pairs
    """
    n = len(y_true)
    concordant = 0
    total = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            if y_true[i] != y_true[j]:
                total += 1
                if (y_pred[i] - y_pred[j]) * (y_true[i] - y_true[j]) > 0:
                    concordant += 1
                elif y_pred[i] == y_pred[j]:
                    concordant += 0.5
                    
    return float(concordant / total) if total > 0 else 0.5


def evaluate_rank_and_trend_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    """Computes full suite of rank, monotonic trend, and concordance metrics."""
    rho, rho_p = compute_spearman_rho(y_true, y_pred)
    tau, tau_p = compute_kendall_tau(y_true, y_pred)
    c_index = compute_concordance_index(y_true, y_pred)
    pearson_r = float(np.corrcoef(y_true, y_pred)[0, 1]) if np.std(y_pred) > 1e-6 else 0.0
    
    return {
        "spearman_rho": round(rho, 4),
        "spearman_p_value": float(f"{rho_p:.2e}"),
        "kendall_tau": round(tau, 4),
        "kendall_p_value": float(f"{tau_p:.2e}"),
        "concordance_index": round(c_index, 4),
        "pearson_r": round(pearson_r, 4)
    }


def define_rank_trend_metrics_spec() -> Dict[str, Any]:
    """Catalog of ranking metrics and their utility for material screening."""
    spec = {
        "title": "Rank and Monotonic Trend Metrics Specification for MoS2 Contacts",
        "rationale": "Cross-lab systematic offsets shift absolute resistance values, but screening algorithms must accurately order contact strategies from best to worst.",
        "metrics": [
            {
                "name": "spearman_rho",
                "range": "[-1.0, +1.0]",
                "target": ">= 0.80",
                "meaning": "Monotonic ranking correlation across experimental devices."
            },
            {
                "name": "kendall_tau",
                "range": "[-1.0, +1.0]",
                "target": ">= 0.65",
                "meaning": "Net proportion of concordant pairwise metal comparisons."
            },
            {
                "name": "concordance_index",
                "range": "[0.0, 1.0]",
                "target": ">= 0.85",
                "meaning": "Probability that the model correctly predicts which of two randomly chosen contacts has lower Rc."
            }
        ]
    }
    
    RANK_METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(RANK_METRICS_JSON, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        
    return spec


if __name__ == "__main__":
    spec = define_rank_trend_metrics_spec()
    print("Rank metrics specification serialized.")
    y_t = np.array([2.5, 3.0, 3.8, 4.5])
    y_p = np.array([2.7, 3.1, 3.6, 4.9])
    print("Example rank metrics:", evaluate_rank_and_trend_metrics(y_t, y_p))
