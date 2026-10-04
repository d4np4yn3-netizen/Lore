# 033 deterministic publication builders

These files reproduce the approved 033 card and two-page spread from the unchanged selected v5 artwork and canonical chapter. They do not generate artwork or confer physical print approval.

- `build_033_final_front.py`: applies ETHEREUM / THE DAO / HACK, Epic rarity, 17 JUN 2016, REMAIN CALM., 033/100 and the stable `/crypto/033/` QR to the archived Epic template; exports SVG, 816 × 1110 PNG at 300 DPI and a one-page PDF with specified media and trim boxes
- `epic.svg`: exact locked LORE-CRYPTO-PRINT-v1.0 template input, Git blob `ba2d3d735fae139f8802c371afa5417ade5fbe19`
- `card-layout-check.json`: measured text widths, output geometry, embedded-art hash, selected copy and QR payload
- `build_033_spread.py`: reads `book/crypto-season-01/033-the-dao-hack.md` and selected `art.png`, exporting the full-art/story A4 pair
- `card-intermediate.pdf`: intermediate file from the deterministic printer export
- `qa_033_assets.py`: verifies art preservation, fixed template geometry, PDF boxes, book pixels and source links, and QR decoding from the final PNG and actual 300-DPI printer-PDF render
- `final-qa.json`: successful final digital QA results; live and physical verification remain separate
- `canonical-033-brief.md`: historical pre-revision brief retained for event identity and planning provenance; its old-vault illustration instructions and proposed clues do not override the approved v5 artwork or current approval record
- `source-verification.md`: historical evidence and interpretation boundaries; current publication approval and QR state are governed by `../approval.json` and `../print-v1-manifest.json`

Run from a complete repository checkout with the existing `cards/master/front-v3/source/fonts`, fontconfig and locked template assets present. Dependencies include Python, Pillow, qrcode, ReportLab, pypdf and Inkscape. The spread additionally uses installed DejaVu Serif. Builders resolve paths relative to their canonical repository location. Run `python book/crypto-season-01/sync_033.py --check` to verify the chapter/website mirror without changing it. Run `python cards/crypto/season-01/the-dao-hack-master-033/source/qa_033_assets.py` after both builders. Digital QR verification uses zxing-cpp and an actual Poppler 300-DPI rendering of the printer PDF.

Preserve the approved output bytes for publication. Compare any rebuild against `../print-v1-manifest.json` before substitution. The native illustration must remain 1060 × 1484 with SHA-256 `f93c3d9bed56839609e27adc0919a3d3dd7680415e048b0d8ad3523ea26e63d5`. This source package performs no upload or deployment.

The stable QR is `https://lore-site-v1.vercel.app/crypto/033/`. Digital decode, live route and physical phone-camera verification are separate. Physical card print and book reproduction release remain false; full-A4 native art resolution is 126.91 PPI. The receiving address is unobstructed but tiny at finished card size.
