import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
import styles from './ShopCollectionTeaser.module.css';

export default function ShopCollectionTeaser() {
  return <section id="collection" className={styles.teaser} aria-labelledby="collection-heading">
    <div className={styles.banner}>
      <Image className={styles.art} src="/collection/histrove-shop-characters-v1.webp" width={2172} height={724} sizes="(max-width:760px) 180vw, 91vw" alt="The HISTROVE tortoise holding collectible cards and the HODL character holding the proposed black and gold companion book"/>
      <div className={styles.copy}>
        <span className="label gold">THE PHYSICAL COLLECTION</span>
        <h2 id="collection-heading">History Worth Holding</h2>
        <p>Booster packs and the companion book.</p>
        <Link href="/shop" className={`gold-button shop-spotlight ${styles.shopLink}`}><span className="shop-glint" aria-hidden="true"/>Explore the shop <Arrow/></Link>
      </div>
    </div>
    <p className={styles.note}>Illustration and product concepts. Purchases are not open yet.</p>
  </section>;
}
