# Proof Systems Website Testing

Updated: 2026-08-29

## AGE-600 round 3 approved-derivative presentation — 29 August 2026

Desktop and laptop (900px and above) present optimised WebP derivatives of the six attended references from `assets/img/age-600/`. Master PNGs stay in `docs/design/` and are not linked. Native SVG/HTML is the narrower-viewport fallback. Gap/Fit/Approach headings remain in the DOM with a visually-hidden clip.

- PASS — `python3 site_check.py` including WebP hashes, sub-500KB budget, 1672×941 dimensions in markup, lazy/async, 900px switch, visually-hidden clip, and retained semantic copy.
- PASS — `python3 proof_media_check.py`.
- PASS — `python3 privacy_notice_check.py`.
- PASS — `python3 crawl_check.py` including the six public WebP routes.
- PASS — `node --check` on `assets/js/site.js` and `assets/js/form.js`.
- PASS — in-memory compile of the four checkers.
- PASS — `git diff --check`.
- NOT COMPLETE — live browser overflow at named viewports; Chromium headless previously SIGSEGV in this environment.

## AGE-600 round 3 independent review corrections — 29 August 2026

Rebuilt the six approved scenes as inline isometric/2.5D SVG, removed the About/Start heading caps, and kept films, form, privacy and public-safety copy unchanged. Generator scratch files were discarded and not committed.

### Automated checks

- PASS — `python3 site_check.py` including three-face isometric construction, amber/blue connection strokes, Gap cues, Fit composition, Approach stages, dimensional route pads, connected slabs, heading `max-width: none`, and no 16.8em/14.5em caps.
- PASS — `python3 proof_media_check.py`.
- PASS — `python3 privacy_notice_check.py`.
- PASS — `python3 crawl_check.py`.
- PASS — `node --check` on `assets/js/site.js` and `assets/js/form.js`.
- PASS — in-memory compile of the four checkers.
- PASS — `git diff --check`.
- PASS — local HTTP 200 for homepage, Selected Systems, SiteLog, LedgerLink, enquiry, privacy and training, with isometric scene markup and connected slabs present.

### Browser visual UAT

NOT COMPLETE IN THIS ENVIRONMENT. Google Chrome for Testing headless aborted with SIGSEGV (exit 139). Independent review should compare each scene with the six files in `docs/design/age-600-round-3/` at 1440×900 and 390×844, and confirm no horizontal overflow at 320–360px without relying on `overflow-x` as the layout fix.

## AGE-600 design round 3 — 29 August 2026

Local static implementation of the attended round-three redesign. No preview host, production deploy, form submission or external contact was made.

### Automated checks run in this worktree

- PASS — `python3 site_check.py` including round-3 headings, proof-grid restoration, ERP/no-ERP stack control, connected-workflow relationships, stale-copy absence, design-reference hashes and no raster mock-ups on public pages.
- PASS — `python3 proof_media_check.py` (eight master hashes unchanged).
- PASS — `python3 privacy_notice_check.py`.
- PASS — `python3 crawl_check.py` including homepage, Selected Systems, eight stories, enquiry, privacy, training and local assets.
- PASS — `node --check` on `assets/js/site.js` and `assets/js/form.js`.
- PASS — in-memory Python compile of the four checkers. `python3 -m py_compile` still cannot write `~/Library/Caches/com.apple.python` in this environment.
- PASS — `git diff --check`.
- PASS — local `http.server` on `127.0.0.1:8770` returned HTTP 200 for homepage, Selected Systems, eight stories, enquiry, privacy and training. Response bodies included the round-3 headings, proof-grid, stack control, connected-workflow disclosure and story return links.

### Browser visual UAT

NOT COMPLETE IN THIS ENVIRONMENT. Google Chrome, Brave and Playwright Chromium headless all aborted with SIGSEGV (exit 139) and Crashpad permission errors (`settings.dat: Operation not permitted`). `safaridriver` is installed but not configured (`--enable` would require interactive authentication). Named viewport, keyboard-focus, reduced-motion and no-JavaScript behaviour were therefore inspected from built HTML/CSS/JS and the local HTTP bodies, not from a live layout engine.

Independent review should start `python3 -m http.server 8000 --bind 127.0.0.1` and check:

