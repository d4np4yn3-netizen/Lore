"""Build proof-only HISTROVE 096 book using recovered template 094 geometry.

The recovered template is preserved verbatim as template-094-build_book.py.
Only input loading, identifiers, content, proof provenance and optional crop export
are adapted. Page geometry, typography, colors and proportional art fit remain
unchanged. Artwork approval is scoped to book preparation only. No book text or publication approval is asserted.
"""
from pathlib import Path
import argparse
import json
import html
import hashlib
import shutil
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

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
TEMPLATE = ROOT / 'source/template-094-build_book.py'
TEMPLATE_SHA256 = '45b535e413ea2f93f38053230d969c473a6d4b83b0b42d09614577a2394425ef'
assert hashlib.sha256(TEMPLATE.read_bytes()).hexdigest() == TEMPLATE_SHA256
assert hashlib.sha1(f'blob {len(TEMPLATE.read_bytes())}\0'.encode() + TEMPLATE.read_bytes()).hexdigest() == '744dc855a817e58f350aead35c25a7bfc8878470'
CARDS = {
    '096': {'title': 'PRESIDENTIAL MEME COIN', 'title_case': 'Presidential Meme Coin', 'slug': 'Presidential-Meme-Coin', 'date': '17 JAN 2025', 'phrase': 'POLITICS MEETS THE MARKET.', 'folio': '192', 'art': '096-fresh-portrait-free-art-v13.png', 'eyebrow': '$TRUMP', 'rarity': 'UNCOMMON'},
}
parser = argparse.ArgumentParser()
parser.add_argument('--card', required=True, choices=sorted(CARDS))
parser.add_argument('--content', required=True, type=Path)
parser.add_argument('--output-dir', type=Path)
parser.add_argument('--crops', type=Path)
args = parser.parse_args()
card = args.card
meta = CARDS[card]
B = (args.output_dir or ROOT).resolve()
assert B.is_relative_to(ROOT), 'All outputs must remain under card096-new-attraction/book-proof'
B.mkdir(parents=True, exist_ok=True)
SOURCE = B / 'source'
SOURCE.mkdir(exist_ok=True)
ART = ROOT.parent / meta['art']
content_input = args.content.resolve()
authoring = json.loads(content_input.read_text())
story = authoring['story']
eggs = authoring['eggs']
sources = authoring['sources']
art_note = authoring['art_note']
assert story and all(isinstance(p, str) and p.strip() for p in story)
assert eggs and all(e.get('title') and e.get('text') for e in eggs)
assert sources and all(s.get('title') and s.get('url') for s in sources)
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / f'{card}.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(SOURCE / 'authoring-content.json').write_bytes(content_input.read_bytes())
(B / f'{card}-{meta["slug"].lower()}.md').write_text(f'# {card} - {meta["title_case"]}\n\n{meta["date"]} / {meta["eyebrow"]} / {meta["rarity"]}\n\n{meta["phrase"]}\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')
ART_SHA256 = '415a3ed990cc89075e126731a99be8da0c0fd8b6a9e6563d3ecf96b539b30044'
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
assert Image.open(ART).size == (1060, 1484)
FONTS = WORKSPACE / 'card087-release/assets/cards/crypto/season-01/the-arbitrum-airdrop-master-087/source/fonts'
FONT_EXPECTED = {'DejaVuSans.ttf': 'fb0bd945a4f5aa716dcb8d9b7476bfa30e365a1e', 'DejaVuSans-Bold.ttf': '426812b9b0ce12f20285adf46d8acc0dd40dfba5'}
font_metadata = {}
for filename, expected_blob in FONT_EXPECTED.items():
    data = (FONTS / filename).read_bytes()
    git_blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert git_blob == expected_blob, (filename, git_blob)
    font_metadata[filename] = {'git_blob': git_blob, 'sha256': hashlib.sha256(data).hexdigest(), 'source': str(FONTS / filename)}
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / f'HISTROVE-{card}-{meta["slug"]}-Book-Proof.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle(f'HISTROVE {card} - {meta["title_case"]} - Book Proof')
c.setSubject('Proof only; awaiting user proof approval; publication not authorized')
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
label(meta['title'], 43, H - 102, 22, '#0B0B0B')
label(f'{card} / {meta["date"]} / {meta["eyebrow"]} / {meta["rarity"]}', 43, H - 124, 8, '#5A574F')
label(meta['phrase'], 43, H - 153, 14)
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
label(f'{card} / {meta["title"]}', 43, 40, 7.5, '#5A574F')
label(meta['folio'], W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / f'HISTROVE-{card}-{meta["slug"]}-Book-Proof-Spread.png')

