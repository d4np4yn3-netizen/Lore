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
const expectedIds = Array.from({ length: 36 }, (_, i) => String(i + 1).padStart(3, '0'));
const mediaIds = media.map(card => card.image.src.match(/\/(\d{3})-/)?.[1]).sort();
const qrIds = fs.readdirSync(path.join(root, 'app/crypto')).filter(id => /^\d{3}$/.test(id)).sort();
const cardSource = fs.readFileSync(path.join(root, 'app/cards/data.js'), 'utf8');
const cardIds = [...cardSource.matchAll(/number:\s*['"](\d{3})\/100['"]/g)].map(m => m[1]).sort();
for (const [label, ids] of Object.entries({ content: contentIds, media: mediaIds, clues: Object.keys(closeups).sort(), QR: qrIds, cards: cardIds })) {
  assert.deepEqual(ids, expectedIds, `${label}: contiguous 001–036`);
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

// Pinned semantic snapshots from remote baseline c8253629dbd15dacbde787c5eec5e67cfc86c09b.
// Removing only the 036 additions must recover every earlier record exactly.
const { '036': latestClues, ...priorCloseups } = closeups;
const { 'rare-pepes': latestMedia, ...priorMedia } = mediaBySlug;
const priorIndex = { ...index, assets: index.assets.filter(asset => asset.pack !== 'display-15.bin') };
const priorDerivatives = { ...derivatives, cards: derivatives.cards.filter(card => card.number !== '036') };
assert.equal(jsonHash(priorCloseups), '4d801b64772f3c66478f616c96e3425c8418aced213ba298e71bac1a7670b353', 'All 150 earlier clue records preserved');
assert.equal(jsonHash(priorMedia), 'b4afe750ae53499e7e31636fb08ae2a39a202addc1cfb81fd6a66f60ead19609', 'All 35 earlier card media records preserved');
assert.equal(jsonHash(priorIndex), 'cec80dab132a0523bbbf4089300db204e27a050beb9cf2c60808d9176c6ef0c7', 'All 290 earlier media index records preserved');
assert.equal(jsonHash(priorDerivatives), '123f409ef55fc4310fab085ef52cf2c3e0069cab5f33599f304d4d6af0d1c463', 'All 35 earlier trim records preserved');

for (const id of ['022', '028', '029', '030', '031', '032', '033', '034', '035', '036']) {
  const added = read('media/' + id + '-derivatives.json');
  assert.equal(added.displayAssets.length, 4 + closeups[id].length, id + ' display assets');
  assert.deepEqual(read('app/cards/content/' + id + '.json').eggs.map(egg => egg.title), added.clues.map(clue => clue.title), id + ' clue order');
  for (const [pack, sha256] of Object.entries(added.previousBundleSHA256)) {
    assert.equal(fileHash(path.join(root, 'media', pack)), sha256, 'Previous bundle ' + pack);
  }
}
assert.equal(read('media/022-derivatives.json').previousAssetsPreserved, 219);
assert.equal(mediaBySlug['buried-fortune'].hashes.artwork, '0f2b071d25d706ca180d3cad4c7c89bff4f4e370eaa32f5b234135282233ce95');
assert.equal(media.filter(card => card.assetOrigin).length, 10, 'Only 022 and 028–036 override original asset origin');
for (const card of media.filter(card => card.assetOrigin)) assert(card.assetOrigin.startsWith('https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/'));
const reader = fs.readFileSync(path.join(root, 'app/components/ReadingRoom.js'), 'utf8');
assert(reader.includes('card.media.assetOrigin || ASSET_ORIGIN'), 'Per-card original asset fallback');
assert.equal((reader.match(/href=\{assetOrigin\+/g) || []).length, 5, 'All original links use per-card asset origin');

const added = read('media/036-derivatives.json');
assert.equal(added.previousAssetsPreserved, priorIndex.assets.length);
assert.equal(added.previousAssetsPreserved, 290);
assert.equal(latestClues.length, 4);
assert.deepEqual(added.displayAssets, index.assets.filter(asset => asset.pack === 'display-15.bin'), '036 index records');
assert.equal(fileHash(path.join(root, 'media/display-15.bin')), added.bundleSHA256, '036 bundle');
assert.equal(latestMedia.hashes.artwork, '6785c45c12c7efb0da14e2cba3307f3001b4bd793942f1cdd7ff7f71fe015f2f', 'Approved 036 artwork');
for (const [source, sha256] of Object.entries(added.sourcesSHA256)) assert.equal(fileHash(path.join(repo, source)), sha256, '036 unchanged original ' + source);
assert.equal(latestMedia.hashes.artwork, added.sourcesSHA256[latestMedia.originalArt]);
assert.equal(latestMedia.hashes.book, added.sourcesSHA256[latestMedia.originalBook]);
const trim = derivatives.cards.find(card => card.number === '036');
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
  assert.deepEqual(display, latestClues[i], '036 clue metadata ' + title);
  const [x1, y1, x2, y2] = box;
  const [w, h] = added.artDimensions;
  assert.deepEqual(display.bbox, Object.fromEntries(['x', 'y', 'w', 'h'].map((key, n) => [key, Number([x1 / w, y1 / h, (x2 - x1) / w, (y2 - y1) / h][n].toFixed(6))])), '036 source box ' + title);
}
const chapter = fs.readFileSync(path.join(repo, 'book/crypto-season-01/036-rare-pepes.md'), 'utf8');
// Parse sections with explicit heading boundaries so paragraph newlines remain intact.
const chapterParts = Object.fromEntries(chapter.split('\n## ').slice(1).map(part => [part.slice(0, part.indexOf('\n')), part.slice(part.indexOf('\n') + 1).trim()]));
const expectedCopy = {
  story: chapterParts['The story'].split('\n\n'),
  eggs: chapterParts['Details in the artwork'].split('\n').map(line => {
    const match = line.match(/^\d+\. \*\*(.*?)\*\* (.*)$/);
    assert(match, '036 chapter clue format');
    return { title: match[1], text: match[2] };
  }),
  sourceNote: chapterParts['Source and art note'].split('\n\n')[0],
};
assert.deepEqual(read('app/cards/content/036.json'), expectedCopy, '036 book/site copy mirror');
assert.equal(expectedCopy.story.length, 5);
assert(fs.readFileSync(path.join(root, 'app/crypto/036/page.js'), 'utf8').includes("permanentRedirect('/cards/rare-pepes')"), '036 QR target');
console.log(`PASS: ${media.length} contiguous cards and QR sources, ${clues} clues, ${pages} book pages, ${positions} non-overlapping marker positions, ${index.assets.length} media hashes; all 150 earlier clues and 290 earlier images preserved; 036 sources and book/site copy match`);

assert(expectedCopy.sourceNote.includes('original issuance record') && expectedCopy.sourceNote.includes('community-archive evidence') && expectedCopy.sourceNote.includes('user-supplied photographs'), '036 primary sources preserved');
assert.equal(expectedCopy.eggs.length, 4);

const experienceSource = fs.readFileSync(path.join(root, 'app/cards/experience.js'), 'utf8');
const yearMetadata = experienceSource.slice(experienceSource.indexOf('export const yearNotes'), experienceSource.indexOf('export const titleCase'));
for (const year of [...cardSource.matchAll(/date:\s*['"][^'"]*?(\d{4})['"]/g)].map(match => Number(match[1]))) {
  assert(yearMetadata.includes(year + ':'), 'Timeline note exists for ' + year);
}
assert(experienceSource.includes("range:'2013 — 2016'"), 'Current chapter range reaches 2016');
assert(fs.readFileSync(path.join(root, 'app/page.js'), 'utf8').includes('years[years.length-1]'), 'Hero year range derives from collection');

const titleCaseFunction = new Function('return ' + experienceSource.match(/^export const titleCase = (.+);$/m)[1])();
assert.equal(titleCaseFunction('THE DAO HACK'), 'The DAO Hack', 'DAO acronym preserved in visible title');
