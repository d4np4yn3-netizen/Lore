"""Current web-only border crop; never edits print, art or book masters."""
from pathlib import Path
import json,hashlib,re,math,xml.etree.ElementTree as ET,sys,argparse
from PIL import Image,ImageDraw,ImageFont,ImageChops
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--qr-deps',type=Path);args=parser.parse_args();R=args.repo;O=args.out
if args.qr_deps:sys.path.insert(0,str(args.qr_deps))
import zxingcpp
for folder in ['site/public/archive','site/public/brand','qa']: (O/folder).mkdir(parents=True,exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();L=Image.Resampling.LANCZOS
manifest=json.loads((R/'cards/crypto/print-ready/histrove-v1/manifest.json').read_text());records=[]
for c in manifest['fronts']:
 n=c['number'];src=R/c['png']['path'];svg=R/c['svg']['path'];assert H(src)==c['png']['sha256'] and H(svg)==c['svg']['sha256']
 root=ET.parse(svg).getroot();g=next(x for x in root.iter() if x.get('id')=='locked-crypto-front');transform=re.fullmatch(r'translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+)\)',g.get('transform'));assert transform
 tx,ty,s=map(float,transform.groups());frames=[x for x in g.iter() if x.tag.endswith('rect') and x.get('fill')=='none' and x.get('x')=='10' and x.get('y')=='10' and x.get('width')=='880'];assert len(frames)==1
 frame=frames[0];x,y,w,h,rx,sw=[float(frame.get(k)) for k in ['x','y','width','height','rx','stroke-width']];assert (x,y,w,h,rx,sw)==(10,10,880,1267.625,25,5)
 bounds=[tx+s*(x-sw/2),ty+s*(y-sw/2),tx+s*(x+w+sw/2),ty+s*(y+h+sw/2)];radius=s*(rx+sw/2)
 crop=(math.floor(bounds[0]),math.floor(bounds[1]),math.ceil(bounds[2]),math.ceil(bounds[3]));assert crop==(72,72,744,1038)
 source=Image.open(src).convert('RGB');cropped=source.crop(crop);ss=8;mask=Image.new('L',(cropped.width*ss,cropped.height*ss),0);draw=ImageDraw.Draw(mask)
 box=((bounds[0]-crop[0])*ss,(bounds[1]-crop[1])*ss,(bounds[2]-crop[0])*ss,(bounds[3]-crop[1])*ss)
 draw.rounded_rectangle(box,radius=radius*ss,fill=255);mask=mask.resize(cropped.size,L)
 native=cropped.convert('RGBA');native.putalpha(mask)
 dims=(600,int(math.floor(600*cropped.height/cropped.width+0.5)));assert dims==(600,863)
 web=native.resize(dims,L);path=O/'site/public/archive'/f'{n}-histrove-border-card.webp';web.save(path,format='WEBP',lossless=True,quality=75,method=4,exact=True)
 decoded=Image.open(path).convert('RGBA');assert ImageChops.difference(web,decoded).getbbox() is None
 assert decoded.getpixel((0,0))[3]==0 and decoded.getpixel((599,862))[3]==0
 assert min(decoded.getpixel(p)[3] for p in [(300,100),(300,750),(500,750)])==255
 payloads=[v.text for v in zxingcpp.read_barcodes(decoded.convert('RGB'))];assert payloads==[c['qr_url']],(n,payloads)
 records.append({'number':n,'title':c['title'],'rarity':c['rarity'],'path':str(path.relative_to(O)),'public_path':'/'+str(path.relative_to(O/'site/public')),'sha256':H(path),'bytes':path.stat().st_size,'dimensions_px':list(dims),'source':c['png']['path'],'source_sha256':H(src),'source_svg':c['svg']['path'],'source_svg_sha256':H(svg),'source_dimensions_px':[816,1110],'outer_border_bounds_ltrb':bounds,'outer_radius_px':radius,'conservative_crop_ltrb':list(crop),'crop_dimensions_px':list(cropped.size),'mask':'Exact outer stroked rounded rectangle, 8x supersampling, transparent exterior','resampling':'LANCZOS','lossless':True,'complete_border_geometry_retained':True,'qr_payloads':payloads,'qr_pass':True,'print_source_unchanged':H(src)==c['png']['sha256']})
# Update only the cards inside the existing approved social composition.
social=Image.new('RGB',(1200,630),'#0B0B0B');d=ImageDraw.Draw(social);d.rectangle((716,0,1199,629),fill='#121211');d.line((715,48,715,582),fill='#514624',width=1);d.line((81,553,651,553),fill='#D4AF37',width=2)
logo=Image.open(R/'brand/assets/png/histrove_primary_white_transparent-2400.png').convert('RGBA').resize((672,403),L);social.paste(logo,(20,98),logo)
for n,xy,width in [('006',(744,178),219),('001',(904,108),260)]:
 card=Image.open(O/'site/public/archive'/f'{n}-histrove-border-card.webp').convert('RGBA');card=card.resize((width,round(width*card.height/card.width)),L);social.paste(card,xy,card)
p=O/'site/public/brand/histrove-social-border.png';social.save(p,optimize=True)
result={'revision':'HISTROVE-WEB-BORDER-v2','reason':'User requested web previews cut to the visible card border; physical trim still had a black surround','sourceCommit':'f8be5b7af291f192e2731949424de559eb87796a','cards':records,'social':{'path':str(p.relative_to(O)),'public_path':'/brand/histrove-social-border.png','sha256':H(p),'dimensions_px':[1200,630]},'all39QrPass':True,'all39PrintPngAndSvgHashesUnchanged':True,'oldWebAssetsRetained':True}
(O/'border-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
proof=Image.new('RGB',(800,670),'#e4e1da');draw=ImageDraw.Draw(proof)
for i,(label,p) in enumerate([('Before: physical trim',R/'site/public/archive/001-histrove-card.webp'),('After: visible border',O/'site/public/archive/001-histrove-border-card.webp')]):
 draw.text((30+i*400,22),label,font=font,fill='#1a1a1a');im=Image.open(p).convert('RGBA');im=im.resize((360,round(360*im.height/im.width)),L);proof.paste(im,(20+i*400,72),im)
draw.text((22,620),'Website preview only. Approved print files, artwork and QR remain unchanged.',font=small,fill='#222222');proof.save(O/'qa/HISTROVE-card-border-before-after.png')
sheet=Image.new('RGB',(1380,2040),'#dedbd5');draw=ImageDraw.Draw(sheet);draw.text((20,15),'HISTROVE: all 39 border-cropped web cards',font=font,fill='#111111')
for i,r in enumerate(records):
 im=Image.open(O/r['path']).convert('RGBA').resize((176,253),L);x=20+i%7*195;y=60+i//7*325;sheet.paste(im,(x,y),im);draw.text((x,y+262),r['number']+' / '+r['rarity'],font=small,fill='#222222');draw.text((x,y+280),r['title'][:23],font=small,fill='#333333')
sheet.save(O/'qa/HISTROVE-all-39-border-crops.jpg',quality=92)
print('PASS all39 exact SVG-derived border crops, transparent corners, QR payloads and unchanged print hashes',flush=True)
