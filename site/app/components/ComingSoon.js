import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
import { archiveCards } from '../cards/experience';
import { rarities, rarityCounts } from '../timeline/gallery-filters.mjs';
import styles from './ComingSoon.module.css';

// First-print interest uses the owner-managed Google Form; no local data collection.
export default function ComingSoon() {
  const counts = rarityCounts(archiveCards);
  return <section className={`coming-soon ${styles.compact}`} id="coming-soon" aria-labelledby="launch-heading">
    <div className="first-print-banner">
      <div className="first-print-banner-copy"><div><span className="label">CRYPTO / SEASON ONE · PHYSICAL CARDS</span><h2 id="launch-heading">First print. Coming soon.</h2></div><p>100 moments of crypto history.<br/>History Worth Holding.</p></div>
      <Image className={styles.bannerArtwork} src="/first-print-workshop-v1.webp" width={2172} height={724} alt="An inventor and a bull inspect a colourful print beside a brass printing press in a lamp-lit workshop." sizes="(max-width:540px) calc(100vw - 48px), (max-width:1600px) 91vw, (max-width:1800px) calc(100vw - 144px), 1656px"/>
    </div>
    <p className="first-print-art-credit">First-print illustration. Final production details to be confirmed.</p>
    <div className="first-print-info">
      <div className="launch-copy">
        <dl className="first-print-numbers"><div><dt>First-run interest target</dt><dd>1,000 <span>packs</span></dd></div><div><dt>Planned lifetime Season One cap</dt><dd>66,666 <span>packs</span></dd></div></dl>
        <p className="first-print-planning-note">A planning target, not current orders. The lifetime cap is not the first batch.</p>
    <div className={styles.rarityBlock}>
        <div className="first-print-rarity-overview" aria-labelledby="first-print-rarity-heading">
          <h3 id="first-print-rarity-heading">{counts.all} card designs</h3>
          <ul className="first-print-rarity-strip">{rarities.map(label => <li key={label}><Link href={'/timeline?layout=grid&rarity=' + label.toLowerCase()} aria-label={'View all ' + counts[label.toLowerCase()] + ' ' + label + ' card designs'}><strong>{counts[label.toLowerCase()]}</strong><span className={'rarity ' + label.toLowerCase()}>{label}</span></Link></li>)}</ul>
          <p className="first-print-count-label">Unique designs, not pack odds.</p>
        </div>
        <details className="first-print-rarity-details"><summary>Print and foil details</summary>
          <p className="first-print-count-note">Design counts are not printed quantities or pack odds. Foil selection and odds are under review.</p>
        </details>
    </div>
      </div>
      <aside className="launch-list" aria-labelledby="launch-list-heading">
        <span className="label">FIRST-PRINT INTEREST · NOW OPEN</span><h3 id="launch-list-heading">Be there for the first print.</h3>
        <p className="first-print-purpose">One email when preorders open. No newsletter.</p>
        <div className="launch-form-preview" aria-describedby="launch-privacy">
          <a className="gold-button" href="https://docs.google.com/forms/d/e/1FAIpQLSfFIPxtdKXZ__3x7PJQbEUJwSH_J0IhPK5h3cGlixnd00sqAw/viewform?usp=header">Register first-print interest <Arrow/></a>
        </div>
        <p className="first-print-no-order">Opens Google Forms. Not an order or reservation. No payment or guaranteed pack.</p>
        <p id="launch-privacy" className="launch-privacy">The form explains how HISTROVE uses your details and asks for your one-off email request. No automatic confirmation email is sent.</p>
      </aside>
    </div>

  </section>;
}
