"""
Unit tests for Out-of-Fold Explainability & Nuanced Decoupling Suite (Sprint 7.7).
"""

from pathlib import Path
import json
import pytest
import numpy as np
import pandas as pd

from src.interpretability.oof_explainability_engine import (
    compute_out_of_fold_shap_values,
    compute_out_of_fold_variance_decomposition,
    compute_observational_path_analysis,
    OOF_BENCHMARK_JSON,
    SHAP_FIGURE_PATH,
    DECOUPLING_FIGURE_PATH
)


def test_oof_shap_computation():
    res = compute_out_of_fold_shap_values(n_splits=3)
    assert "feature_rankings" in res
    assert len(res["feature_rankings"]) > 0
    top_feature = res["feature_rankings"][0]
    assert "feature" in top_feature
    assert "mean_abs_shap_dex" in top_feature
    assert top_feature["mean_abs_shap_dex"] > 0


def test_oof_variance_decomposition_bootstrap():
    res = compute_out_of_fold_variance_decomposition(n_splits=3, n_bootstrap=100)
    assert "intrinsic_share_pct" in res
    assert "extrinsic_share_pct" in res
    assert "unexplained_noise_pct" in res

    int_data = res["intrinsic_share_pct"]
    assert 0 <= int_data["ci_95_lower"] <= int_data["point_estimate"] <= int_data["ci_95_upper"] <= 100


def test_observational_path_analysis():
    res = compute_observational_path_analysis(n_bootstrap=100)
    assert "mediation_proportion_pct" in res
    assert "indirect_mediated_path" in res
    assert "direct_unmediated_path" in res
    assert "scientific_qualification" in res


def test_oof_benchmark_files_exist():
    assert OOF_BENCHMARK_JSON.exists()
    assert SHAP_FIGURE_PATH.exists()
    assert DECOUPLING_FIGURE_PATH.exists()

    with open(OOF_BENCHMARK_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "out_of_fold_shap_analysis" in data
    assert "out_of_fold_variance_decomposition" in data
    assert "observational_path_analysis" in data
