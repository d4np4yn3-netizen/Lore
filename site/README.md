# LORE Crypto Season One site

This site publishes approved cards one at a time. The collection currently contains card 001, Blind Signatures. Its stable QR destination is `/crypto/001/`, which redirects to the card detail page. Card 001's story, four clues and source/art note mirror the approved book chapter through `app/cards/content/001.json`; run `python ../book/crypto-season-01/sync_001.py --check` from the site directory to verify the copy before deployment.

Keep the printed QR destination stable when a custom domain is added, and verify the live destination before preparing each print-ready card. Card artwork and the season register elsewhere in the repository are preserved independently of the published collection.
