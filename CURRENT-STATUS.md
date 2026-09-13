# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: Mail Muncher v6 approved

Dan approved the exact displayed Revised Review v2 with **“yup, lock it in, approved for upload”**. Current Epic / Moment 04/06: `cards/creators/asmongold/mail-muncher-master-01/LORE-Asmongold-Mail-Muncher-Epic-v6.png` and matching SVG. Artwork: `cards/creators/asmongold/mail-muncher-master-01/art-rising-v1.png`. Approval and hashes: `cards/creators/asmongold/mail-muncher-master-01/rising-v6-approval.json` and `manifest.json`.

The approved revision has the body rising from the bottom, a central dorsal crest/single back ridge, deeper moonlit shadows with warm city light underneath, flying WoW-referenced mail and stronger Asmongold likeness. The v6 PNG, SVG and artwork preserve the exact approved review bytes. Fixed layout, logo, badge, fonts, title, phrase **199 ATTEMPTS!**, numbering and QR stay unchanged. Prior Mail Muncher versions remain historical.

This is the approved upload package. Verify the published hashes before reporting success. Resolve all current cards through `cards/creators/asmongold/current-cards.json`.

The six-card visual set is approved: Common — The $2 Steak; Uncommon — Level 60 Homecoming; Rare — Rat Alarm; Epic — Mail Muncher v6; Legendary — Charity Shower v3 with steam; Mythic — Thunderfury. Numbering is 01–06. No further artwork revision or rarity reordering is authorised. Next action after verified publication: await Dan’s next direction.

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
