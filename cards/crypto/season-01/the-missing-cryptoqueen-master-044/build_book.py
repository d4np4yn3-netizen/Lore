from pathlib import Path
import json, html, hashlib
from datetime import datetime, timezone
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
ART_SHA256 = 'ddeffeaa017353051dbab23fda2ac182bd1388877463d3e5ba3e5e72bc55c4a3'
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
story = [
    "On 25 October 2017, Ruja Ignatova traveled from Sofia, Bulgaria, to Athens, Greece. The journey became the date attached to the disappearance of OneCoin's best-known promoter, the woman widely called the Cryptoqueen.",
    "Ignatova had helped build OneCoin into an international sales operation. Its pitch borrowed the language and excitement of cryptocurrency, while packages were promoted through a network that encouraged buyers to recruit others. Investigators later alleged that false claims had drawn investors into a scheme involving billions of dollars.",
    "The FBI's account describes a crucial gap between the sales story and the system behind it: OneCoins were not mined like conventional cryptocurrencies, and the company set their value. Buyers were being asked to trust the organisation selling the promise.",
    "A federal charge and arrest warrant had already been issued in New York on 12 October 2017. The documented trip to Athens followed thirteen days later. The illustration stops at that disappearance; it does not propose a hiding place, a later appearance or an explanation for what happened next.",
    "The stage turns this uncertainty into a fictional vanishing act. Ignatova looks back from the curtain while a microphone and branded folder remain in the spotlight. THE FINAL ACT. is the card's editorial line, not her words or a claim that this performance happened. The spectacle is imagined; the journey and date are the historical anchors."
]
eggs = [
    {'title': 'SOFIA TO ATHENS', 'text': "The itinerary names the route recorded by the FBI for 25 October 2017. It anchors the disappearance to a documented journey. The ticket is an invented prop, not a reproduction of her travel document."},
    {'title': 'THE DATE TAG', 'text': "25 OCT 2017 marks the selected moment. Its placement beside the folder links the theatrical scene to the historical date, without suggesting that this tag existed."},
    {'title': 'THE UNTAKEN MICROPHONE', 'text': "The empty speaking position recalls OneCoin's public promotional spectacle. The theatre and curtain exit are symbolic staging, not evidence of an actual farewell performance."},
    {'title': 'THE FOLDER AND CONFETTI', 'text': "The OneCoin folder represents the sales pitch left behind. Scattered confetti points forward to card 045, BitConnect, as a collection crossover about promotional spectacle. It does not imply a relationship between the organisations."}
]
sources = [
    {'title': 'FBI: Ruja Ignatova wanted profile', 'url': 'https://www.fbi.gov/wanted/topten/ruja-ignatova', 'supports': '25 October 2017 Sofia-to-Athens journey; 12 October 2017 charge and warrant; OneCoin leadership and allegations; published likeness reference'},
    {'title': 'FBI: Cryptoqueen case account, 30 June 2022', 'url': 'https://www.fbi.gov/news/stories/ruja-ignatova-added-to-fbis-ten-most-wanted-fugitives-list', 'supports': 'Marketing structure; investigators account of mining and company-set value; disappearance chronology'}
]
art_note = "Ruja's likeness is informed by published FBI photographs. The stage, costume, props and curtain exit are artistic interpretation, not a documented event. Charges and investigative claims are allegations. THE FINAL ACT. is editorial wording."

source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '044.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / '044-the-missing-cryptoqueen.md').write_text('# 044 - The Missing Cryptoqueen\n\n25 OCT 2017 / UNCOMMON\n\nTHE FINAL ACT.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(B.parent / 'histrove-rollout/repo/cards/master/front-v3/source/fonts' / filename)))
W, H = A4
out = B / 'HISTROVE-044-The-Missing-Cryptoqueen-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1)
c.setTitle('HISTROVE 044 - The Missing Cryptoqueen')
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
label('THE MISSING CRYPTOQUEEN', 43, H - 102, 22, '#0B0B0B')
label('044 / 25 OCT 2017 / CRYPTO / UNCOMMON', 43, H - 124, 8, '#5A574F')
label('THE FINAL ACT.', 43, H - 153, 14)
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
label('044 / THE MISSING CRYPTOQUEEN', 43, 40, 7.5, '#5A574F')
label('088', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-044-Book-Preview.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'linked_source_count': len(doc[1].get_links()), 'event_date': '2017-10-25', 'editorial_line': 'THE FINAL ACT.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
