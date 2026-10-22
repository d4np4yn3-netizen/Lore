import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/078-manifest.json'),c=read('app/cards/content/078.json'),slug='the-ronin-hack';
const master='../cards/crypto/season-01/'+slug+'-master-078/';
assert.equal(m.art.sha256,'0f7c1d557844135330b4e6821e77033fc5b7be4cd04f98bfb5558aa239800545');
for(const a of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+a.path),a.sha256);
for(const a of m.assets){assert.equal(hash('public/'+a.path),a.sha256);const raw=fs.readFileSync('media/'+a.pack).subarray(a.offset,a.offset+a.length);assert.equal(createHash('sha256').update(raw).digest('hex'),a.sha256);}
assert.equal(m.assets.length,8);assert.equal(c.story.length,5);assert.equal(c.eggs.length,4);
assert.equal(read('app/cards/closeups.json')['078'].length,4);
assert.equal(read(master+'approval.json').publication_authorized,true);
const qa=read(master+'card-final-qa.json');assert.equal(qa.art_unchanged,true);for(const qr of Object.values(qa.qr_checks))assert.deepEqual(qr,['https://lore-site-v1.vercel.app/crypto/078/']);
assert.equal(read(master+'card-data.json').context,'FIVE KEYS. ONE BREACH.');assert.equal(read(master+'card-data.json').moment_label,'29 MAR 2022');assert(c.story.join(' ').includes('23 March'));assert.equal(hash(master+'HISTROVE-Crypto-078-Front-Print-v1.png'),'280dd5ec540ac02c7260161c10110e6c9f198b837b48c4e737e1138c31bb047b');
const r=read('../cards/crypto/current-cards.json');assert.equal(r.numbered_published_count,77);assert(!r.cards.some(x=>x.moment_number===58));assert.equal(r.cards.find(x=>x.moment_number===78).publication_approved,true);
assert.equal(r.cards.find(x=>x.moment_number===76).digital_only,true);assert.equal(read('app/cards/print-files.json').cards['076'],undefined);
const indexAssets=read('media/index.json').assets;
for(const asset of m.assets){
  const matches=indexAssets.filter(entry=>entry.path===asset.path);
  assert.equal(matches.length,1,'078 display asset must remain uniquely indexed');
  assert.deepEqual(matches[0],asset,'078 display asset record must remain unchanged');
}
assert.ok(Object.hasOwn(read('app/cards/media.json'),slug),'078 media entry must remain present');
const media=read('app/cards/media.json')[slug];
assert.equal(media.assetOrigin,media.bookAssetOrigin);
// This release gate intentionally fails until an actual uploaded078asset commit is verified.
assert.match(media.assetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/,'078 immutable asset commit must be verified before release');
assert.equal(read('app/cards/print-files.json').cards['078'].assetOrigin,media.assetOrigin);
console.log('PASS:078 exact approved puppet-master art,card/book/8display hashes,copy,QR records,registry,immutable links and preserved digital-only076');
