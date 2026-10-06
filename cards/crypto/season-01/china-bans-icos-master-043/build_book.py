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
ART_SHA256 = '6c1d92a0aa532e8ea27d78b9875117c6714986e1933e362386b0d8abe1d9ed48'
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
story = [
    "On 4 September 2017, seven Chinese authorities issued a joint notice ordering token fundraising, including initial coin offerings, to stop. A fast-growing route for raising money through newly issued tokens had met a national regulatory barrier.",
    "The notice described token fundraising as unauthorized and illegal public financing. It identified risks including illegal securities issuance, fundraising fraud and pyramid schemes. This was a regulatory assessment of the activity; it was not a finding that every individual project had committed each offence.",
    "Organizers of completed offerings were told to make arrangements to unwind them and protect investors. The refund tray in the illustration gives that requirement a human scale: behind the token-sale promises were people waiting to recover their money.",
    "The order also restricted token-financing platforms from exchanging legal tender for tokens or virtual currencies, trading them as a central counterparty, or providing pricing and intermediary services. Financial and payment institutions were barred from providing services for token fundraising and related trading.",
    "The scene imagines the interruption as officials arriving at a neon-lit fundraising market. Its characters, stalls and police encounter are fictional, not a documented raid. The 2017 notice did not establish a blanket ban on possessing every cryptocurrency, and it was not the later mining crackdown."
]
eggs = [
    {'title': 'THE DATED NOTICE', 'text': "The clipboard reads 04 SEP 2017, the date of the joint announcement. Its delivery turns a busy token market into a moment of interruption. The prop is an illustration, not a reproduction of an official form."},
    {'title': 'THE REFUND TRAY', 'text': "The tray marked REFUNDS references the instruction for completed token offerings to make clearance and refund arrangements. Its envelopes are imagined props, not evidence from a particular project."},
    {'title': 'THE UNFINISHED PITCH', 'text': "An upward chart is left on the sales board as the discussion stops. It symbolises fundraising interrupted, without accusing a named project of fraud or promising that prices would keep rising."},
    {'title': 'THE PACKED POWER CABLE', 'text': "The small coil on the equipment case points forward to China's 2021 mining crackdown and card 072. It is an intentional collection crossover, not a mining restriction in the September 2017 ICO notice."}
]
sources = [
    {'title': 'Joint Chinese regulatory notice, 4 September 2017', 'url': 'https://www.cac.gov.cn/2017-09/04/c_1121603512.htm', 'supports': 'Seven issuing authorities; token-fundraising halt; clearance and refund arrangements; platform and financial-service restrictions'},
    {'title': 'NDRC and partner authorities: mining notice, September 2021', 'url': 'https://www.ndrc.gov.cn/xxgk/zcfb/tz/202109/t20210924_1297474.html', 'supports': 'Later mining restrictions; temporal context for the cable crossover'}
]
art_note = "Characters, police visit and market props are fictional visual storytelling, not a documented raid. FUNDRAISING HALTED. is editorial wording, not an official quotation. No specific project's wrongdoing is alleged."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '043.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / '043-china-bans-icos.md').write_text('# 043 - China Bans ICOs\n\n04 SEP 2017 / RARE\n\nFUNDRAISING HALTED.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(B.parent / 'histrove-rollout/repo/cards/master/front-v3/source/fonts' / filename)))
W, H = A4
out = B / 'HISTROVE-043-China-Bans-ICOs-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1)
c.setTitle('HISTROVE 043 - China Bans ICOs')
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
label('CHINA BANS ICOs', 43, H - 102, 22, '#0B0B0B')
label('043 / 04 SEP 2017 / CRYPTO / RARE', 43, H - 124, 8, '#5A574F')
label('FUNDRAISING HALTED.', 43, H - 153, 14)
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
label('043 / CHINA BANS ICOs', 43, 40, 7.5, '#5A574F')
label('086', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-043-Book-Preview.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'linked_source_count': len(doc[1].get_links()), 'event_date': '2017-09-04', 'editorial_line': 'FUNDRAISING HALTED.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
