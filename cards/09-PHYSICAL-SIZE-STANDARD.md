# LORE — locked physical card size

**LORE-SIZE-v1.0 — approved by Daniel Payne, 12 September 2026.**

All standard LORE cards use a **63 mm wide × 88 mm high finished size**, in portrait orientation. This is the standard TCG format listed for Pokémon and Magic: The Gathering. See [the manufacturer's size reference](https://printninja.com/card-dimensions/) and [Daniel's approval record](../operations/13-CARD-SIZE-APPROVAL-2026-09-12.md).

| Specification | Locked value |
| --- | --- |
| Finished width after cutting | 63 mm |
| Finished height after cutting | 88 mm |
| Physical aspect ratio | 63:88 |
| Applies to | Both faces of every standard LORE card, all creators and rarities |
| Visual masters | LORE-FRONT-v3 and LORE-BACK-v5 |

Use the metric dimensions as the authority when requesting printer quotes and preparing print files. A printer's literal 2.5 × 3.5 inch format is 63.5 × 88.9 mm and must not silently replace the locked 63 × 88 mm specification.

## Reference artwork and print preparation

The approved 900 × 1260 pixel/SVG-unit masters remain unchanged visual references. Their 5:7 ratio is slightly different from 63:88: uniform scaling to 63 mm wide gives 88.2 mm height. Prepare separate print derivatives against the actual 63 × 88 mm trim template, accounting for that 0.2 mm edge difference while preserving logo, QR and artwork proportions. Do not stretch the artwork or overwrite the pinned reference files.

The finished size excludes bleed. Bleed, safe inset, corner radius, cutting tolerance, stock thickness and ink/foil treatment are still to be set with the selected printer. Extend backgrounds to that printer's bleed boundary; retain the locked trim size. Check the resulting border balance, small text and QR in the physical proof before release.

This decision approves the finished dimensions. It does not claim that printer-ready derivatives, a die-line or a physical proof have already been produced. The current machine-readable specification is [card-design-lock.json](card-design-lock.json).

## Selected Crypto Season One printer template — 24 September 2026

Crypto Season One now has an approved printer-specific front derivative: [LORE-CRYPTO-PRINT-v1.0](crypto/master/print-v1/README.md). The supplied poker template uses **816 × 1110 px full bleed**, **744 × 1038 px finished cut** and **684 × 981 px safe area** at 300 DPI. Its literal 2.48 × 3.46 inch cut is approximately 62.99 × 87.88 mm and is treated as the manufacturing implementation of the locked nominal 63 × 88 mm LORE size.

The crypto front is uniformly inset, never stretched. This selected printer template does not automatically define a creator-card printer derivative or alter the approved shared back master. Physical sample approval remains outstanding.
