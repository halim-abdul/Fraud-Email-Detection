from pathlib import Path
from fraud_email.schemas import EmailInput
from fraud_email.reports import export_csv,export_xlsx

emails=[EmailInput(message_id="SYN001",sender="alerts@example.invalid",recipient="team@example.invalid",subject="Your dаta",body="We stole your data. Pay ETH or your data will be sold on the deep web."),
        EmailInput(message_id="SYN002",sender="client@example.invalid",recipient="team@example.invalid",subject="Meeting request",body="Please respond with meeting details for Acme procurement.",company_context="Acme procurement"),
        EmailInput(message_id="SYN003",sender="promo@example.invalid",recipient="team@example.invalid",subject="Special offer",body="Promotion: unsubscribe anytime.")]
Path("artifacts").mkdir(exist_ok=True)
export_csv(emails,"artifacts/email_register.csv")
export_xlsx(emails,"artifacts/email_register.xlsx")
print("Generated synthetic example reports in artifacts/")
