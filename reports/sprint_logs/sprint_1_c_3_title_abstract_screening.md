# Sprint 1.c.3: Screen Titles and Abstracts

## Objective
Execute an initial high-throughput screening over the harvested raw corpus, evaluating titles and abstracts against materials keywords, contact performance targets, and noise exclusion rules.

## Screening Results & Analysis
1. **Screening Summary:**
   - Total publications evaluated: 15
   - Accepted (`PASSED_TITLE_ABSTRACT`): 13 papers focusing on experimental $\text{MoS}_2$ contact devices with rigorous TLM, Hall bar, or 2D thermionic extraction.
   - Flagged (`FLAGGED_ERROR_PRONE_METROLOGY`): 1 paper (`ref_008_radisavljevic_2011`) flagged for relying on two-probe extraction without channel resistance subtraction ($R_c \approx 8500\,\Omega\cdot\mu\text{m}$), earmarked for metrological calibration or quarantine.
   - Incomplete review metadata (`REJECTED_INCOMPLETE`): 1 meta-analysis review paper lacking single-device geometric parameters, retained solely as a citation hub rather than a direct data point row.

## Deliverables
- `data/processed/title_abstract_screening_results.json`: Full screening registry detailing decision outcomes, passed rules, and rejection/flag tags.
- `src/data/abstract_screener.py`: High-throughput screening engine.
- `tests/test_abstract_screener.py`: Unit test suite.
