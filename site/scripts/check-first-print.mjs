import fs from 'node:fs';
import assert from 'node:assert/strict';
import test from 'node:test';
const read=p=>fs.readFileSync(p,'utf8');
const pages=['index'].map(p=>read(`.next/server/app/${p}.html`));
const section=html=>html.match(/<section class="coming-soon[^"]*".*?<\/section>/s)[0];
const source=read('app/components/ComingSoon.js');
test('physical first-print purpose, distinct target and lifetime cap stay clear',()=>{
 for(const html of pages){const s=section(html);for(const text of ['PHYSICAL CARDS','66,666','Planned lifetime Season One cap','1,000','First-run interest target','not current orders','One email','No newsletter','Not an order or reservation','No payment or guaranteed pack','No automatic confirmation email is sent.'])assert(s.includes(text),text);assert(!/666,666|\$9\.99|\$1\.80|\$2|50 foil|Dan Payne|Daniel Payne|NFT|redeem/i.test(s));}
});
test('hosted signup is explicit with no dummy fields or local submission',()=>{
 for(const html of pages){const s=section(html);assert.equal((s.match(/<input\b/g)||[]).length,0);assert(s.includes('Register first-print interest'));assert(s.includes('Opens Google Forms'));assert(s.includes('https://docs.google.com/forms/d/e/1FAIpQLSfFIPxtdKXZ__3x7PJQbEUJwSH_J0IhPK5h3cGlixnd00sqAw/viewform?usp=header'));assert(!/<form\b|<iframe\b|type="checkbox"|\baction=/.test(s));}
 assert(!/\bfetch\s*\(|sendBeacon|onSubmit|onClick|localStorage|sessionStorage/.test(source));
});
test('all six rarity counts remain visible outside expandable print details',()=>{
 for(const html of pages){const s=section(html);assert(/<details class="first-print-rarity-details"><summary>/.test(s));for(const [rarity,count]of [['Common',30],['Uncommon',25],['Rare',20],['Epic',13],['Legendary',8],['Mythic',4]]){assert(s.includes(`View all ${count} ${rarity} card designs`));assert(s.includes(`rarity=${rarity.toLowerCase()}`));}assert(s.includes('Unique designs, not pack odds.'));assert(s.replace(/<!--.*?-->/g,'').includes('100 card designs'));assert(s.indexOf('first-print-rarity-strip') < s.indexOf('<details'));assert(!s.match(/<details.*?<\/details>/s)[0].includes('View all 30'));assert(s.includes('Print and foil details'));}
});
test('four-panel banner reuses approved raw artwork with separate text',()=>{
 assert(source.includes('card.media.artwork.src'));assert(!source.includes('card.media.image'));for(const slug of ['birth-of-hodl','cryptopunks','much-wow','cryptokitties'])assert(source.includes(slug));
 for(const html of pages){const s=section(html);assert.equal((s.match(/<img\b/g)||[]).length,4);assert(!/<img[^>]*alt=""/.test(s));assert(s.includes('Original artwork from Crypto Season One.'));assert(s.includes('021 / BIRTH OF HODL'));assert(s.includes('020 / BIRTH OF DOGE'));assert(s.indexOf('first-print-banner-copy') < s.indexOf('first-print-panorama'));}
});
test('Season Two and shop stay closed and independent',()=>{
 const s=read('.next/server/app/season-two.html');assert(s.includes('Suggestions open soon. These preview fields are disabled.'));assert(s.includes('No marketing signup.'));const shop=read('.next/server/app/shop.html');assert(shop.includes('Purchases aren’t open yet'));assert.equal((shop.match(/<button[^>]*disabled=""[^>]*>/g)||[]).length,2);assert(!shop.includes('Add to cart'));for(const p of pages)assert(!p.includes('Add to cart')&&!p.includes('Buy now'));
});

test('all six rarity links sit within the compact left column before signup',()=>{const h=section(pages[0]);const left=h.slice(h.indexOf('class="launch-copy"'),h.indexOf('<aside'));assert(left.includes('first-print-numbers'));assert.equal((left.match(/View all \d+ \w+ card designs/g)||[]).length,6);assert(left.includes('Unique designs, not pack odds.'));assert(!h.includes('first-print-rarities-after-signup'));});
