import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const site=path.resolve(import.meta.dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(site,p)));
const hash=b=>createHash('sha256').update(b).digest('hex');
const slug='the-bouncing-qr';
const source=fs.readFileSync(path.join(site,'app/cards/data.js'),'utf8').replace(/^import (chapter\d+) from .*;$/gm,'const $1 = {};').replace(/export const /g,'const ');
const card=new Function(source+'; return cards;')().find(c=>c.number==='076/100');
assert(card?.digitalOnly);
assert.equal(card.printerPdf,undefined);assert.equal(card.editableSvg,undefined);
assert.equal(read('app/cards/print-files.json').cards['076'],undefined);
const media=read('app/cards/media.json')[slug],content=read('app/cards/content/076.json');
assert.equal(media.variant,'PUBLIC_DIGITAL_ONLY');assert.equal(content.story.length,5);assert.equal(content.eggs.length,4);
assert.deepEqual([media.artwork.width,media.artwork.height],[1033,1523]);
assert.equal(read('app/cards/closeups.json')['076'].length,4);
for(const crop of read('app/cards/closeups.json')['076'])for(const n of Object.values(crop.bbox))assert(n>=0&&n<=1);
for(const a of read('media/index.json').assets.filter(a=>a.pack==='display-076.bin')){
 const pack=fs.readFileSync(path.join(site,'media',a.pack));assert.equal(hash(pack.subarray(a.offset,a.offset+a.length)),a.sha256);
 assert.equal(hash(fs.readFileSync(path.join(site,'public',a.path))),a.sha256);
}
assert.equal(read('media/index.json').assets.filter(a=>a.pack==='display-076.bin').length,8);
const raw=fs.readFileSync(path.join(site,'..',media.originalArt));assert.equal(hash(raw),media.hashes.artwork);
assert.equal(hash(fs.readFileSync(path.join(site,'..',media.originalBook))),media.hashes.book);
const scan=fs.readFileSync(path.join(site,'app/scan/076/page.js'),'utf8');assert(scan.includes('no active challenges, rewards or registration'));assert(scan.includes('/cards/'+slug));
const rendered=path.join(site,'.next/server/app/cards',slug+'.html');
if(fs.existsSync(rendered)){
 const html=fs.readFileSync(rendered,'utf8');
 for(const forbidden of ['Print card PNG','Download print PDF','Editable card SVG','Download shared back PDF'])assert(!html.includes(forbidden),forbidden);
 assert(html.includes('Download book PDF'));assert(html.includes(media.originalArt));assert(html.includes('076-digital-border-card.webp'));
 console.log('PASS: built 076 page has no physical-print links, retains digital artwork/book and approved image');
}
console.log('PASS: 076 digital-only record, exact source hashes, four clues, eight packed images and honest scan route');
