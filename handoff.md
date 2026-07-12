# Proof Systems Website Handoff

Updated: 2026-07-12

## Resume here

Continue under `AGE-424` from branch `agent/mac-mini/age-424-reduced-founding-cohort-site`.

The branch reduces the broad live consultancy site to the bounded founding-cohort proposition. It is pushed at `5dfeb5a`; a disposable Netlify preview and one synthetic submission have now passed, but no merge or production change has occurred.

The implementation, independent review and temporary Netlify form-storage test are complete. The temporary project `phenomenal-marzipan-faf430` detected the correct form, displayed the intended success state and stored one safe synthetic application without putting answers in the URL. The disposable project had no email notification configured, so that part was not repeated; the production notification flow was previously verified on 12 July 2026. Delete the temporary record and project only after action-time confirmation, then obtain explicit production approval before merge/deploy.

## Source of truth

- Full published baseline: annotated tag `published/full-offer-v1-2026-07-12` at `f2d2f25`.
- Reduced homepage: `index.html`.
- Reduced application and Netlify schema: `workflow.html`.
- Privacy wording: `privacy.html`.
- Manual response and handoff: `lead-response-sop.md` and `crm-handoff.md`.
- Preview acceptance: `netlify-test-recipe.md`.

## Current proposition

Proof Systems is recruiting four SMEs for a free, bounded workflow diagnostic. Each engagement covers one recurring workflow, a diagnostic conversation, written findings and a recommended next step. It does not promise implementation, software, a cohort place or paid work.

## Safety and approval

Do not deploy, merge an auto-deploying branch, contact prospects or change production Netlify settings without the applicable explicit approval. The next external gates are irreversible temporary-preview clean-up and, separately, Mat's production approval.

## Rollback

The old site can be reconstructed exactly from `published/full-offer-v1-2026-07-12`. Prefer reverting the reduced merge or deploying a checkout of the tag; do not move the tag.
