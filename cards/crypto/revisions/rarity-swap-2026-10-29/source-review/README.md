# HISTROVE rarity swap — local review, 29 October 2026

User selected option B: 093 Common → Legendary, 071 Legendary → Epic, 064 Epic → Common. 015 remains Legendary; 046 remains Epic. Source baseline: 8456f7f5216e7d391e10e0e48c1515be497f35af.

The source patch contains 16 narrowly changed files. Revised SVG/PNG/WebP fronts and two-page book PDFs are separate review outputs. Do not deploy the source patch alone: active media and print manifests still intentionally select previously published files until a versioned release is integrated. No remote changes, PR, merge or deployment were made. PR12 and PR13 were not touched.

## Checks passed
- Exactly three catalogue rarity changes; other 97 rows unchanged.
- Before and after totals: 30 Common / 25 Uncommon / 20 Rare / 13 Epic / 8 Legendary / 4 Mythic.
- SVG comparison: only tier gradient, outer/inner decorative frame, badge text/width/placement and tier caption colour change. Embedded illustration/logo images, crown and other text/QR/geometry unchanged.
- Preserved restored-footer source for 071.
- All three revised print-size PNGs and border-cropped web cards decode to their original QR URLs.
- All three book art pages are pixel-identical to originals; extracted page-two text changes only the rarity word. Two A4 pages each.
- Four-card and book-spread visuals inspected; no clipping observed.

## Boundaries
015 artwork/card remains untouched. Its website source note is corrected alongside 093 to describe two Legendary frames, not Legendary/Common. The existing 015/093 750×1048 native-art / 90.71 effective A4 PPI and pending print-QA caveats remain. Old approval files, print manifests, historical binaries and prior art remain intact. Current-cards.json is known incomplete (093 absent); no missing catalogue rows were invented.

The gold appearance uses the existing Legendary vector gradient; it is not physical foil. No foil mask, print order or physical acceptance. Full website tests/build are not run because this is an isolated source subset, not an integrated deployable checkout. Before release, wire new versioned frame/book/image artifacts, update active hashes/origins/packed display archives, and run full checks.

See final-qa.json, validation.json and changed-source-files.json for evidence. See source-changes.patch for exact metadata/copy changes. Standalone scripts document the local preparation; they contain this executor’s absolute path.
