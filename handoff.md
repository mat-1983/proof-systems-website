# Proof Systems Website Handoff

Updated: 2026-07-11

## Resume Here

Start with `CODEX-BUNDLE.md`; continue under launch acceptance issue `AGE-408`.

The next agent should:

1. Independently review `AGE-341` and `AGE-342`, keeping them in review posture unless Mat's review has actually occurred.
2. Use the local qualifier flow as the source of truth:
   [workflow.html](/Users/matglendenning/Developer/proof-systems/60_products/proofsystems-website/workflow.html)
3. Use the backend decision note as the backend source of truth:
   [lead-capture-backend-recommendation.md](/Users/matglendenning/Developer/proof-systems/40_knowledge/proof-systems/website-funnel/lead-capture-backend-recommendation.md)
4. Resolve the identified local privacy, URL-data, proof and public-copy risks before requesting approval for the actual Netlify test.
5. When approved, test the actual Netlify path with safe dummy submissions.

## Current Decisions

- Proof Systems is SME-first, with construction as proof rather than market boundary.
- The funnel is:
  diagnostic request, video-first, product/process, 15-minute fit call, training enquiry.
- Netlify Forms is the V1 backend because the old website is already on Netlify and wired to Gmail.
- Local qualification should still work without submitting anything when opened as a local file.

## Open Decisions

- Which notification email address should receive Netlify form alerts.
- Whether the first live test should happen on a Netlify deploy preview or the existing live site.
- Whether any copy should be softened if Mat feels the qualifier is still too heavy.

## Follow-On Issues

- `AGE-343`
  Prepare the website for publish and confirm real Netlify/Gmail behaviour.
- `AGE-16`
  Build the lead response SOP and templates.
- `AGE-17`
  Set up CRM handoff from lead to booked call.
- `AGE-408`
  Launch acceptance umbrella for the minimum safe lead and response path.
