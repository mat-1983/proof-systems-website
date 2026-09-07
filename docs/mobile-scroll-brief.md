# Mobile scroll flow — approved implementation brief

Date: 7 September 2026. Base: `1891e21a21fd0926e38ba61fd41ffbefef6fc668`.
Branch: `codex/website-mobile-flow`. Implementation and independent review use Codex agents, explicitly authorised by Mat instead of Grok. Local review only; no merge, push, deployment, live form submission, Linear or Brain write.

## Outcome

First-time mobile visitors can scroll through the website naturally without interpreting pinned cards as a broken page. Keep the approved premium dark visual language and logo narrative. Every ordinary swipe produces clear content movement or immediate meaningful animation.

Intended user: a prospective SME owner/operator on a phone. Smallest useful change: mobile card sequences become normal document flow over layered moving decoration; the mobile connection diagram travels with the document; the opening retains its animated nodes and appearing words with a substantially shorter journey. Desktop retains its scenes with shorter pauses.

Simple Gate: PASS. Use: scrolling needs no instruction. Explain: swipe to read, with visual depth following the movement. Earn: no extra gesture, control, forced wait or new dependency.

## Approved direction

- Use ordinary vertical document flow for the workflow story and four practical-starting-point cards on phones, including short phone landscape. Do not keep the existing synthetic 4.5-viewport track under new decoration.
- Compact padding, gaps and decorative density, with comfortable body text. Do not force a small fixed height or clip/omit narrative. Where content allows, show a glimpse of the next card. No nested scroller, wheel/touch interception, scroll snapping or mandatory precision landing.
- Give both scenes intentional depth: restrained grid/connection paths, a glow, and a connecting timeline or thread tied to actual scroll. Foreground cards physically travel with native scroll; do not counter-transform them to appear fixed. Avoid distracting autonomous animation.
- Missing software layer: a compact diagram moves through the screen while connections develop; no prolonged mobile sticky hold. Make the complete result readable before it exits. Retain ERP / everyday tools / connecting software / connected-work meaning.
- Opening: retain the approved five-node geometry, nodes forming connections, logo and progressively appearing words. Start visibly responding immediately, shorten travel and remove dead end holds. Do not accelerate so far that text becomes unreadable.
- Desktop: preserve the existing staged visual language, shorten stationary intervals and ensure clear forward/reverse progression. Do not simply rush text past readers.
- Keep all 30-second teaser videos, full films, captions, posters, routes, links, form and privacy contracts unchanged.
- Mobile stage state should track the actual visible card. Decorative scroll cues can remain only where meaningful and clear; remove cues tied to former sticky stages from ordinary flow if they become stranded or misleading.
- Reduced Motion and no JavaScript show complete ordinary-flow content without decorative movement or autoplay. Mode switching, orientation change and resizes must clear obsolete inline transforms/heights/opacities.
- Revise shared CSS/JS asset versions consistently across all public pages to avoid the mixed-cache regression seen previously. Update affected meaningful tests for intended behaviour, retaining all unrelated safety/media/form contracts.

## Completion and proof

Run site, privacy, media, crawl, JavaScript syntax and scroll geometry tests; cumulative diff hygiene. Add/adjust behavioural checks for no mobile artificial scroll runway, no hidden narrative, correct breakpoint switching and no content-countertranslation. Root performs CUA rendering/native scroll tests at 390×844, 320×480, 844×390, 768×1024 and 1440×900, including forward/reverse, short-screen reading, breakpoint changes and visible scroll response. Distinguish viewport simulations from physical touch-device testing.

Commit the coherent local implementation and return exact commit, changed behaviour, tests and limitations. Independent reviewer must return Approved / Changes requested / Blocked on the cumulative change from the base. Return corrections to the same builder/worktree. If a real dependency blocks completion, record it without weakening the outcome.
