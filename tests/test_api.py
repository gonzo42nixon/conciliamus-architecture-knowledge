import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["standard"] == "Google Open Knowledge Format (OKF v0.2)"
    assert data["status"] == "ready"

def test_search_concepts_all():
    res = client.get("/concepts")
    assert res.status_code == 200
    concepts = res.json()
    assert len(concepts) >= 20

def test_search_concepts_with_query():
    res = client.get("/concepts?q=dual-iflow")
    assert res.status_code == 200
    concepts = res.json()
    assert len(concepts) >= 1
    assert any("dual-iflow" in c["id"] for c in concepts)

def test_get_specific_concept():
    res = client.get("/concepts/architecture/dual-iflow-pattern")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "architecture/dual-iflow-pattern"
    assert data["frontmatter"]["type"] == "Architecture Concept"
    assert "IFL_MDM_BP_Batch_Receiver" in data["content"]

def test_get_adr_decision():
    res = client.get("/decisions/ADR-001")
    assert res.status_code == 200
    data = res.json()
    assert "adr-001" in data["adrId"].lower()
    assert data["status"] == "accepted"

def test_get_graph():
    res = client.get("/graph")
    assert res.status_code == 200
    data = res.json()
    assert data["nodesCount"] >= 20
    assert data["edgesCount"] >= 50

def test_verify_rule_compliant():
    res = client.post("/rules/verify", json={
        "proposedDesign": "Trennung von Ingest und Verarbeitung via Dual-iFlow und ProcessDirect",
        "context": "Architektur-Entwurf"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["compliant"] is True

def test_verify_rule_violation():
    res = client.post("/rules/verify", json={
        "proposedDesign": "Wir bauen einen monolithischen iFlow für beide Aufgaben",
        "context": "iFlow Architektur"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["compliant"] is False
    assert len(data["ruleViolations"]) > 0

def test_chat_query():
    res = client.post("/chat", json={
        "question": "Warum wurde ein Dual-iFlow Entwurfsmuster gewählt?"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["primaryConcept"] is not None
    assert "dual-iflow" in data["primaryConcept"]["id"]
    assert data["trustTier"] in ["VERIFIED", "ACCEPTED"]
