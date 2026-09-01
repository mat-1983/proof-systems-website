# Synthetic demonstration media

These silent films show operator-built systems around one synthetic Northstar workflow. They contain no client records or production credentials and are not external client case studies.

## Shared format

Unless noted, each master is H.264 MP4, 1280 × 720, approximately 30 fps, with no audio track. Every public film has a poster, an English WebVTT timed description and an accessible summary on its story page. Story-page players expose that VTT as an optional `English descriptions` captions track. It is not enabled by default, so burned-in titles and browser captions do not appear together during ordinary playback.

## Visible narrative treatment

Inspected start to finish on 1 September 2026. The primary visible narrative is the composition-aware text already in the picture. Optional WebVTT remains available from native player controls. Review frames for every film, including every newly added callout, are in `docs/age-601-film-review/`.

Rebuild the four denser public films from the preserved AGE-600 masters with `python3 assets/demo-media/render_narrative.py render`.

### SiteLog — preserved AGE-600 master

Full-screen chapter cards at the open and at the admin hand-off. Lower-thirds on the tradesperson form, weekly invoice and admin export. Form-filling, weekly summary, project controls and the user-account modal stay clear so controls and the cursor remain visible.

### BudgetFlow — preserved AGE-600 master

Full-screen chapter cards at the open and at the quantity-surveyor hand-off. Lower-thirds on labour allocation. Table allocation, variation and quote modals, payment-report builder and the Sage workbook stay clear.

### Central Project Register — preserved AGE-600 master

Full-screen title card, then the portfolio and project drill-down without extra callouts. The interface already names identity, contract terms and the Applications Ledger hand-off.

### Probables — preserved AGE-600 master

Full-screen title card, then the pipeline and add-probable form without extra callouts. Field labels on the form are the stage narrative; overlaying them would cover the cursor.

### Applications Ledger — re-exported from `source/applications-ledger-demo.mp4`

Existing title card retained. Added compact lower-thirds:

- 4.20–7.40 LIVE CONTRACTS / Status and a route into each ledger
- 8.20–13.80 CONTRACT LEDGER / Application, certification, payment and retention
- 108.80–113.80 FINANCE VIEW / Attention queue for cash and retention
- 119.50–123.80 FORECAST HYGIENE / Missing or stale forecasts

No callout during add-application or valuation modals, the quantity-surveyor dashboard Accept queue, retention year-bucket inspection, or the forecast page itself.

### LedgerLink — re-exported from `source/ledgerlink-demo.mp4`

Existing title card retained. Connection test, Run extraction and evidence drill-down stay clear of overlays because those controls sit in the lower frame. Added raised workbook callouts:

- 47.20–51.50 OVERHEAD ACTUALS / Period transaction listing
- 69.05–70.80 RETENTION BY PROJECT / Held and released from the same extract

The retention callout ends before the Downloads window opens.

### Cashflow — re-exported from `source/cashflow-demo.mp4`

Existing title card retained. Added:

- 8.20–18.40 COMMERCIAL FINANCE / Short-term and long-term cashflow
- 27.00–34.00 SHORT-TERM / Funding events and daily cash
- 38.40–48.00 COST-VALUE / Project schedule feeding the longer view

Workbook callouts sit above the sheet tabs. Dense forecast and facility rows are left uncovered.

### Management Accounts — re-exported from `source/management-accounts-demo.mp4`

Existing title card and the later “One reporting cycle” chapter card retained. Added:

- 6.40–10.80 MONTHLY PACK / Open the reporting workbook
- 14.60–18.20 PROFIT AND LOSS / Current year, budget and forecast
- 22.60–33.80 LIVE PROJECTS / Turnover and gross margin by region

No extra callout on the overheads sheet, where expenditure rows and worksheet tabs fill the lower frame.

## SiteLog

`sitelog-demo.mp4` combines the tradesperson and administrator journeys. It shows current-week site entry, the weekly summary and invoice, a structured back-office export, and simple project and user controls.

- Runtime: 1 minute 31.4 seconds
- Poster: `sitelog-poster.jpg`
- Timed description: `sitelog-demo.vtt`
- Accessible summary: A tradesperson records work against a selected project and location for the current week. The entry appears in the weekly summary and a weekly invoice is generated. An administrator then exports the selected week and reviews the project and user-management controls.

