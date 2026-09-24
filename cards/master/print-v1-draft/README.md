# LORE print master v0.3 — DRAFT

This folder adapts the locked **LORE-FRONT-v4** visual master to the selected printer's American poker template without redesigning any approved card element.

## Printer geometry

- Full bleed: **816 × 1110 px** at 300 DPI
- Finished cut: **744 × 1038 px** (2.48 × 3.46 in)
- Safe area: **684 × 981 px** (2.28 × 3.27 in)
- Trim origin inside bleed canvas: **x 36, y 36**
- Safe origin: **x 66, y 64.5**

## Approved-layout-preserving solution

Do **not** separately redraw, move or resize the logo, rarity badge, titles, QR, footer, outer border or inner corner lines.

Instead, place the complete locked 900 × 1260 LORE-FRONT-v4 composition inside the trim using one uniform transform:

- scale: **0.8033**
- full-canvas x: **46.515 px**
- full-canvas y: **48.921 px**
- inset inside trim: **10.515 px left/right** and **12.921 px top/bottom**

This preserves the exact approved internal geometry while improving printer tolerance. The existing outer rarity-colour border's nearest stroke edge lands about **1.40 mm inside the cut**, and the complete LORE logo is comfortably inside the printer safe zone.

The remaining full-bleed area uses the locked Bone Black **#0B0B0B**.

## Status

**DRAFT — not production approved.**

The original front-v4 masters and every approved card remain unchanged. This folder contains printer derivatives only.
