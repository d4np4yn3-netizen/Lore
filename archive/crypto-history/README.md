# LORE Crypto History Archive

**Status: EVIDENCE RESEARCH — active 26 September 2026**

This directory is the canonical historical research archive behind LORE Crypto.

## Database layers

### 1. Master candidate database

Use:

- `master/index.json`
- `master/years/YYYY.json`

The master contains every captured candidate event and preserves the permanent `LORE-EVT-####` identifiers.

**Do not edit `events.json` anymore.** It is retained only as the legacy snapshot from before the database was split by year.

### 2. Evidence-ready research

Year research files currently live under `years/YYYY.json`. These contain sourced, corrected and editorially cleaned canonical history used for eventual card scoring.

The evidence layer distinguishes:

- verified events
- exact-date corrections
- duplicates / subevents
- context or era nodes
- disputed claims
- records requiring stronger evidence

## Permanent IDs

A `LORE-EVT-####` master ID never becomes a physical card number.

A master event might become:

- Season 1 Card #043
- Season 2 Card #017
- a supporting book/timeline event
- or no physical card at all

## Selection tiers

- **CORE** — central to understanding crypto history
- **MAJOR** — historically significant
- **LORE** — culturally important, strange, infamous or especially strong storytelling
- **DEEP_CUT** — worthwhile archive material that may not justify a physical card

These are research labels, not rarity.

## Research principle

**Event ≠ card.**

Several historical records can collapse into one strong physical card. The DAO creation, fundraise, exploit, debate and fork can remain separate historical records while ultimately producing only one or two cards.

Card scoring starts only after the relevant historical record has been evidence-reviewed.

## Evidence-phase storage

The original `events.json` remains the broad-capture archive and preserves the permanent `LORE-EVT-####` IDs gathered during discovery.

Because the discovery file has grown beyond 1,200 records, detailed source verification is now stored in smaller canonical year shards under `years/YYYY.json`. These files are the working source of truth for the evidence phase and are designed to avoid oversized-file read/write failures.

Year shards:

- contain canonical researched events rather than blindly copying every raw discovery row;
- retain `source_event_ids` where a canonical event maps back to known discovery records;
- explicitly mark records as `VERIFIED`, context, or `RESEARCH_NEEDED...`;
- keep card scoring at `NOT_SCORED` until the research/deduplication pass is complete;
- may merge several discovery rows into one historical event when they describe the same underlying moment.

The master archive will be regenerated/indexed from the year shards after the evidence pass instead of repeatedly rewriting the oversized discovery JSON.
