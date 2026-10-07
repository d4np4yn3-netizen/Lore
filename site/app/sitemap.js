import { archiveCards } from './cards/experience';
import { absoluteUrl } from './site-config';
// Only preferred editorial routes. Existing printed /crypto/ links keep redirecting.
// Publication dates are not inferred from the dates of historical events.
export default function sitemap() {
  return ['/', ...archiveCards.map(card => `/cards/${card.slug}`)].map(path => ({ url: absoluteUrl(path) }));
}
