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

## Approved narrative and selective mobile revision — 8 September

Mat reviewed six points, discussed the proposals, and approved the recommendations with his own Codex subagents. Continue on this branch from `049fbea`. This supersedes the earlier blanket requirement that every mobile scene use ordinary flow: the workflow story stays in flow, while suitable connection and process scenes regain short staged behaviour. Local review only; preserve canonical main, the previous Netlify package and public deployment.

Intended user: a business owner who need not understand software acronyms. Required outcome: a coherent journey from disconnected information to a focused connection and credible examples, with clear scroll feedback on phone and desktop. Smallest useful change: revise existing scenes, copy and evidence relationships without adding another large scroll section or changing the opening. Simple Gate: PASS.

1. Missing Software Layer: keep its headline and short introductory sentence visible with the desktop connection animation. Give the long explanatory paragraph its own ordinary-flow position; it must not consume the pinned scene. Restore the earlier mobile connections drawing into place while the scene briefly stays visible, with continuous meaningful response and no long idle tail. Use ordinary flow when the complete scene cannot fit comfortably on a short screen. Keep full readable Reduced Motion/no-JavaScript content.
2. Desktop workflow story: remove the visibly clipped rectangular scrim behind the left-hand explanation. Use a broad smooth darkening across the scene's left side and arrange the strongest background nodes away from the copy. No local panel edge around the text. Preserve the accepted mobile story composition and native scrolling.
3. Mobile Practical Starting Point: trial smaller cards that briefly stay in one place as 01–04 advance, with the moving logo, a clear compact stage indicator and short responsive transitions. Retain ordinary-flow fallback when a card plus navigation, indicator and cue cannot fit. No nested scroller, scroll interception or long fixed holds. Mobile story cards must continue to move exactly with the swipe. Mode changes must clear obsolete sizing, opacity, transforms and decoration state.
4. Keep all four workflow-story stages about the disconnected problem. Replace the current unexplained connected outcome with 'Someone pieces it back together.' Suggested body: 'The work moves forward. Checking what happened still means searching across emails, spreadsheets and separate records.' The sample record must remain visibly fragmented rather than presenting an already repaired record. Stage labels, styling, explanatory text and any related checks must agree. Make the background routes interrupted in this problem scene; complete connections belong in the following solution section. Retain the general business example and synthetic-data disclosure.
5. Explain setups in ordinary language: 'One main business system' and 'Several everyday tools'. Suggested supporting copy: 'You might run most of the business through one main system, use separate apps and spreadsheets, or combine both. I build the connections around how your business actually works.' Keep the idea that rigid or costly software leaves gaps whether the business uses a main platform, separate tools or both. ERP can be a supporting example, not a required acronym in prominent copy. Review the related homepage service wording for consistency. Preserve the AI economics message.
6. Show evidence as an evolving connection to existing business processes, with a compact sequence alongside the demonstrations, not another prolonged staged section. First: SiteLog fed existing cost-control and payment processes. Later: BudgetFlow extended the workflow between SiteLog and existing accounting software. Mat confirmed the current data path: a weekly scheduled API extraction brings SiteLog records into BudgetFlow; managers allocate costs; a BudgetFlow export is produced at a set point each week for import into accounting software. Only the extraction is confirmed automated. Do not claim automatic accounting sync, real-time/two-way integration or fully automated export/import. Use clear connector labels such as 'Weekly automatic transfer', 'Managers allocate costs', and 'Weekly export → accounts import'. Align SiteLog, BudgetFlow and the selected-systems overview pages with this history and mechanism. Keep construction as qualifying evidence for the wider business proposition.

Preserve the opening logo/words, seven full synthetic films, three 30-second teasers, posters/captions/source-master hashes, legal/privacy/form behaviour, routes and existing links. Avoid customer names or new client claims. Bump shared asset versions consistently across every public page and affected checks. No form submissions, external messages, Brain or Linear writes, push, merge or deployment.

Completion predicate: the agreed narrative and six changes are present and coherent; eligible mobile connection/process scenes visibly respond to scrolling; mobile story and short-screen fallbacks remain readable in normal flow; desktop title remains with the connection scene and has no clipped text scrim. Every factual integration claim matches Mat's description.

