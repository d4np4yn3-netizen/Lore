#!/usr/bin/env python3
"""Check actual binaries and vector geometry; approval comes from the recorded user decision."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,copy,tempfile,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from scipy.ndimage import distance_transform_edt
from build_assets import render
ROOT=Path(__file__).resolve().parents[2]; B=ROOT/'brand'; NS={'s':'http://www.w3.org/2000/svg'}
mp=B/'assets/asset-manifest.json';m=json.loads(mp.read_text());master=json.loads((B/'source/master-components.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'revision':m['revision'],'checks':[],'visual_inspection':'PASS' if '--visual-reviewed' in sys.argv else 'PENDING','user_approval_record':m['approval_record']}
exports=[]
for a in m['assets']:
 sp=ROOT/a['svg'];pp=ROOT/a['png'];rt=ET.parse(sp).getroot();nodes=list(rt.iter())
 assert not any(n.tag.split('}')[-1] in ['image','text','foreignObject','script','use'] for n in nodes),sp
 assert rt.findall('.//s:path',NS)
 im=Image.open(pp);im.load();assert im.width==a['png_width'];assert im.mode in ['RGBA','RGB']
 im=im.convert('RGBA');ar=np.array(im);al=ar[:,:,3];bbox=im.getchannel('A').getbbox();assert bbox
 margins=[bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3]]
 if a['transparent']:
  assert (al==0).any() and (al==255).any() and ((al>0)&(al<255)).any(),pp
  assert min(margins)>=48,(pp,margins)
  expected=np.array([tuple(bytes.fromhex(c[1:]))for c in set(a['colours'])])
  matches=np.zeros(al.shape,dtype=bool)
  for e in expected:matches|=np.all(ar[:,:,:3]==e,axis=2)
  assert matches[al==255].all(),(pp,'Unexpected opaque colour')
  edge=ar[(al>0)&(al<255)].astype(float)
  if len(edge):
   residual=np.stack([np.max(np.abs(edge[:,:3]-e)*edge[:,3:]/255,axis=1)for e in expected])
   assert np.min(residual,axis=0).max()<=1.0,(pp,'Matte contamination')
 else:assert np.all(al==255),pp
 a.update(svg_sha256=sha(sp),png_sha256=sha(pp),dimensions_px=list(im.size),alpha_bbox=list(bbox),transparent_margins_px=margins if a['transparent'] else None)
 for ext,p in [('svg',sp),('png',pp)]:
  exports.append({'path':str(p.relative_to(ROOT)),'format':ext.upper(),'sha256':sha(p),'byte_count':p.stat().st_size,'dimensions_px':list(im.size) if ext=='png' else None,'viewbox':a['viewbox'] if ext=='svg' else None,'role':a['role'],'transparent':a['transparent'],'source_master_sha256':m['source_master_sha256'],'technical_qa_record':'brand/qa/technical-qa.json','approval_record':m['approval_record'],'approved_by':m['approved_by'],'approved_at':m['approved_at']})
 report['checks'].append({'asset':a['name'],'png_decoded':True,'true_vector_paths':True,'alpha_valid':True,'solid_colours_valid':True,'transparent_margins_px':a['transparent_margins_px']})
# Every palette variant of a layout has identical alpha and path geometry.
for family in ['lore_logo_primary_','lore_logo_compact_','lore_lockup_horizontal_','lore_crown_','lore_wordmark_','lore_tagline_primary_','lore_brand_thought_','lore_six_moments_one_icon_']:
 items=[a for a in m['assets']if a['name'].startswith(family)]
 masks=[np.asarray(Image.open(ROOT/a['png']).getchannel('A'))for a in items]
 assert all(np.array_equal(masks[0],b)for b in masks[1:]),family
 def geo(a):
  root=ET.parse(ROOT/a['svg']).getroot()
  return [(n.tag,{k:v for k,v in n.attrib.items()if k!='fill'})for n in root.iter()if n.tag.split('}')[-1]in ['g','path']]
 assert all(geo(items[0])==geo(a)for a in items[1:]),family
report['all_colourway_alpha_and_geometry_identical']=True
# Compare the primary export's entire drawing with the selected, approved source.
original=ET.parse(B/'source/approved-primary.svg').getroot().findall('s:g',NS)
actual=ET.parse(B/'assets/svg/lore_logo_primary_gold_white.svg').getroot().findall('s:g',NS)
assert [[(n.tag,n.attrib)for n in g.iter()]for g in original]==[[(n.tag,n.attrib)for n in g.iter()]for g in actual]
report['primary_geometry_matches_approved_option_04_exactly']=True
# Separate crown and lettering masks at native layout resolution.
with tempfile.TemporaryDirectory() as td:
 masks=[]
 for i,g in enumerate(actual[:2]):
  rt=ET.Element('{http://www.w3.org/2000/svg}svg',{'width':'1200','height':'1020','viewBox':'0 0 1200 1020'});rt.append(copy.deepcopy(g))
  p=Path(td)/f'{i}.svg';ET.ElementTree(rt).write(p);png=p.with_suffix('.png');render(p,png,1200)
  masks.append(np.array(Image.open(png).getchannel('A'))>127)
 assert not(masks[0]&masks[1]).any()
 report['crown_wordmark_overlap_pixels']=0
 report['minimum_crown_wordmark_gap_svg_units']=round(float(distance_transform_edt(~masks[0])[masks[1]].min()),2)
# Visual inspection sheet from actual exported PNGs on light/dark backgrounds.
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,15)
canvas=Image.new('RGB',(1600,7*325+80),'#232323');draw=ImageDraw.Draw(canvas)
draw.text((25,20),'LORE 04 / ACTUAL EXPORTED FILES',font=ImageFont.truetype(font,27),fill='white')
for i,a in enumerate(m['assets']):
 x=(i%4)*400;y=80+(i//4)*325
 bg='#F5F2EB' if ('black' in a['name'] and 'gold' not in a['name'])or 'gold_black' in a['name'] else '#0B0B0B'
 draw.rectangle((x+10,y,x+390,y+267),fill=bg)
 im=Image.open(ROOT/a['png']).convert('RGBA');im.thumbnail((350,243),Image.Resampling.LANCZOS)
 canvas.paste(im,(x+(400-im.width)//2,y+(267-im.height)//2),im)
 label=a['name'].replace('lore_','')
 draw.text((x+15,y+278),label,font=f,fill='white');draw.text((x+15,y+300),str(a['dimensions_px']),font=f,fill='#BBBBBB')
canvas.save(B/'qa/export-contact-sheet.png')
# Check crown extremities on three backgrounds and at practical small sizes.
proof=Image.new('RGB',(1500,620),'#202020');d=ImageDraw.Draw(proof)
for i,(slug,bg)in enumerate([('white','#0B0B0B'),('black','#F5F2EB'),('gold','#111111')]):
 x=i*500;d.rectangle((x,0,x+499,439),fill=bg)
 im=Image.open(B/f'assets/png/lore_crown_{slug}.png').convert('RGBA');im.thumbnail((420,420),Image.Resampling.LANCZOS);proof.paste(im,(x+40,10),im)
for i,size in enumerate([16,24,32,48,64,96]):
 im=Image.open(B/'assets/png/lore_crown_gold.png').convert('RGBA');im.thumbnail((size,size),Image.Resampling.LANCZOS);proof.paste(im,(35+i*245,470),im);d.text((35+i*245,585),f'{size}px',font=f,fill='white')
proof.save(B/'qa/crown-detail-and-size-check.png')

# Real-alpha presentation check, using actual exports over a visible checker.
checker=Image.new('RGB',(1600,760));cd=ImageDraw.Draw(checker)
for x in range(0,1600,32):
 for y in range(0,760,32):
  pair=('#777777','#999999')if x<800 else('#D8D8D8','#EEEEEE')
  cd.rectangle((x,y,x+31,y+31),fill=pair[(x//32+y//32)%2])
for i,slug in enumerate(['gold_white','gold_black']):
 logo=Image.open(B/f'assets/png/lore_logo_primary_{slug}.png').convert('RGBA');logo.thumbnail((760,700),Image.Resampling.LANCZOS)
 checker.paste(logo,(i*800+(800-logo.width)//2,(760-logo.height)//2),logo)
checker.save(B/'qa/alpha-checker-proof.png')

report['technical_qa']='PASS';m['technical_qa']='PASS';m['visual_inspection']=report['visual_inspection']
if report['visual_inspection']=='PASS':m['approved_exports']=exports;m['release_status']='APPROVED_MASTER_AND_DERIVED_EXPORTS'
(B/'qa/technical-qa.json').write_text(json.dumps(report,indent=2)+'\n');mp.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'assets':len(m['assets']),'files':len(exports),'technical_qa':'PASS','visual_inspection':report['visual_inspection'],'minimum_gap':report['minimum_crown_wordmark_gap_svg_units']}))
