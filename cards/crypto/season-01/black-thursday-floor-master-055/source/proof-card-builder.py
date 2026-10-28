from pathlib import Path
import base64,hashlib,json,os,sys,subprocess,copy,xml.etree.ElementTree as E
from PIL import Image
sys.path.insert(0,str(Path('card069-proof/deps').resolve()));import zxingcpp
R=Path(__file__).resolve().parent;A=R.parent/'HISTROVE-055-Bear-Crash-Floor-FINAL-Crisp-Calendar-v3.png';T=R/'sources/055-current-approved.svg';F=Path('card077-release/cards/master/front-v3/source').resolve();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(T)=='12d7db0e7c7a1029b54508dcfbcb15222cb9a5767077eaae4c25f737ce076e38'
S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',S);E.register_namespace('xlink',X);root=E.parse(T).getroot();old=copy.deepcopy(root);ids={x.get('id'):x for x in root.iter() if x.get('id')};assert Image.open(A).size==(1060,1484)
expected={'creator-name':'BITCOIN','title-line-1':'BLACK','title-line-2':'THURSDAY','moment-context':'STILL HODLING.','moment-number':'12 MAR 2020','set-number':'CRYPTO • SEASON 01 • 055/100','rarity-label':'RARE'}
for k,v in expected.items():assert ids[k].text==v,(k,ids[k].text)
original_href=ids['card-illustration'].get('{'+X+'}href');ids['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(A.read_bytes()).decode())
check=copy.deepcopy(root);ci={x.get('id'):x for x in check.iter() if x.get('id')};ci['card-illustration'].set('{'+X+'}href',original_href);assert E.tostring(check)==E.tostring(old),'changes outside illustration'
prefix='HISTROVE-Crypto-055-Bear-Floor';svg=R/(prefix+'-Front-Proof-v3.svg');E.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(F/'fontconfig.xml');env['XDG_CACHE_HOME']=str(R/'cache');subprocess.run(['inkscape',str(svg),'--export-type=png','--export-width=816','--export-height=1110','--export-filename='+str(svg.with_suffix('.png'))],env=env,check=True,capture_output=True)
im=Image.open(svg.with_suffix('.png')).convert('RGB');assert im.size==(816,1110);im.save(svg.with_suffix('.png'),dpi=(300,300));review=R/(prefix+'-Card-Review-v3.png');im.crop((36,36,780,1074)).save(review,dpi=(300,300));d=R/'inspection';d.mkdir(exist_ok=True);im.crop((70,72,745,260)).save(d/'header.png');im.crop((90,400,745,790)).save(d/'floor-hands-bear.png');im.crop((70,795,745,1040)).save(d/'footer.png')
qr={}
for p in [svg.with_suffix('.png'),review]:
 values=[x.text for x in zxingcpp.read_barcodes(Image.open(p))];assert values==['https://lore-site-v1.vercel.app/crypto/055/'],values;qr[p.name]=values
qa={'status':'PASS technical, visual pending','scope':'Separate approved floor composition proof; earlier proofs and published055 unchanged','source_raw':str(A),'raw_sha256':H(A),'native_art_size':[1060,1484],'template_origin':'https://raw.githubusercontent.com/d4np4yn3-netizen/Lore/d851a0a80955a5c7903e9c713f8cbbfaba6e79af/cards/crypto/print-ready/histrove-v1/fronts/svg/HISTROVE-Crypto-055-Front-Print-v1.svg','template_sha256':H(T),'only_svg_change':'embedded illustration bytes','copy':expected,'art_crop':'Exact canonical xMidYMid slice, no extra zoom/pan/warp/padding','canvas_px':[816,1110],'trim_px':[744,1038],'safe_px':[684,981],'dpi':300,'qr_payloads':qr,'original_QR_node_unchanged':True,'files':[{'path':str(p),'sha256':H(p)} for p in [review,svg.with_suffix('.png'),svg]],'no_publication_or_book_changes':True};(R/'QA-v3.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({'review':str(review),'qr':qr},indent=2))
