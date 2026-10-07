import './globals.css';
import { SITE_ORIGIN, SITE_TITLE as title, SITE_DESCRIPTION as description } from './site-config';
import { websiteSchema, jsonLd } from './seo';
export const metadata = {
  metadataBase: new URL(SITE_ORIGIN),
  title, description, alternates: { canonical: '/' }, applicationName: 'HISTROVE',
  openGraph: { title, description, siteName: 'HISTROVE', type: 'website', url: '/', images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
  icons: { icon: [{ url: '/brand/histrove-crown.svg', type: 'image/svg+xml' }, { url: '/brand/histrove-icon.png', type: 'image/png', sizes: '192x192' }], apple: '/brand/histrove-apple-icon.png' },
};
export default function RootLayout({children}) { return <html lang="en"><body><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(websiteSchema) }}/>{children}</body></html>; }
