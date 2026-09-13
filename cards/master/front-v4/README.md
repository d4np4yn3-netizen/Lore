# LORE-FRONT-v4 — current card layout

Dan approved consistent rarity badge padding on 13 September 2026. This version changes only the badge width and lettering position from v3. See [the standard](../../12-RARITY-BADGE-SPACING.md) and [approval record](../../../operations/16-RARITY-BADGE-SPACING-APPROVAL-2026-09-13.md).

- `templates/`: all six current SVG templates.
- `badge-spacing.json`: approved geometry and original measured glyph bounds.
- `source/render_card.py`: current renderer; applies the approved badge rule.
- `source/badge_spacing.py`: shared layout logic and typography checks.
- `source/update_approved_cards.py`: reproducible migration of the four existing cards.
- `source/verify_layout.py`: actual glyph-padding, SVG-change and pixel-preservation checks.
- `references/`: the approved spacing comparison, six layout references and four updated cards.
- `qa/` and `manifest.json`: measured checks and exact hashes.

The original six proof moments in the layout board remain design examples. Current finished cards are listed in [the Asmongold registry](../../creators/asmongold/current-cards.json).

## Render a card

Use Pillow, qrcode and Inkscape. Fonts and their isolated configuration are reused unchanged from `../front-v3/source/`.

```bash
python3 cards/master/front-v4/source/render_card.py --write-example /absolute/path/card.json
python3 cards/master/front-v4/source/render_card.py --data /absolute/path/card.json --out /absolute/path/card.svg
python3 cards/master/front-v4/source/render_card.py --reference 3 --demo --out /absolute/path/rare.svg
```

Input fields and URL safeguards are inherited from v3. Demo `example.com` routes require `--demo`. Live routes require confirmed LORE ownership. Text overflow fails instead of resizing the locked layout.

To check the complete revision, with NumPy also installed:

```bash
python3 cards/master/front-v4/source/verify_layout.py
```

Original v3 files and historical approved card files remain unchanged. Do not rerender an approved file for delivery; use the exact current PNG/SVG and recorded hashes. New design changes require a separate reviewed revision. Physical trim remains 63 × 88 mm; printer preparation and live QR release are separate.