Proof: run site, privacy, media, crawl, both JavaScript syntax, production scroll geometry and cumulative diff checks. Extend meaningful behavioural checks for per-scene mobile eligibility, short-screen fallback, complete narration, responsive/motion-mode cleanup and copy/integration contracts; do not retain tests that enforce superseded blanket mobile flow. Root alone operates CUA and preview servers for phone/desktop rendering, transitions, forward/reverse movement, title visibility, short-screen reading, fallback fixtures and selected-system navigation. Independent Astra reviewer gives a cumulative verdict against `1891e21` after the exact new application head is committed. Return corrections to the same builder and branch. If blocked, report concrete evidence without weakening the outcome or silently publishing.

### Review delivery — 8 September

Implemented through `657f25fba8c9821fe1de1cf754bf1822ee56646b` on `codex/website-mobile-flow`. Independent Astra cumulative review against canonical `1891e21`: **Approved**, no actionable findings. Independent site, privacy, exact media/master hashes, HTTP crawl, both JavaScript syntax, production scroll geometry and cumulative diff checks passed. The six approved changes are present. The opening, full films and 30-second teasers, forms, legal content and routes are preserved.

Root browser evidence:

- At 1440 × 900, the balanced connection heading and introductory sentence stay with the diagram through its final outcome. Connection travel is 800px; normal desktop story/process travel remains 1,512px. Story stages 03 and 04 have smooth broad darkening without the former boxed text backdrop; the final record and interrupted routes consistently describe disconnected work.
- At 390 × 844, the story stays in ordinary flow, the connection scene uses 590.8px travel and process uses 911.52px across four cards. A 186px connection swipe visibly draws the lines while the heading stays in place; reversing restores the same line positions. A 152px process swipe advances 01 to 02 and moves the background about 47px horizontally and 60px vertically. Settled cards, stage labels and the down cue remain readable.
- Rendered QA caught two background edges: insufficient glow overscan and a mobile sticky offset retained in the staged window. Both were corrected. The final mobile backdrop fills exactly the stage from y=67 to y=844, with no hard band, and the third process card is fully readable.
- Resizing an active mobile scene to 320 × 480 or 844 × 390 switches all three tracks to ordinary flow, clears old travel/transforms and shows all eight panels. A 150px swipe moves the second process card exactly 150px. Portrait restores only the eligible connection/process staging. No horizontal page overflow was observed.
- Explicit loopback no-JavaScript and Reduced Motion fixtures at 390 × 844 expose all eight panels in ordinary flow and complete connection content, with decorative cues hidden. These are controlled simulations, not physical-device or operating-system preference claims.
- Clicked homepage → SiteLog → BudgetFlow → Selected Systems → Connected workflow. The three weekly hand-offs and history are readable on each relevant page and the homepage. Existing film controls/posters/description tracks remain; a 30-second muted homepage teaser was observed playing. Browser error/warning log was empty. An occasional stalled CUA preview was resolved by creating a fresh review tab.

The existing same-Wi-Fi preview was refreshed from the 60-file, 56.1MB allow-listed package. Every file matches the reviewed source byte for byte; an HTTP crawl checked 55 routes/assets. Private documentation, Git metadata, tooling, source masters and withdrawn film paths return 404. Asset version: `narrative-selective-20260908`.

Review on this Mac: `http://127.0.0.1:8989/index.html`. Phone: `http://192.168.0.18:8989/index.html`, on the same Wi-Fi while this Mac remains awake. Canonical main and the existing dated Netlify folder remain unchanged. No merge, push, deployment, form submission, external tracking update or Brain write occurred.

Simple Gate: PASS. Next action: Mat reviews the revised experience on his phone. Physical-device pacing acceptance remains with Mat.


## Phone chrome, visual hierarchy and reading pace — 8 September

Mat requested a further bounded refinement from `26bfbec`: restore the prominent desktop Missing Software Layer heading, remove the doubled explanatory rows, make the connections animate on normal phones with browser chrome, and slow process cards and the opening slightly. The root approved relocating the one existing mobile introduction immediately before its diagram track; desktop restores it inside the pinned scene. The opening keeps its mark and words, the workflow story keeps its accepted pacing and native mobile flow, and all evidence/media/form contracts remain intact.

