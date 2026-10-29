from pathlib import Path
import json,copy,hashlib,re,subprocess,math,shutil
from lxml import etree as E
from PIL import Image,ImageDraw
R=Path('/workspace/scratch/58d5f7ed8606/rarity-swap-review');Q=R/'review-output';Q.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
D={'064':('everydays-at-auction-master-064','epic','common'),'071':('bitcoin-becomes-legal-tender-master-071','legendary','epic'),'093':('golden-river-fourth-halving-master-093','common','legendary')}
report={}
for n,(folder,old,new) in D.items():
 b=R/'cards/crypto/season-01'/folder
 src=b/(f'HISTROVE-Crypto-{n}-Front-Proof.svg' if n=='093' else f'HISTROVE-Crypto-{n}-Front-Print-v1'+('-footer-restored-2026-10-26' if n=='071' else '')+'.svg')
 t=E.parse(str(src));before=copy.deepcopy(t);template=E.parse(str(R/f'cards/crypto/master/histrove-print-v1/templates/{new}.svg'))
 def find(tree,pred):return next(x for x in tree.iter() if pred(x))
 # Replace only gradient colour, visible outer frame stroke, rarity badge and label.
 for tree in [t,template]:assert find(tree,lambda x:x.get('id')=='rarity-label') is not None
 g=find(t,lambda x:x.get('id')=='foil');g.getparent().replace(g,copy.deepcopy(find(template,lambda x:x.get('id')=='foil')))
 frame=lambda x:x.tag.endswith('rect') and x.get('x')=='10' and x.get('width')=='880'
 find(t,frame).set('stroke',find(template,frame).get('stroke'))
 badge=lambda x:x.tag.endswith('rect') and x.get('x')=='50' and x.get('y')=='49'
 a=find(t,badge);a.getparent().replace(a,copy.deepcopy(find(template,badge)))
 a=find(t,lambda x:x.get('id')=='rarity-label');a.getparent().replace(a,copy.deepcopy(find(template,lambda x:x.get('id')=='rarity-label')))
 colour={'common':'#BFC4C9','epic':'#B98AFF','legendary':'#D4AF37'}
 for x in t.iter():
  if x.tag.endswith('path') and x.get('stroke')==colour[old]:x.set('stroke',colour[new])
  if x.get('id')=='moment-context':x.set('fill',colour[new])
 out=Q/f'{n}-{new}-review.svg';t.write(str(out),encoding='utf-8',xml_declaration=True)
 # Embedded images and all unrelated XML nodes remain identical.
 def stripped(tree):
  tree=copy.deepcopy(tree)
  for x in list(tree.iter()):
   if x.get('id') in ['foil','rarity-label'] or badge(x):x.getparent().remove(x)
   elif frame(x):x.set('stroke','IGNORED_RARITY')
   elif x.tag.endswith('path') and x.get('stroke') in colour.values():x.set('stroke','IGNORED_RARITY')
   elif x.get('id')=='moment-context':x.set('fill','IGNORED_RARITY')
  return E.tostring(tree,method='c14n')
 assert stripped(before)==stripped(t),n
 assert [dict(x.attrib) for x in before.iter() if x.tag.endswith('image')]==[dict(x.attrib) for x in t.iter() if x.tag.endswith('image')]
 png=out.with_suffix('.png');subprocess.run(['inkscape',str(out),'--export-type=png','--export-width=816','--export-height=1110',f'--export-filename={png}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 # Current canonical frame-only border crop, not physical trim.
 im=Image.open(png).convert('RGB').crop((72,72,744,1038));mask=Image.new('L',(672*8,966*8),0);dr=ImageDraw.Draw(mask);dr.rounded_rectangle((.37923250565251*8,.37923250565251*8,671.6207674946475*8,965.6207674947707*8),radius=20.857787810392498*8,fill=255);mask=mask.resize(im.size,Image.Resampling.LANCZOS);im=im.convert('RGBA');im.putalpha(mask);im=im.resize((600,863),Image.Resampling.LANCZOS);im.save(Q/f'{n}-{new}-card.webp',lossless=True,exact=True)
 import zxingcpp
 qr=[x.text for x in zxingcpp.read_barcodes(Image.open(png))];expected=json.loads((b/'card-data.json').read_text())['qr_url'];assert qr==[expected],(n,qr,expected)
 report[n]={'old':old,'new':new,'source_svg':str(src.relative_to(R)),'source_sha256':H(src),'review_svg':str(out.relative_to(R)),'review_png':str(png.relative_to(R)),'embedded_images_unchanged':True,'all_non_rarity_xml_identical':True,'qr_payloads':qr,'art_sha256':H(b/'art.png')}
 # Current card-data record; historical approvals and QA reports untouched.
 p=b/'card-data.json';j=json.loads(p.read_text());j['rarity']=new
 if 'rarity_status' in j:j['rarity_status']='USER_SELECTED_'+new.upper()+'_2026_10_29'
 j['rarity_revision']='2026-10-29 user-selected three-card swap; local review; publication pending';p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
 # Builder labels and chapter source only; art and historical source PDFs retained.
 p=b/'build_book.py';s=p.read_text().replace('/ '+old.upper(),'/ '+new.upper()).replace("'rarity': '"+old+"'","'rarity': '"+new+"'");p.write_text(s)
 for p in list(b.glob('*.md')):
  if p.name=='README.md':continue
  s=p.read_text();p.write_text(s.replace('/ '+old.upper(),'/ '+new.upper()))
# Both chapters' shared framing description must remain correct, without changing 015 art/card.
old='their separate Legendary and Common frames interrupt a literal edge-to-edge join.'
new='their separate Legendary frames interrupt a literal edge-to-edge join.'
for n,folder in [('015','golden-river-first-halving-master-015'),('093',D['093'][0])]:
 b=R/'cards/crypto/season-01'/folder
 for p in [b/'authoring-content.json',b/(n+'.json'),R/f'site/app/cards/content/{n}.json']+list(b.glob('*.md')):
  if p.exists():p.write_text(p.read_text().replace(old,new))
# Only selected catalogue object rarity changes.
p=R/'site/app/cards/data.js';s=p.read_text()
for n,(_,old,new) in D.items():
 # block bounded by chapter number; source format allows one object per record.
 pat=r'(\{[^{}]*?\b(?:number|"number")\s*:\s*[\'\"]'+n+r'/100[\'\"][^{}]*?\})'
 matches=list(re.finditer(pat,s));assert len(matches)==1,(n,len(matches));m=matches[0];v=m.group();v,k=re.subn(r'((?:rarity|"rarity")\s*:\s*[\'\"])'+old.upper(),lambda x:x.group(1)+new.upper(),v);assert k==1 or new.upper() in v;s=s[:m.start()]+v+s[m.end():]
p.write_text(s)
# Existing numbered registry rows only; 093 absent from stale registry, no invented duplicate.
p=R/'cards/crypto/current-cards.json';j=json.loads(p.read_text())
for c in j['cards']:
 n=str(c.get('moment_number','')).zfill(3)
 if n in D:
  c['rarity']=D[n][2];c['rarity_status']='USER_SELECTED_'+D[n][2].upper()+'_2026_10_29';c['rarity_review_status']='Local revised frames prepared; publication pending'
p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
# Book chapter copies carry same metadata/notes changes.
for p in (R/'book/crypto-season-01/histrove-v1/chapters').glob('*.md'):
 s=p.read_text().replace(old,new) if False else p.read_text()
 s=s.replace('their separate Legendary and Common frames interrupt a literal edge-to-edge join.','their separate Legendary frames interrupt a literal edge-to-edge join.')
 n=p.name[:3]
 if n in D:s=s.replace('/ '+D[n][1].upper(),'/ '+D[n][2].upper())
 p.write_text(s)
(Q/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
