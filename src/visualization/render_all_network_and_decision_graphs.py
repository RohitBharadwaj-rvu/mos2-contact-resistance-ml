"""
Renders network graphs, citation graphs, and decision tree graphs as publication-quality PNG images.
"""

import os
os.environ["LOKY_MAX_CPU_COUNT"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"
import warnings
warnings.filterwarnings("ignore")

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.tree import plot_tree

from src.data.citation_tracer import load_citation_network
from src.pipeline.contact_predictor_pipeline import MoS2ContactPredictor
from src.physics.experimental_recommendations_engine import generate_laboratory_decision_flowchart

ROOT_DIR = Path(__file__).resolve().parents[2]
FIGURES_DIR = ROOT_DIR / "reports" / "figures"
ARTIFACT_FIGURES_DIR = Path("C:/Users/rohit/.gemini/antigravity/brain/40351c3a-3e08-415f-8617-d9dac2b5ded1/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def render_citation_network_graph():
    """Renders the citation network graph of MoS2 literature as a directed graph image."""
    net = load_citation_network()
    G = nx.DiGraph()

    type_colors = {
        "Theory Foundation": "#f59e0b",
        "Landmark Device": "#3b82f6",
        "Low-WF Experiment": "#06b6d4",
        "Phase Engineering": "#8b5cf6",
        "Meta-Analysis Review": "#ef4444",
        "Metrology": "#10b981",
        "TLM Benchmark": "#6366f1",
        "vdW Transferred": "#14b8a6",
        "vdW Experiment": "#10b981",
        "Semimetal Benchmark": "#ec4899",
        "Forward Benchmark": "#84cc16"
    }

    for n in net["nodes"]:
        G.add_node(n["id"], title=n["title"], year=n["year"], type=n["type"])

    for e in net["edges"]:
        G.add_edge(e["source"], e["target"], edge_type=e["type"])

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.9, iterations=60, seed=42)

    node_colors = [type_colors.get(G.nodes[n]["type"], "#94a3b8") for n in G.nodes]
    degrees = dict(G.degree())
    node_sizes = [max(800, degrees[n] * 400) for n in G.nodes]

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, edgecolors="black", linewidths=1.5)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=18, edge_color="#475569", width=1.8, alpha=0.75, connectionstyle="arc3,rad=0.1")

    # Labels with year
    labels = {n: f"{n.replace('_', ' ').title()}\n({G.nodes[n]['year']})" for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=8.5, font_family="sans-serif", font_weight="bold")

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label=k, markerfacecolor=v, markersize=10, markeredgecolor='black')
        for k, v in type_colors.items() if any(G.nodes[n]["type"] == k for n in G.nodes)
    ]
    plt.legend(handles=legend_elements, loc="upper left", title="Paper Type / Classification", framealpha=0.9, fontsize=8.5)

    plt.title("Citation Network & Bibliographic Tracing Graph of $\\text{MoS}_2$ Contact Literature\n(Directed Edges Represent Forward/Backward Influence & Theoretical Foundations)", fontsize=13, fontweight="bold", pad=15)
    plt.axis("off")
    plt.tight_layout()

    out_p = FIGURES_DIR / "citation_network_graph.png"
    plt.savefig(out_p, dpi=300)
    plt.savefig(ARTIFACT_FIGURES_DIR / "citation_network_graph.png", dpi=300)
    plt.close()
    print("Saved citation network graph to:", out_p)


def render_decision_tree_graph():
    """Visualizes an individual decision tree from the winning Random Forest model."""
    predictor = MoS2ContactPredictor()
    rf = predictor.rc_model
    tree_estimator = rf.estimators_[0]

    feature_names = [f.replace("_", " ").title() for f in predictor.task1_cols]

    plt.figure(figsize=(18, 9))
    plot_tree(
        tree_estimator,
        feature_names=feature_names,
        filled=True,
        rounded=True,
        fontsize=8,
        max_depth=3,
        precision=2
    )
    plt.title("Interpretable Physical Decision Tree Graph (Random Forest Sub-Estimator 0)\nMapping Exact Multi-Feature Split Rules to $\\log_{10}(R_c)$ Output Nodes", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()

    out_p = FIGURES_DIR / "random_forest_decision_tree_graph.png"
    plt.savefig(out_p, dpi=300)
    plt.savefig(ARTIFACT_FIGURES_DIR / "random_forest_decision_tree_graph.png", dpi=300)
    plt.close()
    print("Saved decision tree graph to:", out_p)


def render_experimental_decision_flowchart():
    """Renders the 4-step experimental fabrication decision flowchart as a directed graph image."""
    steps = generate_laboratory_decision_flowchart()
    G = nx.DiGraph()

    for i, s in enumerate(steps):
        G.add_node(i + 1, step=s["step"], action=s["action"], guideline=s["guideline"])
        if i > 0:
            G.add_edge(i, i + 1)

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")

    colors = ["#0284c7", "#0d9488", "#7c3aed", "#b45309"]

    for i, s in enumerate(steps):
        y_pos = 0.82 - i * 0.22
        box_text = f"{s['step'].upper()}\nAction: {s['action']}\n\nGuideline: {s['guideline']}"
        ax.text(
            0.5, y_pos,
            box_text,
            ha="center", va="center",
            fontsize=10.5,
            family="sans-serif",
            color="white",
            bbox=dict(boxstyle="round,pad=0.8", facecolor=colors[i], edgecolor="black", linewidth=1.5, alpha=0.92)
        )
        if i < len(steps) - 1:
            ax.annotate(
                "",
                xy=(0.5, y_pos - 0.08),
                xytext=(0.5, y_pos - 0.03),
                arrowprops=dict(facecolor="#334155", edgecolor="#334155", width=2.5, headwidth=10, shrink=0.05)
            )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.title("Laboratory Fabrication Decision Hierarchy Graph\nOptimal Experimental Flowchart for Sub-100 $\\Omega\\cdot\\mu\\text{m}$ $\\text{MoS}_2$ Contacts", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()

    out_p = FIGURES_DIR / "experimental_decision_flowchart_graph.png"
    plt.savefig(out_p, dpi=300)
    plt.savefig(ARTIFACT_FIGURES_DIR / "experimental_decision_flowchart_graph.png", dpi=300)
    plt.close()
    print("Saved decision flowchart graph to:", out_p)


if __name__ == "__main__":
    render_citation_network_graph()
    render_decision_tree_graph()
    render_experimental_decision_flowchart()
