"""
Bivariate Physical Relationship Analysis and Visualization Engine.
Inspects physical trends (Schottky-Mott slope, thermionic Rc vs SBH, gate scaling) and computes correlations.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from src.features.feature_engineer import get_cleaned_and_engineered_dataset

BIVARIATE_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "bivariate_correlation_summary.json"
BIVARIATE_PNG_PATH = Path(__file__).resolve().parents[2] / "reports" / "figures" / "bivariate_physical_relationships.png"


def compute_bivariate_correlations(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes Pearson and Spearman correlations between physical inputs and targets."""
    pairs = [
        ("work_function_ev", "schottky_barrier_height_ev"),
        ("schottky_barrier_height_ev", "log10_rc"),
        ("physics_predicted_sbh_ev", "log10_rc"),
        ("sulfide_formation_enthalpy_kj_mol", "log10_rc"),
        ("fermi_level_shift_ev", "log10_rc")
    ]
    
    results = {}
    for x_col, y_col in pairs:
        subset = df[[x_col, y_col]].dropna()
        if len(subset) >= 5:
            p_corr, p_pval = stats.pearsonr(subset[x_col], subset[y_col])
            s_corr, s_pval = stats.spearmanr(subset[x_col], subset[y_col])
            results[f"{x_col}_vs_{y_col}"] = {
                "n_samples": len(subset),
                "pearson_r": round(float(p_corr), 3),
                "pearson_p_value": float(f"{p_pval:.2e}"),
                "spearman_rho": round(float(s_corr), 3),
                "spearman_p_value": float(f"{s_pval:.2e}")
            }
            
    return results


def generate_bivariate_plots(df: Optional[pd.DataFrame] = None) -> Path:
    """Generates 4-panel bivariate physical relationships figure."""
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    corr_summary = compute_bivariate_correlations(df)
    BIVARIATE_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BIVARIATE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(corr_summary, f, indent=2)
        
    BIVARIATE_PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    sns.set_theme(style="whitegrid")
    
    # Panel 1: Schottky Barrier Height vs Metal Work Function (Schottky-Mott vs Bardeen)
    sns.scatterplot(
        data=df,
        x="work_function_ev",
        y="schottky_barrier_height_ev",
        hue="is_vdw_or_depinned_contact",
        palette={0.0: "crimson", 1.0: "royalblue"},
        s=120,
        ax=axes[0, 0]
    )
    # Reference lines: Schottky-Mott ideal (slope = 1, chi = 4.2 eV)
    wf_grid = np.linspace(3.4, 5.7, 50)
    sm_line = np.clip(wf_grid - 4.20, 0, 1.8)
    axes[0, 0].plot(wf_grid, sm_line, "b--", label="Schottky-Mott Limit (S = 1.0)")
    # Bardeen pinned line (S ~ 0.1)
    bardeen_line = 0.15 * (wf_grid - 4.20) + 0.85 * 0.22
    axes[0, 0].plot(wf_grid, bardeen_line, "r:", label="Bardeen Pinned Limit (S ~ 0.15)")
    axes[0, 0].set_title(r"Schottky Barrier $\Phi_B$ vs Metal Work Function $\Phi_M$", fontsize=13, fontweight="bold")
    axes[0, 0].set_xlabel(r"$\Phi_M$ (eV)")
    axes[0, 0].set_ylabel(r"$\Phi_B$ (eV)")
    axes[0, 0].legend(title="Contact Interface")
    
    # Panel 2: log10(Rc) vs Measured Schottky Barrier Height
    sns.regplot(
        data=df,
        x="schottky_barrier_height_ev",
        y="log10_rc",
        scatter_kws={"s": 90, "color": "darkorange"},
        line_kws={"color": "darkred", "linewidth": 2},
        ax=axes[0, 1]
    )
    axes[0, 1].set_title(r"Contact Resistance $\log_{10}(R_c)$ vs Barrier Height $\Phi_B$", fontsize=13, fontweight="bold")
    axes[0, 1].set_xlabel(r"$\Phi_B$ (eV)")
    axes[0, 1].set_ylabel(r"$\log_{10}(R_c)$ [$\Omega\cdot\mu$m]")
    
    # Panel 3: Physics-Predicted SBH vs Actual Measured SBH
    sns.scatterplot(
        data=df,
        x="physics_predicted_sbh_ev",
        y="schottky_barrier_height_ev",
        hue="contact_architecture",
        s=110,
        ax=axes[1, 0]
    )
    lims = [0, 1.6]
    axes[1, 0].plot(lims, lims, "k--", alpha=0.7, label="Ideal 1:1 Identity")
    axes[1, 0].set_title(r"Actual Measured $\Phi_B$ vs Physics Model Prediction", fontsize=13, fontweight="bold")
    axes[1, 0].set_xlabel(r"Physics-Predicted $\Phi_B$ (eV)")
    axes[1, 0].set_ylabel(r"Actual Measured $\Phi_B$ (eV)")
    axes[1, 0].legend(loc="upper left", fontsize=9)
    
    # Panel 4: log10(Rc) vs Sulfide Formation Enthalpy
    sns.scatterplot(
        data=df,
        x="sulfide_formation_enthalpy_kj_mol",
        y="log10_rc",
        hue="carrier_polarity",
        palette={"n_type": "navy", "p_type": "magenta"},
        s=110,
        ax=axes[1, 1]
    )
    axes[1, 1].set_title(r"$\log_{10}(R_c)$ vs Metal Sulfide Formation Enthalpy $\Delta H_f^\circ$", fontsize=13, fontweight="bold")
    axes[1, 1].set_xlabel(r"$\Delta H_f^\circ$ (kJ/mol per S atom)")
    axes[1, 1].set_ylabel(r"$\log_{10}(R_c)$ [$\Omega\cdot\mu$m]")
    
    plt.tight_layout()
    plt.savefig(BIVARIATE_PNG_PATH, dpi=300)
    plt.close()
    
    return BIVARIATE_PNG_PATH


if __name__ == "__main__":
    p = generate_bivariate_plots()
    print(f"Generated bivariate relationship plots at: {p}")

