# Excel/CSV email register

The report includes sender, receiver, subject, classification, severity indicator, business relevance, response recommendation and short summaries. CSV output requires Python standard library only. XLSX is produced with the optional `reports` dependency. Filenames under `artifacts/` are intentionally ignored by Git because real mail data may be sensitive. Sample addresses use the reserved `.invalid` domain and are fictional. Guard against spreadsheet formula injection and encrypt business exports at rest.
