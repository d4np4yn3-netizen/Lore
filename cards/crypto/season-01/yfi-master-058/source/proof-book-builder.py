"""Build a review-only 058 book using the canonical 094 drawing block.
The full selected v14 lighting-reviewed raw artwork is embedded losslessly, without crop or overlay.
This is not final artwork approval and does not authorize publication.
"""
from pathlib import Path
import json, html, hashlib
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
B=Path(__file__).resolve().parent
ART=B.parent/'058-the-empty-throne-art-v14-receipt-on-ledger.png'
ART_SHA256='1fc66e1930fc1ca0e03ee69cde45328336eea84687f6a5f08e7f88f1a190aee5'
TEMPLATE_SHA256='45b535e413ea2f93f38053230d969c473a6d4b83b0b42d09614577a2394425ef'
assert hashlib.sha256(ART.read_bytes()).hexdigest()==ART_SHA256
assert Image.open(ART).size==(1060,1484)
assert hashlib.sha256((B/'source/template-094-build_book.py').read_bytes()).hexdigest()==TEMPLATE_SHA256
authoring=json.loads((B/'authoring-content.json').read_text())
verification=json.loads((B/'source-verification.json').read_text())
story=authoring['story']; eggs=authoring['eggs']; sources=authoring['sources']; art_note=authoring['art_note']
assert len(eggs)==4
source_note='Sources: '+'; '.join(f"[{s['title']}]({s['url']})" for s in sources)+'. '+art_note
source_pdf='Sources: '+'; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources)+'. '+html.escape(art_note)
FONTS=B.parents[1]/'card087-release/assets/cards/crypto/season-01/the-arbitrum-airdrop-master-087/source/fonts'
for name,filename in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/filename)))
# BEGIN EXACT CANONICAL DRAWING BLOCK, IDENTIFIERS ONLY ADAPTED
W, H = A4
out = B / 'HISTROVE-058-YFI-Book-PROOF.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 058 - YFI - PROOF')
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
label('YFI', 43, H - 102, 22, '#0B0B0B')
label('058 / 17 JUL 2020 / YEARN FINANCE / COMMON', 43, H - 124, 8, '#5A574F')
label('NO RESERVED SEAT.', 43, H - 153, 14)
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
label('058 / YFI', 43, 40, 7.5, '#5A574F')
label('116', W - 62, 40, 7.5, '#5A574F')
c.save()
# END EXACT CANONICAL DRAWING BLOCK
doc=fitz.open(out)
assert len(doc)==2
for i,p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(B/f'book-page-{i+1}.png'))
a=Image.open(B/'book-page-1.png'); b=Image.open(B/'book-page-2.png')
sheet=Image.new('RGB',(a.width+b.width,a.height),'white'); sheet.paste(a,(0,0)); sheet.paste(b,(a.width,0))
spread=B/'HISTROVE-058-YFI-Book-Spread-PROOF.png'; sheet.save(spread)
provenance={
    'selected_for_requested_book_proof':True,
    'artwork_approval_status':'v14 lighting-reviewed book proof only; not finally approved',
    'final_artwork_approved':False,
    'book_approved':False,
    'publication_authorized':False,
    'source_path':str(ART),
    'source_sha256':ART_SHA256,
    'source_rgb_pixel_sha256':hashlib.sha256(Image.open(ART).convert('RGB').tobytes()).hexdigest(),
    'source_dimensions':[iw,ih],
    'library_file_id':'libfile_8b0d2fba592c819192500580bec6e58e',
    'library_version':13,
    'file_id':'file_00000000300081fd853421746236e5bf',
    'lighting_review':'Passed with no further image edit; exact selected v14 raw',
    'refresh_authority':'Parent authorized refreshed book proof with v14 and exact callback text; no publication authority',
    'rendering':'Full native artwork, proportionally contained on A4, no crop, pixel edit, overlay or upsampling claim',
    'user_request':'Okay, let\'s see the book. See the art of the book and then we\'ll look at approving it.',
    'request_evidence':'Sentinel_10fd8a4914f88191ab65aebf92b52f54 2026-10-26 18:20:20 UTC'
}
content={
 'collector_number':'058/100','title':'YFI','eyebrow':'YEARN FINANCE','date':'17 JUL 2020','rarity':'COMMON','tagline':'NO RESERVED SEAT.','folio':'116',
 'story':story,'eggs':eggs,'sourceNote':source_note,'sources':sources,'art_note':art_note,
 'status':'PROOF — subject to user approval','artwork_provenance':provenance,
 'source_verification':verification,
 'layout_reference':{'template':'source/template-094-build_book.py','template_sha256':TEMPLATE_SHA256,'geometry':'Exact canonical drawing block; chapter identifiers only adapted; folio is 2 times collector number','page_size_points':[W,H]},
}
(B/'HISTROVE-058-YFI-Story-Data.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
(B/'058.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
(B/'art-provenance.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
qa={
 'page_count':len(doc),'page_size_points':[W,H],'source_art_dimensions_px':[iw,ih],'source_art_sha256':ART_SHA256,
 'source_art_unmodified':hashlib.sha256(ART.read_bytes()).hexdigest()==ART_SHA256,
 'native_effective_ppi':72/scale,'art_fit':'Contain full native artwork, proportional, unchanged canonical layout; narrow black top/bottom bars',
 'story_column_bottom_points':y,'clues_column_bottom_points':z,'story_paragraphs':len(story),'clue_count':len(eggs),'source_count':len(sources),
 'story_word_count':sum(len(p.split()) for p in story),'event_date':'17 JUL 2020','rarity':'common','collector_number':'058/100','folio':'116','card_phrase':'NO RESERVED SEAT.',
 'phrase_status':'Editorial caption, not a historical quotation',
 'linked_source_annotations':len(doc[1].get_links()),'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'spread_sha256':hashlib.sha256(spread.read_bytes()).hexdigest(),
 'visual_review':'Pending inspection of both rendered pages at full size',
 'book_approval_status':'Review-only proof; awaiting user approval','final_artwork_approved':False,'publication_authorized':False,
 'physical_print_acceptance':'Not claimed','rights_clearance':'Not established',
 'layout_template_sha256':TEMPLATE_SHA256,'source_verification_date':'2026-10-26',
 'artifact_marker':{'operation_kind':'edit','expected_output_count':1,'output_format':'pdf','executed_successfully_exactly_once':True}
}
(B/'book-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
