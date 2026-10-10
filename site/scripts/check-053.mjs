import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/053-manifest.json'),chapter=read('app/cards/content/053.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),index=read('media/index.json'),registry=read('../cards/crypto/current-cards.json'),prior=read('media/pre053-preservation.json'),ctx=read('app/cards/story-context.json');
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'b61779066c394f7470038d917e6e99650e2f03ea26543ea7b8480ae9add2bf2a');
for(const [k,v] of Object.entries(prior.media))assert.deepEqual(media[k],v);
for(const [k,v] of Object.entries(prior.closeups))assert.deepEqual(close[k],v);
for(const [k,v] of Object.entries(prior.context))assert.deepEqual(ctx[k],v);
for(const a of prior.index.assets)assert.deepEqual(index.assets.find(b=>b.path===a.path),a);
for(const old of prior.registry.cards){const c=registry.cards.find(c=>c.id===old.id);assert.equal(createHash('sha256').update(JSON.stringify(c)).digest('hex'),old.sha256);}
assert.deepEqual(registry.cards.filter(c=>c.moment_number).map(c=>c.moment_number).sort((a,b)=>a-b),Array.from({length:53},(_,i)=>i+1));assert.equal(Object.keys(media).length,53);assert.equal(index.assets.length,592);assert.equal(Object.keys(ctx).length,53);assert.equal(Object.values(ctx).reduce((n,c)=>n+c.related.length,0),129);
assert.equal(chapter.story.length,5);assert.equal(chapter.eggs.length,4);assert.equal(chapter.sources.length,1);assert(chapter.story.some(p=>p.includes('three independent node operators')));assert(chapter.sourceNote.includes('fictional'));
const text=fs.readFileSync('../'+m.chapter.path,'utf8');for(const p of chapter.story)assert(text.includes(p));for(const e of chapter.eggs){assert(text.includes(e.title));assert(text.includes(e.text));}
const master='../cards/crypto/season-01/chainlink-mainnet-master-053/';for(const f of read(master+'immutable-package-manifest.json').files)assert.equal(hash(master+f.path),f.sha256);assert.equal(read(master+'card-final-qa.json').svg_embedded_art_exact,true);assert.equal(read(master+'book-qa.json').embedded_art_exact_pixels,true);
const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('CHAINLINK'));assert(svg.includes('THE WORLD, ON-CHAIN.'));assert(svg.includes('translate(0 -80)'));assert(fs.readFileSync('app/crypto/053/page.js','utf8').includes('/cards/chainlink-mainnet'));
console.log('PASS: 053 approved mature-city/beacons art, exact frame/reframe, card/book/source/clues, preserved 52 prior cards, 592 assets, 224 clues, 106 book previews and 129 related links');
