import Image from 'next/image';
import Link from 'next/link';
import { Header, Footer } from '../components/SiteChrome';
import { Arrow } from '../components/Icons';
import { absoluteUrl, SITE_NAME } from '../site-config';

const title = 'HISTROVE shop — Booster packs and companion book';
const description = 'Preview HISTROVE’s 10-card Crypto Season One booster packs and crypto history companion book. Orders are not open yet.';
export const metadata = {
  title, description, alternates: { canonical: absoluteUrl('/shop') },
  openGraph: { title, description, type: 'website', siteName: SITE_NAME, url: absoluteUrl('/shop'), images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
};

export default function ShopPage() {
  return <div id="top"><a className="skip-link" href="#shop-main">Skip to the shop preview</a><Header shop/>
    <main id="shop-main" className="shop-page">
      <section className="shop-intro" aria-labelledby="shop-title"><div><span className="label gold"><span className="status-dot"/> CRYPTO SEASON ONE / COMING SOON</span><h1 id="shop-title">Shop HISTROVE<span>.</span></h1><p className="shop-intro-lead">Booster packs and the companion book.</p></div><p id="shop-closed-note">Purchases aren’t open yet. Preview the two products below; prices and launch details will be announced when confirmed.</p></section>
      <div className="retail-products" aria-label="Products coming soon">
        <article className="retail-product" id="booster-packs" aria-labelledby="booster-heading"><div className="retail-product-heading"><span className="label gold">COLLECTIBLE CARDS</span><h2 id="booster-heading">10-card booster pack</h2></div><div className="retail-product-image"><Image src="/collection/histrove-booster-concept-v1-web.webp" width={1536} height={1024} alt="Concept preview of HISTROVE Crypto Season One booster packs; final finish may differ" priority sizes="(max-width:760px) 88vw, 45vw"/></div><div className="retail-product-body"><p className="retail-description">Ten collectible cards celebrating moments from crypto history. Each card opens its story and artwork in the online archive.</p><a className="retail-cta" href="#launch-details" aria-describedby="shop-closed-note">Booster packs — coming soon <Arrow direction="down"/></a><p className="retail-status">Orders not open yet · Price to be announced</p><Link className="retail-preview-link" href="/#archive">Explore the cards <Arrow/></Link><p className="retail-concept-note">Concept product image. Final packaging finish may differ.</p></div></article>
        <article className="retail-product" id="companion-book" aria-labelledby="book-heading"><div className="retail-product-heading"><span className="label gold">THE COMPANION BOOK</span><h2 id="book-heading">Crypto history companion book</h2></div><div className="retail-product-image"><Image src="/collection/histrove-book-concept-v1-web.webp" width={1536} height={1024} alt="Concept preview of the HISTROVE companion book showing the existing Pizza Day art and story pages; binding is illustrative" sizes="(max-width:760px) 88vw, 45vw"/></div><div className="retail-product-body"><p className="retail-description">The stories behind the cards, with full-page artwork and explanations of the details hidden in each illustration.</p><a className="retail-cta" href="#launch-details" aria-describedby="shop-closed-note">Book — coming soon <Arrow direction="down"/></a><p className="retail-status">Orders not open yet · Price to be announced</p><Link className="retail-preview-link" href="/?moment=pizza-day&view=book">Preview the book pages <Arrow/></Link><p className="retail-concept-note">Concept product image. Book format and binding are not final.</p></div></article>
      </div>
      <section className="shop-closing" id="launch-details" aria-labelledby="shop-closing-heading"><Image src="/brand/histrove-crown.svg" width={34} height={34} alt=""/><h2 id="shop-closing-heading">Ordering opens here.</h2><p>Booster packs and the companion book are coming soon.<br/>Confirmed prices and launch details will appear here before orders open.</p><Link className="outline-button" href="/#archive">Explore the archive while you wait <Arrow/></Link></section>
    </main><Footer/></div>;
}
