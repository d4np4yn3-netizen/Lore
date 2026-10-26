# Footer restoration method and PDF checks

## Result

The eleven current physical-print PDFs for 067–075, 077 and 078 have their missing `SEASON 01 •` restored. Every original file remains untouched. Corrected PDFs are in `../output/corrected/pdf/`. All eleven render with **zero changed pixels outside the footer**, and all twenty-two before/after QR checks decode to the same card-specific route. Every corrected footer was visually inspected in `pdf-footer-before-after-contact-sheet.png`.

The actual changed pixel bounds are `[184, 1003, 340, 1015)` in every 300-DPI PDF render. The existing `CRYPTO •` prefix remains pixel-identical, and the replacement text does not touch the rarity divider or bottom frame. Native vector geometry is retained; these are not flattened image PDFs.

## Sources and scope

- Repository: `d4np4yn3-netizen/Lore`, pinned main `cfcb892c6b4fb80369cec867eca41d036ca10ef5`.
- Source PDFs: `../source/pdf/NNN.pdf`, downloaded by the parent from the current publication map.
- Exact approved native SVGs: `../../footer-audit-publication-map/pinned-svgs/NNN.svg`.
- Policy read: current root and Crypto AGENTS, CURRENT-STATUS, PROJECT-MEMORY, brand lock/core/visual identity/asset QA and Crypto COLLECTION-RULES.
- Canonical approved master: `cards/crypto/master/histrove-print-v1`, not historical LORE master or archived print revisions.
- This work changes only the missing season footer. It does not update QR captions, art, titles, rarity, frame, crop, routes, books or publication state. 076 is digital-only and is not given a physical PDF. Card 100 is not part of this correction.

## Exact native footer specification

All 98 current approved SVGs supplied by the source-mapping agent contain one plain `text` element with `id="set-number"`. Their footer element attributes, ancestor transform and canvas are identical; see `footer-native-style-groups.json`.

```xml
<text x="58" y="1247.625" font-family="DejaVu Sans"
      font-size="17" font-weight="400" letter-spacing="1"
      fill="#F5F2EB" text-anchor="start" id="set-number">
  CRYPTO • SEASON 01 • NNN/100
</text>
```

This is one line, with literal U+2022 bullets and ordinary spaces. The text is bone `#F5F2EB` at every rarity, not rarity-colored. The existing divider is `M58 1223.625H842`, stroke width `1`, opacity `.45`; its rarity color must not change:

| Rarity | Divider color |
|---|---|
| Common | `#BFC4C9` |
| Uncommon | `#59C991` |
| Rare | `#55B7FF` |
| Epic | `#B98AFF` |
| Legendary | `#D4AF37` |
| Mythic | `#CFE5F1` |

The locked front transform is `translate(66.690744921 66.690744921) scale(0.758465011287)`, inside an 816 × 1110 viewBox with 69.088 × 93.98 mm physical canvas. In native raster coordinates, the footer anchor is `(110.6817156, 1012.9706546)`, the font size is `12.8939052 px`, and the divider is at `y=994.7674944`.

The authoritative DejaVu Sans regular font is repository Git blob `fb0bd945a4f5aa716dcb8d9b7476bfa30e365a1e`, SHA-256 `ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280`. The verified local copy is `../../card077-release/cards/master/front-v3/source/fonts/DejaVuSans.ttf`, reached through that directory's original `fontconfig.xml`.

All six downloaded template SHA-256 values match the current print specification. Template files contain generic `ASM` placeholder footer copy; use their geometry/style, not that placeholder text. COLLECTION-RULES expressly records the approved Crypto footer on 26 September 2026 as `CRYPTO • SEASON 01 • NNN/100` and classifies it as a text-field change.

## SVG and PNG recommendation

Change only the contents of the existing `set-number` text element by a tightly asserted byte replacement. Do not call the complete card renderer, rebuild QR, re-embed artwork or reserialize the whole XML tree. Preserve the original XML byte prefix/suffix.

For each PNG, first render the unchanged native SVG with the original pinned font configuration and compare against the exact current PNG. The 067 baseline test is pixel-identical (zero RGB differences). A fully rerendered corrected SVG is therefore valid when its unchanged baseline matches and the corrected raster has zero differences outside the footer. If another source has historical renderer noise, splice only the freshly rendered footer band into the exact original raster after verifying the band is clear of other artwork or frame geometry. Do not accept unquantified full-frame render noise as a default.

For 067, the old footer alpha bounds are `[111,1003,242,1015)`, the restored footer bounds are `[111,1003,340,1015)`, and a conservative patch region is `[108,1000,344,1017)`. Transparent PNG alpha compositing differs by ±1 in 144 existing text-edge pixels because of rounding; rendering against the native opaque backdrop avoids that unnecessary change. Other native SVGs have identical geometry, but still require per-file verification.

## PDF preservation implementation

The current PDFs use outlined text. Each of the eleven affected PDFs ends its page content stream with the footer's outline path. A fresh, isolated export of the exact **old** footer—with the same physical page size, transform, font and Inkscape `--export-text-to-path`—produces a byte-identical terminal footer block in each original PDF. The correction script asserts that equality before it writes anything for that card.

`restore_pdf_footers.py` then exports only the new footer outline and replaces only that final block. All content bytes before it remain identical. It writes an incremental PDF update with pypdf: the entire original PDF is retained byte-for-byte as the output's prefix; the page gets a new compressed content stream containing its original content prefix plus the replacement footer. Resource dictionaries and references are unchanged. No original image, frame, gradient, logo or QR object is rerendered or replaced. The footer remains vector outlines, not an added bitmap or font dependency.

Each output retains its original MediaBox, TrimBox, BleedBox and ArtBox exactly. The original source PDFs have a MediaBox approximately `[0,0,195.839993,266.40001]` pt; precise values are recorded per card in the QA JSON. The minute source floating-point height makes Poppler's 300-DPI raster 816 × 1111; before and after use the same untouched boxes and render dimensions. This is not a change to native 816 × 1110 SVG/PNG production geometry.

Checks performed on every corrected PDF:

1. Exact old-footer outline-byte match against isolated native export.
2. Original source PDF retained as exact file prefix.
3. Exact original page content prefix retained.
4. Exact resource dictionary/reference serialization retained.
5. All four page boxes unchanged.
6. Poppler before/after 300-DPI rendering; zero RGB pixel differences outside the specified footer band.
7. QR decode of both renders equals `https://lore-site-v1.vercel.app/crypto/NNN/`.
8. Visual inspection of every original/restored footer strip, including full wording, collector number, baseline, divider and bottom-frame clearance.

Machine-readable results, source/output SHA-256 values and render paths are in `pdf-footer-correction-qa.json`. Before/after renders and isolated outline proofs are under `pdf-qa/` for reproducibility. The marker for an eleven-PDF edit operation ran successfully once before authoring.

## Limits

These are local review corrections only. No repository, website, Library original, live route or physical-print availability was changed. Technical export QA does not establish physical printer/sample acceptance, rights clearance or publication approval. Incremental PDFs intentionally retain their original pre-correction revision inside the file; only the current visible page references the restored footer.
