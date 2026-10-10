# Fraud Email Detection 🛡️

**Explainable phishing/fraud triage, company relevance, short email summaries and human-reviewed reply drafts.** Includes NLP baseline experiments, FastAPI, Streamlit, n8n Gmail flow, synthetic Excel/CSV register and 12 notebooks.

> **Safety:** This is a research prototype, not an authenticated email security gateway. Threat scores are heuristic, not calibrated probabilities. No automated email replies are sent. Never pay extortion demands or open untrusted attachments based on these results.

## End-to-end flow

```text
Gmail → n8n trigger → normalize subject/body/sender/recipient
      → POST /triage → indicators + relevance + priority + bullets
      ├─ fraudulent/phishing → quarantine / security review, NO reply
      ├─ irrelevant → log / optional archive review
      └─ legitimate and relevant → optional reply DRAFT → HUMAN approval
      → CSV / Excel sender-recipient-subject register
```

## Quick start

```bash
python -m venv .venv
# Activate venv for your operating system
pip install -e '.[api,dashboard,reports,train,dev]'
pytest -q
uvicorn api.app:app --host 127.0.0.1 --port 8000
# in another terminal:
streamlit run dashboard/app.py
```

Test without services:

```bash
printf '%s' '{"subject":"Your dаta","body":"We stole your data. Pay ETH or your data will be sold"}' | python -m fraud_email
python scripts/generate_example_reports.py
python scripts/train.py --mlflow
```

## Features

| Module | Details |
| --- | --- |
| `fraud_email/triage.py` | Fraud/phishing/spam/review/legitimate routing; company relevance and priority |
| `fraud_email/signals.py` | Interpretable extortion, lottery, fake prizes, crypto transfer, urgency indicators |
| `fraud_email/normalization.py` | Unicode normalization and basic anti-homoglyph checks |
| `fraud_email/ml.py` | TF-IDF and logistic regression experimental baseline |
| `api/app.py` | FastAPI `/health`, `/triage`; optional shared API key |
| `dashboard/app.py` | Streamlit review of subjects, bodies, summaries and proposed drafts |
| `n8n/email_triage.workflow.json` | Importable Gmail-to-FastAPI human-review routing (inactive by default) |
| `fraud_email/reports.py` | CSV and optional Excel report with from/to/subject/risk/priority/summary |
| `notebooks/` | 12 experiments and tutorials |

## Research boundaries

The example phishing mail describing a purported data breach and cryptocurrency demand is represented here **only in anonymized, synthetic form**; original personal identifiers, crypto payment addresses and download links are intentionally omitted. ML model notebooks and toy data do not establish deployment quality. Optional LLM guidance is a **non-executing prompt policy**, not a configured live LLM: any integration must ensure it cannot follow email instructions or send messages. For production: validate on real consented data, harden auth, handle SPF/DKIM/DMARC, rate limits, message idempotency, access controls, safe storage and monitoring.

See `docs/architecture.md`, `docs/threat_model.md`, `docs/modeling.md` and `n8n/README.md`.

## License

See [LICENSE](LICENSE).
