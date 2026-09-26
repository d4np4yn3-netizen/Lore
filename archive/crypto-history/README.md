# LORE Crypto History Archive

**Status: ACTIVE RESEARCH — started 25 September 2026**

This directory is the canonical research archive for the history behind LORE Crypto.

The archive is deliberately larger than any physical card season. **An archive event is not automatically a card.** Research first; select cards later.

## Source of truth

- `years/YYYY.json` — **canonical working event records**, split by current event year.
- `years/index.json` — canonical shard index and event counts.
- `taxonomy.json` — controlled branches and research statuses.
- `events.json` — **legacy migration snapshot only**; do not use for routine evidence research or scoring.
- `README.md` — archive rules and workflow.

The archive was migrated to year shards on **26 September 2026** after the master file grew to 1,229 events and became too large for reliable connector reads. Research, verification, duplicate consolidation and scoring now happen in the relevant year file.

## Permanent IDs

Every historical event receives a permanent `LORE-EVT-####` identifier. This ID never becomes the physical card number. Season and card numbering remain separate so the archive can grow without renumbering history.

## Research rule

Newly captured events start as `RESEARCH_REQUIRED`. They are not treated as historically verified merely because they appear in the archive. Promote an event to `VERIFIED` only after its date, wording and material claims are checked against appropriate sources, prioritising primary sources where practical.

## Selection tiers

- **CORE** — central to understanding crypto history.
- **MAJOR** — historically significant but not necessarily essential.
- **LORE** — culturally important, strange, infamous or especially strong storytelling.
- **DEEP_CUT** — worthwhile archive material that may not merit a physical card.

These are research labels, not card rarity.

## Event vs card

One physical card may represent several linked archive events. For example, the DAO creation, raise, exploit, fork debate and chain split can remain separate historical records even if only one or two physical cards are eventually selected.

## Planned record fields

Permanent ID, date/date range, title, summary, why it matters, era, branches, chain/project, people, jurisdiction, research tier, source confidence, primary sources, secondary sources, related events, causal links, visual potential, book-story potential, Easter eggs, existing LORE artwork, card selection status, season, card number and rarity.

## Current seed

The first seed captures major moments already identified during the initial LORE research discussion. It is intentionally incomplete. The next phase expands chronologically and branch-by-branch, including governments, bans/adoption, exchanges, hacks, DeFi, NFTs, stablecoins, mining, privacy, culture, people and human lore.
