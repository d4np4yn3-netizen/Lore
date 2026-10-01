import { notFound } from 'next/navigation';
import { archiveCards, titleCase } from '../experience';
import { Header, Footer } from '../../components/SiteChrome';
import { ReadingRoom } from '../../components/ReadingRoom';
export function generateStaticParams(){return archiveCards.map(card=>({slug:card.slug}));}
export async function generateMetadata({params}){const {slug}=await params;const card=archiveCards.find(c=>c.slug===slug);return {title:card?`${titleCase(card.title)} — LORE Crypto`:'LORE',description:card?`${card.date}. Discover ${titleCase(card.title)}, the original artwork, hidden details and companion book pages.`:undefined};}
export default async function CardPage({params}){const {slug}=await params;const index=archiveCards.findIndex(c=>c.slug===slug);if(index<0)notFound();return <div id="top"><a className="skip-link" href="#main">Skip to story</a><Header detail/><main id="main"><ReadingRoom card={archiveCards[index]} standalone previous={archiveCards[index-1]} next={archiveCards[index+1]}/></main><Footer/></div>}
