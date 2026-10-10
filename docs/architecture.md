# Architecture

Inbound mail (Gmail trigger) → n8n sanitization/metadata → FastAPI /triage → rules and optional offline ML score → n8n IF/route → human review → draft response (never send automatically) → approved Excel/CSV export.

Risk, relevance, priority and reply-needed are separate axes. Subject and body are both inspected. LLM is optional advisory summarization; adversarial email text remains untrusted. No keys are stored in the repository.
