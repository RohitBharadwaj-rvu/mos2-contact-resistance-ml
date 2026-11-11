"""Tests for Abstract Screener."""

from src.data.abstract_screener import (
    screen_paper_title_and_abstract,
    execute_corpus_screening,
    get_screening_summary,
    SCREENING_RESULTS_PATH
)


def test_screen_corpus():
    results = execute_corpus_screening()
    assert len(results) >= 15
    assert SCREENING_RESULTS_PATH.exists()


def test_screening_summary():
    summary = get_screening_summary()
    assert summary["total_screened"] >= 15
    assert summary["passed_count"] > 10
    assert "PASSED_TITLE_ABSTRACT" in summary["decision_counts"]


def test_individual_paper_decisions():
    valid = {
        "title": "Contact engineering for MoS2 FETs with bismuth",
        "contact_metal": "Bi",
        "reported_rc_ohm_um": 123.0,
        "characterization_method": "TLM",
        "abstract": "TLM extraction shows ultralow Rc."
    }
    res_valid = screen_paper_title_and_abstract(valid)
    assert res_valid["decision"] == "PASSED_TITLE_ABSTRACT"

    off_topic = {
        "title": "MoS2 for hydrogen evolution reaction",
        "contact_metal": "Pt",
        "abstract": "Electrocatalysis water splitting."
    }
    res_off = screen_paper_title_and_abstract(off_topic)
    assert res_off["decision"] == "REJECTED_OFF_TOPIC"
