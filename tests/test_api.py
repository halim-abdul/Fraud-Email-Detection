from fastapi.testclient import TestClient
from api.app import app

def test_health():
    assert TestClient(app).get("/health").json()["status"]=="ok"

def test_triage():
    r=TestClient(app).post("/triage",json={"subject":"Lottery winner","body":"Send funds by wire transfer immediately. You won money."})
    assert r.status_code==200
    assert r.json()["review_required"] is True
