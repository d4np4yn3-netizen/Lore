# LORE print master v0.1 — DRAFT

This folder adapts the locked **LORE-FRONT-v4** visual master to the selected printer's American poker template without changing the approved LORE master files.

## Printer geometry

- Full bleed: **816 × 1110 px** at 300 DPI
- Finished cut: **744 × 1038 px** (2.48 × 3.46 in)
- Safe area: **684 × 981 px** (2.28 × 3.27 in)
- Trim origin inside the bleed canvas: **x 36, y 36**
- Safe origin: **x 66, y 64.5**

## Zero-drift transform

The existing 900 × 1260 LORE-FRONT-v4 layout is uniformly scaled by **0.8266666667** so its width is exactly 744 px. That produces a height of 1041.6 px, so the print derivative is centred vertically at **y 34.2**, allowing a symmetric **1.8 px crop** at the top and bottom of the finished trim. Nothing is stretched.

A full-canvas Bone Black (#0B0B0B) background supplies bleed beyond the cut line. The approved card geometry is otherwise unchanged in this draft.

## Review before promotion

This is deliberately **not production approved**.

Two items need Dan's visual decision before this becomes the new production template:

1. The top-right LORE logo begins about **1.37 px / 0.12 mm above** the printer safe line after zero-drift scaling.
2. The thin rarity-colour outer border sits very close to the cut line: its centreline is about **0.70 mm inside trim**, with the near stroke edge about **0.53 mm inside trim**. A small cutting shift may therefore make border weight look uneven.

Do not alter the locked front-v4 masters. Any approved print-specific geometry change should be recorded here as a new print revision and applied only to printer derivatives.

## Files

The six rarity templates in `templates/` are print-canvas derivatives with hidden cut/safe guides. Use `LORE-Print-Guide-v0.1.svg` for review/overlay.
