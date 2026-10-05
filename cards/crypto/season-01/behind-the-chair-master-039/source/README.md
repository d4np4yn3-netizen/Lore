# Recovered 039 production source

The saved Library card PNG/PDF and two-page book PDF are the preserved production artifacts. Do not replace them merely to change metadata or file timestamps. The approved native artwork must always retain SHA-256 c6944000f8ff929d6d793db39aeb994e3befc2300a554e0e2f6a7279f7c79239.

- `common.svg` is the locked Common template from current main commit 946bf9949f356ca2d3a0b73e4a2c3baffd58081a
- `build_039_final_front.py` recreates the SVG, card PNG, and card PDF into a separate `rebuilt` directory by default; it asserts the art hash and preserves the locked geometry
- `build_039_spread.py` recreates the two-page A4 book from the recovered chapter into a separate `rebuilt` directory by default
- `approved-copy.json` is the complete story, five clues, source/art note, and source URLs extracted verbatim from the approved PDF; only line-wrap whitespace was normalized
- `grounded-clue-crops.json` provides native-art coordinates for the five actually visible clues; its explanatory copy is unchanged from the book
- `qa_039_assets.py` verifies preserved native pixels, QR decoding, copy integrity, geometry, and image dimensions
- `source-verification.md` records fresh verification against the historical primary sources and the physical reproduction caveat

Dependencies: Python, Pillow, reportlab, pypdf, PyMuPDF, qrcode, zxing-cpp, and Inkscape. Bundled DejaVu fonts and fontconfig preserve typography. Rebuilds are QA/source-recovery operations; they do not grant new physical reproduction approval.
