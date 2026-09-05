# Website V2 delivery

Recorded: 5 September 2026.

## Delivery state

- Branch: `codex/website-v2`
- Base: `044cf52228bd8adc8b4e66d902baaf2f2a7bd106`
- Initial implementation commit: `c3c1060456e31d09be7e7def0e4c25fe704e8bd6`
- Correction commit: the commit containing this record; use `git rev-parse codex/website-v2` for the exact cumulative head and compare it with the delivery receipt.
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

Root browser UAT passed the 1440px animated story and contrast corrections, the 768px and phone static record trail, 320px opening forwards and backwards, mobile menu anchor closing, and 390px local enquiry validation without submission or URL data. The independent review boundary corrections for no-JavaScript navigation, short-height desktop layout, reduced motion, dark-surface contrast and retained identity/media checks are pending cumulative re-review at the time of this record.

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
