"""Tests for Search Taxonomy and Boolean Query Builder."""

from src.data.search_taxonomies import (
    load_search_taxonomies,
    build_boolean_query,
    validate_query_syntax,
    get_prebuilt_queries
)


def test_load_search_taxonomies():
    tax = load_search_taxonomies()
    assert "material_terms" in tax
    assert "contact_resistance_terms" in tax
    assert "schottky_barrier_terms" in tax
    assert "exclusion_terms" in tax


def test_build_boolean_query():
    q_cr = build_boolean_query(target="contact_resistance", include_exclusions=True)
    assert "MoS2" in q_cr
    assert "contact resistance" in q_cr
    assert "NOT" in q_cr
    assert validate_query_syntax(q_cr) is True

    q_sb = build_boolean_query(target="schottky_barrier", include_exclusions=False)
    assert "Schottky barrier" in q_sb
    assert "NOT" not in q_sb
    assert validate_query_syntax(q_sb) is True


def test_prebuilt_queries_syntax():
    queries = get_prebuilt_queries()
    for name, q in queries.items():
        if "all:" not in q:  # Standard boolean syntax
            assert validate_query_syntax(q) is True, f"Failed syntax on {name}"
