import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const h=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p));
const m=read('media/045-manifest.json'),data=read('app/cards/content/045.json'),media=read('app/cards/media.json').bitconnect;
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(h('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(h('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'06a19f961a37259c8c3d1bf194cf4b8711a920e92e99a12619092428f939a95b');
assert.equal(data.story.length,5);assert.equal(data.eggs.length,4);assert.equal(media.pages.length,2);
assert.equal(media.originalBook,m.book.path);assert.equal(media.originalArt,m.art.path);
assert.equal(m.qr,'https://lore-site-v1.vercel.app/crypto/045/');
assert(fs.readFileSync('app/crypto/045/page.js','utf8').includes('/cards/bitconnect'));
const chapter=fs.readFileSync('../'+m.chapter.path,'utf8');
for(const p of data.story)assert(chapter.includes(p));
for(const e of data.eggs){assert(chapter.includes(e.title));assert(chapter.includes(e.text));}
assert(chapter.includes(data.sourceNote));
const prior=read('media/pre045-preservation.json'),allMedia=read('app/cards/media.json'),allCloseups=read('app/cards/closeups.json'),allIndex=read('media/index.json');
for(const [slug,record] of Object.entries(prior.media))assert.deepEqual(allMedia[slug],record);
for(const [id,record] of Object.entries(prior.closeups))assert.deepEqual(allCloseups[id],record);
for(const record of prior.index.assets)assert.deepEqual(allIndex.assets.find(a=>a.path===record.path),record);
assert.equal(allIndex.assets.filter(a=>!['display-046.bin','display-047.bin','display-048.bin','display-049.bin','display-050.bin'].includes(a.pack)).length,prior.index.assets.length+8);
const registry=read('../cards/crypto/current-cards.json'),r=registry.cards.find(c=>c.id==='crypto-s01-bitconnect');
for(const old of prior.registry.cards){const current=registry.cards.find(c=>c.id===old.id);if(old.id==='crypto-s01-bitconnect')assert.deepEqual(current.historical_versions.at(-1),old);else assert.deepEqual(current,old);}
assert.equal(registry.cards.filter(c=>![46,47,48,49,50].includes(c.moment_number)).length,prior.registry.cards.length);assert.equal(r.moment_number,45);assert.equal(r.title_line_1,'BITCONNECT');assert.equal(r.title_line_2,'');assert.equal(r.single_line_title,true);assert.equal(r.qr_mode,'live');assert.equal(r.qr_url,m.qr);assert.equal(registry.cards.filter(c=>c.moment_number===45).length,1);
assert.equal(r.artwork_file.sha256,m.art.sha256);assert.equal(r.print_ready.pdf.sha256,m.print.pdf.sha256);assert.equal(r.print_release,false);
console.log('PASS: 045 exact art/print/book/chapter, eight display hashes, five shared paragraphs, four actual-art clues, stable QR, all 44 prior card records/520 assets and complete legacy BitConnect preserved');
