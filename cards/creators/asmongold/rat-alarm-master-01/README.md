# Asmongold — Rat Alarm / approved Rare v1

Status: **VISUALLY APPROVED — UPLOAD AUTHORISED**, Dan Payne, 13 September 2026.

Dan approved this exact card with **“Approved for upload”** after reviewing the PNG. Approval covers Rare / blue, Moment 03 of 06, the RAT / ALARM title and **IT WOULD START COOKING.** The original `Review-v1` filenames remain to identify the exact reviewed files. See `approval.json` for approval evidence and unchanged asset hashes.

Dan approved the attached bedroom illustration and requested removal of its embedded LORE branding, keeping everything else the same. He selected Rare / blue, Moment 03 of 06, and the exact phrase **IT WOULD START COOKING.** on 13 September 2026. “RAT / ALARM” is the approved title.

The card is rendered with the actual locked `cards/master/front-v3/templates/rare.svg`, its pinned fonts and existing renderer, fetched from GitHub at commit `0218021b9d62702e36cde2ffede16b2139994b02`. Logo, border, fonts, text positions, gradients and QR placement match the template exactly. The 900 × 1260 visual master is retained; the locked physical trim is 63 × 88 mm. This is a visual approval file, not a printer-specific derivative.

## Files

- `LORE-Asmongold-Rat-Alarm-Rare-Review-v1.png`: the exact approved card.
- Matching `.svg`: editable template-derived card with embedded artwork.
- `art.png`: full uncropped artwork with only the two brand regions changed.
- `art-logo-removal.svg`: source composition embedding the original and image-tool removals, applied only within the two brand regions.
- `approved-user-artwork.jpeg`: unchanged original attachment.
- `card-data.json`: portable renderer inputs; run the pinned renderer from the repository root. Do not rerender during delivery of this approved revision.
- `qa.json` and `manifest.json`: checks and exact file hashes.

## Artwork preservation

The built-in image-editing tool removed the gold crown and LORE lettering from the purple wall hanging and black foreground can. Those two local replacement surfaces were composited over the original, keeping all other original pixels. Verification compared 1,501,884 pixels outside the two bounded removal regions and found zero changes. No change to the face, body, bedding, posters, rat, tail, flies, odour trails, sunlight or composition.

## Phrase and QR

Dan’s exact words: “It would start cooking - is the phrase”. Uppercase and a final full stop follow the existing card presentation.

The phrase is supported by a [published transcript of the rat alarm story](https://fraghero.com/asmongold-admits-to-using-a-dead-rat-as-an-alarm-clock/). A [clip of the story](https://www.youtube.com/watch?v=tthbWjdMjeg) was located; its original audio/timestamp could not be checked in this session. This is recorded separately from Dan’s wording selection.

The QR remains an explicit `example.com` demo in the locked layout, as in the existing review cards. It does not yet open a live moment page. Its exported 37 × 37 module grid, including the clear margin, was verified against the encoded demo payload.

## Delivery and future changes

The original artwork, cleaned artwork, removal composition, card PNG and card SVG are preserved byte for byte from the approved review. Only folder organisation and approval records change for publication. Their expected Git blob and SHA-256 hashes are in `manifest.json`. Verify remote hashes after uploading.

Future design or wording changes require a separate numbered review. The QR remains a demo; primary audio/timestamp verification and print release remain separate.
