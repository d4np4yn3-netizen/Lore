# 045 deterministic card build

Place `build_card.py` beside `art.png` and `card-data.json` in the numbered master folder. Run `python3 build_card.py`; repository root is discovered from the current script location, not the working directory. Optional flags: `--repo-root`, `--data`, and `--out-dir`. Use Python 3, Pillow, qrcode, pypdf, and Inkscape.

The original shared HISTROVE Rare template, renderers and repository fonts are hash-pinned. The script never edits them. It creates a temporary template only to preserve the separately approved one-word BITCONNECT title with an empty second title field. The original first baseline, all sizes, tracking, colors, logo, frame, art crop and QR placement are unchanged. Metadata and exact v3 artwork are validated before export.

The printer PDF is exported using the existing shared exporter. Its MediaBox and CropBox are normalized to exactly 195.84 x 266.4 points to prevent a fractional rounding row; content coordinates and scale are unchanged. Existing BleedBox, TrimBox and ArtBox remain exact. The web PNG is a separate trim crop (36,36)-(780,1074), never a replacement for the full-bleed printer PNG.

A regression build in the assembly environment reproduced the approved final PNG, PDF, SVG and web derivative byte-for-byte. See reproduction-check.json. Native artwork is 1060 x 1484; printer PNG is 816 x 1110 at 300 DPI. Physical printing and sample approval remain separate.

The companion book builder is build_book.py, beside art.png. It uses the canonical repository fonts at cards/master/front-v3/source/fonts and writes its two-page PDF, exact shared narrative/clue JSON, chapter and render previews beside the script. The published book is pinned separately under book/crypto-season-01/histrove-v1.
