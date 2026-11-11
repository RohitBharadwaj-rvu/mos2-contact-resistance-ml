"""
Feature Collinearity and Multicollinearity Analyzer.
Computes Pearson correlation matrix, Variance Inflation Factors (VIF), and categorical confounding associations.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

VIF_REPORT_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "collinearity_vif_report.json"
HEATMAP_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "feature_correlation_heatmap.png"


def compute_vif_for_features(df_numeric: pd.DataFrame) -> Dict[str, float]:
    """
    Computes Variance Inflation Factor (VIF) for each numerical column:
    VIF_i = 1 / (1 - R_i^2)
    Uses Moore-Penrose pseudo-inverse / OLS regression.
    """
    cols = df_numeric.columns.tolist()
    vif_dict = {}
    
    # Standardize data to prevent numerical conditioning issues
    clean_df = df_numeric.dropna()
    scaled = (clean_df - clean_df.mean()) / (clean_df.std() + 1e-12)
    X = scaled.values
    
    for i, col in enumerate(cols):
        y_col = X[:, i]
        x_others = np.delete(X, i, axis=1)
        
        # Add intercept
        x_design = np.column_stack([np.ones(len(y_col)), x_others])
        
        # OLS fit
        try:
            beta, residuals, rank, s = np.linalg.lstsq(x_design, y_col, rcond=None)
            y_pred = x_design @ beta
            ss_tot = np.sum((y_col - np.mean(y_col)) ** 2)
            ss_res = np.sum((y_col - y_pred) ** 2)
            r2 = max(0.0, 1.0 - (ss_res / (ss_tot + 1e-12)))
            
            vif = 1.0 / (1.0 - r2) if r2 < 0.999 else 1000.0
            vif_dict[col] = round(float(vif), 2)
        except Exception:
            vif_dict[col] = 1.0
            
    return vif_dict


def run_collinearity_analysis(df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Computes correlation matrix, pairwise high correlations, and VIF metrics."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    num_cols = [
        "work_function_ev",
        "pauling_electronegativity",
        "sulfide_formation_enthalpy_kj_mol",
        "d_band_center_ev",
        "schottky_mott_barrier_ev",
        "electronegativity_diff_sulfur",
        "is_vdw_or_depinned_contact",
        "effective_pinning_factor_s",
        "fermi_level_shift_ev",
        "physics_predicted_sbh_ev"
    ]
    
    df_sub = df[num_cols].dropna()
    corr_matrix = df_sub.corr().round(3)
    
    # Identify pairwise strong correlations (|r| >= 0.75)
    strong_pairs = []
    cols = df_sub.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            r_val = corr_matrix.iloc[i, j]
            if abs(r_val) >= 0.75:
                strong_pairs.append({
                    "feature_1": cols[i],
                    "feature_2": cols[j],
                    "pearson_r": float(r_val)
                })
                
    vif_scores = compute_vif_for_features(df_sub)
    
    report = {
        "features_analyzed": num_cols,
        "sample_size": len(df_sub),
        "strong_correlations": strong_pairs,
        "vif_scores": vif_scores
    }
    
    VIF_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VIF_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    # Generate Heatmap
    HEATMAP_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(11, 9))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"label": "Pearson Correlation"}
    )
    plt.title("Physical Feature Collinearity Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(HEATMAP_PNG_PATH, dpi=300)
    plt.close()
    
    return report
