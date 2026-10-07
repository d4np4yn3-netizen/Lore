"""Build the two-page 047 book from verified text and approved unchanged art.

Layout is preserved from 046/045/044. Usage: python3 build_book.py --content-only
or python3 build_book.py after art.png and art-provenance.json are supplied.
"""
from pathlib import Path
import argparse
import json
import html
import hashlib
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
story = [
    "On 18 December 2017, MakerDAO launched Dai on the Ethereum mainnet. The original Single-Collateral Dai system made a dollar-targeting cryptocurrency available to use, with Ether providing the backing. Its launch announcement supplied the simple headline on this card: Dai is now live!",
    "Creating Dai began with collateral. Ether was pooled into PETH, which could be deposited in a Collateralized Debt Position, or CDP. Generating Dai created a corresponding debt and locked the collateral. A user needed to repay the debt and the applicable stability fee before recovering all the collateral.",
    "The system required collateral worth more than the debt it supported. That buffer mattered because Ether's price could move sharply. Risk parameters and liquidation mechanisms were part of the design. Dai's one-dollar target was a soft peg, maintained through the system's incentives and controls rather than an unconditional guarantee.",
    "For people using Ethereum, the launch offered a different kind of asset to send, spend or build applications around. The unit aimed to stay near a familiar dollar value even while the collateral beneath it fluctuated. This card marks the first production system, before the later expansion to multiple collateral types.",
    "HISTROVE imagines that engineering challenge as a glass experiment. A professor pours violet and gold into connected vessels; a locked valve and a dollar-target dial sit between them. The larger violet column suggests a collateral buffer. The character, liquids and apparatus are symbolic, not a portrait or a literal diagram of how Dai was created."
]
eggs = [
    {
        "title": "THE PETH VESSEL",
        "text": "The violet vessel names Pooled Ether, the collateral used by the original system. Its larger volume suggests overcollateralisation, without claiming that the artwork measures a fixed collateral ratio."
    },
    {
        "title": "THE CDP LOCK",
        "text": "The padlock marked CDP stands for a Collateralized Debt Position. It points to collateral locked while Dai debt is outstanding. The valve and padlock are invented visual shorthand for smart contracts."
    },
    {
        "title": "THE ONE-DOLLAR TARGET",
        "text": "The central dial explicitly says TARGET $1. It represents Dai's soft peg, not a promise that its market price could never move away from one dollar."
    },
    {
        "title": "THE MAINTENANCE WRENCH",
        "text": "The wrench at the lower right suggests ongoing risk management and parameter decisions. It is an artistic prop, not documented equipment. See the full illustration for this detail beneath the card's title area."
    }
]
sources = [
    {
        "title": "MakerDAO: Dai is now live, 18 December 2017",
        "url": "https://medium.com/@MakerDAO/dai-is-now-live-ad87e34fc826",
        "supports": "Launch date, Ethereum mainnet launch, Ether-backed CDPs and exact heading 'Dai is now live!' used in uppercase on the card.",
        "type": "PROJECT_ANNOUNCEMENT",
        "verified": "2026-10-07"
    },
    {
        "title": "MakerDAO: original Dai Stablecoin System whitepaper",
        "url": "https://makerdao.com/en/whitepaper/sai/",
        "supports": "Single-Collateral Dai sections: PETH, CDPs and debt, excess collateral, target price and risk management. The historical page also discusses future Multi-Collateral Dai features; those are not attributed to the 2017 launch.",
        "type": "PROJECT_TECHNICAL_WHITEPAPER",
        "verified": "2026-10-07"
    }
]
art_note = "The professor and glass experiment are artistic interpretations. Liquid mixing is not Dai's technical mechanism. The $1 figure is a soft-peg target, not a guarantee. The phrase reproduces the launch headline in capitals."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '047.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '047-dai-goes-live.md').write_text('# 047 - Dai-Goes-Live\n\n18 DEC 2017 / MAKERDAO / RARE\n\nDAI IS NOW LIVE!\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

parser = argparse.ArgumentParser()
parser.add_argument('--content-only', action='store_true')
args = parser.parse_args()
if args.content_only:
    print(json.dumps({'story_words': sum(len(p.split()) for p in story), 'clue_count': len(eggs), 'source_count': len(sources)}))
    raise SystemExit(0)

art_provenance = json.loads((B / 'art-provenance.json').read_text())
ART_SHA256 = art_provenance['sha256']
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
assert art_provenance['approval_condition_met'] is True
FONTS = next(p for p in [B.parents[2] / 'master/front-v3/source/fonts', B.parent / 'build-repo/cards/master/front-v3/source/fonts', B / 'canonical-dependencies/cards/master/front-v3/source/fonts'] if p.is_dir())
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-047-Dai-Goes-Live-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 047 - Dai-Goes-Live')
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
label('DAI GOES LIVE', 43, H - 102, 22, '#0B0B0B')
label('047 / 18 DEC 2017 / MAKERDAO / RARE', 43, H - 124, 8, '#5A574F')
label('DAI IS NOW LIVE!', 43, H - 153, 14)
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
label('047 / DAI GOES LIVE', 43, 40, 7.5, '#5A574F')
label('094', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-047-Dai-Goes-Live-Book-Spread.png')
reference_boxes = [[310, 505, 487, 896], [232, 888, 407, 1055], [510, 656, 664, 817], [682, 1213, 1022, 1370]]
boxes = [[round(x * iw / 1060) if k % 2 == 0 else round(x * ih / 1484) for k, x in enumerate(box)] for box in reference_boxes]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'047-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; same as 045/044', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '2017-12-18', 'rarity': 'rare', 'collector_number': '047/100', 'card_phrase': 'DAI IS NOW LIVE!', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'logo_legal_clearance': 'Not established; artwork approval does not imply rights clearance', 'reference_layout': 'cards/crypto/season-01/the-missing-cryptoqueen-master-044/build_book.py via approved 045 book pipeline', 'reference_layout_commit': 'ac21a2bd4eb64c1fe2cb4d76a313a66c4901c323', 'reference_045_build_sha256': '431eb36f340e59b0aca67b3c7a89dd3a1da0a98fed1ba9c786a94a69349d58ec'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))

