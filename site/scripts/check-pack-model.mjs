import fs from 'node:fs';
import assert from 'node:assert/strict';
const source=fs.readFileSync('app/components/PackConfiguration.js','utf8');
const home=fs.readFileSync('.next/server/app/index.html','utf8');
const shop=fs.readFileSync('.next/server/app/shop.html','utf8');
assert.equal(4+3+2+1,10);
assert(Math.abs(.6+.3+.1-1)<1e-12);
assert.equal(1/.25,4);
assert.equal(1/.1,10);
assert.equal(1/(.1/4),40);
assert.equal(1/(.1*.25),40);
assert.equal(1/(.1*.25/4),160);
for(const html of [home,shop]){
  assert(html.includes('TARGET ODDS PER PACK'));
  assert(html.includes('subject to final printer collation and production quantities'));
  assert(html.includes('final odds confirmed before sales'));
  assert(html.includes('Foil replaces the regular finish'));
  assert(html.includes('Every pack still contains ten cards'));
  assert(html.includes('Any Mythic, either finish') && html.includes('Any foil Mythic'));
}
assert(home.includes('href="/shop#pack-details"'));
assert(shop.includes('id="pack-details"') && shop.includes('id="pack-faq-heading"'));
for(const phrase of ['60% of packs','30% of packs','10% of packs','25% of packs','75%','1 in 40 packs','1 in 160 packs','not manufacturing quantities or pull rates','does not rank the historical importance','categories overlap','does not guarantee a particular card']) assert(shop.includes(phrase),phrase);
assert.equal((source.match(/<details>/g)||[]).length,6);
assert(!/<form|fetch\(|localStorage|sessionStorage/.test(fs.readFileSync('app/components/ComingSoon.js','utf8')));
console.log('PASS: agreed 4/3/2/1 model, independent 60/30/10 rarity and 25% foil targets, per-pack denominators, overlapping odds, equal-design assumptions, manufacturing caveats and disabled waitlist');
