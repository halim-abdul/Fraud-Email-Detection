from .signals import inspect
from .domain_checks import url_indicators

def extract_features(subject: str, body: str) -> dict[str, float]:
    hits, score = inspect(subject,body)
    urls = url_indicators(body)
    return {"risk_rules": score, "hit_count": float(len(hits)), "suspicious_url_count":float(len(urls)),
            "subject_length":float(len(subject)), "body_length":float(len(body)),
            "capital_ratio":sum(c.isupper() for c in subject)/max(len(subject),1)}
