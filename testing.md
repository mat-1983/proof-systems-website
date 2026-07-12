# Proof Systems Website Testing

Updated: 2026-07-12

## AGE-424 reduced founding-cohort branch — 12 July 2026

- PASS — all five public HTML files parsed without parser exceptions.
- PASS — local internal-link scan found no missing targets.
- PASS — application JavaScript compiled successfully.
- PASS — homepage and application rendered in headless Chrome at desktop and narrow viewport sizes; no layout defect was found in the desktop review and defensive narrow-screen constraints are present.
- PASS — the application has exactly eight substantive visitor fields: name, business email, company, decision role, workflow, desired outcome, optional hours and contact consent.
- PASS — the existing Netlify form name `proof-systems-qualifier`, honeypot and hidden operational fields remain present.
- PASS — local/localhost submission is explicitly intercepted without sending data and uses customer-safe wording.
- PASS — public HTML contains no £350 price, £1.6m claim, 4,400+ claim, video-first route, training route, fit-call route, product/process route, `not wired` wording or `local only` wording.
- PASS — `/video-series` is an accessible holding page with no timed redirect; the former `/checkout` route points to the founding application without reviving the old offer catalogue.
- PASS — `git diff --check` is clean.
- PASS — an approval-gated temporary Netlify Drop preview detected `proof-systems-qualifier`, accepted one clearly synthetic application and stored one submission against the correct form.
- PASS — the visitor success state appeared in place, and the browser URL remained `workflow.html` with no application answers in it.
- NOT CONFIGURED — the temporary project had no form-submission email notification, so Gmail delivery was not exercised. Production notification wiring is unchanged and was previously verified on 12 July 2026.
- RESOLVED — Mat approved the production replacement; the reviewed site was merged and deployed on 12 July 2026.

Visual receipts were generated locally under `/tmp` and are not committed. One approved synthetic submission was made to the disposable preview only; no merge or production deploy occurred. The independently reviewed feature branch was pushed at `5dfeb5a` before this acceptance note.

## AGE-424 independent review

- PASS — annotated rollback tag `published/full-offer-v1-2026-07-12` resolves to production baseline `f2d2f25` and is pushed.
- PASS — independent desktop (1440px) and mobile (390px) renders showed no horizontal overflow.
- PASS — exactly eight substantive application fields; form name, honeypot and operational hidden fields remain present.
- PASS — privacy wording matches the reduced fields and purpose; form answers remain out of URLs.
- PASS — exactly two internal operational examples, both labelled as non-customer case studies.
- PASS — no £350, paid-diagnostic, fundraising, unavailable-video, training, product/process or fit-call promotion remains.
- CORRECTED — removed user-visible “Local preview only” wording, the timed video-page redirect, inconsistent CTA labels and the stale paid-route reminder.
- RESOLVED — a temporary Netlify Drop project was created with approval, form detection was enabled, and preview form storage passed. The temporary project and its synthetic record remain pending explicitly confirmed deletion.

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

## AGE-424 temporary Netlify acceptance — 12 July 2026

- PASS — temporary preview `phenomenal-marzipan-faf430.netlify.app` served the reviewed reduced-site package without changing `proofsystems.co.uk`.
- PASS — Netlify detected one active form named `proof-systems-qualifier` after form detection was enabled and the package was redeployed.
- PASS — one clearly synthetic founding-cohort application produced the intended `Application received` visitor state.
- PASS — the success state did not add name, email, company, workflow or outcome data to the URL.
- PASS — the temporary Netlify dashboard showed one submission and the correct latest-submission time.
- NOT CONFIGURED — the disposable preview project had no outgoing form email notification; no notification setting was copied from or added to production.
- PENDING CLEAN-UP — delete the synthetic record and temporary project after action-time confirmation. This is irreversible and does not affect the production project.

## AGE-424 credibility revision — 12 July 2026

- PASS — the temporary preview now explains Mat's 16-year progression from operator and managing director to full-time systems, software and AI work since February 2025.
- PASS — four public-safe capability groups cover workforce operations, commercial control, finance/reporting and business development without presenting them as separate Proof Systems offers.
- PASS — two detailed proof examples use systems confirmed as deployed in live internal operations: workforce/labour control and document processing.
- PASS — the copy states that the examples are anonymised internal production systems rather than external customer case studies.
- PASS — no employer name, client/project/supplier details, operational figures, hours-saved claim, screenshots or deployment platform is published.
- PASS — systems still under development or controlled validation are not presented as completed outcomes.
- PASS — revised temporary preview served the new credibility section with no horizontal overflow at the available desktop viewport; responsive rules retain the established one-column mobile layout.
- PASS — `git diff --check` and public-copy safety scans are clean.

## Live production acceptance — 12 July 2026

### AGE-424 founding-cohort release

- PASS — Mat approved the final temporary preview and production promotion.
- PASS — feature branch head `8666119` was merged to `main` at `e1b697b` and pushed to GitHub.
- PASS — the reviewed package was deployed to the existing production Netlify project `bespoke-snickerdoodle-6e4f15`.
- PASS — the live homepage contains the founding proposition and “Since February 2025” credibility wording.
- PASS — live public copy contains no £350, paid-diagnostic or credit-against-build language, no em dash and no old “last 18 months” wording.
- PASS — exactly two detailed operational proof examples remain.
- PASS — rendered sentence boundaries use a non-breaking space followed by a normal space; the checked live boundary resolves to character codes `160, 32`.
- PASS — the live application has eight substantive visitor fields, method POST, form identity `proof-systems-qualifier`, no answers in the URL and no horizontal overflow.
- PASS — the existing production form-notification configuration was left unchanged; its storage and Gmail path was verified earlier on 12 July 2026.
- NOT REPEATED — no additional synthetic application was submitted to production during this release.

### Earlier production acceptance

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
