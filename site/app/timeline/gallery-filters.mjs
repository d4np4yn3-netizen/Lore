export const rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic'];

export function normalizeRarity(value) {
  const rarity = String(value || '').toLowerCase();
  return rarities.some(label => label.toLowerCase() === rarity) ? rarity : 'all';
}

export function filterCards(cards, { query = '', rarity = 'all' } = {}) {
  const search = query.toLowerCase().trim();
  const selected = normalizeRarity(rarity);
  return cards.filter(card =>
    (selected === 'all' || card.rarity.toLowerCase() === selected) &&
    `${card.title} ${card.date} ${card.subject} ${card.number} ${card.rarity}`.toLowerCase().includes(search)
  );
}

// Counts reflect the text search, but never hide the other rarity choices.
export function rarityCounts(cards, query = '') {
  const matches = filterCards(cards, { query });
  const counts = Object.fromEntries(rarities.map(label => [label.toLowerCase(), 0]));
  for (const card of matches) counts[card.rarity.toLowerCase()]++;
  return { all: matches.length, ...counts };
}

export function readGalleryState(url) {
  const rarity = normalizeRarity(url.searchParams.get('rarity'));
  const query = url.searchParams.get('q') || '';
  const view = url.searchParams.get('layout') === 'grid' || rarity !== 'all' || query.trim() ? 'grid' : 'timeline';
  return { view, query, rarity };
}

export function galleryUrl(currentUrl, { view, query = '', rarity = 'all' }) {
  const url = new URL(currentUrl);
  const selected = normalizeRarity(rarity);
  if (view === 'grid' || selected !== 'all' || query.trim()) url.searchParams.set('layout', 'grid');
  else url.searchParams.delete('layout');
  if (selected === 'all') url.searchParams.delete('rarity');
  else url.searchParams.set('rarity', selected);
  if (query) url.searchParams.set('q', query);
  else url.searchParams.delete('q');
  // Keep the card dialog's moment/view parameters, other links and hash intact.
  return url;
}
