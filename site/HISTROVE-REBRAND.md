# Card-edge preview correction — 6 October 2026

Dan requested cutting website cards at their visible borders. The first HISTROVE web export removed physical bleed at the trim line but retained the intentional black print margin outside the coloured frame. Current derivatives are cropped at the frame's outer stroke instead, with SVG-derived transparent rounded corners. All 39 use source bounds (72.3792325, 72.3792325) to (743.6207675, 1037.6207675), conservative integer crop [72,72,744,1038], and 600×863 WebP output. The complete stroke, artwork, lettering and QR remain inside the crop; every actual final QR decodes correctly.

Homepage, timeline/grid/discovery previews, reader's View collectible card link, and social metadata use the current versioned border assets. All earlier web assets remain available. The existing print PNG link is explicitly labelled Print card PNG; its URL and file bytes are unchanged. No shared-back image is displayed on this website; the existing Print shared back PDF download is unchanged. Original art, books, print masters, source files, QR routes and all factual data are unchanged.

Current generator: `python site/scripts/build-histrove-border-cards.py --repo . --out /tmp/histrove-border-review` (Pillow and zxing-cpp). Current exact geometry/QR/hash record: `media/histrove-border-manifest.json`. The earlier trim-only generator below is historical.

---

# HISTROVE website rebrand

6 October 2026 · History Worth Holding

## Scope and authorization

Dan requested the webpage, associated code and tagline update after approving HISTROVE's exact crown/brush identity, 39 card fronts/back and 10-card booster. This release changes current presentation and download pointers. The repository name and existing Vercel address remain unchanged. No domain purchase, project rename, authentication change or artwork regeneration is included.

## Changed

- Homepage, navigation, accessibility labels, footer, reader metadata, social preview and icons use HISTROVE
- Existing timeline, grid/search, modal reader, artwork/clue interactions and desktop/mobile editorial layout are retained
- 39 new 600×837 lossless WebP card fronts are exact LANCZOS resamples of the approved 744×1038 trim crop, excluding the 36px printer bleed on each side
- 39 card PNG/PDF/SVG downloads and the shared back use the approved HISTROVE print release, pinned to an immutable GitHub commit
- Packaging preview uses the current approved 10-card booster, cropped to its front face without bleed or blank heat-seal strips
- 39 new book PDFs, 78 previews and 39 current chapter sources replace brand headers and 20 brand-referencing paragraphs only. Native artwork, facts, clues, sources, links and page dimensions are preserved. The artwork-only page and its preview remain pixel/byte identical
- One longer brand mention on 017 needs a 3.276pt wider text region, inside the existing outer margin; font size, line spacing and paragraph height are unchanged

## Preserved

All 39 /crypto/NNN/ routes, 168 clue records/crops, full-art derivatives and original art download origins are unchanged. The existing https://lore-site-v1.vercel.app/ address remains the physical QR destination. Historical source files and 324 previous display assets remain recoverable. New media is append-only; unchanged book artwork previews share existing packed bytes under new current filenames.

Old names in historical files, original-source paths, GitHub repository addresses and the existing deployment host are intentional. Do not globally replace those references. Historical generators and per-release tests are retained as records; do not run them over current asset maps.

## Reproduce and validate

From the repository root:

```sh
python site/scripts/build-histrove-brand-assets.py --repo . --out /tmp/histrove-web-review --require-qr
cd site
npm test
npm run build
```

The visual builder uses Pillow and zxing-cpp for actual final-image QR decoding. Approved inputs are checked by SHA-256. Output is separate from source masters. Book reconstruction instructions and source are in book/crypto-season-01/histrove-v1/README.md and source/.

Tests cover 39 current/QR records, 168 unchanged clues, 1,344 non-overlapping marker positions across eight widths, 441 indexed historical/current image hashes, completed visual derivative hashes, 120 current printer-file paths/hashes, and current book/chapter/preview hashes. Brand-only substitutions are pinned against pre-rebrand main c887b8ee293e36a0f0c7044a780af77f7b51efa4. Build statically generates the homepage, 39 details and 39 QR redirects. No separate linter was previously configured.

Final deployment readiness and browser screenshots are reported after the exact release commit reaches READY. Local compilation/static-data checks are distinct from production browser and HTTP checks. Physical samples, print colour, phone-camera scanning, book reproduction rights and trademark clearance are not established by this release.
