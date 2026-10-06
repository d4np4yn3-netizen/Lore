import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=path.resolve(import.meta.dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const hash=b=>createHash('sha256').update(b).digest('hex');
const file=p=>fs.readFileSync(path.join(root,p));
const contract=read('rebrand-preservation.json'),media=read('app/cards/media.json'),index=read('media/index.json'),closeups=read('app/cards/closeups.json');
const layouts=file('app/cards/marker-layout.js').toString();
const {placeClueMarkers}=await import('data:text/javascript;base64,'+Buffer.from(layouts).toString('base64'));
const ids=Array.from({length:44},(_,i)=>String(i+1).padStart(3,'0'));
assert.equal(Object.keys(media).length,44);assert.deepEqual(Object.keys(closeups).sort(),ids);
assert.equal(hash(file('media/pre040-closeups.json')),contract.closeupsSHA256);assert.deepEqual(Object.fromEntries(Object.entries(closeups).filter(([id])=>!['040','041','042','043','044'].includes(id))),read('media/pre040-closeups.json'),'Prior39 clues preserved');
let clues=0,pages=0,positions=0;
for(const [slug,card] of Object.entries(media)){
 const id=card.image.src.match(/\/(\d{3})-/)[1],old=contract.originalMedia[slug],copy=read('app/cards/content/'+id+'.json'),crops=closeups[id];
 if(!['040','041','042','043','044'].includes(id)){assert.equal(hash(file('app/cards/content/'+id+'.json')),contract.contentAfterBrandOnly[id],'Brand-only editorial change '+id);
 assert.equal(hash(file('app/crypto/'+id+'/page.js')),contract.qrSourceSHA256[id],'Printed QR source unchanged '+id);
 assert.deepEqual(card.artwork,old.artwork);assert.equal(card.originalArt,old.originalArt);assert.equal(card.assetOrigin,old.assetOrigin);assert.equal(card.hashes.artwork,old.hashes.artwork);
 }
 assert(card.image.src.endsWith('-histrove-border-card.webp'));assert.equal(card.image.width,600);assert.equal(card.image.height,863);
 assert.equal(card.pages.length,2);assert(card.originalBook.includes('/histrove-v1/'));assert.match(card.bookAssetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/);
 assert.equal(crops.length,copy.eggs.length);clues+=crops.length;pages+=2;
 for(const asset of [card.image,card.artwork,...card.pages,...crops]){
  assert(fs.existsSync(path.join(root,'public',asset.src)),'Displayed asset '+asset.src);
  assert(index.assets.some(a=>'/'+a.path===asset.src),'Indexed display '+asset.src);
 }
 for(const crop of crops){const b=crop.bbox;assert(b.x>=0&&b.y>=0&&b.w>0&&b.h>0&&b.x+b.w<=1.001&&b.y+b.h<=1.001);}
 for(const width of [240,260,288,351,600,1000,1200,1400]){
  const height=width*card.artwork.height/card.artwork.width;const points=placeClueMarkers(crops,width,height);
  points.forEach((p,i)=>{assert(p.x>=24&&p.x<=width-24&&p.y>=24&&p.y<=height-24);for(let j=0;j<i;j++)assert(Math.hypot(p.x-points[j].x,p.y-points[j].y)>=51.999);positions++;});
 }
}
assert.equal(clues,188);assert.equal(pages,88);
assert.equal(new Set(index.assets.map(a=>a.path)).size,index.assets.length,'Unique media paths');
for(const asset of contract.originalIndex.assets)assert.deepEqual(index.assets.find(a=>a.path===asset.path),asset,'Historical display asset retained '+asset.path);
for(const a of index.assets){const packed=fs.readFileSync(path.join(root,'media',a.pack)).subarray(a.offset,a.offset+a.length);assert.equal(hash(packed),a.sha256);assert.equal(hash(file('public/'+a.path)),a.sha256);}
const reader=file('app/components/ReadingRoom.js').toString(),experience=file('app/cards/experience.js').toString(),home=file('app/page.js').toString();
assert(reader.includes('card.media.assetOrigin || ASSET_ORIGIN'));assert(reader.includes('card.media.bookAssetOrigin || assetOrigin'));assert.equal((reader.match(/href=\{printOrigin\+/g)||[]).length,4);
assert(home.includes('years[years.length-1]'));assert(experience.includes("range:'2013 — 2017'"));
assert(home.includes('History<br/>Worth <span>Holding</span>'));assert(!home.includes('COLLECT THE INTERNET'));assert(!home.includes('loreMoment'));
for(const p of ['app/page.js','app/components/SiteChrome.js','app/components/DiscoveryReveal.js','app/components/PhysicalCollection.js','app/layout.js','app/cards/[slug]/page.js'])assert(!/\bLORE\b/.test(file(p).toString()),'Current brand '+p);
console.log(`PASS: 44 cards and preserved earlier QR sources, ${clues} total clues, ${pages} current book previews, ${positions} marker positions; all ${index.assets.length} image hashes and historical assets verified`);
const brand=read('media/histrove-brand-manifest.json');assert.equal(brand.card_count,39);assert.equal(brand.master_tagline,'History Worth Holding');for(const asset of brand.files){assert.equal(hash(fs.readFileSync(path.join(root,'..',asset.path))),asset.sha256,'Final brand asset '+asset.path);}
console.log('PASS: every final logo, social image, icon, booster and current card derivative matches its completed QA manifest');

const border=read('media/histrove-border-manifest.json');assert.equal(border.cards.length,39);assert.equal(border.all39QrPass,true);for(const c of border.cards){assert.deepEqual(c.dimensions_px,[600,863]);assert.deepEqual(c.conservative_crop_ltrb,[72,72,744,1038]);assert.equal(c.complete_border_geometry_retained,true);assert.equal(c.print_source_unchanged,true);assert.equal(c.qr_pass,true);assert.deepEqual(c.qr_payloads,['https://lore-site-v1.vercel.app/crypto/'+c.number+'/']);assert.equal(hash(file('public'+c.public_path)),c.sha256);}
assert(reader.includes('href={card.media.image.src}'),'Reader opens the border-only web card');assert(reader.includes('Print card PNG'),'Print PNG destination remains separately available');console.log('PASS: all39 SVG-derived complete-border crops, recorded final QR decodes and separate web/print links');
