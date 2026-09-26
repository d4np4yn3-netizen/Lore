# LORE Crypto History — Raw Discovery by Year

This directory is the **lossless year-by-year split** of the broad `events.json` discovery archive.

## Layers

- `raw/YYYY.json` — every discovery record for that year, preserving permanent IDs, research fields, corrections and duplicate/context links.
- `../YYYY.json` — curated canonical evidence records used for historical review and eventual card scoring.
- `../../events.json` — legacy aggregate snapshot retained for compatibility.

## Rules

1. No raw event is deleted merely because it is duplicated, contextual, disputed or a deep cut.
2. Permanent `LORE-EVT-####` IDs are preserved.
3. Card scoring must use canonical evidence records, not unverified raw rows.
4. Future research should update year-sized files rather than repeatedly loading the monolithic master.
5. `raw/index.json` is the integrity check. Its grouped count must match the aggregate master.

Generated from the 1,229-event master on 26 September 2026.
