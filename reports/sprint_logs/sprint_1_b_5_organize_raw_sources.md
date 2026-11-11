# Sprint 1.b.5: Organize Raw Collected Sources

## Objective
Establish a formal tracking system, provenance registry, and canonical UID ledger to catalog all mined publication files, supplementary data documents, and materials database exports.

## Canonical Identification Scheme
- **UID Syntax:** `SRC-<TYPE>-<YEAR>-<KEYWORD>`
  - Types: `EXP` (Experimental device), `REV` (Review / Meta-analysis), `THEO` (Theory foundation), `DB` (Materials database).
  - Examples: `SRC-EXP-2021-SHEN`, `SRC-REV-2015-ALLAIN`, `SRC-DB-2024-C2DB`.
- **Recorded Provenance Attributes:**
  - Unique Identifier (`source_uid`)
  - Canonical Title, Authors, Journal Venue, Publication Year
  - Digital Object Identifier (DOI)
  - Specific Contact System (e.g. `Bi/MoS2`, `Sc/MoS2`, `1T-MoS2/2H-MoS2`)
  - Reported Electrical Metrics (`Rc`, `SBH`)
  - Curation Status (`Mined`, `Audited`, `Extracted`)
  - Relative Raw File Path & Fragment Pointer

## Deliverables
- `data/raw/source_tracking_ledger.json`: Master JSON source catalog.
- `data/raw/source_tracking_ledger.csv`: Exportable spreadsheet ledger.
- `src/data/source_catalog.py`: Python ledger management module.
- `tests/test_source_catalog.py`: Automated test suite verifying uniqueness and metadata integrity.
