# LORE — current status

Updated 2026-09-26. Read with AGENTS.md and PROJECT-MEMORY.md.

## Latest: 001 Blind Signatures and print-first approval — 26 September 2026

Dan approved 001's exact illustration, **Legendary** rarity, bold
`UNTRACEABLE PAYMENTS.` phrase and complete numbered front. The approved
printer-sized front and editable SVG are in
`cards/crypto/season-01/blind-signatures-master-01/`. The current v2 816×1110, 300-DPI front has a QR for the public Vercel route
`https://lore-site-v1.vercel.app/crypto/001/`, which redirects to the story,
four clues and the original Chaum paper. The owner-private QR v1 and prior
review proof remain historical. Dan reports the digital QR scan works. Physical proof and printed camera scan
remain open; `print_release` is false.

The 11 earlier approved Crypto cards remain in the canonical repository but
are not listed on the public site; they still have print derivatives with demo
QRs. Their collector numbers and the remaining rarity allocation are not yet
approved. The phrase treatment is bold at the subject-label size for the print
master. Keep each new approval with its print derivative. The first book
entry has a full-art A4 editorial comparison in
`book/crypto-season-01/proofs/001-blind-signatures-full-art-spread-v2.pdf`,
alongside the earlier card-front spread and reproducible script. Book wording
and page layout await separate review; the 1060×1484 art needs a higher-resolution
source or smaller trim for production. Final trim and print specifications
are undecided.

## Active milestone: 100 card briefs and 400 Easter egg concepts

Dan requested a brief and at least four Easter eggs for every selected card. The complete **100-brief / 400-clue draft pack** is at `cards/crypto/season-01/briefs/v1/README.md`, with individual briefs, a combined reading file, structured data and coverage QA. Each brief specifies story, scene, composition, mood, factual boundaries, four clue locations/meanings, copy status and sources.

All **11 approved artworks and registers are unchanged**. Four clue entries retain details already described in approved records; 396 are new proposals. Additional clues on approved cards require separate revision approval. The 89 new moment choices and working titles remain proposals. No new illustration, phrase approval, rarity allocation, live QR or print release was created.

First Transfer/First Halving remain paused; parked Slush Pool/Silk Road concepts remain parked. Other existing holds are untouched. Historical references, symbolism and cross-card callbacks are labelled; inherited source/date flags remain open. This is complete briefing, not a claim of 400 newly verified historical props.

The underlying **250-event timeline = 100 card moments + 150 supporting events**, spanning 1976–26 September 2026, remains at `archive/crypto-history/selection/v1/README.md`. Proposed cards stop at 2025; 2026 context is provisional.

Next: review one active card's brief and four clues, resolve its targeted evidence/copy gaps, then make a separately reviewed illustration. CASH OUT remains the recorded proposed next concept. Do not restart exhaustive research on all 1,229 discovery candidates or automatically resume held art.

## Current milestone: Crypto print rollout complete

All **11 approved Crypto Season One cards** have been converted to **LORE-CRYPTO-PRINT-v1.0** and remotely verified beside their approved masters.

Canonical print master: `cards/crypto/master/print-v1/`.
Printer geometry: **816×1110 full bleed @300 DPI; 744×1038 cut; 684×981 safe**.
Uniform transform: `translate(46.515 48.921) scale(0.8033)`.
Crypto phrase: **25 / 700**, with position, tracking and rarity colour preserved.
QA: `cards/crypto/master/print-v1/qa/approved-card-conversions.json`.

The original approved PNG/SVG/art files were not replaced. Every print derivative retains the approved wording, rarity and QR status. All QRs remain **DEMO_ONLY** and `print_release` remains **false**.

## Next physical-print action

Use the converted files for physical print samples. Check the physical cut/bleed/safe result and scan the printed QR before any production release. Live QR routing, CMYK/production colour decisions and foil separations remain separate gates.

## Permanent crypto references

Before EVERY generation/edit inspect and directly supply BOTH pinned artworks:
- cards/crypto/season-01/birth-of-hodl-master-02/art.png
  SHA-256 412f3c10be87a73afbf04c292d5bae605382189f6f34bd925b6cfb77555632d1
- cards/crypto/season-01/birth-of-doge-master-02/art.png
  SHA-256 6b106345ef9c6564e7ede345196eb34120eb19b5e4a1240af0f33b9e5876f422
Characters, props and backgrounds use LORE-CRYPTO-STYLE-v1.1. New approvals do
not change this pair.

## Compact working method

1. Keep this file short and update it in place after each completed milestone: active task, exact paths, approval, verified delivery, next action.
2. Read current status first. Load only relevant standards and files. Historical recovery logs are for resolving a specific gap; do not reconstruct every past chat on routine continuation.
3. Work through one reviewable card milestone at a time: illustration, layout/copy, approval, upload verification. Preserve approved work.
4. Existing explicit approval for an unchanged file persists across chats. Check the recorded approval and delivery before asking again or retrying an upload.
5. Transfer assets as files using an available authorized git/file-transfer route. Keep base64, image bytes, embedded-image SVG payloads and large logs out of model-visible messages. If a connector is necessary, handle payloads programmatically and return only paths, sizes, hashes and results.
6. A large file may return an empty content field through GitHub's contents API. Check its blob SHA; do not assume it is missing or empty, or re-upload it unnecessarily.
7. Verify the actual remote file/hash before saying uploaded. Save a small checkpoint for an incomplete transfer and resume only missing work.
8. Report the outcome briefly with the file or commit link. Do not create another long handover for every interruption.
