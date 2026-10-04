# Separately saved website media

These deterministic transport bundles contain the individual display files listed in index.json. They are separate from every approved art, book and print master. `npm run build` and `npm run dev` automatically restore each file into public/archive or public/closeups and verify its SHA-256 before serving it.

Bundling keeps the preview publication atomic and avoids hundreds of individual upload operations. It does not alter or combine the images displayed on the site. Each is served at its own URL, loaded independently and eligible for Next image optimization.

`web-card-derivatives.json` records all 31 card sources, original checksums and precise print-bleed removal. Cropped web previews use the approved print-v1 cut box [36,36,744,1038] on the 816×1110 master. Originals are unchanged. Book pages are rasterized from their current published PDFs. Clues are deterministic, visually verified crops of the exact approved artwork; no generated objects.


The 022 addition is append-only: display-06.bin holds eight new WebP images (card, full artwork, two PDF pages and four actual-art clue crops). The six earlier bundles and all 219 earlier media records and hashes are unchanged. The full index contains 227 images and 119 close-ups.

The 028 addition is append-only: display-07.bin holds eight images from the approved cliff artwork and final card/book (card, full artwork, two PDF pages and four visually verified clue crops). All 227 earlier media records and bundles remain unchanged. The full index now contains 235 images, 123 clue close-ups and 56 book-page previews.

029 is append-only: display-08.bin holds seven new WebPs (card trim, full art, two book pages, three actual-art clues). All 235 previous images and bundles are unchanged. Totals: 242 images, 126 clue close-ups and 58 book previews.

030 is append-only: display-09.bin holds eight new WebPs (card trim, full art, two book pages and four actual-art clues). All 242 previous images and bundles are unchanged. Totals: 250 images, 130 clue close-ups and 60 book previews.

031 is append-only: display-10.bin holds seven WebPs (card trim, full art, two book pages and three actual-art clues). All 250 earlier images and bundles are unchanged. Totals: 257 images, 133 clue close-ups and 62 book previews.

## 032 Ethereum Goes Live

The approved 032 artwork, Mythic card and two-page book are preserved as originals. `display-11.bin` appends eight separate website images: a bleed-free trim preview, full art, two full book-page previews and four actual-art clue crops. The first 257 image records and all earlier bundles are unchanged. See `032-derivatives.json` for source hashes, crop boxes and derived-image hashes. Original downloads are pinned to the immutable 032 asset commit; full-A4 reproduction remains a separate approval.
