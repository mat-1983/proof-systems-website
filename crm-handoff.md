# General enquiry handoff

Updated: 2026-08-29

## System boundary

- Netlify Forms receives the source enquiry under form name `proof-systems-qualifier`.
- The restricted Notion identity register holds name, business email, company, consent, owner and response history.
- The AGE-421 workbook holds the pseudonymous commercial record only. It must not contain names, emails or detailed workflow descriptions.
- Linear tracks delivery work, not individual prospects.

## One-route mapping

| Website value | Meaning | Initial action |
|---|---|---|
| `route_key: general-enquiry` | Discuss a workflow | Review the enquiry |
| `route_label: Discuss a workflow` | Public enquiry action | Respond by next working day |
| `lead_state: enquiry-received` | Submitted and awaiting review | Respond by next working day |
| `page_source: workflow.html` | Short enquiry form | Keep visitor answers out of URLs |
| `interest_source: ai-team-training` | Reached from Ask about team training | Discuss the workshop; same general-enquiry route |

## Manual handoff

1. Review Netlify by the next working day.
2. Search the restricted identity register by business email and company; update an existing relationship rather than creating a duplicate.
3. Assign or retain the pseudonymous `PS-L###` identifier.
4. Record the minimum identity/contact details, consent evidence, owner, next action and due date in the restricted register.
5. Create or update one AGE-421 row with the pseudonymous ID, source `Website enquiry`, current stage and no identifying or sensitive narrative.
6. Apply the response recipe in `lead-response-sop.md`.
7. Delete unprogressed Netlify source enquiries within 90 days.

## Controls

- One owner, one next action and one due date per enquiry.
- Never copy confidential workflow evidence into the workbook or Linear.
- Website contact consent is not recording, transcription or AI-processing consent.
- Use synthetic data only in an explicitly approved preview test and delete it after verification.
- Do not submit the form to production from this local build.
