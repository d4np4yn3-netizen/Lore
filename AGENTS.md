# LORE — mandatory project instructions

Read `CURRENT-STATUS.md` first for the active task, exact approved files, verified delivery and next action. Follow its compact working method. Read `PROJECT-MEMORY.md` for current decisions and exact selected artwork. Repository memory is authoritative when old chat recollections conflict with it. For an unchanged-file delivery check, inspect the current status and remote hashes; do not reload the full design history or repeat recorded approvals.

Read these files from the current repository before any brand, card, packaging or website work:
1. `brand/brand-lock.json`
2. `brand/01-BRAND-CORE.md`
3. `brand/02-VISUAL-IDENTITY.md`
4. `brand/assets/asset-manifest.json`
5. `brand/ASSET-QA.md`

## No design drift

- The locked name is LORE. The only approved brand lines are `COLLECT THE INTERNET.`, `ICONS ARE MADE OF MOMENTS.`, and `SIX MOMENTS. ONE ICON.` Use their assigned roles. Do not invent an alternative slogan, even in a mock-up.
- Earlier chat suggestions and incidental copy inside generated reference boards do not override the lock.
- The approved master is LORE-04-v1.0: 04 / Rising Strokes crown with the preserved brush LORE wordmark. Daniel approved this exact revision and deterministic exports on 2026-09-11; see operations/10-BRAND-APPROVAL-04.md. Other generated-sheet content does not extend that approval.
- Do not regenerate a logo, crown, tagline, serial number or QR inside a final illustration. Composite the exact approved separate assets and typeset approved text instead.
- Produce new illustrations without brand lettering; apply the locked brand layer afterwards. An export request is not permission to redesign.
- Generate every colourway and lockup from the SAME approved lettering geometry and the SAME approved crown geometry. No separately invented crowns.
- Keep the six rarity names and order unchanged. Keep the researched-six-moments principle. Do not reintroduce game stats or crypto into the collectible-first launch without approval.
- If a change to wording, geometry, proportion, palette or layout is necessary, present the precise change separately and wait for Daniel Payne's approval before promoting it.

## Assets and delivery

- `approved_exports` in the brand manifest is the approved reusable brand file list. Card masters are separately identified by `cards/card-design-lock.json` and their own master manifests. Never infer production/print approval from a visual design lock.
- Rejected v1 files must not be used. Do not infer that a file exists because it appears in a README.
- Run the QA checklist on actual files, not just on a generated showcase. Check crown apex, both outer tips and BOTH lower base edges, complete brush strokes, true alpha, panel-border contamination, placement collisions and safe margins.
- Open exports on dark and light backgrounds. Record dimensions, SHA-256, visual inspection and approval independently.
- Technical QA cannot confer user approval. Never self-approve a candidate or label an unreviewed file production-ready.
- Read the current branch before writes, preserve unrelated work, and verify the committed file exists. A tool failure or local-only file must be reported accurately; never claim it was uploaded.
- No creator is a partner until permission is recorded. A sourced moment is not automatically a licensed image/video asset.

## Moment phrases

Read `cards/11-MOMENT-PHRASE-STANDARD.md` before selecting or changing card copy. The small line beneath the title uses a short phrase from that specific moment, agreed with Dan, in the existing font and position. Verify the words against the primary source and record the evidence; do not invent or silently paraphrase quotations. Visual approval and source verification are separate statuses.

## Selected card front reference

Before any card generation or revision, also read `cards/10-ILLUSTRATION-CONSISTENCY.md` and `cards/style-reference-lock.json`. Carry approved original art references into every generation, including edits; do not let a chain of new outputs silently become the style master. Use screenshots for factual clothes, settings and props, and approved LORE art for the drawing treatment. Daniel's specifically approved steak illustration is `cards/creators/asmongold/steak-master-01/art.png`, with his exact attached approval reference and hashes beside it. Preserve it unchanged for exports. Review card crops separately and never substitute another variant during packaging.

## Current Asmongold steak continuation

Historical recovery is recorded in `operations/14-STEAK-ARTWORK-CONTINUATION-2026-09-12.md` and resolved in `operations/14-STEAK-AND-STYLE-REFERENCE-2026-09-12.md`; consult them only if current records leave a specific gap. The current signed-off visual is `cards/creators/asmongold/steak-master-01/LORE-Asmongold-Steak-Final-v2.png` and its matching SVG. Dan approved replacing the context line with `I’M A SIMPLE MAN.` and requested visual sign-off; see `operations/15-STEAK-V2-VISUAL-SIGNOFF-2026-09-12.md`. Preserve the exact approved art, its upward translation of 70 SVG units, and every other fixed element. Original art approval, visual sign-off, source verification and print release remain separate.

Before card art, templates or new creator sets, also read `cards/card-design-lock.json` and `cards/07-FRONT-LAYOUT-AND-ART-MASTER.md`. The selected front baseline is the exact Asmongold v3 front-QR set, including its increased headroom. Use the pinned templates, font files and visual references; fill new creator content into the existing layout. Do not regenerate the whole card or silently substitute fonts. The universal LORE-BACK-v5 is explicitly approved; also read `cards/08-SHARED-BACK-MASTER.md`. Use its exact PNG/SVG and manifest in `cards/master/shared-back-v5`: no diamond, thick gold outer border, clearer thin inner border. LORE-CARD-v1.0 locks the visual front and back system. The finished card size is also locked at 63 × 88 mm; read `cards/09-PHYSICAL-SIZE-STANDARD.md`. Keep the existing 900 × 1260 visual references unchanged and prepare separate printer-specific derivatives. Bleed, safe inset, corner die and manufacturing/print approval remain separate; do not silently alter the back to invent a cutting allowance.
