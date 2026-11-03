import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import test from 'node:test';
const read = p => fs.readFileSync(p, 'utf8');
const shop = read('.next/server/app/shop.html');
const interior = read('.next/server/app/shop/interior.html');
const home = read('.next/server/app/index.html');
const shopSource = read('app/shop/page.js');
const shopCss = read('app/shop/shop.module.css');
const teaser = read('app/components/ShopCollectionTeaser.js');

test('shop preserves chrome, canonical route, product anchors and unavailable purchases', () => {
  for (const id of ['shop-main', 'shop-heading', 'booster-packs', 'companion-book', 'pack-details']) assert(shop.includes(`id="${id}"`), id);
  assert(shop.includes('https://www.histrove.co.uk/shop'));
  assert(shop.includes('Analytics preferences'));
  assert(shop.includes('hello@histrove.co.uk'));
  const buttons = [...shop.matchAll(/<button\b[^>]*>[\s\S]*?<\/button>/g)].map(m => m[0]).filter(b => b.includes('Buy now'));
  assert.equal(buttons.length, 2);
  for (const button of buttons) { assert(button.includes('disabled=""')); assert(button.includes('aria-describedby=')); }
  assert.equal((shop.match(/>Coming soon</g) || []).length, 2);
  assert(!/<form\b/.test(shop));
  assert(!/onClick|onSubmit|fetch\s*\(/.test(shopSource));
  assert(shop.includes('Cards and book purchases are not open yet.'));
});

test('actual draft pages remain byte-identical and are accessible at the interior route', () => {
  const images = [
    ['histrove-6x9-draft-pizza-page-16.png', '9d964bbe114216a929d1e832f62d75ccb8f5cb55ed9b05f33aacb06bf75fb999'],
    ['histrove-6x9-draft-pizza-page-17.png', '0fef53826bc69b6367f13db8c677962cf3fc8f6a6c3ba4ec5cf6bbb4247b939d'],
  ];
  for (const [name, hash] of images) {
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync('public/collection/' + name)).digest('hex'), hash);
    assert(shop.includes('/collection/' + name));
    assert(interior.includes(`href="/collection/${name}"`));
  }
  assert(shop.includes('Draft interior · 6 × 9 in'));
  assert(shop.includes('Book visualization, final production details to be confirmed.'));
  assert(shop.includes('href="/shop/interior"'));
  assert(interior.includes('href="/shop#inside-heading"'));
  assert(!/A5|£\d|\$\d/.test(shopSource));
});

test('homepage swaps duplicate product tiles for one linked character banner', () => {
  assert.equal((home.match(/id="collection"/g) || []).length, 1);
  assert(!home.includes('class="home-products"'));
  for (const id of ['coming-soon', 'season-two-teaser-title', 'about', 'archive', 'pack-preview']) assert(home.includes(`id="${id}"`), id);
  assert(teaser.includes('histrove-shop-characters-v1.webp'));
  assert(teaser.includes('href="/shop"'));
  assert(teaser.includes('shop-glint'));
  assert(teaser.includes('Illustration and product concepts. Purchases are not open yet.'));
  assert(teaser.includes('(max-width:760px) 180vw, 91vw'));
});

test('bright perimeter has static fallback and respects reduced motion', () => {
  assert(shopCss.includes('.buy-button.shop-spotlight:disabled{opacity:1;cursor:not-allowed}'));
  assert(shopCss.includes('box-shadow:0 0 0 1px'));
  assert(shopCss.includes('animation:shop-border-glint 8s linear infinite'));
  assert(shopCss.includes('@media(prefers-reduced-motion:reduce){.shop-glint{display:none!important}'));
  assert(shopCss.includes('.shop-glint:after{animation:none!important}'));
});
