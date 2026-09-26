# Year Evidence Files

The original `events.json` remains the permanent discovery archive and retains every `LORE-EVT-####` ID.

Evidence work is now written into year-sized files because the master archive is large enough to exceed connector read limits. These files are the working source for research, deduplication, canonical-event selection and later card scoring.

Rules:

- Never renumber an existing `LORE-EVT-####` master ID.
- `master_event_id: null` means a researched event has not yet been reconciled to a raw master row.
- Primary/government/project sources are preferred.
- Context/era nodes are not automatically card candidates.
- Duplicate or related raw events should eventually point to a single canonical event.
- Card scoring starts only after an event is evidence-ready.
