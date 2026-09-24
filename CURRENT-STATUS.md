# LORE — current status

Updated 2026-09-24. Read with AGENTS.md and PROJECT-MEMORY.md.

## Current milestone: Crypto print master approved

Dan approved **LORE-CRYPTO-PRINT-v1.0** across all six crypto rarities after selecting the larger/bold phrase treatment: the moment phrase now uses size 25 / weight 700, with its existing position, tracking and rarity colour preserved.

Canonical master: `cards/crypto/master/print-v1/`.
Printer geometry: 816×1110 full bleed @300DPI; 744×1038 cut; 684×981 safe.
The complete LORE-FRONT-v4 front is uniformly inset with `translate(46.515 48.921) scale(0.8033)`; no stretching.
Approval record: `operations/17-CRYPTO-PRINT-TEMPLATE-APPROVAL-2026-09-24.md`.

Creator cards are unchanged. Existing approved crypto card exports are preserved.

## Next action

Rebuild the **eleven approved Crypto Season One cards** one by one as new print derivatives using LORE-CRYPTO-PRINT-v1.0, preserving each card's exact approved art, wording, rarity and QR status. Start with Birth of HODL as the reference conversion, then roll through the approved register.

Physical sample approval, live QR routes and physical QR scan testing remain separate release gates.

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
