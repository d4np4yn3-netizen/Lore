import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { rarities, normalizeRarity, filterCards, rarityCounts, readGalleryState, galleryUrl } from '../app/timeline/gallery-filters.mjs';

// Load the real catalogue without changing its JSON imports or metadata.
const dataUrl = new URL('../app/cards/data.js', import.meta.url);
const source = fs.readFileSync(dataUrl, 'utf8').replace(/import (\w+) from '(\.\/content\/\d+\.json)';/g,
  (_, name, path) => `const ${name} = ${fs.readFileSync(new URL(path, dataUrl), 'utf8')};`);
const { cards } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const ids = list => list.map(card => card.number);

test('all six rarities follow the brand order and reset returns the complete catalogue', () => {
  assert.deepEqual(rarities, ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythic']);
  assert.deepEqual(ids(filterCards(cards)), ids(cards));
  assert.equal(normalizeRarity('MYTHIC'), 'mythic');
  assert.equal(normalizeRarity('unknown'), 'all');
  assert.deepEqual(ids(filterCards(cards, { rarity: 'unknown' })), ids(cards));
});

test('each rarity shows every matching card in original order, without mutating data', () => {
  const before = JSON.stringify(cards);
  const counts = rarityCounts(cards);
  assert.equal(counts.all, cards.length);
  assert.equal(rarities.reduce((sum, rarity) => sum + counts[rarity.toLowerCase()], 0), cards.length);
  for (const rarity of rarities) {
    const expected = cards.filter(card => card.rarity.toLowerCase() === rarity.toLowerCase());
    assert(expected.length > 0, rarity);
    assert.deepEqual(ids(filterCards(cards, { rarity })), ids(expected));
    assert.equal(counts[rarity.toLowerCase()], expected.length);
    assert.deepEqual(ids(filterCards(cards, { rarity })), ids(filterCards(cards, { rarity })));
  }
  assert.equal(JSON.stringify(cards), before);
});

test('text search and rarity intersect; counts and empty results remain accurate', () => {
  for (const query of ['bitcoin', '  2017  ', cards[0].number, 'no-such-card-xyz']) {
    const textMatches = filterCards(cards, { query });
    const counts = rarityCounts(cards, query);
    assert.equal(counts.all, textMatches.length);
    for (const rarity of rarities) {
      const matches = filterCards(cards, { query, rarity });
      assert.deepEqual(ids(matches), ids(textMatches.filter(card => card.rarity.toLowerCase() === rarity.toLowerCase())));
      assert.equal(counts[rarity.toLowerCase()], matches.length);
    }
  }
  assert.equal(filterCards(cards, { query: 'no-such-card-xyz', rarity: 'epic' }).length, 0);
});

test('rarity URLs survive refresh/back, preserve dialog links, and repeated selection is idempotent', () => {
  const original = new URL('https://www.histrove.co.uk/timeline?moment=genesis-block&view=clues&return=shop#archive');
  for (const rarity of rarities.map(label => label.toLowerCase())) {
    const state = { view: 'grid', rarity, query: 'Bitcoin & 2017' };
    const selected = galleryUrl(original, state);
    assert.deepEqual(readGalleryState(selected), state);
    assert.equal(galleryUrl(selected, state).href, selected.href);
    assert.equal(selected.searchParams.get('moment'), 'genesis-block');
    assert.equal(selected.searchParams.get('view'), 'clues');
    assert.equal(selected.searchParams.get('return'), 'shop');
    assert.equal(selected.hash, '#archive');
    const reset = galleryUrl(selected, { view: 'grid', rarity: 'all', query: '' });
    assert.deepEqual(readGalleryState(reset), { view: 'grid', rarity: 'all', query: '' });
    assert.equal(reset.searchParams.has('rarity'), false);
    assert.equal(reset.searchParams.has('q'), false);
    assert.deepEqual(readGalleryState(selected), state); // History restores earlier URL.
    assert.equal(galleryUrl(reset, { view: 'timeline' }).href, original.href);
  }
  assert.deepEqual(readGalleryState(new URL('https://www.histrove.co.uk/timeline?rarity=MYTHIC')), { view: 'grid', query: '', rarity: 'mythic' });
  assert.deepEqual(readGalleryState(new URL('https://www.histrove.co.uk/timeline?rarity=invalid')), { view: 'timeline', query: '', rarity: 'all' });
});

test('gallery uses a labeled native control, announces counts and renders the full filtered list', () => {
  const timeline = fs.readFileSync(new URL('../app/timeline/Timeline.js', import.meta.url), 'utf8');
  assert.match(timeline, /<label className="rarity-filter"><span>Rarity<\/span><select/);
  assert.match(timeline, /<option value="all">All rarities/);
  assert.match(timeline, /role="status" aria-live="polite" aria-atomic="true"/);
  assert.match(timeline, /filtered\.map\(c=><Moment/);
  assert.doesNotMatch(timeline, /filtered\.slice/);
  assert.match(timeline, /setGallery\(readGalleryState\(url\)\)/);
  assert.match(timeline, /window\.addEventListener\('popstate',sync\)/);
  assert.match(timeline, /if\(url.href!==window.location.href\)/);
});

console.log('Published catalogue counts:', rarityCounts(cards));
