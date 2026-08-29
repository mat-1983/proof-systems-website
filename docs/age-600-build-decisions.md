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

## 2026-08-29 — Map captions and tall identity bus

Wide-map captions sit in dedicated lanes below their connectors so they do not cross node borders. The tall map uses a dashed identity bus with side-gutter branches to Applications Ledger and Probables, and a legend instead of on-path captions. Connector labels use `--amber` at 12px.

## 2026-08-29 — Architecture diagram uses identity grouping

The connected-system visual now groups Central Project Register as a shared identity bus into SiteLog, BudgetFlow, Applications Ledger and Probables, distinct from transactional arrows: weekly labour cost, payment export to accounts software, accounts extraction into LedgerLink, and checked local processing into both Cashflow and Management Accounts. The homepage map is full-width for 1280px legibility. Mobile uses a grouped tall layout rather than a single sequence.

## 2026-08-29 — Unpublished chapters numbered consecutively

With the testimonial unpublished, Operator First is `05` and Start is `06`, immediately after `04 / APPROACH`. No Pantera copy was added.

## 2026-08-29 — Round 2 brand reveal fallback

The header always shows the compact canonical icon so navigation is never a barrier. The first viewport shows the full logo and one positioning line. JavaScript only compactifies the header after the opening leaves view. Reduced motion and no-JavaScript keep both the opening and the proposition visible, with no scale, timer or scroll hijack.

## 2026-08-29 — Inter Variable provenance

Self-hosted `assets/fonts/InterVariable.woff2` is official Inter v4.1, SIL OFL 1.1, SHA-256 `693b77d4f32ee9b8bfc995589b5fad5e99adf2832738661f5402f9978429a8e3`. Licence file SHA-256 `262481e844521b326f5ecd053e59b98c8b2da78c8ee1bdbb6e8174305e54935a`. Weights used are 400, 600 and 700. No remote font is loaded.

## 2026-08-29 — System-map relationship evidence

The architecture diagram only shows relationships visible in the approved films and design review: CPR as project-identity master; SiteLog weekly labour cost into BudgetFlow; BudgetFlow payment export; accounts software to LedgerLink; LedgerLink plus verified live inputs into deterministic local processing for Cashflow and Management Accounts. Suggested story-to-story links are labelled Suggested next and are not described as direct data dependencies unless that evidence exists.

## 2026-08-29 — CPR public name correction

The earlier decision to publish Contract Performance Reporting is superseded. Public wording is Central Project Register. The master film is unchanged.

## 2026-08-29 — Narrow-mobile navigation with compact mark

The 320px wrap (brand and Menu on row one, enquiry CTA on row two) is retained. The persistent header now uses the compact canonical icon rather than the wordmark, which keeps that wrap valid.

## 2026-08-29 — Training interest source

Ask about team training reuses `workflow.html` with `?interest=ai-team-training`. `form.js` copies that exact value into hidden `interest_source` and strips the query so visitor answers are not kept in the URL. `route_key` remains `general-enquiry`.

## 2026-08-29 — 320px header wraps onto two rows

Independent review found 350px overflow at 320px while 360px still fitted. Below 360px the header wraps: brand and Menu stay on the first row, and Discuss a workflow moves to a full-width second row. 360px and wider keep the single-row mobile bar.

## 2026-08-29 — Mobile header fits 390px without overflow hiding

The 390px overflow came from nowrap brand, enquiry CTA and Menu items plus a 1.25rem flex gap exceeding the wrapped nav width. Below 760px the bar is `width: 100%` with 16px padding and a 0.4rem gap, and the CTA/Menu type is reduced. Desktop and tablet headers are unchanged. Overflow hiding is not the fix.

## 2026-08-29 — Enquiry field reduction

The Netlify form name `proof-systems-qualifier`, honeypot, POST behaviour and notification path are unchanged. Visible fields are name, business email, company, workflow description and contact consent. Hidden values are `route_key=general-enquiry`, `route_label=Discuss a workflow`, `lead_state=enquiry-received` and `page_source=workflow.html`.