Simple Gate: PASS. Intended user: a business owner reading on a normal phone or desktop. Required outcome: a clear visual hierarchy, visible connection drawing and enough time to read. Smallest useful change: one responsive heading placement, one consolidated explanation row, and independent travel adjustments.

- Desktop heading returns to `clamp(2.6rem, 5.7vw, 6rem)` at a maximum width of 1000px, with balanced lines. Diagram gaps reduce before compromising that hierarchy.
- The existing left explanation now combines main-system/separate-tools/mixed setups, the remaining gaps and how I trace and connect the work. The original AI economics paragraph remains on its right; mobile stacks that single row.
- Mobile stages the complete diagram beneath navigation when it fits, with the existing cue and 32px safety allowance. Its single introduction scrolls naturally before it. Tests include 390 × 664 and 375 × 667 viewport-height equivalents. Short screens retain flow, but their wires visibly draw as the diagram crosses the viewport rather than completing on arrival. Reduced Motion and no JavaScript remain complete and static.
- Process reading travel increases by 40% independently of the story. The opening’s actual animation travel rises from 40svh to 54svh (35%), giving a total track of 154svh. No scroll interception is introduced.

Builder gates: site, privacy, exact media/master hashes, HTTP crawl, both JavaScript syntax, production geometry and current/cumulative diff checks pass. Geometry tests exercise mobile introduction relocation/restoration, diagram-only phone eligibility, active resize and Reduced Motion cleanup, forward/reverse flow wires, the unchanged story/process ratio and the longer opening journey. Shared CSS/JS key: `readable-connection-20260908`. Root browser validation and independent cumulative review follow on the exact committed head; physical phone acceptance remains separate. Local only: no merge, push, deployment, form submission or external record write.

### Refined review delivery

Independent cumulative verdict against `1891e21`: **Approved** at application head `656f2970640a1c07f02bfe54de4d42574b450ca2`, with no actionable findings. All independent gates above passed, including the transient HTTP crawl.

Root reproduced the reported failure at 390 × 664: the former title-inclusive fit check selected flow, with input wires already complete before the full diagram entered view. The corrected scene stages at both 390 × 664 and 375 × 667. At the former size, a 150px swipe changes input wire offsets from .859476 to .102396 while the board stays at y=171.27; the complete outcome then fits through y=522.94. At 320 × 480 the diagram follows ordinary scrolling, with visible wire progression over 100px and exact reverse restoration. One heading remains through responsive changes. Explicit no-JavaScript/Reduced Motion fixtures retain all content and no horizontal overflow.

Desktop rendering confirms the restored heading at 82.08px in 1440 × 900, with a fixed title through the final diagram and one supporting text row below. A further compact-spacing correction preserves the same hierarchy and staging on laptops: 77.86px heading at 1366 × 768, and 72.96px at 1280 × 720. At the latter size, the title begins at y=105.67 and the complete diagram ends at y=650.52, with a clear cue and unchanged readable body/label fonts. Genuine short-screen fallback and the 32px fit allowance remain.

Pacing checks: at 375 × 667, the first 150px process swipe keeps card 01 fully visible while the logo moves about 39px horizontally and 51px vertically; the next swipe shows card 02. Desktop 1280 × 720 likewise keeps card 01 readable over a 150px scroll, with visible background movement. Mobile opening travel is now 359px at 390 × 664, compared with 266px previously: the first 150px scroll is still revealing the name, and all words are fully visible at 350px. Desktop opening travel is 415px at 1366 × 768. Physical touch-device pacing still requires Mat's review; these measurements are browser viewport simulations.

The same phone preview was refreshed from 60 allow-listed public files (56.1MB). All bytes match the reviewed source; 55 HTTP routes/assets pass and the five private/withdrawn path probes return 404. Review links remain `http://127.0.0.1:8989/index.html` on this Mac and `http://192.168.0.18:8989/index.html` on the same Wi-Fi. No merge, push, Netlify deployment, external record update or form submission occurred. Simple Gate: PASS.


## Clearer offer and an illustrative information route — 8 September

