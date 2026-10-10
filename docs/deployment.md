# Deployment guidance

Local API: `uvicorn api.app:app --host 127.0.0.1 --port 8000`. Container: `docker compose up --build`. Set a long random `FRAUD_API_KEY`. Never publish the development server to the internet unprotected. Production needs TLS termination, identity-based auth, rate limits, redacted structured logs, secret manager, monitoring, backup and a retention schedule. n8n triggers require credential setup and are not activated in source control.
