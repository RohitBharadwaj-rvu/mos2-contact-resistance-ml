# Sprint 1.e.3: Investigate Missing Data Patterns

## Objective
Analyze missing value patterns across the experimental feature matrix, establish domain-informed physical default rules, and track provenance with explicit missingness indicator variables.

## Missingness Analysis & Domain Inferences
1. **Unstated Annealing Parameters:**
   - In literature, authors measuring as-fabricated devices do not explicitly report annealing temperature.
   - *Inference Rule:* Impute $T_{anneal} = 20^\circ\text{C}$ (room temperature) and ambient gas `"None"`, recording indicator `anneal_temp_was_missing = 1`.
2. **Unstated Vacuum Chamber Pressure:**
   - Evaporation chambers operate at typical base vacuum $1.0\times 10^{-6}\,\text{Torr}$, whereas glovebox transfers operate at $1.0\times 10^{-7}\,\text{Torr}$.
   - *Inference Rule:* Conditional imputation keyed to `deposition_method`.
3. **Carrier Density Reporting:**
   - High gate overdrive ON-state measurements typically operate at $n_{2D} \sim 1.0\times 10^{13}\,\text{cm}^{-2}$.
   - *Inference Rule:* Impute default $1.0\times 10^{13}\,\text{cm}^{-2}$ with `carrier_density_was_missing = 1`.
4. **Adhesion Layer:**
   - Defaults to `"None"` when single-metal or semimetal contact is specified.

## Deliverables
- `src/features/imputation_engine.py`: Missingness auditor and domain-inferred imputation engine with missing indicator columns.
- `tests/test_imputation_engine.py`: Unit test suite.
