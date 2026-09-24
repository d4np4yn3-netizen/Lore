# Crypto print template approval — 24 September 2026

## Decision

Dan approved **LORE-CRYPTO-PRINT-v1.0** as the print master for Crypto Season One
across all six rarities.

Approval sequence:

> “what about same size and bold like the BITCOIN text above BIRTH OF HODL”

followed by:

> “ok, thats the one, this is approved, can we update the github for the latest
> apporved template, across all rarity and also the print ready size so all cards
> going fit the same size and tmeplate”

## Approved template change

The short moment phrase beneath the title keeps its existing position, rarity
colour and tracking, but now uses the same **25-unit size** and **700 bold weight**
as the crypto subject label such as `BITCOIN`.

No other internal card geometry is redesigned by this approval.

## Printer master

The supplied poker template defines:

- full bleed: **816 × 1110 px at 300 DPI** — 2.72 × 3.70 in
- finished cut: **744 × 1038 px** — 2.48 × 3.46 in
- safe area: **684 × 981 px** — 2.28 × 3.27 in

The complete locked LORE-FRONT-v4 card composition is uniformly inset with
`translate(46.515 48.921) scale(0.8033)`. It is not stretched and its internal
logo/title/QR/badge/footer relationships remain fixed.

The nearest stroke edge of the existing outer rarity border is approximately
**1.40 mm inside the cut**.

## Scope

Applies to crypto front print derivatives for:

- Common
- Uncommon
- Rare
- Epic
- Legendary
- Mythic

Canonical master:
`cards/crypto/master/print-v1/`

Existing approved card artwork and historical exports remain unchanged until
each card is deliberately rebuilt as a new print derivative.

Creator cards remain on their existing approved layout rules.

## Remaining release gates

This approval locks the template and printer-file geometry. It does not by
itself confirm a received physical proof, final live QR routes, a physical QR
scan test, stock/finish choice or a production quantity.
