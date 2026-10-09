"""Build the two-page 051 book from verified text and frozen final art.

Page geometry and typography are preserved exactly from the 050 builder.
Only chapter identifiers, content, source art and crop boxes differ.

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
(B / '051.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '051-lightning-torch.md').write_text('# 051 - Lightning Torch\n\n19 JAN 2019 / BITCOIN / COMMON\n\nPASS IT ON.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

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
FONTS = next(p for p in [B.parents[2] / 'master/front-v3/source/fonts', B.parent / 'build-repo/cards/master/front-v3/source/fonts', B / 'canonical-dependencies/cards/master/front-v3/source/fonts', B / 'source/fonts'] if p.is_dir())
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-051-Lightning-Torch-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 051 - Lightning Torch')
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
label('LIGHTNING TORCH', 43, H - 102, 22, '#0B0B0B')
label('051 / 19 JAN 2019 / BITCOIN / COMMON', 43, H - 124, 8, '#5A574F')
label('PASS IT ON.', 43, H - 153, 14)
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
label('051 / LIGHTNING TORCH', 43, 40, 7.5, '#5A574F')
label('102', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-051-Lightning-Torch-Book-Spread.png')
reference_boxes = [[211, 598, 294, 728], [135, 552, 225, 635], [49, 598, 220, 736], [481, 555, 589, 750]]
boxes = [[round(x * iw / 1060) if k % 2 == 0 else round(x * ih / 1484) for k, x in enumerate(box)] for box in reference_boxes]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'051-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; unchanged 048 layout', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '19 JAN 2019', 'rarity': 'common', 'collector_number': '051/100', 'card_phrase': 'PASS IT ON.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'logo_legal_clearance': 'Not established; artwork approval does not imply rights clearance', 'reference_layout': 'cards/crypto/season-01/the-pineapple-fund-master-050/build_book.py', 'reference_050_build_sha256': '8cfc699e49adb076416cdd941545c370f7c048b71c3c89cab6215daf6dca4276', 'ancestor_048_layout_commit': '9e71c54b64212f955e6f85eaf40b5ab9f934ac30', 'reference_048_build_sha256': '6125ff644b42c1be45718389f636ad5276868b3979eebf14e364774f2f4e3418'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))


