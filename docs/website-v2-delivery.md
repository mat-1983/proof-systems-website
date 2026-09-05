# Website V2 refinement delivery

Recorded: 5 September 2026.

## Current state

Implementation is complete locally. Final acceptance is **Blocked** solely on rendered browser UAT: the Mac is locked and the CUA tool cannot unlock it automatically. Mat was asked to unlock it; no new desktop rendering, phone viewport, physical iOS/Android, touch or media/form interaction verification is claimed for this refinement.

The independent reviewer found no outstanding source issues at application commit `e374fc7fb0d6eb7e405fdb754e8683db2dac884c`. Code and controlled-geometry checks passed. These do not substitute for visual acceptance. The earlier V2 delivery's browser checks covered an older implementation, including a static mobile story, and do not establish acceptance of this refinement.

- Branch: `codex/website-v2`
- Original V1 base and fallback: `044cf52228bd8adc8b4e66d902baaf2f2a7bd106`
- Refinement baseline: `e6359f60b07116f6a8bf7cf91a1257a9a94b85ea`
- Refinement implementation: `5ab57bbb028dbfacff8f16092282a27f108a05f7`
- Final application correction: `e374fc7fb0d6eb7e405fdb754e8683db2dac884c`
- Implementation agent: `/root/v2_refinement_build`, assigned Astra / high.
- Read-only contract audit: `/root/v2_contract_audit`, assigned Sol / high.
- Independent reviewer: `/root/v2_refinement_review`, assigned Astra / high.
- Resolved runtime model metadata was not independently exposed; assignments are recorded above.
- Mat explicitly authorised Codex agents in place of the default Grok routing for this task.
- Installed development/review skills were aligned at source revision `350c84899df49fd6b1376cc62e660c5783763498`.
- Simple Gate: PASS

## Implemented

The approved B opening retains the original five-node logo geometry, node movement and progressively revealed words. Stable small-viewport sizing drives its travel. The workflow uses one customer request with a source, owner, next action and attached approval/history, replacing the confusing date example.

The missing software layer begins without connections. Routes draw from an ERP and everyday tools, meet at the Proof Systems software layer, then resolve into connected source, ownership and history. Copy covers ERP, separate tools and mixed setups, and explains how AI-assisted development makes earlier demonstrations, shorter iterations and a focused bespoke layer more viable. It distinguishes using AI to build software from using AI on operational data.

A Practical Starting Point now has a dark moving-light background and four process cards: understand the work, try a working demo, refine it together and prove it in use. Native scrolling drives their entry, hold and departure, with a persistent stage indicator. Services use editorial rows and a shared layered working record.

Normal mobile and short screens retain the reversible scroll sequences. Cards taller than the available area have a reading phase: the heading enters first, then the bottom travels into view before the next card. Indicators stay in place. No nested scroller, gesture interception or negative sticky top is used. Reduced Motion and no-JavaScript modes show the complete narrative in ordinary document flow; screen readers retain all narrative stages in normal-motion mode too. Switching to Reduced Motion stops and hides previously started decorative teaser videos.

The opening, workflow story, connecting-layer scene and practical-starting-point scene each carry the same small amber-and-cream down arrow while their dynamic stage is visible. The cue is decorative and does not alter native scrolling. Sticky-stage bottom padding reserves its footprint, including mobile safe-area space, so it cannot cover the disclosure, indicator or a tall card's reading phase. Reduced Motion and no-JavaScript ordinary flow hide it.

The three poster-first homepage teasers now show 30 seconds of continuous demonstration footage rather than 5 seconds. They remain lazy-loaded, muted, looping and `playsinline`; the full films, posters and VTT files are unchanged. Exact source intervals and encoding settings are recorded in `assets/demo-media/README.md`.

All public pages request the changed shared stylesheet and script with revision `scroll-cues-teasers-20260905`. This prevents a normal reload from combining the new cue markup with the former cached renderer. The current renderer also null-checks the former cue selector so it remains safe when paired with an earlier cached homepage during rollout.

All eight evidence stories, the collection, enquiry, training and privacy pages share the new navigation, type and spacing. Stories lead with outcomes and show their media immediately after the hero; Management Accounts remains written evidence. The collection uses editorial rows and a linked, text-readable connected workflow. Original substantive story copy, seven film/poster/caption associations, synthetic disclosures, accounting-data controls, form contract, legal text, public routes, hashes and redirects remain intact.

## Verified

Builder, root and independent checks passed as applicable on the final application changes:

- `python3 site_check.py`
- `python3 privacy_notice_check.py`
- `python3 proof_media_check.py`
- `python3 crawl_check.py`
- `node --check assets/js/site.js`
- `node --check assets/js/form.js`
- `node tools/scroll_scene_check.cjs`
- Cumulative `git diff --check`, Python compilation and pre-commit secret checks.

The production scroll test executes the actual scene functions with six controlled viewport/card geometries. Independent VM checks cover 24 synthetic panel geometries, forward/reverse states, readable top/bottom holds, indicators, toolbar travel stability and connection sequencing. These are executable maths checks, not rendered layout or physical-device tests.

Independent comparisons confirm the exact opening SVG geometry, opening words and `renderOpening` function are preserved. Form JavaScript and redirects remain byte-identical. Normalised privacy main text is unchanged. Root's story comparison found only the previous outcome paragraphs promoted to H1, with the other explanatory paragraphs retained.

Review corrections included the enquiry styling selector and removal of `visibility:hidden` from inactive narrative panels so screen-reader users can read every stage. There are no outstanding source findings.

## Remaining acceptance work

Once browser access is available, use the existing local V2 server to verify:

1. Desktop, tablet, phone portrait and short/landscape layouts, including headings, clipping, horizontal overflow and visible stage indicators.
2. Opening, request story, forming connection, four process cards and shared inner-page reveals, scrolling forwards and backwards.
3. Taller-card reading phases, orientation changes and browser toolbar expansion/collapse. Distinguish viewport simulation from physical iOS/Android testing.
4. All eight system stories and onward links, connected-view hashes, navigation, keyboard focus, media controls/captions and local form validation without submitting.
5. Reduced Motion and no-JavaScript rendering, plus ordinary phone scrolling smoothness where device access exists.

Return any defects to the implementation agent on the same cumulative branch and obtain a fresh independent verdict after corrections. Do not mark the visual/mobile acceptance complete from the VM checks alone.

## Local previews and boundary

V2: `http://127.0.0.1:8988/`

V1 fallback: `http://127.0.0.1:8986/`

The V1 checkout remains clean on `main` at `044cf52`; local annotated tag `website-v1-fallback-2026-09-05` resolves to that same commit. The existing V2 worktree is separate. No merge to main, push, deployment, publication, external message, Brain write or live form submission occurred. No new Linear issue or project placement was inferred from this task.

The publish allow-list excludes `docs/` and testing tools. This record is not public website content. Earlier implementation and review history remains in Git.
