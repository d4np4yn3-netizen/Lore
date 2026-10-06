// Verify the pinned website revision and the current approved print release separately.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
const site=path.resolve(import.meta.dirname,'..'),repo=path.resolve(site,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(repo,p),'utf8'));
const manifest=read('cards/crypto/print-ready/v1.2/manifest.json');
const currentManifest=read('cards/crypto/print-ready/histrove-v1/manifest.json');
const links=read('site/app/cards/print-files.json');
const registry=read('cards/crypto/current-cards.json');
const numbers=Array.from({length:39},(_,i)=>String(i+1).padStart(3,'0'));
assert.equal(manifest.revision,'LORE-CRYPTO-PRINT-v1.2');
assert.equal(currentManifest.revision,'HISTROVE-CRYPTO-PRINT-v1.0');
assert.equal(registry.print_revision,currentManifest.revision);
assert.equal(manifest.front_count,39);assert.equal(manifest.shared_back_count,1);
assert.equal(currentManifest.front_count,39);assert.equal(currentManifest.shared_back_count,1);
assert.deepEqual(Object.keys(links.cards).sort(),numbers);
assert.deepEqual(currentManifest.fronts.map(c=>c.number).sort(),numbers);
assert.match(links.assetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/);
const hash=p=>createHash('sha256').update(fs.readFileSync(path.join(repo,p))).digest('hex');
for(const card of manifest.fronts){
 const current=registry.cards.find(c=>c.moment_number===Number(card.number));
 assert(current,'Numbered card exists: '+card.number);
 const historical=(current.historical_print_ready??[]).filter(r=>r.revision===manifest.revision);
 assert.equal(historical.length,1,'Exactly one archived website print revision: '+card.number);
 const latest=currentManifest.fronts.find(c=>c.number===card.number);
 assert.equal(current.print_ready.revision,currentManifest.revision);
 for(const format of ['png','pdf','svg']){
  // Website links remain pinned to the exact historical LORE release.
  assert.equal(links.cards[card.number][format],card[format].path);
  assert.equal(historical[0][format].path,card[format].path);
  assert.equal(historical[0][format].sha256,card[format].sha256);
  assert.equal(hash(card[format].path),card[format].sha256);
  // Current registry must resolve to the specific HISTROVE release, not any successor.
  assert.equal(current.print_ready[format].path,latest[format].path);
  assert.equal(current.print_ready[format].sha256,latest[format].sha256);
  assert.equal(hash(latest[format].path),latest[format].sha256);
 }
 assert.equal(card.artwork_bytes_unchanged,true);assert.equal(card.qr_png_and_pdf_pass,true);
 assert.equal(latest.all_nonlogo_elements_unchanged,true);assert.equal(latest.qr_png_pdf_pass,true);
 assert.equal(latest.artwork_sha256,card.artwork_sha256);
 assert.equal(latest.qr_url,current.qr_url);
 assert.equal(latest.source.path,card.svg.path);assert.equal(latest.source.sha256,card.svg.sha256);
 assert.equal(latest.physical_print_release,false);
}
for(const format of ['png','pdf','svg']){
 assert.equal(hash(links.sharedBack[format]),manifest.shared_back[format].sha256);
 const back=currentManifest.shared_back[format];
 assert.equal(registry.shared_print_back[format].path,back.path);
 assert.equal(registry.shared_print_back[format].sha256,back.sha256);
 assert.equal(hash(back.path),back.sha256);
}
const spec=read('cards/crypto/master/histrove-print-v1/print-spec.json');
assert.equal(spec.revision,currentManifest.revision);
assert.deepEqual(spec.full_bleed_px,[816,1110]);assert.equal(spec.dpi,300);
assert.deepEqual(spec.trim_box_px,[36,36,744,1038]);assert.deepEqual(spec.safe_box_px,[66,64.5,684,981]);
assert.equal(spec.templates.length,6);
for(const template of spec.templates)assert.equal(hash(template.path),template.sha256);
const templateQA=read('cards/crypto/master/histrove-print-v1/template-verification.json');
assert.deepEqual(templateQA.map(t=>t.rarity).sort(),['common','epic','legendary','mythic','rare','uncommon']);
for(const result of templateQA){assert.equal(result.png_pdf_qr_pass,true);assert.deepEqual(result.dimensions,[816,1110]);assert.equal(result.dpi,300);}
for(const p of ['site/app/cards/data.js','site/app/cards/media.json','site/app/cards/closeups.json','site/media/index.json','site/web-card-derivatives.json']){
 const original=execFileSync('git',['show','9aeeb54baa4f291fc38242ba7f5e73f892b57f42:'+p],{cwd:repo,maxBuffer:1024*1024});
 assert(fs.readFileSync(path.join(repo,p)).equals(original),'Preserve '+p);
}
console.log('PASS: 39 historical website mappings and 39 current HISTROVE fronts, both shared backs, all file hashes and six printer templates; original display/art/book/closeup data unchanged.');
