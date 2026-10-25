from pathlib import Path
import sys,os,base64,json,subprocess,hashlib,xml.etree.ElementTree as E
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path('card069-proof/deps').resolve()))
import qrcode,zxingcpp
p=Path('bull-pair'); S='http://www.w3.org/2000/svg'; X='http://www.w3.org/1999/xlink'; E.register_namespace('',S);E.register_namespace('xlink',X)
entries=[('018','Young-Bull','FOUR','A BULL TAKES ITS FIRST STEPS.','27 NOV 2013'),('095','Bull-Herd','SIX','NOW THE HERD FOLLOWS.','05 DEC 2024')]
qa=[]
for no,name,title,context,date in entries:
 r=E.parse(p/'common-template.svg').getroot();ids={n.get('id'):n for n in r.iter() if n.get('id')}
 for k,v in {'creator-name':'BITCOIN','title-line-1':title,'title-line-2':'FIGURES','moment-context':context,'moment-number':date,'set-number':f'CRYPTO • SEASON 01 • {no}/100'}.items():ids[k].text=v
 art=p/f'HISTROVE-{no}-{name}-Art-v1.png';ids['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(art.read_bytes()).decode())
 url=f'https://www.histrove.co.uk/crypto/{no}/'; qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4);qr.add_data(url);qr.make(fit=True);m=qr.get_matrix();node=ids['moment-qr'];node[:]=[];node.set('viewBox',f'0 0 {len(m)} {len(m)}');E.SubElement(node,'{'+S+'}rect',{'width':str(len(m)),'height':str(len(m)),'fill':'#fff'})
 for y,row in enumerate(m):
  for x,b in enumerate(row):
   if b:E.SubElement(node,'{'+S+'}rect',{'x':str(x),'y':str(y),'width':'1','height':'1','fill':'#000'})
 svg=p/f'HISTROVE-Crypto-{no}-Bull-Front-Proof-v2.svg';E.ElementTree(r).write(svg,encoding='utf-8',xml_declaration=True)
 env=os.environ.copy();env['FONTCONFIG_FILE']=str(Path('card077-release/cards/master/front-v3/source/fontconfig.xml').resolve());env['XDG_CACHE_HOME']=str((p/'cache').resolve());png=svg.with_suffix('.png');subprocess.run(['inkscape',str(svg),'--export-width=816','--export-height=1110',f'--export-filename={png}'],env=env,check=True,capture_output=True)
 im=Image.open(png).convert('RGB');im.save(png,dpi=(300,300));rev=im.crop((72,72,744,1038)).convert('RGBA');mask=Image.new('L',rev.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,671,965),radius=21,fill=255);rev.putalpha(mask);rp=p/f'HISTROVE-Crypto-{no}-Bull-Card-Proof-v2.png';rev.save(rp)
 qa.append({'number':no,'rarity':'Common','template_sha':'fe9537de4a82fee22b92c113dd9d7d708c451512','art_sha256':hashlib.sha256(art.read_bytes()).hexdigest(),'qr_decodes':[a.text for a in zxingcpp.read_barcodes(im)],'qr_route_status':'planned, not newly verified','context_status':'proposed paired editorial line, user requested preview, awaiting approval','dimensions':list(im.size),'card_path':str(rp)})
# Preview composition only: exact raster renders remain untouched.
can=Image.new('RGB',(1404,1014),'#15171b')
for i,q in enumerate(qa):
 im=Image.open(q['card_path']);can.paste(im,(20+i*692,24),im)
can.save(p/'HISTROVE-018-095-Bull-Card-Pair-v2.png')
(p/'card-proof-qa-v2.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
