# Website V2 delivery

Recorded: 5 September 2026.

## Delivery state

- Branch: `codex/website-v2`
- Base: `044cf52228bd8adc8b4e66d902baaf2f2a7bd106`
- Initial implementation commit: `c3c1060456e31d09be7e7def0e4c25fe704e8bd6`
- Independently reviewed implementation head: `a27b6e57950bae5fc1cdc1fddc2fc02705243035`.
- Independent review: **Approved**. All four P2 findings were corrected; no material findings remain. This final record update changes documentation only.
- Requested implementation runtime: `gpt-5.6-sol`, high reasoning. Resolved runtime metadata was not independently exposed to the implementation lane.
- Simple Gate: PASS

The V2 implements the approved B five-node opening, the software-fit narrative and a continuous order-change example in which conflicting copies and a detached approval resolve into one connected record. Construction systems appear later as evidence. Existing public routes, seven films, the written Management Accounts example, enquiry form, privacy terms and sole-trader identity remain in place.

## Verification

Passed locally:

- `python3 site_check.py`
- `python3 privacy_notice_check.py`
- `python3 proof_media_check.py`
- `python3 crawl_check.py`
- `node --check assets/js/site.js`
- `node --check assets/js/form.js`
- Python compilation of the four check scripts
- `git diff --check`
- pre-commit secret scan

Root browser UAT passed the 1440px animated story and contrast corrections, the 768px and phone static record trail, 320px opening forwards and backwards, mobile menu anchor closing, and 390px local enquiry validation without submission or URL data. The retained SiteLog film played locally with native controls and no playback error; its phone layout remained usable.

Final boundary verification passed: opaque, readable no-JavaScript navigation over cream sections; a complete opening at 1280×600; ordinary-flow short-window storytelling with all four fragments at opacity 1, no blur and no scaling; and corrected light/dark text and action contrast. No-script rendering stripped scripts in an external loopback fixture. Reduced-motion rendering used a simulated media preference in that fixture, rather than changing the operating-system setting. The fixtures are outside the repository and are not part of the public package.

The independent reviewer reran public gates, executable forward/reverse opening and motion-mode checks, and mutation checks for identity, readable footers, exact film/caption associations, caption defaults, redirects and the short-window CSS cascade. Review approval applies to the local branch; merge and publication remain separate decisions.

## Local review

V1: `http://127.0.0.1:8986/`

```sh
python3 -m http.server 8986 --bind 127.0.0.1 --directory /Users/matglendenning/Developer/proof-systems/60_products/proofsystems-website
```

V2: `http://127.0.0.1:8988/`

```sh
python3 -m http.server 8988 --bind 127.0.0.1 --directory /Users/matglendenning/Developer/proof-systems/60_products/proofsystems-website-v2
```

The public package allow-list in `tools/prepare_publish.py` excludes `docs/`; this record is not part of the deployable package.

## Boundary

The original V1 checkout remains clean on `main` at the base commit. The annotated local fallback tag `website-v1-fallback-2026-09-05` resolves to the same commit. No merge, push, deploy, publish or live form submission was performed.

## Approved refinement implementation — 5 September 2026

Refinement base: `e6359f60b07116f6a8bf7cf91a1257a9a94b85ea`, same `codex/website-v2` branch. See `website-v2-refinement-brief.md` for the authorised direction. Codex agent implementation was explicitly authorised for this refinement; runtime model metadata was not independently exposed by the tools.

The opening retains the exact B mark geometry, node movement and words. Stable small-viewport units now drive its travel. The workflow uses a simple customer request, source, owner, next action and attached approval/history. A new connection scene draws routes from ERP and everyday tools into the Proof Systems software layer, followed by connected source, ownership and history. Four native-scroll process cards replace the previous starting-point list, with a moving-light background and persistent stage indicator. Services use editorial rows and a shared layered working record.

All eight evidence pages retain their original substantive copy and media but lead with outcomes and show the film (or Management Accounts written evidence) immediately after the hero. The collection uses eight editorial rows plus a linked, text-readable connected workflow. Enquiry, training and privacy share the same navigation, type and spacing. Form fields, consent, logic, legal text, routes, hashes, seven film/caption/poster associations and accounting-data controls remain intact.

Normal mobile and short-screen layouts use the same reversible scroll mechanism as desktop. A card taller than the available area has a reading phase during its hold: its heading enters first, then its bottom travels into view before the next card arrives. The stage indicator remains in place. This is driven by native page scrolling, with no nested scroller, gesture interception or negative sticky top. Reduced Motion and no-JavaScript modes instead show all panels in ordinary document flow. Changing to Reduced Motion also stops and hides any previously started decorative teaser video.

Implementation verification includes the repository site, privacy, media and HTTP crawl gates, JavaScript syntax and diff checks. `node tools/scroll_scene_check.cjs` executes the production scroll functions against six controlled viewport/card geometries and verifies forward/reverse states, readable top/bottom holds, stable toolbar travel and Reduced Motion final geometry. It is a maths regression test, not a browser layout or physical touch test.

Browser UAT and final independent review remain separate pending checks at this implementation handoff. The Mac was locked during implementation, so no new browser or physical iOS/Android device verification is claimed here. No form was submitted; no merge, push, deployment or publication was performed.

Simple Gate: PASS

Independent review correction: normal-motion visual panels now use opacity alone rather than `visibility: hidden`, so screen-reader virtual-cursor reading retains the complete workflow and process narrative. Inactive panels ignore pointer input and contain no focusable controls. The scroll regression gate verifies these accessibility contracts. Browser verification remains pending.
