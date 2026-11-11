"""
Target Variable Transformation and Scaling Engine.
Evaluates skewness, applies logarithmic transformations for Rc, and provides inverse transforms for evaluation.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats

from src.data.tabular_extractor import load_tabular_dataset


def evaluate_target_distributions(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes statistical skewness, kurtosis, min, max, median, and log-transformed skewness
    for contact resistance and Schottky barrier height.
    """
    rc_clean = df["contact_resistance_rc_ohm_um"].dropna().values
    sbh_clean = df["schottky_barrier_height_ev"].dropna().values
    
    log_rc = np.log10(rc_clean)
    
    return {
        "rc_stats": {
            "count": len(rc_clean),
            "min": float(np.min(rc_clean)),
            "max": float(np.max(rc_clean)),
            "median": float(np.median(rc_clean)),
            "raw_skewness": round(float(stats.skew(rc_clean)), 3),
            "raw_kurtosis": round(float(stats.kurtosis(rc_clean)), 3),
            "log10_skewness": round(float(stats.skew(log_rc)), 3),
            "log10_kurtosis": round(float(stats.kurtosis(log_rc)), 3),
            "recommended_transform": "log10 or natural log (reduces skewness from >2 to near zero)"
        },
        "sbh_stats": {
            "count": len(sbh_clean),
            "min": float(np.min(sbh_clean)),
            "max": float(np.max(sbh_clean)),
            "median": float(np.median(sbh_clean)),
            "raw_skewness": round(float(stats.skew(sbh_clean)), 3),
            "raw_kurtosis": round(float(stats.kurtosis(sbh_clean)), 3),
            "recommended_transform": "linear (well-behaved within [0.0, 1.8] eV)"
        }
    }


def transform_target_rc(rc_values: np.ndarray, method: str = "log10") -> np.ndarray:
    """Transforms raw Rc values to log scale."""
    rc_arr = np.asarray(rc_values, dtype=float)
    if method == "log10":
        return np.log10(rc_arr)
    elif method == "ln":
        return np.log(rc_arr)
    else:
        return rc_arr


def inverse_transform_target_rc(transformed_values: np.ndarray, method: str = "log10") -> np.ndarray:
    """Inverts transformed values back to physical Ohm*um."""
    trans_arr = np.asarray(transformed_values, dtype=float)
    if method == "log10":
        return np.power(10.0, trans_arr)
    elif method == "ln":
        return np.exp(trans_arr)
    else:
        return trans_arr
