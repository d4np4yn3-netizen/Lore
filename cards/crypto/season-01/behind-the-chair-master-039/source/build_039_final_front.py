"""Assemble unchanged approved native art in the locked LORE Common print template."""
from pathlib import Path
import base64, hashlib, json, os, subprocess, xml.etree.ElementTree as ET
import argparse
import qrcode
from PIL import Image, ImageFont
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FONT=HERE
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, default=HERE/'rebuilt')
args=parser.parse_args()
args.output_dir.mkdir(parents=True,exist_ok=True)
ART=ROOT/'art.png'
OUT=args.output_dir/'LORE-Crypto-039-Behind-the-Chair-Common-Print-v1'
EXPECTED='c6944000f8ff929d6d793db39aeb994e3befc2300a554e0e2f6a7279f7c79239'
assert hashlib.sha256(ART.read_bytes()).hexdigest()==EXPECTED
S='http://www.w3.org/2000/svg'; X='http://www.w3.org/1999/xlink'
ET.register_namespace('',S); ET.register_namespace('xlink',X)
root=ET.parse(HERE/'common.svg').getroot()
nodes={n.get('id'):n for n in root.iter() if n.get('id')}
values={'creator-name':'BITCOIN','title-line-1':'BEHIND','title-line-2':'THE CHAIR','moment-context':'BUY BITCOIN.','moment-number':'12 JUL 2017','set-number':'CRYPTO • SEASON 01 • 039/100'}
widths={}
for key,value in values.items():
 n=nodes[key]
 f=ImageFont.truetype(str(FONT/'fonts'/('DejaVuSans-Bold.ttf' if n.get('font-weight')=='700' else 'DejaVuSans.ttf')),int(n.get('font-size')))
 width=f.getlength(value)+float(n.get('letter-spacing','0'))*max(0,len(value)-1)
 assert float(n.get('x'))+width<=620,(key,width)
 widths[key]=round(width,3)
 n.text=value
nodes['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(ART.read_bytes()).decode())
payload='https://lore-site-v1.vercel.app/crypto/039/'
code=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8)
code.add_data(payload);code.make(fit=True)
matrix=code.get_matrix();size=len(matrix)
qr=nodes['moment-qr'];qr.set('viewBox',f'0 0 {size} {size}')
for n in list(qr):qr.remove(n)
ET.SubElement(qr,'{'+S+'}rect',{'width':str(size),'height':str(size),'fill':'#FFFFFF'})
d=' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v)
ET.SubElement(qr,'{'+S+'}path',{'d':d,'fill':'#000000'})
nodes['qr-caption'].text='SCAN TO DISCOVER'
root.find('{'+S+'}metadata').text='LORE CRYPTO 039 PRINT v1. Approved exact native art, Common, date and caption retained. Production-route QR. Physical print release remains separate. Locked LORE-CRYPTO-PRINT-v1.0 geometry.'
ET.ElementTree(root).write(OUT.with_suffix('.svg'),encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(FONT/'fontconfig.xml')
subprocess.run(['inkscape',str(OUT.with_suffix('.svg')),'--export-type=png',f'--export-filename={OUT.with_suffix(".png")}'],env=env,check=True,capture_output=True)
with Image.open(OUT.with_suffix('.png')) as im:
 assert im.size==(816,1110)
 im.convert('RGB').save(OUT.with_suffix('.png'),dpi=(300,300))
tmp=args.output_dir/'card-intermediate.pdf'
c=canvas.Canvas(str(tmp),pagesize=(195.84,266.4),pageCompression=1,invariant=1)
c.setTitle('LORE 039 Behind the Chair - Common Print v1')
c.setAuthor('LORE')
c.drawImage(str(OUT.with_suffix('.png')),0,0,width=195.84,height=266.4);c.showPage();c.save()
r=PdfReader(tmp);w=PdfWriter();w.add_page(r.pages[0]);w.pages[0].trimbox=RectangleObject([8.64,8.64,187.2,257.76]);w.add_metadata({'/Title':'LORE 039 Behind the Chair - Common Print v1','/Author':'LORE','/Subject':'Approved visual artwork and copy. Physical print release remains separate.'})
PDF=args.output_dir/'LORE-Crypto-039-Behind-the-Chair-Common-Print-v1.pdf'
with PDF.open('wb') as f:w.write(f)
assert hashlib.sha256(ART.read_bytes()).hexdigest()==EXPECTED
(args.output_dir/'card-layout-check.json').write_text(json.dumps({'text_widths_unscaled':widths,'embedded_art_sha256':EXPECTED,'canvas_px':[816,1110],'dpi':300,'trim_px':[744,1038],'safe_px':[684,981],'transform':nodes['locked-crypto-front'].get('transform'),'qr_payload':payload,'rarity':'Common','caption':'BUY BITCOIN.','approval':True},indent=2))
print(OUT.with_suffix('.png'));print(PDF)
