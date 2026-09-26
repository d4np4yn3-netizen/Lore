"""Build either two-page editorial proof for card 001 (not a print specification)."""
from pathlib import Path
import argparse

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--full-art", action="store_true", help="Use the approved illustration edge to edge on page one")
args = parser.parse_args()
OUT = ROOT / "book/crypto-season-01/proofs" / ("001-blind-signatures-full-art-spread-v2.pdf" if args.full_art else "001-blind-signatures-spread-v1.pdf")
ART = ROOT / "cards/crypto/season-01/blind-signatures-master-01/LORE-Blind-Signatures-Legendary-v1-Print-v2.png"
ILLUSTRATION = ROOT / "cards/crypto/season-01/blind-signatures-master-01/art.png"
LOGO = ROOT / "brand/assets/png/lore_logo_primary_gold_white.png"
FONT = ROOT / "cards/master/front-v3/source/fonts"

pdfmetrics.registerFont(TTFont("DejaVu", str(FONT / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Serif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))

W, H = A4
BLACK, CREAM, GOLD, GREY = [HexColor(x) for x in ("#0B0B0B", "#F5F2EB", "#D4AF37", "#5A574F")]

def paragraph(c, text, x, top, width, style, gap=0):
    p = Paragraph(text, style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top - height)
    return top - height - gap

def label(c, text, x, y, color=GOLD, size=9):
    c.setFillColor(color)
    c.setFont("DejaVu-Bold", size)
    c.drawString(x, y, text)

OUT.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
c.setTitle("LORE Crypto Season One - 001 Blind Signatures - editorial spread proof")
c.setAuthor("LORE")

# Page 1 - compare the existing card-front layout with the approved raw art full bleed.
if args.full_art:
    # The art's 1060:1484 aspect ratio nearly matches A4; crop about 3pt per side.
    scale = max(W / 1060, H / 1484)
    image_width, image_height = 1060 * scale, 1484 * scale
    c.drawImage(str(ILLUSTRATION), (W-image_width)/2, (H-image_height)/2,
                width=image_width, height=image_height)
else:
    c.setFillColor(BLACK); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(.7); c.line(43, H-49, W-43, H-49)
    c.drawImage(str(LOGO), 43, H-43, width=104, height=48, preserveAspectRatio=True, mask='auto')
    c.setFont("DejaVu", 8); c.setFillColor(CREAM)
    c.drawRightString(W-43, H-32, "CRYPTO  /  SEASON ONE")
    label(c, "001 / 100    LEGENDARY    1982", 43, H-91)
    c.setFont("DejaVu-Bold", 43); c.setFillColor(CREAM)
    c.drawString(40, H-148, "BLIND SIGNATURES")
    c.drawImage(str(ART), 122, 142, width=351, height=478, preserveAspectRatio=True)
    c.setStrokeColor(GOLD); c.line(43, 125, W-43, 125)
    c.setFillColor(GOLD); c.setFont("DejaVu-Serif", 17)
    c.drawString(43, 94, "UNTRACEABLE PAYMENTS.")
    c.setFillColor(CREAM); c.setFont("DejaVu", 8)
    c.drawString(43, 67, "DAVID CHAUM  /  CRYPTO '82")
    c.drawRightString(W-43, 67, "EDITORIAL LAYOUT STUDY  -  01")
c.showPage()

# Page 2 - story, decoded artwork and source boundaries.
c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(43, H-57, W-43, H-57)
label(c, "LORE / CRYPTO SEASON ONE" if args.full_art else "LORE / THE STORY", 43, H-39, BLACK)
c.setFillColor(BLACK); c.setFont("DejaVu-Bold", 28)
c.drawString(43, H-102, "BLIND SIGNATURES" if args.full_art else "THE HIDDEN MESSAGE")
c.setFillColor(GREY); c.setFont("DejaVu", 9)
c.drawString(43, H-122, "001  /  1982  /  DAVID CHAUM  /  LEGENDARY" if args.full_art else "001  /  BLIND SIGNATURES  /  DAVID CHAUM")
if args.full_art:
    c.setFillColor(GOLD); c.setFont("DejaVu-Serif", 15)
    c.drawString(43, H-151, "UNTRACEABLE PAYMENTS.")

body = ParagraphStyle("body", fontName="DejaVu", fontSize=10.2, leading=15.2,
                      textColor=BLACK, spaceAfter=0)
egg = ParagraphStyle("egg", fontName="DejaVu", fontSize=9.4, leading=14.2,
                     textColor=BLACK)
note = ParagraphStyle("note", fontName="DejaVu", fontSize=8.4, leading=12.8,
                      textColor=GREY)
left, right, col = 43, 307, 242
y = H-(190 if args.full_art else 164)
story = [
    "Imagine taking a letter to someone whose signature you need. You want them to confirm it is valid, but you do not want them to read what is inside. In LORE's illustration, the envelope stays closed as the stamper lifts away. That gap between the signer and the hidden message is the idea behind a blind signature.",
    "In 1982, David Chaum presented <i>Blind Signatures for Untraceable Payments</i> at CRYPTO '82. The requester disguises a message; a signer signs the disguised version; and the requester removes the disguise. The result can still be verified against the original message, even though the signer did not see it at signing time.",
    "Chaum applied the idea to electronic payments. A bank could sign a digital payment token at withdrawal, then recognise a valid token when it was spent. Because the bank signed a blinded version, it could not simply match that later token to the particular one it saw at withdrawal. The card's line, <b>UNTRACEABLE PAYMENTS.</b>, expresses the aim of the proposed scheme. It does not mean every surrounding detail of a real payment is anonymous.",
    "The card freezes the instant after the seal is made. An old-fashioned envelope turns an abstract cryptographic move into a scene you can read at a glance.",
]
for part in story:
    y = paragraph(c, part, left, y, col, body, gap=13)
if y < 79: raise RuntimeError(f"Story column overflows: {y:.1f}")

label(c, "HIDDEN IN THE ART", right, H-(186 if args.full_art else 160), BLACK, 9)
z = H-(205 if args.full_art else 179)
clues = [
    ("01  THE FRESH SEAL", "The raised stamper and its shadow show the mark has just been made. The envelope stands for a message authenticated without being read."),
    ("02  THE CONCEALED SLIP", "The partly hidden payment slip points to the payment application: withdrawal and later spending need not be directly linked."),
    ("03  FADING FOOTPRINTS", "The trail breaks across the desk, a metaphor for the intended break in the transaction link. Other information can still compromise privacy."),
    ("04  THE DRAWER DIAGRAM", "The node sketch is a deliberate forward reference to the 2008 Bitcoin whitepaper, not a real object from Chaum's 1982 setting."),
]
for heading, copy in clues:
    label(c, heading, right, z, GOLD, 8.2)
    z = paragraph(c, copy, right, z-10, col, egg, gap=17)

c.setStrokeColor(GOLD); c.line(right, z+1, right+col, z+1)
label(c, "SOURCE & ART NOTE", right, z-18, BLACK, 8.2)
z = paragraph(c,
    "David Chaum, <i>Blind Signatures for Untraceable Payments</i>, Proceedings of CRYPTO '82, pp. 199-203. Chaum's publication list records 1982. The room, computer, envelope, drawer and characters are illustrative, not a reconstruction of his workspace.",
    right, z-30, col, note, gap=10)
z = paragraph(c,
    "Original paper: chaum.com/wp-content/uploads/2022/01/Chaum-blind-signatures.pdf",
    right, z, col, note)
if z < 80: raise RuntimeError(f"Clue column overflows: {z:.1f}")

c.setStrokeColor(GOLD); c.line(43, 57, W-43, 57)
c.setFont("DejaVu", 7.5); c.setFillColor(GREY)
c.drawString(43, 40, "BOOK WORDING AND PAGE DESIGN: REVIEW DRAFT")
c.drawRightString(W-43, 40, "002")
c.save()
print(f"{OUT} | story bottom {y:.1f} | clue bottom {z:.1f}")
