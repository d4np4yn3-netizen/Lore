import Link from 'next/link';
import { Arrow } from './Icons';

const slots = [
  { count: 4, label: 'Common', className: 'common' },
  { count: 3, label: 'Uncommon', className: 'uncommon' },
  { count: 2, label: 'Rare', className: 'rare' },
  { count: 1, label: 'Premium', className: 'premium' },
];

// Private revision proposal: no final foil eligibility, placement or pull-rate claim.
export default function PackConfiguration({ detailed = false }) {
  return <section className={'pack-config' + (detailed ? ' pack-config-detailed' : '')} id={detailed ? 'pack-details' : 'pack-preview'} aria-labelledby={detailed ? 'pack-details-heading' : 'pack-preview-heading'}>
    <div className="pack-heading"><div><span className="label gold">INSIDE A BOOSTER PACK / CURRENT PLAN</span><h2 id={detailed ? 'pack-details-heading' : 'pack-preview-heading'}>Ten cards.<br/>One premium pull.</h2></div><p>Four Common, three Uncommon, two Rare and one premium card. The premium slot is Epic, Legendary or Mythic.</p></div>
    <ol className="pack-slots" aria-label="Planned contents of each ten-card pack">{slots.map(slot => <li key={slot.label}><strong>{slot.count}</strong><span className={'rarity ' + slot.className}>{slot.label}</span></li>)}</ol>
    <div className="pack-review-note"><h3>The finish is still taking shape.</h3><p>Foil selection and odds are under review. Which designs receive a foil finish, how foils appear in packs and the final rarity distribution will be confirmed before orders open.</p><p>No final foil count or pull rate is promised here. The pack plan remains subject to printer collation and production quantities.</p></div>
    {detailed ? <>
      <section className="pack-faq" aria-labelledby="pack-faq-heading"><span className="label gold">COLLECTING, EXPLAINED</span><h3 id="pack-faq-heading">A few things worth knowing.</h3>
        <details><summary>What do the six rarity tiers mean?</summary><p>Common, Uncommon, Rare, Epic, Legendary and Mythic describe a card’s place in the collection and its intended distribution. Rarity does not rank the historical importance of an event.</p></details>
        <details><summary>How is the 100-card set divided?</summary><p>The set contains 30 Common, 25 Uncommon, 20 Rare, 13 Epic, 8 Legendary and 4 Mythic designs. These are design counts, not manufacturing quantities or pull rates. Final printing and collation determine how many copies of each card are produced.</p></details>
        <details><summary>Which cards will have foil versions?</summary><p>The selection and pack placement are being reviewed. No final number of foil designs or foil odds has been confirmed. A foil finish does not add another historical moment to the 100-design collection.</p></details>
        <details><summary>Does registering interest reserve packs?</summary><p>No. An interest signup would request one email when first-print pre-orders open. It is not an order, payment or reservation, does not guarantee availability and does not subscribe you to a newsletter.</p></details>
        <details><summary>Can I order or register interest now?</summary><p>Orders and email registration are not open yet. Prices, availability and final product details will be confirmed before launch. The signup preview does not collect or store email addresses.</p></details>
      </section>
      <Link className="text-link pack-explore" href="/timeline">Meet the cards in the timeline <Arrow/></Link>
    </> : <Link className="text-link pack-explore" href="/shop#pack-details">Explore the pack details and FAQ <Arrow/></Link>}
  </section>;
}
