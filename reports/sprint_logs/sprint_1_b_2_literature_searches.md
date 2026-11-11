# Sprint 1.b.2: Execute Literature Searches

## Objective
Run finalized search queries across top-tier semiconductor literature engines and harvest a comprehensive raw corpus of experimental and review papers reporting contact resistance ($R_c$) and Schottky barrier height ($\Phi_B$) on $\text{MoS}_2$.

## Execution & Corpus Profile
1. **Literature Corpus Composition:**
   - 15 landmark peer-reviewed publications spanning 2011 to 2021.
   - High-impact venues: Nature, Nature Materials, Nature Electronics, Nature Nanotechnology, Nano Letters, Advanced Materials, IEEE IEDM, IEEE TED, Applied Physics Letters.
   - Contact technologies covered:
     - Semimetal contacts (Bi, Sb)
     - Conventional evaporated 3d & noble metals (Ti, Au, Sc, Ni, Pd, Cr)
     - Mechanically transferred van der Waals contacts (Ag, In)
     - Chemically engineered metallic phases ($1\text{T}\text{-}\text{MoS}_2$)
     - 2D interlayers (monolayer graphene)
     - Transition metal sub-oxides ($\text{MoO}_x$)
     - Annealed interfaces ($300^\circ\text{C}$ vacuum forming gas)
2. **Recorded Parameters:**
   - Paper metadata: unique ID, title, DOI, authors, venue, publication year, volume/pages.
   - Experimental parameters: contact metal, contact architecture, carrier injection type (n-type vs p-type), characterization metrology (TLM, Modified Richardson, sub-threshold activation, multi-terminal Hall), temperature (K), reported $R_c$ ($\Omega\cdot\mu\text{m}$), reported $\Phi_B$ (eV), and abstract context.

## Deliverables
- `data/raw/raw_literature_corpus.json`: Structured raw dataset of harvested papers.
- `src/data/literature_harvester.py`: Pipeline module for corpus extraction, persistence, and statistical validation.
- `tests/test_literature_harvester.py`: Test suite validating corpus integrity.
