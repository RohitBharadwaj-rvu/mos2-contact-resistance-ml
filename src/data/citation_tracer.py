"""
Citation Graph and Bibliographic Tracing Engine.
Performs forward and backward citation network analysis on MoS2 contact literature.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Set

CITATION_GRAPH_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "citation_network.json"

# Curated citation linkages between landmark papers, foundational theory, and forward studies
CITATION_NETWORK = {
    "nodes": [
        {"id": "bardeen_1947", "title": "Surface states and rectifying properties of metal-semiconductor contacts", "year": 1947, "type": "Theory Foundation"},
        {"id": "cowley_sze_1965", "title": "Surface states and barrier height of metal-semiconductor systems", "year": 1965, "type": "Theory Foundation"},
        {"id": "radisavljevic_2011", "title": "Single-layer MoS2 transistors", "year": 2011, "type": "Landmark Device"},
        {"id": "das_2013", "title": "High performance pristine MoS2 FETs with scandium contacts", "year": 2013, "type": "Low-WF Experiment"},
        {"id": "kappera_2014", "title": "Phase-engineered low-resistance contacts to monolayer 2D semiconductors", "year": 2014, "type": "Phase Engineering"},
        {"id": "allain_2015", "title": "Electrical contacts to two-dimensional semiconductors", "year": 2015, "type": "Meta-Analysis Review"},
        {"id": "cui_2015", "title": "Multi-terminal transport in pristine monolayer MoS2", "year": 2015, "type": "Metrology"},
        {"id": "english_2016", "title": "Contact resistance benchmarks and scaling limits in monolayer MoS2 FETs", "year": 2016, "type": "TLM Benchmark"},
        {"id": "liu_2018", "title": "Approaching the Schottky-Mott limit in van der Waals metal-semiconductor junctions", "year": 2018, "type": "vdW Transferred"},
        {"id": "schulman_2018", "title": "Contact engineering for 2D materials and devices", "year": 2018, "type": "Meta-Analysis Review"},
        {"id": "wang_2019", "title": "Low resistance van der Waals contacts to two-dimensional materials", "year": 2019, "type": "vdW Experiment"},
        {"id": "shen_2021", "title": "Ultralow contact resistance between semimetal and monolayer semiconductors", "year": 2021, "type": "Semimetal Benchmark"},
        {"id": "zheng_2022", "title": "Universal contact engineering for two-dimensional materials", "year": 2022, "type": "Forward Benchmark"}
    ],
    "edges": [
        {"source": "allain_2015", "target": "bardeen_1947", "type": "theoretical_basis"},
        {"source": "allain_2015", "target": "cowley_sze_1965", "type": "theoretical_basis"},
        {"source": "allain_2015", "target": "radisavljevic_2011", "type": "data_synthesis"},
        {"source": "allain_2015", "target": "das_2013", "type": "data_synthesis"},
        {"source": "allain_2015", "target": "kappera_2014", "type": "data_synthesis"},
        {"source": "liu_2018", "target": "allain_2015", "type": "cites_benchmark"},
        {"source": "schulman_2018", "target": "allain_2015", "type": "cites_review"},
        {"source": "schulman_2018", "target": "english_2016", "type": "data_synthesis"},
        {"source": "shen_2021", "target": "allain_2015", "type": "benchmark_comparison"},
        {"source": "shen_2021", "target": "liu_2018", "type": "methodology_contrast"},
        {"source": "shen_2021", "target": "english_2016", "type": "benchmark_comparison"},
        {"source": "zheng_2022", "target": "shen_2021", "type": "forward_expansion"},
        {"source": "zheng_2022", "target": "liu_2018", "type": "forward_expansion"}
    ]
}


def save_citation_network(network: Dict[str, Any] = CITATION_NETWORK) -> Path:
    """Saves the citation network graph to disk."""
    CITATION_GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CITATION_GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(network, f, indent=2)
    return CITATION_GRAPH_PATH


def load_citation_network() -> Dict[str, Any]:
    """Loads the citation network graph."""
    if not CITATION_GRAPH_PATH.exists():
        save_citation_network()
    with open(CITATION_GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_backward_citations(paper_id: str) -> List[str]:
    """Returns list of paper IDs cited by paper_id (edges where paper_id is source)."""
    net = load_citation_network()
    return [edge["target"] for edge in net["edges"] if edge["source"] == paper_id]


def get_forward_citations(paper_id: str) -> List[str]:
    """Returns list of paper IDs that cite paper_id (edges where paper_id is target)."""
    net = load_citation_network()
    return [edge["source"] for edge in net["edges"] if edge["target"] == paper_id]


def compute_degree_centrality() -> Dict[str, int]:
    """Computes total degree centrality (in-degree + out-degree) for each node."""
    net = load_citation_network()
    degree = {node["id"]: 0 for node in net["nodes"]}
    for edge in net["edges"]:
        if edge["source"] in degree:
            degree[edge["source"]] += 1
        if edge["target"] in degree:
            degree[edge["target"]] += 1
    return dict(sorted(degree.items(), key=lambda x: x[1], reverse=True))
