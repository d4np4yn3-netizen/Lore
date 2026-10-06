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
ART_SHA256 = '576e9b94275106918e77ea41720a21d127cee6cf92dd5e433c6388d490ec11ba'
assert hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256
story = [
    "On 24 August 2017, Segregated Witness, or SegWit, activated on Bitcoin at block 481,824. The soft-fork upgrade changed how transactions carry validation data and how block capacity is measured, while continuing Bitcoin's existing chain.",
    "SegWit moved signatures and related validation data into a separate witness structure. That witness remains part of Bitcoin's blockchain and is cryptographically committed through the block's coinbase transaction. Separating it from the data used to calculate a transaction's ID did not mean moving it off-chain.",
    "For transactions spending only SegWit inputs, the upgrade fixed nonintentional transaction-ID malleability: changing a signature could no longer change the txid. This made it easier to build reliable chains of unconfirmed transactions, an important foundation for payment-channel systems such as Lightning.",
    "SegWit also introduced a limit of 4,000,000 weight units per block. Base data counts four units per byte; witness data counts one. The extra usable capacity depends on the transaction mix. It is not a promise of four megabytes of ordinary transaction data or four times as many payments.",
    "The two bulls show Bitcoin before and after the upgrade. The smaller bull carries bundled paperwork; the larger one separates gold transaction tiles from blue witness channels. They represent one network evolving, not two rival coins. The lightning hints at technology built on that foundation later, and the stronger form makes no promise about price."
]
eggs = [
    {'title': 'THE 481,824 PLAQUE', 'text': "The stone plaque marks the Bitcoin block where SegWit became active on 24 August 2017. It anchors the transformation to a specific point in the chain."},
    {'title': 'THE BIP 141 PLATE', 'text': "The larger bull's armour names the Bitcoin Improvement Proposal defining SegWit's consensus rules, including its witness commitment and block-weight limit. It is a technical reference, not a manufacturer's badge."},
    {'title': 'GOLD AND BLUE CHANNELS', 'text': "Gold transaction tiles and blue witness channels make the data separation visible. Both belong to the same Bitcoin transaction and blockchain. The colours are an artistic key, not a literal protocol diagram."},
    {'title': 'THE LIGHTNING FORESHADOW', 'text': "The bolt and storm point toward Lightning payment channels. They foreshadow later development; Lightning Labs announced its first lnd mainnet beta in March 2018, after SegWit's activation."}
]
sources = [
    {'title': 'BIP 141: Segregated Witness', 'url': 'https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki', 'supports': 'Witness commitment, soft-fork compatibility and block weight'},
    {'title': 'Bitcoin Core: mainnet activation height', 'url': 'https://github.com/bitcoin/bitcoin/blob/master/src/kernel/chainparams.cpp', 'supports': 'SegwitHeight 481824 and its block hash'},
    {'title': 'Block 481,824 record', 'url': 'https://blockstream.info/block/0000000000000000001c8018d9cb3b742ef25114f27563e3fc4a1902167f9893', 'supports': 'Block height and timestamp of 24 August 2017'},
    {'title': 'Bitcoin Core: SegWit benefits', 'url': 'https://bitcoincore.org/en/2016/01/26/segwit-benefits/', 'supports': 'Malleability fix for transactions with all inputs spending SegWit outputs and Lightning implications'},
    {'title': 'Lightning Labs: lnd mainnet beta', 'url': 'https://lightning.engineering/posts/2018-03-15-lnd-beta/', 'supports': '15 March 2018 release, later than SegWit activation'}
]
art_note = "The bulls, armour, channels and storm are visual metaphors. BITCOIN UPGRADED. is editorial wording, not a quotation or a price prediction. No affiliation or endorsement is implied."
source_note = 'Sources: ' + '; '.join(f"[{s['title']}]({s['url']})" for s in sources) + '. ' + art_note
source_pdf = 'Sources: ' + '; '.join(f'<link href="{html.escape(s["url"], quote=True)}">{html.escape(s["title"])}</link>' for s in sources) + '. ' + html.escape(art_note)
content = {'story': story, 'eggs': eggs, 'sourceNote': source_note, 'sources': sources}
(B / '042.json').write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
(B / '042-segwit-activates.md').write_text('# 042 - SegWit Activates\n\n24 AUG 2017 / UNCOMMON\n\nBITCOIN UPGRADED.\n\n## The story\n\n' + '\n\n'.join(story) + '\n\n## Details in the artwork\n\n' + '\n'.join(f"{i}. **{e['title']}** {e['text']}" for i, e in enumerate(eggs, 1)) + '\n\n## Source and art note\n\n' + source_note + '\n')

for name, filename in [('DV', 'DejaVuSans.ttf'), ('DVB', 'DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, '/usr/share/fonts/truetype/dejavu/' + filename))
W, H = A4
out = B / 'HISTROVE-042-SegWit-Activates-Book.pdf'
c = canvas.Canvas(str(out), pagesize=A4, pageCompression=1)
c.setTitle('HISTROVE 042 - SegWit Activates')
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
label('SEGWIT ACTIVATES', 43, H - 102, 22, '#0B0B0B')
label('042 / 24 AUG 2017 / BTC / UNCOMMON', 43, H - 124, 8, '#5A574F')
label('BITCOIN UPGRADED.', 43, H - 153, 14)
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
label('042 / SEGWIT ACTIVATES', 43, 40, 7.5, '#5A574F')
label('084', W - 62, 40, 7.5, '#5A574F')
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
sheet.save(B / 'HISTROVE-042-Book-Preview.png')
qa = {'page_count': len(doc), 'page_size_points': [W, H], 'source_art_sha256': ART_SHA256, 'source_art_unmodified': hashlib.sha256(ART.read_bytes()).hexdigest() == ART_SHA256, 'story_column_bottom_points': y, 'clues_column_bottom_points': z, 'story_paragraphs': len(story), 'clue_count': len(eggs), 'linked_source_count': len(doc[1].get_links()), 'activation_timestamp_utc': datetime.fromtimestamp(1503539857, timezone.utc).isoformat(), 'editorial_line': 'BITCOIN UPGRADED.', 'pdf_sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'visual_review': 'Pending inspection of rendered pages'}
(B / 'book-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(qa, indent=2))
