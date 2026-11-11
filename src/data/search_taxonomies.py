"""
Search Taxonomy Builder and Query Generator.
Generates optimized boolean search strings and filters noise for literature databases.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

TAXONOMY_PATH = Path(__file__).resolve().parents[2] / "data" / "reference" / "search_taxonomies.json"


def load_search_taxonomies() -> Dict[str, Any]:
    """Loads search taxonomies and keyword clusters."""
    if not TAXONOMY_PATH.exists():
        raise FileNotFoundError(f"Taxonomy file not found at {TAXONOMY_PATH}")
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_boolean_query(target: str = "contact_resistance", include_exclusions: bool = True) -> str:
    """
    Constructs a calibrated boolean search query for literature indexes.
    Target options: 'contact_resistance', 'schottky_barrier', 'combined'.
    """
    tax = load_search_taxonomies()
    mat_clause = ' OR '.join([f'"{t}"' for t in tax["material_terms"][:4]])
    
    if target == "contact_resistance":
        metric_clause = ' OR '.join([f'"{t}"' for t in tax["contact_resistance_terms"][:4]])
    elif target == "schottky_barrier":
        metric_clause = ' OR '.join([f'"{t}"' for t in tax["schottky_barrier_terms"][:4]])
    else:  # combined
        metric_clause = ' OR '.join([f'"{t}"' for t in (tax["contact_resistance_terms"][:3] + tax["schottky_barrier_terms"][:3])])
    
    query = f"({mat_clause}) AND ({metric_clause})"
    
    if include_exclusions:
        not_clause = ' OR '.join([f'"{t}"' for t in tax["exclusion_terms"][:4]])
        query = f"{query} NOT ({not_clause})"
        
    return query


def validate_query_syntax(query: str) -> bool:
    """Verifies balanced quotes and parentheses in query string."""
    if query.count('"') % 2 != 0:
        return False
    stack = []
    for char in query:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0


def get_prebuilt_queries() -> Dict[str, str]:
    """Returns pre-tested query templates for specific APIs."""
    tax = load_search_taxonomies()
    return tax.get("query_templates", {})
