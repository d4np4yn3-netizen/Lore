from pathlib import Path
import base64,hashlib,json,os,sys,subprocess,xml.etree.ElementTree as ET,copy
from PIL import Image,ImageFont,ImageDraw
sys.path.insert(0,str(Path('card069-proof/deps').resolve()))
import qrcode,zxingcpp
R=Path(__file__).resolve().parent;ART=Path(sys.argv[1]).resolve();T=R/'sources/rare.svg';F=Path('card077-release/cards/master/front-v3/source').resolve();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(ART)==sys.argv[2], 'final raw hash mismatch'
# Fresh remote text was saved with final newline; XML identity checked against verified local template.
NS='http://www.w3.org/2000/svg';XL='http://www.w3.org/1999/xlink';ET.register_namespace('',NS);ET.register_namespace('xlink',XL)
root=ET.parse(T).getroot();original=copy.deepcopy(root);ids={n.get('id'):n for n in root.iter() if n.get('id')}
texts={'creator-name':'GENIUS ACT','title-line-1':'NEW SHERIFF','title-line-2':'IN TOWN','moment-context':'NEW RULES. SAME FRONTIER.','moment-number':'18 JUL 2025','set-number':'CRYPTO • SEASON 01 • 100/100'}
widths={}
for k,text in texts.items():
 n=ids[k];f=ImageFont.truetype(str(F/'fonts'/('DejaVuSans-Bold.ttf' if n.get('font-weight')=='700' else 'DejaVuSans.ttf')),int(n.get('font-size')));w=f.getlength(text)+float(n.get('letter-spacing','0'))*(len(text)-1);widths[k]={'width':w,'right':float(n.get('x'))+w};assert widths[k]['right']<620,(k,widths[k]);n.text=text
assert ids['rarity-label'].text=='RARE'
ids['card-illustration'].set('{'+XL+'}href','data:image/png;base64,'+base64.b64encode(ART.read_bytes()).decode())
ids['card-illustration'].set('transform','translate(-18 0) translate(450 14) scale(1.05) translate(-450 -14)')
route='https://www.histrove.co.uk/crypto/100/';qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8);qr.add_data(route);qr.make(fit=True);matrix=qr.get_matrix();n=ids['moment-qr'];n.set('viewBox',f'0 0 {len(matrix)} {len(matrix)}')
for child in list(n):n.remove(child)
ET.SubElement(n,'{'+NS+'}rect',{'width':str(len(matrix)),'height':str(len(matrix)),'fill':'#FFFFFF'});ET.SubElement(n,'{'+NS+'}path',{'d':' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v),'fill':'#000000'})
# Only approved copy/art/QR slots may differ; geometry, typography, gradients, logo and frame stay byte-equivalent XML.
new=copy.deepcopy(root);ni={x.get('id'):x for x in new.iter() if x.get('id')};oi={x.get('id'):x for x in original.iter() if x.get('id')}
for k in texts:ni[k].text=oi[k].text
ni['card-illustration'].attrib=oi['card-illustration'].attrib.copy();ni['moment-qr'].attrib=oi['moment-qr'].attrib.copy()
for child in list(ni['moment-qr']):ni['moment-qr'].remove(child)
for child in oi['moment-qr']:ni['moment-qr'].append(copy.deepcopy(child))
assert ET.tostring(new)==ET.tostring(original),'template drift'
prefix='HISTROVE-Crypto-100-New-Sheriff';svg=R/(prefix+'-Front-Proof-v2.svg');ET.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(F/'fontconfig.xml');env['XDG_CACHE_HOME']=str(R/'cache');subprocess.run(['inkscape',str(svg),'--export-type=png','--export-width=816','--export-height=1110','--export-filename='+str(svg.with_suffix('.png'))],env=env,check=True,capture_output=True)
im=Image.open(svg.with_suffix('.png')).convert('RGB');assert im.size==(816,1110);im.save(svg.with_suffix('.png'),dpi=(300,300));review=im.crop((36,36,780,1074));reviewpath=R/(prefix+'-Card-Review-v2.png');review.save(reviewpath,dpi=(300,300))
d=R/'inspection';d.mkdir(exist_ok=True);im.crop((70,72,740,280)).save(d/'header.png');im.crop((200,230,742,670)).save(d/'face-notices.png');im.crop((70,795,745,1040)).save(d/'footer.png')
qrresults={}
for p in [svg.with_suffix('.png'),reviewpath]:
 q=[x.text for x in zxingcpp.read_barcodes(Image.open(p))];assert q==[route],(p,q);qrresults[p.name]=q
qa={'status':'PASS technical; visual inspection pending','source_art':str(ART),'source_sha256':H(ART),'source_dimensions':[1060,1484],'raw_embedded_unchanged':True,'template_source':'cards/crypto/master/histrove-print-v1/templates/rare.svg','verified_template_sha256':'ff9c1a840fca644acf240cf3a76028748105ee4e0d3c945db889d5902207720a','copy':texts,'copy_status':'User approved composition/copy on 2026-10-27 18:51; this proof tests only tiny pullback for logo clearance; publication not authorized','rarity':'RARE','canvas_px':[816,1110],'dpi':300,'cut_px':[744,1038],'safe_px':[684,981],'standard_art_crop':'xMidYMid slice plus authorized top-anchored 1.05 uniform crop and 18 inner-unit left pan of extended v6 raw; no warp, no blank edges; overall scene remains modestly pulled back from v5','template_unchanged_except_copy_art_QR':True,'width_checks':widths,'qr':qrresults,'qr_route_status':'intended numbered collection route; 100 not published','files':[{ 'path':str(p),'sha256':H(p)} for p in [reviewpath,svg.with_suffix('.png'),svg]],'publication_authorized':False}
(R/'QA-v2.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({'review':str(reviewpath),'source_hash':H(ART),'qr':qrresults,'widths':widths},indent=2))
