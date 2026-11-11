"""
Symbolic Regression Algorithm and Library Survey (Sprint 2.d.1).
Surveys genetic programming, sparse dictionary regression, and Pareto-optimal equation discovery frameworks for semiconductor contact physics.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

SYMBOLIC_SURVEY_JSON = Path(__file__).resolve().parents[2] / "data" / "reference" / "symbolic_regression_survey.json"


def survey_symbolic_regression_frameworks() -> Dict[str, Any]:
    """
    Evaluates available symbolic regression algorithms, libraries, and runtime requirements
    for closed-form equation discovery on small-N semiconductor datasets.
    """
    frameworks = [
        {
            "name": "gplearn",
            "algorithm": "Genetic Programming (Koza-style tree evolution)",
            "implementation_language": "Pure Python / scikit-learn API",
            "strengths": [
                "Native scikit-learn estimator interface (SymbolicRegressor)",
                "No external heavy dependencies or foreign binaries (Julia/C++)",
                "Tunable parsimony coefficients to penalize complex equation trees",
                "Direct support for custom mathematical operators (e.g., safe exp, safe log)"
            ],
            "limitations": [
                "Stochastic search can require multiple random restarts",
                "Does not enforce dimensional unit consistency automatically"
            ],
            "suitability_score": 9.5,
            "status": "PRIMARY_RECOMMENDED"
        },
        {
            "name": "PySR",
            "algorithm": "Multi-population Genetic Algorithm with Simulated Annealing and BFGS refinement",
            "implementation_language": "Python wrapper around Julia engine (SymbolicRegression.jl)",
            "strengths": [
                "Produces full Pareto frontier (Accuracy vs Complexity)",
                "Local gradient optimization of continuous constants (BFGS)",
                "Supports dimensional constraints"
            ],
            "limitations": [
                "Requires Julia runtime environment and native compilation",
                "Heavier deployment footprint and cold-start latency"
            ],
            "suitability_score": 8.0,
            "status": "SECONDARY_ALTERNATIVE"
        },
        {
            "name": "PySINDy",
            "algorithm": "Sparse Identification of Non-Linear Dynamics / Dictionary Regression",
            "implementation_language": "Python / NumPy / Scipy",
            "strengths": [
                "Deterministic convex optimization (Sequential Thresholded Least Squares)",
                "Strict linear combinations of predefined non-linear basis functions",
                "Extremely fast execution"
            ],
            "limitations": [
                "Requires pre-defining the exact basis dictionary (cannot synthesize novel functional compositions)",
                "Less suited for nested exponentials like exp(q*Phi / kT)"
            ],
            "suitability_score": 8.2,
            "status": "BENCHMARK_METHOD"
        }
    ]
    
    survey_data = {
        "title": "Symbolic Regression Algorithm Survey for MoS2 Contact Physics",
        "primary_objective": "Discover closed-form analytical formulas mapping work function, pinning factor, and gate density directly to contact resistance.",
        "frameworks": frameworks,
        "recommended_implementation_stack": "gplearn with custom physics operators and strict parsimony constraints"
    }
    
    SYMBOLIC_SURVEY_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(SYMBOLIC_SURVEY_JSON, "w", encoding="utf-8") as f:
        json.dump(survey_data, f, indent=2)
        
    return survey_data


if __name__ == "__main__":
    survey = survey_symbolic_regression_frameworks()
    print("Symbolic regression survey completed successfully:")
    print(json.dumps(survey, indent=2))
