from pathlib import Path
import base64,copy,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageChops
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz,zxingcpp

REPO=Path(__file__).resolve().parents[5]
BASE=REPO/'.cache/lore-print-v1.2';BASE.mkdir(parents=True,exist_ok=True)
PRINT=REPO/'cards/crypto/print-ready/v1.2';MASTER=REPO/'cards/crypto/master/print-v1.2'
TMP=BASE/'working';TMP.mkdir(exist_ok=True)
for d in ['fronts/png','fronts/pdf','fronts/svg','back','review','qa']: (PRINT/d).mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('convert_front',MASTER/'source/convert_front.py')
conv=importlib.util.module_from_spec(spec);spec.loader.exec_module(conv)
S=conv.SCALE;X=conv.OFFSET;D=conv.HEIGHT_DELTA;SVG=conv.SVG;XLINK=conv.XLINK;ns=conv.ns
FONT=REPO/'cards/master/front-v3/source'
ENV=os.environ.copy();ENV['FONTCONFIG_FILE']=str(FONT/'fontconfig.xml')
TRIM=(36,36,780,1074);SAFE=(66,64.5,750,1045.5)
BASE_COMMIT='9aeeb54baa4f291fc38242ba7f5e73f892b57f42'
def sha(b):return hashlib.sha256(b).hexdigest()
def atomic_bytes(path,data):
 temp=path.with_name(path.name+'.writing')
 with temp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 assert temp.stat().st_size==len(data)
 temp.replace(path)
def save_image(im,path,**kwargs):
 buf=io.BytesIO();im.save(buf,format='PNG',**kwargs);atomic_bytes(path,buf.getvalue())
