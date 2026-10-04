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
const expectedIds = Array.from({ length: 33 }, (_, i) => String(i + 1).padStart(3, '0'));
const mediaIds = media.map(card => card.image.src.match(/\/(\d{3})-/)?.[1]).sort();
const qrIds = fs.readdirSync(path.join(root, 'app/crypto')).filter(id => /^\d{3}$/.test(id)).sort();
const cardSource = fs.readFileSync(path.join(root, 'app/cards/data.js'), 'utf8');
const cardIds = [...cardSource.matchAll(/number:\s*['"](\d{3})\/100['"]/g)].map(m => m[1]).sort();
for (const [label, ids] of Object.entries({ content: contentIds, media: mediaIds, clues: Object.keys(closeups).sort(), QR: qrIds, cards: cardIds })) {
  assert.deepEqual(ids, expectedIds, `${label}: contiguous 001–033`);
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

// Pinned semantic snapshots from remote baseline e254f9c71ce96b847dc11bf16318aaf32a174b7a.
// Removing only the 033 additions must recover every earlier record exactly.
const { '033': latestClues, ...priorCloseups } = closeups;
const { 'the-dao-hack': latestMedia, ...priorMedia } = mediaBySlug;
const priorIndex = { ...index, assets: index.assets.filter(asset => asset.pack !== 'display-12.bin') };
const priorDerivatives = { ...derivatives, cards: derivatives.cards.filter(card => card.number !== '033') };
assert.equal(jsonHash(priorCloseups), '31971d0142d1a5bf91033753783fd9eba4a2da7aca698d3e8d3fb3e21602c8f0', 'All 137 earlier clue records preserved');
assert.equal(jsonHash(priorMedia), 'eeaae0472d53d8bb1a38d0d9cd14003b7b57b34e1e9068a3a4c64ce34a9a6b5e', 'All 32 earlier card media records preserved');
assert.equal(jsonHash(priorIndex), 'cd49bb0e02fc9da07fc1b156cddf7ec3847e4458be3e59fade23944b9a26e52a', 'All 265 earlier media index records preserved');
assert.equal(jsonHash(priorDerivatives), 'c5b54baee6f3942e1b1062acdd4cbc1b9d673ed1fc9f8dfaa75dba9a0d19178a', 'All 32 earlier trim records preserved');

for (const id of ['022', '028', '029', '030', '031', '032', '033']) {
  const added = read('media/' + id + '-derivatives.json');
  assert.equal(added.displayAssets.length, 4 + closeups[id].length, id + ' display assets');
  assert.deepEqual(read('app/cards/content/' + id + '.json').eggs.map(egg => egg.title), added.clues.map(clue => clue.title), id + ' clue order');
  for (const [pack, sha256] of Object.entries(added.previousBundleSHA256)) {
    assert.equal(fileHash(path.join(root, 'media', pack)), sha256, 'Previous bundle ' + pack);
  }
}
assert.equal(read('media/022-derivatives.json').previousAssetsPreserved, 219);
assert.equal(mediaBySlug['buried-fortune'].hashes.artwork, '0f2b071d25d706ca180d3cad4c7c89bff4f4e370eaa32f5b234135282233ce95');
assert.equal(media.filter(card => card.assetOrigin).length, 7, 'Only 022, 028, 029, 030, 031, 032 and 033 override original asset origin');
for (const card of media.filter(card => card.assetOrigin)) assert(card.assetOrigin.startsWith('https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/'));
const reader = fs.readFileSync(path.join(root, 'app/components/ReadingRoom.js'), 'utf8');
assert(reader.includes('card.media.assetOrigin || ASSET_ORIGIN'), 'Per-card original asset fallback');
assert.equal((reader.match(/href=\{assetOrigin\+/g) || []).length, 5, 'All original links use per-card asset origin');

const added = read('media/033-derivatives.json');
assert.equal(added.previousAssetsPreserved, priorIndex.assets.length);
assert.equal(added.previousAssetsPreserved, 265);
assert.equal(latestClues.length, 4);
assert.deepEqual(added.displayAssets, index.assets.filter(asset => asset.pack === 'display-12.bin'), '033 index records');
assert.equal(fileHash(path.join(root, 'media/display-12.bin')), added.bundleSHA256, '033 bundle');
assert.equal(latestMedia.hashes.artwork, 'f93c3d9bed56839609e27adc0919a3d3dd7680415e048b0d8ad3523ea26e63d5', 'Approved 033 artwork');
for (const [source, sha256] of Object.entries(added.sourcesSHA256)) assert.equal(fileHash(path.join(repo, source)), sha256, '033 unchanged original ' + source);
assert.equal(latestMedia.hashes.artwork, added.sourcesSHA256[latestMedia.originalArt]);
assert.equal(latestMedia.hashes.book, added.sourcesSHA256[latestMedia.originalBook]);
const trim = derivatives.cards.find(card => card.number === '033');
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
  assert.deepEqual(display, latestClues[i], '033 clue metadata ' + title);
  const [x1, y1, x2, y2] = box;
  const [w, h] = added.artDimensions;
  assert.deepEqual(display.bbox, Object.fromEntries(['x', 'y', 'w', 'h'].map((key, n) => [key, Number([x1 / w, y1 / h, (x2 - x1) / w, (y2 - y1) / h][n].toFixed(6))])), '033 source box ' + title);
}
const chapter = fs.readFileSync(path.join(repo, 'book/crypto-season-01/033-the-dao-hack.md'), 'utf8');
// Parse sections with explicit heading boundaries so paragraph newlines remain intact.
const chapterParts = Object.fromEntries(chapter.split('\n## ').slice(1).map(part => [part.slice(0, part.indexOf('\n')), part.slice(part.indexOf('\n') + 1).trim()]));
const expectedCopy = {
  story: chapterParts['The story'].split('\n\n'),
  eggs: chapterParts['Details in the artwork'].split('\n').map(line => {
    const match = line.match(/^\d+\. \*\*(.*?)\*\* (.*)$/);
    assert(match, '033 chapter clue format');
    return { title: match[1], text: match[2] };
  }),
  sourceNote: chapterParts['Source and art note'].split('\n\n')[0],
};
assert.deepEqual(read('app/cards/content/033.json'), expectedCopy, '033 book/site copy mirror');
assert.equal(expectedCopy.story.length, 4);
assert(fs.readFileSync(path.join(root, 'app/crypto/033/page.js'), 'utf8').includes("permanentRedirect('/cards/the-dao-hack')"), '033 QR target');
console.log(`PASS: ${media.length} contiguous cards and QR sources, ${clues} clues, ${pages} book pages, ${positions} non-overlapping marker positions, ${index.assets.length} media hashes; all 137 earlier clues and 265 earlier images preserved; 033 sources and book/site copy match`);

assert(expectedCopy.sourceNote.includes('17 June alert') && expectedCopy.sourceNote.includes('20 July completion notice'), '033 primary sources preserved');
assert.equal(expectedCopy.eggs.length, 4);

const experienceSource = fs.readFileSync(path.join(root, 'app/cards/experience.js'), 'utf8');
const yearMetadata = experienceSource.slice(experienceSource.indexOf('export const yearNotes'), experienceSource.indexOf('export const titleCase'));
for (const year of [...cardSource.matchAll(/date:\s*['"][^'"]*?(\d{4})['"]/g)].map(match => Number(match[1]))) {
  assert(yearMetadata.includes(year + ':'), 'Timeline note exists for ' + year);
}
assert(experienceSource.includes("range:'2013 — 2016'"), 'Current chapter range reaches 2016');
assert(fs.readFileSync(path.join(root, 'app/page.js'), 'utf8').includes('years[years.length-1]'), 'Hero year range derives from collection');
