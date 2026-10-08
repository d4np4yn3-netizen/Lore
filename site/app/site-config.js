// Keep public identity URLs independent of temporary deployment/preview hosts.
// Change only after an approved domain migration; printed /crypto/ URLs stay valid.
export const SITE_ORIGIN = 'https://lore-site-v1.vercel.app';
export const SITE_NAME = 'HISTROVE';
export const SITE_TITLE = 'HISTROVE — History Worth Holding';
export const SITE_DESCRIPTION = 'Explore crypto history through illustrated collectible cards, original artwork, hidden details and companion book pages. Discover HISTROVE Crypto Season One.';
export const absoluteUrl = path => new URL(path, SITE_ORIGIN).href;
