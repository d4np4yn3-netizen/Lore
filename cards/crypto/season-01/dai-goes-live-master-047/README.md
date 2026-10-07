# HISTROVE Crypto 047 Dai Goes Live

Final card and two-page A4 book package using the approved glass-experiment v8 artwork unchanged.

- Date: 18 December 2017
- Subject: MakerDAO
- Rarity: Rare
- Phrase: DAI IS NOW LIVE!
- Collector number: 047/100
- QR destination: https://lore-site-v1.vercel.app/crypto/047/

The card uses the locked HISTROVE-CRYPTO-PRINT-v1.0 geometry: 816 x 1110 pixels at 300 DPI; trim 744 x 1038; safe area 684 x 981. The PDF preserves exact media, bleed, trim and safe-area boxes, native artwork, outlined type and vector frame/QR.

The book contains the complete unchanged illustration followed by vector story text, four details and linked sources. The wrench is visible in the book's full illustration and closeup; the card's standard title/QR region obscures it.

## Resolution and release limits

The approved art is 1060 x 1484 pixels. Its effective resolution on the A4 book art page is 128.21 PPI. Native artwork was intentionally retained; the user deferred book-resolution changes to finish the cards. This package does not assert printer acceptance, physical-sample approval or press clearance.

## Reproduction

The source lock pins the canonical renderer, Rare template, font configuration and fonts at repository commit 779f93a7eaa66f759557fe3847a3ae05c0f98082. Use Python with Pillow, qrcode, pypdf, ReportLab, PyMuPDF and Inkscape.

Card: python3 source/build_card.py --repo-root /path/to/Lore --out-dir /desired/output

Book: python3 build_book.py from its canonical repository location. The book builder uses the pinned fonts in cards/master/front-v3/source/fonts.

Approved illustration bytes: e144c21d3a83cf3f96b39ffb1822f7bc4848fafd96769dc15610cc3c95e93bd8
