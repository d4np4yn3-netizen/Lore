# LORE — current status

Updated 2026-09-12. Read this first with AGENTS.md; use PROJECT-MEMORY.md for design decisions.

## Current delivery: COMPLETE

Dan's approved Asmongold steak v2 PNG and SVG are on main. The context line is **I’M A SIMPLE MAN.** Exact approved art and layout are preserved.

Directory: `cards/creators/asmongold/steak-master-01/`
- `LORE-Asmongold-Steak-Final-v2.png` — Git blob `5ec0ca149b90b348954c7d951dc292091688f0a0`
- `LORE-Asmongold-Steak-Final-v2.svg` — Git blob `c9fcbc368beb08d541c1b80fcef5fb0cad564ff5`

Verification: live GitHub file SHAs matched Git blob hashes computed from the local files; their SHA-256 values also matched `final-qa-v2.json`. Approval: `operations/15-STEAK-V2-VISUAL-SIGNOFF-2026-09-12.md`. Phrase rule: `cards/11-MOMENT-PHRASE-STANDARD.md`. These records are on main.

No upload remains pending. Resume from Dan's next requested task. Audio/timestamp verification, live QR, final rarity/set allocation and print release remain separate open work.

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
