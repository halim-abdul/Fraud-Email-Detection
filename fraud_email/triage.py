import re
from .schemas import EmailInput, TriageResult
from .signals import inspect
from .normalization import normalize

def summarize(email: EmailInput, reasons: list[str]) -> list[str]:
    body = re.sub(r"\\s+", " ", email.body).strip()
    clauses = [s.strip() for s in re.split(r"(?<=[.!?])\\s+", body) if s.strip()]
    out = [f"Subject: {email.subject[:130] or '(none)'}"]
    out += [s[:220] for s in clauses[:2]]
    if reasons:
        out.append("Risk indicators: " + ", ".join(reasons[:6]))
    return out[:4]

def classify(email: EmailInput) -> TriageResult:
    reasons, score = inspect(email.subject, email.body)
    context = normalize(email.company_context)
    text = normalize(email.subject + " " + email.body)
    relevant = bool(context and any(w in text for w in re.findall(r"[a-z]{4,}", context)[:8]))
    if score >= 0.65:
        label = "fraud" if any(x in reasons for x in ["extortion", "prize", "threat", "payment"]) else "phishing"
    elif score >= 0.25:
        label = "needs_review"
    elif "marketing" in reasons:
        label = "spam"
    else:
        label = "legitimate"
    priority = "critical" if score >= 0.75 else "high" if score >= 0.4 else "normal" if relevant else "low"
    # Never automatically reply to suspicious/untrusted emails or let them supply instructions.
    reply_needed = relevant and label == "legitimate" and any(w in text for w in ("question", "request", "please respond", "meeting", "invoice"))
    proposed = ("Thank you for your message. We have received your request and will review it." if reply_needed else None)
    return TriageResult(message_id=email.message_id, label=label, risk_score=round(score,3),
        confidence=round(max(0.5, 1 - abs(score - 0.5)),3), priority=priority,
        relevant=relevant, reply_needed=reply_needed, review_required=True,
        reasons=reasons, summary=summarize(email,reasons), proposed_reply=proposed)
