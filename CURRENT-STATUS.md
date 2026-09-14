# LORE — current status

Updated 2026-09-14. Read with AGENTS.md.

## Current milestone: Ninja Legendary approved for GitHub and website

Dan approved **VEGAS / TAKEOVER — Legendary / Moment 05 of 06**, phrase **ONE MILLION PERCENT.**: “Yep, let's lock that in, add it to GitHub and add it to the site.”.

Canonical PNG: cards/creators/ninja/vegas-takeover-master-01/LORE-Ninja-Vegas-Takeover-Legendary-v1.png. Matching SVG, selected art.png, approval, source notes and hashes are beside it. These preserve the exact displayed Review-v2 and selected art-v2 bytes.

Ninja now has five approved visuals: Common 01/06, Uncommon 02/06, Epic 04/06, Legendary 05/06 and Mythic 06/06. Only Rare 03/06 remains. Resolve exact files through cards/creators/ninja/current-cards.json. Asmongold's six approved cards remain unchanged.

Website: https://lore.d4np4yn3.chatgpt.site, existing owner-private Sites project appgprj_6aa7012d260881919cdb0f797a84d234. Add the card and /m/ninja/05/ route using the existing QR-only sample workflow; retain the reviewed demo QR in the canonical master. Source: the venue's full Ninja Vegas '18 archive, https://www.youtube.com/watch?v=9iPLee-FWvw. Event date 21 April 2018; archive uploaded June 2025. Phrase verified as an excerpt of the venue-published Ninja quotation; independent spoken audio/timestamp verification remains open.

Publication verification will be recorded after GitHub and website delivery. Existing approval persists across chats.

Next card direction: Dan wants Rare to be much wilder and action-led, with energy comparable to Asmongold riding Mail Muncher. The 32-elimination solo-squads game is proposed as a source; moment selection and artwork remain unapproved. Avoid another standing portrait under stage lights.

## Preserved verified milestones

- Ninja Uncommon — Low Taper Fade: GitHub a1ac8b48a0b0397abc5f6d595323790392c3af30 verified all 12 blobs; site version 3 published with /m/ninja/02/, source commit 2a0dd83374efeeeaeda54ac8efe66294325bb05a. Exact approved Review-v1 and PROPHECY FULFILLED. preserved.
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
