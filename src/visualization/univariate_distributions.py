"""
Univariate Distribution Analysis and Visualization Pipeline.
Computes statistical moments, detects outliers, and generates distribution plots for input features and targets.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

SUMMARY_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "univariate_distribution_summary.json"
FIGURE_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "univariate_distributions.png"


def compute_univariate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes comprehensive univariate descriptive statistics and detects outliers."""
    num_cols = [
        "work_function_ev",
        "pauling_electronegativity",
        "sulfide_formation_enthalpy_kj_mol",
        "d_band_center_ev",
        "contact_resistance_rc_ohm_um",
        "log10_rc",
        "schottky_barrier_height_ev",
        "physics_predicted_sbh_ev"
    ]
    
    numerical_stats = {}
    for col in num_cols:
        if col in df.columns:
            series = df[col].dropna()
            q1 = float(np.percentile(series, 25))
            q3 = float(np.percentile(series, 75))
            iqr = q3 - q1
            lower_fence = q1 - 1.5 * iqr
            upper_fence = q3 + 1.5 * iqr
            outliers = series[(series < lower_fence) | (series > upper_fence)].tolist()
            
            numerical_stats[col] = {
                "mean": round(float(np.mean(series)), 3),
                "std": round(float(np.std(series)), 3),
                "median": round(float(np.median(series)), 3),
                "q1": round(q1, 3),
                "q3": round(q3, 3),
                "iqr": round(iqr, 3),
                "skewness": round(float(stats.skew(series)), 3),
                "kurtosis": round(float(stats.kurtosis(series)), 3),
                "outlier_count": len(outliers),
                "outliers": [round(float(o), 3) for o in outliers]
            }
            
    cat_cols = ["contact_metal", "contact_architecture", "deposition_method", "carrier_polarity"]
    categorical_counts = {}
    for col in cat_cols:
        if col in df.columns:
            categorical_counts[col] = df[col].value_counts().to_dict()
            
    return {
        "dataset_sample_size": len(df),
        "numerical_statistics": numerical_stats,
        "categorical_distributions": categorical_counts
    }


def generate_univariate_distribution_plots(df: Optional[pd.DataFrame] = None) -> Path:
    """Generates 4-panel univariate distribution figure."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    summary = compute_univariate_statistics(df)
    SUMMARY_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    FIGURE_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.set_theme(style="whitegrid")
    
    # Panel 1: log10(Rc) Target Distribution
    sns.histplot(df["log10_rc"].dropna(), kde=True, ax=axes[0, 0], color="royalblue", bins=8)
    axes[0, 0].set_title(r"Distribution of Target: $\log_{10}(R_c)$ [$\Omega\cdot\mu$m]", fontsize=13, fontweight="bold")
    axes[0, 0].set_xlabel(r"$\log_{10}(R_c)$")
    
    # Panel 2: Schottky Barrier Height Distribution
    sns.histplot(df["schottky_barrier_height_ev"].dropna(), kde=True, ax=axes[0, 1], color="crimson", bins=8)
    axes[0, 1].set_title(r"Distribution of Target: Schottky Barrier $\Phi_B$ [eV]", fontsize=13, fontweight="bold")
    axes[0, 1].set_xlabel(r"$\Phi_B$ (eV)")
    
    # Panel 3: Contact Metal Work Function
    sns.histplot(df["work_function_ev"].dropna(), kde=True, ax=axes[1, 0], color="forestgreen", bins=8)
    axes[1, 0].set_title(r"Input Feature: Metal Work Function $\Phi_M$ [eV]", fontsize=13, fontweight="bold")
    axes[1, 0].set_xlabel(r"$\Phi_M$ (eV)")
    
    # Panel 4: Contact Architecture Frequencies
    arch_counts = df["contact_architecture"].value_counts()
    sns.barplot(x=arch_counts.values, y=arch_counts.index, hue=arch_counts.index, legend=False, ax=axes[1, 1], palette="viridis")
    axes[1, 1].set_title("Categorical Class Distribution: Contact Architecture", fontsize=13, fontweight="bold")
    axes[1, 1].set_xlabel("Device Count")
    
    plt.tight_layout()
    plt.savefig(FIGURE_PNG_PATH, dpi=300)
    plt.close()
    
    return FIGURE_PNG_PATH
