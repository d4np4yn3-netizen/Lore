import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p));const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const registry=read('../cards/crypto/current-cards.json');const media=read('app/cards/media.json');
for(const [n,slug,artHash] of [['074','constitutiondao','3cdcd2dc96a7a8c03315ddc0217d915b90c7cc81ef04491817dbbb4edff00816']]){
 const m=read(`media/${n}-manifest.json`),c=read(`app/cards/content/${n}.json`),master=`../cards/crypto/season-01/${slug}-master-${n}/`;
 assert.equal(m.art.sha256,artHash);
 for(const a of [m.art,m.book,m.chapter,...Object.values(m.print)])assert.equal(hash('../'+a.path),a.sha256,a.path);
 for(const a of m.assets)assert.equal(hash('public/'+a.path),a.sha256,a.path);
 assert.equal(c.story.length,5);assert.equal(c.eggs.length,4);assert.equal(read('app/cards/closeups.json')[n].length,4);
 const qa=read(master+'card-final-qa.json');assert.equal(qa.source_art_unmodified,true);assert.equal(qa.approved_trim_pixel_match,true);assert.equal(m.print.png.sha256,'099bf258201b8e8dc33aadad3e73c6b1f46d3b9156357cc9f114894277fcb809');assert.deepEqual(qa.qr,[`https://lore-site-v1.vercel.app/crypto/${n}/`]);assert.deepEqual(qa.pdf_qr,qa.qr);
 assert.equal(hash(master+'art.png'),m.art.sha256);assert.equal(read(master+'approval.json').publication_authorized,true);assert.equal(read(master+'book-qa.json').publication_authorized,true);
 const svg=fs.readFileSync('../'+m.print.svg.path,'utf8');const embedded=svg.match(/id="card-illustration"[^>]*xlink:href="data:image\/png;base64,([^"]+)"/)||svg.match(/xlink:href="data:image\/png;base64,([^"]+)"[^>]*id="card-illustration"/);assert(embedded);assert.equal(createHash('sha256').update(Buffer.from(embedded[1],'base64')).digest('hex'),m.art.sha256);
 assert(fs.readFileSync(`app/crypto/${n}/page.js`,'utf8').includes('/cards/'+slug));assert.match(media[slug].assetOrigin,/\/[0-9a-f]{40}\/$/);assert.equal(media[slug].assetOrigin,media[slug].bookAssetOrigin);
 assert(c.story.join(' ').includes('18 November 2021'));assert(c.story.join(' ').includes('43.173'));assert.equal(read(master+'card-data.json').rarity,'common');assert.equal(read(master+'card-data.json').context,'A COMMUNITY BIDS FOR HISTORY.');
 const card=registry.cards.find(c=>c.moment_number===Number(n));assert.equal(card.publication_approved,true);assert.equal(card.print_release,false);
}
assert.equal(Object.keys(media).length,77);assert.equal(read('media/index.json').assets.length,787);assert.equal(registry.numbered_published_count,77);assert(!registry.cards.some(c=>c.moment_number===58));
console.log('PASS: 074 approved framing derivative v1, Common frame, source hashes, book, four actual-art clues, QR and 77-card collection');
