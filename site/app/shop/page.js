import Image from 'next/image';
import Link from 'next/link';
import { Header, Footer } from '../components/SiteChrome';
import { Arrow } from '../components/Icons';
import { archiveCards } from '../cards/experience';
import { absoluteUrl, SITE_NAME } from '../site-config';

const title = 'HISTROVE shop — Coming soon';
const description = 'A first look at HISTROVE Crypto Season One booster packs, the companion book and artwork display concepts. The shop is coming soon; orders are not open yet.';
export const metadata = {
  title, description, alternates: { canonical: absoluteUrl('/shop') },
  openGraph: { title, description, type: 'website', siteName: SITE_NAME, url: absoluteUrl('/shop'), images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
};

export default function ShopPage() {
  const pizza = archiveCards.find(card => card.slug === 'pizza-day');
  return <div id="top"><a className="skip-link" href="#shop-main">Skip to the shop preview</a><Header shop/>
    <main id="shop-main" className="shop-page">
      <section className="shop-intro" aria-labelledby="shop-title">
        <div><span className="label gold"><span className="status-dot"/> THE HISTROVE SHOP / COMING SOON</span><h1 id="shop-title">History Worth Holding.<br/><span>Taking shape.</span></h1></div>
        <div className="shop-intro-note"><p>A first look at the physical collection.</p><p>Purchases aren’t open yet. Explore the previews while Crypto Season One comes together.</p><a className="text-link" href="#booster-packs">Explore the previews <Arrow direction="down"/></a></div>
      </section>
      <section className="shop-booster" id="booster-packs" aria-labelledby="booster-heading">
        <div className="shop-pack-stage"><span className="shop-image-label">PRODUCT VISUALISATION / PREVIEW</span><div className="shop-pack-image"><Image src="/collection/histrove-booster-concept-v1-web.webp" width={1536} height={1024} alt="Concept preview of HISTROVE Crypto Season One booster packs; final finish may differ" priority sizes="(max-width:760px) 88vw, 55vw"/></div><span className="shop-stage-coordinate">HISTROVE / CRYPTO / SEASON 01</span></div>
        <div className="shop-product-copy"><span className="label gold">01 / BOOSTER PACKS</span><h2 id="booster-heading">Crypto Season One.</h2><p className="shop-product-lead">The moments behind the movement, made collectible.</p><p>The approved 10-card pack design brings the HISTROVE artwork into the physical collection. Each card opens a deeper story in the online archive.</p><div className="shop-availability"><span className="status-dot"/><span>Coming soon <small>Prices and release details to be announced</small></span></div><Link className="text-link" href="/#archive">Explore the card stories <Arrow/></Link></div>
      </section>
      <section className="shop-companions" aria-labelledby="companions-heading"><div className="shop-section-heading"><span className="label gold">MORE OF THE STORY</span><h2 id="companions-heading">Beyond the pack.</h2><p>The book and display ideas taking shape alongside the cards.</p></div>
        <div className="shop-companion-grid"><article className="shop-companion"><div className="shop-book-stage"><span className="shop-image-label">BOOK VISUALISATION / PREVIEW</span><div className="shop-book-mockup"><Image src="/collection/histrove-book-concept-v1-web.webp" width={1536} height={1024} alt="Concept preview of an open HISTROVE companion book with the existing Pizza Day art and story spread; binding is illustrative" sizes="(max-width:760px) 88vw, 45vw"/></div></div><div className="shop-companion-copy"><span className="label gold">02 / THE COMPANION BOOK</span><h3>The whole story, together.</h3><p>Original artwork, the history behind it, and the details hidden in each illustration. Explore the editorial spreads as the book takes shape.</p><Link className="text-link" href="/cards/pizza-day">Explore a sample chapter <Arrow/></Link></div></article>
        <article className="shop-companion"><div className="shop-display-stage"><span className="shop-image-label">ART DISPLAY / CONCEPT</span><div className="display-frame"><Image src={pizza.media.artwork.src} width={pizza.media.artwork.width} height={pizza.media.artwork.height} alt="Pizza Day artwork in a proposed display frame; concept preview" sizes="(max-width:760px) 55vw, 280px"/></div></div><div className="shop-companion-copy"><span className="label gold">03 / ARTWORK BEYOND THE CARD</span><h3>A place for the artwork.</h3><p>An early display concept for the illustrations. Formats, materials and availability are still to be confirmed.</p><span className="collection-status">CONCEPT PREVIEW</span></div></article></div>
      </section>
      <section className="shop-closing" aria-labelledby="shop-closing-heading"><Image src="/brand/histrove-crown.svg" width={34} height={34} alt=""/><h2 id="shop-closing-heading">The shop is on its way.</h2><p>These are concept previews, not products available to order.<br/>Packaging finish, book binding and display materials are illustrative.</p><Link className="outline-button" href="/#archive">Back to the archive <Arrow/></Link></section>
    </main><Footer/></div>;
}
