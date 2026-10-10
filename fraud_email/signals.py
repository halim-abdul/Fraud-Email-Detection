import re
from urllib.parse import urlparse
from .normalization import normalize

SIGNALS = {
    "extortion": (r"\\b(?:pay|send|transfer)\\b.{0,80}\\b(?:eth|bitcoin|crypto|wallet)\\b|\\b(?:data|information)\\b.{0,60}\\b(?:sold|leaked|deep web)\\b", 0.58),
    "prize": (r"\\b(?:lottery|jackpot|prize|winner|won money|inheritance)\\b", 0.31),
    "credentials": (r"\\b(?:verify|confirm|reset)\\b.{0,55}\\b(?:password|account|login|bank)\\b", 0.3),
    "urgency": (r"\\b(?:within 24 hours|act now|immediately|final warning|deadline)\\b", 0.16),
    "payment": (r"\\b(?:gift card|wire transfer|send funds|crypto wallet|metamask|payment address)\\b", 0.25),
    "threat": (r"\\b(?:stole your data|your data will be sold|we have your data|blackmail|ransom)\\b", 0.42),
    "marketing": (r"\\b(?:unsubscribe|promotion|special offer|advertisement)\\b", 0.08),
}
URL_RE = re.compile(r"https?://[^\\s<>\\\"']+", re.I)

def inspect(subject: str, body: str) -> tuple[list[str], float]:
    content = normalize(subject + " " + body)
    hits, score = [], 0.0
    for name, (expression, weight) in SIGNALS.items():
        if re.search(expression, content):
            hits.append(name)
            score += weight
    if URL_RE.search(body):
        hosts = [urlparse(x.rstrip(").,")).hostname or "" for x in URL_RE.findall(body)]
        if any(x.startswith("xn--") for x in hosts):
            hits.append("punycode_link")
            score += 0.3
    if subject and normalize(subject) != unicase(subject):
        hits.append("confusable_characters")
        score += 0.12
    return hits, min(1.0, score)

def unicase(text: str) -> str:
    import unicodedata
    return unicodedata.normalize("NFKC", text).casefold()
