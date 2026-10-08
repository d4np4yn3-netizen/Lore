import { SITE_NAME, SITE_ORIGIN, absoluteUrl } from './site-config';
import searchMetadata from './cards/search-metadata.json';

export function cardMetadata(card) {
  const search = searchMetadata[card.slug];
  const title = `${search.title} | ${SITE_NAME}`;
  const description = search.description;
  const url = absoluteUrl(`/cards/${card.slug}`);
  const image = { url: absoluteUrl(card.media.artwork.src), width: card.media.artwork.width, height: card.media.artwork.height, alt: `${card.title}: original HISTROVE illustration` };
  return { title, description, alternates: { canonical: url },
    openGraph: { title, description, url, siteName: SITE_NAME, type: 'article', images: [image] },
    twitter: { card: 'summary_large_image', title, description, images: [{ url: image.url, alt: image.alt }] },
  };
}
export function jsonLd(value) { return JSON.stringify(value).replace(/</g, '\\u003c'); }
const plainText = text => text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*+/g, '');
export const websiteSchema = { '@context': 'https://schema.org', '@type': 'WebSite', '@id': `${SITE_ORIGIN}/#website`, url: absoluteUrl('/'), name: SITE_NAME, alternateName: 'HISTROVE — History Worth Holding', inLanguage: 'en' };
export function cardSchema(card) {
  const metadata = cardMetadata(card);
  const url = metadata.alternates.canonical;
  return { '@context': 'https://schema.org', '@graph': [
    { '@type': 'Article', '@id': `${url}#article`, mainEntityOfPage: url, url,
      headline: metadata.title.replace(` | ${SITE_NAME}`, ''), description: metadata.description,
      image: [absoluteUrl(card.media.artwork.src)], inLanguage: 'en', articleSection: 'Crypto history',
      isPartOf: { '@id': `${SITE_ORIGIN}/#website` },
      about: { '@type': 'Thing', name: `${card.title} (${card.date})` },
      articleBody: card.story.map(plainText).join('\n\n'),
      citation: [...new Set((card.sources || []).map(source => source.url).concat(card.source || []).filter(Boolean))],
    },
    { '@type': 'BreadcrumbList', '@id': `${url}#breadcrumb`, itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'HISTROVE archive', item: absoluteUrl('/') },
      { '@type': 'ListItem', position: 2, name: card.title, item: url },
    ] },
  ] };
}
