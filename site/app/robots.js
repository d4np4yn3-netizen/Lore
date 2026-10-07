import { absoluteUrl } from './site-config';
export default function robots() {
  return { rules: { userAgent: '*', allow: '/' }, sitemap: absoluteUrl('/sitemap.xml') };
}
