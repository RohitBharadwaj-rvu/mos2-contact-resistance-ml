# Sprint 1.c.4: Audit Full Texts for Methodological Quality

## Objective
Read and evaluate full-text experimental methodology, deposition environments, vacuum chamber conditions, interface encapsulation, and metrology rigor across candidate papers, computing a multi-dimensional quality score for each source.

## Quality Scoring Dimensions (Total: 100 Points)
1. **Metrology Rigor (Max 30 pts):**
   - Gold-standard multi-length TLM ($R^2 > 0.99$) or 2D Richardson thermionic activation = 28-30 pts.
   - Sub-threshold slope or Hall bar = 25-27 pts.
   - Two-probe uncalibrated resistance = 12 pts (penalized).
2. **Vacuum & Deposition Control (Max 25 pts):**
   - Ultra-high vacuum (UHV $< 10^{-8}\,\text{Torr}$) or clean mechanical transfer = 23-25 pts.
   - High vacuum ($10^{-7} - 10^{-6}\,\text{Torr}$) = 18-22 pts.
3. **Encapsulation & Substrate Interface (Max 25 pts):**
   - Pristine hexagonal boron nitride (hBN) encapsulation or in-situ glovebox handling = 24-25 pts.
   - ALD oxide dielectric ($\text{Al}_2\text{O}_3$, $\text{HfO}_2$) = 20-22 pts.
   - Unpassivated $\text{SiO}_2$ ambient = 16-19 pts.
4. **Reporting Completeness (Max 20 pts):**
   - Full disclosure of channel dimensions ($W, L$), carrier density ($n_{2D}$), gate oxide thickness, and temperature series = 18-20 pts.

## Tier Stratification
- **Tier 1 (Exceptional, $\ge 85$ pts):** Shen 2021 (Nature), English 2016 (IEDM), Liu 2018 (Nature), Cui 2015 (Nano Letters), Wang 2019 (Nature Electronics), Li 2019 (Adv. Mater.), Liu 2020 (IEEE TED).
- **Tier 2 (High Quality, $70-84$ pts):** Allain 2015, Das 2013, Kappera 2014, Guimaraes 2016, McDonnell 2014, Kim 2017, Chwang 2014.
- **Tier 4 (Flagged / Low Quality, $< 70$ pts):** Radisavljevic 2011 (due to two-probe extraction limitations).

## Deliverables
- `data/processed/methodological_quality_audit.json` & `.csv`: Audited scores and qualitative notes.
- `src/data/methodology_auditor.py`: Auditing engine and tier classifier.
- `tests/test_methodology_auditor.py`: Test suite validating quality scoring distributions.
