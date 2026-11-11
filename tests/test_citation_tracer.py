"""Tests for Citation Network Tracer."""

from src.data.citation_tracer import (
    save_citation_network,
    load_citation_network,
    get_backward_citations,
    get_forward_citations,
    compute_degree_centrality
)


def test_save_and_load_network():
    path = save_citation_network()
    assert path.exists()
    net = load_citation_network()
    assert len(net["nodes"]) >= 10
    assert len(net["edges"]) >= 10


def test_backward_citations():
    # allain_2015 should cite bardeen_1947, cowley_sze_1965, etc.
    cited = get_backward_citations("allain_2015")
    assert "bardeen_1947" in cited
    assert "cowley_sze_1965" in cited


def test_forward_citations():
    # allain_2015 should be cited by liu_2018, schulman_2018, shen_2021
    citing = get_forward_citations("allain_2015")
    assert "liu_2018" in citing
    assert "shen_2021" in citing


def test_degree_centrality():
    degree = compute_degree_centrality()
    # allain_2015 is a major meta-analysis hub
    assert degree["allain_2015"] >= 5
