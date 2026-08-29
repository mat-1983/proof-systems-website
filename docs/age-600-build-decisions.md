# AGE-600 build decisions

Append-only log of material implementation choices. Routine edits are not recorded.

## 2026-08-29 — Omit chapter 05

The approved design keeps the Pantera quotation unpublished until exact approval is recorded. The homepage therefore uses chapters 00, 01, 02, 03, 04, 06 and 07, and public HTML contains no client-perspective chapter, quotation or attribution. Publication of that chapter remains blocked.

## 2026-08-29 — Work URL scheme

Selected systems live at `work/index.html` and `work/{slug}.html`. Those paths are the stable public story routes. Existing `/workflow` remains the enquiry form. `/checkout` is a noindex redirect to the enquiry form. `/video-series` is a noindex redirect to the homepage. Netlify `_redirects` and HTML fallback pages are both present so the change is hostable without Netlify.

## 2026-08-29 — Homepage teasers are not the masters

Homepage proof uses posters first. JavaScript may lazy-load a 5-second muted teaser only when the card is visible and motion is allowed. Full `*-demo.mp4` files are referenced only on story pages, with native controls and `preload="none"`. Reduced-motion and no-JavaScript states keep the poster.

## 2026-08-29 — Contract Performance Reporting public name

The CPR film title card says Central Project Register. Public pages use the approved name Contract Performance Reporting and describe the film as a portfolio overview with project-level drill-down. The story page notes that the demonstration uses a Central Project Register to hold identity and terms.

## 2026-08-29 — Story copy derived from films and design outcomes

The design review supplies audience, outcome and film identity, not word-for-word story body copy. Problem, users, flow, design-choice and relationship copy was written from those outcomes and from sampled frames of the synthetic films. No client result or unverified performance claim was added.

## 2026-08-29 — Shared static assets

CSS and JavaScript live in `assets/css/site.css`, `assets/js/site.js` and `assets/js/form.js`. The site has no framework, WebGL, scroll hijacking, cursor replacement or intro loader. The default CSS `--progress: 1` keeps the workflow diagram readable without JavaScript.

## 2026-08-29 — Mobile header fits 390px without overflow hiding

The 390px overflow came from nowrap brand, enquiry CTA and Menu items plus a 1.25rem flex gap exceeding the wrapped nav width. Below 760px the bar is `width: 100%` with 16px padding and a 0.4rem gap, and the CTA/Menu type is reduced. Desktop and tablet headers are unchanged. Overflow hiding is not the fix.

## 2026-08-29 — Enquiry field reduction

The Netlify form name `proof-systems-qualifier`, honeypot, POST behaviour and notification path are unchanged. Visible fields are name, business email, company, workflow description and contact consent. Hidden values are `route_key=general-enquiry`, `route_label=Discuss a workflow`, `lead_state=enquiry-received` and `page_source=workflow.html`.
