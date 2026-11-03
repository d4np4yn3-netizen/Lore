import Image from 'next/image';
import Link from 'next/link';
import { Header, Footer } from '../components/SiteChrome';
import { absoluteUrl, SITE_NAME } from '../site-config';
import styles from './shop.module.css';

const title = 'HISTROVE shop — Booster packs and companion book';
const description = 'Preview HISTROVE’s 10-card Crypto Season One booster packs and crypto history companion book. Orders are not open yet.';
export const metadata = {
  title, description, alternates: { canonical: absoluteUrl('/shop') },
  openGraph: { title, description, type: 'website', siteName: SITE_NAME, url: absoluteUrl('/shop'), images: [{ url: '/brand/histrove-social-border.png', width: 1200, height: 630, alt: 'HISTROVE — History Worth Holding' }] },
  twitter: { card: 'summary_large_image', title, description, images: ['/brand/histrove-social-border.png'] },
};


export default function ShopPage() {
 return <div id="top"><a className="skip-link" href="#shop-main">Skip to the shop</a><Header shop/>
 <main id="shop-main" className={styles.shop}>
<section className={styles['shop-intro']} aria-labelledby="shop-heading">
<div><p className={styles['eyebrow']}>HISTORY WORTH HOLDING</p><h1 id="shop-heading">Shop History<span>.</span></h1></div>
<p className={styles['intro-copy']}>Collect the cards.<br/> Discover the stories behind them.</p>
</section>
<figure className={styles['character-banner']}><div className={styles['banner-art']}><Image src="/collection/histrove-shop-characters-v1.webp" width="2172" height="724" alt="Illustration of the HISTROVE tortoise holding collectible cards and the HODL character holding the proposed black and gold book" sizes="(max-width:700px) 180vw, 91vw"/><div className={styles['banner-copy']}><span>CARDS. ART. STORIES.</span><p>Find your<br/>next story.</p></div></div><figcaption>Illustration and product concept.</figcaption></figure>
<section className={styles['products']} aria-label="HISTROVE products">
<article className={styles['product']} id="booster-packs">
<div className={styles['product-image']}><Image src="/collection/histrove-booster-concept-v1-web.webp" alt="HISTROVE Crypto Season One 10-card booster pack artwork" width="1536" height="1024" sizes="(max-width:700px) 90vw, 48vw"/><span className={styles['image-label']}>CRYPTO / SEASON ONE</span></div>
<div className={styles['product-copy']}><p className={styles['eyebrow']}>01 / COLLECT THE CARDS</p><h2>10-card booster pack</h2><p>Ten cards. A new handful of history.<br/>Discover the moments that shaped crypto.</p>
<div className={styles['product-foot']}><div className={styles['availability']}><span className={styles['status-dot']} aria-hidden="true"/>Coming soon</div><button type="button" className={[styles['buy-button'],styles['shop-spotlight']].join(" ")} disabled aria-describedby="booster-availability"><span className={styles['shop-glint']} aria-hidden="true"></span>Buy now <svg aria-hidden="true" width="19" height="19" viewBox="0 0 24 24" fill="none"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" strokeWidth="1.5"/></svg></button></div>
<p id="booster-availability" className={styles['availability-note']}>Purchasing will open when the shop is ready.</p></div>
</article>
<article className={styles['product']} id="companion-book">
<div className={styles['product-image']}><Image src="/collection/histrove-hardback-cover-concept-v1.webp" alt="Concept visualization of the black and gold HISTROVE companion book cover" width="1536" height="1024" sizes="(max-width:700px) 90vw, 48vw"/><span className={styles['image-label']}>COVER CONCEPT</span></div>
<div className={styles['product-copy']}><p className={styles['eyebrow']}>02 / GO BEHIND THE ART</p><h2>HISTROVE companion book</h2><p>The artwork, the details and the stories.<br/>A companion to Crypto Season One.</p>
<div className={styles['product-foot']}><div className={styles['availability']}><span className={styles['status-dot']} aria-hidden="true"/>Coming soon</div><button type="button" className={[styles['buy-button'],styles['shop-spotlight']].join(" ")} disabled aria-describedby="book-availability"><span className={styles['shop-glint']} aria-hidden="true"></span>Buy now <svg aria-hidden="true" width="19" height="19" viewBox="0 0 24 24" fill="none"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" strokeWidth="1.5"/></svg></button></div>
<p id="book-availability" className={styles['availability-note']}>Book visualization, final production details to be confirmed.</p></div>
</article>
</section>
<section className={styles['inside']} aria-labelledby="inside-heading">
<div className={styles['inside-heading']}><div><p className={styles['eyebrow']}>A CLOSER LOOK</p><h2 id="inside-heading">The story opens here<span>.</span></h2></div><p>Draft interior · 6 × 9 in<br/><span>008 / Pizza Day</span></p></div>
<div className={styles['book-stage']}>
<figure className={styles['open-book']} aria-label="Open-book visualization using the actual draft pages 16 and 17">
<div className={[styles['page'],styles['page-left']].join(" ")}><Image src="/collection/histrove-6x9-draft-pizza-page-16.png" width="778" height="1167" alt="Draft page 16: Pizza Day illustration with the caption 10,000 Bitcoins for Pizza" unoptimized/></div>
<div className={[styles['page'],styles['page-right']].join(" ")}><Image src="/collection/histrove-6x9-draft-pizza-page-17.png" width="778" height="1167" alt="Draft page 17: Pizza Day, 22 May 2010, historical story and details in the artwork" unoptimized/></div>
</figure>
</div>
<div className={styles['inside-caption']}><p>Actual editorial draft pages, presented as an open-book visualization.</p><Link href="/shop/interior">Read the draft pages <svg aria-hidden="true" width="19" height="19" viewBox="0 0 24 24" fill="none"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" strokeWidth="1.5"/></svg></Link></div>
</section>
<details id="pack-details" className={styles.packDetails}>
<summary>Pack contents, finishes and FAQ</summary>
<div className={styles.packDetailsBody}>
<h2>What is in a booster pack?</h2><p>The current plan is four Common, three Uncommon, two Rare and one premium card. The premium slot is Epic, Legendary or Mythic. The pack plan remains subject to printer collation and production quantities.</p>
<h3>Which cards will have foil versions?</h3><p>Foil selection and odds are under review. No final foil count or pull rate is promised. Final product details will be confirmed before orders open.</p>
<h3>Can I order or register interest?</h3><p>Purchases aren’t open yet. First-print interest requests one email when preorders open. It is not an order, payment or reservation, does not guarantee availability and does not subscribe you to a newsletter.</p>
<Link href="/#coming-soon">First-print plans and interest signup <svg aria-hidden="true" width="19" height="19" viewBox="0 0 24 24" fill="none"><path d="M5 19 19 5M5 5h14v14" stroke="currentColor" strokeWidth="1.5"/></svg></Link>
</div></details>
<section className={styles['closing']} aria-label="Shop availability"><span className={styles['status-dot']} aria-hidden="true"/><p>A new chapter is coming.</p><span>Cards and book purchases are not open yet.</span></section>
</main><Footer/></div>;
}
