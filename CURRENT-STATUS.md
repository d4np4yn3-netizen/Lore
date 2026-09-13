# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: Ninja Epic approved; two Ninja cards selected

Dan approved **NOT ENOUGH / MOVEMENT — Epic / Moment 04 of 06**: **“Lock it in and upload to github! Two great cards so far”**. Phrase: **I’M NOT SEEING ENOUGH MOVEMENT!**

Canonical PNG: cards/creators/ninja/not-enough-movement-master-01/LORE-Ninja-Not-Enough-Movement-Epic-v1.png; matching SVG, original art.png, approval, source notes and hash manifest are beside it. These preserve the exact signed-off Review-v4 PNG/SVG and final softened-cheek illustration. Keep the anime treatment, red hair/dark bandana, cool viewer-left face shadow, yellow/pink light from viewer-right and restrained amber-peach cheek highlight. Earlier v1-v3 drafts are superseded.

Publication contains the approved package and updated two-card Ninja register. The upload runner verifies every published blob against its local manifest before reporting completion. Existing upload approval persists; do not ask again or substitute an earlier draft. Resolve the set through cards/creators/ninja/current-cards.json.

Ninja's two approved visuals are **Epic — Not Enough Movement (04/06)** and **Mythic — Becoming the Icon (06/06)**. Four remain unapproved; other provisional moments have not been reassigned after Dan moved Times Square to Epic. Next after verification: await Dan's next card direction.

The six-card Asmongold set remains approved and unchanged. Resolve exact files through cards/creators/asmongold/current-cards.json. Mail Muncher v6 publication: 6839ffc685887c36cd076c424c2a8df53e342c0e, all 11 file blobs verified.

Ninja's QRs remain the reviewed demos. Primary audio/timestamp verification and physical print release are separate from visual approval.

## Preserved verified milestones

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
