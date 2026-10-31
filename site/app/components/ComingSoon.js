import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
import { archiveCards, titleCase } from '../cards/experience';
import { rarities, rarityCounts } from '../timeline/gallery-filters.mjs';

const bannerArt = [
  ['birth-of-hodl', '021 / BIRTH OF HODL'],
  ['cryptopunks', '038 / CRYPTOPUNKS'],
  ['much-wow', '020 / BIRTH OF DOGE'],
  ['cryptokitties', '046 / CRYPTOKITTIES'],
].map(([slug, caption]) => ({ card: archiveCards.find(card => card.slug === slug), caption }));
// Private art-led proposal. No collection endpoint, submission handler or new artwork.
export default function ComingSoon() {
  const counts = rarityCounts(archiveCards);
  return <section className="coming-soon" id="coming-soon" aria-labelledby="launch-heading">
    <div className="first-print-banner">
      <div className="first-print-banner-copy"><div><span className="label">CRYPTO / SEASON ONE · PHYSICAL CARDS</span><h2 id="launch-heading">First print. Coming soon.</h2></div><p>100 moments of crypto history.<br/>History Worth Holding.</p></div>
      <div className="first-print-panorama">{bannerArt.map(({ card, caption }) => <figure key={card.slug}><Image src={card.media.artwork.src} width={card.media.artwork.width} height={card.media.artwork.height} alt={titleCase(card.title) + ' — original Season One illustration, without the card frame.'} sizes="(max-width:760px) 44vw, 22vw"/><figcaption>{caption}</figcaption></figure>)}</div>
    </div>
    <p className="first-print-art-credit">Original artwork from Crypto Season One.</p>
    <div className="first-print-info">
      <div className="launch-copy">
        <dl className="first-print-numbers"><div><dt>First-run interest target</dt><dd>1,000 <span>packs</span></dd></div><div><dt>Planned lifetime Season One cap</dt><dd>66,666 <span>packs</span></dd></div></dl>
        <p className="first-print-planning-note">A planning target, not current orders. The lifetime cap is not the first batch.</p>
        <div className="first-print-rarity-overview" aria-labelledby="first-print-rarity-heading">
          <h3 id="first-print-rarity-heading">{counts.all} card designs</h3>
          <ul className="first-print-rarity-strip">{rarities.map(label => <li key={label}><Link href={'/timeline?layout=grid&rarity=' + label.toLowerCase()} aria-label={'View all ' + counts[label.toLowerCase()] + ' ' + label + ' card designs'}><strong>{counts[label.toLowerCase()]}</strong><span className={'rarity ' + label.toLowerCase()}>{label}</span></Link></li>)}</ul>
          <p className="first-print-count-label">Unique designs, not pack odds.</p>
        </div>
        <details className="first-print-rarity-details"><summary>Print and foil details</summary>
          <p className="first-print-count-note">Design counts are not printed quantities or pack odds. Foil selection and odds are under review.</p>
        </details>
      </div>
      <aside className="launch-list" aria-labelledby="launch-list-heading">
        <span className="label">FIRST-PRINT INTEREST · NOT OPEN YET</span><h3 id="launch-list-heading">Be there for the first print.</h3>
        <p className="first-print-purpose">One email when preorders open. No newsletter.</p>
        <div className="launch-form-preview" aria-describedby="launch-privacy">
          <label htmlFor="launch-email">Email address</label><input id="launch-email" type="email" placeholder="you@example.com" autoComplete="off" disabled aria-describedby="launch-privacy"/>
          <label htmlFor="launch-quantity">How many packs might you want? <small>(optional)</small></label><input id="launch-quantity" type="number" min="1" step="1" placeholder="e.g. 2" disabled aria-describedby="launch-quantity-note"/>
          <p id="launch-quantity-note" className="first-print-quantity-note">Non-binding estimate. You can change your mind.</p>
          <button className="gold-button" type="button" disabled>Notify me when preorders open <Arrow/></button>
        </div>
        <p className="first-print-no-order">Interest only — not an order, payment or reservation. No guaranteed pack.</p>
        <p id="launch-privacy" className="launch-privacy">Signup remains closed; no details are collected.</p>
      </aside>
    </div>
  </section>;
}