## BudgetFlow

`budgetflow-demo.mp4` combines the site manager, quantity surveyor and accounts journeys. It shows weekly labour allocation against project budgets, variation and quote control, overspend review, and a coded payment export.

- Runtime: 2 minutes 6.9 seconds
- Poster: `budgetflow-poster.jpg`
- Timed description: `budgetflow-demo.vtt`
- Accessible summary: A site manager allocates weekly labour costs to project budget locations and checks remaining value. A quantity surveyor creates a controlled variation, builds a client quote and reviews an overspend request. Accounts then generates a payment workbook with detailed records and a Sage-compatible nominal and cost-code export.

## LedgerLink

`ledgerlink-demo.mp4` shows a connection to accounts software, a period extraction and reusable workbook outputs. Public wording must say “connection to accounts software”, not “connection to a workbook”.

- Runtime: 1 minute 49.3 seconds
- Poster: `ledgerlink-poster.jpg`
- Timed description: `ledgerlink-demo.vtt`
- Accessible summary: The operator tests a connection to accounts software, queues the period datasets, runs the extraction and reviews evidence counts before opening the resulting workbooks.

## Central Project Register

`cpr-demo.mp4` shows a portfolio of live, completed and pipeline projects with identity and contract value, then a project-level drill-down. The public name is Central Project Register. The real service is a database and API; the filmed interface visualises synthetic demonstration data. The master film file is unchanged.

- Runtime: 18.6 seconds
- Poster: `cpr-poster.jpg`
- Timed description: `cpr-demo.vtt`
- Accessible summary: A portfolio of live, completed and pipeline projects is shown with identity and contract value. Opening a live project reveals codes, contract terms and a hand-off into Applications Ledger.

## Applications Ledger

`applications-ledger-demo.mp4` shows one controlled route from live contracts through application, certification, payment, retention and role dashboards.

- Runtime: 2 minutes 10.7 seconds
- Poster: `applications-ledger-poster.jpg`
- Timed description: `applications-ledger-demo.vtt`
- Accessible summary: A commercial user opens live contracts, works in a ledger that keeps applications, certificates, payments and retention together, and uses role dashboards for due actions, variances and forecast hygiene.

## Cashflow

`cashflow-demo.mp4` shows short- and long-term cashflow views built from connected source data.

- Runtime: 1 minute 18.7 seconds
- Poster: `cashflow-poster.jpg`
- Timed description: `cashflow-demo.vtt`
- Accessible summary: The commercial finance console opens short-term and long-term cashflow. A daily workbook, a project cost-value schedule and a longer forecast with facility checks are reviewed in turn.

## Probables

`probables-demo.mp4` shows a pipeline of likely future work and a consistent form for adding a new probable.

- Runtime: 58.1 seconds
- Poster: `probables-poster.jpg`
- Timed description: `probables-demo.vtt`
- Accessible summary: The pipeline lists likely future work with value, margin, status, owner and division. A new probable is captured through a consistent form, including year-by-year value and retention, and joins the same list.

## Management Accounts

`management-accounts-demo.mp4` shows a structured monthly reporting workbook with comparative views and supporting schedules.

- Runtime: 53.9 seconds
- Poster: `management-accounts-poster.jpg`
- Timed description: `management-accounts-demo.vtt`
- Accessible summary: A monthly reporting workbook is opened on the profit and loss schedule, then on live project turnover and gross margin, then on supporting overhead schedules that stay in the same pack.

## Homepage teasers

`sitelog-teaser.mp4`, `budgetflow-teaser.mp4` and `ledgerlink-teaser.mp4` are 5-second, 960 × 540 muted clips derived from the masters. They exist only so the homepage can lazy-load a short loop when visible and motion is allowed. They are not substitutes for the story-page films.

## Relationship

SiteLog captures weekly site records. BudgetFlow uses those cost records for allocation and payment export. Central Project Register holds project identity and status. Applications Ledger records applications, certificates, payments and retention. LedgerLink extracts controlled accounts data through a connection to accounts software. Deterministic local processing produces Cashflow and Management Accounts. Probables keeps likely future work in one consistent list.

