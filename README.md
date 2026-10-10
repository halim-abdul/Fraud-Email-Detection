# Fraud Email Detection 🛡️

**Explainable phishing/fraud triage, company relevance, short email summaries and human-reviewed reply drafts.** Includes NLP baseline experiments, FastAPI, Streamlit, n8n Gmail flow, synthetic Excel/CSV register and 12 notebooks.

> **Safety:** This is a research prototype, not an authenticated email security gateway. Threat scores are heuristic, not calibrated probabilities. No automated email replies are sent. Never pay extortion demands or open untrusted attachments based on these results.

## Gmail → n8n → Fraud Detection → AI Chatbot Summaries

The project separates **suspiciousness (security risk)** from **business importance (urgency)**. The n8n workflow calls a local FastAPI service and creates review-only routing data; it does not send emails or automatically create finished Excel files.

```text
                       ┌────────────────────────┐
                       │     INCOMING GMAIL     │
                       └────────────┬───────────┘
                                    ↓
                    Extract sender, receiver, subject,
                       body and Gmail message ID
                                    ↓
                    ┌───────────────────────────┐
                    │ Fraud / Phishing Analysis │
                    └─────────────┬─────────────┘
                                  ↓
                    Suspicion: LOW / MEDIUM / HIGH
                                  ↓
                     ┌────────────┴─────────────┐
                     │                          │
           Suspicious email                 Other emails
          (fraud/phishing/                (non-suspicious)
            needs_review)                      │
                     ↓                          ↓
            SECURITY REVIEW          Company Relevance Assessment
             No auto-reply                     │
             Review threats              ┌─────┴─────────────┐
                     │                    │                   │
                     │              Not relevant          Relevant
                     │                 / unknown             │
                     │                    ↓                   ↓
                     │                Review queue      Email Priority
                     │                                  Classification
                     │                                       │
                     │                             ┌─────────┴─────────┐
                     │                             │                   │
                     │                         Urgent / High       Normal / Low
                     │                             ↓                   ↓
                     │                       URGENT HUMAN          Legitimate
                     │                         REVIEW               Review
                     │                             └────────┬──────────┘
                     │                                      ↓
                     │                       AI Chatbot Email Summarization
                     │                         (2–4 short explanatory lines)
                     │                                      ↓
                     │                           Is a reply necessary?
                     │                             ┌────────┴────────┐
                     │                             │                 │
                     │                            YES                NO
                     │                             ↓                 ↓
                     │                         Draft Reply        No Reply
                     │                             ↓                 │
                     │                       HUMAN APPROVAL          │
                     │                             └────────┬────────┘
                     │                                      │
                     └───────────────────┬──────────────────┘
                                         ↓
                               Excel / CSV Report Queue
                       (From, To, Subject, Risk, Priority,
                          Relevance, Summary, Reply Status)
```

### What happens at each stage

1. **Gmail ingestion:** n8n's Gmail Trigger reads message metadata and available plain-text content. Real Gmail OAuth credentials are configured only in n8n; never commit them. Fields depend on your Gmail Trigger setup, so verify the input preview before activation.
2. **Fraud and phishing analysis:** FastAPI `POST /triage` scans subject and body for threats such as phishing, extortion, fake lotteries, unusual payment instructions, urgency and Unicode lookalike characters. Severity bands are based on a **heuristic index**, not validated fraud probabilities: **low** (<0.25), **medium** (0.25–<0.65), and **high** (≥0.65).
3. **Security routing:** `fraud`, `phishing` and `needs_review` messages enter a **human security review** queue regardless of company relevance. No suspicious message can trigger an automatic response. Treat even low-scoring messages with caution.
4. **Company relevance:** benign/other messages are assessed against the supplied `COMPANY_CONTEXT`. Messages with relevance not confirmed are routed to a review/log queue, not silently deleted.
5. **Business priority:** potentially urgent, relevant mail is surfaced for human review. Business urgency must be verified independently of the security-risk score; this repository currently provides a **heuristic routing placeholder**, not a trained SLA/urgency classifier.
6. **AI chatbot summarization automation:** n8n calls `POST /assistant/summarize` for relevant legitimate mail and retrieves short bullet-point summaries. The default is the **offline/rule-based summarizer**; a real external LLM is opt-in, disabled by default and only used for low-risk messages after explicit privacy approval. Email content is always treated as untrusted data. Review summaries for inaccuracies.
7. **Reply needed?** `reply_needed` is a conservative suggestion. For legitimate, relevant requests, the API can provide a short **draft**. An authorized human must verify sender, content and tone before any reply. **There is no Gmail Send node.**
8. **Excel / CSV register:** routing outputs include sender, recipient, subject, risk, relevance, priority, short summary and review/reply status. The n8n flow ends at an **export handoff**; connect a protected CSV/XLSX/Google Sheets destination yourself. Local Python example report generation is available using `python scripts/generate_example_reports.py`. Keep sensitive reports out of Git.

