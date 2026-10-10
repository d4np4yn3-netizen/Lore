import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/055-manifest.json'),chapter=read('app/cards/content/055.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),index=read('media/index.json'),registry=read('../cards/crypto/current-cards.json'),prior=read('media/pre055-preservation.json'),ctx=read('app/cards/story-context.json');
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'f694c4433f2271c5f3d26d53610573fba2f4e3f639681608c9ac6888632b2370');
for(const [k,v] of Object.entries(prior.media))assert.deepEqual(media[k],v);
for(const [k,v] of Object.entries(prior.closeups))assert.deepEqual(close[k],v);
for(const [k,v] of Object.entries(prior.context))assert.deepEqual(ctx[k],v);
for(const a of prior.index.assets)assert.deepEqual(index.assets.find(b=>b.path===a.path),a);
for(const old of prior.registry.cards){const c=registry.cards.find(c=>c.id===old.id);assert.equal(createHash('sha256').update(JSON.stringify(c)).digest('hex'),old.sha256);}
assert.deepEqual(registry.cards.filter(c=>c.moment_number&&c.moment_number<=55).map(c=>c.moment_number).sort((a,b)=>a-b),Array.from({length:55},(_,i)=>i+1));assert.equal(Object.keys(media).length,55);assert.equal(index.assets.length,608);assert.equal(Object.keys(ctx).length,55);assert.equal(Object.values(ctx).reduce((n,c)=>n+c.related.length,0),135);
assert.equal(chapter.story.length,5);assert.equal(chapter.eggs.length,4);assert.equal(chapter.sources.length,4);assert(chapter.eggs[3].text.includes('US equity circuit breaker'));assert(chapter.sourceNote.includes('fictional'));
const text=fs.readFileSync('../'+m.chapter.path,'utf8');for(const p of chapter.story)assert(text.includes(p));for(const e of chapter.eggs){assert(text.includes(e.title));assert(text.includes(e.text));}
const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('THURSDAY'));assert(svg.includes('STILL HODLING.'));assert(!svg.includes('translate(0 -80)'));assert(fs.readFileSync('app/crypto/055/page.js','utf8').includes('/cards/black-thursday'));
console.log('PASS: 055 final approved artwork, card/book/clues, 54 previous cards preserved and 608 display assets');
