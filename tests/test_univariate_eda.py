"""Tests for Univariate EDA Module."""

from src.visualization.univariate_distributions import (
    compute_univariate_statistics,
    generate_univariate_distribution_plots,
    SUMMARY_JSON_PATH,
    FIGURE_PNG_PATH
)
from src.features.feature_engineer import get_cleaned_and_engineered_dataset


def test_compute_univariate_stats():
    df = get_cleaned_and_engineered_dataset()
    stats = compute_univariate_statistics(df)
    assert stats["dataset_sample_size"] >= 20
    assert "log10_rc" in stats["numerical_statistics"]
    assert "schottky_barrier_height_ev" in stats["numerical_statistics"]
    assert "contact_architecture" in stats["categorical_distributions"]


def test_generate_univariate_plots():
    fig_path = generate_univariate_distribution_plots()
    assert fig_path.exists()
    assert SUMMARY_JSON_PATH.exists()
    assert FIGURE_PNG_PATH.exists()
