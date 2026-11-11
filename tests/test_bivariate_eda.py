"""Tests for Bivariate Physical Relationships EDA."""

from src.visualization.bivariate_analysis import (
    compute_bivariate_correlations,
    generate_bivariate_plots,
    BIVARIATE_JSON_PATH,
    BIVARIATE_PNG_PATH
)
from src.features.feature_engineer import get_cleaned_and_engineered_dataset


def test_bivariate_correlations():
    df = get_cleaned_and_engineered_dataset()
    corrs = compute_bivariate_correlations(df)
    
    # Check key physical correlation: log10_rc vs schottky_barrier_height_ev
    key = "schottky_barrier_height_ev_vs_log10_rc"
    assert key in corrs
    # Must be positively correlated: higher barrier implies higher contact resistance!
    assert corrs[key]["pearson_r"] > 0.5
    assert corrs[key]["spearman_rho"] > 0.5


def test_generate_bivariate_plots():
    fig_path = generate_bivariate_plots()
    assert fig_path.exists()
    assert BIVARIATE_JSON_PATH.exists()
    assert BIVARIATE_PNG_PATH.exists()
