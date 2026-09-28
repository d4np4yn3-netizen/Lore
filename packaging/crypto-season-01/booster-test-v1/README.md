# LORE Crypto Season 01 booster - physical test v1

New packaging composition for Dan's review and sample order, prepared 28 September 2026. This is a test-print candidate, not a production approval. The source art, logos and brand colours are the exact approved assets already in this repository.

## Send to the pack printer

Upload [`LORE-Crypto-S01-Booster-Test-v1-300dpi.png`](LORE-Crypto-S01-Booster-Test-v1-300dpi.png), or use the [clean vector PDF](LORE-Crypto-S01-Booster-Test-v1.pdf) if the printer accepts PDF. Both cover the full 172 x 132 mm page of the [supplied QPMN template](Booster-Pack-Printer-Template.pdf). Print at 100% / actual size. The PNG is 2032 x 1560 px, tagged at 300 DPI. The PDF has the exact media box and trim geometry from the template. No dielines or guides are printed in these two clean files.

The [preview](LORE-Crypto-S01-Booster-Test-v1-Preview.png) shows the front and an indicative assembled back. The [proof PDF](LORE-Crypto-S01-Booster-Test-v1-Proof.pdf) has a separate flat guide overlay with fold, cut and heat-seal areas. **Do not send the proof PDF as the artwork.**

Front: approved HODL v2 and Birth of Doge v2 art beneath the exact gold/white LORE primary lockup. Back: approved Whitepaper 005 art, exact compact lockup, six approved rarity names, and a QR to `https://lore-site-v1.vercel.app/`. The QR digitally decodes at 28.22 mm including its four-module quiet zone. All lettering and logo geometry in the [SVG source](LORE-Crypto-S01-Booster-Test-v1.svg) and PDF are vector outlines; approved artwork remains embedded at original resolution. [Manifest](LORE-Crypto-S01-Booster-Test-v1-Manifest.json) records source SHA-256 hashes, page geometry and QA.

Flat printed gold is `#D4AF37` on `#0B0B0B` black. The printer has not supplied an ICC profile, substrate or metallic-foil separation. The sample needs a physical cut/fold, colour and printed QR scan check before any larger production order. Pack quantity and pull-rate claims have deliberately been left off.

`build_booster.py` is the deterministic layout source. It reads the existing `brand/`, `cards/crypto/season-01/` and `cards/master/front-v3/source/fonts/` paths from this repository, and writes the files into this folder. Python packages: Pillow, fontTools, CairoSVG, PyMuPDF, pypdf and qrcode. Preserve the approved source files when rebuilding; any visible pack layout revision needs a new review version.
