# CryptoKitties 046 reproducible card and book

From this numbered master, run `python source/build_card.py --repo-root ../../../.. --data card-data.json --out-dir rebuilt-card`. The script auto-detects the root if `--repo-root` is omitted. It validates the exact pinned master, fonts and corrected art before rendering; the existing title lines read CRYPTO / KITTIES. Dependencies are Pillow, qrcode, pypdf and Inkscape.

Run `python build_book.py` to reproduce the book using the exact corrected art, locally archived story/source definitions and repository-pinned fonts. Dependencies are reportlab, Pillow and PyMuPDF. It outputs the book PDF, previews, chapter/content and clue crops beside the script.

The approved card uses the 816×1110 300-DPI HISTROVE print canvas, 744×1038 trim and 684×981 safe area. Exact PDF boxes and QR decodes are recorded in card-final-qa.json. Native artwork remains 1060×1484.

The immutable-package-manifest.json preserves the delivered Library package layout and hashes; it is a manifest of that package, not a file-path map for this flattened repository directory. Original-review-v1.png preserves the earlier image. The final art is the approved symbol-removal edit; imagegen caused minor background texture variations that are disclosed in source provenance.

Physical printer/sample acceptance, phone-camera scanning and commercial reproduction rights remain separate.
