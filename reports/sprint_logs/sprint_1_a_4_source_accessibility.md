# Sprint 1.a.4: Evaluate Source Accessibility and Coverage

## Objective
Assess the programmatic and manual accessibility, rate limits, licensing, and export tooling across all identified literature indexes and materials property databases to configure an optimal operational data extraction pipeline.

## Evaluation & Operational Architecture
1. **Source Accessibility Matrix:**
   - **OpenAlex (Score: 10/10):** Unrestricted CC0 REST API, complete forward/backward citation graphs, automated DOI resolution, and open-access PDF links. Selected as primary discovery engine.
   - **Crossref (Score: 9.5/10):** Essential for verifying official publisher metadata, license types, and author affiliations.
   - **C2DB (Score: 10/10):** Completely open access DFT data for monolayer $\text{MoS}_2$ and related 2D crystals.
   - **NIST & CRC (Score: 9.0-9.5/10):** Standard experimental baselines for work functions, atomic radii, and electronegativities.
   - **Publisher Portals (Nature, IEEE, ACS, Wiley - Score: 7.0-7.5/10):** Used for full-text experimental details, TLM plots, and supplementary information tables.

2. **Optimal Automated Extraction Strategy:**
   - Step 1: Literature searches executed via OpenAlex API + Crossref.
   - Step 2: Citation network traversal to discover all citing and cited papers around landmark benchmarks (Allain 2015, Shen 2021, Liu 2018, Schulman 2018).
   - Step 3: Direct tabular extraction from landmark review supplements and primary paper characterization sections.
   - Step 4: Automated enrichment with physical constants from C2DB, NIST, and CRC registries.

## Deliverables
- `data/reference/source_accessibility_matrix.json`: Detailed scoring matrix across all surveyed sources.
- `src/data/source_evaluator.py`: Module for ranking sources, assessing format capabilities, and defining pipeline workflows.
- `tests/test_source_evaluator.py`: Automated test suite for evaluator functionality.
