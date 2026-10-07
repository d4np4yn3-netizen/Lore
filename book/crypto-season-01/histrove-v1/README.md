# HISTROVE Crypto Season One book revision

Current branded online-book derivatives, 6 October 2026. The 39 historical two-page proofs remain intact under `../proofs/`; this revision adds separate PDFs and page previews. The original artwork, history, clues, source links and page dimensions are preserved. This is not a physical book reproduction or printer approval.

## Changes

- Replaced the editorial page header with HISTROVE / CRYPTO SEASON ONE in all 39 PDFs
- Replaced 20 editorial brand references in 15 chapters; exact before/after wording is in `text-replacements.json`
- Replaced the old brand in document titles/authors, preserving the other metadata
- Preserved all 39 artwork pages, including their native image streams and exact rendered pixels
- Preserved every factual paragraph, clue, source URL, illustration, original review/release footer and page geometry
- Kept original font families, sizes and line spacing; affected paragraphs retain the same line count and height. The cup clue in 017 uses an extra 3.276 pt of available width up to the existing 43 pt right margin

The book headers are editorial text, as in the originals. No brush logo or new tagline has been added inside an otherwise unchanged book layout.

## Current sources

`chapters/` contains all 39 current brand-wording chapter files. Only visible standalone brand words were replaced. Link targets are protected from brand substitution; the existing card-image and book-PDF links point to the approved current HISTROVE files, and relative paths are rebased for this chapter directory. External URL targets are unchanged. Original source Markdown and historical builders remain recoverable in their original locations. Use these current chapters rather than rerunning an old brand-specific sync script over the active website.

`manifest.json` maps every old/new PDF and preview, plus source/output SHA-256 values. `qa.json` records geometry, unchanged artwork, pixel comparison, URI, exact paragraph and visual checks. `chapter-links-qa.json` verifies all 39 chapter files: two relative targets resolve to exact pinned/current assets and all external URL targets remain unchanged. `source/layout-audit.json` records each affected semantic paragraph and the original position/style.

## Rebuild

The original input revision is c887b8ee293e36a0f0c7044a780af77f7b51efa4 in d4np4yn3-netizen/Lore. Required packages are PyMuPDF, ReportLab, Pillow and NumPy, plus Poppler pdftoppm. The original repository-pinned DejaVu Sans files are required; their hashes are recorded in the manifest.

From a complete repository checkout, run the following with a separate output directory. The original PDF SHA-256 values are checked before any derivative is authored. The original media snapshot selects the old preview paths, and the preserved site media bundles supply those files.

    python book/crypto-season-01/histrove-v1/source/rebrand_books.py --original-root . --site-root site --font-root cards/master/front-v3/source/fonts --output-root /tmp/histrove-book-output

Previews use distinct `NNN-histrove-page-N.webp` paths. First-page previews are exact original bytes under new names. Second pages are full Poppler renders at 778 × 1100, encoded WebP quality 90, matching the existing display format. Do not overwrite the historic originals or their previews.

## Verification limits

All 39 PDFs pass digital checks. At 144 dpi there are zero altered pixels outside the permitted header and brand-paragraph regions. All original paragraph punctuation and word order are retained after replacing LORE with HISTROVE. Source URI target lists remain exact. Every changed paragraph and all artwork pages have been visually inspected. Physical reproduction and print acceptance remain separate.

045 BitConnect appends a two-page full-art/editorial book chapter, matching 044's layout. Five story paragraphs and four clue texts exactly mirror the site. The native artwork remains 1060×1484; contain placement is 128.21 effective PPI. Physical reproduction approval is not implied.
