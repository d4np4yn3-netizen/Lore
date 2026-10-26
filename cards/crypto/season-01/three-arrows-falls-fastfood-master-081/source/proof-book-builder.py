"""Build a review-only 081 fast-food book using the canonical 094 drawing block.
The full approved v4 raw artwork is embedded losslessly, without crop or overlay.
Raw artwork and card are approved; this book is pending user approval and publication is not authorized.
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
ART=B.parent/'081-three-arrows-fastfood-art-v4-card-fit.png'
ART_SHA256='5c644442062411b1179be26069c88ff89c0cd3ae7da36b3eeae06767c5e0fa63'
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
FONTS=B/'source/fonts'
for name,filename in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/filename)))
# BEGIN EXACT CANONICAL DRAWING BLOCK, IDENTIFIERS ONLY ADAPTED
W, H = A4
out = B / 'HISTROVE-081-Three-Arrows-Falls-Fast-Food-Book-PROOF.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 081 - Three Arrows Falls - Fast Food - PROOF')
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
label('THREE ARROWS FALLS', 43, H - 102, 22, '#0B0B0B')
label('081 / JULY 2022 / THREE ARROWS / RARE', 43, H - 124, 8, '#5A574F')
label('FROM FUND TO FRIES', 43, H - 153, 14)
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
label('081 / THREE ARROWS FALLS', 43, 40, 7.5, '#5A574F')
label('162', W - 62, 40, 7.5, '#5A574F')
c.save()
# END EXACT CANONICAL DRAWING BLOCK

doc=fitz.open(out)
assert len(doc)==2
for i,p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(B/f'book-page-{i+1}.png'))
a=Image.open(B/'book-page-1.png'); b=Image.open(B/'book-page-2.png')
sheet=Image.new('RGB',(a.width+b.width,a.height),'white'); sheet.paste(a,(0,0)); sheet.paste(b,(a.width,0))
spread=B/'HISTROVE-081-Three-Arrows-Falls-Fast-Food-Book-Spread-PROOF.png'; sheet.save(spread)
provenance={
 'selected_for_requested_book_proof':True,
 'artwork_approval_status':'Approved current v4 fast-food artwork and card; book approval pending',
 'final_artwork_approved':True,'card_approved':True,'book_approved':False,'publication_authorized':False,
 'source_path':str(ART),'source_sha256':ART_SHA256,
 'source_rgb_pixel_sha256':hashlib.sha256(Image.open(ART).convert('RGB').tobytes()).hexdigest(),
 'source_dimensions':[iw,ih],
 'library_file_id':'libfile_2cf07d1d64e48191a983421ea236ea9c','library_version':3,
 'file_id':'file_000000004be48209bdf5661f9be863cc',
 'card_review_library_file_id':'libfile_bbcc7d3fc7648191bb7a5761be6d2d3e','card_review_library_version':1,
 'rendering':'Full native artwork proportionally contained on A4; no crop, pixel edit, overlay or upsampling claim',
 'approval_evidence':verification['authorization']['trusted_user_evidence'],
 'prior_boat_book':'Preserved unchanged; this new fast-food proof uses separate paths and identities'
}
content={
 'collector_number':'081/100','title':'THREE ARROWS FALLS','eyebrow':'THREE ARROWS',
 'date':'JULY 2022','event_date':'2022-07','date_precision':'month','rarity':'RARE',
 'tagline':'FROM FUND TO FRIES','folio':'162',
 'story':story,'eggs':eggs,'sourceNote':source_note,'sources':sources,'art_note':art_note,
 'status':'PROOF - subject to user approval','book_approved':False,'publication_authorized':False,
 'artwork_provenance':provenance,'source_verification':verification,
 'layout_reference':{'template':'source/template-094-build_book.py','template_sha256':TEMPLATE_SHA256,
 'geometry':'Exact canonical drawing block; chapter identifiers only adapted; folio is 2 times collector number','page_size_points':[W,H]}
}
story_path=B/'HISTROVE-081-Three-Arrows-Falls-Fast-Food-Story-Data.json'
story_path.write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
(B/'081.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
(B/'art-provenance.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
qa={
 'page_count':len(doc),'page_size_points':[W,H],'source_art_dimensions_px':[iw,ih],'source_art_sha256':ART_SHA256,
 'source_art_unmodified':hashlib.sha256(ART.read_bytes()).hexdigest()==ART_SHA256,
 'native_effective_ppi':72/scale,
 'art_fit':'Contain full native artwork, proportional, unchanged canonical layout; narrow black top/bottom bars',
 'story_column_bottom_points':y,'clues_column_bottom_points':z,
 'story_paragraphs':len(story),'clue_count':len(eggs),'source_count':len(sources),
 'story_word_count':sum(len(p.split()) for p in story),
 'event_date':'2022-07','display_date':'JULY 2022','date_precision':'month','rarity':'rare',
 'collector_number':'081/100','folio':'162','card_phrase':'FROM FUND TO FRIES',
 'phrase_status':'Approved scene-linked editorial caption, not a historical quotation',
 'linked_source_annotations':len(doc[1].get_links()),'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
 'spread_sha256':hashlib.sha256(spread.read_bytes()).hexdigest(),
 'story_data_sha256':hashlib.sha256(story_path.read_bytes()).hexdigest(),
 'visual_review':'Pending inspection of both rendered pages at full size',
 'book_approval_status':'Review-only proof; awaiting user approval','final_artwork_approved':True,'card_approved':True,'book_approved':False,'publication_authorized':False,
 'physical_print_acceptance':'Not claimed','rights_clearance':'Not established',
 'layout_template_sha256':TEMPLATE_SHA256,'source_verification_date':'2026-10-26',
 'artifact_marker':{'operation_kind':'create','expected_output_count':1,'output_format':'pdf','executed_successfully_exactly_once':True}
}
assert qa['story_word_count']==198
(B/'book-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
