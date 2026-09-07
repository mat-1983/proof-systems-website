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

## Review receipt

Implementation: `562d00dc7d2c898664a6d3bbda1b93e46c453acc`. Independent cumulative verdict: **Approved**, with no actionable findings. Builder and independent reviewer were each assigned Astra / high; Mat explicitly authorised Codex agents instead of Grok.

Independent site, privacy, media, HTTP crawl, both JavaScript syntax checks, executable scroll geometry and cumulative diff checks passed. Public markup changes only update shared asset versions; narrative, media, form, privacy and route contracts remain intact.

Root rendered verification:

- At 390 × 844, the process scene reduced from 4,575px to 1,427px. A native 380px scroll moved the first card from top 417.92px to 37.92px, exactly following input. All story and process cards remain readable, with the following card visible where space permits. Reverse scrolling returns to the same positions.
- At 320 × 480, the opening completes over 192px of travel, with all words visible and the final line ending at 376.8px. Longer cards are read in ordinary flow; the complete second record and final process outcome can be reached without clipping or a fixed hold.
- At 844 × 390, a native 195px scroll moves the card 195px. The four process cards occupy a 910px track. The mobile software diagram travels with the document while connections draw and reverse. At 320 × 480 its result is readable before it exits.
- At 1440 × 900 and 768 × 1024, the shorter desktop sequences retain readable cards, stage indicators and clear cues. Switching an active desktop stage to phone width clears former scene heights and transforms; returning to tablet reinstates the desktop layout.
- An additional 1280 × 320 desktop check covers the overflow reading phase. A 271px story card has a 122px visible area; its record top, complete heading and explanation, then final record fields can all be read across the retained 149px pan. Reverse scrolling is stable.
- Reduced Motion and no-JavaScript browser fixtures at 390 × 844 show all eight cards at full opacity in ordinary flow, with cues hidden and no teaser autoplay. These are explicit simulations, not operating-system preference or physical touch-device tests. Executable tests additionally cover preference changes after motion has begun.
- No horizontal overflow or current browser console warning/error was found in the tested views.

A separate allow-listed public package passed an HTTP crawl and byte comparison against the reviewed source. Review URLs: `http://127.0.0.1:8989/index.html` on this Mac and `http://192.168.0.18:8989/index.html` from a phone on the same Wi-Fi while the Mac remains awake. The existing V2 preview and dated Netlify upload folder remain unchanged.

Simple Gate: PASS. Next action: Mat reviews the native phone experience, especially whether a first-time visitor continues without explanation. Physical visitor validation remains a human acceptance step. No merge, push, deployment, form submission or memory write occurred.
