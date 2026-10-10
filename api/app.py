import os
from fastapi import FastAPI, Header, HTTPException
from fraud_email.schemas import EmailInput, TriageResult
from fraud_email.triage import classify

app = FastAPI(title="Fraud Email Detection", version="0.1.0")

@app.get("/health")
def health():
    return {"status":"ok","mode":"human-review"}

@app.post("/triage", response_model=TriageResult)
def triage(email: EmailInput, x_api_key: str | None = Header(default=None)):
    key = os.getenv("FRAUD_API_KEY")
    if key and x_api_key != key:
        raise HTTPException(401, "Invalid API key")
    return classify(email)
