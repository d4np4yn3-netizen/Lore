'use client';
import Image from 'next/image';
import Link from 'next/link';
import { Arrow, Book } from './Icons';

export default function PhysicalCollection({ card, onOpen }) {
  return <section className="physical-collection" id="collection" aria-labelledby="collection-heading">
    <div className="collection-heading"><div><span className="label gold">BEYOND THE SCREEN</span><h2 id="collection-heading">The physical collection.</h2></div><p>Collectible cards and a companion book, taking shape around the archive.</p></div>
    <div className="collection-grid">
      <article className="collection-object booster-object"><div className="collection-stage"><div className="booster-display"><Image src="/collection/histrove-booster-front.webp" width={800} height={1209} alt="HISTROVE Crypto Season One booster pack front design" sizes="(max-width:760px) 55vw, 240px"/></div></div><div className="collection-caption"><span className="label gold">01 / THE BOOSTER PACK</span><h3>Ten cards. More to discover.</h3><p>A 10-card pack from Crypto Season One. Follow each card into its story, artwork and hidden details online.</p><Link className="text-link" href="/shop#booster-packs">Explore the booster pack <Arrow/></Link></div></article>
      <article className="collection-object"><div className="collection-stage collection-book">{card.media.pages.map((asset,i)=><Image key={asset.src} src={asset.src} width={asset.width} height={asset.height} alt={'Pizza Day book spread, page '+(i+1)} sizes="(max-width:760px) 39vw, 280px"/>)}</div><div className="collection-caption"><span className="label gold">02 / THE COMPANION BOOK</span><h3>Keep the whole story.</h3><p>Full-page illustrations, the history behind each moment and a closer look at the details within the artwork.</p><button className="text-button" onClick={e=>onOpen(card,false,e.currentTarget,'book')}>Preview the book pages <Book/></button></div></article>
    </div>
    <p className="collection-note">Coming soon. Product images are previews; final details and availability will be announced when confirmed.</p>
  </section>;
}
