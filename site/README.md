# LORE Crypto Season One site

Collection: 001–028, including 022 BURIED FORTUNE and 028 THE ETHER SALE. Existing card numbers and the redesigned chronological archive are unchanged. All 28 stable /crypto/NNN/ QR routes redirect to /cards/{slug}. The archive has 123 inspected clues, 28 trimmed card previews and 56 book-page previews. Each story, art clue and source/art note mirrors its numbered Markdown chapter in book/crypto-season-01 through its sync_NNN.py script; run with --check before deployment. Exact artwork, printer fronts and full-art two-page editorial PDFs are linked from each card.

Keep stable printed QR routes when changing domains. Visual approval, source checks, live QR verification, physical print and book reproduction/rights approvals remain separate.

Existing original-asset links stay pinned to ac8d3634. Each card may provide media.assetOrigin for a later asset commit. The 022 original artwork, front and book links are pinned to the immutable asset commit 984c828300ade347878cac62e4996ff04f2f31a6.

Build: cd site && npm install && npm run build. Discovery and media integrity checks: node scripts/check-discovery.mjs. The project exposes no lint script.

The 028 original artwork, final print front and book links are pinned to immutable asset commit 9fa6524091ba10d5c8c8941277176405c274ac85. Website derivatives preserve all earlier media and are packed separately in display-07.bin.
