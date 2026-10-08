"""Build the two-page 049 book from verified text and approved unchanged art.

Layout is preserved from 048 at 9e71c54b64212f955e6f85eaf40b5ab9f934ac30. Usage: python3 build_book.py --content-only
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
story = ['On 2 November 2018, the final day of Devcon 4 in Prague, Hayden Adams announced Uniswap and deployed its exchange contracts to Ethereum mainnet. After more than a year of development, a small application was ready to let people swap assets through on-chain code.', 'Uniswap V1 paired each supported ERC20 token with ETH. An exchange contract held reserves of both assets, and traders swapped against those reserves rather than a conventional order book. Token-to-token trades could pass through ETH as an intermediate step. Anyone could create an exchange for a token through the factory contract.', 'Prices followed a constant-product market-making rule, commonly written x*y=k. Adding one asset in a swap removed some of the other, changing the reserve ratio and the next price. Larger trades moved that ratio further. The equation is a simplified swap relationship: trading fees increase the reserve product, and liquidity deposits or withdrawals also change it.', "Liquidity providers supplied both assets, normally in the pool's current ratio, and received pool tokens recording their share. A 0.3% trading fee accumulated in the reserves for those providers. The unicorn in this scene pours into both chambers to suggest that paired contribution. These are two reserves of one illustrated pool, not two independent markets.", "HISTROVE imagines the protocol as an enchanted exchange engine in a vaulted hall. Its unicorn operator is an invented character, not a portrait of Adams or an official logo. The V1 plate and launch-date engraving anchor the fantasy to 2018. UNI, the later governance token, arrived in September 2020; V1's liquidity-share tokens were a different thing."]
eggs = [{'title': 'THE PAIRED RESERVES', 'text': "ETH and ERC20 label the two chambers. Together they represent one V1 exchange's paired reserves. Pouring into both suggests providing liquidity; a swap instead adds one asset and removes some of the other."}, {'title': 'THE CONSTANT-PRODUCT PLATE', 'text': 'The x*y=k engraving recalls the pricing rule. The reserve ratio changes as trades occur. Fees and liquidity changes affect the reserve product, so the inscription does not promise a fixed price or an unchanging k.'}, {'title': 'THE V1 BADGE', 'text': 'V1 identifies the original protocol generation. Its exchanges paired a token with ETH, and token-to-token swaps could route through ETH. The badge keeps the scene distinct from later Uniswap versions.'}, {'title': 'THE LAUNCH DATE', 'text': '2 NOV 2018 marks the public launch on Ethereum mainnet during Devcon 4 in Prague. It is visible on the engine in the full artwork and repeated at the top of the framed card.'}]
sources = [{'title': 'Hayden Adams: A Short History of Uniswap', 'url': 'https://blog.uniswap.org/uniswap-history', 'supports': '2 November 2018 mainnet announcement; Devcon 4 in Prague; development history and x*y=k background.', 'type': 'PROJECT_CREATOR_HISTORY', 'verified': '2026-10-08'}, {'title': 'Uniswap V1: original overview', 'url': 'https://github.com/Uniswap/v1-docs/blob/3d71d5d7e0ffefd08596de29b7630fe9744721d2/README.md', 'supports': 'ETH-ERC20 exchange contracts, factory, paired reserves, token-to-token routing via ETH, constant-product pricing and 0.3% liquidity-provider fee.', 'type': 'ORIGINAL_PROTOCOL_DOCUMENTATION', 'verified': '2026-10-08'}, {'title': 'Uniswap V1: pool liquidity', 'url': 'https://github.com/Uniswap/v1-docs/blob/3d71d5d7e0ffefd08596de29b7630fe9744721d2/frontend-integration/pool.md', 'supports': 'Reserve definitions; paired asset deposits at the existing ratio; initial-provider exception; liquidity tokens and proportional withdrawals.', 'type': 'ORIGINAL_PROTOCOL_DOCUMENTATION', 'verified': '2026-10-08'}, {'title': 'Uniswap V1: exchange contract', 'url': 'https://github.com/Uniswap/v1-contracts/blob/master/contracts/uniswap_exchange.vy', 'supports': 'addLiquidity/removeLiquidity change reserves; getInputPrice applies the 997/1000 fee factor. Pool tokens are distinct from the later governance token.', 'type': 'ORIGINAL_PROTOCOL_CODE', 'verified': '2026-10-08'}, {'title': 'Uniswap Labs: Introducing UNI', 'url': 'https://blog.uniswap.org/uni', 'supports': 'Governance-token introduction dated 16 September 2020, separate from the 2018 V1 launch and liquidity-share tokens.', 'type': 'PROJECT_ANNOUNCEMENT', 'verified': '2026-10-08'}]
art_note = 'The unicorn, hall and machine are original allegory, not a historical scene, a technical diagram or an official Uniswap logo. LIQUIDITY, PAIRED. is the approved editorial caption describing the paired-reserve concept; it is not a historical quotation.'
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '049.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / 'sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / '049-uniswap-launches.md').write_text('# 049 - Uniswap Launches\n\n02 NOV 2018 / ETHEREUM / LEGENDARY\n\nLIQUIDITY, PAIRED.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

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
out = B / 'HISTROVE-049-Uniswap-Launches-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1, invariant=1)
c.setTitle('HISTROVE 049 - Uniswap-Launches')
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
label('UNISWAP LAUNCHES', 43, H - 102, 22, '#0B0B0B')
label('049 / 02 NOV 2018 / ETHEREUM / LEGENDARY', 43, H - 124, 8, '#5A574F')
label('LIQUIDITY, PAIRED.', 43, H - 153, 14)
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
label('049 / UNISWAP LAUNCHES', 43, 40, 7.5, '#5A574F')
label('098', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-049-Uniswap-Launches-Book-Spread.png')
reference_boxes = [[270, 778, 800, 992], [434, 1026, 631, 1096], [480, 983, 585, 1031], [447, 1160, 618, 1209]]
boxes = [[round(x * iw / 1060) if k % 2 == 0 else round(x * ih / 1484) for k, x in enumerate(box)] for box in reference_boxes]
closeups = {'source_dimensions': [iw, ih], 'boxes': boxes, 'titles': [e['title'] for e in eggs]}
(B / 'closeup-boxes.json').write_text(json.dumps(closeups, indent=2) + '\n')
CROPS = B / 'closeups'; CROPS.mkdir(exist_ok=True)
for n, box in enumerate(boxes, 1):
    Image.open(ART).crop(box).save(CROPS / f'049-detail-{n}.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_dimensions_px': [iw, ih], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'native_effective_ppi': 72 / scale, 'art_fit': 'Contain proportional full artwork with black edge bars; unchanged 048 layout', 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'source_count': len(sources), 'linked_source_annotations': len(doc[1].get_links()), 'event_date': '2018-11-02', 'rarity': 'legendary', 'collector_number': '049/100', 'card_phrase': 'LIQUIDITY, PAIRED.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages', 'physical_print_acceptance': 'Not claimed', 'logo_legal_clearance': 'Not established; artwork approval does not imply rights clearance', 'reference_layout': 'cards/crypto/season-01/lightning-goes-live-master-048/build_book.py', 'reference_layout_commit': '9e71c54b64212f955e6f85eaf40b5ab9f934ac30', 'reference_048_build_sha256': '6125ff644b42c1be45718389f636ad5276868b3979eebf14e364774f2f4e3418'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))


