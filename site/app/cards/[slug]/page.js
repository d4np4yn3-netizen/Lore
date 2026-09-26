import Image from 'next/image';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { cards, getCard } from '../data';

const GH = 'https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/main/';

// The editorial master is the book Markdown. Keep its emphasis and source links on the web.
function editorial(text) {
  return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))/g).map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>;
    if (part.startsWith('*') && part.endsWith('*')) return <em key={index}>{part.slice(1, -1)}</em>;
    const link = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (link) return <a key={index} href={link[2]} target="_blank" rel="noopener noreferrer">{link[1]}</a>;
    return part;
  });
}

export function generateStaticParams() {
  return cards.map(card => ({ slug: card.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const card = getCard(slug);
  return { title: card ? `${card.title} — LORE` : 'LORE' };
}

export default async function CardPage({ params }) {
  const { slug } = await params;
  const card = getCard(slug);
  if (!card) notFound();
  const index = cards.indexOf(card);
  const next = cards.length > 1 ? cards[(index + 1) % cards.length] : null;

  return <main className="detail">
    <nav><Link href="/"><Image src={GH + 'brand/assets/png/lore_logo_primary_gold_white.png'} width={180} height={85} alt="LORE" /></Link><Link href="/#season">← COLLECTION</Link></nav>
    <header className="detailHero">
      <div className="detailCard"><Image src={GH + card.image} width={540} height={756} alt={card.title} /></div>
      <div className="detailCopy">
        <div className={'rarity ' + card.rarity.toLowerCase()}>{card.rarity} · CRYPTO SEASON ONE {card.number && '· ' + card.number}</div>
        <h1>{card.title}</h1>
        <div className="date">{card.date} · {card.subject}</div>
        <blockquote>“{card.phrase}”</blockquote>
        {card.story.map((paragraph, i) => <p key={i}>{editorial(paragraph)}</p>)}
        <div className="scroll">SCROLL TO DECODE THE ART ↓</div>
      </div>
    </header>
    <section className="decode">
      <span>HIDDEN IN THE ART</span><h2>THE EASTER<br /><em>EGGS.</em></h2>
      <div className="eggGrid">{card.eggs.map((egg, i) => <article key={egg.title}>
        <b>{String(i + 1).padStart(2, '0')}</b><h3>{egg.title}</h3><p>{editorial(egg.text)}</p>
      </article>)}</div>
      <div className="sourceNote"><h3>SOURCE &amp; ART NOTE</h3><p>{editorial(card.sourceNote)}</p></div>
    </section>
    <section className="next"><span>{next ? 'NEXT MOMENT' : 'MORE MOMENTS TO COME'}</span><Link href={next ? '/cards/' + next.slug : '/#season'}>{next ? next.title : 'BACK TO COLLECTION'} →</Link></section>
  </main>;
}
