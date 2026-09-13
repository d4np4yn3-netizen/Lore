# Rarity badge spacing approval — 13 September 2026

Dan identified inconsistent space around rarity labels. Inspection confirmed that v3 used `max(180, 24 × character count + 50)`, producing unequal right-side gaps, especially for Rare and Epic.

The comparison presented the actual six existing badges on the left and measured, equal-padding badges on the right. The proposal retained font, tracking, colours, border treatment and height, and used 22 units on each side of the visible word with centred lettering.

Dan's exact approval: **“agreed, right hand version is approved”**.

The accompanying proposal explicitly covered applying the rule to the approved cards, all six templates, the renderer and GitHub rules. This record authorises that mechanical badge change. It does not authorise changes to illustrations, copy, logos, other geometry, physical size or the shared back.

Implementation: **LORE-FRONT-v4 / LORE-CARD-v1.1 / LORE-BADGE-v1.0**. The [standard](../cards/12-RARITY-BADGE-SPACING.md) and [machine-readable specification](../cards/master/front-v4/badge-spacing.json) are authoritative. [Current approved card files](../cards/creators/asmongold/current-cards.json) list the new versions and hashes. All old files are retained; each new PNG has zero pixel differences outside its badge. Each new SVG changes only badge width and label x/y.

Visual rule approval is recorded independently of GitHub merge status, primary-source verification, live QR release and print approval.
