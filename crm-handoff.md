# Minimum CRM Handoff

## Approved V1 system boundary

The manual V1 path is:

`Netlify form submission -> restricted Proof Systems Launch Contacts database in Notion -> pseudonymous Lead Register in the AGE-421 workbook`

- **Netlify** is the short-lived source submission and notification transport.
- **Restricted Notion** is the identity/contact register. It may hold the person's name, company, business contact details, contact preference/permission, source submission reference and retention-review date.
- **AGE-421 workbook** is the approved commercial source of truth. Its `Lead Register` holds one pseudonymous row per prospect and no name, email, telephone number, detailed submission, recording, transcript or sensitive workflow evidence.
- **Linear** remains task tracking, not a lead database. Do not create one issue per lead or mirror the pipeline there.

There is no live automation between these systems. Mat performs or explicitly approves every transfer.

## Intake procedure

1. Open the Netlify submission from the approved notification and check for sensitive information before copying anything.
2. If the submission includes credentials, customer-identifiable data, special-category data, confidential documents or unusually sensitive commercial detail, restrict it, do not copy the detail, and follow the sensitive-data procedure in `lead-response-sop.md`.
3. Search the restricted Notion register by email, telephone number and company. Update the existing record if it is the same relationship; do not create a duplicate.
4. If it is new, allocate the next unused `PS-L###` lead ID in Notion. Never recycle an ID.
5. In Notion, record only identity/contact data, the Netlify submission ID or reference, source, contact permission, owner, next action, next-action due date and retention-review date. Use a short, non-sensitive workflow label only if needed to identify the enquiry.
6. Create or update the row with the same lead ID in the AGE-421 workbook `Lead Register`. Record the commercial facts using the workbook's existing columns:

   - `Source`: Website qualifier
   - `Stage`: the current commercial stage
   - `Lead state`: the live route state or subsequent state
   - `Broad segment` and `Workflow class`: broad, non-identifying categories only
   - `Next action (generic)` and `Due date`: one action and one date
   - `Permission / consent`: contact permission only; do not imply recording or AI-processing consent
   - dates and `Notes (non-sensitive)`: only what is needed to manage the launch evidence

7. Confirm the workbook `Row check` is `OK`. Resolve duplicates or missing required fields before treating intake as complete.
8. Delete the Netlify submission when it is no longer required for intake or dispute handling, and no later than the published 90-day limit for an unprogressed enquiry.

## Live route-state mapping

These values come from `workflow.html` and must not be silently renamed in the handoff:

| `route_key` | Netlify `lead_state` | Initial workbook interpretation | First generic next action |
| --- | --- | --- | --- |
| `paid` | `diagnostic_requested` | New / diagnostic request | Review diagnostic fit |
| `product` | `product_process_route` | New / product-process route | Review simplest suitable route |
| `video` | `video_routed` | New / guidance route | Select an available resource or alternative |
| `call` | `call_requested` | New / fit-call request | Review whether a 15-minute call is useful |
| `training` | `training_enquiry` | New / training enquiry | Review team need and fit-call route |

The website result is a recommendation and enquiry, not proof of qualification, a booking, payment or consent to marketing.

## Ownership and deadlines

- Mat owns every V1 lead. The named owner is canonical in restricted Notion because the AGE-421 `Lead Register` has no owner column. Any delegation requires an explicit Notion owner before handoff; do not overload a workbook field with identity data.
- Every open lead has exactly one owner, one dated next action and one canonical commercial stage.
- Review a new submission by the end of the next working day.
- Send an acknowledgement or a bounded clarification request within one working day of review. If the full response will take longer, state the response date.
- When awaiting a lead reply, follow up once after three working days and once after seven working days, then close as `no response` unless a specific later date was agreed.
- A booked appointment belongs in the calendar and CRM record; do not duplicate it as a Linear task.

## Stalled-lead fail-safe

The restricted Notion register must retain an `Open - due or overdue` view. At the start of each Proof Systems working day, Mat reviews it against the AGE-421 workbook.

An open lead is invalid if the owner, next action or due date is blank. Correct it that day by choosing one of three outcomes: perform the action, set a justified new date, or close/defer the lead. Do not repeatedly roll an overdue date forward without recording why. A deferred lead needs a specific review date; otherwise close it.

Reconcile Notion and the workbook weekly by lead ID. Identity, contact and named owner win in Notion; stage, activity, value, next action and launch evidence win in AGE-421. Resolve disagreement rather than maintaining two versions.

## Consent and retention boundary

- `consent_contact` from the website records permission to respond to that enquiry. It is not general marketing consent.
- Recording consent and AI-processing consent are separate, session-specific decisions. Record their status in the approved diagnostic operating record, not by changing the meaning of website contact consent.
- Offer a non-recorded diagnostic without disadvantage.
- Never store recordings, transcripts or diagnostic evidence in this website repository, Notion identity register or AGE-421 workbook.
- If contact permission is withdrawn, stop optional contact, update both registers and action deletion/correction requests across Netlify and Notion. Preserve only any minimum record that has a documented lawful need.
- Review unprogressed enquiry data for deletion within 90 days. A progressed relationship gets a new, explicit retention review rather than an indefinite extension.

## Synthetic route tests

Use invented data only. Do not submit these to the live site unless Mat separately approves a live test.

For each of the five rows in the route mapping table:

1. Confirm the local qualifier produces the expected `route_key`, `lead_state` and `checkout.html?route=...` URL.
2. Create a temporary synthetic Notion-shaped record in test notes, allocate a clearly synthetic ID and check duplicate matching by email/company.
3. Give the temporary Notion-shaped record one owner, then create a temporary synthetic workbook row with the same ID, one generic next action, a due date and contact-permission state.
4. Check `Row check` reports `OK`, no identity/contact or detailed workflow text reaches the workbook, and no Linear issue is created.
5. Exercise fit confirmed, needs clarification, deferred and no-response closure, including the three- and seven-working-day follow-ups.
6. Remove all synthetic records and confirm no live contact, message, booking or payment was produced.

Pass condition: one identity record and one pseudonymous commercial row remain consistently linked throughout each simulated route, with one owner and one dated next action.
