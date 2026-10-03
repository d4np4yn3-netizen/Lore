from pathlib import Path
import base64, hashlib, json, os, subprocess, xml.etree.ElementTree as ET
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"lore-022/prep/python-deps"))
import qrcode
from PIL import Image, ImageFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
WORK=ROOT.parents[1]
FONT=WORK/'lore-022/cards/master/front-v3/source'
ART=ROOT/'art.png'
OUT=ROOT/'LORE-Crypto-030-The-Dollar-Token-Uncommon-Print-v1'
S='http://www.w3.org/2000/svg'; X='http://www.w3.org/1999/xlink'
ET.register_namespace('',S); ET.register_namespace('xlink',X)
root=ET.parse(HERE/'uncommon.svg').getroot()
nodes={n.get('id'):n for n in root.iter() if n.get('id')}
values={'creator-name':'REALCOIN','title-line-1':'THE DOLLAR','title-line-2':'TOKEN','moment-context':'THE DOLLAR GOES DIGITAL.','moment-number':'06 OCT 2014','set-number':'CRYPTO • SEASON 01 • 030/100'}
for key,value in values.items():
 n=nodes[key]
 f=ImageFont.truetype(str(FONT/'fonts'/('DejaVuSans-Bold.ttf' if n.get('font-weight')=='700' else 'DejaVuSans.ttf')),int(n.get('font-size')))
 width=f.getlength(value)+float(n.get('letter-spacing','0'))*(len(value)-1)
 assert float(n.get('x'))+width<=620,(key,width)
 n.text=value
nodes['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(ART.read_bytes()).decode())
payload='https://lore-site-v1.vercel.app/crypto/030/'
code=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8)
code.add_data(payload);code.make(fit=True)
matrix=code.get_matrix();size=len(matrix)
qr=nodes['moment-qr'];qr.set('viewBox',f'0 0 {size} {size}')
for n in list(qr):qr.remove(n)
ET.SubElement(qr,'{'+S+'}rect',{'width':str(size),'height':str(size),'fill':'#FFFFFF'})
d=' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v)
ET.SubElement(qr,'{'+S+'}path',{'d':d,'fill':'#000000'})
nodes['qr-caption'].text='SCAN TO DISCOVER'
ET.ElementTree(root).write(OUT.with_suffix('.svg'),encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(FONT/'fontconfig.xml')
subprocess.run(['inkscape',str(OUT.with_suffix('.svg')),'--export-type=png',f'--export-filename={OUT.with_suffix(".png")}'],env=env,check=True,capture_output=True)
with Image.open(OUT.with_suffix('.png')) as im:
 assert im.size==(816,1110)
 im.convert('RGB').save(OUT.with_suffix('.png'),dpi=(300,300))
tmp=HERE/'card-intermediate.pdf'
c=canvas.Canvas(str(tmp),pagesize=(195.84,266.4),pageCompression=1,invariant=1)
c.setTitle('LORE 030 The Dollar Token - Uncommon Print v1')
c.setAuthor('LORE')
c.drawImage(str(OUT.with_suffix('.png')),0,0,width=195.84,height=266.4);c.showPage();c.save()
r=PdfReader(tmp);w=PdfWriter();w.add_page(r.pages[0]);w.pages[0].trimbox=RectangleObject([8.64,8.64,187.2,257.76]);w.add_metadata({'/Title':'LORE 030 The Dollar Token - Uncommon Print v1','/Author':'LORE'})
with OUT.with_suffix('.pdf').open('wb') as f:w.write(f)
print(OUT.with_suffix('.png'))
print('Original art SHA256',hashlib.sha256(ART.read_bytes()).hexdigest())
