# LORE Crypto History — Year Evidence Files

**Working source of truth for evidence research and card scoring.**

The original `../events.json` remains the preserved broad discovery archive (1,229 raw candidates). It should now be treated as **read-only discovery history**, not the day-to-day research file.

## Working structure

- `YYYY.json` — researched/triaged records for that calendar year.
- `origins.json` — researched pre-Bitcoin foundations and precursor material.
- `*-legacy-candidates.json` — preserved raw candidates used during reconciliation.
- `*-reconciliation.json` — reconciliation working records where used.
- `index.json` — high-level year/evidence index.
- `raw/` — preserved supporting raw material where required.

## Rules

1. **Research and edit the year files, not the giant master.**
2. Preserve every permanent `LORE-EVT-####` identifier.
3. A raw discovery event is not automatically a card candidate.
4. Verify dates and claims, preferring primary, project, government, court, regulatory, on-chain and strong contemporary sources.
5. Mark duplicates/context/subevents by relationship instead of independently scoring the same story multiple times.
6. Correct dates in the year evidence layer when research disproves the original raw capture.
7. Card scoring must use sourced/triaged year-file records only.
8. Records still marked as future, unresolved, needs-source/data, or duplicate-linked are not independently scoreable.
9. Do not delete the original raw discovery archive; it preserves provenance and ideas that may later become book/sidebar material.

## Research status

The archive has already been split into year files through 2026. The large 2021–2025 years have been reconciled and marked `YEAR_TRIAGED_AND_SOURCED`. Continue future evidence work directly in these smaller year files.

## Next phase

Finish any remaining weak/deep-cut evidence flags, then add a separate **card scoring layer** so historical importance, LORE/story value, visual potential and duplication are evaluated without changing the underlying history records.
