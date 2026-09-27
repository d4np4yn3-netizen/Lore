# LORE Crypto Season One site

This site publishes approved cards one at a time. The collection contains 001 Blind Signatures, 002 Cypherpunk Manifesto, 003 Hashcash and 004 RPOW. Their stable QR destinations are `/crypto/001/` through `/crypto/004/`, each redirecting to its detail page. The stories, clues and source notes mirror approved book chapters in `app/cards/content/001.json` through `004.json`; run the corresponding `book/crypto-season-01/sync_*.py --check` before deployment.

Keep the printed QR destination stable when a custom domain is added, and verify the live destination before preparing each print-ready card. Card artwork and the season register elsewhere in the repository are preserved independently of the published collection.
