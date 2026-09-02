# Preserved AGE-600 source masters

These files are the AGE-600 public masters as they stood before the AGE-601
narrative re-export. They live under ``tools/`` so they are outside the
production-shaped publish package built by ``tools/prepare_publish.py``.

Rebuild Applications Ledger, LedgerLink and Cashflow into the public media
tree, and the withdrawn Management Accounts rendition into
`tools/demo-film-narrative/retained-withdrawn/management-accounts/`, from the
repository root with:

```
python3 tools/demo-film-narrative/render_narrative.py render
```
