import Image from 'next/image';
import Link from 'next/link';
import { Arrow } from './Icons';
import { archiveCards, titleCase } from '../cards/experience';
import { rarities, rarityCounts } from '../timeline/gallery-filters.mjs';

const riverCards = ['the-first-halving', 'the-fourth-halving'].map(slug => archiveCards.find(card => card.slug === slug));
const artCards = ['the-bybit-heist', 'three-arrows-falls', 'black-thursday'].map(slug => archiveCards.find(card => card.slug === slug));
// Private art-led proposal. No collection endpoint, submission handler or new artwork.
export default function ComingSoon() {
  const counts = rarityCounts(archiveCards);
  return <section className="coming-soon" id="coming-soon" aria-labelledby="launch-heading">
    <div className="first-print-banner">
      <div className="first-print-panorama">{riverCards.map(card => <div key={card.slug}><Image src={card.media.artwork.src} width={card.media.artwork.width} height={card.media.artwork.height} alt={card.slug === 'the-first-halving' ? 'The First Halving artwork: a traveller beside a golden river flowing through the mountains.' : 'The Fourth Halving artwork: the traveller looks across a mountain valley and a smaller golden stream.'} sizes="(max-width:760px) 50vw, 44vw"/></div>)}</div>
      <div className="first-print-banner-copy"><span className="label">CRYPTO / SEASON ONE · PHYSICAL CARDS</span><h2 id="launch-heading">First print.<br/>Coming soon.</h2></div>
    </div>
    <p className="first-print-art-credit">The Golden River · Artwork from cards 015 &amp; 093</p>
    <div className="first-print-info">
      <div className="launch-copy">
        <span className="label gold">THE FIRST PRINT / THE WHOLE SEASON</span>
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
        <span className="label">FIRST-PRINT INTEREST · NOT OPEN YET</span><h3 id="launch-list-heading">Email registration opens soon</h3>
        <p className="first-print-purpose">One email when first-print pre-orders open. No newsletter.</p>
        <div className="launch-form-preview" aria-describedby="launch-privacy">
          <label htmlFor="launch-email">Email address</label><input id="launch-email" type="email" placeholder="you@example.com" autoComplete="off" disabled aria-describedby="launch-privacy"/>
          <label htmlFor="launch-quantity">How many packs might you want?</label><input id="launch-quantity" type="number" min="1" step="1" placeholder="e.g. 2" disabled aria-describedby="launch-quantity-note"/>
          <p id="launch-quantity-note" className="first-print-quantity-note">Non-binding estimate. You can change your mind.</p>
          <button className="gold-button" type="button" disabled>Notify me when pre-orders open <Arrow/></button>
        </div>
        <p className="first-print-no-order">Interest only — not an order, payment or reservation. No guaranteed pack.</p>
        <p id="launch-privacy" className="launch-privacy">This preview does not collect or store email addresses or quantities. Privacy and response handling must be ready before signup opens.</p>
      </aside>
    </div>
    <div className="first-print-art-showcase" aria-labelledby="first-print-art-heading">
      <div className="first-print-art-heading"><div><span className="label gold">A CLOSER LOOK</span><h3 id="first-print-art-heading">The history. The art.</h3></div><Link className="text-link" href="/timeline?layout=grid">Explore all {counts.all} cards <Arrow/></Link></div>
      <ul className="first-print-art-strip" aria-label="Three Season One artworks">{artCards.map(card => <li key={card.slug}><Link href={'/cards/' + card.slug} aria-label={'Explore ' + titleCase(card.title)}><Image src={card.media.artwork.src} width={card.media.artwork.width} height={card.media.artwork.height} alt={titleCase(card.title) + ' — original Season One illustration, without the card frame.'} sizes="(max-width:760px) 74vw, 29vw"/><span><small>{card.id} / SEASON ONE</small><strong>{titleCase(card.title)}</strong><Arrow/></span></Link></li>)}</ul>
      <p className="first-print-swipe-hint">Swipe to explore the artwork, or select a moment to read its story.</p>
    </div>
  </section>;
}
