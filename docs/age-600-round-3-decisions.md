# AGE-600 round 3 decisions

Append-only log of material implementation choices. Routine edits are not recorded.

| Date | Decision |
| --- | --- |
| 2026-08-29 | Copied the six approved raster references into `docs/design/age-600-round-3/` under durable names. Source bytes preserved. Hashes recorded in `docs/design/age-600-round-3/README.md`. Rasters are not linked from public HTML. |
| 2026-08-29 | Opening sequence uses a large inline SVG node mark, sticky natural scroll and CSS `--opening` / `data-phase`. Default CSS is the completed connected state so no-JavaScript and reduced-motion readers see Proof Systems and the tagline immediately. No scroll hijack, preloader or WebGL. |
| 2026-08-29 | Replaced the homepage selected-systems architecture map with one general SME stack scene and a native `With ERP` / `Without ERP` radiogroup. Both states stay in the DOM; a figcaption describes the proposition that Proof Systems adds the fitted layer rather than replacing commodity platforms. |
| 2026-08-29 | Restored chapter rhythm with near-black, warm cream, deep ink-blue and muted sandstone panels. Canonical logo amber `#d89042` and self-hosted Inter are unchanged. |
| 2026-08-29 | Rebuilt 01 / The Gap, 01B / Fit, 02 / Capability and 04 / Approach from the approved round-3 copy and architectural language. Proof restores the compact three-item `proof-grid` from `c2a40d8` while keeping 50cd562 SiteLog, finance and synthetic wording. |
| 2026-08-29 | Selected Systems keeps the eight-story index as the default Individual systems view and adds a Connected workflow radiogroup. The connected diagram is the synthetic Northstar story, not the general offer, with amber operational links distinct from blue finance paths. |
| 2026-08-29 | Operator First and Start headings override the global `h2 { max-width: 22ch; }` with `max-width: none` so they use the available wrap width and wrap naturally on small screens. The earlier 16.8em/14.5em caps are removed. |
| 2026-08-29 | Independent review found the first round-3 scenes too flat. The six approved views are now inline isometric/2.5D SVG with three-face blocks, amber/blue connections and HTML keys for small viewports. Raster references remain in `docs/design/` only. |
| 2026-08-29 | Desktop/laptop (900px and above) now presents optimised WebP derivatives of the six approved references from `assets/img/age-600/`. Master PNGs stay in `docs/design/` and are not linked. Native SVG/HTML remains the mobile, no-JavaScript and accessibility fallback. Gap/Fit/Approach headings stay in the DOM with a visually-hidden clip rather than `display:none`. |
