from fraud_email.schemas import EmailInput
from fraud_email.reports import export_csv

def test_csv_export(tmp_path):
    p=tmp_path/"report.csv"
    export_csv([EmailInput(sender="test@example.invalid",subject="Meeting")],str(p))
    content=p.read_text()
    assert "sender,recipient,subject" in content
    assert "test@example.invalid" in content
