import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from fraud_email.schemas import EmailInput, TriageResult
from fraud_email.triage import classify
from fraud_email.assistant import summarise_email
from fraud_email.chatbot import answer

app = FastAPI(title="Fraud Email Detection", version="0.2.0")


def authorize(x_api_key: str | None) -> None:
    key = os.getenv("FRAUD_API_KEY")
    if key and x_api_key != key:
        raise HTTPException(401, "Invalid API key")


class ChatRequest(BaseModel):
    email: EmailInput
    question: str = Field(min_length=1, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok", "mode": "human-review", "auto_send": False}


@app.post("/triage", response_model=TriageResult)
def triage(email: EmailInput, x_api_key: str | None = Header(default=None)):
    authorize(x_api_key)
    return classify(email)


@app.post("/assistant/summarize")
def email_summary(email: EmailInput, x_api_key: str | None = Header(default=None)):
    authorize(x_api_key)
    return summarise_email(email)


@app.post("/assistant/chat")
def chat(request: ChatRequest, x_api_key: str | None = Header(default=None)):
    authorize(x_api_key)
    return answer(request.email, request.question)
