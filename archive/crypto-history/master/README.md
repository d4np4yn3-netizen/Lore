# LORE Crypto History — Master Candidate Database

**Canonical master structure: 26 September 2026**

The discovery archive contains **1,229 candidate events** and is now split into year-sized files under `master/years/`.

## Canonical master rules

- Every historical candidate retains its permanent `LORE-EVT-####` ID.
- A record lives in the year file matching its current effective date.
- Date corrections may move a record between year files, but **never renumber its event ID**.
- `master/index.json` is the lightweight entry point for year counts and paths.
- `../events.json` is frozen as a **legacy monolithic snapshot**. Do not continue editing it.
- Raw candidate status does not imply factual verification.
- Evidence work is kept separate from the master candidate layer.
- Card scoring begins only from evidence-ready/canonical events.

## Structure

```text
archive/crypto-history/
  master/
    README.md
    index.json
    years/
      1976.json
      ...
      2025.json

  years/
    2021.json   # evidence-ready research layer (existing)
    ...
    2025.json

  events.json   # legacy snapshot; frozen
```

This split exists to prevent oversized-file timeouts and make chronological research, deduplication and scoring reliable.
