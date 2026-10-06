import './globals.css';
const title = 'HISTROVE — History Worth Holding';
const description = 'History Worth Holding. Explore an illustrated history of crypto through collectible cards, original artwork, hidden details and the stories of Crypto Season One.';
export const metadata = {
  metadataBase: new URL('https://lore-site-v1.vercel.app'),
  title, description, applicationName: 'HISTROVE',
  openGraph: { title, description, siteName: 'HISTROVE', type: 'website', url: '/', images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
  icons: { icon: [{ url: '/brand/histrove-crown.svg', type: 'image/svg+xml' }, { url: '/brand/histrove-icon.png', type: 'image/png', sizes: '192x192' }], apple: '/brand/histrove-apple-icon.png' },
};
export default function RootLayout({children}) { return <html lang="en"><body>{children}</body></html>; }
