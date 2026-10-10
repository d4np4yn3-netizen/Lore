import Link from 'next/link';
import { Arrow } from './Icons';

const slots = [
  { count: 4, label: 'Common', className: 'common' },
  { count: 3, label: 'Uncommon', className: 'uncommon' },
  { count: 2, label: 'Rare', className: 'rare' },
  { count: 1, label: 'Premium', className: 'premium' },
];
const notice = 'Planned pack configuration and target odds, subject to final printer collation and production quantities; final odds confirmed before sales.';

export default function PackConfiguration({ detailed = false }) {
  return <section className={'pack-config' + (detailed ? ' pack-config-detailed' : '')} id={detailed ? 'pack-details' : 'pack-preview'} aria-labelledby={detailed ? 'pack-details-heading' : 'pack-preview-heading'}>
    <div className="pack-heading"><div><span className="label gold">INSIDE A BOOSTER PACK</span><h2 id={detailed ? 'pack-details-heading' : 'pack-preview-heading'}>Ten cards.<br/>One premium pull.</h2></div><p>Four Common, three Uncommon, two Rare and one premium card. The premium slot is Epic, Legendary or Mythic.</p></div>
    <ol className="pack-slots" aria-label="Planned contents of each ten-card pack">{slots.map(slot => <li key={slot.label}><strong>{slot.count}</strong><span className={'rarity ' + slot.className}>{slot.label}</span></li>)}</ol>
    <div className="pack-targets-heading"><span className="label gold">TARGET ODDS PER PACK</span><span>Each figure describes a pack, not an individual card</span></div>
    <dl className="pack-highlights"><div><dt>Any foil premium card</dt><dd>1 in 4 <small>packs</small></dd></div><div><dt>Any Mythic, either finish</dt><dd>1 in 10 <small>packs</small></dd></div><div><dt>Any foil Mythic</dt><dd>1 in 40 <small>packs</small></dd></div></dl>
    <p className="pack-finish-note">Foil replaces the regular finish of the premium card. Every pack still contains ten cards.</p>
    <p className="pack-production-note">{notice}</p>
    {detailed ? <>
      <div className="pack-detail-grid">
        <div><h3>The premium slot</h3><p>Target distribution across packs:</p><ul className="pack-distribution"><li><span className="rarity epic">Epic</span><strong>60% of packs</strong></li><li><span className="rarity legendary">Legendary</span><strong>30% of packs</strong></li><li><span className="rarity mythic">Mythic</span><strong>10% of packs</strong></li></ul><p className="pack-small">The premium card’s finish is selected independently of its rarity: a target 25% of packs contain a foil premium card and 75% contain a regular premium card. The rarity mix is the same for both finishes.</p></div>
        <div><h3>Looking for one Mythic?</h3><p>With four planned Mythic designs, assuming equal distribution within the tier and each finish:</p><dl className="pack-specific"><div><dt>A particular Mythic, either finish</dt><dd>1 in 40 packs</dd></div><div><dt>A particular foil Mythic</dt><dd>1 in 160 packs</dd></div></dl><p className="pack-small">These are nominal targets across the print run. Production quantities and rounding may make individual design or finish counts unequal. Buying this many packs does not guarantee a particular card.</p></div>
      </div>
      <section className="pack-faq" aria-labelledby="pack-faq-heading"><span className="label gold">COLLECTING, EXPLAINED</span><h3 id="pack-faq-heading">A few things worth knowing.</h3>
        <details><summary>What do the six rarity tiers mean?</summary><p>Common, Uncommon, Rare, Epic, Legendary and Mythic describe a card’s place in the collection and its intended distribution. Rarity does not rank the historical importance of an event.</p></details>
        <details><summary>How is the 100-card set divided?</summary><p>The planned set contains 30 Common, 25 Uncommon, 20 Rare, 13 Epic, 8 Legendary and 4 Mythic designs. These are design counts, not manufacturing quantities or pull rates. Final printing and collation determine how many copies of each card are produced.</p></details>
        <details><summary>Are foil cards extra cards?</summary><p>No. A foil card takes the place of the regular-finish card in the premium slot. It is an Epic, Legendary or Mythic card, and the pack still contains ten cards.</p></details>
        <details><summary>Can I add the odds together?</summary><p>No. The categories overlap: a foil Mythic counts as both a foil card and a Mythic card. “Any foil Mythic” means any of the four planned Mythic designs; “a particular foil Mythic” means one specified design.</p></details>
        <details><summary>Are these guaranteed pull rates?</summary><p>These are planned targets, not a guarantee for an individual pack or purchase. Final odds will be confirmed before sales after printer collation and production quantities are settled. No number of packs guarantees completing the set.</p></details>
        <details><summary>Can I order or join the launch list?</summary><p>Orders and email registration are not open yet. Prices, availability and final product details will be confirmed before launch. The signup preview does not collect or store email addresses.</p></details>
      </section>
      <Link className="text-link pack-explore" href="/timeline">Meet the cards in the timeline <Arrow/></Link>
    </> : <Link className="text-link pack-explore" href="/shop#pack-details">Explore the pack details and FAQ <Arrow/></Link>}
  </section>;
}
