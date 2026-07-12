# Founding Diagnostic Application Handoff

Updated: 2026-07-12

## System boundary

- Netlify Forms receives the source application under form name `proof-systems-qualifier`.
- The restricted Notion identity register holds name, business email, company, role, consent, owner and response history.
- The AGE-421 workbook holds the pseudonymous commercial record only. It must not contain names, emails or detailed workflow descriptions.
- Linear tracks delivery work, not individual prospects.

## One-route mapping

| Website value | Meaning | Initial action |
|---|---|---|
| `route_key: founding-diagnostic` | Founding diagnostic application | Review cohort fit |
| `lead_state: application-received` | Submitted and awaiting review | Respond by next working day |

## Manual handoff

1. Review Netlify by the next working day.
2. Search the restricted identity register by business email and company; update an existing relationship rather than creating a duplicate.
3. Assign or retain the pseudonymous `PS-L###` identifier.
4. Record the minimum identity/contact details, consent evidence, owner, next action and due date in the restricted register.
5. Create or update one AGE-421 row with the pseudonymous ID, source `Website founding cohort`, current stage and no identifying or sensitive narrative.
6. Apply the response recipe in `lead-response-sop.md`.
7. Delete unprogressed Netlify source applications within 90 days.

## Controls

- One owner, one next action and one due date per application.
- Never copy confidential workflow evidence into the workbook or Linear.
- Website contact consent is not recording, transcription or AI-processing consent.
- Use synthetic data only in an explicitly approved preview test and delete it after verification.
