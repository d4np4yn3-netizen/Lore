# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: Ninja Common approved, uploaded and verified

Dan approved **PON / PON — Common / Moment 01 of 06**: **“Ok approved for upload, this turned out better than I thought”**.
Phrase: **THE FIRST OF 2018!**, supplied by Dan and approved on the complete card.

Canonical PNG: cards/creators/ninja/pon-pon-master-01/LORE-Ninja-Pon-Pon-Common-v1.png; matching SVG, original art.png, approval, source notes and hash manifest are beside it. Preserve exact review revision 2 (the phrase-added version), the hand-drawn scene, red/yellow circular burst with longer inward red bars, hands behind the border and foreground stars. Earlier red-emote and ceiling-light variants were not selected.

**Uploaded to main and verified:** commit [4690eb6373ad137c64ad9e7c67f79e5e4a301307](https://github.com/d4np4yn3-netizen/Lore/commit/4690eb6373ad137c64ad9e7c67f79e5e4a301307). All 13 published file blob hashes match the upload manifest, including the exact approved PNG, SVG and artwork. Ninja Epic, Ninja Mythic and all unrelated repository files are preserved. Upload is complete; do not repeat it or ask for the same approval. Resolve the set through cards/creators/ninja/current-cards.json.

Ninja's three approved visuals are **Common — Pon Pon (01/06)**, **Epic — Not Enough Movement (04/06)** and **Mythic — Becoming the Icon (06/06)**. Three remain unapproved; no other provisional moments have been reassigned. Next action: await Dan's next card direction.

The six-card Asmongold set remains approved and unchanged. Resolve exact files through cards/creators/asmongold/current-cards.json. Mail Muncher v6 publication: 6839ffc685887c36cd076c424c2a8df53e342c0e, all 11 file blobs verified.

Ninja's QRs remain the reviewed demos. Primary audio/timestamp verification and physical print release are separate from visual approval.

## Preserved verified milestones

- Ninja Epic — Not Enough Movement: main commit 5038b7cca2d1e0e4b4859d44e580c10b930ca85b, all 13 file blobs verified. Exact approved Review-v4 PNG/SVG and softened-cheek artwork preserved; phrase **I’M NOT SEEING ENOUGH MOVEMENT!**
- Ninja Mythic — Becoming the Icon: main commit 6a073bd56618cf596994a34089053f7f5d8af4a3, all 12 file blobs verified. Exact approved Review-v4 PNG/SVG and darker v3 illustration preserved; phrase **IT LOOKS JUST LIKE ME.**
- Shower steam v3: main commit `a136683cdf9f1e3444889654c552efd655e92c8f`, all nine file blobs verified. Current PNG/SVG and art preserve the exact Steam Review v1 bytes.
- Thunderfury Mythic v1: main commit `92e9d9546609dbb24184ad06333a5efda87fb787`, all 11 file blobs verified. Preserve the original diagonal sword and accepted logo overlap; upright-sword experiment was not selected.
- Level 60 Homecoming plain-blue-flag original: main commit `03fab8b15b8fe63b1eafc87ddae78ece6fff9ee6`, all 11 file blobs verified. Crown-on-flags/tabards revision rejected.
- Badge spacing: LORE-FRONT-v4 / LORE-CARD-v1.1, equal 22-unit visible-glyph side padding and 47-unit height. Six templates and four approved derivatives published in PR #2, merge `a1a2d76f8c3b9e71e7424655d9962d757a381eac`; all 54 files verified.
- Renderer: `cards/master/front-v4/source/render_card.py`. Rules: `cards/12-RARITY-BADGE-SPACING.md`. Shared back v5 and 63 × 88 mm trim unchanged.

Live QR routes, primary audio/count/source checks, creator permissions and physical print release remain separate from visual approval.

## Compact working method

1. Keep this file short and update it in place after each completed milestone: active task, exact paths, approval, verified delivery, next action.
2. Read current status first. Load only relevant standards and files. Historical recovery logs are for resolving a specific gap; do not reconstruct every past chat on routine continuation.
3. Work through one reviewable card milestone at a time: illustration, layout/copy, approval, upload verification. Preserve approved work.
4. Existing explicit approval for an unchanged file persists across chats. Check the recorded approval and delivery before asking again or retrying an upload.
5. Transfer assets as files using an available authorized git/file-transfer route. Keep base64, image bytes, embedded-image SVG payloads and large logs out of model-visible messages. If a connector is necessary, handle payloads programmatically and return only paths, sizes, hashes and results.
6. A large file may return an empty content field through GitHub's contents API. Check its blob SHA; do not assume it is missing or empty, or re-upload it unnecessarily.
7. Verify the actual remote file/hash before saying uploaded. Save a small checkpoint for an incomplete transfer and resume only missing work.
8. Report the outcome briefly with the file or commit link. Do not create another long handover for every interruption.

The exact cause of the app's conversation-limit errors has not been established. This workflow reduces repeated context and makes completed work recoverable.

