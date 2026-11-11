"""Tests for Source Evaluator and Accessibility Matrix."""

from src.data.source_evaluator import (
    load_accessibility_matrix,
    rank_sources_by_accessibility,
    get_export_formats_summary,
    get_primary_extraction_pipeline_recommendation
)


def test_load_accessibility_matrix():
    matrix = load_accessibility_matrix()
    assert "literature_indexes" in matrix
    assert "materials_databases" in matrix


def test_rank_sources():
    ranked_lit = rank_sources_by_accessibility("literature_indexes")
    assert len(ranked_lit) >= 5
    # Highest ranked should be OpenAlex or Crossref (public open APIs)
    top_source = ranked_lit[0][0]
    assert top_source in ["openalex", "crossref"]

    ranked_mat = rank_sources_by_accessibility("materials_databases")
    assert len(ranked_mat) >= 3


def test_export_formats_summary():
    formats = get_export_formats_summary()
    assert "openalex" in formats
    assert "JSON" in formats["openalex"]


def test_pipeline_recommendation():
    rec = get_primary_extraction_pipeline_recommendation()
    assert "literature_discovery" in rec
    assert "OpenAlex" in rec["literature_discovery"]
