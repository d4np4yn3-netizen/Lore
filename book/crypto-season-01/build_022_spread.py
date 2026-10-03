"""Build the two-page Crypto 022 publication spread without changing its artwork."""
from pathlib import Path
import html
import re

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ART = REPO / "cards/crypto/season-01/buried-fortune-master-022/art.png"
OUT = HERE / "proofs/022-buried-fortune-full-art-spread-v1.pdf"
FONT = REPO / "cards/master/front-v3/source/fonts"
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Serif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")

W, H = A4
BLACK, CREAM, GOLD, GREY = map(HexColor, ("#0B0B0B", "#F5F2EB", "#886615", "#5A574F"))
document = (HERE / "022-buried-fortune.md").read_text(encoding="utf-8")

def section(heading):
    match = re.search(r"(?m)^## " + re.escape(heading) + r"\n(.*?)(?=\n## |\Z)", document, re.S)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group(1).strip()

def rich(value):
    value = html.escape(value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<link href="\2" color="#785910">\1</link>', value)
    value = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", value)
    return re.sub(r"\*(.*?)\*", r"<i>\1</i>", value)

def para(value, x, top, width, style, gap=8):
    p = Paragraph(rich(value), style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top-height)
    return top-height-gap

def label(value, x, y, size=8, color=GOLD):
    c.setFillColor(color)
    c.setFont("DejaVu-Bold", size)
    c.drawString(x, y, value)

OUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle("LORE Crypto Season One - 022 Buried Fortune - publication spread")
c.setAuthor("LORE")

with Image.open(ART) as image:
    iw, ih = image.size
scale = max(W/iw, H/ih)
c.drawImage(str(ART), (W-iw*scale)/2, (H-ih*scale)/2, width=iw*scale, height=ih*scale)
c.showPage()

c.setFillColor(CREAM)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setStrokeColor(GOLD)
c.line(43, H-57, W-43, H-57)
label("LORE / CRYPTO SEASON ONE", 43, H-39, 9, BLACK)
c.setFillColor(BLACK)
c.setFont("DejaVu-Bold", 22)
c.drawString(43, H-102, "BURIED FORTUNE")
c.setFillColor(GREY)
c.setFont("DejaVu", 9)
c.drawString(43, H-122, "022  /  2013  /  BITCOIN  /  RARE")
c.setFillColor(GOLD)
c.setFont("DejaVu-Serif", 15)
c.drawString(43, H-151, "ONE DRIVE. A FORTUNE.")

body = ParagraphStyle("body", fontName="DejaVu", fontSize=9.3, leading=13.8, textColor=BLACK)
egg = ParagraphStyle("egg", fontName="DejaVu", fontSize=8.8, leading=12.9, textColor=BLACK)
note = ParagraphStyle("note", fontName="DejaVu", fontSize=7.5, leading=10.9, textColor=GREY)
y = H-190
for part in section("The story").split("\n\n"):
    y = para(part, 43, y, 242, body)

label("DETAILS IN THE ART", 307, H-186, 9, BLACK)
z = H-205
for i, line in enumerate(section("Details in the artwork").splitlines(), 1):
    match = re.fullmatch(r"\d+\. \*\*(.*?)\*\* (.*)", line)
    if not match:
        raise ValueError(f"Invalid art note: {line}")
    label(f"{i:02d}  {match.group(1).rstrip('.').upper()}", 307, z, 7.8)
    z = para(match.group(2), 307, z-10, 242, egg, 10)

c.setStrokeColor(GOLD)
c.line(307, z+1, 549, z+1)
label("SOURCE & ART NOTE", 307, z-18, 8.2, BLACK)
z = para(section("Source and art note").split("\n\n")[0], 307, z-30, 242, note, 0)
if min(y, z) < 80:
    raise RuntimeError(f"Column overflow: story={y}, notes={z}")

c.setStrokeColor(GOLD)
c.line(43, 57, W-43, 57)
c.setFillColor(GREY)
c.setFont("DejaVu", 7.5)
c.drawString(43, 40, "022 / BURIED FORTUNE")
c.drawRightString(W-43, 40, "044")
c.save()
print(f"{OUT} | story bottom {y:.1f} | notes bottom {z:.1f}")



# Self-contained HTML edition. Embed the selected PNG bytes and the same fonts;
# no network fetches are required to read or print this chapter.
import base64

def uri(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(Path(path).read_bytes()).decode('ascii')

def web_rich(value):
    value = html.escape(value)
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', value)
    value = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', value)
    return re.sub(r'\*(.*?)\*', r'<em>\1</em>', value)

story_html = '\n'.join('<p>' + web_rich(p) + '</p>' for p in section('The story').split('\n\n'))
clue_html = []
for i, line in enumerate(section('Details in the artwork').splitlines(), 1):
    match = re.fullmatch(r'\d+\. \*\*(.*?)\*\* (.*)', line)
    clue_html.append('<section class="clue"><h3>' + f'{i:02d}  ' + html.escape(match.group(1).rstrip('.').upper()) + '</h3><p>' + web_rich(match.group(2)) + '</p></section>')
font_normal = uri(FONT / 'DejaVuSans.ttf', 'font/ttf')
font_bold = uri(FONT / 'DejaVuSans-Bold.ttf', 'font/ttf')
font_serif = uri('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 'font/ttf')
art_uri = uri(ART, 'image/png')
css = '''
@font-face{font-family:DejaVu;src:url(NORMAL);font-weight:400;font-display:block}
@font-face{font-family:DejaVu;src:url(BOLD);font-weight:700;font-display:block}
@font-face{font-family:DejaVuSerif;src:url(SERIF);font-weight:400;font-display:block}
*{box-sizing:border-box}html{background:#202020}body{margin:0;padding:24px 0;color:#0B0B0B;font-family:DejaVu,sans-serif}
.page{width:595.2756pt;height:841.8898pt;margin:0 auto 24px;position:relative;overflow:hidden;box-shadow:0 6px 24px #0006}
.art-page{background:#0B0B0B;display:flex;align-items:center;justify-content:center}.art-page img{display:block;width:100%;height:100%;object-fit:contain}
.text-page{background:#F5F2EB}.running-head{position:absolute;left:43pt;right:43pt;top:28pt;height:30pt;font-size:9pt;font-weight:700;border-bottom:1px solid #886615}
h1{position:absolute;left:43pt;top:79pt;margin:0;font-size:22pt;line-height:26.4pt;font-weight:700}
.metadata{position:absolute;left:43pt;top:113pt;margin:0;color:#5A574F;font-size:9pt;line-height:12pt}
.phrase{position:absolute;left:43pt;top:137pt;margin:0;color:#886615;font-family:DejaVuSerif,serif;font-size:15pt;line-height:18pt}
.columns{position:absolute;left:43pt;right:46.2756pt;top:181pt;display:grid;grid-template-columns:242pt 242pt;gap:22pt}
.story{padding-top:9pt;font-size:9.3pt;line-height:13.8pt}.story p{margin:0 0 8pt}
h2{font-size:9pt;line-height:11pt;margin:0 0 9pt;font-weight:700}.clue h3{font-size:7.8pt;line-height:10pt;color:#886615;margin:0 0 2pt;font-weight:700}
.clue p{font-size:8.8pt;line-height:12.9pt;margin:0 0 10pt}
.source-note{border-top:1px solid #886615;padding-top:13pt;margin-top:1pt}.source-note h2{font-size:8.2pt;line-height:11pt;margin:0 0 7pt}.source-note p{font-size:7.5pt;line-height:10.9pt;color:#5A574F;margin:0}a{color:#785910;text-decoration:none}a:hover,a:focus{text-decoration:underline}
footer{position:absolute;left:43pt;right:43pt;bottom:38pt;border-top:1px solid #886615;padding-top:10pt;display:flex;justify-content:space-between;font-size:7.5pt;color:#5A574F;line-height:9pt}
@page{size:A4;margin:0}@media print{html,body{background:white;padding:0}.page{margin:0;box-shadow:none;break-after:page}.page:last-child{break-after:auto}}
@media screen and (max-width:820px){body{padding:12px 0}.page{width:calc(100vw - 24px);height:auto;min-height:0;margin-bottom:12px}.art-page{aspect-ratio:1060/1484}.art-page img{height:auto}.text-page{padding:24px}.running-head,h1,.metadata,.phrase,.columns,footer{position:static}.running-head{height:auto;padding-bottom:14px;margin-bottom:24px;font-size:12px}h1{font-size:28px;line-height:1.2}.metadata{font-size:12px;line-height:1.5;margin-top:8px}.phrase{font-size:21px;line-height:1.4;margin-top:12px}.columns{grid-template-columns:1fr;gap:28px;margin-top:28px}.story{padding-top:0;font-size:14px;line-height:1.65}.story p{margin-bottom:14px}h2{font-size:14px;line-height:1.4;margin-bottom:16px}.clue h3{font-size:12px;line-height:1.4;margin-bottom:6px}.clue p{font-size:14px;line-height:1.6;margin-bottom:18px}.source-note{padding-top:18px}.source-note h2{font-size:12px;margin-bottom:12px}.source-note p{font-size:12px;line-height:1.65}footer{font-size:11px;margin-top:28px;padding-top:14px;line-height:1.4}}
'''.replace('NORMAL', font_normal).replace('BOLD', font_bold).replace('SERIF', font_serif)
html_doc = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LORE 022 - Buried Fortune</title><style>' + css + '</style></head><body><main>'
html_doc += '<section class="page art-page" aria-label="Full selected illustration"><img src="' + art_uri + '" alt="A man looks across Newport landfill beside a DOCKS WAY / NEWPORT fence sign. Below him, a symbolic cutaway reveals an enlarged hard drive with a 2009 label and a partly buried WAVES coffee cup."></section>'
html_doc += '<article class="page text-page"><div class="running-head">LORE / CRYPTO SEASON ONE</div><h1>BURIED FORTUNE</h1><p class="metadata">022&nbsp; / &nbsp;2013&nbsp; / &nbsp;BITCOIN&nbsp; / &nbsp;RARE</p><p class="phrase">ONE DRIVE. A FORTUNE.</p><div class="columns"><section class="story" aria-label="The story">' + story_html + '</section><aside><h2>DETAILS IN THE ART</h2>' + ''.join(clue_html) + '<section class="source-note"><h2>SOURCE &amp; ART NOTE</h2><p>' + web_rich(section('Source and art note').split('\n\n')[0]) + '</p></section></aside></div><footer><span>022 / BURIED FORTUNE</span><span>044</span></footer></article></main></body></html>\n'
HTML_OUT = OUT.with_suffix('.html')
HTML_OUT.write_text(html_doc, encoding='utf-8')
print(HTML_OUT)
