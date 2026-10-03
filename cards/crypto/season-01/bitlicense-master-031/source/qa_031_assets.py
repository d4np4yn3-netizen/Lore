from pathlib import Path
import base64, hashlib, json, sys, xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'lore-022/prep/python-deps'))
import zxingcpp

ROOT = Path(__file__).resolve().parent.parent
NAME = 'LORE-Crypto-031-BitLicense-Rare-Print-v1'
ART_SHA = 'edac6ab5c807165ccfa7c18ed5a2c1a7205ab45621b6e160e5ab2ee3cdf5e8be'
PAYLOAD = 'https://lore-site-v1.vercel.app/crypto/031/'
art = (ROOT / 'art.png').read_bytes()
assert hashlib.sha256(art).hexdigest() == ART_SHA
assert art == (ROOT.parent / 'LORE-Crypto-031-BitLicense-Art-Review-v8.png').read_bytes()
a = ET.parse(ROOT / 'source/rare.svg').getroot()
b = ET.parse(ROOT / (NAME + '.svg')).getroot()
nodes = {n.get('id'): n for n in b.iter() if n.get('id')}
href = '{http://www.w3.org/1999/xlink}href'
assert base64.b64decode(nodes['card-illustration'].get(href).split(',')[1]) == art
fields = {'creator-name': 'NEW YORK', 'title-line-1': 'BITLICENSE', 'title-line-2': '', 'moment-context': 'RULES FOR A NEW FRONTIER', 'moment-number': '24 JUN 2015', 'set-number': 'CRYPTO • SEASON 01 • 031/100', 'qr-caption': 'SCAN TO DISCOVER'}
for key, value in fields.items():
    assert (nodes[key].text or '') == value
for root in (a, b):
    for n in root.iter():
        if n.get('id') in fields:
            n.text = 'NORMALIZED'
        if n.get('id') == 'card-illustration':
            n.set(href, 'NORMALIZED')
        if n.get('id') == 'moment-qr':
            for child in list(n):
                n.remove(child)
            n.set('viewBox', 'NORMALIZED')
def tree(n):
    return n.tag, tuple(sorted(n.attrib.items())), (n.text or '').strip(), tuple(tree(c) for c in n)
assert tree(a) == tree(b), 'Geometry, logo or template changed'
assert nodes['locked-crypto-front'].get('transform') == 'translate(46.515 48.921) scale(0.8033)'
assert nodes['cut-line'].get('width') == '744' and nodes['cut-line'].get('height') == '1038'
assert nodes['safe-area'].get('width') == '684' and nodes['safe-area'].get('height') == '981'
qr = {}
for path in (ROOT / (NAME + '.png'), ROOT / 'qa/front-300dpi.png'):
    im = Image.open(path)
    assert im.size == (816, 1110)
    qr[path.name] = [v.text for v in zxingcpp.read_barcodes(im)]
    assert qr[path.name] == [PAYLOAD]
png = Image.open(ROOT / (NAME + '.png'))
assert all(abs(v - 300) < 0.01 for v in png.info['dpi'])
card = PdfReader(ROOT / (NAME + '.pdf'))
assert len(card.pages) == 1
assert list(card.pages[0].mediabox) == [0, 0, 195.84, 266.4]
assert list(card.pages[0].trimbox) == [8.64, 8.64, 187.2, 257.76]
assert card.pages[0].images[0].image.convert('RGB').tobytes() == png.convert('RGB').tobytes()
book = PdfReader(ROOT / '031-bitlicense-full-art-spread-v1.pdf')
assert len(book.pages) == 2
assert book.pages[0].images[0].image.convert('RGB').tobytes() == Image.open(ROOT / 'art.png').convert('RGB').tobytes()
text = book.pages[1].extract_text()
assert all(s in text for s in ('BITLICENSE', 'RULES FOR A NEW FRONTIER', 'Part 200', 'Circle', 'editorial caption'))
assert all(s not in text for s in ('Trezor', 'Mastercoin junction', 'rail-carriage', 'PROPOSED', 'REVIEW PROOF', 'review proof'))
qa = {'status': 'APPROVED_PUBLICATION_ASSETS_AWAITING_LIVE_VERIFICATION', 'original_art_sha256': ART_SHA, 'artwork_bytes_preserved': True, 'svg_embedded_art_matches': True, 'book_embedded_art_pixels_match': True, 'card_pdf_embedded_png_pixels_match': True, 'locked_template_geometry_fonts_logo_unchanged': True, 'qr_decodes': qr, 'qr_live_status': 'NOT_YET_PUBLISHED', 'card_dimensions_px': [816,1110], 'dpi': 300, 'trim_px': [744,1038], 'safe_px': [684,981], 'book_pages': 2, 'book_page_dimensions_pt': list(map(float,book.pages[0].mediabox)), 'card_and_book_pages_visually_checked': True, 'folder_outline_and_entrance_sign_clear_of_title_and_qr': True, 'actual_art_details': ['The application folder.', 'The New York outline.', 'One State Street.'], 'caption_status': 'APPROVED_EDITORIAL_CAPTION_NOT_HISTORICAL_QUOTE', 'print_release': False, 'book_reproduction_release': False, 'physical_qr_scan_test': False, 'native_art_dimensions': [1060,1484], 'full_page_art_ppi_approx': 127, 'files': {p.name: {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in ROOT.iterdir() if p.is_file() and p.suffix in ('.png','.pdf','.svg','.md')}}
(ROOT / 'publication-assets-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