| Viewport | What to confirm |
| --- | --- |
| 1440×900 | Large opening mark, name then tagline on scroll, ERP/no-ERP stack, cream Gap, ink Fit, proof-grid, sandstone Approach, wider About/Start headings |
| 1280×800 | Same structure without horizontal overflow |
| 1024×768 | Chapters stack cleanly; stack control remains usable |
| 768×1024 | Single-column chapters; Menu not used yet; enquiry CTA visible |
| 500px | Mobile header; no horizontal overflow |
| 390×844 | Native Menu plus Discuss a workflow; radios tappable |
| 360×800 | Same as 390 with the 359px header wrap still unused |
| 320×568 | Header wraps to two rows; no clipped Menu |

Also open `/work/` Individual systems and Connected workflow, `/work/sitelog.html`, `/work/ledgerlink.html`, `/workflow.html` and `/privacy.html`. Tab from the skip link. Enable `prefers-reduced-motion: reduce` and disable JavaScript: opening name/tagline, both stack states, Gap/Fit/Approach stories, posters and the enquiry fields must remain readable. Do not submit the form.

### Not run / not authorised

- No Netlify preview, production deploy, DNS, credential or billing change.
- No production or preview form submission.
- No contact with Pete Mills, Pantera or any prospect.
- No publication of the pending testimonial.

## AGE-600 independent review corrections 3 — 29 August 2026

Reset `.system-map` horizontal figure margins and enlarged tall-map type at the mobile breakpoint so the 360-unit SVG uses wrap width at 320–390px.

## AGE-600 independent review corrections 2 — 29 August 2026

Restyled architecture captions and the tall identity bus so labels do not collide with nodes. Relationships are unchanged. Label colour is `--amber` at 12px.

## AGE-600 independent review corrections 1 — 29 August 2026

Corrected the architecture diagrams, mobile Menu `:focus-visible` treatment, and homepage chapter numbering after `04 / APPROACH`.

## AGE-600 design round 2 — 29 August 2026

Local refinement of the cumulative branch. Canonical brand assets, self-hosted Inter Variable, Selected Systems language, system architecture, economics chapter, larger Proof bands, AI Team Training page, CPR correction and LinkedIn were added. Enquiry identity is unchanged.

- PASS — `python3 site_check.py` including round-2 brand, font hash, training route, CPR name, story navigation and no remote fonts.
- PASS — `python3 proof_media_check.py` (eight master hashes unchanged).
- PASS — `python3 privacy_notice_check.py`.
- PASS — `python3 crawl_check.py` including `/training.html` and local font/brand assets.
- PASS — `node --check` on `assets/js/site.js` and `assets/js/form.js`.
- PASS — in-memory Python compile of the four checkers.
- PASS — `git diff --check`.
- NOT RUN — browser visual UAT of the redesigned header, logo, Proof bands and 320–1440 viewports. Leave that for independent Codex review.

## AGE-600 independent review correction 2 — 29 August 2026

Independent re-review found `scrollWidth` 350px at 320×568 because brand, Discuss a workflow and Menu still shared one nowrap row. Below 360px the header now wraps: Menu stays on the first row with the brand; the enquiry CTA takes a second full-width row. 360px, 390px, tablet and desktop headers are unchanged. Overflow hiding is not the fix. `site_check.py` asserts the 359px wrap strategy.

## AGE-600 independent review correction 1 — 29 August 2026

Independent Codex review found a 415px document width at 390×844 because the mobile header's Menu control overflowed. The 760px header now uses a 100% `.nav-inner` with 16px inset padding, 0.4rem gap, and reduced CTA/Menu padding and type. Menu and Discuss a workflow remain visible. `body { overflow-x: hidden; }` was not used as the fix. `site_check.py` now asserts those mobile header rules.

- PASS — `python3 site_check.py` (including `check_mobile_header`)
- PASS — `python3 proof_media_check.py`
- PASS — `python3 privacy_notice_check.py`
- PASS — `python3 crawl_check.py`
- PASS — `node --check` on `assets/js/site.js` and `assets/js/form.js`
- PASS — in-memory Python compile of the four checkers
- PASS — `git diff --check`
- NOT RUN — no Chrome or other browser viewport measurement in this correction turn, as instructed.

