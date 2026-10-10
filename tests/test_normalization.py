from fraud_email.normalization import normalize
from fraud_email.signals import inspect

def test_homoglyph():
    assert normalize("dаta") == "data"

def test_threat_signal():
    reasons, risk = inspect("Your dаta", "We stole your dаta. Pay 0.005 ETH or your data will be sold")
    assert "threat" in reasons and risk > 0