def run(args):
 p=subprocess.run(args,env=ENV,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 return p.stdout
def rel(p):return str(p.relative_to(REPO))
def file_info(p):return {'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def json_write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')

registry=json.loads((REPO/'cards/crypto/current-cards.json').read_text())
cards=sorted([c for c in registry['cards'] if c.get('moment_number')],key=lambda c:c['moment_number'])
assert [c['moment_number'] for c in cards]==list(range(1,40))
results=[]
def export(root,svg,png,pdf,key,payload=None):
 ET.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
 run(['inkscape',str(svg),'--export-type=png','--export-width=816','--export-height=1110',f'--export-filename={png}'])
 with Image.open(png) as im:rgb=im.convert('RGB')
 save_image(rgb,png,dpi=(300,300))
 raw=TMP/(key+'-raw.pdf')
 run(['inkscape',str(svg),'--export-type=pdf','--export-text-to-path',f'--export-filename={raw}'])
 page=PdfReader(raw).pages[0]
 assert abs(float(page.mediabox.width)-195.84)<.01 and abs(float(page.mediabox.height)-266.4)<.01
 page.trimbox=RectangleObject([8.64,8.64,187.2,257.76]);page.bleedbox=RectangleObject([0,0,195.84,266.4])
 page.artbox=RectangleObject([15.84,15.48,180,250.92])
 writer=PdfWriter();writer.add_page(page);writer.add_metadata({'/Title':svg.stem,'/Subject':'LORE print v1.2; physical proof acceptance pending'})
 with pdf.open('wb') as f:writer.write(f)
 with Image.open(png) as im:
  assert im.size==(816,1110) and abs(im.info['dpi'][0]-300)<.01
  bbox=ImageChops.difference(im,Image.new('RGB',im.size,'#0B0B0B')).getbbox()
  assert bbox[0]>=71 and bbox[1]>=71 and bbox[2]<=745 and bbox[3]<=1040,(key,bbox)
  save_image(im.crop(TRIM),TMP/(key+'-trim.png'))
  if payload:assert [r.text for r in zxingcpp.read_barcodes(im)]==[payload],key+' PNG QR'
 with fitz.open(pdf) as doc:
  assert len(doc)==1 and not doc[0].get_fonts(),key+' outlined fonts'
  pix=doc[0].get_pixmap(dpi=300,alpha=False)
  if payload:
   im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
   assert [r.text for r in zxingcpp.read_barcodes(im)]==[payload],key+' PDF QR'
 bounds={}
 if payload:
  ids={key for key in conv.LOWER_IDS|{'rarity-label','moment-number'}
       if (node:=root.find(f".//*[@id='{key}']")).tag!=ns('text') or ''.join(node.itertext()).replace('\u200b','').strip()}
  for line in run(['inkscape',str(svg),'--query-all']).splitlines():
   a=line.split(',')
   if a[0] in ids:
    x,y,w,h=[float(v)*300/96 for v in a[1:]]
    assert x>=SAFE[0] and y>=SAFE[1] and x+w<=SAFE[2] and y+h<=SAFE[3],(key,a)
    bounds[a[0]]=[round(v,4) for v in [x,y,w,h]]
  assert set(bounds)==ids,(key,set(bounds))
 return {'png':file_info(png),'pdf':file_info(pdf),'svg':file_info(svg),'visible_bounds_px':bbox,'essential_bounds_px':bounds,'qr_png_and_pdf_pass':bool(payload),'outlined_pdf_text':True}

for card in cards:
 number=card['moment_number'];key=f'{number:03d}';source=REPO/card['editable_svg']
 checkpoint=PRINT/'qa'/f'{key}.json'
 if checkpoint.exists():
  prior=json.loads(checkpoint.read_text())
  if prior['source_svg']['sha256']==sha(source.read_bytes()) and all(sha((REPO/prior[k]['path']).read_bytes())==prior[k]['sha256'] for k in ['png','pdf','svg']):
   with Image.open(REPO/prior['png']['path']) as im:save_image(im.crop(TRIM),TMP/(key+'-trim.png'))
   results.append(prior);print(f'{key} retained: verified export checkpoint',flush=True);continue
 original=ET.parse(source).getroot();root=conv.convert(original)
 stem=f'LORE-Crypto-{key}-Front-Print-v1.2'
 record=export(root,PRINT/'fronts/svg'/(stem+'.svg'),PRINT/'fronts/png'/(stem+'.png'),PRINT/'fronts/pdf'/(stem+'.pdf'),key,card['qr_url'])
 art=root.find(".//*[@id='card-illustration']");data=base64.b64decode(art.get('{'+XLINK+'}href').split(',',1)[1])
 with Image.open(io.BytesIO(data)) as im:dimensions=list(im.size)
 source_records=card.get('current_files',[])
 for r in source_records:
  if r['path']==card['editable_svg']:assert sha(source.read_bytes())==r['sha256']
 art_record=card.get('artwork_file',{})
 if art_record.get('sha256'):assert sha(data)==art_record['sha256'],key+' art hash'
 if number==1:
  approved=MASTER/'approval/LORE-001-Front-v1.2-Approved.png'
  assert ImageChops.difference(Image.open(approved),Image.open(REPO/record['png']['path'])).getbbox() is None,'001 must match approved proof exactly'
 record.update({'number':key,'id':card['id'],'title':' '.join([card.get('title_line_1',''),card.get('title_line_2','')]).strip(),
  'rarity':card['rarity'],'source_svg':file_info(source),'source_front':card['front'],'source_commit':BASE_COMMIT,
  'artwork_sha256':sha(data),'artwork_native_px':dimensions,'artwork_bytes_unchanged':True,
  'artwork_translation_preserved':art.get('transform'),
  'wording_typography_logo_qr_preserved':True,'qr_url':card['qr_url'],
  'layout_approval':'001 v1.2 approved; collection rollout authorised by Dan on 2026-10-06',
  'physical_print_release':False})
 results.append(record);json_write(PRINT/'qa'/f'{key}.json',record)
 print(f'{key} complete: artwork preserved, bounds pass, PNG/PDF QR pass',flush=True)

# The already approved shared back v6 is sourced from its review branch.
back_source=MASTER/'source-assets/shared-back-v6.svg'
assert sha(back_source.read_bytes())=='d75cc8da13e2750f4a6a26ee9e4298f5011069a23a9218ce94f8812fe96fe207'
back=ET.parse(back_source).getroot();g=back.find(".//*[@id='locked-shared-back-v6-review']");n=g[0]
logo=copy.deepcopy(n[-1]);assert n[-1].tag==ns('svg')
g.set('transform',f'translate({conv.fmt(X)} {conv.fmt(X)}) scale({S:.12f})')
n.set('height',conv.fmt(1260+D));n.set('viewBox',f'0 0 900 {conv.fmt(1260+D)}')
for a in n:
 if a.tag==ns('rect'):a.set('height',conv.fmt(float(a.get('height'))+D))
n[-1].set('y',conv.fmt(float(n[-1].get('y'))+D/2))
expected=copy.deepcopy(logo);expected.set('y',conv.fmt(float(logo.get('y'))+D/2))
assert ET.tostring(expected)==ET.tostring(n[-1])
back.set('width','69.088mm');back.set('height','93.98mm')
back.find(ns('metadata')).text='LORE shared back v6 / print v1.2. Matching even frame adaptation requested by Dan on 2026-10-06. Approved logo paths preserved and physically centred. Physical proof pending.'
stem='LORE-Shared-Back-v6-Print-v1.2'
back_record=export(back,*[PRINT/'back'/(stem+ext) for ext in ['.svg','.png','.pdf']],'back')
back_record.update({'source_branch':'review/shared-back-v6-print','source_path':'cards/review/shared-back-v6-print/LORE-Shared-Back-v6-Print-v1.svg','source_svg_sha256':sha(back_source.read_bytes()),'logo_paths_and_size_preserved':True,'logo_centre_canvas_px':[408,555],'frame_margin_mm':3.048,'physical_print_release':False,'status':'MATCHING_V1_2_ADAPTATION_REQUESTED_BY_DAN'})
json_write(PRINT/'qa/back.json',back_record)
print('Shared back complete: even margins and centred original logo',flush=True)

# All six future rarity templates use the same authorised transform and taller layout.
template_records=[]
(MASTER/'templates').mkdir(parents=True,exist_ok=True)
for path in sorted((REPO/'cards/crypto/master/print-v1/templates').glob('*.svg')):
 target=MASTER/'templates'/path.name
 ET.ElementTree(conv.convert(ET.parse(path).getroot())).write(target,encoding='utf-8',xml_declaration=True)
 template_records.append(file_info(target))
renderer=(REPO/'cards/crypto/master/print-v1/source/render_print_card.py').read_text()
renderer=renderer.replace('LORE-CRYPTO-PRINT-v1.0','LORE-CRYPTO-PRINT-v1.2').replace('approved uniform print inset','approved even-margin frame and proportional illustration crop')
renderer=renderer.replace("'--export-type=png',","'--export-type=png','--export-width=816','--export-height=1110',")
renderer=renderer.replace("n.text=value","n.text=value")
(MASTER/'source/render_print_card.py').write_text(renderer)
front_bounds=[X+7.5*S,X+7.5*S,816-X-7.5*S,1110-X-7.5*S]
print_spec={'revision':'LORE-CRYPTO-PRINT-v1.2','approved_by':'Dan Payne','approved_at':'2026-10-06',
 'approval_scope':'001 v1.2 framing and authorised application to numbered cards 001-039; matching shared back requested',
 'full_bleed_px':[816,1110],'dpi':300,'full_bleed_mm':[69.088,93.98],
 'trim_box_px':[36,36,744,1038],'safe_box_px':[66,64.5,684,981],
 'layout_units':[900,1287.625],'scale':S,'translate':[X,X],'layout_height_delta':D,
 'front_frame_stroke_bounds_px':front_bounds,'front_margin_mm':3.0801083521444683,'back_margin_mm':3.048,
 'artwork_proportional_enlargement_from_v1_1_percent':D/1232*100,
 'illustration_bytes':'unchanged; proportional centre fill with existing per-card translations retained',
 'text_logo_qr':'same dimensions as approved 001 v1.2; header/footer positions follow taller frame',
 'fonts':'cards/master/front-v3/source/fontconfig.xml','templates':template_records,
 'printer_acceptance':False,'physical_sample_approval':False,'print_release':False}
json_write(MASTER/'print-spec.json',print_spec)
manifest={'revision':'LORE-CRYPTO-PRINT-v1.2','date':'2026-10-06','source_commit':BASE_COMMIT,
 'status':'APPROVED_FRAMING_APPLIED_TO_APPROVED_NUMBERED_ARTWORK',
 'front_count':len(results),'shared_back_count':1,'fronts':results,'shared_back':back_record,
 'unreleased_unnumbered_designs':[c['id'] for c in registry['cards'] if not c.get('moment_number')],
 'website_full_art_and_book_files_changed':False,'physical_print_release':False}
json_write(PRINT/'manifest.json',manifest)

# Contact sheets are document renders, not raster artwork edits.
pdfmetrics.registerFont(TTFont('LoreReview',str(FONT/'fonts/DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('LoreReviewBold',str(FONT/'fonts/DejaVuSans-Bold.ttf')))
for start in range(0,39,6):
 chunk=results[start:start+6];page_no=start//6+1
 report=PRINT/'review'/f'LORE-Print-v1.2-Contact-{page_no:02d}.pdf'
 c=canvas.Canvas(str(report),pagesize=(842,950))
 c.setFillColor(HexColor('#F5F2EB'));c.rect(0,0,842,950,fill=1,stroke=0)
 c.setFillColor(HexColor('#1A1A1A'));c.setFont('LoreReviewBold',22);c.drawString(32,906,f'LORE / PRINT v1.2 / {chunk[0]["number"]}–{chunk[-1]["number"]}')
 c.setFont('LoreReview',10);c.drawString(32,885,'Approved framing applied to existing art. Finished-cut previews; files include bleed.')
 for i,r in enumerate(chunk):
  x=32+(i%3)*270;y=510-(i//3)*420
  c.drawImage(str(TMP/(r['number']+'-trim.png')),x,y,width=238,height=238*1038/744)
  c.setFillColor(HexColor('#1A1A1A'));c.setFont('LoreReviewBold',11);c.drawString(x,y-19,r['number']+' / '+r['rarity'].upper())
  c.setFont('LoreReview',8);c.drawString(x,y-34,r['title'])
 c.setFont('LoreReview',8);c.drawString(32,22,'39 numbered fronts + one shared back / printer and physical sample acceptance remain separate.')
 c.save()
 with fitz.open(report) as doc:atomic_bytes(report.with_suffix('.png'),doc[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).tobytes('png'))

# Review pair: exact approved 001 + adapted matching back.
pair=PRINT/'review/LORE-001-and-Shared-Back-v1.2.pdf';c=canvas.Canvas(str(pair),pagesize=(842,595))
c.setFillColor(HexColor('#F5F2EB'));c.rect(0,0,842,595,fill=1,stroke=0)
c.setFillColor(HexColor('#1A1A1A'));c.setFont('LoreReviewBold',20);c.drawString(32,560,'001 / APPROVED FRONT + MATCHING BACK')
c.setFont('LoreReview',9);c.drawString(32,541,'Print v1.2 / even framing / original artwork and logo preserved / finished-cut previews')
for x,key,label in [(45,'001','001 FRONT'),(450,'back','SHARED BACK')]:
 c.setFont('LoreReviewBold',10);c.drawString(x,521,label)
 c.drawImage(str(TMP/(key+'-trim.png')),x,35,width=744*.24*1.9,height=1038*.24*1.9)
c.save()
with fitz.open(pair) as doc:atomic_bytes(pair.with_suffix('.png'),doc[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).tobytes('png'))
print(json.dumps({'fronts':39,'shared_back':1,'templates':6,'all_png_and_pdf_qr_checks':True,'output':str(PRINT)}),flush=True)
