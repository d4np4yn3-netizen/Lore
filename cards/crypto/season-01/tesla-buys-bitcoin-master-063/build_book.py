"""Build the two-page 063 book from verified text and frozen final art.

Page geometry and typography are preserved exactly from the 062 builder at a744fdb45b6a7c221973077ebfc9536ca408a3c3.
Only chapter identifiers, content, source art and crop boxes differ. Five actual-art detail entries are used.

Layout is preserved from 050, which inherited 048 at 9e71c54b64212f955e6f85eaf40b5ab9f934ac30. Usage: python3 build_book.py --content-only
or python3 build_book.py after art.png and art-provenance.json are supplied.
"""
from pathlib import Path
import argparse
import json
import html
import hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import fitz

B = Path(__file__).resolve().parent
ART = B / 'art.png'
authoring = json.loads((B / 'authoring-content.json').read_text())
story = authoring['story']
eggs = authoring['eggs']
sources = authoring['sources']
art_note = authoring['art_note']
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '063.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '063-tesla-buys-bitcoin.md').write_text('# 063 - Tesla Buys Bitcoin\n\n08 FEB 2021 / TESLA / UNCOMMON\n\nBITCOIN ON THE BALANCE SHEET.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

parser = argparse.ArgumentParser()
parser.add_argument('--content-only', action='store_true')
args = parser.parse_args()
if args.content_only:
    print(json.dumps({'story_words': sum(len(p.split()) for p in story), 'clue_count': len(eggs), 'source_count': len(sources)}))
    raise SystemExit(0)

art_provenance = json.loads((B / 'art-provenance.json').read_text())
ART_SHA256 = art_provenance['sha256']
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
assert art_provenance.get('final_input_confirmed', art_provenance.get('approval_condition_met')) is True
FONTS = B / 'source/fonts'
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-063-Tesla-Buys-Bitcoin-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 063 - Tesla Buys Bitcoin')
c.setAuthor('HISTROVE')
iw, ih = Image.open(ART).size
scale = min(W / iw, H / ih)
c.setFillColor(HexColor('#0B0B0B'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.drawImage(ImageReader(str(ART)), (W - iw * scale) / 2, (H - ih * scale) / 2, width=iw * scale, height=ih * scale)
c.showPage()
c.setFillColor(HexColor('#F5F2EB'))
c.rect(0, 0, W, H, fill=1, stroke=0)

def label(txt, x, y, size=9, color='#886615'):
    c.setFillColor(HexColor(color))
    c.setFont('DVB', size)
    c.drawString(x, y, txt)

def para(txt, x, y, width, fs=9.3, leading=13.8):
    p = Paragraph(txt, ParagraphStyle('p', fontName='DV', fontSize=fs, leading=leading, textColor=HexColor('#171717')))
    _, height = p.wrap(width, H)
    p.drawOn(c, x, y - height)
    return y - height - 10

label('HISTROVE / CRYPTO SEASON ONE', 43, H - 39, 9, '#0B0B0B')
c.setStrokeColor(HexColor('#886615'))
c.line(43, H - 57, W - 43, H - 57)
label('TESLA BUYS BITCOIN', 43, H - 102, 22, '#0B0B0B')
label('063 / 08 FEB 2021 / TESLA / UNCOMMON', 43, H - 124, 8, '#5A574F')
label('BITCOIN ON THE BALANCE SHEET.', 43, H - 153, 14)
y = H - 188
for p in story:
    y = para(html.escape(p), 43, y, 242)
z = H - 188
label('DETAILS IN THE ART', 307, z, 9, '#0B0B0B')
z -= 20
for i, e in enumerate(eggs, 1):
    label(f"{i:02}  {e['title']}", 307, z, 7.8)
    z = para(html.escape(e['text']), 307, z - 11, 242, 8.7, 12.5)
label('SOURCE & ART NOTE', 307, z - 8, 8, '#0B0B0B')
z = para(source_pdf, 307, z - 21, 242, 7.2, 10.3)
assert min(y, z) > 72, (y, z)
c.line(43, 57, W - 43, 57)
label('063 / TESLA BUYS BITCOIN', 43, 40, 7.5, '#5A574F')
label('126', W - 62, 40, 7.5, '#5A574F')
c.save()
doc = fitz.open(out)
assert len(doc) == 2
for i, p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(str(B / f'book-page-{i+1}.png'))
a = Image.open(B / 'book-page-1.png')
b = Image.open(B / 'book-page-2.png')
sheet = Image.new('RGB', (a.width + b.width, a.height), 'white')
sheet.paste(a, (0, 0))
sheet.paste(b, (a.width, 0))
sheet.save(B / 'HISTROVE-063-Tesla-Buys-Bitcoin-Book-Spread.png')
crop_input = json.loads((B / 'crop-input.json').read_text())
assert crop_input['source_dimensions'] == [iw, ih], crop_input
boxes = crop_input['boxes']
assert len(boxes) == len(eggs) == 5
assert all(0 <= x0 < x1 <= iw and 0 <= y0 < y1 <= ih for x0, y0, x1, y1 in boxes)
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'normalized_boxes': [[round(x0/iw, 8), round(y0/ih, 8), round(x1/iw, 8), round(y1/ih, 8)] for x0, y0, x1, y1 in boxes], 'coordinate_system': 'Top-left origin; normalized [x0,y0,x1,y1] fractions of full raw artwork', 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'063-detail-{n}.png')
qa = {
    'page_count': len(doc), 'page_size_points': [W,H],
    'source_art_dimensions_px': [iw,ih], 'source_art_sha256': ART_SHA256,
    'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256,
    'native_effective_ppi': 72/scale,
    'native_resolution_note': f'{iw} x {ih} raw pixels at proportional A4 fit; {72/scale:.2f} effective PPI. Upsampling is not native resolution.',
    'art_fit': 'Contain proportional full native artwork with black edge bars; unchanged 062 layout',
    'story_column_bottom_points': y, 'clues_column_bottom_points': z,
    'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources),
    'story_word_count': sum(len(p.split()) for p in story),
    'event_date': '08 FEB 2021', 'rarity': 'uncommon', 'collector_number': '063/100',
    'card_phrase': 'BITCOIN ON THE BALANCE SHEET.',
    'phrase_status': 'Approved original editorial copy',
    'linked_source_annotations': len(doc[1].get_links()),
    'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'visual_review': 'Pending inspection of rendered pages',
    'physical_print_acceptance': 'Not claimed',
    'rights_clearance': 'Not established; artwork approval does not imply rights clearance',
    'layout_reference': json.loads((B/'source/layout-reference.json').read_text()),
    'source_verification_date': '2026-10-13',
    'book_approval_status': 'Publication authorized; technical QA separate',
    'publication_authorized': True,
    'content_review': '8 February 2021 is the public filing date; January 2021 is the investment-policy change; aggregate $1.50 billion purchase followed the policy change but precise purchase day is not asserted; Note 23 is Subsequent Events; payments remained a future plan; fictional professor and FUTURE envelope are cross-card motifs; stylized documents are not authentic facsimiles; rights review unresolved.'
}
(B/'book-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))

