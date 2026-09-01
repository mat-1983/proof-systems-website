# AGE-600 round 14 decisions

Append-only log of material implementation choices. Routine edits are not recorded.

| Date | Decision |
| --- | --- |
| 2026-09-01 | Narrow Fit keeps sticky 300vh travel and the 12%/66% stage contract. Continuity comes from compacting the mobile vertical connector, not from retiming stages or changing desktop Fit. |
| 2026-09-01 | The mobile Fit scene shortens from 48rem to 38rem. The two-way amber connector is an explicit 4.6rem span from the receded industry-specific block to the Bespoke Layer instead of `calc(100% - 33.8rem)` (14.2rem). Desktop Fit stays 26rem / 240vh. |
| 2026-09-01 | Narrow Fit sticky alignment is `flex-start` so the compacted stack is not vertically centred out of the phone viewport. Reduced-motion and no-JavaScript still show the complete scene. |
