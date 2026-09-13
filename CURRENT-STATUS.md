# LORE — current status

Updated 2026-09-13. Read with AGENTS.md.

## Current milestone: approved badge spacing applied

Dan approved the right-hand rarity badge comparison: **“agreed, right hand version is approved”**. All six templates now use equal 22-unit side padding based on visible lettering, fixed 47-unit height and centred text. Font, colours, stroke and corners are unchanged.

- Current layout: **LORE-FRONT-v4** / card design lock **LORE-CARD-v1.1**.
- Rule and approval: `cards/12-RARITY-BADGE-SPACING.md` and `operations/16-RARITY-BADGE-SPACING-APPROVAL-2026-09-13.md`.
- Current files and exact hashes: `cards/creators/asmongold/current-cards.json`.
- Generator: `cards/master/front-v4/source/render_card.py`.
- QA and previews: `cards/master/front-v4/qa/` and `cards/master/front-v4/references/`.

## Current approved card derivatives

- `cards/creators/asmongold/steak-master-01/LORE-Asmongold-Steak-Final-v3.png` and its matching SVG.
- `cards/creators/asmongold/shower-master-01/LORE-Asmongold-Shower-Legendary-v2.png` and its matching SVG.
- `cards/creators/asmongold/mail-muncher-master-01/LORE-Asmongold-Mail-Muncher-Epic-v5.png` and its matching SVG.
- `cards/creators/asmongold/rat-alarm-master-01/LORE-Asmongold-Rat-Alarm-Rare-v2.png` and its matching SVG.

Every pixel outside each badge matches the preceding approved PNG. SVG comparison confirms only badge width and label x/y changed; artwork, crop, QR, copy, logo and all other geometry are intact. Earlier card versions and the full front-v3 reference set remain unchanged historical assets.

**Uploaded and merged into main:** [PR #2](https://github.com/d4np4yn3-netizen/Lore/pull/2), merge commit `a1a2d76f8c3b9e71e7424655d9962d757a381eac`. Dan explicitly authorised upload and merge with **“approved, upload”**. All 54 changed files on the fetched main branch match the verified local files byte for byte; all seven PNG exports decode successfully. Six templates and four approved cards passed the badge checks, with zero pixel changes outside the badges. GitHub publication is complete. Do not re-upload, regenerate or request this approval again. Use the current v4 templates and card register for subsequent work. Prior Rat Alarm upload is complete on main via PR #1.

Live QR routes, primary source/audio checks, creator permissions and print release remain separate open work. The shared back v5 and 63 × 88 mm trim are unchanged.

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
