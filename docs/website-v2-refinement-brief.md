# Proof Systems V2 refinement direction

Build authorised by Mat on 5 September 2026, using Codex agents with task-specific model and effort selection. Scope includes the approved refinement direction and full mobile scroll functionality. Local V2 only; V1 remains the fallback. No push, merge to main or deployment is authorised.

## Intended visitor and outcome

An owner or operator should recognise the gaps around their existing software, understand that Proof Systems works with an ERP, separate tools or a mixture, and see a practical, AI-assisted path from one workflow to a useful system. Construction systems qualify Mat's experience; they do not define the audience.

Simple Gate: PASS

## Accepted direction and latest proposal

- Preserve the approved opening B: original logo geometry and connected nodes settling with the scroll, followed by the words.
- Keep the layered option A. The missing-layer heading must include software or technology. Current proposal: “The software layer that connects your business.”
- Cover an ERP's limits and the gaps between separate tools. Include the cost and complexity reasons some businesses do not adopt a large ERP. Integration can cover either setup or a mixture.
- Explain AI as the reason earlier demonstrations, shorter iterations and a more viable bespoke layer are possible. Do not conflate AI-assisted development with AI processing a client's operational data.
- Remove the confusing date-based homepage illustration. Use a simple source, owner, next-action and history thread.
- Use the dark moving-light treatment for A Practical Starting Point. Replace the sample application card with four process cards: understand the work, try a working demo, refine it together, prove it in use. One card holds, leaves and gives way to the next; a small stage indicator stays visible. Reverse scrolling reverses the sequence.
- The missing connection is absent on entry. Routes draw from the existing systems, meet at the new software layer, then resolve into connected source, ownership and history. Use restrained depth and precise timing, without endless animated particles or a static completed diagram.
- Mobile retains every scroll feature available on the equivalent desktop page. Adapt layout and travel to the available screen; do not replace the experience with a static sequence solely because the viewport is narrow or short. Preserve native touch scrolling and reverse motion. No wheel interception; no repeated logo intro on detail pages.
- Respect the visitor's Reduced Motion preference and retain complete content when JavaScript is unavailable. These accessibility and resilience modes are separate from the normal mobile experience.

## Mobile motion requirement

Mat is reviewing on a mobile phone. The mobile browser is a primary delivery target, including all existing homepage scroll features and the refined sections, plus the effects used on the inner pages.

- Opening: preserve node movement, logo assembly and scroll-revealed words.
- Workflow story: preserve the progressive hand-offs, connecting information and reverse sequence, using a narrow-screen composition without the confusing date example.
- Missing software layer: connections form during native touch scrolling; the software layer and connected outcome arrive in sequence.
- Practical starting point: keep the dark moving-light background, all four entering/leaving cards, readable holds and the visible stage indicator.
- Evidence and supporting pages: retain their shared reveal/transition behaviour, working links and usable media controls. Do not invent additional motion on pages that do not need it.
- Keep content and controls within the visible area. Adjust the composition and scroll distance for portrait, landscape, short screens and browser toolbar changes; do not shrink desktop text until it is unreadable.
- Finger scrolling forwards and backwards must drive the same sequence without gesture capture, hover requirements, forced snapping or a nested scroll trap. Preserve keyboard scrolling and normal links.
- Test phone-sized and tablet-sized layouts, orientation changes and browser toolbar expansion/collapse. Include iOS Safari and Android Chrome where test access is available; distinguish actual-device verification from viewport simulation in the delivery record.
- Check that the phone experience is smooth and stable under ordinary touch scrolling; reduce decorative rendering cost without removing the narrative stages.

Verified implementation gap: `assets/js/site.js` currently sets `story-static` for `(max-width: 900px), (max-height: 760px)`. `assets/css/site.css` also disables the story's sticky layout and connecting thread at these breakpoints. Replace both the JavaScript and CSS mobile/short-screen fallback rules with a responsive animated composition; simply removing one media query will not meet the requirement.

## Click-through audit

The local V2 homepage was followed through all eight stories and their onward enquiry, training and privacy routes in the browser. Source inspection independently confirmed the route graph and compatibility redirects.

