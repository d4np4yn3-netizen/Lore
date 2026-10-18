import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p));const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const registry=read('../cards/crypto/current-cards.json');const media=read('app/cards/media.json');
for(const [n,slug,artHash,proofHash] of [
['069','eip-1559','1efc6bd85a8a4c5e2aec5ab6d33de264c8104ad0842a066f4416411a6903f646','55406f949952998a053a4df0542d3509594eca5ae5094393cad486b402c6028f'],
['070','the-poly-network-exploit','7f268a75fba03dc02198e0d571537a88dbe7f49d4e1aab238da9a85bcb5e21b6','737dd92220de55750e8ee77b1910e2a855e87ff71891b50e6b12acc3aacd13a8']]){
 const m=read(`media/${n}-manifest.json`),c=read(`app/cards/content/${n}.json`),master=`../cards/crypto/season-01/${slug}-master-${n}/`;
 assert.equal(m.art.sha256,artHash);assert.equal(m.print.png.sha256,proofHash);
 for(const a of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+a.path),a.sha256,a.path);
 for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256,a.path);
 assert.equal(c.story.length,5);assert.equal(c.eggs.length,4);assert.equal(read('app/cards/closeups.json')[n].length,4);
 const qa=read(master+'card-final-qa.json');assert.equal(qa.approved_trim_pixel_match,true);assert.equal(qa.source_art_unmodified,true);assert.deepEqual(qa.qr,[`https://lore-site-v1.vercel.app/crypto/${n}/`]);assert.deepEqual(qa.pdf_qr,qa.qr);
 assert.equal(hash(master+'art.png'),m.art.sha256);assert.equal(read(master+'approval.json').publication_authorized,true);assert.equal(read(master+'book-qa.json').publication_authorized,true);
 const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');const embedded=svg.match(/id="card-illustration"[^>]*xlink:href="data:image\/png;base64,([^"]+)"/)||svg.match(/xlink:href="data:image\/png;base64,([^"]+)"[^>]*id="card-illustration"/);assert(embedded);assert.equal(createHash('sha256').update(Buffer.from(embedded[1],'base64')).digest('hex'),m.art.sha256);
 assert(fs.readFileSync(`app/crypto/${n}/page.js`,'utf8').includes('/cards/'+slug));assert.match(media[slug].assetOrigin,/\/[0-9a-f]{40}\/$/);assert.equal(media[slug].assetOrigin,media[slug].bookAssetOrigin);
 if(n==='070'){assert.equal(m.art.sha256,artHash);assert.equal(m.print.png.sha256,proofHash);assert(c.story[0].includes('10 August 2021'));assert(c.story[2].includes('11 August'));assert(c.story[3].includes('26 August'));assert(c.story[4].includes('fictional pirate'));}
 const card=registry.cards.find(c=>c.moment_number===Number(n));assert.equal(card.publication_approved,true);assert.equal(card.print_release,false);
}
assert.equal(Object.keys(media).length,70);assert.equal(read('media/index.json').assets.length,731);assert.equal(registry.numbered_published_count,70);assert(!registry.cards.some(c=>c.moment_number===58));
console.log('PASS: 069 and 070 exact approved source bytes, embedded art, print/book aliases, five-paragraph stories, four clues, QR evidence and 70-card collection');
