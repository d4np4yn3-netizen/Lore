import fs from 'node:fs';
import assert from 'node:assert/strict';
const source=fs.readFileSync('app/components/PackConfiguration.js','utf8');
for(const path of ['index','shop']){
 const html=fs.readFileSync(`.next/server/app/${path}.html`,'utf8');
 assert(html.includes('Four Common, three Uncommon, two Rare and one premium card.'));
 assert(html.includes('Foil selection and odds are under review.'));
 assert(html.includes('subject to printer collation and production quantities'));
 assert(!html.includes('1 in 40') && !html.includes('1 in 160') && !html.includes('TARGET ODDS PER PACK'));
 assert(!html.includes('Foil replaces the regular finish') && !html.includes('25% of packs'));
}
assert(!/60%|30%|10%|25%|75%|50 foil/.test(source));
console.log('PASS: current 4/3/2/1 pack plan retained; unconfirmed foil count, placement, eligibility and odds not promised.');
