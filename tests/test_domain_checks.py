from fraud_email.domain_checks import sender_domain,url_indicators

def test_sender():
    assert sender_domain("Example <foo@example.com>") == "example.com"

def test_domain_indicators():
    assert "ip_literal_url" in url_indicators("https://127.0.0.1/login")
    assert "url_userinfo" in url_indicators("https://user@bad.test/login")