### Import and use the n8n automation

1. Launch the FastAPI service with `pip install -e '.[api,reports]'` and `uvicorn api.app:app --host 127.0.0.1 --port 8000` (use TLS, a proper reverse proxy, authentication, and network restrictions when deployed).
2. Import [`n8n/email_triage.workflow.json`](n8n/email_triage.workflow.json) into your n8n editor.
3. Set the **Gmail Trigger** OAuth credential and choose a testing inbox containing **synthetic** messages. Ensure the trigger returns sender, receiver, subject and body (otherwise add a Gmail Get Message node).
4. Configure n8n `FRAUD_TRIAGE_API_URL`, `FRAUD_SUMMARY_API_URL` and `COMPANY_CONTEXT`. Configure matching API authentication in production; the example HTTP nodes require authentication setup when `FRAUD_API_KEY` is set.
5. Execute with a synthetic test email, inspect the fraud band, security/other routing, chatbot summary, business relevance, priority and draft-approval fields. Confirm each branch is reached with relevant examples.
6. Add an approved human-review interface and a secure export destination. **Do not enable unattended replies.** After testing and adapting to your n8n version, activate the workflow.

### AI assistant / chatbot endpoints

| Endpoint | Function | Safety |
|---|---|---|
| `POST /triage` | Explainable fraud labels, risk score, priority, relevance, short baseline summary, draft suggestion | Always requires human review |
| `POST /assistant/summarize` | 2–4 line summary, baseline by default, optional external LLM | External LLM disabled unless explicitly enabled and privacy-approved |
| `POST /assistant/chat` | Answer analyst questions about risk, relevance and reply need | Read-only; cannot send mail |
| `GET /health` | API health check | No email access |

**Optional external LLM (only for approved synthetic/non-sensitive inputs):** install `pip install -e '.[api,llm]'`; set `FRAUD_ENABLE_EXTERNAL_LLM=1`, `FRAUD_LLM_PRIVACY_APPROVED=1`, `OPENAI_API_KEY`, and `FRAUD_LLM_MODEL` **outside Git**. Leave these unset for real company mail unless your organization's privacy/security team has approved the provider and data flow. Failures revert to offline summaries. LLM output never overrides fraud classification or triggers a send.

**Example local export:** `python scripts/generate_example_reports.py` creates ignored `artifacts/email_register.csv` and `artifacts/email_register.xlsx` using fictional messages. These examples do not access your live inbox. For actual mail exports, apply access control, retention, redaction and spreadsheet-injection protections.

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

The example phishing mail describing a purported data breach and cryptocurrency demand is represented here **only in anonymized, synthetic form**; original personal identifiers, crypto payment addresses and download links are intentionally omitted. ML model notebooks and toy data do not establish deployment quality. External LLM summarization is an optional opt-in read-only integration (disabled by default): any integration must ensure it cannot follow email instructions or send messages. For production: validate on real consented data, harden auth, handle SPF/DKIM/DMARC, rate limits, message idempotency, access controls, safe storage and monitoring.

See `docs/architecture.md`, `docs/threat_model.md`, `docs/modeling.md` and `n8n/README.md`.

## License

See [LICENSE](LICENSE).
