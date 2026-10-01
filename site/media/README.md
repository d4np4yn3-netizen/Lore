# Separately saved website media

These deterministic transport bundles contain the individual display files listed in index.json. They are separate from every approved art, book and print master. `npm run build` and `npm run dev` automatically restore each file into public/archive or public/closeups and verify its SHA-256 before serving it.

Bundling keeps the preview publication atomic and avoids hundreds of individual upload operations. It does not alter or combine the images displayed on the site. Each is served at its own URL, loaded independently and eligible for Next image optimization.

`web-card-derivatives.json` records all 26 card sources, original checksums and precise print-bleed removal. Cropped web previews use the approved print-v1 cut box [36,36,744,1038] on the 816×1110 master. Originals are unchanged. Book pages are rasterized from their current published PDFs. Clues are deterministic, visually verified crops of the exact approved artwork; no generated objects.