## AGE-600 website repositioning — 29 August 2026

Local static implementation only. No preview host, production deploy, production form submission or external contact was made.

### Automated checks run in this worktree

- PASS — `python3 site_check.py`: eight story routes, five-field `proof-systems-qualifier` enquiry, omitted client-perspective chapter, poster-first homepage teasers, no full films on the homepage, and public-copy rejection of founding-cohort, Pantera, Pete Mills, Xonetic and YouTube wording.
- PASS — `python3 proof_media_check.py`: eight H.264 1280×720 masters with exact required SHA-256 hashes, posters, English WebVTT files, and 5-second homepage teasers under 400KB. Existing SiteLog and BudgetFlow master/poster hashes were unchanged.
- PASS — `python3 privacy_notice_check.py`: general-enquiry field list, B2B lawful-basis wording, transfer mechanisms, retention and ICO link. Founding-diagnostic application copy is absent.
- PASS — `python3 crawl_check.py`: HTTP 200 for homepage, Work, eight stories, enquiry, privacy, legacy checkout/video-series pages and shared assets. Homepage HTML declared three teasers and did not reference the eight full films.
- PASS — `node --check assets/js/site.js` and `node --check assets/js/form.js`.
- PASS — in-memory Python compile of `site_check.py`, `proof_media_check.py`, `privacy_notice_check.py` and `crawl_check.py`. `python3 -m py_compile` could not write a cache directory in this environment (`PermissionError` under `~/Library/Caches/com.apple.python`).
- PASS — `git diff --check`.

### Media probes

ffprobe on each master: H.264, 1280×720, no audio stream. Durations matched the design review within 0.2s. Sampled frames showed synthetic Northstar labels and local demonstration chrome only.

### Performance / lazy media

- Homepage markup contains posters and `data-teaser-src` attributes only. Full `*-demo.mp4` files are not present in `index.html`.
- `assets/js/site.js` injects a muted looping teaser only when the card is intersecting, JavaScript runs, and `prefers-reduced-motion: reduce` is false.
- Story films use `preload="none"`, native `controls`, and no `autoplay` or `loop`.
- This is a static/HTML/JS proof, not a browser network-panel measurement.

### Browser visual UAT

NOT RUN HERE. Google Chrome headless (`--headless=new`) aborted with SIGSEGV (exit 139) after `--user-data-dir` was supplied. No screenshots or interactive keyboard pass were captured. Independent Codex review should run the viewport, keyboard, reduced-motion and no-JavaScript checks locally.

### Responsive UAT instructions for independent review

Start a local server from the worktree:

```
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/` and check these viewports:

| Viewport | What to confirm |
| --- | --- |
| 1440×900 | Large editorial headline, two-column hero, sticky gap visual, three proof cards, compact nav after the first viewport |
| 1280×720 | Same structure without horizontal overflow; body copy remains readable |
| 768×1024 | Single-column chapters; SVG remains in its connected/readable state; enquiry CTA stays visible |
| 390×844 | Native menu button plus visible Discuss a workflow; one-column cards; no horizontal overflow |

Repeat Work (`/work/`), one capture story (`/work/sitelog.html`), LedgerLink (`/work/ledgerlink.html`), enquiry (`/workflow.html`) and privacy (`/privacy.html`) at 1440×900 and 390×844.

### Keyboard, reduced-motion and no-JavaScript checks

- Tab from the skip link through nav, CTAs, form fields and film controls. Focus rings are `outline: 2px solid #F2A65A`.
- Enable `prefers-reduced-motion: reduce`. The workflow SVG must already show the connected state; teasers must not load or play.
- Disable JavaScript. Homepage posters, copy, story films (native controls), enquiry fields and privacy copy must remain readable. The checkbox menu still opens. Local form POST is not intercepted; published JS keeps answers out of the URL.

### Not run / not authorised

- No Netlify preview, production deploy, DNS, credential or billing change.
- No production or preview form submission.
- No contact with Pete Mills, Pantera or any prospect.
- No publication of the pending testimonial.

---

## Earlier records

The sections below are historical evidence from AGE-590, AGE-505 and AGE-424. They describe the previous founding-cohort site and are not the current public contract.

