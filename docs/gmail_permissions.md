# Gmail integration

OAuth credentials are configured exclusively inside n8n and never committed. Review Google's least-privilege scopes and domain-wide delegation policy. A Gmail trigger is useful for prototypes, but production ingestion requires message-ID deduplication, retry queues, monitoring and secure retention. The sample flow does not send or modify mail and is intentionally inactive until configured.