## Public-safety status

All films and posters contain synthetic Northstar names, projects and values only. No client identifiers, production credentials, live URLs, personal contact details or real commercial performance claims are present. The synthetic-demonstration label is visible on every public film surface.

## Source provenance

SiteLog and BudgetFlow were recorded and reviewed on 28 August 2026 from the approved AGE-584 local synthetic demonstration suite.

The six staged AGE-600 masters were added from the approved local synthetic demonstration suite on 29 August 2026. Public-safety review of sampled frames found only synthetic Northstar labels, local demonstration chrome and Sage-style simulated accounts software. Sage itself is not connected.

On 1 September 2026, Applications Ledger, LedgerLink, Cashflow and Management Accounts were re-exported from those preserved AGE-600 masters with composition-aware stage callouts. SiteLog, BudgetFlow, CPR and Probables were not re-encoded. Opening poster frames are unchanged.

Source-file SHA-256 hashes for the earlier SiteLog and BudgetFlow recordings:

- `01-Tradesman Journey.mov`: `afcd4b7941103abf3fda8d869c780cf42355360ece4b58a554ae11be0a2e9b27`
- `02-SiteLog-Admin.mov`: `a7fdc7ef11c6fd5b5777d62f77e8e319646a103e781db13ef4776ba3d3909173`
- `03-BudgetFlow-Site-Manager-edited.mp4`: `df5f1edd48cec2e18e001f31051e496a013e93c78b13124cc7447a4505b816af`
- `04-BudgetFlow-QS-edited.mp4`: `9004da959a11bbd1977a1871889571201906eb8fdaec2328f73dda14670e15c1`
- `05-BudgetFlow-Accounts.mov`: `fa49e71ba6c25e6a50737db8450b9f752eca3048ee1532d2a9bc2ced07c8bee9`

Final-file SHA-256 hashes:

- `sitelog-demo.mp4`: `f91d00ff10fb5b5159ad8ffe3a2ea277f6d55da0dfe17b9492c6469a32eb0e51`
- `budgetflow-demo.mp4`: `dda5c8ac812c5dce7a33a0d3ec22296e552087ec38a8626bd79e00a9d485ed62`
- `ledgerlink-demo.mp4`: `58b88ac057fc0f1fa06e7f8115733c9efd83939d92e040dcebc2b11cdda4afeb`
- `cpr-demo.mp4`: `ca066cfd62834562bcc000cb501172047600a4356b68613ff13e97aec3f748af`
- `applications-ledger-demo.mp4`: `3c4ec8c43e7d71bb416a19be245d9b119434840820985b84291609bdbc5921bb`
- `cashflow-demo.mp4`: `26bbf1c2cee540a1b60edbd7d22f86e849dcaa3b06c019d2d452dd8e117ed901`
- `probables-demo.mp4`: `647300de26440d2afa33ae0b64a5e7ccd4a04a0909f72f906c5726a1377dfc63`
- `management-accounts-demo.mp4`: `6ffc9169688be1d4bceb683465e8a773bf8a5b52dae071c2b66cfc0dee34b710`
- `sitelog-poster.jpg`: `4022b4b2829dc32d004bfdd10c9dc0297fad5a353545832cc6dea5a1cf028a40`
- `budgetflow-poster.jpg`: `1af478e41bf80428b75aa9fcda6b9c3b469ec997b8189875c863a19e4f513162`

AGE-600 source masters retained in `source/` for the four re-exported films:

- `source/ledgerlink-demo.mp4`: `2123f74adf316d22b0efbaff6c7cfced227ba0c0850c58be572cb1c760c3db02`
- `source/applications-ledger-demo.mp4`: `e63d2c36dca58e3f5b234e3c9ff9e8819d129edbd05c72bcecb2317a8035598a`
- `source/cashflow-demo.mp4`: `769e9b44cf7c97ec565c52938c1b194e14eed97e49d65bcdb8c34fedf11c109f`
- `source/management-accounts-demo.mp4`: `38bbe17c361e4252ed288f0df095236394cb9b4402b6c74941bd19ba1c67df9c`

No publication or deployment is authorised by this record.
