from pathlib import Path
import json,base64,xml.etree.ElementTree as ET,subprocess,os
import qrcode
from PIL import Image
D=Path(__file__).resolve().parent
S='http://www.w3.org/2000/svg'; X='http://www.w3.org/1999/xlink'
ET.register_namespace('',S);ET.register_namespace('xlink',X)
url='https://lore-site-v1.vercel.app/scan/076/'
q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4);q.add_data(url);q.make(fit=True);m=q.get_matrix();n=len(m)
root=ET.Element('{%s}svg'%S,{'viewBox':'0 0 1033 1523','width':'1033','height':'1523'})
ET.SubElement(root,'{%s}image'%S,{'width':'1033','height':'1523','{%s}href'%X:'data:image/png;base64,'+base64.b64encode((D/'HISTROVE-Crypto-076-Raw-v17.png').read_bytes()).decode()})
# Screen-mounted digital QR, following the near LED band's slope.
import copy
screen=ET.SubElement(root,'{%s}g'%S,{'transform':'matrix(1 0.13 0 0.95 480 260)'})
g=ET.SubElement(screen,'{%s}svg'%S,{'id':'tv-scan-qr','x':'0','y':'0','width':'250','height':'250','viewBox':f'0 0 {n} {n}','shape-rendering':'crispEdges'})
ET.SubElement(g,'{%s}rect'%S,{'width':str(n),'height':str(n),'fill':'#ffffff'})
ET.SubElement(g,'{%s}path'%S,{'fill':'#000000','d':' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(m) for x,v in enumerate(row) if v)})
ET.ElementTree(root).write(D/'HISTROVE-Crypto-076-Art-QR-v17.svg')
subprocess.run(['inkscape',str(D/'HISTROVE-Crypto-076-Art-QR-v17.svg'),'--export-type=png',f'--export-filename={D}/HISTROVE-Crypto-076-Art-QR-v17.png'],check=True,capture_output=True)
data={'rarity':'common','creator':'COINBASE','title_line_1':'THE','title_line_2':'BOUNCING QR','context':'SUPER BOWL LVI','moment_label':'13 FEB 2022','set_label':'CRYPTO • 076/100','qr_url':'https://lore-site-v1.vercel.app/crypto/076/','confirmed_lore_owned_route':True,'artwork':str(D/'HISTROVE-Crypto-076-Art-QR-v17.png')}
(D/'card-data-v17.json').write_text(json.dumps(data,indent=2))
subprocess.run(['python',str(D.parent/'card075-proof/render_print_card.py'),'--data',str(D/'card-data-v17.json'),'--out',str(D/'HISTROVE-Crypto-076-Card-Proof-v17.svg')],check=True)
# Restore TV overlay as true vector in final frame as well, using the exact image cover transform.
p=D/'HISTROVE-Crypto-076-Card-Proof-v17.svg'; tree=ET.parse(p);r=tree.getroot();im=next(i for i in r.iter() if i.get('id')=='card-illustration'); parent=next(i for i in r.iter() if im in list(i))
scale=max(872/1033,1259.625/1523); ox=14+(872-1033*scale)/2; oy=14+(1259.625-1523*scale)/2
wrapper=ET.SubElement(parent,'{%s}g'%S,{'transform':f'translate({ox} {oy}) scale({scale})','id':'vector-tv-qr-overlay'})
wrapper.append(copy.deepcopy(screen))
tree.write(p,encoding='utf-8',xml_declaration=True)
subprocess.run(['inkscape',str(p),'--export-type=png','--export-width=816','--export-height=1110',f'--export-filename={p.with_suffix(".png")}'],check=True,capture_output=True)
a=Image.open(p.with_suffix('.png')).convert('RGB');a.save(p.with_suffix('.png'),dpi=(300,300));a.crop((36,36,780,1074)).save(D/'HISTROVE-Crypto-076-Trim-v17.png');a.resize((408,555)).save(D/'qa-small-v17.png')
print('TV modules including quiet zone:',n)
