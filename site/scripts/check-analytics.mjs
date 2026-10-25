import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { ANALYTICS_PREFERENCE_KEY, PREFERENCE_MAX_AGE, encodePreference, parsePreference, savePreference, sanitizePageview } from '../app/analytics-policy.mjs';

const now = 1_800_000_000_000;
const origin = 'https://www.histrove.co.uk';
const allowedPaths = new Set(['/', '/timeline', '/shop', '/cards/genesis-block']);
const options = { allowed: true, origin, allowedPaths };

test('only a valid, current, explicitly accepted choice permits analytics', () => {
  assert.equal(parsePreference(encodePreference('accepted', now), now), 'accepted');
  assert.equal(parsePreference(encodePreference('declined', now), now), 'declined');
  for (const invalid of [null, '', '{}', 'true', 'accepted', '{broken', JSON.stringify({ version: 2, choice: 'accepted', savedAt: now }), JSON.stringify({ version: 1, choice: 'maybe', savedAt: now }), JSON.stringify({ version: 1, choice: 'accepted' })]) assert.equal(parsePreference(invalid, now), null);
  assert.equal(parsePreference(encodePreference('accepted', now), now + PREFERENCE_MAX_AGE), null);
  assert.equal(parsePreference(encodePreference('accepted', now + 1), now), null);
  assert.throws(() => encodePreference('maybe'));
});

test('preference storage contains no visitor identifier or profile', () => {
  assert.equal(ANALYTICS_PREFERENCE_KEY, 'histrove.analytics.v1');
  assert.deepEqual(JSON.parse(encodePreference('accepted', now)), { version: 1, choice: 'accepted', savedAt: now });
});

test('failed withdrawal storage never reports success or reload safety', () => {
  let value = encodePreference('accepted', now);
  const storage = { getItem: () => value, setItem() { throw new Error('storage blocked'); }, removeItem() { value = null; } };
  assert.equal(savePreference(storage, 'declined', now), false);
  assert.equal(value, null);
  value = encodePreference('accepted', now);
  storage.removeItem = () => { throw new Error('storage blocked'); };
  assert.equal(savePreference(storage, 'declined', now), false);
  assert.equal(parsePreference(value, now), 'accepted'); // Caller must stay blocked without reloading.
  storage.setItem = (_, next) => { value = next; };
  assert.equal(savePreference(storage, 'declined', now), true);
  assert.equal(parsePreference(value, now), 'declined');
});

test('default, declined, revoked, custom and unknown-page events are blocked', () => {
  const pageview = { type: 'pageview', url: `${origin}/` };
  assert.equal(sanitizePageview(pageview, { ...options, allowed: false }), null);
  for (const event of [undefined, { type: 'event', url: `${origin}/`, payload: { name: 'purchase' } }, { type: 'pageview', url: 'invalid' }, { type: 'pageview', url: 'https://other.example/' }, { type: 'pageview', url: `${origin}/person@example.com` }, { type: 'pageview', url: `${origin}/scan/076?answer=private` }, { type: 'pageview', url: `${origin}/cards/unknown-private-slug` }]) assert.equal(sanitizePageview(event, options), null);
});

test('accepted pageviews remove every query, fragment and unexpected field', () => {
  for (const path of allowedPaths) {
    assert.deepEqual(sanitizePageview({ type: 'pageview', url: `${origin}${path}?email=private%40example.com&moment=genesis-block#private`, payload: { secret: 'no' }, __cdp: 'no' }, options), { type: 'pageview', url: `${origin}${path}` });
  }
});

test('integration mounts only after consent and withdrawal blocks before reload', () => {
  const source = readFileSync(new URL('../app/components/AnalyticsConsent.js', import.meta.url), 'utf8');
  assert.match(source, /ready && choice === 'accepted' \? <Analytics beforeSend=\{beforeSend\}/);
  assert.match(source, /allowed\.current = false;\s+window\.va\?\.\('beforeSend', \(\) => null\)/);
  assert.match(source, /if \(next === 'declined'\) stop\(\)/);
  assert.match(source, /if \(revoking && persisted\.current\) window\.location\.reload\(\)/);
  assert.match(source, /window\.addEventListener\('storage', onStorage\)/);
  assert.match(source, /Accept analytics/);
  assert.match(source, /Decline analytics/);
  assert.doesNotMatch(source, /\b(track|identify|group)\(/);
});
