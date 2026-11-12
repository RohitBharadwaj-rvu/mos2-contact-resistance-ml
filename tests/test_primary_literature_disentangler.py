"""
Unit tests for Primary Literature Disentangler & Corpus Expansion (Sprint 7.1).
"""

from pathlib import Path
import pytest
import pandas as pd

from src.data.primary_literature_disentangler import (
    build_primary_experimental_corpus,
    build_secondary_review_dataset,
    run_primary_disentanglement,
    PRIMARY_CSV_PATH,
    SECONDARY_REVIEW_CSV_PATH,
    EXPANDED_LEDGER_CSV_PATH
)


def test_build_primary_experimental_corpus():
    df = build_primary_experimental_corpus()
    assert len(df) >= 25
    assert df["source_uid"].nunique() >= 15
    # Strict guarantee: NO review-derived sources in primary benchmark
    assert "SRC-REV-2015-ALLAIN" not in df["source_uid"].values
    assert (df["is_primary_experimental"] == True).all()

    # Verify essential physical fields are present and valid
    assert (df["work_function_ev"] > 3.0).all()
    assert (df["contact_resistance_rc_ohm_um"] > 0).all()
    assert (df["log10_rc"] > 0).all()
    assert (df["layer_count"] >= 1).all()


def test_build_secondary_review_dataset():
    df_rev = build_secondary_review_dataset()
    assert len(df_rev) == 4
    assert (df_rev["is_primary_experimental"] == False).all()
    assert "SRC-REV-2015-ALLAIN" in df_rev["source_uid"].values
    assert "compilation_table_reference" in df_rev.columns


def test_run_primary_disentanglement():
    res = run_primary_disentanglement()
    assert res["status"] == "success"
    assert res["primary_records_count"] >= 25
    assert res["primary_independent_sources"] >= 15

    assert PRIMARY_CSV_PATH.exists()
    assert SECONDARY_REVIEW_CSV_PATH.exists()
    assert EXPANDED_LEDGER_CSV_PATH.exists()

    df_p = pd.read_csv(PRIMARY_CSV_PATH)
    assert len(df_p) == res["primary_records_count"]
    assert "SRC-REV-2015-ALLAIN" not in df_p["source_uid"].values
