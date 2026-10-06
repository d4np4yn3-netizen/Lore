import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const site=path.resolve(import.meta.dirname,'..'),repo=path.resolve(site,'..');const read=p=>JSON.parse(fs.readFileSync(path.join(repo,p),'utf8'));
const manifest=read('cards/crypto/print-ready/histrove-v1/manifest.json'),links=read('site/app/cards/print-files.json'),registry=read('cards/crypto/current-cards.json');
assert.equal(links.revision,manifest.revision);assert.equal(registry.print_revision,manifest.revision);assert.equal(manifest.front_count,43);assert.equal(manifest.shared_back_count,1);
assert.match(links.assetOrigin,/^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/);
assert.equal(Object.keys(links.cards).length,43);let count=0;
for(const card of manifest.fronts){assert(card.qr_png_pdf_pass);assert.equal(card.qr_url,'https://lore-site-v1.vercel.app/crypto/'+card.number+'/');for(const ext of ['png','pdf','svg']){assert.equal(links.cards[card.number][ext],card[ext].path);assert.equal(createHash('sha256').update(fs.readFileSync(path.join(repo,card[ext].path))).digest('hex'),card[ext].sha256);count++;}}
for(const ext of ['png','pdf','svg']){const asset=manifest.shared_back[ext];assert.equal(links.sharedBack[ext],asset.path);assert.equal(createHash('sha256').update(fs.readFileSync(path.join(repo,asset.path))).digest('hex'),asset.sha256);count++;}
assert.equal(manifest.physical_print_release,false);console.log(`PASS: ${count} exact approved HISTROVE print download paths and hashes, all 43 QR destinations; physical print approval remains separate`);
const data=fs.readFileSync(path.join(site,'app/cards/data.js'),'utf8').replace(/^import (chapter\d+) from .*;$/gm,'const $1 = {};').replace(/export const /g,'const ');
const cards=new Function(data+'; return cards;')();assert.equal(cards.length,43);for(const card of cards){const current=links.cards[card.number.split('/')[0]];assert.equal(card.image,current.png);if(card.printerPdf)assert.equal(card.printerPdf,current.pdf);if(card.editableSvg)assert.equal(card.editableSvg,current.svg);}
console.log('PASS: all card-code print fallbacks reference the current HISTROVE revision');
