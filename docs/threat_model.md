# Threat model

Attacker controls headers, display name, subject, body, link text, URLs and attachments. Threats include lookalike domains, unicode homoglyphs, credential theft, crypto-extortion, fake lottery, business email compromise and prompt injection. The scorer is heuristic and is not proof of fraud. Analyze attachments only inside hardened sandbox, never execute or fetch them by default. Do not log raw email bodies or credentials. Restrict Gmail scopes. Quarantine high risk mail, record reasons, require human review, and never auto-send replies.
