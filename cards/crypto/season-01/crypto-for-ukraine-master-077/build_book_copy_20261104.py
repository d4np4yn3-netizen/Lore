from pathlib import Path
import json,html,hashlib
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
ART=B/'art.png'
assert hashlib.sha256(ART.read_bytes()).hexdigest() == '6e1680b3eb2450adff2c84c8f05723b098145ee413937fbc972b1905bc7304ec'
authoring=json.loads((B/'authoring-content-copy-2026-11-04.json').read_text())
story=authoring['story']; eggs=authoring['eggs']; sources=authoring['sources']
art_note=authoring['art_note']
source_note='Sources: '+'; '.join(f"[{s['title']}]({s['url']})" for s in sources)+'. '+art_note
source_pdf='Sources: '+'; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources)+'. '+html.escape(art_note)
for name,filename in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(B/'source/fonts'/filename)))
W, H = A4
out = B / 'HISTROVE-077-Crypto-for-Ukraine-Book-copy-2026-11-04.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 077 - Crypto for Ukraine')
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
label('CRYPTO FOR UKRAINE', 43, H - 102, 22, '#0B0B0B')
label('077 / 03 MAR 2022 / UKRAINE / COMMON', 43, H - 124, 8, '#5A574F')
label('FROM WALLETS TO AID', 43, H - 153, 14)
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
label('077 / CRYPTO FOR UKRAINE', 43, 40, 7.5, '#5A574F')
label('154', W - 62, 40, 7.5, '#5A574F')
c.save()
doc=fitz.open(out)
for i,p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(B/f'book-page-{i+1}-copy-2026-11-04.png'))
a=Image.open(B/'book-page-1-copy-2026-11-04.png')
b=Image.open(B/'book-page-2-copy-2026-11-04.png')
spread=Image.new('RGB',(a.width+b.width,a.height),'white')
spread.paste(a,(0,0));spread.paste(b,(a.width,0))
spread.save(B/'book-spread-copy-2026-11-04.png')
