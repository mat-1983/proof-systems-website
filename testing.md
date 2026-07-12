# Proof Systems Website Testing

Updated: 2026-07-12

## Checks Run

- Independent code review of qualifier routing, Netlify submission and route-review handoff.
- URL-data regression: route-review links contain only `route`; contact and workflow fields are absent.
- Consent/submission copy and privacy-link review.
- Public-copy scan for internal planning wording, empty-library claims and the unsupported 4,400+ hours claim.
- Form-schema check against the Netlify V1 field list.
- Synthetic proof-asset inspection and metadata/source review.
- Local route, link, HTML, JavaScript, desktop/mobile and diff checks (see current command/test receipts below).

## 12 July Results

- Desktop viewport (1440×900): qualifier rendered without horizontal overflow.
- Mobile viewport (390×844): qualifier and route review rendered without horizontal overflow.
- Synthetic diagnostic scenario routed correctly; local mode made no submission and the handoff URL was exactly `checkout.html?route=paid`.
- Same-session checkout recovered the synthetic handoff details without placing them in the URL.
- Local-link scan: no broken internal targets.
- Form schema: all required fields present, with no extras.
- JavaScript syntax checks and `git diff --check`: passed.
- Sensitive URL/public-copy scan: no contact/workflow query fields, 4,400+ claim or internal launch note remained in public HTML.
- Independent close-out review corrected stale public wording on the route page: live submissions are acknowledged as sent for manual review, while local previews are explicitly described as unsent; neither path claims that payment or booking occurred.

- Local route regression in Chrome for all five route types:
  diagnostic, video, product/process, call, training.
- Conditional phone validation:
  call and training require phone.
- Video-to-call guardrail:
  call request from a video result is blocked until phone is present.
- Desktop and mobile visual pass for the qualifier and route review pages.
- Simulated Netlify HTTPS POST:
  confirmed one submission is sent on route calculation with the expected schema fields.
- Duplicate-submission guardrail:
  clicking the matching route handoff after a successful submission does not resubmit the same route.
- `git diff --check`:
  clean for `workflow.html` and the backend recommendation note.

## What Passed

- Route selection still behaves correctly after Netlify Forms wiring.
- Hidden route fields populate correctly:
  `route_key`, `route_label`, `lead_state`, `page_source`, `submitted_at`.
- Netlify-compatible form fields are present:
  `form-name`, honeypot, schema-aligned field names.
- Local `file://` usage does not submit data anywhere.

## Not Yet Tested / Approval Gated

- Real Netlify submission storage on the live or preview site.
- Real Gmail notification delivery from the current Netlify setup.
- Netlify dashboard export behaviour with actual dummy submissions.
- Whether the notification should go to one inbox or multiple recipients.
- Professional legal review of the privacy wording.
- Mat's commercial-tone and visual approval.
- Real Netlify preview/live storage and Gmail delivery; use `netlify-test-recipe.md` only after explicit approval.

## Close-Out Preparation Check

- `CODEX-BUNDLE.md` exists and routes a fresh Codex chat through the correct Linear issues.
- The prompt prohibits deploy, publish, payment, credentials, live personal data and external messages without approval.
- Existing local website behaviour was not re-tested during this close-out because no website implementation code changed.

## Residual Risk

- The commercial feel may still be slightly heavy if the contact capture feels too long in practice.
- Live notification wiring could still expose an environment-specific quirk that local simulation cannot catch.

## Live production acceptance — 12 July 2026

- PASS — the reviewed seven-file site package was deployed to the existing `proofsystems.co.uk` Netlify project.
- PASS — public home, workflow and privacy routes serve the reviewed content; Netlify's extensionless-link normalisation is the only observed source transformation.
- PASS — form detection was enabled and a subsequent production deploy registered `proof-systems-qualifier` as one active form.
- PASS — the approved form-submission email notification was configured for the privately confirmed Proof Systems inbox.
- PASS — one synthetic diagnostic-route submission displayed `Route saved` and kept workflow/contact answers out of the browser URL.
- PASS — Netlify stored route key/label, lead state, page source, timestamp, workflow/outcome/context, hours, desired help, contact/company/role/sector and consent as expected.
- PASS — the matching email notification arrived at 18:08 with the correct route and submission timestamp.
- PASS — the synthetic Netlify submission and notification email were deleted after verification; Netlify reported no remaining verified submissions.
- CLEAN-UP — the accidental temporary Netlify project `shimmering-mandazi-0fbee6` was permanently deleted; only `proofsystems.co.uk` remains.

## Lead handoff documentation verification — 12 July 2026

- PASS — `crm-handoff.md` maps Netlify submissions into the restricted Notion identity register and the pseudonymous AGE-421 commercial register without duplicating Linear.
- PASS — all five live route/state pairs match `workflow.html` exactly.
- PASS — duplicate prevention, one-owner/one-next-action rules, next-working-day review, 3/7-working-day follow-ups and overdue/deferred controls are explicit.
- PASS — `lead-response-sop.md` separates website contact permission from recording and AI-processing consent.
- PASS — synthetic test instructions require removal of test records and prohibit live submission without separate approval.
- PASS — `git diff --check` is clean.
