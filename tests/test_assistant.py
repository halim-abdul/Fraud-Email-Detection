from fastapi.testclient import TestClient
from api.app import app
from fraud_email.schemas import EmailInput
from fraud_email.assistant import summarise_email


def test_default_is_offline(monkeypatch):
    monkeypatch.delenv("FRAUD_ENABLE_EXTERNAL_LLM", raising=False)
    r = summarise_email(EmailInput(subject="Meeting request", body="Please respond to our meeting question."))
    assert r["mode"] == "offline_rules"
    assert r["review_required"] is True
    assert 1 <= len(r["bullets"]) <= 4


def test_threat_never_forwarded_even_with_llm_opt_in(monkeypatch):
    monkeypatch.setenv("FRAUD_ENABLE_EXTERNAL_LLM", "1")
    monkeypatch.setenv("FRAUD_LLM_PRIVACY_APPROVED", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key-for-tests")
    monkeypatch.setenv("FRAUD_LLM_MODEL", "fake-model-for-tests")
    email = EmailInput(subject="Your data", body="We stole your data. Pay ETH or your data will be sold.")
    r = summarise_email(email)
    assert r["mode"] == "offline_rules"
    assert r["label"] == "fraud"


def test_summary_api_and_chat_endpoint():
    c = TestClient(app)
    msg = {"message_id": "synthetic-1", "subject": "Meeting", "body": "Please review the agenda"}
    r = c.post("/assistant/summarize", json=msg)
    assert r.status_code == 200
    assert r.json()["mode"] == "offline_rules"
    chat = c.post("/assistant/chat", json={"email": msg, "question": "Summarize this email"})
    assert chat.status_code == 200
    assert chat.json()["action_executed"] is False