closeups = None
if args.crops:
    crop_input = json.loads(args.crops.read_text())
    assert crop_input['source_dimensions'] == [iw, ih], crop_input
    boxes = crop_input['boxes']
    assert len(boxes) == len(eggs)
    assert all(0 <= x0 < x1 <= iw and 0 <= y0 < y1 <= ih for x0, y0, x1, y1 in boxes)
    closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'normalized_boxes': [[round(x0/iw, 8), round(y0/ih, 8), round(x1/iw, 8), round(y1/ih, 8)] for x0, y0, x1, y1 in boxes], 'coordinate_system': 'Top-left origin; normalized [x0,y0,x1,y1] fractions of full supplied proof artwork', 'titles': [e['title'] for e in eggs]}
    (B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
    CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
    for n, box in enumerate(boxes, 1):
        Image.open(ART).crop(box).save(CROPS / f'{card}-detail-{n}.png')

inherited_reference = json.loads((ROOT / 'source/template-094-layout-reference.json').read_text())
layout_reference = {
    'active_template': str(TEMPLATE),
    'active_template_sha256': TEMPLATE_SHA256,
    'canonical_repository_tree_sha': '057ec73ad1541848ea77531883cb1eedd4ddb5f5',
    'canonical_repository_template_git_blob': '744dc855a817e58f350aead35c25a7bfc8878470',
    'geometry': 'Unchanged recovered template 094 A4 two-page geometry, typography, colors, coordinates and proportional native artwork containment.',
    'inherited_parent_reference': inherited_reference,
    'inherited_parent_reference_preserved_without_changes': True,
    'folio': meta['folio'],
}
(SOURCE / 'layout-reference.json').write_text(json.dumps(layout_reference, indent=2) + '\n')
extracted = doc[1].get_text()
for expected_text in [meta['title'], f'{card} / {meta["date"]} / {meta["eyebrow"]} / {meta["rarity"]}', meta['phrase'], meta['folio']]:
    assert expected_text in extracted, (expected_text, extracted)
assert {link['uri'] for link in doc[1].get_links()} == {source['url'] for source in sources}
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
provenance = {
    'artifact_kind': 'proof-only book',
    'card': card,
    'book_approval_status': 'awaiting user proof',
    'publication_authorized': False,
    'artwork_status': 'art v13 and frame v5 approved for book preparation only; book text and publication not approved',
    'source_art_path': str(ART),
    'source_art_sha256': ART_SHA256,
    'source_art_bytes_modified': False,
    'trusted_art_preparation_approval': {'time_utc': '2026-10-25 11:45:15', 'message_id': 'Sentinel_b53947c250c481918be02c7edfc7129c', 'text': 'i thin kwe got it, approved for the book pages!', 'scope': 'art v13/frame v5 approved for book preparation only; not book text or publication'},
    'content_input': str(content_input),
    'content_sha256': hashlib.sha256(content_input.read_bytes()).hexdigest(),
    'proof_builder_path': str(Path(__file__).resolve()),
    'proof_builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'active_layout_reference': layout_reference,
    'fonts': font_metadata,
}
(B / 'proof-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
qa = {
    'page_count': len(doc), 'page_size_points': [W, H],
    'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256,
    'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256,
    'artwork_status': 'art v13 and frame v5 approved for book preparation only; book text and publication not approved',
    'native_effective_ppi': 72/scale,
    'native_resolution_note': f'{iw} x {ih} raw pixels at proportional A4 fit; {72/scale:.2f} effective PPI. Upsampling is not native resolution.',
    'art_fit': 'Contain proportional full supplied proof artwork with #0B0B0B edge bars; unchanged recovered 094 layout',
    'story_column_bottom_points': y, 'clues_column_bottom_points': z,
    'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources),
    'story_word_count': sum(len(p.split()) for p in story),
    'event_date': meta['date'], 'rarity': meta['rarity'].lower(), 'collector_number': f'{card}/100',
    'card_phrase': meta['phrase'], 'folio': meta['folio'],
    'phrase_status': 'Supplied editorial caption; no additional approval asserted',
    'linked_source_annotations': len(doc[1].get_links()),
    'unique_linked_sources': len({link['uri'] for link in doc[1].get_links()}),
    'source_link_uri_set_validation': 'passed',
    'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
    'visual_review': 'Pending inspection of all rendered pages',
    'physical_print_acceptance': 'Not claimed',
    'rights_clearance': 'Not established; artwork approval does not imply rights clearance',
    'layout_reference': layout_reference,
    'fonts': font_metadata,
    'source_verification_date': '2026-10-25',
    'book_approval_status': 'awaiting user proof',
    'publication_authorized': False,
    'content_review': art_note,
    'closeups_generated': closeups is not None,
    'render_scale': 1.5,
    'page_png_dimensions_px': [list(a.size), list(b.size)],
    'text_metadata_assertions': 'passed',
}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps({'card': card, 'pdf': str(out), 'qa': qa}, indent=2))
