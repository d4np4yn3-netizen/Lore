# Historical LORE revision — superseded 6 October 2026

Retained unchanged artwork and geometry for reproducibility. Current HISTROVE printer files: `cards/crypto/print-ready/histrove-v1`; future templates: `cards/crypto/master/histrove-print-v1`. Do not use this historical branding for new print runs.

# LORE-CRYPTO-PRINT-v1.2

Dan approved the exact 001 even-frame proof and authorised its application to the 39 numbered cards on 6 October 2026. See [approval](approval.json), [specification](print-spec.json) and [current printer files](../../print-ready/v1.2).

This is the default print template for all six Crypto Season One rarities going forward. Creator card templates, original illustrations and historical v1.0 print masters remain unchanged.

The template height is 1287.625 units at a constant width of 900. Uniform element scale is 672/886; translation is (66.690744921, 66.690744921). Border height increases by 27.625 units. The lower labels, QR and fade move down by that amount; the logo/header keep their local coordinates. Artwork height becomes 1259.625 with proportional centre fill. This is the specific reviewed layout exception. Do not stretch the illustration, logo, lettering or QR.

- [Six templates](templates)
- [New-card renderer](source/render_print_card.py): same JSON fields as v1.0, with explicit 816×1110 PNG export at 300 DPI.
- [Existing-front converter](source/convert_front.py): transforms a source print-v1 front without regenerating any art or QR.
- [Collection builder](source/rebuild_collection.py): rebuilds the current 39-card export set and review documents.
- [Original reviewed 001](approval): exact files Dan approved, preserved with hashes.
- [Original back v6 SVG](source-assets/shared-back-v6.svg): exact no-tagline source, recovered from `review/shared-back-v6-print` and hash-pinned.

Use the supplied `cards/master/front-v3/source/fontconfig.xml` and fonts. Required Python packages for the batch builder: Pillow, pypdf, reportlab, PyMuPDF and zxing-cpp; Inkscape on PATH. The new-card renderer additionally uses qrcode. Do not re-render with substitute fonts.

Physical printer and sample acceptance are separate from layout approval. New card art, copy and individual exceptions still follow the normal review workflow.
