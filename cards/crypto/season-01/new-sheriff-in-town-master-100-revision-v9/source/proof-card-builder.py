from pathlib import Path
import base64,hashlib,json,os,sys,subprocess,copy,xml.etree.ElementTree as E
from PIL import Image
sys.path.insert(0,str(Path('card069-proof/deps').resolve()));import zxingcpp
R=Path(__file__).resolve().parent;A=R.parent/'100-the-new-sheriff-art-v9-crisp-restored-candidate.png';T=R.parent/'card-proof-v4/HISTROVE-Crypto-100-New-Sheriff-Front-Proof-v4.svg';F=Path('card077-release/cards/master/front-v3/source').resolve();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(A)=='97de5699a1187cbfdc092a34d81794eb0648891decd2fd8089b7c0f2f1a50a80';assert H(T)=='147f9b28645568c857f30d9a07cf3f4c9fe9632721fd8984bbd6addb878333d5'
S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',S);E.register_namespace('xlink',X);root=E.parse(T).getroot();old=copy.deepcopy(root);ids={x.get('id'):x for x in root.iter() if x.get('id')};assert Image.open(A).size==(1060,1484)
expected={'creator-name':'GENIUS ACT','title-line-1':'NEW SHERIFF','title-line-2':'IN TOWN','moment-context':'NEW RULES. SAME FRONTIER.','moment-number':'18 JUL 2025','set-number':'CRYPTO • SEASON 01 • 100/100','rarity-label':'RARE'}
for k,v in expected.items():assert ids[k].text==v,(k,ids[k].text)
transform=ids['card-illustration'].get('transform');assert transform=='translate(-18 0) translate(450 14) scale(1.05) translate(-450 -14)'
original_href=ids['card-illustration'].get('{'+X+'}href');ids['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(A.read_bytes()).decode())
check=copy.deepcopy(root);ci={x.get('id'):x for x in check.iter() if x.get('id')};ci['card-illustration'].set('{'+X+'}href',original_href);assert E.tostring(check)==E.tostring(old),'changes outside illustration'
prefix='HISTROVE-Crypto-100-New-Sheriff';svg=R/(prefix+'-Front-Proof-v5.svg');E.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(F/'fontconfig.xml');env['XDG_CACHE_HOME']=str(R/'cache');subprocess.run(['inkscape',str(svg),'--export-type=png','--export-width=816','--export-height=1110','--export-filename='+str(svg.with_suffix('.png'))],env=env,check=True,capture_output=True)
im=Image.open(svg.with_suffix('.png')).convert('RGB');assert im.size==(816,1110);im.save(svg.with_suffix('.png'),dpi=(300,300));review=R/(prefix+'-Card-Review-v5.png');im.crop((36,36,780,1074)).save(review,dpi=(300,300));d=R/'inspection';d.mkdir(exist_ok=True);im.crop((70,72,745,290)).save(d/'header.png');im.crop((275,235,745,705)).save(d/'face-posters.png');im.crop((70,795,745,1040)).save(d/'footer.png')
qr={}
for p in [svg.with_suffix('.png'),review]:
 values=[x.text for x in zxingcpp.read_barcodes(Image.open(p))];assert values==['https://www.histrove.co.uk/crypto/100/'],values;qr[p.name]=values
qa={'status':'PASS technical, visual pending','scope':'Combined horizontal poster edge/no dollar sign review only; livev6/v2 unchanged','source_raw':str(A),'raw_sha256':H(A),'native_art_size':[1060,1484],'template_library_id':'libfile_60e9598ca15081919ceb78a0aba90be4','template_library_version':3,'template_sha256':H(T),'only_svg_change':'embedded illustration bytes','copy':expected,'art_transform_exact':transform,'canvas_px':[816,1110],'trim_px':[744,1038],'safe_px':[684,981],'dpi':300,'qr_payloads':qr,'original_QR_node_unchanged':True,'files':[{'path':str(p),'sha256':H(p)} for p in [review,svg.with_suffix('.png'),svg]],'no_publication_changes':True};(R/'QA-v5.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({'review':str(review),'qr':qr},indent=2))
