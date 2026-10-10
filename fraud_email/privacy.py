import re

def redact(text: str) -> str:
    text = re.sub(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[REDACTED_EMAIL]", text)
    text = re.sub(r"0x[a-fA-F0-9]{30,}", "[REDACTED_CRYPTO_ADDRESS]", text)
    return re.sub(r"\b(?:\+?\d[ -]?){10,15}\b", "[REDACTED_PHONE]", text)
