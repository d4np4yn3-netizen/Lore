import Timeline from './Timeline';
import { absoluteUrl } from '../site-config';
export const metadata = {
 title: 'Crypto History Timeline & Card Archive | HISTROVE',
 description: 'Explore every published HISTROVE crypto-history card, from the ideas before Bitcoin to the moments that shaped a culture. Search by event, year, subject or rarity.',
 alternates: { canonical: absoluteUrl('/timeline') },
 openGraph: { title: 'Crypto History Timeline | HISTROVE', description: 'Explore the full illustrated crypto-history timeline.', url: absoluteUrl('/timeline'), type: 'website' },
};
export default function TimelinePage() { return <Timeline/>; }
