import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/077-manifest.json'),c=read('app/cards/content/077.json'),slug='crypto-for-ukraine';
const master='../cards/crypto/season-01/'+slug+'-master-077/';
assert.equal(m.art.sha256,'6e1680b3eb2450adff2c84c8f05723b098145ee413937fbc972b1905bc7304ec');
for(const a of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+a.path),a.sha256);
for(const a of m.assets){assert.equal(hash('public/'+a.path),a.sha256);const raw=fs.readFileSync('media/'+a.pack).subarray(a.offset,a.offset+a.length);assert.equal(createHash('sha256').update(raw).digest('hex'),a.sha256);}
assert.equal(m.assets.length,8);assert.equal(c.story.length,5);assert.equal(c.eggs.length,4);
assert.equal(read('app/cards/closeups.json')['077'].length,4);
assert.equal(read(master+'approval.json').publication_authorized,true);
const qa=read(master+'card-final-qa.json');assert.equal(qa.art_unchanged,true);for(const qr of Object.values(qa.qr_checks))assert.deepEqual(qr,['https://lore-site-v1.vercel.app/crypto/077/']);
assert.equal(read(master+'card-data.json').context,'IN SUPPORT OF UKRAINE');assert.equal(read(master+'card-data.json').moment_label,'03 MAR 2022');assert(c.story.join(' ').includes('vast majority'));
const r=read('../cards/crypto/current-cards.json');assert.equal(r.numbered_published_count,77);assert(!r.cards.some(x=>x.moment_number===58));assert.equal(r.cards.find(x=>x.moment_number===77).publication_approved,true);
assert.equal(r.cards.find(x=>x.moment_number===76).digital_only,true);assert.equal(read('app/cards/print-files.json').cards['076'],undefined);
assert.equal(Object.keys(read('app/cards/media.json')).length,77);assert.equal(read('media/index.json').assets.length,787);
const media=read('app/cards/media.json')[slug];
assert.equal(media.assetOrigin,media.bookAssetOrigin);
// This release gate intentionally fails until an actual uploaded077asset commit is verified.
assert.match(media.assetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/,'077 immutable asset commit must be verified before release');
assert.equal(read('app/cards/print-files.json').cards['077'].assetOrigin,media.assetOrigin);
console.log('PASS:077 exact corrected-desk art,card/book/8display hashes,copy,QR records,registry,immutable links and preserved digital-only076');
