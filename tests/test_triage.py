from fraud_email.schemas import EmailInput
from fraud_email.triage import classify

def test_extortion():
    e = EmailInput(subject="We've got your dаta",body="We stole your data. Pay ETH to a wallet or your data will be sold on the deep web.")
    r = classify(e)
    assert r.label == "fraud"
    assert r.risk_score >= .65
    assert not r.reply_needed

def test_business_request():
    r = classify(EmailInput(subject="Meeting request",body="Please respond to my meeting question about Acme contracts.",company_context="Acme contracts"))
    assert r.relevant and r.reply_needed and r.review_required

def test_lottery():
    r = classify(EmailInput(subject="Lottery winner",body="You have won money! Send funds by wire transfer immediately."))
    assert r.label == "fraud"
    assert not r.reply_needed
