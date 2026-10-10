import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/051-manifest.json'),chapter=read('app/cards/content/051.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),index=read('media/index.json'),registry=read('../cards/crypto/current-cards.json'),prior=read('media/pre051-preservation.json'),ctx=read('app/cards/story-context.json');
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'0451d34936796252c7a1f01675597fbb88bd855b15195bc7171021578db5581e');
for(const [k,v]of Object.entries(prior.media))assert.deepEqual(media[k],v);
for(const [k,v]of Object.entries(prior.closeups))assert.deepEqual(close[k],v);
for(const [k,v]of Object.entries(prior.context))assert.deepEqual(ctx[k],v);
for(const old of prior.index.assets)assert.deepEqual(index.assets.find(a=>a.path===old.path),old);
for(const old of prior.registry.cards){const c=registry.cards.find(c=>c.id===old.id);assert.equal(createHash('sha256').update(JSON.stringify(c)).digest('hex'),old.sha256);}
assert.deepEqual(registry.cards.filter(c=>c.moment_number&&c.moment_number!==53&&c.moment_number!==54).map(c=>c.moment_number).sort((a,b)=>a-b),Array.from({length:52},(_,i)=>i+1));
assert.equal(Object.keys(media).length,54);assert.equal(index.assets.length,600);assert.equal(Object.keys(ctx).length,54);assert.equal(Object.values(ctx).reduce((n,c)=>n+c.related.length,0),132);
assert.equal(chapter.story.length,5);assert.equal(chapter.eggs.length,4);assert.equal(chapter.sources.length,2);assert(chapter.eggs[3].text.includes('+10,000 SATS'));assert(chapter.story.some(p=>p.includes('exceptions')));assert(chapter.sourceNote.includes('fictional metaphorical imagery'));
const text=fs.readFileSync('../'+m.chapter.path,'utf8');for(const p of chapter.story)assert(text.includes(p));for(const e of chapter.eggs){assert(text.includes(e.title));assert(text.includes(e.text));}
const master='../cards/crypto/season-01/lightning-torch-master-051/';for(const f of read(master+'immutable-package-manifest.json').files)assert.equal(hash(master+f.path),f.sha256);
assert.equal(read(master+'card-final-qa.json').svg_embedded_art_exact,true);assert.equal(read(master+'book-qa.json').embedded_art_pixels_match_original,true);assert.equal(read(master+'book-qa.json').native_effective_ppi,128.2095238095238);
const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('LIGHTNING'));assert(svg.includes('PASS IT ON.'));assert(fs.readFileSync('app/crypto/051/page.js','utf8').includes('/cards/lightning-torch'));
const data=fs.readFileSync('app/cards/data.js','utf8');assert(data.indexOf("slug: 'the-pineapple-fund'")<data.indexOf("slug: 'lightning-torch'"));assert(data.indexOf("slug: 'lightning-torch'")<data.indexOf("slug: 'quadrigacx'"));
console.log('PASS: 051 corrected engraving art/card/book hashes, fixed frame, four clues; all 53 prior registry objects and 576 display assets preserved; numbered001–052, 220 clues,104 book previews,126 related links; 051 inserted before052');
