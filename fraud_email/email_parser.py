from email import policy
from email.parser import BytesParser
from .schemas import EmailInput

def parse_eml(data: bytes) -> EmailInput:
    if len(data) > 2_000_000:
        raise ValueError("Email exceeds configured size limit")
    message = BytesParser(policy=policy.default).parsebytes(data)
    part = message.get_body(preferencelist=("plain",))
    body = part.get_content() if part is not None else ""
    return EmailInput(message_id=message.get("Message-ID",""),sender=message.get("From",""),
        recipient=message.get("To",""),subject=str(message.get("Subject","")),body=body[:200000])