## AGE-590 SiteLog and BudgetFlow proof videos — 28 August 2026

- PASS — `index.html` operational-proof section contains exactly two cards titled SiteLog and BudgetFlow.
- PASS — both cards show visible `Synthetic demonstration` labelling before the native video player.
- PASS — each video uses `controls`, `playsinline`, `preload="metadata"`, the committed poster, a local MP4 source and an English `kind="captions"` track. Autoplay and loop are absent. No homepage JavaScript was added.
- PASS — `python3 proof_media_check.py` confirms exact-case local media paths, caption tracks, committed MP4/poster SHA-256 hashes, the two-system relationship sentence, founding CTAs to `workflow.html`, and unchanged `proof-systems-qualifier` form identity.
- PASS — `python3 privacy_notice_check.py` and `git diff --check` are clean. `workflow.html`, `privacy.html` and `assets/demo-media/` are unchanged.
- PASS — a local loopback server returned HTTP 200 for homepage, application, privacy and all six committed SiteLog/BudgetFlow media files; response bodies matched the worktree files.
- NOT RUN HERE — Chromium, Brave and Playwright headless browsers aborted in this sandbox (SIGSEGV / crashpad permission). Desktop 1440 and mobile 390 visual UAT, native control interaction and caption overlay rendering remain for the reviewer.
- NOT RUN — no Netlify preview, form submission, upload, deployment or production change was made.

## AGE-505 wide-screen responsive layout — 20 July 2026

- PASS — the homepage headline uses three lines at 760, 1,024, 1,366 and 1,440 px rather than retaining the former four-line narrow composition.
- PASS — the homepage expands to a 1,320 px composition from 1,500 px and a 1,480 px composition from 2,400 px.
- PASS — the headline uses two lines at 1,500, 1,920, 2,560 and 3,440 px; paragraph widths remain capped at 840–900 px.
- PASS — no horizontal overflow at 390, 760, 1,024, 1,366, 1,440, 1,499, 1,500, 1,920, 2,560 or 3,440 px.
- CORRECTED — the legacy checkout notice previously measured 424 px at a 390 px viewport because padding sat outside its declared width; border-box sizing now produces a 350 px card with 20 px side margins.
- PASS — homepage, application, privacy, checkout and video holding routes have no horizontal overflow at 390 or 1,920 px.
- PASS — all five HTML files parse, all local links resolve and every public route returns HTTP 200 from the local server.
- PASS — application JavaScript passes `node --check`; the `proof-systems-qualifier` form identity and Netlify marker are unchanged.
- PASS — `git diff --check` is clean.
- NOT RUN — no Netlify preview, form submission, notification test, deployment or production change was made; Mat will add the reviewed local folder to Netlify.

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
- RESOLVED — a temporary Netlify Drop project was created with approval, form detection was enabled, and preview form storage passed. The temporary project and its synthetic record were permanently deleted after explicit confirmation.

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
- PASS — the synthetic record and temporary project were permanently deleted after action-time confirmation. The production project was unaffected.

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

## Final homepage refinement — 13 July 2026

- PASS — removed only the note stating that newer finance and commercial systems remained under development and validation.
- PASS — `git diff --check` is clean and the removed wording is absent from the deployment package.
- PASS — Mat deployed the updated seven-file package to the existing production Netlify project.
- PASS — the live homepage still contains the two approved operational proof cards and no longer contains the removed note.
- PASS — the live homepage, application, privacy, checkout and video holding routes respond successfully.
- NOT REPEATED — no form submission or notification test was needed because the form and application code did not change.

## Lead handoff documentation verification — 12 July 2026

- PASS — `crm-handoff.md` maps Netlify submissions into the restricted Notion identity register and the pseudonymous AGE-421 commercial register without duplicating Linear.
- PASS — all five live route/state pairs match `workflow.html` exactly.
- PASS — duplicate prevention, one-owner/one-next-action rules, next-working-day review, 3/7-working-day follow-ups and overdue/deferred controls are explicit.
- PASS — `lead-response-sop.md` separates website contact permission from recording and AI-processing consent.
- PASS — synthetic test instructions require removal of test records and prohibit live submission without separate approval.
- PASS — `git diff --check` is clean.
