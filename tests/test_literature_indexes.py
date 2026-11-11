"""Unit tests for Literature Index Registry."""

import pytest
from src.data.literature_indexes import (
    load_literature_indexes,
    filter_indexes_by_priority,
    get_api_capable_indexes,
    summarize_index_registry
)


def test_load_literature_indexes():
    indexes = load_literature_indexes()
    assert len(indexes) >= 10
    ids = [idx["id"] for idx in indexes]
    assert "ieee_xplore" in ids
    assert "acs_pubs" in ids
    assert "nature_springer" in ids
    assert "openalex" in ids


def test_filter_indexes_by_priority():
    critical = filter_indexes_by_priority(min_priority="Critical")
    assert len(critical) > 0
    for idx in critical:
        assert idx["priority_rating"] == "Critical"


def test_get_api_capable_indexes():
    api_indexes = get_api_capable_indexes()
    assert len(api_indexes) >= 5
    for idx in api_indexes:
        assert idx["api_available"] is True


def test_summarize_index_registry():
    summary = summarize_index_registry()
    assert summary["total_indexes_surveyed"] >= 10
    assert summary["api_enabled_count"] > 0
    assert len(summary["venue_list"]) > 10
