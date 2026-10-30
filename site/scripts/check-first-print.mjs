import fs from 'node:fs';
import assert from 'node:assert/strict';
import test from 'node:test';
const read=p=>fs.readFileSync(p,'utf8');
const pages=['index','shop'].map(p=>read(`.next/server/app/${p}.html`));
const section=html=>html.match(/<section class="coming-soon".*?<\/section>/s)[0];
const source=read('app/components/ComingSoon.js');
test('physical first-print purpose, distinct target and lifetime cap stay clear',()=>{
 for(const html of pages){const s=section(html);for(const text of ['PHYSICAL CARDS','66,666','Planned lifetime Season One cap','1,000','First-run interest target','not current orders','One email','No newsletter','not an order, payment or reservation','No guaranteed pack','does not collect or store email addresses or quantities'])assert(s.includes(text),text);assert(!/666,666|\$9\.99|\$1\.80|\$2|50 foil|Dan Payne|Daniel Payne|NFT|redeem/i.test(s));}
});
test('disabled email and quantity have labels; no collection path or false success',()=>{
 for(const html of pages){const s=section(html);assert.equal((s.match(/<input\b/g)||[]).length,2);for(const id of ['launch-email','launch-quantity']){assert(s.includes(`for="${id}"`));assert(new RegExp(`<input[^>]*id="${id}"[^>]*disabled=""`).test(s));}assert(s.includes('Non-binding estimate'));assert(/<button[^>]*type="button"[^>]*disabled=""/.test(s));assert(!/<form\b|<iframe\b|type="checkbox"|\baction=/.test(s));}
 assert(!/\bfetch\s*\(|sendBeacon|onSubmit|onClick|localStorage|sessionStorage|google\.com\/forms/.test(source));
});
test('all six rarity counts remain visible outside expandable print details',()=>{
 for(const html of pages){const s=section(html);assert(/<details class="first-print-rarity-details"><summary>/.test(s));for(const [rarity,count]of [['Common',30],['Uncommon',25],['Rare',20],['Epic',13],['Legendary',8],['Mythic',4]]){assert(s.includes(`View all ${count} ${rarity} card designs`));assert(s.includes(`rarity=${rarity.toLowerCase()}`));}assert(s.includes('Unique designs, not pack odds.'));assert(s.replace(/<!--.*?-->/g,'').includes('100 card designs'));assert(s.indexOf('first-print-rarity-strip') < s.indexOf('<details'));assert(!s.match(/<details.*?<\/details>/s)[0].includes('View all 30'));assert(s.includes('Print and foil details'));}
});
test('banner and showcase reuse approved raw artwork without framed cards or new assets',()=>{
 assert(source.includes('card.media.artwork.src'));assert(!source.includes('card.media.image'));for(const slug of ['the-first-halving','the-fourth-halving','the-bybit-heist','three-arrows-falls','black-thursday'])assert(source.includes(slug));
 for(const html of pages){const s=section(html);assert.equal((s.match(/<img\b/g)||[]).length,5);assert(!/<img[^>]*alt=""/.test(s));assert(s.includes('Artwork from cards 015'));assert(s.includes('The history. The art.'));}
});
test('Season Two and shop stay closed and independent',()=>{
 const s=read('.next/server/app/season-two.html');assert(s.includes('Suggestions are not open yet.'));assert(s.includes('will not sign you up for marketing emails'));assert(pages[1].includes('Purchases aren’t open yet'));for(const p of pages)assert(!p.includes('Add to cart')&&!p.includes('Buy now'));
});
