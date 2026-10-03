import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const root=path.resolve(import.meta.dirname,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const layout=fs.readFileSync(path.join(root,'app/cards/marker-layout.js'),'utf8');
const {placeClueMarkers}=await import('data:text/javascript;base64,'+Buffer.from(layout).toString('base64'));
const closeups=read('app/cards/closeups.json');const media=Object.values(read('app/cards/media.json'));const index=read('media/index.json');
let clues=0,positions=0;
assert.equal(media.length,27);assert.equal(Object.keys(closeups).length,27);assert.equal(closeups['022'].length,4);
for(const [id,crops] of Object.entries(closeups)){
 const card=media.find(m=>m.image.src.includes('/'+id+'-'));assert(card,'Card media '+id);
 assert(fs.existsSync(path.join(root,'app/crypto',id,'page.js')),'QR source '+id);
 const content=read('app/cards/content/'+id+'.json');assert.equal(crops.length,content.eggs.length,'Clue count '+id);
 for(const crop of crops){const b=crop.bbox;assert(b.x>=0&&b.y>=0&&b.w>0&&b.h>0&&b.x+b.w<=1.001&&b.y+b.h<=1.001,'Box '+id);assert(fs.existsSync(path.join(root,'public',crop.src)));clues++;}
 for(const width of [240,260,288,351,600,1000,1200,1400]){
  const height=width*card.artwork.height/card.artwork.width;const points=placeClueMarkers(crops,width,height);
  points.forEach((p,i)=>{assert(p.x>=24&&p.x<=width-24&&p.y>=24&&p.y<=height-24,'Edge '+id);for(let j=0;j<i;j++)assert(Math.hypot(p.x-points[j].x,p.y-points[j].y)>=51.999,'Overlap '+id);positions++;});
 }
}
assert.equal(clues,119);assert.equal(fs.readdirSync(path.join(root,'app/crypto')).length,27);
assert.equal(index.assets.length,227);
assert.equal(new Set(index.assets.map(asset=>asset.path)).size,227,'No duplicate media paths');
const added=read('media/022-derivatives.json');
assert.equal(added.previousAssetsPreserved,219);
assert.equal(added.displayAssets.length,8);
assert.deepEqual(read('app/cards/content/022.json').eggs.map(egg=>egg.title),added.clues.map(clue=>clue.title),'022 clue order');
for(const [pack,sha256] of Object.entries(added.previousBundleSHA256)){assert.equal(createHash('sha256').update(fs.readFileSync(path.join(root,'media',pack))).digest('hex'),sha256,'Previous bundle '+pack);}
const addedMedia=read('app/cards/media.json')['buried-fortune'];
assert.equal(addedMedia.hashes.artwork,'0f2b071d25d706ca180d3cad4c7c89bff4f4e370eaa32f5b234135282233ce95');
assert(addedMedia.assetOrigin.startsWith('https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/'));
assert.equal(media.filter(card=>card.assetOrigin).length,1,'Only 022 overrides original asset origin');
const reader=fs.readFileSync(path.join(root,'app/components/ReadingRoom.js'),'utf8');
assert(reader.includes('card.media.assetOrigin || ASSET_ORIGIN'),'Per-card original asset fallback');
assert.equal((reader.match(/href=\{assetOrigin\+/g)||[]).length,3,'All three original links use per-card asset origin');
for(const asset of index.assets){const bytes=fs.readFileSync(path.join(root,'public',asset.path));assert.equal(createHash('sha256').update(bytes).digest('hex'),asset.sha256,asset.path);}
console.log(`PASS: 27 cards, 27 QR sources, ${clues} clue boxes and explanations, ${positions} non-overlapping marker layouts, ${index.assets.length} verified media hashes; 219 earlier images preserved, 022 present`);
