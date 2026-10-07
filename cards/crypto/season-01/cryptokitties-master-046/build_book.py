"""Build the two-page 046 book from verified text and approved art.

Layout is preserved from 045/044. Usage: python3 build_book.py --content-only
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
    "On 28 November 2017, Axiom Zen released CryptoKitties to the public on Ethereum. Players could collect and breed digital cats, paying with ether. The launch announcement aimed to make blockchain accessible through the power of fun: a playful introduction to a technical world.",
    "Each cat carried programmed traits. Pairing two cats produced a new one whose appearance drew on both parents. Players could explore combinations and see which features emerged. The breeding was a software mechanic, with smart contracts doing the work on Ethereum.",
    "The queues followed the launch. By early December, demand was putting pressure on the network. On 4 December, the CryptoKitties team reported congestion, recommended higher gas prices and raised the birthing fee. Players were encountering the cost and delay of completing their game's transactions on a busy blockchain.",
    "Developers from CryptoKitties, MetaMask, Infura and other projects worked on the response. Their later accounts describe growing pending-transaction queues and confused players. Status indicators and ways to resubmit transactions helped. A popular game had made Ethereum's capacity limits tangible to people using it.",
    "HISTROVE turns that experience into a workshop. Parent-trait cards hang beside a kitten's cradle; waiting cats fill a railway of baskets. PENDING tags crowd the counter, and a raised paw hovers above a pink hourglass. The left Ethereum box stays lit. This imagined scene joins the November launch to the congestion that followed in December."
]
eggs = [
    {'title': 'THE PARENT TRAIT CARDS', 'text': "PARENT A and PARENT B point towards a new kitten. They explain the game's trait-combination mechanic through an illustrated workshop diagram. The cards are invented props, and the breeding is a software process."},
    {'title': 'THE PENDING TAGS', 'text': "The stacked tags turn delayed transactions into a visible backlog. They refer to congestion in early December, after the 28 November launch. They do not represent lost kittens or documented delivery slips."},
    {'title': 'THE IMPATIENT PAW', 'text': "The raised paw and pink hourglass make waiting personal. This is a comic expression of the player's experience, not a recorded incident or a timer for the release of new cats."},
    {'title': 'THE STILL-LIT ETHEREUM BOX', 'text': "The illuminated box recalls Ethereum's first-light motif elsewhere in the collection. Its continuing glow links the game to the network beneath it: busy and under strain. The electrical box is a symbolic crossover, not historical equipment."}
]
sources = [
    {'title': 'Axiom Zen: launch release, 28 November 2017', 'url': 'https://www.prnewswire.com/news-releases/cryptokitties-the-worlds-first-ethereum-game-launches-today-660494083.html', 'supports': 'Public launch date, Axiom Zen developer attribution, Ethereum and ether, collecting and parent-trait breeding mechanic. The source subheading supplies the four-word phrase the power of fun. Marketing first-ever claims are not repeated.', 'type': 'PROJECT_PRESS_RELEASE', 'verified': '2026-10-07'},
    {'title': 'CryptoKitties: fee update, 4 December 2017', 'url': 'https://medium.com/cryptokitties/cryptokitties-birthing-fees-increases-in-order-to-accommodate-demand-acc314fcadf5', 'supports': 'Contemporaneous developer account of congestion, slow transactions, increased gas prices and birthing fees; explains the software breeding process. Establishes December conditions separately from November launch.', 'type': 'PROJECT_UPDATE', 'verified': '2026-10-07'},
    {'title': 'Consensys: developer interviews, 20 February 2018', 'url': 'https://consensys.io/blog/the-inside-story-of-the-cryptokitties-congestion-crisis', 'supports': 'First-person accounts from CryptoKitties, MetaMask, Infura and Grid+ contributors: pending queues, player confusion, collaboration, status indicators and resubmission improvements. Used for the congestion response, not the page introduction\'s imprecise launch dating.', 'type': 'PARTICIPANT_INTERVIEWS', 'verified': '2026-10-07'}
]
art_note = "28 November marks the public launch; the queue anticipates early December's congestion. The phrase is adapted from the launch-release subheading. All four workshop clues are artistic interpretations. The continuing light does not depict a network shutdown. Logo use is not a claim of endorsement or legal clearance."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '046.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '046-cryptokitties.md').write_text('# 046 - CryptoKitties\n\n28 NOV 2017 / ETHEREUM / EPIC\n\nTHE POWER OF FUN.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

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
FONTS = B.parents[2] / 'master/front-v3/source/fonts'
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-046-CryptoKitties-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 046 - CryptoKitties')
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
label('CRYPTOKITTIES', 43, H - 102, 22, '#0B0B0B')
label('046 / 28 NOV 2017 / ETHEREUM / EPIC', 43, H - 124, 8, '#5A574F')
label('THE POWER OF FUN.', 43, H - 153, 14)
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
label('046 / CRYPTOKITTIES', 43, 40, 7.5, '#5A574F')
label('092', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-046-CryptoKitties-Book-Spread.png')
reference_boxes = [[150, 119, 530, 505], [840, 647, 1050, 906], [319, 724, 519, 1018], [0, 99, 164, 359]]
boxes = [[round(x * iw / 1060) if k % 2 == 0 else round(x * ih / 1484) for k, x in enumerate(box)] for box in reference_boxes]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'046-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; same as 045/044', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '2017-11-28', 'congestion_period': 'early December 2017', 'rarity': 'epic', 'collector_number': '046/100', 'card_phrase': 'THE POWER OF FUN.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'logo_legal_clearance': 'Not established; artwork approval does not imply rights clearance', 'reference_layout': 'cards/crypto/season-01/the-missing-cryptoqueen-master-044/build_book.py via approved 045 book pipeline', 'reference_layout_commit': 'ac21a2bd4eb64c1fe2cb4d76a313a66c4901c323', 'reference_045_build_sha256': '431eb36f340e59b0aca67b3c7a89dd3a1da0a98fed1ba9c786a94a69349d58ec'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
