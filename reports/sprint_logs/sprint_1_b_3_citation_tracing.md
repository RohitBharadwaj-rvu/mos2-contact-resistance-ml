# Sprint 1.b.3: Perform Citation Tracing

## Objective
Trace forward citations and backward bibliographies of foundational and landmark papers to construct a directed citation network, identify central bibliographic hubs, and capture contact characterization papers missed by keyword searches.

## Network Architecture & Insights
1. **Network Centrality:**
   - **Allain et al. (Nature Materials 2015):** Central meta-analysis hub (highest degree centrality = 6), connecting fundamental semiconductor contact theories (Bardeen 1947, Cowley & Sze 1965) to modern 2D device demonstrations (Radisavljevic 2011, Das 2013, Kappera 2014).
   - **Liu et al. (Nature 2018):** Pivotal bridge between conventional evaporated contacts and van der Waals transferred pristine contacts.
   - **Shen et al. (Nature 2021):** Landmark forward nexus that cites previous TLM benchmarks (English 2016, Allain 2015) while introducing semimetallic Bi/Sb contacts.
2. **Discovered Studies Captured via Tracing:**
   - Forward citations mapped through Zheng et al. 2022 and Wang et al. 2019, revealing Indium and Antimony transferred contact datasets.

## Deliverables
- `data/reference/citation_network.json`: Directed graph containing nodes and citation edges.
- `src/data/citation_tracer.py`: Python module providing backward/forward traversal and degree centrality metrics.
- `tests/test_citation_tracer.py`: Test suite validating citation linkages and graph queries.
