# Sprint 1.a.1: Survey Scientific Literature Indexes

## Objective
Research and compile an exhaustive list of academic search engines, publisher portals, and citation indexes covering condensed matter physics, materials science, and nanoelectronics relevant to $\text{MoS}_2$ contact resistance ($R_c$) and Schottky barrier height ($\Phi_B$).

## Key Findings & Registry Architecture
1. **Critical Publisher Portals & Indexes:**
   - **IEEE Xplore:** Gold standard for nanoelectronics device characterization, TLM protocols, and conference breakthroughs (IEDM, EDL, TED).
   - **ACS Publications:** Key for nanoscale interface engineering, chemical treatments, and van der Waals contact physics (ACS Nano, Nano Letters).
   - **Nature / SpringerLink:** Premier source for high-performance sub-10 nm contact engineering (Nature Nano, Nature Electronics, Nature Materials).
   - **APS Physics:** Theoretical grounding on metal work functions, Fermi-level pinning (Bardeen vs Schottky-Mott limit), and DFT models (PRL, PRB, PRApplied).
   - **Wiley Online Library:** Seminal studies on phase-engineered contacts ($1\text{T}/\text{2H}$ transitions), bismuth/antimony contacts, and vdW gapless interfaces (Adv. Mater., Small).
   - **Elsevier ScienceDirect:** High-volume characterization data and contact annealing protocols (Solid-State Electronics, Applied Surface Science).
   - **IOP Science:** Specialized 2D crystal growth, interface states, and defect interactions (2D Materials).

2. **Open Access & Programmatic API Indexes:**
   - **OpenAlex:** Comprehensive CC0 bibliographic database with 250M+ works, direct DOI matching, and automated citation graphs.
   - **Crossref:** Direct verification of publisher metadata, open access licensing, and full-text links.
   - **Semantic Scholar:** Citation influence metrics and TLDR paper abstractions.
   - **arXiv cond-mat:** Fast access to preprints (mes-hall and mtrl-sci).

## Deliverables
- `data/reference/literature_indexes.json`: Structured registry of 11 surveyed academic engines and indexes.
- `src/data/literature_indexes.py`: Module providing programmatic access, priority filtering, and registry audits.
- `tests/test_literature_indexes.py`: Automated pytest test suite verifying registry integrity and completeness.
