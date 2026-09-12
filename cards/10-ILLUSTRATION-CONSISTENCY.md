# Illustration consistency standard

**Status: original LORE-FRONT-v3 art direction reaffirmed by Daniel Payne on 2026-09-12.** The specifically selected steak artwork supplements that direction. This does not redesign the front template, branding, back or physical format.

## Authority

Use [the reference manifest](style-reference-lock.json) to locate and verify the files. The original v3 set remains the baseline. Dan specifically reattached these four fronts and described them as almost perfect:

| Reference | What to carry forward |
| --- | --- |
| [Rare / Going Live](master/front-v3/references/fronts/03-rare.png) | Expressive drawn face, clear eyes and brow, confident character silhouette. |
| [Epic / Mount Off](master/front-v3/references/fronts/04-epic.png) | Animated expression, dynamic ink, simplified facial shadow shapes. |
| [Legendary / The Builder](master/front-v3/references/fronts/05-legendary.png) | Rich scene detail and cinematic lighting held within the same illustrated language. |
| [Original Common / steak](master/front-v3/references/fronts/01-common.png) | Warm palette and ink treatment. Its imagined clothes, props and kitchen are not factual authority. |
| [Approved steak illustration](creators/asmongold/steak-master-01/README.md) | Specific approved balance of anime expression, hand-drawn texture and source-informed kitchen detail. |

For generation, use the corresponding **art-only PNGs**, not just the finished card images. Preserve the exact approved steak illustration for steak exports. Earlier experimental variants are not approved replacements.

## Drawing rules

- Apply the same hand-drawn anime/manga treatment to the entire scene: creator, mounts and other creatures, props, buildings, foliage, sky and water. Use deliberate ink contours, grouped shapes, cel-shaded planes and selective drawn texture throughout. Do not combine an illustrated person with a photorealistic mount or background. Keep background detail and contrast subordinate to the main subjects. Dan explicitly reaffirmed this whole-scene requirement during the Mail Muncher review.
- Faces must read as drawn characters at card size: deliberate contours, expressive eyes and brows, clear mouth shapes, recognisable adult likeness and intentional simplification.
- Use variable ink weight, grouped hair shapes, controlled fine strands, designed shadow masses and selective hatching. Retain the approved level of texture; do not remove all detail or turn it into a generic flat cartoon.
- Keep cinematic light and colour in the illustrated treatment. Avoid photographic skin pores, airbrushed portrait rendering, photographic depth of field or a photo with an edge filter.
- Maintain the same rendering language across rarity levels. Rarity may change colour, finish and presentation; it must not change the character into a different drawing style.
- Each creator keeps their own identity and proportions. Asmongold's facial features are not a template to copy onto other people.

## Facts and style are separate inputs

Original footage/screenshots establish clothes, setting, objects and actions. Approved LORE art establishes linework, expression and shading. Do not copy the camera's photographic surface treatment. Do not invent a different kitchen, outfit or hero prop merely because an earlier concept looked attractive.

The steak illustration is an expressive interpretation combining details from the cooking video. It is not a claim that every prop occupied that precise position in one frame. Unverified spoken recollections must not become verbatim quotations or exact timestamps.

## Workflow for every card and revision

1. Read `PROJECT-MEMORY.md`, the design lock, front standard and this document.
2. Attach approved original art references and a factual source reference to the generation request. Always carry original references into revisions; do not rely on a chain of generated derivatives alone.
3. Generate only artwork. Use a composition plan for the fixed front template: head clear of the top labels/logo, expressive gesture and main object above the lower information area. Preserve full uncropped approved art separately from card crops.
4. Apply the existing SVG template and pinned fonts. Keep logo, border, labels, title geometry and front QR unchanged. Resolve fitting problems through a reviewable art-placement proposal, not silent layout changes.
5. Compare the result beside the original references at full size and card size. Review face style, mount/creature treatment, background rendering, line weight, shadow language, likeness, source accuracy and layout collisions. Reject obvious drift before presenting it.
6. Identify the exact proposed image and approval scope. Only explicit user selection can promote a new artwork; technical QA alone cannot. Preserve the approval evidence and hashes.

## Current steak selection

Dan's **“This is the one!”** selects the [attached steak picture](creators/asmongold/steak-master-01/approved-user-reference.jpeg). Its corresponding source PNG is preserved unchanged. He subsequently authorised moving/rescaling the image to clear the potato when assembling the final card. The [latest assembly](creators/asmongold/steak-master-01/LORE-Asmongold-Steak-Final-v2.png) moves only the image upward by 70 SVG units: no rescaling, repainting or fixed-layout change. Potato and pan now clear the QR. Dan subsequently selected `I’M A SIMPLE MAN.` for the context line and requested visual sign-off of v2. That phrase is the only change from v1; see [the visual approval record](../operations/15-STEAK-V2-VISUAL-SIGNOFF-2026-09-12.md). Original art approval, visual sign-off, quotation verification and print release remain separate.

See [the decision record](../operations/14-STEAK-AND-STYLE-REFERENCE-2026-09-12.md).
