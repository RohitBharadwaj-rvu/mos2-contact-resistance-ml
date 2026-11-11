"""Tests for Target Variable Transformation."""

import numpy as np
from src.features.target_transformer import (
    evaluate_target_distributions,
    transform_target_rc,
    inverse_transform_target_rc
)
from src.data.tabular_extractor import load_tabular_dataset


def test_evaluate_target_distributions():
    df = load_tabular_dataset()
    dist = evaluate_target_distributions(df)
    assert "rc_stats" in dist
    assert "sbh_stats" in dist
    
    # Raw Rc is strongly right-skewed (> 2.0)
    assert dist["rc_stats"]["raw_skewness"] > 1.5
    
    # Log-transformed Rc skewness is dramatically reduced (close to 0, < 1.0)
    assert abs(dist["rc_stats"]["log10_skewness"]) < 1.0


def test_invertibility():
    orig = np.array([123.0, 740.0, 3200.0, 65000.0])
    
    # log10
    log_vals = transform_target_rc(orig, "log10")
    inv_vals = inverse_transform_target_rc(log_vals, "log10")
    np.testing.assert_allclose(orig, inv_vals, rtol=1e-5)

    # natural log
    ln_vals = transform_target_rc(orig, "ln")
    inv_ln = inverse_transform_target_rc(ln_vals, "ln")
    np.testing.assert_allclose(orig, inv_ln, rtol=1e-5)
