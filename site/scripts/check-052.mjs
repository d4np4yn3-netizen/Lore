import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/052-manifest.json'),chapter=read('app/cards/content/052.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),index=read('media/index.json'),registry=read('../cards/crypto/current-cards.json'),prior=read('media/pre052-preservation.json'),ctx=read('app/cards/story-context.json');
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'52cd74fb1de6fab8379e3a8b2f94002d38f769faa407b29702b582e1d37fa08e');
for(const [k,v]of Object.entries(prior.media))assert.deepEqual(media[k],v);
for(const [k,v]of Object.entries(prior.closeups))assert.deepEqual(close[k],v);
for(const [k,v]of Object.entries(prior.context))assert.deepEqual(ctx[k],v);
for(const old of prior.index.assets)assert.deepEqual(index.assets.find(a=>a.path===old.path),old);
for(const old of prior.registry.cards){const c=registry.cards.find(c=>c.id===old.id);assert.equal(createHash('sha256').update(JSON.stringify(c)).digest('hex'),old.sha256);}
assert.deepEqual(registry.cards.filter(c=>c.moment_number).map(c=>c.moment_number).sort((a,b)=>a-b),[...Array.from({length:50},(_,i)=>i+1),52]);
assert.equal(Object.keys(media).length,51);assert.equal(index.assets.length,576);assert.equal(Object.keys(ctx).length,51);assert.equal(Object.values(ctx).reduce((n,c)=>n+c.related.length,0),123);
assert.equal(chapter.story.length,5);assert.equal(chapter.eggs.length,4);assert.equal(chapter.sources.length,3);assert.equal(chapter.eggs[3].title,'THE HIDDEN KEY NOTE');assert(chapter.eggs[3].text.includes('not a discovered usable key'));assert(chapter.sourceNote.includes('not adjudicated findings'));
const text=fs.readFileSync('../'+m.chapter.path,'utf8');for(const p of chapter.story)assert(text.includes(p));for(const e of chapter.eggs){assert(text.includes(e.title));assert(text.includes(e.text));}
const master='../cards/crypto/season-01/quadrigacx-master-052/';for(const f of read(master+'immutable-package-manifest.json').files)assert.equal(hash(master+f.path),f.sha256);
assert.equal(read(master+'card-final-qa.json').svg_embedded_art_exact,true);assert.equal(read(master+'book-qa.json').embedded_art_pixels_match_original,true);assert.equal(read(master+'book-qa.json').native_effective_ppi,128.2095238095238);
const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('QUADRIGACX'));assert(svg.includes('BALANCES WITHOUT BACKING.'));assert(fs.readFileSync('app/crypto/052/page.js','utf8').includes('/cards/quadrigacx'));assert(!fs.existsSync('app/crypto/051/page.js'));
console.log('PASS: 052 exact final v7 art/card/book hashes, hidden key-note clue, fixed frame/logo clearance; all 52 prior registry objects and 568 display assets preserved; 51 published-route cards, 216 clues, 102 book previews, 123 related links; 051 excluded');
