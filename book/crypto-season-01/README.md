# LORE — Crypto Season One book manuscript

Build the book one approved card at a time. Each numbered chapter draws on the exact approved front and keeps its story, four hidden details, primary source and factual boundary together. The manuscript is editorial source material; trim size, page design, typography, image reproduction, rights and print approval are separate decisions.

| Card | Chapter | Status |
| --- | --- | --- |
| 001 — Blind Signatures | [Approved chapter](001-blind-signatures.md) · [Full-art spread with approved copy v3](proofs/001-blind-signatures-full-art-spread-v3.pdf) · [Earlier full-art v2](proofs/001-blind-signatures-full-art-spread-v2.pdf) | Story and clues approved for book and site; book page design remains a review proof |

| 002 - Cypherpunk Manifesto | [Approved chapter](002-cypherpunk-manifesto.md) · [Full-art spread with approved copy v2](proofs/002-cypherpunk-manifesto-full-art-spread-v2.pdf) · [Earlier v1](proofs/002-cypherpunk-manifesto-full-art-spread-v1.pdf) | Card and chapter approved for book and site; book page design remains a review proof |
| 003 - Hashcash | [Approved chapter](003-hashcash.md) · [Approved editorial spread v3](proofs/003-hashcash-full-art-spread-v3.pdf) · [Review v2](proofs/003-hashcash-full-art-spread-review-v2.pdf) | Card, rarity, story and page design approved for book and site; physical reproduction pending |

The other 97 chapter numbers should be added only as their collector sequence is approved. The previous 11 approved artworks retain their separate art approvals and do not gain chapter numbers from this table.

## Proposed two-page entry pattern

The two-page entry gives page one entirely to the approved illustration, edge to edge. Page two carries the number, rarity, date, phrase, historical explanation, decoded art details and primary-source/art note. The [earlier card-front layout](proofs/001-blind-signatures-spread-v1.pdf) remains available for comparison. The chapter Markdown is the approved copy master. Run the matching `sync_001.py`, `sync_002.py` or `sync_003.py` after editing a chapter to refresh its website JSON, then `--check` to verify the mirror. Each spread builder reads its chapter directly. The A4 PDFs are editorial studies; final book trim, bleed, binding, colour reproduction, rights and printer specifications are not locked. The 1060×1484 source art is roughly 128 DPI at full A4 and needs a higher-resolution source or a smaller page before production.
