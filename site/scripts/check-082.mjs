// Run manually from the integrated site's directory: node /path/to/check-082.mjs
// Reads local files only. This is not proof of a successful upload or deployment.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';

const read = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const fileHash = path => hash(fs.readFileSync(path));
const slug = 'tornado-cash-sanctioned';
const manifest = read('media/082-manifest.json');
const chapter = read('app/cards/content/082.json');
const media = read('app/cards/media.json')[slug];
const closeups = read('app/cards/closeups.json')['082'];
const prints = read('app/cards/print-files.json').cards['082'];
const index = read('media/index.json');
const data = fs.readFileSync('app/cards/data.js', 'utf8');
const route = fs.readFileSync('app/crypto/082/page.js', 'utf8');
const originals = [manifest.art, manifest.book, manifest.chapter, ...Object.values(manifest.print)];

assert.equal(manifest.qr, 'https://lore-site-v1.vercel.app/crypto/082/');
assert.equal(manifest.assets.length, 8);
assert.equal(chapter.eggs.length, 4);
assert.ok(chapter.story.length > 0);
assert.ok(chapter.sources.length > 0);
assert.equal(closeups.length, chapter.eggs.length);
for (const original of originals) {
  const path = '../' + original.path;
  assert.equal(fileHash(path), original.sha256, 'Original hash: ' + original.path);
  assert.equal(fs.statSync(path).size, original.bytes, 'Original size: ' + original.path);
}
const pack = fs.readFileSync('media/display-082.bin');
let end = 0;
for (const asset of manifest.assets) {
  assert.equal(asset.pack, 'display-082.bin');
  assert.equal(asset.offset, end);
  const packedBytes = pack.subarray(asset.offset, asset.offset + asset.length);
  assert.equal(hash(packedBytes), asset.sha256, 'Packed hash: ' + asset.path);
  assert.equal(fileHash('public/' + asset.path), asset.sha256, 'Public hash: ' + asset.path);
  const matches = index.assets.filter(entry => entry.path === asset.path);
  assert.equal(matches.length, 1, 'Unique media index path: ' + asset.path);
  assert.deepEqual(matches[0], asset);
  end += asset.length;
}
assert.equal(pack.length, end);
assert.equal(media.originalArt, manifest.art.path);
assert.equal(media.originalBook, manifest.book.path);
assert.equal(media.hashes.image, manifest.print.png.sha256);
assert.equal(media.hashes.artwork, manifest.art.sha256);
assert.equal(media.hashes.book, manifest.book.sha256);
assert.equal(media.hashes.webImage, manifest.web_border.sha256);
assert.equal(media.assetOrigin, media.bookAssetOrigin);
assert.match(media.assetOrigin, /^https:\/\/raw\.githubusercontent\.com\/d4np4yn3-netizen\/Lore\/[0-9a-f]{40}\/$/);
assert.equal(prints.assetOrigin, media.assetOrigin);
for (const extension of ['png', 'pdf', 'svg']) {
  assert.equal(prints[extension], manifest.print[extension].path);
}
for (const [i, closeup] of closeups.entries()) {
  assert.equal(closeup.src, '/closeups/082-' + String(i + 1).padStart(2, '0') + '.webp');
  assert.equal(closeup.alt, chapter.eggs[i].title + '. ' + chapter.eggs[i].text);
  const box = closeup.bbox;
  assert.ok(box.x >= 0 && box.y >= 0 && box.w > 0 && box.h > 0);
  assert.ok(box.x + box.w <= 1.000000001 && box.y + box.h <= 1.000000001);
}
assert.equal((data.match(/import chapter082 from '\.\/content\/082\.json';/g) || []).length, 1);
assert.equal((data.match(/number["']?\s*:\s*['"]082\/100['"]/g) || []).length, 1);
assert.ok(data.includes('slug: "' + slug + '"'));
assert.ok(data.includes('"title": "SANCTIONED"'));
assert.ok(data.includes('"subject": "TORNADO CASH"'));
assert.ok(data.includes('"phrase": "SEALED"'));
assert.ok(data.includes('"rarity": "RARE"'));
assert.ok(data.includes('"date": "08 AUG 2022"'));
assert.ok(data.includes('Approved original editorial metaphor, not a historical quotation'));
assert.ok(route.includes("redirect('/cards/" + slug + "')"));
assert.deepEqual(manifest.web_border.qr_payloads, [manifest.qr]);
assert.equal(manifest.web_border.qr_pass, true);
assert.equal(manifest.web_border.source_sha256, manifest.print.png.sha256);
assert.equal(manifest.web_border.source_svg_sha256, manifest.print.svg.sha256);
console.log('PASS: 082 original hashes, eight packed/public assets, unique site entries, chapter, metadata, crop bounds and redirect. Upload, deployment, visual and live-download verification remain separate.');
