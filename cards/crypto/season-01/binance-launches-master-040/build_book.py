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
story=["On 14 July 2017, Changpeng Zhao and a team that included colleagues from his earlier company, Bijie Tech, launched Binance. They brought experience building exchange software to a new task: operating a cryptocurrency exchange of their own.","The launch followed the BNB token sale. Binance's announcement of 8 July recorded the issuance of 100 million BNB for the ICO. BNB and the exchange were closely linked from the beginning, but the token sale and the opening of trading were separate events.","This was a small startup, not the vast institution the name would later suggest. Binance's own retrospective describes a founding team of approximately 30 people, mostly former software engineers, initially providing crypto-to-crypto spot trading.","The illustration brings that beginning back to human scale. CZ opens a glass door into an ordinary reception area: a counter, plants, ceiling lights and colleagues working beyond it. The composition draws on surviving office-tour footage, while the welcoming pose, warm light and small props are artistic staging.","Binance's first months also brought disruption. In his later account, Zhao describes the September 2017 restrictions in China and the team's departure. This card stays with the opening chapter, before that relocation and the exchange's later global growth."]
eggs=[{'title':'THE BNB FOLDER','text':'BNB / ICO 2017 connects the new exchange to the preceding token sale. The folder is an illustrative prop, not an authenticated company document.'},{'title':'THE JULY CALENDAR','text':'July 2017 anchors the launch month. The card date, 14 July, is supported by Zhao’s retrospective; the calendar is invented staging.'},{'title':'BUY BITCOIN','text':'The yellow note is a deliberate callback to card 039 and its handwritten sign. It is not claimed to have appeared in the real office.'},{'title':'THE MODEST RECEPTION','text':'The glass doorway, counter, wall sign and plants draw on office-tour footage. This environmental detail recalls the startup’s small beginnings; the footage’s exact recording date and address are unverified.'}]
source='Sources: <link href="https://www.binance.com/en/blog/from-our-ceo/2386330931319516973">CZ’s 2022 account</link>; <link href="https://www.binance.com/en/support/announcement/detail/115000574131">BNB issuance announcement, 8 July 2017</link>; <link href="https://www.binance.com/en/blog/ecosystem/1968152125579137703">Binance’s 2023 founding-team retrospective</link>; <link href="https://www.binance.com/en/square/post/1186706">reposted office-tour footage</link>. The scene is an artistic interpretation, not a photograph of launch day. OPEN FOR THE WORLD. is editorial wording, not a quotation. Binance marks belong to their owner; no affiliation, endorsement or rights clearance is implied. Commercial rights and physical-print review remain outstanding.'
content={'story':story,'eggs':eggs,'sourceNote':source.replace('<link href="','<a href="').replace('</link>','</a>')}
# Website uses plain Markdown for clickable source links.
import re
content['sourceNote']=re.sub(r'<link href="([^"]+)">(.*?)</link>',r'[\2](\1)',source)
(B/'040.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
md='# 040 - Binance Launches\n\n14 JUL 2017 / UNCOMMON\n\nOPEN FOR THE WORLD.\n\n## The story\n\n'+'\n\n'.join(story)+'\n\n## Details in the artwork\n\n'+'\n'.join(f"{i}. **{e['title']}** {e['text']}" for i,e in enumerate(eggs,1))+'\n\n## Source and art note\n\n'+content['sourceNote']+'\n'
(B/'040-binance-launches.md').write_text(md)
for n,f in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
W,H=A4;out=B/'HISTROVE-040-Binance-Launches-Book.pdf';c=canvas.Canvas(str(out),pagesize=A4,pageCompression=1);c.setTitle('HISTROVE 040 - Binance Launches');c.setAuthor('HISTROVE')
art=B/'HISTROVE-040-Shanghai-Office-Art-Proof-03.png';iw,ih=Image.open(art).size;s=min(W/iw,H/ih);c.setFillColor(HexColor('#0B0B0B'));c.rect(0,0,W,H,fill=1,stroke=0);c.drawImage(str(art),(W-iw*s)/2,(H-ih*s)/2,width=iw*s,height=ih*s);c.showPage()
c.setFillColor(HexColor('#F5F2EB'));c.rect(0,0,W,H,fill=1,stroke=0)
def label(txt,x,y,size=9,color='#886615'):
 c.setFillColor(HexColor(color));c.setFont('DVB',size);c.drawString(x,y,txt)
def para(txt,x,y,w,fs=9.3,leading=13.8):
 p=Paragraph(txt,ParagraphStyle('p',fontName='DV',fontSize=fs,leading=leading,textColor=HexColor('#171717')));_,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h-10
label('HISTROVE / CRYPTO SEASON ONE',43,H-39,9,'#0B0B0B');c.setStrokeColor(HexColor('#886615'));c.line(43,H-57,W-43,H-57)
label('BINANCE LAUNCHES',43,H-102,22,'#0B0B0B');label('040 / 14 JUL 2017 / CHANGPENG ZHAO / UNCOMMON',43,H-124,8,'#5A574F');label('OPEN FOR THE WORLD.',43,H-153,14)
y=H-188
for p in story:y=para(html.escape(p),43,y,242)
z=H-188;label('DETAILS IN THE ART',307,z,9,'#0B0B0B');z-=20
for i,e in enumerate(eggs,1):label(f"{i:02}  {e['title']}",307,z,7.8);z=para(html.escape(e['text']),307,z-11,242,8.7,12.5)
label('SOURCE & ART NOTE',307,z-8,8,'#0B0B0B');z=para(source,307,z-21,242,7.2,10.3)
assert min(y,z)>72,(y,z)
c.line(43,57,W-43,57);label('040 / BINANCE LAUNCHES',43,40,7.5,'#5A574F');label('080',W-62,40,7.5,'#5A574F');c.save()
d=fitz.open(out)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(str(B/f'book-page-{i+1}.png'))
a=Image.open(B/'book-page-1.png');b=Image.open(B/'book-page-2.png');sheet=Image.new('RGB',(a.width+b.width,a.height),'white');sheet.paste(a,(0,0));sheet.paste(b,(a.width,0));sheet.save(B/'HISTROVE-040-Book-Preview.png')
print('Book two pages; column bottoms',y,z)