| Page | Current finding | Proposed alignment |
| --- | --- | --- |
| `/work/index.html` | Dense two-column product cards, pill view switch, old bevelled blue-and-amber connected-system image. | Editorial evidence rows and a restrained connected-workflow view, with readable names and working links. |
| `/work/sitelog.html` | Heavy title, narrow document layout, film well below the opening. | Shared evidence template; outcome-led hero and early media. |
| `/work/budgetflow.html` | Same legacy story template. | Same evidence template; preserve the cost-allocation and approval explanation. |
| `/work/applications-ledger.html` | Same legacy story template. | Same evidence template; preserve application, certification, payment and retention context. |
| `/work/cpr.html` | Same template. Demonstration interface represents a database/API service. | Same template; retain the distinction between the real service and its demonstration interface. |
| `/work/probables.html` | Same legacy story template. | Same template; retain the pipeline ownership and future-work context. |
| `/work/ledgerlink.html` | Same template. Explicit controls around accounting extraction and AI use. | Same template; retain the exact meaning of those controls. |
| `/work/cashflow.html` | Same template. Source-linked workbook evidence. | Same template; preserve film, captions and source traceability. |
| `/work/management-accounts.html` | Written evidence rather than a film. | Use the same visual family with a written-evidence variant; do not invent a film or performance claim. |
| `/workflow.html` | Older navigation and form surround. | Align the shell and typography; preserve form identity, fields, consent and submission behaviour. |
| `/training.html` | Older navigation and three-card service treatment. | Align the shared shell and editorial layout, keeping training subordinate to the systems proposition. |
| `/privacy.html` | Separate minimal header/footer and document styling. | Align typography, navigation and spacing while preserving approved legal content. |

The header currently changes from The problem / How it works / Experience / About to Selected Systems / AI Team Training / About on the inner pages. Use a consistent navigation hierarchy across the full journey, with local breadcrumbs and back/next links for evidence.

## Related routes to preserve

- Homepage: SiteLog, BudgetFlow, LedgerLink and Explore all selected systems.
- SiteLog → BudgetFlow → Applications Ledger → Cashflow → Management Accounts → connected collection.
- Central Project Register → Applications Ledger; Probables → Cashflow; LedgerLink → Cashflow.
- Story enquiry links → `/workflow.html`; training enquiries keep the `ai-team-training` source; privacy links and return links remain valid.
- Work anchors: `#connect`, `#connected-workflow`, `#individual-systems`, `#finance`.
- Existing compatibility: `/checkout` and `/checkout.html` redirect to the enquiry; `/video-series` and `/video-series.html` redirect home. Preserve their 301 rules and fallback pages.
- Preserve all existing film files, captions, poster identities, synthetic-data disclosures and public URLs. Restyling the website does not imply restyling the applications shown in the films.

## Proposed implementation boundary

One shared inner-page style and one reusable evidence-page structure, with a written-evidence variant for Management Accounts. Apply a restrained reveal treatment to secondary pages; reserve the longer scroll scenes for the homepage. Verify the complete click-through journey, full mobile scroll functionality, keyboard navigation, motion preferences, media and local form validation when the build is authorised.

The illustrative SiteLog layout in `website-connection-process-study.html` previews hierarchy and composition, not every retained paragraph, control or onward link of the final page.


## Build execution

- Baseline: `e6359f60b07116f6a8bf7cf91a1257a9a94b85ea`, branch `codex/website-v2`, existing V2 worktree.
- One implementation owner for shared HTML, CSS and JavaScript; fresh independent review after completion. Read-only audits can run alongside implementation.
- Primary references: approved `website-connection-process-study.html` for connection, process and evidence composition; `website-connected-software-proposals.html` for services and moving-light background. References are stored in the task visualisations directory; do not ship their demonstration controls.
- Completion: all approved scenes built and reversible through native scrolling on desktop, phone and short viewports; all eight evidence stories and supporting routes aligned; existing privacy, form, media and link contracts preserved; repository gates, browser UAT and independent review completed.
- Proof: site, privacy, media, crawl, JavaScript syntax and diff checks; browser forward/reverse scene checks, phone/tablet/landscape layouts, navigation, media controls and local form validation without posting. Distinguish simulated viewport tests from actual-device verification.
- Permission boundary: local code and local commits only. No external messages, form submission, publishing, deployments, merges to main, pushes or Brain writes.
- Escape hatch: report a concrete dependency only after reasonable safe alternatives are exhausted; ordinary styling and responsive choices are implementation decisions.
