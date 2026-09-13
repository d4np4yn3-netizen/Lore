# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: Shower steam revision approved

Dan approved the displayed Steam Review v1 with **“yeah, i think this is better, approved for upload”**. The current Legendary card is `cards/creators/asmongold/shower-master-01/LORE-Asmongold-Shower-Legendary-v3.png` and its matching SVG, with `art-steam-v1.png`, `steam-v3-approval.json` and the updated manifest. The v3 exports preserve the exact review bytes. Subtle illustrated steam and condensation are the sole artwork revision; the fixed layout, text, logo, QR and Moment 05/06 remain unchanged. Prior shower versions stay historical.

This is the approved upload package. Verify published file hashes against the upload checkpoint before reporting success. Resolve active exports through `cards/creators/asmongold/current-cards.json`.

Next planned artwork review: **Mail Muncher**, improving Asmon’s likeness, integrated lighting and depth. Its existing approved card remains current until Dan approves a replacement. All six selected card visuals remain approved with the current rarity order.

## Previous milestone: Thunderfury Mythic approved, uploaded and verified

Dan attached the original **Thunderfury / Mythic / Moment 06 of 06** card and said **“we will stick with this, its too good to start tweaking, approved for upload to github”**. The approved PNG in `cards/creators/asmongold/thunderfury-master-01/LORE-Asmongold-Thunderfury-Mythic-v1.png` preserves that exact attachment. Its matching SVG, original art, render data, approval and hashes are beside it. **Keep the original diagonal sword and logo overlap.** The later upright-sword clearance experiment was not selected and must not replace this version.

The current collection now has six visually approved cards: Common — The $2 Steak; Uncommon — Level 60 Homecoming; Rare — Rat Alarm; Epic — Mail Muncher; Legendary — Charity Shower; Mythic — Thunderfury. Current numbering is 01–06 respectively. Dan may review the rarity order with the finished set; no reordering is authorised here.

**Uploaded to main and verified:** commit [`92e9d9546609dbb24184ad06333a5efda87fb787`](https://github.com/d4np4yn3-netizen/Lore/commit/92e9d9546609dbb24184ad06333a5efda87fb787). All 11 published file blob hashes match the upload checkpoint, including the exact attached PNG, original editable SVG and artwork. Upload is complete. Resolve the exact current files through `cards/creators/asmongold/current-cards.json`; do not regenerate or request the same approval again.

## Preserved prior milestones

- Level 60 Homecoming plain-blue-flag original: main commit `03fab8b15b8fe63b1eafc87ddae78ece6fff9ee6`, all 11 file blobs verified. Crown-on-flags/tabards revision rejected.
- Approved badge spacing: LORE-FRONT-v4 / LORE-CARD-v1.1, equal 22-unit visible-glyph side padding and 47-unit height. All six templates and four earlier approved card derivatives published in PR #2, merge `a1a2d76f8c3b9e71e7424655d9962d757a381eac`; all 54 files verified. Original art and pixels outside badges preserved.
- Renderer: `cards/master/front-v4/source/render_card.py`. Rules: `cards/12-RARITY-BADGE-SPACING.md`. Shared back v5 and 63 × 88 mm trim unchanged.

Live QR routes, primary audio/source checks, creator permissions and print release remain separate. Visual approval does not settle those items.

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
