"""Render a Crypto Season One card into the approved printer-sized front master.

LORE-CRYPTO-PRINT-v1.0
Canvas: 816x1110 px at 300 DPI
Trim:   744x1038 px
Safe:   684x981 px

The six templates already contain the approved uniform print inset and the
approved crypto phrase typography. Existing approved art should be supplied
unchanged.
"""
from pathlib import Path
import argparse, base64, json, os, subprocess
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from PIL import Image, ImageFont
import qrcode

MASTER=Path(__file__).resolve().parents[1]
FRONT_V4=MASTER.parents[2]/'master/front-v4'
FRONT_V3=MASTER.parents[2]/'master/front-v3'
sys_path=str(FRONT_V4/'source')

SVG='http://www.w3.org/2000/svg'
XLINK='http://www.w3.org/1999/xlink'
ET.register_namespace('',SVG)
ET.register_namespace('xlink',XLINK)

FIELDS={
    'creator-name':'creator',
    'title-line-1':'title_line_1',
    'title-line-2':'title_line_2',
    'moment-context':'context',
    'moment-number':'moment_label',
    'set-number':'set_label'
}

RARITIES=['common','uncommon','rare','epic','legendary','mythic']

def render(data,out,demo=False):
    rarity=data['rarity'].lower()
    if rarity not in RARITIES:
        raise ValueError('Choose one of the six approved rarity templates.')

    url=urlparse(data['qr_url'])
    if url.scheme!='https' or not url.hostname:
        raise ValueError('QR requires an HTTPS URL.')
    if url.hostname=='example.com' and not demo:
        raise ValueError('Demo QR requires --demo.')
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
        font=ImageFont.truetype(str(FRONT_V3/'source/fonts'/font_name),int(n.get('font-size')))
        width=font.getlength(value)+float(n.get('letter-spacing','0'))*max(0,len(value)-1)
        right=float(n.get('x'))+width
        if right>620:
            raise ValueError(f'{key} overflows the fixed left column; review copy instead of shrinking the template.')
        n.text=value

    artwork=Path(data['artwork'])
    if not artwork.is_file():
        raise FileNotFoundError(artwork)
    if artwork.suffix.lower()!='.png':
        raise ValueError('Use a reviewed illustration PNG.')

    by_id['card-illustration'].set(f'{{{XLINK}}}href',
        'data:image/png;base64,'+base64.b64encode(artwork.read_bytes()).decode())

    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8)
    qr.add_data(data['qr_url']); qr.make(fit=True)
    matrix=qr.get_matrix(); size=len(matrix)
    n=by_id['moment-qr']; n.set('viewBox',f'0 0 {size} {size}')
    for child in list(n): n.remove(child)
    ET.SubElement(n,f'{{{SVG}}}rect',{'width':str(size),'height':str(size),'fill':'#FFFFFF'})
    d=' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v)
    ET.SubElement(n,f'{{{SVG}}}path',{'d':d,'fill':'#000000'})

    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)

    env=os.environ.copy()
    env['FONTCONFIG_FILE']=str(FRONT_V3/'source/fontconfig.xml')
    subprocess.run([
        'inkscape',str(out),'--export-type=png',
        f'--export-filename={out.with_suffix(".png")}'
    ],env=env,check=True,capture_output=True)

    with Image.open(out.with_suffix('.png')) as exported:
        if exported.size!=(816,1110):
            raise ValueError(f'Unexpected print export size {exported.size}; expected (816, 1110).')

    print(json.dumps({
        'revision':'LORE-CRYPTO-PRINT-v1.0',
        'svg':str(out),
        'png':str(out.with_suffix('.png')),
        'canvas_px':[816,1110],
        'trim_px':[744,1038],
        'safe_px':[684,981],
        'demo':demo
    }))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--demo',action='store_true')
    a=p.parse_args()
    render(json.loads(a.data.read_text()),a.out,a.demo)

if __name__=='__main__':
    main()
