"""Tests for Collinearity and VIF Analyzer."""

from src.features.collinearity_analyzer import (
    run_collinearity_analysis,
    compute_vif_for_features,
    VIF_REPORT_PATH,
    HEATMAP_PNG_PATH
)
from src.features.feature_engineer import get_cleaned_and_engineered_dataset


def test_collinearity_analysis():
    report = run_collinearity_analysis()
    assert VIF_REPORT_PATH.exists()
    assert HEATMAP_PNG_PATH.exists()
    assert "strong_correlations" in report
    assert "vif_scores" in report
    
    # Check that Schottky-Mott barrier is collinear with work function (r = 1.0)
    sm_wf_pair = next(
        (p for p in report["strong_correlations"]
         if ("work_function_ev" in [p["feature_1"], p["feature_2"]] and
             "schottky_mott_barrier_ev" in [p["feature_1"], p["feature_2"]])),
        None
    )
    assert sm_wf_pair is not None
    assert abs(sm_wf_pair["pearson_r"] - 1.0) < 1e-4


def test_vif_calculation():
    df = get_cleaned_and_engineered_dataset()
    sub = df[["work_function_ev", "pauling_electronegativity", "d_band_center_ev"]].dropna()
    vifs = compute_vif_for_features(sub)
    for col in sub.columns:
        assert col in vifs
        assert vifs[col] >= 1.0
