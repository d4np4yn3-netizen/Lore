from pathlib import Path
import json, html, hashlib, shutil, subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import fitz

B = Path(__file__).resolve().parent
ART = B / 'art.png'
ART_SOURCE = B.parent / 'HISTROVE-045-BitConnect-Lighting-Investor-Art-Proof-v3.png'
ART_SHA256 = '06a19f961a37259c8c3d1bf194cf4b8711a920e92e99a12619092428f939a95b'
if not ART.exists():
    assert hashlib.sha256(ART_SOURCE.read_bytes()).hexdigest() == ART_SHA256
    shutil.copyfile(ART_SOURCE, ART)
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
story = [
    "On 28 October 2017, Carlos Matos took the stage at BitConnect's annual ceremony in Pattaya, Thailand. His exuberant greeting, HEY, HEY, HEY!, became the sound of a crypto meme that outlived the company it celebrated.",
    "BitConnect sold an appealing story: software could turn cryptocurrency trading into dependable returns. Promoters spread that pitch through videos, testimonials and a referral network. The Pattaya ceremony wrapped it in spectacle, recognising leading promoters with cash and luxury cars. A celebration of success doubled as an advertisement for joining in.",
    "Matos later told WNYC that he had invested $25,610. He described being caught up in the event and wanting to tell other people what had happened to him. The speech travelled through remixes, songs and reaction clips. Its confidence made it instantly recognisable, even to people who had never used BitConnect.",
    "The lending operation and exchange closed on 16 January 2018. The later legal record described a Ponzi scheme, in which money from new investors paid earlier ones. U.S. authorities identified Satish Kumbhani as BitConnect's founder. Matos is shown here as the enthusiastic investor and viral speaker, not as the founder or the architect of the scheme.",
    "HISTROVE holds the image at the 2017 celebration. Amber beams and blue stage lights frame a raised fist, a microphone and a crowd swept up in the moment. The miniature car, numbered plinth and cracked pyramid are illustrated clues rather than a reconstruction of the stage. The crack lets hindsight enter the scene while the performance is still full of conviction."
]
eggs = [
    {'title': 'THE MINIATURE CAR', 'text': "The small sports car recalls luxury-car awards to leading promoters at the convention. Its placement is symbolic; it does not claim that Matos won a car or that this model stood onstage."},
    {'title': '25,610', 'text': "The number on the plinth is the US-dollar amount Matos later said he invested. It is a self-reported investment, not an audited balance, a prize value or a promised return."},
    {'title': 'THE CRACKED PYRAMID', 'text': "The broken gold pyramid is a retrospective metaphor for the scheme's failure. It brings knowledge of the later collapse into the illustration; it is not a documented stage prop."},
    {'title': 'THE INVESTOR LANYARD', 'text': "The badge makes Matos's role explicit: investor and viral speaker. It is an illustrative label, not a reproduction of an authenticated event badge. BitConnect's founder was Satish Kumbhani."}
]
sources = [
    {'title': 'Conceptual Events: 28 October 2017 ceremony', 'url': 'https://micemagic.wixsite.com/conceptual-events/single-post/2017/10/28/crypto-currency-event-bitconnect-1st-annual-ceremony-in-pattaya-thailand', 'supports': 'Contemporaneous organiser account: 28 October 2017 event date, Pattaya location and recognition of national and regional promoters.'},
    {'title': 'WNYC: Matos interview and speech, 2021', 'url': 'https://www.wnycstudios.org/podcasts/otm/segments/meme-known-cryptocurrencys-biggest-scam-now-nft-on-the-media', 'supports': 'Recorded HEY, HEY, HEY greeting; Matos self-reported US$25,610 investment; attendee/investor account; speech and subsequent remixes. His testimony is attributed, not independently audited.'},
    {'title': 'SEC complaint, 2021, paras. 71, 81-82, 222', 'url': 'https://www.sec.gov/files/litigation/complaints/2021/comp-pr2021-90.pdf', 'supports': 'October 2017 Pattaya event; awards of cash and luxury cars to top promoters; 16 January 2018 closure announcement. A civil complaint contains allegations, not judicial findings.'},
    {'title': 'DOJ: BitConnect restitution, 2023', 'url': 'https://www.justice.gov/archives/opa/pr/crypto-fraud-victims-receive-over-17-million-restitution-bitconnect-scheme', 'supports': 'Ponzi mechanism; Glenn Arcaro guilty plea; Satish Kumbhani identified as founder. Kumbhani indictment is not a conviction.'}
]
art_note = "The date is corroborated by the organiser; the speech excerpt is verified through WNYC, not the original full video. The stage and props are artistic interpretation. The car does not identify Matos as a prize winner; the pyramid is retrospective symbolism. The 2018 closure is separate. Matos's investment figure is self-reported; SEC complaint claims remain allegations."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '045.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '045-bitconnect.md').write_text('# 045 - BitConnect\n\n28 OCT 2017 / RARE\n\nHEY, HEY, HEY!\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

FONTS = B.parents[2] / 'master/front-v3/source/fonts'
FONTS.mkdir(exist_ok=True)
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    assert (FONTS / filename).exists(), f'Missing canonical font: {filename}'
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-045-BitConnect-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1)
c.setTitle('HISTROVE 045 - BitConnect')
c.setAuthor('HISTROVE')
iw, ih = Image.open(ART).size
scale = min(W / iw, H / ih)
c.setFillColor(HexColor('#0B0B0B'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.drawImage(str(ART), (W - iw * scale) / 2, (H - ih * scale) / 2, width=iw * scale, height=ih * scale)
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
label('BITCONNECT', 43, H - 102, 22, '#0B0B0B')
label('045 / 28 OCT 2017 / CRYPTO / RARE', 43, H - 124, 8, '#5A574F')
label('HEY, HEY, HEY!', 43, H - 153, 14)
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
label('045 / BITCONNECT', 43, 40, 7.5, '#5A574F')
label('090', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-045-BitConnect-Book-Spread.png')
boxes = [[0, 830, 240, 950], [66, 935, 222, 1003], [926, 755, 1060, 922], [575, 760, 696, 974]]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n,box in enumerate(boxes,1):
    Image.open(ART).crop(box).save(CROPS / f'045-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw,ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; same as 044', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '2017-10-28', 'closure_date': '2018-01-16', 'rarity': 'rare', 'collector_number': '045/100', 'card_phrase': 'HEY, HEY, HEY!', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'reference_layout': 'cards/crypto/season-01/the-missing-cryptoqueen-master-044/build_book.py', 'reference_layout_commit': 'ac21a2bd4eb64c1fe2cb4d76a313a66c4901c323'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
