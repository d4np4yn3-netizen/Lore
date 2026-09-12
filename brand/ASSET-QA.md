# LORE Asset QA and approval gates

Current approved revision: **LORE-04-v1.0 / 04 — Rising Strokes**, explicitly selected by Daniel Payne with authorisation to create its deterministic PNG/SVG exports. See [the approval record](../operations/10-BRAND-APPROVAL-04.md). These checks validate implementation of that decision; they cannot authorise a redesign.

## 1. Freeze the input

Read AGENTS.md, the brand lock and the current asset register. Record source filename, source hash and approved revision. Record whether the task is an export or a redesign; default to export. Do not invent copy.

## 2. Build deterministic exports

Use one lettering component and one crown component across every colourway and lockup. Preserve all silhouette extremities. Compose approved text separately. Do not let a new generative sheet substitute for separate master files.

For recovery from a concept board, retain the source resolution and label the files review-only. Upscaling does not turn a crop into production vector artwork. Keep art, texture and identity decisions separate.

## 3. Inspect the actual PNGs

- Decode every file; check format, dimensions, colour mode and SHA-256.
- Check a real alpha channel; a rendered checkerboard is not transparency.
- Inspect on dark, light and checker backgrounds, including at native resolution and at target card-corner size.
- Inspect the crown apex, left/right outer points and both lower corners of its curved base.
- Inspect every brush tip of LORE. Safe exterior padding does not repair pixels already lost in a source crop.
- Reject rectangular panel lines, captions, ghost crowns, leftover tagline fragments and matte halos.
- Ensure the crown and lettering do not hide or cut each other's geometry in a lockup.
- Retain the approved lockup transforms and built-in exterior padding. The LORE-04-v1.0 transparent exports all exceed 48 px exterior padding. A future change to composition or clear space needs approval.
- Compare black and white alpha masks; geometry must match. Compare shared crown placements across lockups.
- Verify every displayed brand line against brand-lock.json. No alternative slogans.

## 4. Separate statuses

DIRECTION_APPROVED is not EXPORT_APPROVED. An export can pass technical checks and still be REVIEW_ONLY. Daniel Payne must approve the specific revision before it enters the approved asset register. Finishes, vector readiness and print proofs are separate gates.

## 5. Verify the upload

Write real image bytes, not a base64 string disguised as a PNG/JPEG. Confirm the committed path, byte count and hash; decode the downloaded result. Do not claim an upload based on a local file, filename list or successful Markdown commit.

## 6. Release

Record the approved revision, hashes, dimensions, native source, QA record and explicit approval. Only then use it across cards, packaging and web. Keep rejected packs out of the active asset list. Any subsequent visual/copy change requires a new proof and approval; never silently replace a master.
