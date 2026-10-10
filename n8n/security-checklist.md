# Deployment safety checklist

- Use read-only Gmail permissions where feasible; never auto-send responses.
- Validate sender authentication separately; a display name is not identity.
- Do not give an LLM tools that can send mail, visit arbitrary links, or access secrets.
- Apply per-user authorization to human approval and restrict export access.
- Mask stored PII and avoid logging bodies.
- Test against prompt injection in sender, subject, body and attachments.
- Use retries, deduplication by message ID and idempotency for durable processing.
