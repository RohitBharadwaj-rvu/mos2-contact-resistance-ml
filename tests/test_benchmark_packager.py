"""
Unit tests for benchmark dataset packaging (Sprint 6.b.1).
"""

import json
from pathlib import Path
import pandas as pd
import pytest

from src.data.benchmark_packager import (
    build_data_dictionary,
    build_source_provenance_registry,
    package_curated_benchmark_dataset,
    BENCHMARK_DIR,
    BENCHMARK_CSV_PATH,
    DATA_DICT_JSON_PATH,
    DATA_DICT_MD_PATH,
    PROVENANCE_JSON_PATH,
    PROVENANCE_MD_PATH,
    KAGGLE_METADATA_PATH,
    BENCHMARK_README_PATH
)


def test_build_data_dictionary():
    df = pd.DataFrame({
        "device_id": ["dev_0"],
        "contact_metal": ["Bi"],
        "contact_resistance_ohm_um": [123.0],
        "physics_predicted_sbh_ev": [0.05],
        "custom_feature": [1.23]
    })
    data_dict = build_data_dictionary(df)
    assert data_dict["total_records"] == 1
    assert data_dict["total_features"] == 5
    assert "contact_metal" in data_dict["columns"]
    assert data_dict["columns"]["contact_metal"]["type"] == "string"


def test_build_source_provenance_registry():
    prov = build_source_provenance_registry()
    assert len(prov) >= 5
    for p in prov:
        assert "source_uid" in p
        assert "citation" in p
        assert "doi" in p
        assert "extraction_method" in p


def test_package_curated_benchmark_dataset():
    res = package_curated_benchmark_dataset()
    assert res["status"] == "success"
    assert res["total_records"] == 20
    assert res["total_features"] == 44

    assert BENCHMARK_CSV_PATH.exists()
    assert DATA_DICT_JSON_PATH.exists()
    assert DATA_DICT_MD_PATH.exists()
    assert PROVENANCE_JSON_PATH.exists()
    assert PROVENANCE_MD_PATH.exists()
    assert KAGGLE_METADATA_PATH.exists()
    assert BENCHMARK_README_PATH.exists()

    with open(KAGGLE_METADATA_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["id"] == "rohitajitbharadwaj/mos2-contact-resistance-benchmark"
    assert meta["licenses"][0]["name"] == "CC-BY-4.0"
