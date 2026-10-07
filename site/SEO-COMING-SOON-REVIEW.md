# Search visibility and launch-list review

Status: review branch only. Email registration is deliberately closed. Production release is a separate approval.

## Changes

- One public origin configuration for the existing site address, canonical URLs, sitemap, robots and structured data
- A 48-page sitemap covering the homepage and 47 preferred `/cards/` routes; printed `/crypto/` aliases remain unchanged
- Descriptive event metadata and individual approved artwork for Open Graph and Twitter on every card
- WebSite, Article and BreadcrumbList JSON-LD, without invented authors, publication dates, product offers or historical dates presented as publication dates
- All existing clue text, original-art/print links and companion-book PDF links in the initial HTML, with the tab experience retained and inactive images lazy-loaded
- A no-JavaScript fallback that exposes all editorial panels
- A responsive Coming soon section and a visibly closed launch-list design. Disabled controls, no form submission, no API endpoint, no email storage, no success simulation and no analytics integration

Card names, story copy, artwork, 200 historical clues, 94 book previews, print files and 47 printed QR routes are preserved. The public puzzle mention is a teaser only.

## Verification

Run from `site/`:

```sh
npm test
npm run build
npm run test:search
```

All three pass locally. `test:search` examines built HTML for all preferred routes, unique metadata and artwork, JSON-LD, 200 clue texts, 94 lazy book previews, sitemap/robots, safe JSON serialization and the closed signup state.

A same-process local HTTP sweep also passes: all 47 editorial routes return 200; all printed `/crypto/NNN/` aliases retain their existing 308 → 308 → 200 chain; homepage, sitemap and robots return 200; unknown stories and the nonexistent collection endpoint return 404.

Browser interaction and visual checks are pending on the protected preview. These local checks do not establish search-engine indexing, physical-device testing, social-platform crop appearance or email deliverability.

## Email activation gate

Do not enable the launch list until a real provider, costs, sending domain, controller/contact details, retention policy and privacy notice are approved. The final implementation must record the consent-copy/privacy versions, confirm email ownership, honour unsubscribes and retry safely. Pending addresses must not silently become subscribed. Review rate limiting and quota caps; never log email addresses or confirmation secrets to analytics.

No new service, account, credential, billing plan, domain, marketing message or live email capture is included in this change.
