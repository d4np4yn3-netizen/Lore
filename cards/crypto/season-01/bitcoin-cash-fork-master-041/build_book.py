from pathlib import Path
import json,html,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import fitz
B=Path(__file__).resolve().parent
story=["On 1 August 2017, a long-running argument over Bitcoin's capacity produced a lasting split. Bitcoin and Bitcoin Cash shared the same transaction history through block 478,558. After that common point, their networks began extending separate chains under different rules.", "The disagreement was about how to serve more users. Supporters of larger blocks wanted more payments recorded directly on the blockchain. Bitcoin Cash launched with an 8 MB block-size limit, allowing larger batches of transactions than Bitcoin's existing rules permitted.", "Others worried that sharply increasing the data processed by the network would make it harder for ordinary users to run a fully validating node. Bitcoin's alternative scaling path included Segregated Witness and payment-channel technology. SegWit's activation was a separate event later that August, not the Bitcoin Cash split itself.", "Because the chains inherited a common ledger, a person controlling the private keys for coins before the split could generally control corresponding balances on both networks. Custodial users depended on their provider's support. Two balances did not mean the market value of their holdings had doubled.", 'The artwork turns the disagreement into two routes through one city. The matching ledgers hold a common past; the gateways lead toward different futures. The fictional engineers and capacity plans describe competing priorities, without declaring either community fraudulent or reducing the debate to a fight between heroes and villains.']
eggs=[{'title': 'THE SHARED BLOCK', 'text': '478,558 is the last common block. The plaque marks the shared history before the two chains diverged; it is not the number of Bitcoin Cash’s first distinct block.'}, {'title': 'THE 8 MB PLAQUE', 'text': 'This refers to Bitcoin Cash’s initial block-size limit in August 2017, not its present limit, a transaction count or a guarantee of speed.'}, {'title': 'THE MATCHING LEDGERS', 'text': 'Identical books symbolise the common transaction record inherited by both networks. No real historical books or physical coin duplication are claimed.'}, {'title': 'THE CAPACITY PLANS', 'text': 'Both drawings show a linear sequence of blocks. Larger boxes and more slips on the BCH plan illustrate extra capacity. They are not to scale or literal software diagrams, and do not imply a different block interval.'}]
source='Sources: <link href="https://www.irs.gov/pub/irs-wd/202114020.pdf">IRS memorandum: Bitcoin / Bitcoin Cash hard-fork background</link>; <link href="https://docs.bitcoincashnode.org/doc/bch-upgrades/">Bitcoin Cash Node upgrade documentation</link>; <link href="https://bitcoincore.org/en/2015/12/07/roadmap/">Bitcoin Core capacity roadmap</link>. The fictional city, people, books and plans are visual metaphors. ONE PAST. TWO PATHS. is editorial wording, not a quotation. No affiliation or endorsement is implied.'
content={'story':story,'eggs':eggs,'sourceNote':source.replace('<link href="','<a href="').replace('</link>','</a>')}
# Website uses plain Markdown for clickable source links.
import re
content['sourceNote']=re.sub(r'<link href="([^"]+)">(.*?)</link>',r'[\2](\1)',source)
(B/'041.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
md='# 041 - Bitcoin Cash Fork\n\n01 AUG 2017 / UNCOMMON\n\nONE PAST. TWO PATHS.\n\n## The story\n\n'+'\n\n'.join(story)+'\n\n## Details in the artwork\n\n'+'\n'.join(f"{i}. **{e['title']}** {e['text']}" for i,e in enumerate(eggs,1))+'\n\n## Source and art note\n\n'+content['sourceNote']+'\n'
(B/'041-bitcoin-cash-fork.md').write_text(md)
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
W,H=A4;out=B/'HISTROVE-041-Bitcoin-Cash-Fork-Book.pdf';c=canvas.Canvas(str(out),pagesize=A4,pageCompression=1);c.setTitle('HISTROVE 041 - Bitcoin Cash Fork');c.setAuthor('HISTROVE')
art=B/'art.png';iw,ih=Image.open(art).size;s=min(W/iw,H/ih);c.setFillColor(HexColor('#0B0B0B'));c.rect(0,0,W,H,fill=1,stroke=0);c.drawImage(str(art),(W-iw*s)/2,(H-ih*s)/2,width=iw*s,height=ih*s);c.showPage()
c.setFillColor(HexColor('#F5F2EB'));c.rect(0,0,W,H,fill=1,stroke=0)
def label(txt,x,y,size=9,color='#886615'):
 c.setFillColor(HexColor(color));c.setFont('DVB',size);c.drawString(x,y,txt)
def para(txt,x,y,w,fs=9.3,leading=13.8):
 p=Paragraph(txt,ParagraphStyle('p',fontName='DV',fontSize=fs,leading=leading,textColor=HexColor('#171717')));_,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h-10
label('HISTROVE / CRYPTO SEASON ONE',43,H-39,9,'#0B0B0B');c.setStrokeColor(HexColor('#886615'));c.line(43,H-57,W-43,H-57)
label('BITCOIN CASH FORK',43,H-102,22,'#0B0B0B');label('041 / 01 AUG 2017 / BTC / BCH / UNCOMMON',43,H-124,8,'#5A574F');label('ONE PAST. TWO PATHS.',43,H-153,14)
y=H-188
for p in story:y=para(html.escape(p),43,y,242)
z=H-188;label('DETAILS IN THE ART',307,z,9,'#0B0B0B');z-=20
for i,e in enumerate(eggs,1):label(f"{i:02}  {e['title']}",307,z,7.8);z=para(html.escape(e['text']),307,z-11,242,8.7,12.5)
label('SOURCE & ART NOTE',307,z-8,8,'#0B0B0B');z=para(source,307,z-21,242,7.2,10.3)
assert min(y,z)>72,(y,z)
c.line(43,57,W-43,57);label('041 / BITCOIN CASH FORK',43,40,7.5,'#5A574F');label('082',W-62,40,7.5,'#5A574F');c.save()
d=fitz.open(out)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(B/f'book-page-{i+1}.png'))
a=Image.open(B/'book-page-1.png');b=Image.open(B/'book-page-2.png');sheet=Image.new('RGB',(a.width+b.width,a.height),'white');sheet.paste(a,(0,0));sheet.paste(b,(a.width,0));sheet.save(B/'HISTROVE-041-Book-Preview.png')
print('Book two pages; column bottoms',y,z)
