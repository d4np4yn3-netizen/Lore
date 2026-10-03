# LORE Crypto Season One site

Collection: 001–027, including 022 BURIED FORTUNE. Existing card numbers and the redesigned chronological archive are unchanged. All 27 stable /crypto/NNN/ QR routes redirect to /cards/{slug}. The archive has 119 inspected clues, 27 trimmed card previews and 54 book-page previews. Each story, art clue and source/art note mirrors its numbered Markdown chapter in book/crypto-season-01 through its sync_NNN.py script; run with --check before deployment. Exact artwork, printer fronts and full-art two-page editorial PDFs are linked from each card.

Keep stable printed QR routes when changing domains. Visual approval, source checks, live QR verification, physical print and book reproduction/rights approvals remain separate.

Existing original-asset links stay pinned to ac8d3634. Each card may provide media.assetOrigin for a later asset commit. The 022 original artwork, front and book links are pinned to the immutable asset commit dc6e02cbac384c2a3e64c2a706c106d6c8de3da1.

Build: cd site && npm install && npm run build. Discovery and media integrity checks: node scripts/check-discovery.mjs. The project exposes no lint script.
