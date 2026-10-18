import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/056-manifest.json'),chapter=read('app/cards/content/056.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),index=read('media/index.json'),registry=read('../cards/crypto/current-cards.json'),prior=read('media/pre056-preservation.json'),ctx=read('app/cards/story-context.json');
for(const r of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+r.path),r.sha256);
for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(m.art.sha256,'f341ff4b8fcfc673df5a2fdfadc00897cd4777a73333adf440b33a36f7f50c73');
for(const [k,v] of Object.entries(prior.media))assert.deepEqual(media[k],v);
for(const [k,v] of Object.entries(prior.closeups))assert.deepEqual(close[k],v);
for(const [k,v] of Object.entries(prior.context))assert.deepEqual(ctx[k],v);
for(const a of prior.index.assets)assert.deepEqual(index.assets.find(b=>b.path===a.path),a);
for(const old of prior.registry.cards){const c=registry.cards.find(c=>c.id===old.id);assert.equal(createHash('sha256').update(JSON.stringify(c)).digest('hex'),old.sha256);}
assert.deepEqual(registry.cards.filter(c=>c.moment_number&&c.moment_number<=56).map(c=>c.moment_number).sort((a,b)=>a-b),Array.from({length:56},(_,i)=>i+1));assert.equal(Object.keys(media).length,75);assert.equal(index.assets.length,771);assert.equal(Object.keys(ctx).length,75);
assert.equal(chapter.story.length,5);assert.equal(chapter.eggs.length,6);assert.equal(chapter.sources.length,6);assert(chapter.sourceNote.includes('hindsight'));assert(chapter.sourceNote.includes('fictional'));
const text=fs.readFileSync('../'+m.chapter.path,'utf8');for(const p of chapter.story)assert(text.includes(p));for(const e of chapter.eggs){assert(text.includes(e.title));assert(text.includes(e.text));}
const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('translate(0 14)'));assert(svg.includes('generated-top-sky-extension'));assert(svg.includes('BUILT FOR WHAT COMES NEXT.'));assert(fs.readFileSync('app/crypto/056/page.js','utf8').includes('/cards/solana-mainnet-beta'));
for(const r of ctx['solana-mainnet-beta','defi-summer-begins'].related)assert(media[r.slug],r.slug);
console.log('PASS: 056 approved art/card/book/six clues; 55 prior numbered cards, registry objects and all previous display assets preserved');
