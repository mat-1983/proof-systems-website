# AGE-600 round 4 decisions

Append-only log of material implementation choices. Routine edits are not recorded.

| Date | Decision |
| --- | --- |
| 2026-08-29 | Homepage With ERP / Without ERP, Gap, Fit and Approach no longer present WebP derivatives as rectangular desktop screenshots. The existing isometric SVG/HTML is the visible visual at every width. Master PNGs stay in `docs/design/` and public WebP files remain on disk; only the connected Selected Systems diagram still uses a desktop WebP. |
| 2026-08-29 | Chapter headings and explanatory copy stay live HTML. The round-3 `desktop-hide-copy` clip is no longer applied to Gap, Fit or Approach. |
| 2026-08-29 | Desktop/laptop (900px and above, with JavaScript and motion allowed) stages each of the four scenes in three reading-order layers via IntersectionObserver. Default CSS, `prefers-reduced-motion: reduce`, no-JavaScript and viewports below 900px show the complete final scene. |
| 2026-08-29 | Proposition uses a large lead line and a smaller supporting line, both larger than the former marker/lede pair. Heading-width relaxation is scoped to the affected homepage chapters so Capability keeps the global `22ch` measure. |
| 2026-08-29 | ERP/no-ERP explanations sit outside the scene. Native radios plus `:has()` expose the selected explanation and a shared closing statement without JavaScript. |
| 2026-08-29 | Proof keeps the three demonstrations and Explore links, shortens the three narratives, removes the finance-card `View all systems` link, and adds one prominent `View all selected systems` button below the grid. |
| 2026-08-29 | General Selected Systems actions use the explicit destination `work/index.html#individual-systems` (or the correct relative equivalent). `#individual-systems` selects the individual view from hash, `:target` and `pageshow`, including after the connected view was previously selected. Finance deep links stay finance-specific. |
| 2026-08-29 | Fit right-hand cue `ONLY THE MISSING LAYER` is end-anchored at x=868 inside viewBox `-26 92 914 459` so the label grows left into the available scene. The live HTML duplicate below the illustration is unchanged. `overflow-x: hidden` is not the fix. |
| 2026-08-29 | Round-four correction 2 restores the five approved homepage WebP files as the primary rendered visuals. Progressive presentation uses clip-path on those rasters. The simplified SVG chapter drawings are not shown. Desktop/laptop shows the uncropped final artwork; mobile may crop/pan the same source with live copy. |
