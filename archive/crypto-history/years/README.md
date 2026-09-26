# LORE Crypto History — Year-by-Year Canonical Archive

**Status: ACTIVE RESEARCH**

The original `../events.json` remains the **raw discovery pool** containing broad candidate events.

From this point forward, the canonical researched archive is built **year by year** in this directory.

## Rule

Each year gets its own JSON file:

- one event per historically distinct moment;
- exact date/date range where evidence supports it;
- concise factual summary;
- why it mattered;
- research tier;
- source confidence;
- primary and secondary sources;
- duplicate/context relationships;
- card-scoring fields left blank until the year is research-complete.

## Workflow

1. Pull all raw candidates for one year.
2. Research each candidate.
3. Correct dates and wording.
4. Merge duplicates into a canonical event.
5. Mark broad trends as context rather than fake point events.
6. Add missed events discovered during research.
7. Lock the year as `RESEARCH_COMPLETE`.
8. Only then score that year's canonical events for card potential.

## Status values

- `VERIFIED`
- `VERIFIED_WITH_QUALIFIER`
- `CONTEXT`
- `DUPLICATE`
- `REJECTED`
- `RESEARCH_NEEDED`

## Card scoring

Card scoring must not begin until the event is verified. Event IDs remain independent from future Season/Card numbers.
