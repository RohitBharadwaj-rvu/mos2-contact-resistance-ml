"""Tests for Source Tracking Ledger and Catalog."""

from src.data.source_catalog import (
    save_source_catalog,
    load_source_catalog,
    find_source_by_uid,
    get_catalog_summary,
    INITIAL_CATALOG_SOURCES
)


def test_save_and_load_catalog():
    paths = save_source_catalog()
    assert paths["json"].exists()
    assert paths["csv"].exists()

    catalog = load_source_catalog()
    assert len(catalog) == len(INITIAL_CATALOG_SOURCES)
    assert len(catalog) >= 15


def test_find_source_by_uid():
    src = find_source_by_uid("SRC-EXP-2021-SHEN")
    assert src is not None
    assert src["venue"] == "Nature"
    assert "Bi/MoS2" in src["contact_system"]

    not_found = find_source_by_uid("NON_EXISTENT_UID")
    assert not_found is None


def test_find_by_metal_and_metric():
    from src.data.source_catalog import find_sources_by_metal, find_sources_by_metric
    bi_sources = find_sources_by_metal("Bi")
    assert len(bi_sources) >= 1
    assert bi_sources[0]["source_uid"] == "SRC-EXP-2021-SHEN"

    rc_sources = find_sources_by_metric("Rc")
    assert len(rc_sources) >= 10


def test_unique_uids():
    catalog = load_source_catalog()
    uids = [s["source_uid"] for s in catalog]
    assert len(uids) == len(set(uids)), "Source UIDs must be unique"


def test_catalog_summary():
    summary = get_catalog_summary()
    assert summary["total_cataloged_sources"] >= 15
    assert "Experimental_Device" in summary["by_category"]
