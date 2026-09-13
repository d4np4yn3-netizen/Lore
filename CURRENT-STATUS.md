# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: Ninja Mythic visually approved

Dan approved the completed **BECOMING / THE ICON — Mythic / Moment 06 of 06** with **“Approved upload to github”**. Phrase: **IT LOOKS JUST LIKE ME.** This is Ninja's first approved visual; the other five remain to be developed and approved.

Canonical PNG: `cards/creators/ninja/becoming-the-icon-master-01/LORE-Ninja-Becoming-The-Icon-Mythic-v1.png`; matching SVG, original `art.png`, approval, source notes and hash manifest are beside it. These preserve the exact signed-off Review-v4 PNG/SVG and darker v3 illustration. Keep matching blue-grey eyes, clearly drawn cel shading and the dramatic avatar light. No regeneration or layout change was made for upload. Resolve the Ninja set through `cards/creators/ninja/current-cards.json`.

Publication includes the approved package and creator register. The upload runner compares all published file hashes with the local manifest before reporting completion. Existing upload approval persists; do not ask again or substitute an earlier draft. Next action after verification: await Dan's next card direction.

The six-card Asmongold set remains approved and unchanged: Common — The $2 Steak; Uncommon — Level 60 Homecoming; Rare — Rat Alarm; Epic — Mail Muncher v6; Legendary — Charity Shower v3 with steam; Mythic — Thunderfury. Resolve exact files through `cards/creators/asmongold/current-cards.json`. Mail Muncher v6 publication: `6839ffc685887c36cd076c424c2a8df53e342c0e`, all 11 file blobs verified.

Ninja's QR remains the approved demo. Original audio/timestamp verification and print release are separate from this visual approval.

## Preserved verified milestones

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

