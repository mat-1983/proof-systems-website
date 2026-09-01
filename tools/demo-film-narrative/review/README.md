# AGE-601 film review frames

Representative frames for independent review. Callout files show every
added stage label. `*-controls-desktop.jpg` and `*-controls-phone.jpg`
show each callout on the story-page video size (828×466 at 1440, 342×192
at 390) with a Chrome-sized native control bar open.

System Chrome and Playwright Chromium SIGSEGV in this environment
(Crashpad `settings.dat` permission). The control stills are therefore
the public frame scaled to the live player geometry with a 48px control
overlay matching Chrome's occupied strip.

These stills are not public site assets and are excluded from the
publish package built by ``tools/prepare_publish.py``.
