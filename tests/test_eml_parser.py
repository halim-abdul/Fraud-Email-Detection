from fraud_email.email_parser import parse_eml

def test_parse():
    mail = parse_eml(b"From: alice@example.org\\nTo: bob@example.org\\nSubject: Hello\\nContent-Type: text/plain; charset=utf-8\\n\\nPlease review this.")
    assert mail.subject == "Hello"
    assert mail.sender == "alice@example.org"
