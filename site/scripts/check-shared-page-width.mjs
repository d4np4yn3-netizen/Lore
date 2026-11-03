import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
const read = p => fs.readFileSync(p, 'utf8');
const shared = read('app/globals.css').split('/* Shared page edges:')[1];
const shop = read('app/shop/shop.module.css');
const banner = read('app/components/ShopCollectionTeaser.module.css');
const seasonTwo = read('app/season-two/season-two.module.css');
test('one bounded gutter and centered outer shell define page edges', () => {
 assert(shared.includes('--site-shell-max:1800px;'));
 assert(shared.includes('--site-gutter:clamp(24px,4.5vw,72px);'));
 assert(shared.includes('--site-inline-padding:max(var(--site-gutter),calc((100% - var(--site-shell-max))/2 + var(--site-gutter)));'));
 for (const selector of ['.site-header','.site-footer','.product-home .hero','.product-home .family-preview','.product-home .coming-soon','.product-home .discovery','.product-home .pack-config','.product-home .timeline-teaser','.product-home .about-histrove']) assert(shared.includes(selector));
 for (const declaration of ['width:100%','max-width:none','margin-left:0','margin-right:0','padding-left:var(--site-inline-padding)','padding-right:var(--site-inline-padding)']) assert(shared.includes(declaration));
});
test('shop and homepage teasers have no independent cap or extra inset', () => {
 assert(shop.startsWith('.shop{width:100%;max-width:none;margin:0;padding:0 var(--site-inline-padding)}'));
 assert.equal((shop.match(/\.shop\{/g)||[]).length,1);
 assert(banner.startsWith('.teaser{width:100%;margin:0 0 75px;padding:0 var(--site-inline-padding);'));
 assert(!banner.includes('max-width:1360px'));
 assert(!banner.includes('padding:0 6vw'));
 assert(seasonTwo.includes('.teaser{margin:0 var(--site-inline-padding);padding:48px 0;'));
});
test('shell arithmetic is fluid below cap, bounded above', () => {
 // Formula checks supplement, not replace, rendered and native-zoom QA.
 for (const viewport of [320,390,768,1024,1440,1920,2560,3840,7680]) {
  const body=viewport-15;
  const gutter=Math.max(24,Math.min(viewport*.045,72));
  const inset=Math.max(gutter,(body-1800)/2+gutter);
  const content=body-inset*2;
  assert(content>0&&content<=1800);
  assert.equal(content,Math.min(body,1800)-2*gutter);
  if(body>=1800)assert.equal(content,1656);
 }
});
