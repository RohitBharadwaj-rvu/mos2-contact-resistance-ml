"""
Tests for Grouped Cross-Validation Scheme Evaluator (Sprint 3.a.2).
"""

from pathlib import Path
import json
import pytest
import numpy as np
from src.features.feature_engineer import get_cleaned_and_engineered_dataset
from src.validation.grouped_cv_evaluator import (
    get_paper_grouped_splits,
    get_leave_one_group_out_splits,
    compare_random_vs_grouped_cv,
    GROUPED_CV_JSON
)


def test_get_paper_grouped_splits():
    """Verify GroupKFold splits guarantee zero overlap in source_uid."""
    df = get_cleaned_and_engineered_dataset()
    splits = get_paper_grouped_splits(df, n_splits=5)
    
    assert len(splits) == 5
    for train_idx, val_idx in splits:
        train_sources = set(df.iloc[train_idx]["source_uid"])
        val_sources = set(df.iloc[val_idx]["source_uid"])
        # Strict zero-leakage requirement
        assert len(train_sources.intersection(val_sources)) == 0


def test_get_leave_one_group_out_splits():
    """Verify LOGO splits generate exactly one fold per literature publication."""
    df = get_cleaned_and_engineered_dataset()
    n_papers = df["source_uid"].nunique()
    splits = get_leave_one_group_out_splits(df)
    
    assert len(splits) == n_papers
    for train_idx, val_idx in splits:
        train_sources = set(df.iloc[train_idx]["source_uid"])
        val_sources = set(df.iloc[val_idx]["source_uid"])
        assert len(val_sources) == 1
        assert len(train_sources.intersection(val_sources)) == 0


def test_compare_random_vs_grouped_cv():
    """Verify comparative cross-validation evaluation runs and outputs optimism penalties."""
    res = compare_random_vs_grouped_cv()
    
    assert res["dataset_n_samples"] >= 20
    assert res["dataset_n_clusters"] >= 10
    
    models = res["models_evaluated"]
    assert "Ridge_Regression" in models
    assert "Gradient_Boosting" in models
    assert "Gaussian_Process_Matern" in models
    
    for m_name, m_res in models.items():
        assert "random_5fold" in m_res
        assert "grouped_5fold" in m_res
        assert "leave_one_group_out" in m_res
        assert "optimism_penalty_rmse" in m_res
        
    assert GROUPED_CV_JSON.exists()
