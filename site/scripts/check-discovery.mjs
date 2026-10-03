import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';

const root = path.resolve(import.meta.dirname, '..');
const repo = path.resolve(root, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const jsonHash = value => hash(JSON.stringify(value));
const fileHash = p => hash(fs.readFileSync(p));
const layout = fs.readFileSync(path.join(root, 'app/cards/marker-layout.js'), 'utf8');
const { placeClueMarkers } = await import('data:text/javascript;base64,' + Buffer.from(layout).toString('base64'));
const closeups = read('app/cards/closeups.json');
const mediaBySlug = read('app/cards/media.json');
const media = Object.values(mediaBySlug);
const index = read('media/index.json');
const derivatives = read('web-card-derivatives.json');
const contentIds = fs.readdirSync(path.join(root, 'app/cards/content')).filter(f => /^\d{3}\.json$/.test(f)).map(f => f.slice(0, 3)).sort();
const expectedIds = Array.from({ length: 28 }, (_, i) => String(i + 1).padStart(3, '0'));
const mediaIds = media.map(card => card.image.src.match(/\/(\d{3})-/)?.[1]).sort();
const qrIds = fs.readdirSync(path.join(root, 'app/crypto')).filter(id => /^\d{3}$/.test(id)).sort();
const cardSource = fs.readFileSync(path.join(root, 'app/cards/data.js'), 'utf8');
const cardIds = [...cardSource.matchAll(/number:\s*['"](\d{3})\/100['"]/g)].map(m => m[1]).sort();
for (const [label, ids] of Object.entries({ content: contentIds, media: mediaIds, clues: Object.keys(closeups).sort(), QR: qrIds, cards: cardIds })) {
  assert.deepEqual(ids, expectedIds, `${label}: contiguous 001–028`);
}

let clues = 0;
let positions = 0;
let pages = 0;
const displayedPaths = [];
for (const id of contentIds) {
  const card = media.find(m => m.image.src.includes('/' + id + '-'));
  const crops = closeups[id];
  const content = read('app/cards/content/' + id + '.json');
  assert.equal(crops.length, content.eggs.length, 'Clue count ' + id);
  assert.equal(card.pages.length, 2, 'Two book pages ' + id);
  pages += card.pages.length;
  displayedPaths.push(card.image.src, card.artwork.src, ...card.pages.map(page => page.src), ...crops.map(crop => crop.src));
  for (const crop of crops) {
    const b = crop.bbox;
    assert(b.x >= 0 && b.y >= 0 && b.w > 0 && b.h > 0 && b.x + b.w <= 1.001 && b.y + b.h <= 1.001, 'Box ' + id);
    assert(fs.existsSync(path.join(root, 'public', crop.src)), 'Crop file ' + id);
    clues++;
  }
  for (const width of [240, 260, 288, 351, 600, 1000, 1200, 1400]) {
    const height = width * card.artwork.height / card.artwork.width;
    const points = placeClueMarkers(crops, width, height);
    points.forEach((p, i) => {
      assert(p.x >= 24 && p.x <= width - 24 && p.y >= 24 && p.y <= height - 24, 'Edge ' + id);
      for (let j = 0; j < i; j++) assert(Math.hypot(p.x - points[j].x, p.y - points[j].y) >= 51.999, 'Overlap ' + id);
      positions++;
    });
  }
}
assert.equal(index.assets.length, media.length * 2 + pages + clues, 'Derived media count');
assert.equal(new Set(index.assets.map(asset => asset.path)).size, index.assets.length, 'No duplicate media paths');
assert.deepEqual(index.assets.map(asset => '/' + asset.path).sort(), displayedPaths.sort(), 'Index covers every displayed image exactly once');
for (const asset of index.assets) {
  assert.equal(fileHash(path.join(root, 'public', asset.path)), asset.sha256, asset.path);
  const packed = fs.readFileSync(path.join(root, 'media', asset.pack)).subarray(asset.offset, asset.offset + asset.length);
  assert.equal(hash(packed), asset.sha256, 'Packed bytes ' + asset.path);
}

// Pinned semantic snapshots from remote baseline 986261d9dad38198d201a34f53027564b2cfe93d.
// Removing only the 028 additions must recover every earlier record exactly.
const { '028': latestClues, ...priorCloseups } = closeups;
const { 'the-ether-sale': latestMedia, ...priorMedia } = mediaBySlug;
const priorIndex = { ...index, assets: index.assets.filter(asset => asset.pack !== 'display-07.bin') };
const priorDerivatives = { ...derivatives, cards: derivatives.cards.filter(card => card.number !== '028') };
assert.equal(jsonHash(priorCloseups), 'e6de4632aefb7d1b66ec841758c23a359f4825095f95ea761e05ad9733363f93', 'All 119 earlier clue records preserved');
assert.equal(jsonHash(priorMedia), '6686d49cf24a79e6620b71e445ff13eccd85060481231a0674058f78ca186aa9', 'All 27 earlier card media records preserved');
assert.equal(jsonHash(priorIndex), '4a79fbeff23b97f2816dd62d924de2ff41dc30f40090b773577d2f14a1db22f0', 'All 227 earlier media index records preserved');
assert.equal(jsonHash(priorDerivatives), '380a567b777d57d8b3f92c193233c743f69f96c7a5453a9297215ec01884ee92', 'All 27 earlier trim records preserved');

for (const id of ['022', '028']) {
  const added = read('media/' + id + '-derivatives.json');
  assert.equal(added.displayAssets.length, 4 + closeups[id].length, id + ' display assets');
  assert.deepEqual(read('app/cards/content/' + id + '.json').eggs.map(egg => egg.title), added.clues.map(clue => clue.title), id + ' clue order');
  for (const [pack, sha256] of Object.entries(added.previousBundleSHA256)) {
    assert.equal(fileHash(path.join(root, 'media', pack)), sha256, 'Previous bundle ' + pack);
  }
}
assert.equal(read('media/022-derivatives.json').previousAssetsPreserved, 219);
assert.equal(mediaBySlug['buried-fortune'].hashes.artwork, '0f2b071d25d706ca180d3cad4c7c89bff4f4e370eaa32f5b234135282233ce95');
assert.equal(media.filter(card => card.assetOrigin).length, 2, 'Only 022 and 028 override original asset origin');
for (const card of media.filter(card => card.assetOrigin)) assert(card.assetOrigin.startsWith('https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/'));
const reader = fs.readFileSync(path.join(root, 'app/components/ReadingRoom.js'), 'utf8');
assert(reader.includes('card.media.assetOrigin || ASSET_ORIGIN'), 'Per-card original asset fallback');
assert.equal((reader.match(/href=\{assetOrigin\+/g) || []).length, 3, 'All three original links use per-card asset origin');

const added = read('media/028-derivatives.json');
assert.equal(added.previousAssetsPreserved, priorIndex.assets.length);
assert.equal(added.previousAssetsPreserved, 227);
assert.equal(latestClues.length, 4);
assert.deepEqual(added.displayAssets, index.assets.filter(asset => asset.pack === 'display-07.bin'), '028 index records');
assert.equal(fileHash(path.join(root, 'media/display-07.bin')), added.bundleSHA256, '028 bundle');
assert.equal(latestMedia.hashes.artwork, 'bf8010c31fd090b42aa4ecda171ae3de3212364433df231516a041a1ad080cf7', 'Approved 028 artwork');
for (const [source, sha256] of Object.entries(added.sourcesSHA256)) assert.equal(fileHash(path.join(repo, source)), sha256, '028 unchanged original ' + source);
assert.equal(latestMedia.hashes.artwork, added.sourcesSHA256[latestMedia.originalArt]);
assert.equal(latestMedia.hashes.book, added.sourcesSHA256[latestMedia.originalBook]);
const trim = derivatives.cards.find(card => card.number === '028');
assert.equal(latestMedia.hashes.image, added.sourcesSHA256[trim.source]);
assert.equal(trim.sourceSHA256, latestMedia.hashes.image);
assert.deepEqual(trim.sourceDimensions, [816, 1110]);
assert.deepEqual(trim.trimBoxXYWH, [36, 36, 744, 1038]);
assert.deepEqual(added.printTrimBoxXYWH, trim.trimBoxXYWH);
assert.equal(fileHash(path.join(repo, trim.webPreview)), trim.webSHA256);
const png = fs.readFileSync(path.join(repo, trim.source));
assert.deepEqual([png.readUInt32BE(16), png.readUInt32BE(20)], trim.sourceDimensions);
for (const [i, clue] of added.clues.entries()) {
  const { title, sourceBoxXYXY: box, ...display } = clue;
  assert.deepEqual(display, latestClues[i], '028 clue metadata ' + title);
  const [x1, y1, x2, y2] = box;
  const [w, h] = added.artDimensions;
  assert.deepEqual(display.bbox, Object.fromEntries(['x', 'y', 'w', 'h'].map((key, n) => [key, Number([x1 / w, y1 / h, (x2 - x1) / w, (y2 - y1) / h][n].toFixed(6))])), '028 source box ' + title);
}
const chapter = fs.readFileSync(path.join(repo, 'book/crypto-season-01/028-the-ether-sale.md'), 'utf8');
// Parse sections with explicit heading boundaries so paragraph newlines remain intact.
const chapterParts = Object.fromEntries(chapter.split('\n## ').slice(1).map(part => [part.slice(0, part.indexOf('\n')), part.slice(part.indexOf('\n') + 1).trim()]));
const expectedCopy = {
  story: chapterParts['The story'].split('\n\n'),
  eggs: chapterParts['Details in the artwork'].split('\n').map(line => {
    const match = line.match(/^\d+\. \*\*(.*?)\*\* (.*)$/);
    assert(match, '028 chapter clue format');
    return { title: match[1], text: match[2] };
  }),
  sourceNote: chapterParts['Source and art note'].split('\n\n')[0],
};
assert.deepEqual(read('app/cards/content/028.json'), expectedCopy, '028 book/site copy mirror');
assert.equal(expectedCopy.story.length, 4);
assert(fs.readFileSync(path.join(root, 'app/crypto/028/page.js'), 'utf8').includes("permanentRedirect('/cards/the-ether-sale')"), '028 QR target');
console.log(`PASS: ${media.length} contiguous cards and QR sources, ${clues} clues, ${pages} book pages, ${positions} non-overlapping marker positions, ${index.assets.length} media hashes; all 119 earlier clues and 227 earlier images preserved; 028 sources and book/site copy match`);
