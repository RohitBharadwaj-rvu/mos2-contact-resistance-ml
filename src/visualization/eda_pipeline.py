"""
Consolidated Exploratory Data Analysis (EDA) Pipeline.
Integrates univariate, bivariate, collinearity, lab bias, and modeling recommendation modules into a single reproducible workflow.
"""

from pathlib import Path
from typing import Dict, Any
import pandas as pd

from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.visualization.univariate_distributions import generate_univariate_distribution_plots
from src.visualization.bivariate_analysis import generate_bivariate_plots
from src.features.collinearity_analyzer import run_collinearity_analysis, HEATMAP_PNG_PATH
from src.visualization.lab_bias_analyzer import generate_variance_plots
from src.visualization.eda_synthesis import generate_eda_modeling_recommendations


def run_full_eda_suite(df: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Executes the complete EDA suite and produces all figures and statistical summaries:
    1. Univariate distributions and outlier detection
    2. Bivariate physics correlations (Schottky-Mott, Richardson thermionic trends)
    3. Multicollinearity matrix and VIF scoring
    4. Inter-paper variance and systematic lab bias
    5. Modeling synthesis recommendations
    """
    if df is None:
        df = get_cleaned_and_engineered_dataset()
        
    p_univariate = generate_univariate_distribution_plots(df)
    p_bivariate = generate_bivariate_plots(df)
    run_collinearity_analysis(df)
    p_collinear = HEATMAP_PNG_PATH
    p_variance = generate_variance_plots(df)
    recs = generate_eda_modeling_recommendations(df)
    
    return {
        "status": "success",
        "n_samples": len(df),
        "figures": {
            "univariate_distributions": str(p_univariate),
            "bivariate_relationships": str(p_bivariate),
            "collinearity_heatmap": str(p_collinear),
            "inter_paper_variance": str(p_variance)
        },
        "recommendations_summary": recs
    }


if __name__ == "__main__":
    res = run_full_eda_suite()
    print("Full EDA Suite Completed Successfully.")
    for fig_name, fig_path in res["figures"].items():
        print(f"  - {fig_name}: {fig_path}")
