"""Check the recovered 039 release without regenerating its approved assets."""
from pathlib import Path
import argparse
import base64
import hashlib
import io
import json
import xml.etree.ElementTree as ET
import fitz
from PIL import Image
import zxingcpp

HERE = Path(__file__).resolve().parent
MASTER = HERE.parent
REPO = MASTER.parents[3]
EXPECTED_ART = 'c6944000f8ff929d6d793db39aeb994e3befc2300a554e0e2f6a7279f7c79239'
PAYLOAD = 'https://lore-site-v1.vercel.app/crypto/039/'
BASE = MASTER / 'LORE-Crypto-039-Behind-the-Chair-Common-Print-v1'
BOOK = REPO / 'book/crypto-season-01/proofs/039-behind-the-chair-full-art-spread-v1.pdf'
CHAPTER = REPO / 'book/crypto-season-01/039-behind-the-chair.md'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def decode(im):
    values = [r.text for r in zxingcpp.read_barcodes(im)]
    assert PAYLOAD in values, values
    return values

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--report', type=Path, default=MASTER / 'publication-assets-qa.json')
args = parser.parse_args()
art = Image.open(MASTER / 'art.png').convert('RGB')
card = Image.open(BASE.with_suffix('.png'))
assert sha(MASTER / 'art.png') == EXPECTED_ART
assert art.size == (1060, 1484)
assert card.size == (816, 1110)
assert all(abs(v - 300) < 0.01 for v in card.info['dpi'])
png_qr = decode(card)

svg = ET.parse(BASE.with_suffix('.svg')).getroot()
nodes = {n.get('id'): n for n in svg.iter() if n.get('id')}
assert nodes['locked-crypto-front'].get('transform') == 'translate(46.515 48.921) scale(0.8033)'
assert nodes['moment-context'].get('font-size') == '25'
assert nodes['moment-context'].get('font-weight') == '700'
assert nodes['rarity-label'].text == 'COMMON'
assert nodes['moment-number'].text == '12 JUL 2017'
assert nodes['creator-name'].text == 'BITCOIN'
assert nodes['title-line-1'].text == 'BEHIND'
assert nodes['title-line-2'].text == 'THE CHAIR'
assert nodes['moment-context'].text == 'BUY BITCOIN.'
assert nodes['qr-caption'].text == 'SCAN TO DISCOVER'
embedded_art = base64.b64decode(nodes['card-illustration'].get('{http://www.w3.org/1999/xlink}href').split(',', 1)[1])
assert hashlib.sha256(embedded_art).hexdigest() == EXPECTED_ART
assert [float(nodes['cut-line'].get(k)) for k in ('width', 'height')] == [744, 1038]
assert [float(nodes['safe-area'].get(k)) for k in ('width', 'height')] == [684, 981]

card_pdf = fitz.open(BASE.with_suffix('.pdf'))
assert len(card_pdf) == 1
embedded_card = fitz.Pixmap(card_pdf, card_pdf[0].get_images()[0][0])
assert embedded_card.samples == card.convert('RGB').tobytes()
render = card_pdf[0].get_pixmap(dpi=300)
pdf_qr = decode(Image.frombytes('RGB', (render.width, render.height), render.samples))
book = fitz.open(BOOK)
assert len(book) == 2
assert all(abs(p.rect.width - 595.27559) < 0.01 and abs(p.rect.height - 841.88976) < 0.01 for p in book)
embedded_book_art = fitz.Pixmap(book, book[0].get_images()[0][0])
assert embedded_book_art.width == 1060 and embedded_book_art.height == 1484
assert embedded_book_art.samples == art.tobytes()

copy = json.loads((HERE / 'approved-copy.json').read_text())
blocks = book[1].get_text('blocks')
normalize = lambda value: ' '.join(value.split())
assert copy['story'] == [normalize(b[4]) for b in blocks[4:9]]
for i, detail in enumerate(copy['details']):
    assert detail['title'] == normalize(blocks[10 + 2*i][4]).split(' ', 1)[1]
    assert detail['body'] == normalize(blocks[11 + 2*i][4])
assert copy['sourceAndArtNote'] == normalize(blocks[21][4])
chapter = CHAPTER.read_text()
for text in copy['story'] + [d['body'] for d in copy['details']] + [copy['sourceAndArtNote']]:
    assert text in chapter
assert sha(BOOK) == copy['provenance']['copySourceSha256']

report = {
    'status': 'pass',
    'nativeArtSha256': EXPECTED_ART,
    'nativeArtDimensions': list(art.size),
    'nativeArtPixelsPreservedInBookPdf': True,
    'nativeArtBytesPreservedInSvg': True,
    'approvedCardPixelsPreservedInPrintPdf': True,
    'cardPngQrDecoded': png_qr,
    'cardPdfRenderedAt300DpiQrDecoded': pdf_qr,
    'canvasPx': list(card.size),
    'dpi': card.info['dpi'],
    'trimPx': [744, 1038],
    'safePx': [684, 981],
    'transform': nodes['locked-crypto-front'].get('transform'),
    'phraseTypography': {'size': 25, 'weight': 700},
    'bookPages': 2,
    'bookPageSize': 'A4',
    'bookNativeArtPpi': 1484 / (297 / 25.4),
    'bookPhysicalReproductionApproved': False,
    'storyParagraphsVerbatim': len(copy['story']),
    'cluesVerbatim': len(copy['details']),
    'sourceAndArtNoteVerbatim': True,
    'hashes': {str(p.relative_to(REPO)): sha(p) for p in [MASTER/'art.png', BASE.with_suffix('.png'), BASE.with_suffix('.svg'), BASE.with_suffix('.pdf'), BOOK, CHAPTER]},
}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
