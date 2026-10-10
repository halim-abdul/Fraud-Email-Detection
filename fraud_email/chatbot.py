"""Auditable, offline triage assistant. Does not execute instructions from email text."""
from .schemas import EmailInput
from .triage import classify

def answer(email: EmailInput, question: str) -> dict:
    result = classify(email)
    q = question.casefold().strip()
    if any(word in q for word in ("reply", "respond", "answer")):
        text = ("A draft is suggested, but an authorized human must approve it." if result.reply_needed
                else "Do not automatically reply; review the message before any response.")
    elif any(word in q for word in ("why", "fraud", "phish", "risk")):
        text = ("Indicators: " + ", ".join(result.reasons)) if result.reasons else "No configured fraud indicators matched; absence of indicators is not proof of safety."
    elif any(word in q for word in ("relevant", "company", "important")):
        text = ("Relevant to provided company context." if result.relevant else
                "Company relevance was not confirmed; route for human triage if business critical.")
    else:
        text = "Summary: " + " / ".join(result.summary)
    return {"answer":text,"classification":result.label,"priority":result.priority,
            "review_required":True,"action_executed":False}
