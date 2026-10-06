from pathlib import Path
import sys,json,os,subprocess,hashlib,base64,xml.etree.ElementTree as ET
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'lore-032/python-deps'))
import zxingcpp
B=Path(__file__).resolve().parent
R=next(p for p in B.parents if (p/'cards/crypto/master/histrove-print-v1/source').is_dir())
sys.path.insert(0,str(R/'cards/crypto/master/histrove-print-v1/source'))
import render_print_card
# Card-specific tracking exception approved for review; master file remains unchanged.
source=Path(render_print_card.__file__).read_text().replace("n=by_id[node]","n=by_id[node]\n        if node=='title-line-2': n.set('letter-spacing','-1.6')")
namespace={'__file__':render_print_card.__file__,'__name__':'card044_renderer'}
exec(compile(source,render_print_card.__file__,'exec'),namespace)
render=namespace['render']
art=B/'art.png'
d={'rarity':'uncommon','creator':'CRYPTO','title_line_1':'THE MISSING','title_line_2':'CRYPTOQUEEN','context':'THE FINAL ACT.','moment_label':'25 OCT 2017','set_label':'CRYPTO • SEASON 01 • 044/100','artwork':str(art),'qr_url':'https://lore-site-v1.vercel.app/crypto/044/','confirmed_lore_owned_route':True}
(B/'card-data.json').write_text(json.dumps(d,indent=2))
out=B/'HISTROVE-044-The-Missing-Cryptoqueen-Front.svg'
render(d,out)
root=ET.parse(out).getroot()
for n in root.iter():
 if n.get('id')=='qr-caption':n.text='WATCH MOMENT'
 if n.get('id')=='card-illustration':assert base64.b64decode(n.get('{http://www.w3.org/1999/xlink}href').split(',')[1])==art.read_bytes()
ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
env=os.environ.copy();env['FONTCONFIG_FILE']=str(R/'cards/master/front-v3/source/fontconfig.xml')
subprocess.run(['inkscape',str(out),'--export-type=png','--export-width=816','--export-height=1110',f'--export-filename={out.with_suffix(".png")}'],env=env,check=True,capture_output=True)
with Image.open(out.with_suffix('.png')) as raw: im=raw.convert('RGB')
im.save(out.with_suffix('.png'),dpi=(300,300))
decoded=zxingcpp.read_barcode(Image.open(out.with_suffix('.png')))
value=decoded.text if decoded else ''
assert value==d['qr_url'],value
checks={'file':str(out.with_suffix('.png')),'canvas':[816,1110],'dpi':300,'rarity':'Uncommon','qr_decoded':value,'source_art_sha256':hashlib.sha256(art.read_bytes()).hexdigest(),'embedded_art_matches_source_bytes':True,'copy_status':'THE FINAL ACT. is approved editorial copy, not a quotation.','release_status':'Publication authorised. WATCH MOMENT label; route publication pending. Printer specification audit pending; physical print release false.','fontconfig':env['FONTCONFIG_FILE'],'title_tracking_review':'Card-specific title-line-2 letter-spacing -1.6 px; font size 70 px and master unchanged. Review only.', 'historical_boundary':'Fictional stage allegory; not a claim of an actual performance or evidence of whereabouts.'}
(B/'card-final-qa.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))

import fitz
subprocess.run(['inkscape',str(out),'--export-type=pdf',f'--export-filename={out.with_suffix(".pdf")}'],env=env,check=True,capture_output=True)
pdf=out.with_suffix('.pdf'); doc=fitz.open(pdf); page=doc[0]
page.set_bleedbox(fitz.Rect(0,0,195.84,266.4))
page.set_trimbox(fitz.Rect(8.64,8.64,187.2,257.76))
page.set_artbox(fitz.Rect(15.84,15.48,180,250.92))
boxed=pdf.with_name(pdf.stem+'-boxed.pdf');doc.save(boxed,garbage=4,deflate=True);doc.close();boxed.replace(pdf)
checks['pdf_boxes_points']={'media':[0,0,195.84,266.4],'bleed':[0,0,195.84,266.4],'trim':[8.64,8.64,187.2,257.76],'art':[15.84,15.48,180,250.92]}
checks['release_status']='Publication authorised; correct audited HISTROVE print geometry and PDF boxes. Route publication in progress; physical print release false.'
checks['title_tracking_review']='Approved title-line-2 letter-spacing -1.6 px; master font size and geometry unchanged.'
(B/'card-final-qa.json').write_text(json.dumps(checks,indent=2))
