"""Build the two-page 014 Litecoin editorial spread from its chapter."""
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
ART = REPO / "cards/crypto/season-01/litecoin-launches-master-014/art.png"
OUT = HERE / "proofs/014-litecoin-launches-full-art-spread-v1.pdf"
FONT = REPO / "cards/master/front-v3/source/fonts"
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Serif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold")

W, H = A4
BLACK, CREAM, GOLD, GREY = map(HexColor, ("#0B0B0B", "#F5F2EB", "#886615", "#5A574F"))
document = (HERE / "014-litecoin-launches.md").read_text(encoding="utf-8")

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
c.setTitle("LORE Crypto Season One - 014 Digital Silver - editorial spread")
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
c.drawString(43, H-102, "DIGITAL SILVER")
c.setFillColor(GREY)
c.setFont("DejaVu", 9)
c.drawString(43, H-122, "014  /  13 OCT 2011  /  LITECOIN  /  UNCOMMON")
c.setFillColor(GOLD)
c.setFont("DejaVu-Serif", 15)
c.drawString(43, H-151, "SILVER TO BITCOIN'S GOLD.")

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
c.drawString(43, 40, "014 / DIGITAL SILVER / REVIEW")
c.drawRightString(W-43, 40, "028")
c.save()
print(f"{OUT} | story bottom {y:.1f} | notes bottom {z:.1f}")
