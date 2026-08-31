# AGE-600 Netlify Preview Test Recipe

Run only after explicit approval to create/use a deploy preview and send one synthetic submission. Never test first on production. This local AGE-600 build does not authorise a preview host, production submission or notification change.

## Synthetic values

- Name: `Proof Systems Test Lead`
- Business email: an approved non-personal test inbox
- Company: `Synthetic Workflow Ltd`
- Workflow: `Weekly synthetic status report compiled from three sample trackers`
- Consent: checked

Do not send decision role, desired outcome or hours. Those fields were removed.

## Checks

1. Confirm the preview uses the expected branch commit and production remains unchanged.
2. Check homepage, Work, one story, enquiry and privacy at 1440×900, 1280×720, 768×1024 and 390×844.
3. Confirm the page presents the operational-systems proposition, Discuss a workflow, eight story routes and synthetic-demonstration labelling.
4. Confirm no founding-cohort dates, place counts, free-diagnostic claims, £350 price, Pantera quotation, Xonetic, YouTube, public prices or unverified performance claims appear publicly.
5. Submit the approved synthetic record once, only on an approved preview.
6. Confirm `proof-systems-qualifier` is detected and contains: `name`, `email`, `company`, `workflow_help`, `contact_consent`, `route_key=general-enquiry`, `route_label=Discuss a workflow`, `lead_state=enquiry-received`, `page_source=workflow.html`, `submitted_at`. An allow-listed CTA may also set hidden `interest_source` to `focused-build`, `workflow-diagnostic` or `ai-team-training` without changing the route. Invalid `interest` values must fall back to the generic form.
7. Confirm notification delivery to the approved inbox and that no answers appear in the browser URL.
8. Confirm `/video-series` noindexes and returns to the homepage, and `/checkout` noindexes and points to the enquiry form.
9. Delete the synthetic Netlify record and notification email after evidence is recorded.

Stop before merging or production deployment and ask Mat for explicit approval with screenshots, test evidence, residual risks and rollback instructions.
