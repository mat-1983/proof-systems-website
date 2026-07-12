# AGE-424 Netlify Preview Test Recipe

Run only after explicit approval to create/use a deploy preview and send one synthetic submission. Never test first on production.

## Synthetic values

- Name: `Proof Systems Test Lead`
- Business email: an approved non-personal test inbox
- Company: `Synthetic Workflow Ltd`
- Role: `Owner; controls this synthetic workflow`
- Workflow: `Weekly synthetic status report compiled from three sample trackers`
- Outcome: `One controlled view with visible exceptions`
- Hours: `4`
- Consent: checked

## Checks

1. Confirm the preview uses the expected branch commit and production remains unchanged.
2. Check homepage and application at desktop and mobile widths.
3. Confirm the page presents one free founding-cohort proposition, one dominant CTA and two operational examples.
4. Confirm no £350 price, fundraising claim, video CTA, training route, fit-call route, product route or internal/local-planning language appears publicly.
5. Submit the approved synthetic record once.
6. Confirm `proof-systems-qualifier` is detected and contains: `name`, `email`, `company`, `decision_role`, `workflow_help`, `desired_outcome`, `hours_per_week`, `contact_consent`, `route_key`, `route_label`, `lead_state`, `page_source`, `submitted_at`.
7. Confirm notification delivery to the approved inbox and that no answers appear in the browser URL.
8. Confirm `/video-series` intentionally returns to the homepage and `/checkout` points to the founding application.
9. Delete the synthetic Netlify record and notification email after evidence is recorded.

Stop before merging or production deployment and ask Mat for explicit approval with screenshots, test evidence, residual risks and rollback instructions.
