import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const m=read('media/060-manifest.json'),ch=read('app/cards/content/060.json'),media=read('app/cards/media.json'),close=read('app/cards/closeups.json'),registry=read('../cards/crypto/current-cards.json');
for(const a of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+a.path),a.sha256);for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256);
assert.equal(Object.keys(media).length,62);assert.equal(close['060'].length,4);assert(!close['058']);assert.deepEqual(registry.cards.filter(c=>c.moment_number).map(c=>c.moment_number).sort((a,b)=>a-b),[...Array.from({length:57},(_,i)=>i+1),59,60,61,62,63]);
assert.equal(ch.story.length,5);assert.equal(ch.eggs.length,4);assert.equal(ch.sources.length,4);assert(ch.story[2].includes('rather than a hack or theft'));assert(!ch.sourceNote.includes('proposed rarity'));
assert.equal(m.art.sha256,'ac0ec8a8521ca94feb282d4728ec3536c8519eb2095dbefa4842dedac16aee4d');const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');assert(svg.includes('1234.4325'));assert(svg.includes('A TASTE FOR LIQUIDITY.'));assert(fs.readFileSync('app/crypto/060/page.js','utf8').includes('/cards/the-vampire-attack'));
console.log('PASS: 060 approved artwork/card/book/four clues and intentional 058 gap; 62 published cards');
