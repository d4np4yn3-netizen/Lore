// Check the print-download rollout while pinning the existing display/art/book data.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
const site=path.resolve(import.meta.dirname,'..'),repo=path.resolve(site,'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(repo,p),'utf8'));
const manifest=read('cards/crypto/print-ready/v1.2/manifest.json');
const links=read('site/app/cards/print-files.json');
const registry=read('cards/crypto/current-cards.json');
assert.equal(manifest.front_count,39);assert.equal(manifest.shared_back_count,1);
assert.deepEqual(Object.keys(links.cards).sort(),Array.from({length:39},(_,i)=>String(i+1).padStart(3,'0')));
assert.match(links.assetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/);
const hash=p=>createHash('sha256').update(fs.readFileSync(path.join(repo,p))).digest('hex');
for(const card of manifest.fronts){
 const current=registry.cards.find(c=>c.moment_number===Number(card.number));
 for(const format of ['png','pdf','svg']){
  assert.equal(links.cards[card.number][format],card[format].path);
  assert.equal(current.print_ready[format].path,card[format].path);
  assert.equal(hash(card[format].path),card[format].sha256);
 }
 assert.equal(card.artwork_bytes_unchanged,true);assert.equal(card.qr_png_and_pdf_pass,true);
}
for(const format of ['png','pdf','svg'])assert.equal(hash(links.sharedBack[format]),manifest.shared_back[format].sha256);
for(const p of ['site/app/cards/data.js','site/app/cards/media.json','site/app/cards/closeups.json','site/media/index.json','site/web-card-derivatives.json']){
 const original=execFileSync('git',['show','9aeeb54baa4f291fc38242ba7f5e73f892b57f42:'+p],{cwd:repo,maxBuffer:1024*1024});
 assert(fs.readFileSync(path.join(repo,p)).equals(original),'Preserve '+p);
}
console.log('PASS: 39 print-download mappings, shared back, manifest and registry hashes; original display/art/book/closeup data unchanged.');
