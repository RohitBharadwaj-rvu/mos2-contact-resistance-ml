"""Tests for Literature Corpus Harvester."""

from src.data.literature_harvester import (
    load_raw_corpus,
    save_raw_corpus,
    get_corpus_statistics,
    FOUNDATIONAL_LITERATURE
)


def test_save_and_load_corpus():
    path = save_raw_corpus()
    assert path.exists()
    corpus = load_raw_corpus()
    assert len(corpus) == len(FOUNDATIONAL_LITERATURE)
    assert len(corpus) >= 15


def test_corpus_statistics():
    stats = get_corpus_statistics()
    assert stats["total_papers_harvested"] >= 15
    assert "Nature" in stats["unique_venues"]
    assert "Bi" in stats["unique_contact_metals"]
    assert "TLM" in stats["characterization_methods"]
    assert stats["year_range"][0] <= 2012
    assert stats["year_range"][1] >= 2021
