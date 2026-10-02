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
assert.equal(media.length,26);assert.equal(Object.keys(closeups).length,26);assert(!closeups['022']);
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
assert.equal(clues,115);assert.equal(fs.readdirSync(path.join(root,'app/crypto')).length,26);
for(const asset of index.assets){const bytes=fs.readFileSync(path.join(root,'public',asset.path));assert.equal(createHash('sha256').update(bytes).digest('hex'),asset.sha256,asset.path);}
console.log(`PASS: 26 cards, 26 QR sources, ${clues} clue boxes and explanations, ${positions} non-overlapping marker layouts, ${index.assets.length} unchanged media hashes; 022 absent`);
