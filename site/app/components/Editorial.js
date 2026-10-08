import { ExternalLink } from './Icons';
// Render the shared book manuscript without injecting HTML.
export function Editorial({ text }) {
  return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[^\]]+\]\([^)]+\))/g).map((part,index) => {
    if(part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2,-2)}</strong>;
    if(part.startsWith('*') && part.endsWith('*')) return <em key={index}>{part.slice(1,-1)}</em>;
    const link=part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if(link && /^https?:\/\//.test(link[2])) return <a key={index} href={link[2]} target="_blank" rel="noopener noreferrer">{link[1]} <ExternalLink/></a>;
    return part;
  });
}
