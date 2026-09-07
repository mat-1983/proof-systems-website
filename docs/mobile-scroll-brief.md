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

## Approved visual and pacing refinement

Mat accepted the functional phone flow and requested stronger depth and clearer movement on 7 September. Continue on this branch from `ccf5c511886e511d23bd3270f3b441fc00f22ef1`, using the same Codex builder and independent reviewer. The scope is Follow One Piece of Work and A Practical Starting Point; preserve the opening and software connection scene.

- Practical Starting Point: place an oversized, cropped outline of the existing five-node mark behind the cards, with unmistakable diagonal movement tied to scrolling and stronger amber light catching nodes. Give foreground cards convincing shadows and edge highlights while keeping the text quiet and readable.
- Follow One Piece of Work: use related large nodes and connecting routes behind the records, with an amber highlight progressing along the route. Relate both scenes through the brand without repeating an identical watermark.
- Phone cards must continue to move exactly with native scrolling. Use a slower decorative background for depth and soften repetitive outer borders, particularly the nested story card framing. Do not restore phone pinning, artificial runway or content counter-translation.
- Desktop: shorten the actual stationary interval as well as the overall track. Cap normal reading travel so taller monitors do not create longer pauses. Retain sufficient travel for genuinely overflowing content on short desktop screens; transitions and reverse scrolling must remain smooth and readable.
- Motion must visibly respond to real scrolling, with no autonomous logo animation, excessive bloom, scroll interception, added dependency or raster replacement of the brand geometry. Keep complete ordinary-flow Reduced Motion and no-JavaScript fallbacks.
- Preserve all narrative, media, forms, privacy and routes. Bump the shared asset version consistently. Extend meaningful geometry tests for bounded desktop travel and visible decorative progress, including mode cleanup.

Simple Gate: PASS. Intended user: a prospective business owner on phone or desktop. Required outcome: an obviously responsive, premium narrative that remains effortless to read. Smallest useful change: improve the two existing scene backdrops, foreground treatment and pacing without adding a new interaction.

Root will render the actual reported 1493 × 1146 desktop size, normal desktop and compact phone views, check native foreground versus background movement, and review contrast, overflow, forward/reverse scrolling and fallback behaviour. The independent reviewer will assess the cumulative application change against `1891e21`. Refresh the existing allow-listed phone preview only after validation. Main, the previous Netlify package and public deployment remain unchanged.

## Visual refinement review receipt

Final application head: `6f7bbf3a3293850d8914c592a3b58c987947f0b2`, following the main refinement at `cc9bd75a5bca93a8979ba9446165f82e93119d01`. Independent cumulative verdict against `1891e21`: **Approved**, no actionable findings. Implementation and independent review used the same separate Astra / high agents, under Mat's explicit Codex-agent instruction.

Both scenes now have large, scroll-linked SVG backgrounds: the existing five-node mark behind process cards, and a distinct branching route behind the workflow records. Mobile story outer framing is removed; foreground surfaces, amber lighting and local feathered text protection establish depth. Desktop normal travel is bounded at 1,680px, with a maximum 210px fully stationary middle-card interval. Genuine overflow retains its separate reading allowance. Card handovers use sequential fades, preventing double-exposed copy.

All required site, privacy, media, crawl, JavaScript syntax, production geometry and cumulative diff gates passed. The final CSS contrast correction was independently checked with the relevant gates; unrelated media and form contracts are unchanged. Tests sample desktop card states across the travel, including taller monitors, one visible panel during handover, bounded low-opacity transition distance, overflow reading, reversible decorative progress and mode cleanup.

Root CUA rendered verification:

- At 390 × 844, a native 380px scroll moved the first process card from 417.52px to 37.52px. A subsequent 304px scroll moved the card another 304px while the background moved 46.12px vertically and 35.87px horizontally. Reverse scrolling restored the exact previous state. All eight cards remained in ordinary flow, with no horizontal overflow.
- At 320 × 480, all four process outcomes were reachable without clipping; the longer story's two records and final fields remained readable. At 844 × 390, process cards were 204px tall, with full outcomes and the following card visible through native scrolling.
- At the reported 1493 × 1146 desktop size, story and process travel each reduced from 3,438px to 1,680px. Full cards and the large moving mark were clearly visible. The transition at progress 0.2626 was rechecked after correction: outgoing opacity 0, incoming opacity 0.626554, all others 0; no overlapping copy.
- At 1440 × 900, story travel was 1,512px. The route remained clearly visible while the final feathered scrim protected the heading where a node crossed behind it. Final 390px rendering also confirmed the former rectangular text background was removed.
- At 1280 × 320, the longer story card retained a 149px reading pan within a 122px visible area. At progress 0.3776, its complete heading occupied 149–178px and its explanation 184–224px; at 0.4291 the final record fields were visible. Reverse scrolling returned to the exact prior reading state. Switching the active scene into phone landscape cleared desktop geometry and transforms.
- Explicit Reduced Motion and no-JavaScript fixtures at 390 × 844 retained all eight panels at opacity 1, in ordinary flow, with no transforms or autoplay. Decorative windows were static. These are browser simulations, not physical-device or operating-system preference tests. No browser warning or error was found in the final QA tab.

The existing same-Wi-Fi preview was refreshed from an allow-listed 60-file, 56.1MB public package. Every public file matches the reviewed source byte for byte; an HTTP crawl checked 55 routes/assets. Private tooling, documentation, source masters and withdrawn media return 404. Shared asset version: `brand-depth-contrast-20260907`.

Review on this Mac: `http://127.0.0.1:8989/index.html`. Phone: `http://192.168.0.18:8989/index.html`, on the same Wi-Fi while this Mac remains awake. Canonical main remains clean at `1891e21`; the dated Netlify V2 folder remains unchanged. No merge, push, deployment, external tracking update, form submission or Brain write occurred.

Simple Gate: PASS. Next action: Mat reviews the refined appearance and pacing on his phone. Physical touch-device acceptance remains with Mat.
