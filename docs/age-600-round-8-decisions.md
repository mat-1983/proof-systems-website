# AGE-600 round 8 decisions

Append-only log of material implementation choices. Routine edits are not recorded.

| Date | Decision |
| --- | --- |
| 2026-08-31 | Gap, Fit and Approach replace the homepage rasters with staged semantic HTML/CSS/SVG scenes. Wide composition is used from 901px; vertical composition at 900px and below. Prototype Previous/Next and view toggles are not shipped. |
| 2026-08-31 | Scene travel is sticky and short: Gap/Fit 300vh (4 steps), Approach 360vh (5 steps), Capability 400vh (6 steps). Reduced-motion and no-JavaScript show the complete final scene. |
| 2026-08-31 | Capability keeps the horizontal five-node SVG on wide screens and uses the approved vertical node-and-rail journey on thinner screens instead of a bullet list. Actions remain gated to stage 6. |
| 2026-08-31 | Fit two-way connectors use a 3-unit amber stroke in both compositions; the narrow connecting arrow is vertical. Inline SVG icons replace any Lucide/runtime dependency. |
| 2026-08-31 | Narrow Gap clips `.gap-scene` (`overflow: hidden`) so the rotated `.gap-links` AABB cannot widen the document at 320/360/390. Nodes and labels stay inside the scene. Page-level overflow-x is not the fix. |
| 2026-08-31 | Legacy `.approach-stage` card/span/strong/em rules are scoped to `.approach-stages`. `.approach-journey .approach-stage` is a transparent unframed wrapper so numbers/titles read in ink on the sand section. |
| 2026-08-31 | Closing Approach route SVGs use `fill: none; stroke: currentColor` so the three symbols read as cream lines on the dark tiles. |
| 2026-08-31 | Fit recedes the industry-software structure and grows a slender two-way amber link, then the foundation and bespoke layer, instead of swapping snapshot cards. |
| 2026-08-31 | Approach is one persistent field with a caption rail: scatter recedes, the lens becomes the selected core, a check and branches grow, then the three routes appear beneath. |
| 2026-08-31 | A fixed `Continue scrolling` cue uses scrollBy, hides at `#start`/page bottom, and animates only under `prefers-reduced-motion: no-preference`. |
| 2026-08-31 | Narrow reduced-motion Fit keeps `translateX(-50%)` via a later combined `max-width: 900px` and `prefers-reduced-motion: reduce` rule, so the unscoped reduce `transform: none !important` cannot un-centre the vertical composition. |
| 2026-08-31 | Fit connector SVG paths span the viewBox; the wide box runs from the receded monolith to the foundation (`left: calc(4% + 14.8rem); width: calc(55% - 14.8rem)`), and the narrow box is an explicit vertical span from the monolith to the bespoke layer. The missing-layer label sits in the right gutter. |
