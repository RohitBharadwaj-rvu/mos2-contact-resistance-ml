"""
Unit tests for web dashboard and API endpoints (Sprint 6.b.3).
"""

import json
import pytest
from src.dashboard.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_dashboard_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Contact Resistance & Semiconductor Physics Explorer" in response.data
    assert b"Device Parameters" in response.data


def test_dashboard_api_predict_bi(client):
    payload = {
        "metal": "Bi",
        "n2d": 1.8e13,
        "vdw": True
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_contact_resistance" in data
    assert data["predicted_contact_resistance"]["ml_model_ridge"]["rc_ohm_um"] < 150.0
    assert data["transport_regime"]["regime_id"] == "Regime_I_Quantum_Limited"


def test_dashboard_api_predict_ti(client):
    payload = {
        "metal": "Ti",
        "n2d": 5.0e12,
        "vdw": False
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["predicted_contact_resistance"]["ml_model_ridge"]["rc_ohm_um"] > 1000.0
