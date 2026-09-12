"""Populate the pinned LORE v3 template without regenerating its design.

Requires Pillow, qrcode and Inkscape. Use --reference for an exact Asmongold
reference rebuild, or --data with the fields shown by --write-example.
"""
from pathlib import Path
import argparse, base64, json, os, subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from PIL import ImageFont
import qrcode

MASTER=Path(__file__).resolve().parents[1]
SVG='http://www.w3.org/2000/svg'
XLINK='http://www.w3.org/1999/xlink'
ET.register_namespace('',SVG)
ET.register_namespace('xlink',XLINK)
FIELDS={'creator-name':'creator','title-line-1':'title_line_1','title-line-2':'title_line_2','moment-context':'context','moment-number':'moment_label','set-number':'set_label'}

def reference_data(index):
    cards=json.loads((MASTER/'source/asmongold-reference-data.json').read_text())
    c=cards[index-1]
    root=ET.parse(MASTER/c['reference_template']).getroot()
    by_id={n.get('id'):n for n in root.iter() if n.get('id')}
    data={key:by_id[node].text for node,key in FIELDS.items()}
    data.update(rarity=c['rarity'].lower(),artwork=str(MASTER/c['reference_art']),qr_url=c['qr_demo_payload'])
    return data

def render(data,out,demo=False):
    rarity=data['rarity'].lower()
    if rarity not in ['common','uncommon','rare','epic','legendary','mythic']:
        raise ValueError('Choose one of the six pinned rarity templates.')
    url=urlparse(data['qr_url'])
    if url.scheme!='https' or not url.hostname:raise ValueError('QR requires an HTTPS URL.')
    if url.hostname=='example.com' and not demo:raise ValueError('Demo QR requires --demo.')
    if url.hostname!='example.com' and not data.get('confirmed_lore_owned_route',False):
        raise ValueError('Confirm LORE ownership and the intended live route before inserting it.')
    root=ET.parse(MASTER/'templates'/f'{rarity}.svg').getroot()
    by_id={n.get('id'):n for n in root.iter() if n.get('id')}
    for node,key in FIELDS.items():
        value=data[key]
        if not isinstance(value,str) or not value.strip() or '\n' in value:
            raise ValueError(f'{key} must be one nonempty line.')
        n=by_id[node]
        font_name='DejaVuSans-Bold.ttf' if n.get('font-weight')=='700' else 'DejaVuSans.ttf'
        font=ImageFont.truetype(str(MASTER/'source/fonts'/font_name),int(n.get('font-size')))
        width=font.getlength(value)+float(n.get('letter-spacing','0'))*max(0,len(value)-1)
        right=float(n.get('x'))+width
        if right>620:raise ValueError(f'{key} overflows the fixed left column; review shorter copy. Do not resize the template.')
        n.text=value
    artwork=Path(data['artwork'])
    if not artwork.is_file():raise FileNotFoundError(artwork)
    if artwork.suffix.lower()!='.png':raise ValueError('Use a reviewed illustration PNG.')
    by_id['card-illustration'].set(f'{{{XLINK}}}href','data:image/png;base64,'+base64.b64encode(artwork.read_bytes()).decode())
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8)
    qr.add_data(data['qr_url']);qr.make(fit=True)
    matrix=qr.get_matrix();size=len(matrix)
    n=by_id['moment-qr'];n.set('viewBox',f'0 0 {size} {size}')
    for child in list(n):n.remove(child)
    ET.SubElement(n,f'{{{SVG}}}rect',{'width':str(size),'height':str(size),'fill':'#FFFFFF'})
    d=' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v)
    ET.SubElement(n,f'{{{SVG}}}path',{'d':d,'fill':'#000000'})
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
    env=os.environ.copy();env['FONTCONFIG_FILE']=str(MASTER/'source/fontconfig.xml')
    subprocess.run(['inkscape',str(out),'--export-type=png',f'--export-filename={out.with_suffix(".png")}'],env=env,check=True,capture_output=True)
    print(json.dumps({'svg':str(out),'png':str(out.with_suffix('.png')),'qr_modules_with_margin':size,'demo':demo}))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--reference',type=int,choices=range(1,7))
    group.add_argument('--data',type=Path)
    group.add_argument('--write-example',type=Path)
    p.add_argument('--out',type=Path)
    p.add_argument('--demo',action='store_true')
    args=p.parse_args()
    if args.write_example:
        args.write_example.write_text(json.dumps(reference_data(1),indent=2));return
    if not args.out:p.error('--out is required when rendering')
    data=reference_data(args.reference) if args.reference else json.loads(args.data.read_text())
    render(data,args.out,args.demo)

if __name__=='__main__':main()
