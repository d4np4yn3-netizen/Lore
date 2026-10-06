from pathlib import Path
import copy, json, hashlib, subprocess, xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[1]
NS='http://www.w3.org/2000/svg'; ET.register_namespace('',NS);ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
def tag(n): return '{'+NS+'}'+n
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def export(root,name,width):
 p=B/'assets/svg'/f'{name}.svg'; ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
 png=B/'assets/png'/f'{name}-{width}.png'; subprocess.run(['inkscape',str(p),f'--export-width={width}',f'--export-filename={png}'],check=True,capture_output=True)
 return p,png
master=ET.parse(B/'source/approved-primary.svg').getroot()
for t in master.findall(tag('desc')):t.text='HISTROVE approved primary lockup, 6 October 2026. Exact approved raster brush lettering; original vector crown; outlined tagline. Raster lettering is not an infinitely scalable vector master.'
for t in master.findall(tag('title')):t.text='HISTROVE — History Worth Holding — Approved Primary'
ET.ElementTree(master).write(B/'source/approved-primary.svg',encoding='utf-8',xml_declaration=True)
base=copy.deepcopy(master)
for e in list(base):
 if e.tag==tag('rect') and e.get('width')=='2400':base.remove(e)
# Master retains approved transform; crop changes below remove surrounding empty canvas only.
variants=[]
for kind in ['primary','compact','wordmark']:
 for color in ['white','obsidian']:
  r=copy.deepcopy(base)
  if kind!='primary':
   for e in list(r):
    if e.get('id')=='tagline':r.remove(e)
  if kind=='compact':r.set('viewBox','0 0 2400 1180');r.set('height','1180')
  if kind=='wordmark':
   for e in list(r):
    if e.get('id')=='approved-rising-strokes-crown':r.remove(e)
   r.set('viewBox','0 380 2400 780');r.set('height','780')
  if color=='obsidian':
   for e in r.iter():
    if e.tag==tag('rect') and e.get('mask'):e.set('fill','#0B0B0B')
    if e.get('id')=='tagline':
     for t in e.iter():
      if 'fill' in t.attrib:t.set('fill','#0B0B0B')
      if 'style' in t.attrib:t.set('style',t.get('style').replace('#f5f2eb','#0b0b0b'))
  variants.append((f'histrove_{kind}_{color}_transparent',r,2400))
  if kind=='primary':
   bg=copy.deepcopy(r); bg.insert(0,ET.Element(tag('rect'),{'width':'2400','height':'1440','fill':'#0B0B0B' if color=='white' else '#F5F2EB'}))
   variants.append((f'histrove_primary_{"obsidian" if color=="white" else "bone"}',bg,2400))
comp=json.loads((B/'source/master-components.json').read_text())
for color,fill in [('gold','#D4AF37'),('white','#FFFFFF'),('obsidian','#0B0B0B')]:
 r=ET.Element(tag('svg'),{'width':'2048','height':'2048','viewBox':'0 0 512 512'})
 ET.SubElement(r,tag('title')).text='HISTROVE Rising Strokes crown'
 ET.SubElement(r,tag('path'),{'fill':fill,'fill-rule':'evenodd','d':comp['crown']['d'],'transform':'translate(82 116) scale(1.11182108626) translate(-4 -8)'})
 variants.append((f'histrove_crown_{color}_transparent',r,2048))
 if color=='gold':
  a=copy.deepcopy(r);a.insert(0,ET.Element(tag('rect'),{'width':'512','height':'512','fill':'#0B0B0B'}));variants.append(('histrove_avatar_gold_obsidian',a,1024))
assets=[]
for name,r,width in variants:
 p,png=export(r,name,width)
 for f in [p,png]:
  entry={'path':'brand/'+str(f.relative_to(B)),'sha256':sha(f),'byte_count':f.stat().st_size,'role':name,'contains_raster_wordmark':any(z.tag==tag('image') for z in r.iter())}
  if f.suffix=='.png':
   im=Image.open(f).convert('RGBA');a=im.getchannel('A');entry.update(dimensions_px=list(im.size),transparent=a.getextrema()[0]==0,alpha_bbox=a.getbbox())
   box=a.getbbox();assert box
   if entry['transparent']:assert box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height
  assets.append(entry)
 if width==2400:
  web=B/'assets/png'/f'{name}-1200.png';subprocess.run(['inkscape',str(p),'--export-width=1200',f'--export-filename={web}'],check=True,capture_output=True)
  im=Image.open(web).convert('RGBA');assets.append({'path':'brand/'+str(web.relative_to(B)),'sha256':sha(web),'byte_count':web.stat().st_size,'role':name+' web','dimensions_px':list(im.size),'transparent':im.getchannel('A').getextrema()[0]==0,'contains_raster_wordmark':True})
# Alpha geometry must remain identical in light/dark variants.
for kind in ['primary','compact','wordmark']:
 a=Image.open(B/'assets/png'/f'histrove_{kind}_white_transparent-2400.png').getchannel('A')
 b=Image.open(B/'assets/png'/f'histrove_{kind}_obsidian_transparent-2400.png').getchannel('A')
 assert a.tobytes()==b.tobytes(),kind
# A useful contact sheet showing real assets against contrasting surfaces.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
sheet=Image.new('RGB',(1600,1900),'#e7e3dc');d=ImageDraw.Draw(sheet)
d.text((40,25),'HISTROVE  /  BRAND PACK v1.0',font=font,fill='#0b0b0b')
for i,(name,r,width) in enumerate(variants):
 x=40+(i%2)*780;y=85+(i//2)*295
 light='obsidian_transparent' in name or 'bone' in name
 bg='#F5F2EB' if light else '#0B0B0B';d.rectangle((x,y,x+740,y+245),fill=bg)
 im=Image.open(B/'assets/png'/f'{name}-{width}.png').convert('RGBA');im.thumbnail((700,220),Image.Resampling.LANCZOS);sheet.paste(im,(x+(740-im.width)//2,y+(245-im.height)//2),im)
 d.text((x,y+252),name.replace('histrove_','').replace('_',' '),font=font,fill='#0b0b0b')
sheet.save(B/'previews/HISTROVE-Brand-Guide.png')
manifest={'revision':'HISTROVE-v1.0','date':'2026-10-06','release_status':'APPROVED_IDENTITY_DETERMINISTIC_EXPORTS','approval_scope':'User approved HISTROVE full proof and 001 placement and requested replacement brand pack with PNG variants. Export QA does not imply trademark clearance or physical print approval.','source_master':'brand/source/approved-primary.svg','source_raster_native_px':[2172,724],'raster_limit':'2400px full canvas uses a 2080px-wide lettering image. Larger interpolation creates no new brush detail. SVG assemblies embed raster lettering. Crown and outlined tagline are vector.','approved_exports':assets}
(B/'assets/asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(B/'qa/technical-qa.json').write_text(json.dumps({'revision':'HISTROVE-v1.0','automated_checks':'PASS','png_count':sum(a['path'].endswith('.png') for a in assets),'svg_count':sum(a['path'].endswith('.svg') for a in assets),'light_dark_alpha_identical':True,'transparent_edges_clear':True,'crown_d_sha256':hashlib.sha256(comp['crown']['d'].encode()).hexdigest(),'visual_review':'PENDING','physical_print_approval':False},indent=2)+'\n')
print('Built',len(assets),'assets')
