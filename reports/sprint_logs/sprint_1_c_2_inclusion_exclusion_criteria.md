# Sprint 1.c.2: Define Inclusion and Exclusion Criteria

## Objective
Establish a formal, reproducible multi-tier criteria checklist to screen and filter candidate literature records and experimental databases, guaranteeing high data fidelity for machine learning.

## Criteria Rules Matrix
1. **Inclusion Requirements (All Mandatory):**
   - `INC-01`: Target material must be $\text{MoS}_2$ (monolayer, few-layer, or bulk single crystal).
   - `INC-02`: Explicit identification of contact electrode material (metal, semimetal, 1T phase, or vdW interlayer).
   - `INC-03`: Quantitative reporting of $R_c$ (width-normalized in $\Omega\cdot\mu\text{m}$ or specific $\Omega\cdot\text{cm}^2$) or $\Phi_B$ (in eV).
   - `INC-04`: Valid metrology (TLM, multi-terminal Hall bar, modified Richardson activation, or XPS band bending).
   - `INC-05`: Device geometry disclosure sufficient to audit normalizations.
2. **Exclusion Triggers (Immediate Rejection/Quarantine):**
   - `EXC-01`: Pure simulation/theory lacking experimental device transport verification.
   - `EXC-02`: Two-probe extraction without channel resistance decoupling.
   - `EXC-03`: Off-topic domain (photocatalytic water splitting, solid lubricants, battery anodes).
   - `EXC-04`: Unphysical metrics ($R_c \le 0$ or $\Phi_B > 2.0\,\text{eV}$ exceeding bandgap).
   - `EXC-05`: Ambiguous or unspecified contact electrode material.

## Deliverables
- `data/reference/inclusion_exclusion_criteria.json`: Machine-readable criteria checklist.
- `src/data/quality_filter.py`: Automated rule evaluator returning pass/fail status and specific rejection codes.
- `tests/test_quality_filter.py`: Unit tests validating criteria enforcement across valid and edge-case records.
