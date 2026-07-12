# Proof Systems Website Task State

Updated: 2026-07-12

## Current State

- `AGE-341` is in `Agent Review`.
- `AGE-342` is in `Agent Review`.
- The website qualifier and route review are implemented locally and independently reviewed under `AGE-408`.
- Netlify Forms wiring is now present in the local qualifier without any live deploy.
- Sensitive workflow/contact answers no longer appear in route-review URLs; temporary same-session storage supplies the local review page.
- Submission/consent copy now states that the website action sends the enquiry.
- A proportionate privacy notice, response SOP, minimum CRM handoff and gated Netlify test recipe now exist.
- The unsupported 4,400+ hours claim was removed; empty video routes are honestly labelled as planned guides.
- A fully synthetic proof visual and safety register were created for `AGE-344`.
- The Growth Engine has been cleaned up and launch acceptance is now tracked by `AGE-408`.
- A complete safe publish-preparation starter prompt is available in `CODEX-BUNDLE.md`.

## What Changed This Session

- `workflow.html`
  Added progressive lead capture, route states, call/training guardrails, and Netlify Forms-compatible submission fields.
- `checkout.html`
  Converted the old payment-first handoff into a route-aware review page.
- `40_knowledge/proof-systems/website-funnel/lead-capture-backend-recommendation.md`
  Locked Netlify Forms as the V1 backend direction because the old site is already on Netlify and wired to Gmail.

## Next Steps

1. [x] Mat reviewed the commercial tone, privacy wording and synthetic proof visual.
2. [x] Mat chose live deployment and confirmed the notification inbox.
3. [x] Ran `netlify-test-recipe.md` with synthetic data and recorded storage/Gmail evidence for `AGE-343`.
4. Keep `AGE-341` and `AGE-342` in Agent Review; AGE-343 live-path acceptance is complete.

## Live Result

The reviewed website is live at `proofsystems.co.uk`. Netlify form detection is enabled, `proof-systems-qualifier` is registered, and the approved inbox receives form notifications. One synthetic diagnostic enquiry passed browser success, stored-schema and email-delivery checks; its Netlify record and email were then deleted. The accidental temporary Netlify project created during upload was permanently deleted.

The V1 manual lead handoff is also complete: Netlify → restricted Notion identity record → pseudonymous AGE-421 workbook row, with five exact route mappings, one owner/next action/due date, duplicate prevention and stalled-lead controls.

## Queue

- Immediate:
  `AGE-341`/`AGE-342` independent review and local safety fixes under `AGE-408` acceptance.
- Next:
  `AGE-16` lead response SOP and `AGE-17` minimum CRM handoff.
- Then:
  `AGE-343` approved Netlify/Gmail verification and publish decision.

## Notes

- Other local changes exist in `index.html`, `video-series.html`, `favicon.svg`, and `proof-visual-assets.md`. They were not reverted here.
