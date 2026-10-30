import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';

const read = path => fs.readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const page = read('.next/server/app/season-two.html');
const home = read('.next/server/app/index.html');
const main = page.match(/<main\b[^>]*>.*?<\/main>/s)[0];
const anchors = html => [...html.matchAll(/<a\b([^>]*)>/g)].map(match => Object.fromEntries([...match[1].matchAll(/([\w:-]+)="([^"]*)"/g)].map(m => [m[1], m[2]])));

test('Season Two describes the 50-card plan and truthful private editorial process', () => {
  assert(main.includes('50 new cards.'));
  assert(main.includes('When submissions open'));
  assert(main.includes('private editorial review'));
  assert(main.includes('final selection remains editorial'));
  assert(main.includes('not a binding vote or a competition'));
  assert(main.includes('will not sign you up for marketing emails'));
});

test('unconnected suggestion preview cannot accept, transmit or pretend to save data', () => {
  assert(main.includes('Preview only · Suggestions are not open yet.'));
  assert(/<fieldset\b[^>]*disabled=""/.test(main));
  assert.equal((main.match(/<input\b/g) || []).length, 3);
  assert.equal((main.match(/<textarea\b/g) || []).length, 1);
  assert(/<button[^>]*type="button"[^>]*disabled=""/.test(main));
  assert(!/<form\b|\baction=|type="email"|name="email"/.test(main));
  const source = read('app/season-two/page.js');
  assert.doesNotMatch(source, /\bfetch\s*\(|localStorage|sessionStorage|sendBeacon|onSubmit|onClick|mailto:/);
  assert(source.includes('does not send, collect or save suggestions'));
});

test('preview prompts have explicit labels, accessible status and no private identity fields', () => {
  for (const field of ['moment', 'date', 'reason', 'source']) {
    assert(main.includes(`for="suggestion-${field}"`));
    assert(main.includes(`id="suggestion-${field}"`));
  }
  assert(main.includes('aria-describedby="suggestion-status suggestion-privacy"'));
  assert(main.includes('contact details, private keys, wallet details or other personal information'));
  assert(!main.includes('type="file"') && !main.includes('type="password"'));
});

test('draft privacy route explains verified storage and leaves unresolved choices visibly gated', () => {
  const privacy = read('.next/server/app/season-two/privacy.html');
  assert(main.includes('href="/season-two/privacy"'));
  assert(main.includes('Private response storage has been set up and tested.'));
  for (const phrase of ['Draft for review', 'Public suggestions remain closed.', 'not a final live privacy notice', '12 months', 'Google Forms', 'linked Google Sheet', 'not automatic deletion', 'not a promise of complete anonymity', 'Legitimate interests is proposed', 'It has not yet been adopted']) assert(privacy.includes(phrase), phrase);
  assert(privacy.includes('name="robots" content="noindex, nofollow"'));
  assert(privacy.includes('href="mailto:hello@histrove.co.uk"'));
  assert(!/Dan Payne|Daniel Payne|1i_HeTd2|14nvZ0QMrj|<form\b|<iframe\b/.test(privacy));
  assert(!read('.next/server/app/sitemap.xml.body').includes('/season-two/privacy'));
});

test('global navigation and contact destination are correct without changing the active collection', () => {
  const active = anchors(page).find(a => a.href === '/season-two');
  assert.equal(active['aria-current'], 'page');
  for (const html of [page, home, read('.next/server/app/timeline.html'), read('.next/server/app/shop.html')]) {
    assert(anchors(html).some(a => a.href === '/season-two'));
    assert(anchors(html).some(a => a.href === 'mailto:hello@histrove.co.uk'));
    assert(html.includes('Analytics preferences'));
  }
  assert(home.includes('CRYPTO / SEASON ONE'));
  assert(read('.next/server/app/shop.html').includes('Purchases aren’t open yet'));
});

test('homepage invitation stays secondary to Season One products and timeline', () => {
  const position = home.indexOf('id="season-two-teaser-title"');
  assert(position > home.indexOf('id="collection"'));
  assert(position > home.indexOf('id="teaser-title"'));
  assert(position < home.indexOf('id="coming-soon"'));
  assert(home.includes('Email registration opens soon'));
});

test('canonical metadata and sitemap include the new page without losing existing pages', () => {
  assert(page.includes('href="https://www.histrove.co.uk/season-two"'));
  assert(page.includes('The suggestion form is not open yet.'));
  const urls = [...read('.next/server/app/sitemap.xml.body').matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1]);
  const cards = Object.keys(JSON.parse(read('app/cards/media.json')));
  assert.equal(urls.length, cards.length + 4);
  assert.equal(new Set(urls).size, urls.length);
  for (const path of ['/', '/shop', '/timeline', '/season-two', ...cards.map(slug => `/cards/${slug}`)]) assert(urls.includes('https://www.histrove.co.uk' + path), path);
});
