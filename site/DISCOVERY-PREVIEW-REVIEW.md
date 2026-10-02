# Discovery and physical collection review — 2 October 2026

Dan reviewed the rendered discovery and physical-collection preview and explicitly authorized making it live on 2 October 2026. Work is tracked in PR #7, based on production b020fa81. Publication follows the final mobile marker-spacing check. The existing approved booster front was reused rather than redesigned.

## Changed experience
- A compact four-step preview near the top introduces the card, complete illustration, hidden detail and book spread. Each action opens the matching reader tab.
- Optional numbered clue markers use the existing 115 normalized bounding boxes. Tap or keyboard activation opens the exact inspected crop and canonical explanation. Closing returns focus to the chosen marker.
- Three era introductions group the unchanged year timeline: 1982–2004, 2008–2012 and 2013–2014.
- The physical collection section uses a separate website-only render of the approved booster front, actual editorial book pages and an explicitly labelled art-display concept. No prices, stock, checkout, physical sample or finished-book claim.
- The book feature CTA goes directly to Book pages.

## Verification so far
- Local `npm run build`: PASS, all 55 generated pages; 26 card pages and 26 existing QR destinations.
- Vercel isolated preview: READY for commit 7f3fda0e529d020e0f1d07c686999131c13f556a; Vercel commit check successful.
- All 219 existing website media files verified against the committed SHA-256 index. All 115 clue boxes are valid and their crops exist.
- Remote comparison: only the six UI source files and one new web booster derivative changed in the initial preview commit. Original card art, print masters, story/clue prose, QR route source, existing media bundles and logo geometry are unchanged. Card 022 remains absent.
- No lint or test command is configured in the source project. `git diff --check`: PASS.
- The authorized temporary review link opens successfully. Actual desktop discovery and physical-collection screenshots have been captured and visually checked. Independent mobile/keyboard verification is in progress. Local Chromium fails to launch in the current execution environment, so rendering checks use the cloud browser. Project protection settings have not been changed.
- A source-level small-screen marker collision was corrected with collision-aware placement and leader lines back to the unchanged source coordinates. 920 positions across eight canvas widths (240–1400px) pass a minimum 52px separation and 24px edge-inset check. A new optimized build also passed.

## Release boundary
Dan's explicit production approval is recorded on 2 October 2026. Finish independent mobile/keyboard checks before merging. Actual desktop screenshots have been reviewed. Production deployment and all stable QR routes must be verified after merge. Physical sample, print and book reproduction release statuses remain unchanged.

Run `node scripts/check-discovery.mjs` from `site/` for the reproducible data, spacing, source-route and asset-hash checks. Booster source/website derivative provenance is recorded in `collection-media.json`.
