# LORE Crypto Print Master v1.0

**Status: APPROVED + 11-CARD ROLLOUT VERIFIED — 24 September 2026**

This is the production-layout master for **Crypto Season One** front print derivatives.
It applies to **Common, Uncommon, Rare, Epic, Legendary and Mythic**.

It does **not** replace or overwrite the historical 900 × 1260 LORE-FRONT-v4
visual masters or existing approved card exports. It creates a deterministic,
printer-sized derivative standard for the crypto collection.

## Printer canvas

- full bleed: **816 × 1110 px @ 300 DPI** — 2.72 × 3.70 in
- finished cut: **744 × 1038 px** — 2.48 × 3.46 in
- safe area: **684 × 981 px** — 2.28 × 3.27 in
- cut origin: **x 36, y 36**
- safe origin: **x 66, y 64.5**

The complete locked front geometry is uniformly inset with:

- scale **0.8033**
- canvas translation **x 46.515, y 48.921**
- no stretching
- no independent repositioning of the logo, title, QR, rarity badge or footer

This places the nearest edge of the existing outer rarity border about **1.40 mm**
inside the cut while preserving the approved card proportions.

## Approved crypto phrase treatment

Dan approved the moment phrase under the main title at the **same size and bold
weight as the subject label** (for example `BITCOIN`), while keeping the phrase
in its rarity colour and retaining its existing position/tracking.

`moment-context` is therefore:

- DejaVu Sans
- **25 units**
- **700 bold**
- letter-spacing **1.1**
- baseline unchanged at **y 1152**

This is a crypto-specific approved template revision. Creator cards remain on
their existing approved front rules unless separately changed.

## Workflow

All **11 approved Crypto Season One fronts** now have separate `LORE-CRYPTO-PRINT-v1.0` PNG/SVG derivatives stored beside their approved masters. Each card folder also contains `print-v1-manifest.json`, and the original visual master pointers remain unchanged.

Remote blob verification passed for all 11 PNGs, all 11 SVGs and all 11 print manifests. Conversion QA and cut-review sheets are in `qa/approved-card-conversions.json` and `qa/cut-review-*.jpg`. The six templates also contain the non-visual nested SVG close required for valid XML.

Physical proof, final QR routes and production release remain separate gates.
