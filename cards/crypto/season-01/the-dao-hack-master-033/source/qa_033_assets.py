from pathlib import Path
import base64,hashlib,json,xml.etree.ElementTree as ET,tempfile,subprocess
from PIL import Image,ImageChops
from pypdf import PdfReader
import zxingcpp
ROOT=Path(__file__).resolve().parent.parent;REPO=ROOT.parents[3];SRC=ROOT/'source'
S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';H=lambda b:hashlib.sha256(b).hexdigest();expected='f93c3d9bed56839609e27adc0919a3d3dd7680415e048b0d8ad3523ea26e63d5';base=ROOT/'LORE-Crypto-033-The-DAO-Hack-Epic-Print-v1';art=ROOT/'art.png'
r=ET.parse(base.with_suffix('.svg')).getroot();nodes={n.get('id'):n for n in r.iter() if n.get('id')};embedded=base64.b64decode(nodes['card-illustration'].get('{'+X+'}href').split(',',1)[1]);assert H(embedded)==H(art.read_bytes())==expected
assert nodes['locked-crypto-front'].get('transform')=='translate(46.515 48.921) scale(0.8033)';assert nodes['moment-context'].get('font-size')=='25' and nodes['moment-context'].get('font-weight')=='700'
original=ET.parse(SRC/'epic.svg').getroot();allowed={'creator-name','title-line-1','title-line-2','moment-context','moment-number','set-number','card-illustration','moment-qr','qr-caption'}
def norm(n):
 if n.tag=='{'+S+'}metadata':n.text=''
 if n.get('id') in allowed:
  if n.get('id')=='card-illustration':n.set('{'+X+'}href','')
  elif n.get('id')=='moment-qr':
   n.set('viewBox','0 0 37 37')
   for child in list(n):n.remove(child)
  else:n.text=''
 for child in n:norm(child)
norm(r);norm(original);assert ET.tostring(r)==ET.tostring(original)
png=Image.open(base.with_suffix('.png'));assert png.size==(816,1110) and png.info['dpi'][0]>299.5
pdf=PdfReader(base.with_suffix('.pdf'));assert len(pdf.pages)==1;assert list(map(float,pdf.pages[0].mediabox))==[0,0,195.84,266.4];assert list(map(float,pdf.pages[0].trimbox))==[8.64,8.64,187.2,257.76]
book=PdfReader(REPO/'book/crypto-season-01/proofs/033-the-dao-hack-full-art-spread-v1.pdf');assert len(book.pages)==2
native=list(book.pages[0].images);im=Image.open(art);assert len(native)==1 and native[0].image.size==im.size;assert ImageChops.difference(native[0].image.convert('RGB'),im.convert('RGB')).getbbox() is None
text=book.pages[1].extract_text();assert 'REVIEW' not in text and 'THE DAO HACK' in text and 'REMAIN CALM.' in text
links=[a.get_object()['/A']['/URI'] for a in book.pages[1].get('/Annots',[])];assert len(links)==3
payload='https://lore-site-v1.vercel.app/crypto/033/'
with tempfile.TemporaryDirectory() as temp:
 pre=Path(temp)/'card';subprocess.run(['pdftoppm','-r','300','-png','-singlefile',str(base.with_suffix('.pdf')),str(pre)],check=True,capture_output=True)
 for image in [png,Image.open(pre.with_suffix('.png'))]:
  codes=zxingcpp.read_barcodes(image);assert len(codes)==1 and codes[0].text==payload
qa={'number':'033','art_sha256':expected,'exact_embedded_art':True,'book_pixels_exact':True,'fixed_template_geometry_logo_colours':True,'canvas_px':[816,1110],'trim_px':[744,1038],'safe_px':[684,981],'dpi':300,'book_pages':2,'book_native_ppi':126.91,'source_links':links,'qr_decoded_png':payload,'qr_decoded_300dpi_printer_pdf':payload,'visual_qa':'Card and both book pages inspected; all four clue regions unobstructed. Small receiver address requires physical assessment. Website clue crops inspected.','visual_approval':True,'book_copy_approved':True,'publication_authorised':True,'live_verification':'PENDING','print_release':False,'physical_qr_test':False,'book_reproduction_release':False}
(SRC/'final-qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
