# Proof Systems Website Testing

Updated: 2026-07-11

## Checks Run

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

## Not Yet Tested

- Real Netlify submission storage on the live or preview site.
- Real Gmail notification delivery from the current Netlify setup.
- Netlify dashboard export behaviour with actual dummy submissions.
- Whether the notification should go to one inbox or multiple recipients.
- The privacy, URL-data, public-copy and proof-claim fixes listed in `CODEX-BUNDLE.md` have not yet been implemented or tested.

## Close-Out Preparation Check

- `CODEX-BUNDLE.md` exists and routes a fresh Codex chat through the correct Linear issues.
- The prompt prohibits deploy, publish, payment, credentials, live personal data and external messages without approval.
- Existing local website behaviour was not re-tested during this close-out because no website implementation code changed.

## Residual Risk

- The commercial feel may still be slightly heavy if the contact capture feels too long in practice.
- Live notification wiring could still expose an environment-specific quirk that local simulation cannot catch.
