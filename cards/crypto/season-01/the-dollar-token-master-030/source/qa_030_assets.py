from pathlib import Path
import base64, hashlib, json, sys, xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'lore-022/prep/python-deps'))
import zxingcpp

ROOT = Path(__file__).resolve().parent.parent
NAME = 'LORE-Crypto-030-The-Dollar-Token-Uncommon-Print-v1'
ART_SHA = '0cc86230d8e5a6aa056351cd3d694f807b2f98c838e00bffd9f35b2a2eb33be9'
PAYLOAD = 'https://lore-site-v1.vercel.app/crypto/030/'
art = (ROOT / 'art.png').read_bytes()
assert hashlib.sha256(art).hexdigest() == ART_SHA
assert art == (ROOT.parent / 'LORE-Crypto-030-The-Dollar-Token-Art-Final-v6.png').read_bytes()
a = ET.parse(ROOT / 'source/uncommon.svg').getroot()
b = ET.parse(ROOT / (NAME + '.svg')).getroot()
nodes = {n.get('id'): n for n in b.iter() if n.get('id')}
href = '{http://www.w3.org/1999/xlink}href'
assert base64.b64decode(nodes['card-illustration'].get(href).split(',')[1]) == art
fields = {'creator-name': 'REALCOIN', 'title-line-1': 'THE DOLLAR', 'title-line-2': 'TOKEN', 'moment-context': 'THE DOLLAR GOES DIGITAL.', 'moment-number': '06 OCT 2014', 'set-number': 'CRYPTO • SEASON 01 • 030/100', 'qr-caption': 'SCAN TO DISCOVER'}
for key, value in fields.items():
    assert nodes[key].text == value
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
book = PdfReader(ROOT / '030-the-dollar-token-full-art-spread-v1.pdf')
assert len(book.pages) == 2
assert book.pages[0].images[0].image.convert('RGB').tobytes() == Image.open(ROOT / 'art.png').convert('RGB').tobytes()
text = book.pages[1].extract_text()
assert all(s in text for s in ('THE DOLLAR TOKEN', 'THE DOLLAR GOES DIGITAL.', 'Realcoin', '20 November 2014', '007', 'editorial caption'))
assert all(s not in text for s in ('Trezor', 'Mastercoin junction', 'rail-carriage'))
qa = {'status': 'CHECKED_PROOF_AWAITING_PARENT_REVIEW_AND_LIVE_PUBLICATION', 'original_art_sha256': ART_SHA, 'artwork_bytes_preserved': True, 'svg_embedded_art_matches': True, 'book_embedded_art_pixels_match': True, 'card_pdf_embedded_png_pixels_match': True, 'locked_template_geometry_fonts_logo_unchanged': True, 'qr_decodes': qr, 'qr_live_status': 'NOT_YET_PUBLISHED', 'card_dimensions_px': [816,1110], 'dpi': 300, 'trim_px': [744,1038], 'safe_px': [684,981], 'book_pages': 2, 'book_page_dimensions_pt': list(map(float,book.pages[0].mediabox)), 'card_and_book_pages_visually_checked': True, 'plane_visible_clear_of_logo_and_header': True, 'paper_plane_art_box_xyxy_approx': [649,126,691,154], 'actual_art_details': ['The Realcoin clasp.', 'The dollar entry.', 'The rising seal.', 'The paper plane.'], 'caption_status': 'NEW_EDITORIAL_CAPTION_NOT_HISTORICAL_QUOTE', 'print_release': False, 'book_reproduction_release': False, 'physical_qr_scan_test': False, 'native_art_dimensions': [1060,1484], 'full_page_art_ppi_approx': 127, 'files': {p.name: {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in ROOT.iterdir() if p.is_file() and p.suffix in ('.png','.pdf','.svg','.md')}}
(ROOT / 'publication-assets-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
