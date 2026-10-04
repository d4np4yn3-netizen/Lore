# 032 deterministic publication builders

These files reproduce the approved 032 card and two-page spread from the unchanged selected artwork and canonical chapter. They do not generate new artwork or confer physical print approval.

- `build_032_final_front.py`: applies the approved ETHEREUM / GOES LIVE text, Mythic rarity, date, caption, collector number and stable `/crypto/032/` QR to the archived Mythic print template; exports SVG, 816 × 1110 PNG at 300 DPI and a one-page PDF with the specified media and trim boxes
- `mythic.svg`: exact locked print-template input used by the builder, preserving LORE-CRYPTO-PRINT-v1.0 geometry
- `card-layout-check.json`: output geometry, measured text widths, embedded-art hash, selected copy and QR payload
- `build_032_spread.py`: reads `book/crypto-season-01/032-ethereum-goes-live.md` and the selected `art.png`, then exports the full-art/story A4 pair
- `card-intermediate.pdf`: intermediate front PDF retained from the deterministic printer export

Run from a complete repository checkout with the existing `cards/master/front-v3/source/fonts`, fontconfig and locked template assets present. Dependencies include Python, Pillow, qrcode, ReportLab, pypdf and Inkscape; the spread also uses the installed DejaVu Serif font. The builders resolve paths relative to their canonical repository location. Run `python book/crypto-season-01/sync_032.py --check` to verify the chapter/website copy mirror without changing it.

Rebuilding is optional: preserve the approved existing output bytes for publication and compare any rebuilt output against the hashes in `../print-v1-manifest.json` before substitution. The native illustration must remain 1060 × 1484 with SHA-256 `5db2bd45176367f74c595925fecb3d537b5a493966ca02850178903563422ef0`. This source package has no upload or deployment action.

Digital QR decoding is recorded separately from live-route verification and a physical phone-camera test. Physical card print and book reproduction releases remain false; full-A4 art resolution is approximately 127 PPI.

Digital verification uses Pillow, qrcode, reportlab, pypdf and zxing-cpp; Inkscape and Poppler are required system tools. Run `qa_032_assets.py` after both builders. The exact committed DejaVu Sans files are loaded from the shared front-v3 source folder; the established book template uses system DejaVu Serif. The QR check renders the actual printer PDF at 300 dpi before decoding it.
