# AGE-600 round 10 decisions

Append-only log of material implementation choices. Routine edits are not recorded.

| Date | Decision |
| --- | --- |
| 2026-08-31 | Approach returns to four independent modules (Understand, Choose, Prove, Extend) plus a fifth route stage. Wide screens keep all four module positions in one row from 901px; 900px and below accumulate the same modules as a vertical journey. |
| 2026-08-31 | Desktop Approach travel stays 360vh. Narrow Approach travel is 220vh so each stage remains reachable without a miniature whole-image crop. Unrevealed mobile modules are removed from layout (`display: none`) so the completed state can grow taller than the viewport. |
| 2026-08-31 | Closing routes are whole-route links: Clear workflow and Needs clarity go to `workflow.html`; Team capability / AI team training goes to `training.html`. No new query-string routing. |
| 2026-08-31 | Generic Selected Systems / See selected systems / View selected systems / View all selected systems / Back to Selected Systems destinations open the index top (`work/index.html`, `../work/index.html`, or `index.html`). `#finance` and `#connected-workflow` stay contextual. `site.js` no longer writes `#individual-systems` on individual-view selection or initial load. |
| 2026-08-31 | Mobile opening follows the same mark → connect → name → tagline sequence as desktop, with `125vh` travel instead of `170vh`. The previous `max-width: 760px` completed-state shortcut is removed. Reduced-motion and no-JavaScript still show the completed opening. |
| 2026-08-31 | Approach uses a cream-to-sand gradient, a restrained amber glow on the active module, and a faint electric-blue `drop-shadow` on completed connectors. No blur filters on type. |