Mat approved option A and an early offer diagram, continuing from `3e6449b` with the same authorised Codex builder and independent reviewer. The design reference is a planning fragment; none of its preview tabs, stage buttons or Tweak controls belong in the website.

Simple Gate: PASS. Intended user: a prospective business owner. Required outcome: quickly understand that Mat builds bespoke software, connects existing tools and reduces repetitive admin, then recognise familiar gaps in information flow. Smallest useful change: replace the existing early problem introduction and fictional request story; add no new long scroll section.

The `fit` slot retains `fit`, `proposition` and `gap` anchors, now headed “Bespoke software. Built around your business.” Its native text diagram connects Accounts, Business software and Spreadsheets to focused Proof Systems software, with Capture and updates / Approvals / Reporting scope and a start-small closing line. Shared navigation calls the destination “What I do”, preserving its links.

The following story is “Where the work loses its flow”: re-enter, work around, chase and reconcile. Each stage retains the approved plain-language explanation of manual information work. One shared map has Email and forms, Working spreadsheet, Business software, Updates and approvals and Management report. It is an illustrative pattern, not a required workflow. Desktop copy advances beside the persistent map; each step highlights adjacent nodes and an interrupted link. The existing interrupted branded backdrop remains. On phones the complete map appears once in native flow; each explanation has only a small decorative two-node fragment, avoiding repeated full diagrams and repeated screen-reader narration. Short desktops use flow if the whole map cannot fit safely.

The opening’s 54svh animation travel, process travel at 140% of its earlier baseline, phone connection staging/title relocation, prominent desktop title/laptop fit, single explanatory row/AI economics, all evidence integration facts and media/form/legal contracts remain intact. Shared CSS/JS revision: `clear-offer-route-20260908`.

Builder gates pass: site, privacy, exact films/masters/posters/captions/teasers, HTTP crawl, both JavaScript syntax, production scene geometry and current/cumulative diff checks. Tests replace fictional-order requirements with the single-map/copy/adjacent-highlight/physical-break contracts and cover map overflow fallback. Root browser validation and independent cumulative review follow on the committed candidate. No merge, push, deployment, form submission or external record write.

### Clearer-offer review delivery

Application head `f05d60ac53eb72cac6db323a1ab456925ddd4fc8` received independent cumulative **Approved** against canonical `1891e21`, with no actionable findings. All independent gates passed. Root's rendered review found and returned one diagram contrast/spacing defect to the builder; the corrected label and note use readable light text and intentional spacing.

At 1440 × 900, desktop stages 01 → 02 → 04 → 02 retain the same 368.56px-high map bounds while the relevant two nodes and interrupted link are highlighted. The 1280 × 720 laptop scene fits with readable type. At 390 × 664, one 315.8px-high map precedes four compact native-flow explanations; a 150px scroll moves the map and explanations exactly 150px while the branded background moves. Narrow layouts through 320 × 480 remain readable without horizontal page overflow. A 1280 × 480 desktop correctly falls back to flow rather than clipping the map.

At 375 × 667, the connection section remains staged and a 120px scroll changes progress from .5737 to .8307 and finishes the remaining wire. Resizing to 1280 × 720 restores the single introduction inside the scene, the 72.96px connection heading and all eligible desktop modes. No-JavaScript and Reduced Motion server fixtures retain all narration and diagrams; these are controlled simulations. The selected-systems navigation returns correctly to the new “What I do” section. Physical phone feel and commercial wording remain Mat's review decision.

The existing phone preview now serves the reviewed `clear-offer-route-20260908` build: 60 public files match source byte-for-byte, 55 HTTP paths pass, and private docs, Git metadata, tooling, source masters and withdrawn film paths return 404. Current review: `http://127.0.0.1:8989/index.html` on this Mac and `http://192.168.0.18:8989/index.html` on the same Wi-Fi while the Mac is awake. The preserved pre-thread V1 comparison remains available on port 8991. Canonical main remains clean at `1891e21`; the dated Netlify folder is unchanged. No merge, push, deployment, form submission or external write occurred.

Simple Gate: PASS. Next action: Mat compares the clearer offer and information journey on desktop and phone.
