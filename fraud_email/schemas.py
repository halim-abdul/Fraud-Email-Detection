from typing import Literal
from pydantic import BaseModel, Field

class EmailInput(BaseModel):
    message_id: str = ""
    sender: str = ""
    recipient: str = ""
    subject: str = Field(default="", max_length=2000)
    body: str = Field(default="", max_length=200000)
    company_context: str = ""

class TriageResult(BaseModel):
    message_id: str
    label: Literal["phishing", "fraud", "spam", "legitimate", "needs_review"]
    risk_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    priority: Literal["critical", "high", "normal", "low"]
    relevant: bool
    reply_needed: bool
    review_required: bool = True
    reasons: list[str]
    summary: list[str]
    proposed_reply: str | None = None
