# LORE

**COLLECT THE INTERNET.**

The approved identity is **04 / Rising Strokes**: the hand-drawn crown paired with the existing LORE brush wordmark, with the selected spacing preserved. Locked by Daniel Payne on 11 September 2026.

[Download the complete PNG + SVG pack](https://github.com/d4np4yn3-netizen/Lore/raw/refs/heads/main/brand/downloads/LORE-Brand-Pack-v1.0.zip) · [Browse individual assets](assets/README.md) · [Open the full-size brand guide](previews/LORE-Brand-Guide.png)

![LORE approved brand guide](previews/LORE-Brand-Guide.png)

## Choose a file

| Use | Recommended asset |
|---|---|
| Main brand presence on dark backgrounds | [Gold crown + white primary logo](assets/png/lore_logo_primary_gold_white.png) |
| Main brand presence on light backgrounds | [Gold crown + black primary logo](assets/png/lore_logo_primary_gold_black.png) |
| Small placements without a tagline | [Compact logo](assets/svg/lore_logo_compact_gold_white.svg) |
| Horizontal space | [Horizontal lockup](assets/svg/lore_lockup_horizontal_gold_white.svg) |
| Crown alone | [Gold](assets/svg/lore_crown_gold.svg), [white](assets/svg/lore_crown_white.svg), [black](assets/svg/lore_crown_black.svg) |
| Monochrome production | [White primary](assets/svg/lore_logo_primary_white.svg), [black primary](assets/svg/lore_logo_primary_black.svg) |
| Social profile | [Gold crown on Obsidian](assets/png/lore_avatar_gold_dark.png) |
| App tile | [White wordmark on Obsidian](assets/png/lore_app_icon_dark.png) |

## Brand language

| Role | Exact line |
|---|---|
| Master tagline | **COLLECT THE INTERNET.** |
| Brand thought | **ICONS ARE MADE OF MOMENTS.** |
| Six-card collection line | **SIX MOMENTS. ONE ICON.** |

## Palette

| Colour | RGB hex | Role |
|---|---|---|
| Obsidian | `#0B0B0B` | Main dark surface |
| Bone | `#F5F2EB` | Warm light surface |
| Gold | `#D4AF37` | Flat crown and accent |
| Charcoal | `#1A1A1A` | Secondary dark surface |
| White / Black | `#FFFFFF` / `#000000` | Monochrome logo artwork |

## Use the master consistently

Use a complete supplied lockup and scale it uniformly. Keep the built-in margins; preserve the selected crown-to-L spacing. Do not redraw the crown, replace the LORE lettering with a brush font, or add a shadow, bevel or metallic gradient. Apply the logo as a separate layer over card and packaging artwork.

SVG is the scalable master format. PNG is suitable for raster workflows: logos, wordmarks and brand lines are 4096 px wide; crowns are 2048 × 2048; avatars are 1024 × 1024; the app icon is 512 × 512. All 23 core marks/lockups have transparent backgrounds. The five social/app tiles have intentional backgrounds. The brand guide has a presentation background.

The supplied taglines are outlined artwork. Body/UI font choice remains a recommendation rather than a separate locked typeface. Flat RGB gold is a colour, not a physical foil specification.

## Source and approval

[Exact primary master](source/approved-primary.svg) · [Component paths and provenance](source/master-components.json) · [Brand lock](brand-lock.json) · [Approval record](../operations/10-BRAND-APPROVAL-04.md) · [QA report](qa/technical-qa.json)

Previous reference images and crown alternatives have been removed from the current repository asset set. Use this page and the active register for current work.

## Rebuild the exports

The deterministic scripts require Python 3, Pillow, NumPy, SciPy and Inkscape. Run from the repository root:

```sh
python brand/scripts/build_assets.py
python brand/scripts/build_brand_page.py
python brand/scripts/verify_assets.py
```

The verification script checks the output files and creates inspection sheets. The `--visual-reviewed` flag records completed human/assistant inspection of those sheets; it is not a substitute for the recorded design approval. Any actual design change requires a new approval.
