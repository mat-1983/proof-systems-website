# Website V2 refinement delivery

Recorded: 5 September 2026.

## Current state

Mat reviewed V2 on mobile and reported that it works great, then requested bouncing scroll cues and longer autoplay demos. Those changes are complete locally. The independent final verdict is **Approved** for application commit `3673c30cb43d051d126e62b154a3482760e6cc08`, with no outstanding findings for this increment.

Browser access was restored after the earlier locked-Mac limitation. Root completed rendered checks of the changed homepage scenes and playback at desktop, phone portrait and short landscape sizes. Physical iOS/Android automation is not claimed. The unchanged inner-page and form contracts passed the automated checks; their full interactive acceptance was not repeated in this increment.

- Branch: `codex/website-v2`
- Original V1 base and fallback: `044cf52228bd8adc8b4e66d902baaf2f2a7bd106`
- Refinement baseline: `e6359f60b07116f6a8bf7cf91a1257a9a94b85ea`
- Refinement implementation: `5ab57bbb028dbfacff8f16092282a27f108a05f7`
- Prior refinement accessibility correction: `e374fc7fb0d6eb7e405fdb754e8683db2dac884c`
- Arrow/teaser increment baseline: `2ce6b336dfd0fd7e6e3263ca286a40ab6cb42d35`
- Final approved application commit: `3673c30cb43d051d126e62b154a3482760e6cc08`
- Arrow/teaser implementation agent: `/root/v2_scroll_cues_teasers`, assigned Sol / high.
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

Independent comparisons confirm the opening SVG geometry and words are preserved. The opening renderer now safely handles the former cue being absent; its scroll behaviour is retained. Form JavaScript and redirects remain byte-identical. Normalised privacy main text is unchanged. Root's story comparison found only the previous outcome paragraphs promoted to H1, with the other explanatory paragraphs retained.

Review corrections included the enquiry styling selector and removal of `visibility:hidden` from inactive narrative panels so screen-reader users can read every stage. There are no outstanding source findings.

## Rendered verification and limits

Root checked native forward and reverse scrolling in the opening, workflow story, forming software connection and all four practical-starting-point stages. The arrow stays visible through each final hold. At 390 × 844, 320 × 480 and 844 × 390 viewport sizes, the tested content clears the arrow and has no horizontal overflow. Tall cards retain a readable top and bottom phase; the short landscape connection copy retains correct sentence spacing.

At 1440 × 900, all three actual teaser videos autoplayed muted with 30-second durations, and playback was observed beyond the old five-second limit. Fresh 390 × 844 rendering also confirmed inline playback beyond five seconds. Midpoint frames contain useful demonstration content. Independent media comparisons confirmed faithful excerpts and unchanged full-film, poster and caption files.

Normal reload and fresh-tab checks verified the revised shared asset URLs and an empty current console. Explicit browser fixtures for Reduced Motion and no JavaScript showed all process cards in readable ordinary flow, with decorative cues hidden and no teaser autoplay. These fixtures simulate those conditions; they are not claims of physical device or operating-system preference testing.

No remaining rendered defect was found in this increment. Physical-device toolbar behaviour, a complete fresh inner-page click-through and interactive form/caption controls were not re-tested here. No form was submitted. Earlier delivery and review history remains in Git.

## Local previews and boundary

V2: `http://127.0.0.1:8988/`

V1 fallback: `http://127.0.0.1:8986/`

Mobile preview on the same Wi-Fi: `http://192.168.0.18:8988/index.html`. The existing LAN server serves a public allow-list copy, refreshed with this increment. HTTP checks confirmed all four cues, revisioned assets and the three updated teaser files; documentation, tooling and source-master paths return 404. The Mac must remain awake.

The V1 checkout remains clean on `main` at `044cf52`; local annotated tag `website-v1-fallback-2026-09-05` resolves to that same commit. The existing V2 worktree is separate. No merge to main, push, deployment, publication, external message, Brain write or live form submission occurred. No new Linear issue or project placement was inferred from this task.

The publish allow-list excludes `docs/` and testing tools. This record is not public website content. Earlier implementation and review history remains in Git.
