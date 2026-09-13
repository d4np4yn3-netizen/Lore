# LORE — current status

Updated 2026-09-13. Read this first with AGENTS.md; use PROJECT-MEMORY.md for design decisions.

## Current delivery: COMPLETE

### Rat Alarm card

Dan approved the **Rare v1 visual / Moment 03 of 06** with **“Approved for upload”** on 2026-09-13. Title: **RAT / ALARM**. Phrase: **IT WOULD START COOKING.** Exact files, approval evidence and SHA-256 hashes are in `cards/creators/asmongold/rat-alarm-master-01/`.

- `art.png` — Git blob `52f3c07e9b3b3d3f8c91e7bf18756b096dd9b8c9`
- `LORE-Asmongold-Rat-Alarm-Rare-Review-v1.png` — Git blob `2f0bcf45a01da31d99c6c7c083519cda53e6f9b0`
- `LORE-Asmongold-Rat-Alarm-Rare-Review-v1.svg` — Git blob `a3a32650fbadcd598543cba0a3f6cf8330f4fa45`

The exact reviewed assets are preserved unchanged. Both embedded artwork LORE marks are removed, with zero pixel changes outside the two removal regions. The actual pinned Rare SVG, logo, fonts and fixed geometry were used. Original `Review-v1` filenames remain despite approval. Source-audio verification, live QR and print release remain open.

### Mail Muncher card

Dan approved the **Epic v4 visual** and explicitly requested locking and uploading it. Exact files and approval evidence are together in `cards/creators/asmongold/mail-muncher-master-01/`.

- `art.png` — Git blob `8b7feba5ab2dd3f199a08236464b384d696a8237`
- `LORE-Asmongold-Mail-Muncher-Epic-Layout-Review-v4.png` — Git blob `4e316cf3441a6413de36569ba05a9769ddd8695f`
- `LORE-Asmongold-Mail-Muncher-Epic-Layout-Review-v4.svg` — Git blob `2211f5c10fd4c17478bdf666f31e35698db34b26`

The exact reviewed bytes are preserved, with SHA-256 and local checks in `manifest.json`; the SVG embeds the same approved `art.png`. Original `Layout-Review-v4` filenames are retained. Phrase: **199 ATTEMPTS!** The approved version includes whole-scene anime styling, corrected moonlight, side-edge space and the removed foreground QR-area tower. Count/source verification, live QR, final numbering, commercial permissions and print release remain open.

### Shower card

Dan approved the shower visual and manually uploaded the unchanged PNG, SVG and approval README in commit `938aa3a93b1733e8ccd66edededd3f68bdfa88d2`. They are filed together in `cards/creators/asmongold/shower-master-01/`. The parent collection README was restored as an index with links to both cards.

- `LORE-Asmongold-Shower-Legendary-Review-v1.png` — Git blob `c8bc8c4b0c0070354ca6461acd586cc9966678f3`
- `LORE-Asmongold-Shower-Legendary-Review-v1.svg` — Git blob `c6e6053d36de2a8a894c4ee8f58b4e2fe99907d7`

Verification: the live uploaded PNG/SVG blob SHAs match the approved export hashes; the folder correction reuses those same blobs without changing image bytes. Approval and SHA-256 records: `cards/creators/asmongold/shower-master-01/README.md`. Original `Review-v1` filenames are retained despite visual approval. Phrase: **I’M A VERY CLEAN BOY.** The QR is still a demo; audio/timestamp checks, final numbering/rarity allocation and print release remain open.

### Steak card

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
