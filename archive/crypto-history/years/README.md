# LORE Crypto History — Year Shards

This directory is the **canonical working store** for the crypto-history archive.

- One JSON file per event year.
- Permanent `LORE-EVT-####` IDs are preserved.
- Evidence research, duplicate consolidation and later card scoring should update the relevant year file.
- `index.json` records counts and paths.
- If research corrects an event into a different year, move that record to the corrected year's file during normalization.
- `../events.json` is retained temporarily as a legacy snapshot only; do not use it for routine research edits.

This structure replaces repeated reads/writes of the oversized 1,229-event monolith.
