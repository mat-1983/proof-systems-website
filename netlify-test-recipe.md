# AGE-343 Netlify Preview/Live Dummy-Submission Recipe

## Approval gate

Mat must choose deploy preview or live site, confirm the notification inbox, approve the commercial copy and authorise one synthetic submission. Do not proceed without that approval.

## Safe dummy record

- Name: `Test Lead — Delete`
- Email: an approved Proof Systems-controlled test address
- Phone (call/training test only): `07000 000000` if Netlify accepts it, otherwise an approved non-personal test number
- Company: `Example Operations Ltd`
- Role: `Operations test`
- Sector: `Business services`
- Workflow: `Synthetic weekly document register test; no real customer data.`
- Outcome: `Confirm form storage and notification only.`
- Context: `Synthetic test submission for AGE-343; delete after verification.`
- Hours: `5`

## Exact test

1. Open the approved Netlify URL in a private window and record the URL, deploy identifier and time.
2. Confirm `privacy.html` loads and the qualifier contains the submission/consent wording.
3. Submit the synthetic record once for the diagnostic route. Confirm the browser shows a saved-success message and the route-review URL contains only `route`, never contact or workflow answers.
4. In Netlify, confirm one `proof-systems-qualifier` submission exists and the schema contains: `workflow_help`, `desired_outcome`, `workflow_context`, `hours_per_week`, `desired_help`, `name`, `email`, `phone`, `company`, `role`, `sector`, `consent_contact`, `route_key`, `route_label`, `lead_state`, `page_source`, `submitted_at`.
5. Confirm the approved Gmail inbox receives one notification and that its timestamp and route match the stored submission. Do not forward it.
6. Test a call route with the phone blank and confirm the browser blocks submission. Do not create a second stored record unless Mat explicitly approves it.
7. Delete the dummy submission and notification after recording pass/fail evidence.
8. Record the result on AGE-343. Only then can storage and Gmail delivery be marked verified; publication remains a separate approval.

## Evidence

Record: tested URL, deploy/live choice, timestamp, form name, submission ID, notification inbox (redacted in public notes), delivery timestamp, schema pass/fail, URL-data pass/fail, deletion confirmation and any retry. Never paste the full dummy submission or inbox address into public material.
