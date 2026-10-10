# REST API

Start: `pip install -e '.[api]'`, then `uvicorn api.app:app --host 127.0.0.1 --port 8000`.

`POST /triage` consumes JSON `{"message_id":"id-1","sender":"alice@example.org","recipient":"team@example.org","subject":"Meeting request","body":"Please respond","company_context":"team meetings"}`. Return values: label, risk_score, confidence, priority, relevant, reply_needed, review_required, reasons, summary, proposed_reply. `GET /health` probes service. Configure `FRAUD_API_KEY` and pass `X-API-Key` outside a private development network. Bind locally by default and use TLS in deployment.
