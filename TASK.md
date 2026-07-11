# Proof Systems Website Task State

Updated: 2026-07-11

## Current State

- `AGE-341` is in `Agent Review`.
- `AGE-342` is in `Agent Review`.
- The website qualifier and route review are implemented locally.
- Netlify Forms wiring is now present in the local qualifier without any live deploy.
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

1. Start a fresh Codex chat in this repo using `CODEX-BUNDLE.md`.
2. Independently review AGE-341/342 and address the privacy, URL-data, proof and public-copy gaps before any live test.
3. Complete AGE-16 and define the minimum AGE-17 handoff without sending or automating anything.
4. In AGE-343, prepare the approved Netlify preview/live test recipe.
5. Stop for Mat's approval before any deploy, live dummy submission, Gmail notification test or publication.

## Queue

- Immediate:
  `AGE-341`/`AGE-342` independent review and local safety fixes under `AGE-408` acceptance.
- Next:
  `AGE-16` lead response SOP and `AGE-17` minimum CRM handoff.
- Then:
  `AGE-343` approved Netlify/Gmail verification and publish decision.

## Notes

- Other local changes exist in `index.html`, `video-series.html`, `favicon.svg`, and `proof-visual-assets.md`. They were not reverted here.
