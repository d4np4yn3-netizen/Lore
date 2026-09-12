# LORE — Card Anatomy

## Front of card

The front should prioritise artwork. The selected v3 front layout is specified in [the exact front master](07-FRONT-LAYOUT-AND-ART-MASTER.md) and [card-design-lock.json](card-design-lock.json).

Required elements:

- LORE branding in compact form
- creator name
- moment title
- rarity indicator
- bottom-right public moment QR with its clear margin and `WATCH MOMENT` caption
- optional moment number / series identifier
- optional serial number where relevant

Avoid large rules text or clutter.

The card must feel like a premium collectible first.

## Back of card

A universal shared LORE back is under review following the selection of the front QR layout. See [the current back proposal](review/shared-back-v3/README.md). It is not yet approved. The earlier recommendation to put card-specific stories and the QR on every back is superseded by this review direction; do not continue producing those earlier six different backs by default.

The current proposal uses the same brand design across creators and rarities. Card-specific story, dates and sources are carried by the moment page reached from the front. Production/legal marks and any concealed-claim mechanism must be resolved separately before manufacture.

## Public QR

Each card front should contain a small public QR code that resolves through a LORE-owned redirect URL rather than directly to X, YouTube or another platform.

Example conceptual route:

`lore.cards/m/creator-id/moment-id`

The LORE moment page can then link onward to the original source.

### Why use a redirect

- external posts/videos can move or disappear
- destinations can be updated without reprinting cards
- scans return users to the LORE ecosystem
- analytics can measure engagement
- the moment page can show card population, story, creator profile and related cards

## Private claim code

Ownership claiming must use a **separate concealed one-time credential**.

Do not use the visible public QR as proof of ownership.

Possible physical implementations to test:

- scratch-off claim panel
- tamper-evident insert
- concealed code inside packaging
- other secure one-time mechanism

Final implementation requires anti-counterfeit and manufacturing review.

## Moment page

A scan should open a premium mobile page containing:

- full card artwork
- creator name
- moment title
- why the moment matters
- original-source link
- rarity and population information
- serial information where applicable
- creator collection progress / the other five moments
- claim action for legitimate owners

## Original source principle

Where possible, link users back to the creator's original content rather than rehosting their content.

A LORE card should create rediscovery and traffic for the creator, not replace the creator's original work.
