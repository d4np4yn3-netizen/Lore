"""Build the two-page 048 book from verified text and approved unchanged art.

Layout is preserved from 047 at f7713fc954cecdbe94295a02bef380b9a746a72d. Usage: python3 build_book.py --content-only
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
story = ["On 15 March 2018, Lightning Labs released lnd 0.4-beta, its first mainnet beta. The software now offered an option to run on Bitcoin's live network with real funds. This card marks that release milestone; Lightning's proposal and earlier experiments already existed.", 'Lightning begins with funded payment channels. An opening transaction commits bitcoin on the blockchain. The two participants can then update their balances between themselves, making repeated payments without recording every update on-chain. Closing a channel settles its balance on the blockchain, which remains the foundation for enforcing the arrangement.', 'A payment can also travel through linked channels to someone beyond a direct partner. Conditional transfers connect the steps, while onion routing limits what each forwarding node learns about the route. Available channel funds and routing fees still matter. The aim is faster, lower-cost payments, not unlimited or free transfers.', 'The beta was aimed at application developers, technical users and prospective routing-node operators. It brought stronger fault handling and improved route finding, but Lightning Labs urged people to experiment with small amounts. The announcement looked ahead to friendlier applications and more infrastructure: this was an early network still being built.', 'HISTROVE turns that moment into a storm-to-Earth allegory. An invented guardian channels golden light toward a web of connections below; paired Bitcoin clasps, a release plaque and a date tag carry the historical clues. The figure represents no real person or central controller, and the scene is not an engineering demonstration.']
eggs = [{'title': 'THE BETA PLAQUE', 'text': "The chest plaque reads lnd 0.4-beta. It identifies the specific software release, anchoring the scene to Lightning Labs' first mainnet beta rather than the invention of Lightning itself."}, {'title': 'THE HANGING DATE', 'text': "The tag reads 15 MAR 2018, the release announcement's date. It records this milestone, not the date of the first Lightning idea or the first payment ever made."}, {'title': 'THE BITCOIN CLASPS', 'text': "Two Bitcoin clasp halves are joined by light. They suggest the two participants in a funded channel, whose balances can change off-chain while their channel remains anchored to Bitcoin's blockchain."}, {'title': 'THE SPHINX BRACER', 'text': 'The engraved Sphinx nods to the Sphinx-derived packet format used for Lightning onion routing. Layered instructions guide a payment through its route. The mythical engraving is an artistic clue, not actual networking equipment.'}]
sources = [{'title': 'Lightning Labs: mainnet beta announcement', 'url': 'https://lightning.engineering/posts/2018-03-15-lnd-beta/', 'supports': "15 March 2018 date; lnd 0.4-beta as Lightning Labs' first mainnet beta; technical-user audience; small-amounts caution; fault handling and route finding; Beyond Beta opening contains the continuous words 'the very beginning'.", 'type': 'PROJECT_ANNOUNCEMENT', 'verified': '2026-10-08'}, {'title': 'lnd v0.4-beta release notes', 'url': 'https://github.com/lightningnetwork/lnd/releases/tag/v0.4-beta', 'supports': "Specific release and mainnet flag, compatibility and reliability work, routing updates and fees. Its reference to closing prior channels confirms this milestone should not be represented as Lightning's first-ever payment.", 'type': 'PROJECT_RELEASE_NOTES', 'verified': '2026-10-08'}, {'title': 'Poon and Dryja: Lightning whitepaper', 'url': 'https://lightning.network/lightning-network-paper.pdf', 'supports': 'Historical proposal, funded payment channels, off-chain balance updates, on-chain settlement and enforcement, and conditional transfers across multiple channels. Used for the broad channel model, not to claim every draft implementation detail shipped in March 2018.', 'type': 'ORIGINAL_TECHNICAL_WHITEPAPER', 'verified': '2026-10-08'}, {'title': 'lightning-onion: historical Sphinx design', 'url': 'https://github.com/lightningnetwork/lightning-onion/blob/6d4b1353e2835def84ee240f40499464521c6046/README.md', 'supports': 'Exact lightning-onion revision used by lnd v0.4-beta explains a Sphinx-derived message format, onion routing and per-hop forwarding instructions.', 'type': 'PROJECT_TECHNICAL_DOCUMENTATION', 'verified': '2026-10-08'}, {'title': 'lnd v0.4-beta: dependency record', 'url': 'https://github.com/lightningnetwork/lnd/blob/v0.4-beta/Gopkg.lock', 'supports': 'Pins lightningnetwork/lightning-onion at revision 6d4b1353e2835def84ee240f40499464521c6046, establishing that the cited Sphinx-derived design was present for this release.', 'type': 'PROJECT_RELEASE_DEPENDENCY_RECORD', 'verified': '2026-10-08'}]
art_note = "The guardian and storm-to-Earth scene are allegory, not a real person or technical demonstration. THE VERY BEGINNING. uses continuous words from the announcement's Beyond Beta opening, with capitals and a final full stop added for the card."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '048.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '048-lightning-goes-live.md').write_text('# 048 - Lightning Goes Live\n\n15 MAR 2018 / BITCOIN / UNCOMMON\n\nTHE VERY BEGINNING.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

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
FONTS = next(p for p in [B.parents[2] / 'master/front-v3/source/fonts', B.parent / 'card-proof/build-repo/cards/master/front-v3/source/fonts', B / 'canonical-dependencies/cards/master/front-v3/source/fonts'] if p.is_dir())
for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
W, H = A4
out = B / 'HISTROVE-048-Lightning-Goes-Live-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 048 - Lightning-Goes-Live')
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
label('LIGHTNING GOES LIVE', 43, H - 102, 22, '#0B0B0B')
label('048 / 15 MAR 2018 / BITCOIN / UNCOMMON', 43, H - 124, 8, '#5A574F')
label('THE VERY BEGINNING.', 43, H - 153, 14)
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
label('048 / LIGHTNING GOES LIVE', 43, 40, 7.5, '#5A574F')
label('096', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-048-Lightning-Goes-Live-Book-Spread.png')
reference_boxes = [[412, 376, 536, 459], [432, 636, 522, 774], [510, 429, 646, 534], [151, 465, 348, 641]]
boxes = [[round(x * iw / 1060) if k % 2 == 0 else round(x * ih / 1484) for k, x in enumerate(box)] for box in reference_boxes]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'048-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; unchanged 047 layout', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '2018-03-15', 'rarity': 'uncommon', 'collector_number': '048/100', 'card_phrase': 'THE VERY BEGINNING.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'logo_legal_clearance': 'Not established; artwork approval does not imply rights clearance', 'reference_layout': 'cards/crypto/season-01/dai-goes-live-master-047/build_book.py', 'reference_layout_commit': 'f7713fc954cecdbe94295a02bef380b9a746a72d', 'reference_047_build_sha256': 'f9c22c272f9f320d9f70994fadf594b9c900665008668cd27eb45d591d1cf2c5'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))


