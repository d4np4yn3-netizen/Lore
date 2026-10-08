// Keep public identity URLs independent of temporary deployment/preview hosts.
// Change only after an approved domain migration; printed /crypto/ URLs stay valid.
export const SITE_ORIGIN = 'https://lore-site-v1.vercel.app';
export const SITE_NAME = 'HISTROVE';
export const SITE_TITLE = 'Crypto History Collectible Cards & Illustrated Stories | HISTROVE';
export const SITE_DESCRIPTION = 'Explore 47 illustrated crypto-history stories from HISTROVE’s 100-card collection in the making, with physical card and companion-book previews. History Worth Holding.';
export const absoluteUrl = path => new URL(path, SITE_ORIGIN).href;
