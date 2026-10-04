#!/usr/bin/env python3
"""Create the additive 032 web derivatives without altering earlier media."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'
ART = 'cards/crypto/season-01/ethereum-goes-live-master-032/art.png'
FRONT = 'cards/crypto/season-01/ethereum-goes-live-master-032/LORE-Crypto-032-Ethereum-Goes-Live-Mythic-Print-v1.png'
BOOK = 'book/crypto-season-01/proofs/032-ethereum-goes-live-full-art-spread-v1.pdf'
ART_SHA = '5db2bd45176367f74c595925fecb3d537b5a493966ca02850178903563422ef0'
PACK = 'display-11.bin'
CROPS = [
    ('The Frontier sign.', (290, 513, 450, 577), 'FRONTIER gantry sign naming Ethereum’s first live release'),
    ('The genesis zero.', (488, 575, 580, 656), 'Illuminated zero at the central pipe junction symbolising the genesis block'),
    ('The 5,000 limit.', (912, 597, 1060, 696), 'BLOCK GAS LIMIT 5,000 sign recording the initial Frontier thawing restriction'),
    ('The unfinished landmark.', (290, 2, 584, 466), 'Unfinished concrete-panel Ethereum-shaped tower with open floors and scaffolding'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def save(image, relative):
    dest = SITE / 'public' / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, 'WEBP', quality=90, method=6)
    return {'src': '/' + relative, 'width': image.width, 'height': image.height}

assert sha(ROOT / ART) == ART_SHA, 'Selected art changed'
source_hashes = {p: sha(ROOT / p) for p in (ART, FRONT, BOOK)}
art = Image.open(ROOT / ART).convert('RGB')
front = Image.open(ROOT / FRONT).convert('RGB')
assert art.size == (1060, 1484)
assert front.size == (816, 1110)
index = read(SITE / 'media/index.json')
old_entries = [entry for entry in index['assets'] if entry['pack'] != PACK]
old_count = len(old_entries)
assert old_count > 0, 'Existing media must be preserved'
old_pack_hashes = {name: sha(SITE / 'media' / name) for name in {entry['pack'] for entry in old_entries}}
card_image = save(front.crop((36, 36, 780, 1074)).resize((600, 837), Image.Resampling.LANCZOS), 'archive/032-web-card.webp')
art_image = save(art, 'archive/032-art.webp')
pages = []
with tempfile.TemporaryDirectory(prefix='lore-032-pages-') as temp:
    prefix = Path(temp) / 'page'
    subprocess.run(['pdftoppm', '-png', '-scale-to-y', '1100', '-scale-to-x', '-1', str(ROOT / BOOK), str(prefix)], check=True)
    rendered = sorted(Path(temp).glob('page-*.png'))
    assert len(rendered) == 2, 'Book spread must contain two pages'
    for i, path in enumerate(rendered, 1):
        image = Image.open(path).convert('RGB')
        assert image.size == (778, 1100), f'Unexpected book preview dimensions {image.size}'
        pages.append(save(image, f'archive/032-page-{i}.webp'))
closeups = []
for i, (_, box, alt) in enumerate(CROPS, 1):
    crop = art.crop(box)
    crop.thumbnail((700, 500), Image.Resampling.LANCZOS)
    asset = save(crop, f'closeups/032-{i:02}.webp')
    closeups.append({**asset, 'alt': alt, 'bbox': dict(zip(('x', 'y', 'w', 'h'), (
        round(box[0] / art.width, 6), round(box[1] / art.height, 6),
        round((box[2] - box[0]) / art.width, 6), round((box[3] - box[1]) / art.height, 6))))})
media = read(SITE / 'app/cards/media.json')
origin = media.get('ethereum-goes-live', {}).get('assetOrigin', 'https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/main/')
media['ethereum-goes-live'] = {'image': card_image, 'artwork': art_image, 'pages': pages,
    'originalArt': ART, 'originalBook': BOOK, 'assetOrigin': origin,
    'hashes': {'image': source_hashes[FRONT], 'artwork': source_hashes[ART], 'book': source_hashes[BOOK]}}
write(SITE / 'app/cards/media.json', media)
clue_data = read(SITE / 'app/cards/closeups.json')
clue_data['032'] = closeups
write(SITE / 'app/cards/closeups.json', clue_data)
assets = sorted([card_image, art_image, *pages, *closeups], key=lambda a: a['src'])
entries = []
offset = 0
with (SITE / 'media' / PACK).open('wb') as pack:
    for asset in assets:
        relative = asset['src'].lstrip('/')
        content = (SITE / 'public' / relative).read_bytes()
        entries.append({'path': relative, 'pack': PACK, 'offset': offset, 'length': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
        pack.write(content)
        offset += len(content)
index['assets'] = old_entries + entries
write(SITE / 'media/index.json', index)
derivatives = read(SITE / 'web-card-derivatives.json')
derivatives['cards'] = [card for card in derivatives['cards'] if card['number'] != '032']
derivatives['cards'].append({'number': '032', 'source': FRONT, 'sourceSHA256': source_hashes[FRONT],
    'sourceDimensions': list(front.size), 'trimBoxXYWH': [36, 36, 744, 1038],
    'webPreview': 'site/public/archive/032-web-card.webp', 'webDimensions': [600, 837],
    'webSHA256': sha(SITE / 'public/archive/032-web-card.webp'), 'masterUnchanged': True})
write(SITE / 'web-card-derivatives.json', derivatives)
assert old_pack_hashes == {name: sha(SITE / 'media' / name) for name in old_pack_hashes}, 'Old bundle changed'
assert source_hashes == {p: sha(ROOT / p) for p in source_hashes}, 'Original master changed'
write(SITE / 'media/032-derivatives.json', {'card': '032', 'purpose': 'Separately saved website-only derivatives from exact selected original files.',
    'sourcesSHA256': source_hashes, 'artDimensions': list(art.size), 'webpEncoding': {'quality': 90, 'method': 6},
    'printTrimBoxXYWH': [36, 36, 744, 1038], 'bookRasterization': 'Poppler pdftoppm, full pages, 1100 pixels high',
    'clues': [{'title': title, 'sourceBoxXYXY': list(box), **asset} for (title, box, _), asset in zip(CROPS, closeups)],
    'displayAssets': entries, 'bundleSHA256': sha(SITE / 'media' / PACK), 'previousAssetsPreserved': old_count,
    'previousBundleSHA256': old_pack_hashes, 'originalMastersUnchanged': True})
print(f'032 media ready: {len(entries)} new images, {len(index["assets"])} total; all {old_count} earlier images and bundles preserved')
