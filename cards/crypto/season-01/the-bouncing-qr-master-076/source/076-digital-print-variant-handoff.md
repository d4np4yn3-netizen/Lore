# Card 076: digital and physical QR separation

Status: planning note only; no visual change, secret generation, or publishing performed.
Source: Dan Payne, 18 October 2026 16:08:50 UTC: “there will be a different QR code on the digital version on the site to there is in the physical version”. Parent task direction: a free ARG opening on the website/digital images, with Common card 076 the first physical-card step.

## Current assets

HISTROVE-Crypto-076-Card-Proof-v2 and Art-QR-v2 are DIGITAL DRAFTS ONLY. Their existing TV destination is https://lore-site-v1.vercel.app/scan/076/, intended as the public digital entry. This route has not been made live by this task. The 816×1110 canvas and 300-DPI metadata do not designate this as the private physical variant.

Footer story QR remains https://lore-site-v1.vercel.app/crypto/076/ in BOTH variants.

No physical-only URL or secret has been minted. The physical puzzle structure and destination must be defined and approved before creating the physical variant.

## Required build change before dual-variant production

Replace hard-coded TV URL in build076v2.py with an explicit variant configuration:
- variant: digital | physical
- tv_qr_url: required, validated HTTPS destination supplied for that variant
- footer_qr_url: fixed shared story route
- output_root: separate public-digital and private-print destinations

Do not derive or guess a physical secret from the public route. Reject physical builds until their destination is explicitly supplied after puzzle approval. Label current provenance and output manifests DIGITAL_DRAFT.

Generate the main TV QR and the phone-preview miniature from the SAME QR matrix/configuration for each variant. Never reuse a digital phone-preview raster in the physical master. Both currently use deterministic SVG; maintain this connection during the parameterization. Keep the footer story QR independent and unchanged.

Version outputs distinctly, with variant in filenames, provenance, QA reports, and release manifests. Verify decoded TV destination equals the selected variant; verify decoded footer destination equals the fixed story route. Inspect phone-preview correspondence and full/trim/small renders. Physical paper scanning still needs a real printed sample.

## Publication boundary and leak prevention

Only digital art and digital-derived previews belong on the public website or in public source-control assets. Private physical masters, PDFs, book spreads, proof PNGs, SVGs, embedded images, build configuration and manifests may reveal the physical TV destination. SVG source exposes a code even if its visible display is hidden. The miniature phone preview also carries the same physical QR data.

Do NOT upload physical-only secrets or physical artwork to public GitHub, public Vercel assets, public PDF/download routes, public card books, public build logs, or ordinary public previews. Store physical masters in an authorized private destination and limit printer handoff to approved recipients. Public books must use the digital variant or a deliberately approved redacted representation, never the physical master by default. Check repository visibility and actual asset access before publishing; names such as “private” do not restrict access by themselves.

A physical QR is shareable through photos and is not proof of ownership. The ARG design must tolerate sharing or add a separately approved ownership mechanism; do not present this split alone as access control.
