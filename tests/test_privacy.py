from fraud_email.privacy import redact

def test_redaction():
    assert "alice@example.org" not in redact("Email alice@example.org")
