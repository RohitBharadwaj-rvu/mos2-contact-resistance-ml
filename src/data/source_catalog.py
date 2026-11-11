"""
Source Tracking Ledger and Catalog Management System.
Assigns canonical IDs, tracks provenance, and catalogs all mined publications, databases, and supplementary tables.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

LEDGER_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "source_tracking_ledger.json"
LEDGER_CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "source_tracking_ledger.csv"

INITIAL_CATALOG_SOURCES = [
    {
        "source_uid": "SRC-EXP-2021-SHEN",
        "title": "Ultralow contact resistance between semimetal and monolayer semiconductors",
        "doi": "10.1038/s41586-021-03472-9",
        "venue": "Nature",
        "year": 2021,
        "category": "Experimental_Device",
        "contact_system": "Bi/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_001_shen_2021"
    },
    {
        "source_uid": "SRC-REV-2015-ALLAIN",
        "title": "Electrical contacts to two-dimensional semiconductors",
        "doi": "10.1038/nmat4452",
        "venue": "Nature Materials",
        "year": 2015,
        "category": "Meta_Analysis",
        "contact_system": "Multi-Metal/MoS2",
        "reported_metrics": ["Rc", "SBH", "Fermi-pinning-factor"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_002_allain_2015"
    },
    {
        "source_uid": "SRC-EXP-2018-LIU",
        "title": "Approaching the Schottky-Mott limit in van der Waals metal-semiconductor junctions",
        "doi": "10.1038/s41586-018-0129-8",
        "venue": "Nature",
        "year": 2018,
        "category": "Experimental_Device",
        "contact_system": "vdW Transferred Ag,In,Au,Pt,Cu,Ti/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_003_liu_2018"
    },
    {
        "source_uid": "SRC-EXP-2014-KAPPERA",
        "title": "Phase-engineered low-resistance contacts to monolayer 2D semiconductors",
        "doi": "10.1038/nmat4080",
        "venue": "Nature Materials",
        "year": 2014,
        "category": "Experimental_Device",
        "contact_system": "1T-MoS2/2H-MoS2",
        "reported_metrics": ["Rc"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_004_kappera_2014"
    },
    {
        "source_uid": "SRC-EXP-2016-ENGLISH",
        "title": "Contact resistance benchmarks and scaling limits in monolayer MoS2 FETs",
        "doi": "10.1109/IEDM.2016.7838355",
        "venue": "IEEE IEDM",
        "year": 2016,
        "category": "Experimental_Device",
        "contact_system": "Ti/Au/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_005_english_2016"
    },
    {
        "source_uid": "SRC-EXP-2013-DAS",
        "title": "High performance pristine MoS2 field effect transistors with scandium contacts",
        "doi": "10.1021/nl303583v",
        "venue": "Nano Letters",
        "year": 2013,
        "category": "Experimental_Device",
        "contact_system": "Sc/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_006_das_2013"
    },
    {
        "source_uid": "SRC-EXP-2014-CHWANG",
        "title": "Investigation of metal contacts on MoS2 using transfer length method",
        "doi": "10.1063/1.4862491",
        "venue": "Applied Physics Letters",
        "year": 2014,
        "category": "Experimental_Device",
        "contact_system": "Ni/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_007_chwang_2014"
    },
    {
        "source_uid": "SRC-EXP-2011-RADISAV",
        "title": "Single-layer MoS2 transistors",
        "doi": "10.1038/nnano.2010.279",
        "venue": "Nature Nanotechnology",
        "year": 2011,
        "category": "Experimental_Device",
        "contact_system": "Au/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_008_radisavljevic_2011"
    },
    {
        "source_uid": "SRC-EXP-2015-CUI",
        "title": "Multi-terminal transport in pristine monolayer MoS2",
        "doi": "10.1021/nl504118s",
        "venue": "Nano Letters",
        "year": 2015,
        "category": "Experimental_Device",
        "contact_system": "Cr/Au/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_009_cui_2015"
    },
    {
        "source_uid": "SRC-EXP-2019-WANG",
        "title": "Low resistance van der Waals contacts to two-dimensional materials",
        "doi": "10.1038/s41928-019-0245-0",
        "venue": "Nature Electronics",
        "year": 2019,
        "category": "Experimental_Device",
        "contact_system": "In/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_010_wang_2019"
    },
    {
        "source_uid": "SRC-EXP-2019-LI",
        "title": "Antimony semimetal contacts for ultrathin 2D electronics",
        "doi": "10.1002/adma.201903106",
        "venue": "Advanced Materials",
        "year": 2019,
        "category": "Experimental_Device",
        "contact_system": "Sb/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_011_li_2019"
    },
    {
        "source_uid": "SRC-EXP-2016-GUIMARAES",
        "title": "Atomically thin Ohmic contacts to MoS2 through graphene interlayers",
        "doi": "10.1021/acs.nanolett.6b00676",
        "venue": "Nano Letters",
        "year": 2016,
        "category": "Experimental_Device",
        "contact_system": "Graphene/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_012_guimaraes_2016"
    },
    {
        "source_uid": "SRC-EXP-2014-MCDONNELL",
        "title": "Defect-dominated doping and contact resistance in MoS2",
        "doi": "10.1021/nn5004445",
        "venue": "ACS Nano",
        "year": 2014,
        "category": "Experimental_Device",
        "contact_system": "Pd/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_013_mcdonnell_2014"
    },
    {
        "source_uid": "SRC-EXP-2020-LIU",
        "title": "Thermal annealing and contact engineering of molybdenum disulfide FETs",
        "doi": "10.1109/TED.2020.2974152",
        "venue": "IEEE TED",
        "year": 2020,
        "category": "Experimental_Device",
        "contact_system": "Annealed Ti/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_014_liu_2020"
    },
    {
        "source_uid": "SRC-EXP-2017-KIM",
        "title": "Approaching Ohmic contact to MoS2 via molybdenum oxide interlayers",
        "doi": "10.1002/aelm.201700124",
        "venue": "Advanced Electronic Materials",
        "year": 2017,
        "category": "Experimental_Device",
        "contact_system": "MoOx/MoS2",
        "reported_metrics": ["Rc", "SBH"],
        "curation_status": "Mined",
        "raw_file_location": "data/raw/raw_literature_corpus.json#ref_015_kim_2017"
    },
    {
        "source_uid": "SRC-DB-2024-C2DB",
        "title": "Computational 2D Materials Database (C2DB)",
        "doi": "10.1088/2053-1583/aacfc1",
        "venue": "2D Materials",
        "year": 2024,
        "category": "Materials_Database",
        "contact_system": "2D Monolayers",
        "reported_metrics": ["Bandgap", "Work Function", "Effective Mass"],
        "curation_status": "Mined",
        "raw_file_location": "data/reference/material_property_databases.json#c2db"
    }
]


def save_source_catalog(catalog: List[Dict[str, Any]] = INITIAL_CATALOG_SOURCES) -> Dict[str, Path]:
    """Saves the tracking ledger in both JSON and CSV formats."""
    LEDGER_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        
    df = pd.DataFrame(catalog)
    # Serialize list fields for clean CSV export
    df_csv = df.copy()
    if "reported_metrics" in df_csv.columns:
        df_csv["reported_metrics"] = df_csv["reported_metrics"].apply(lambda x: ";".join(x) if isinstance(x, list) else x)
    df_csv.to_csv(LEDGER_CSV_PATH, index=False)
    
    return {"json": LEDGER_JSON_PATH, "csv": LEDGER_CSV_PATH}


def load_source_catalog() -> List[Dict[str, Any]]:
    """Loads the source tracking catalog."""
    if not LEDGER_JSON_PATH.exists():
        save_source_catalog()
    with open(LEDGER_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_source_by_uid(uid: str) -> Optional[Dict[str, Any]]:
    """Retrieves a source catalog record by its unique identifier."""
    catalog = load_source_catalog()
    for src in catalog:
        if src["source_uid"] == uid:
            return src
    return None


def find_sources_by_metal(metal_symbol: str) -> List[Dict[str, Any]]:
    """Finds all sources that tested or reviewed a specific metal contact."""
    catalog = load_source_catalog()
    results = []
    for src in catalog:
        system = src.get("contact_system", "")
        if metal_symbol.lower() in system.lower():
            results.append(src)
    return results


def find_sources_by_metric(metric: str) -> List[Dict[str, Any]]:
    """Finds all sources that report a specific metric (e.g. 'Rc' or 'SBH')."""
    catalog = load_source_catalog()
    results = []
    for src in catalog:
        metrics = src.get("reported_metrics", [])
        if any(metric.lower() in m.lower() for m in metrics):
            results.append(src)
    return results


def get_catalog_summary() -> Dict[str, Any]:
    """Generates ledger summary by category and curation status."""
    catalog = load_source_catalog()
    total = len(catalog)
    by_category = {}
    by_status = {}
    for item in catalog:
        cat = item.get("category", "Unknown")
        stat = item.get("curation_status", "Unknown")
        by_category[cat] = by_category.get(cat, 0) + 1
        by_status[stat] = by_status.get(stat, 0) + 1
        
    return {
        "total_cataloged_sources": total,
        "by_category": by_category,
        "by_status": by_status
    }
