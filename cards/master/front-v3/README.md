# LORE-FRONT-v3 reusable master

This directory pins the exact selected Asmongold v3 front references and the reusable layout. The full specification and approval scope are in [the front standard](../../07-FRONT-LAYOUT-AND-ART-MASTER.md).

- `references/fronts`: six unchanged PNGs selected by Daniel.
- `references/art`: six unchanged illustration-only PNGs used in those fronts.
- `templates`: one SVG per rarity, preserving the selected geometry and styling. Illustration and QR content are empty insertion slots; example text is retained as a fit reference.
- `source/render_card.py`: inserts reviewed artwork, text and a generated vector QR into a template.
- `source/fonts` and `source/fontconfig.xml`: the exact fonts and mapping used by the selected reference renders.
- `source/asmongold-reference-data.json`: the inherited provisional moment/source data and reference content.
- `source/asmongold-v3-edit-prompts.md`: exact composition-edit prompts, with provenance; new creators use the general style rules rather than inheriting Asmongold's physical features or scenes.
- `manifest.json`: hashes of the pinned assets.
- `qa`: measured validation of the saved master.

## Render an existing reference

Install Pillow and qrcode in your Python environment, and make Inkscape available. From the repository root:

```bash
python3 cards/master/front-v3/source/render_card.py --reference 6 --demo --out /absolute/output/path/mythic.svg
```

The SVG and PNG are written together. `--demo` is required for the reference example.com QR routes.

## Fill a new card

Create a data example, edit its content and render it to a new output directory:

```bash
python3 cards/master/front-v3/source/render_card.py --write-example /absolute/output/path/card.json
python3 cards/master/front-v3/source/render_card.py --data /absolute/output/path/card.json --out /absolute/output/path/card.svg
```

The JSON fields are `rarity`, `creator`, `title_line_1`, `title_line_2`, `context`, `moment_label`, `set_label`, `artwork` (PNG path), and `qr_url`. Add `confirmed_lore_owned_route: true` only after the real LORE destination has been checked. Demo-only review work uses example.com with `--demo`.

Text overflow is rejected rather than shrinking or moving the master layout. A renderer success is not artistic approval: review the illustration, likeness, moment accuracy and the full set. New QR lengths can increase density; decode the export and test the final physical card before release.

The front SVG compositions embed raster art. They are editable mixed-media files, not entirely vector illustrations. The common back is outside this master directory because it remains under review.
