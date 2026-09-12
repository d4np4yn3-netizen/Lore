"""Build signed-off v2 by replacing only the context text in preserved v1.

The v1 SVG already contains the exact approved art and authorised placement.
Keep every other byte of that SVG unchanged. Requires Pillow and Inkscape.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from PIL import ImageFont
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MASTER = ROOT / 'cards/master/front-v3'
EXPECTED_ART = '109b68cc5c662feb5ee587d7e3bb935b02cfdcf6f59a72ff9202902a46680d61'

def main():
    art = HERE / 'art.png'
    assert hashlib.sha256(art.read_bytes()).hexdigest() == EXPECTED_ART
    data = json.loads((HERE / 'render-data.json').read_text())
    assert data['context'] == 'I’M A SIMPLE MAN.'
    baseline = (HERE / 'LORE-Asmongold-Steak-Final-v1.svg').read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == 'ecb22e08a828d734ef0b5372f4d171c0cadf4ad34cc5100780e3f78dec0044fd'
    root = ET.fromstring(baseline)
    context = next(n for n in root.iter() if n.get('id') == 'moment-context')
    assert context.text == 'THE COOKING VIDEO'
    font = ImageFont.truetype(str(MASTER / 'source/fonts/DejaVuSans.ttf'), int(context.get('font-size')))
    text_width = font.getlength(data['context']) + float(context.get('letter-spacing')) * (len(data['context']) - 1)
    assert float(context.get('x')) + text_width <= 620
    old_text = b'>THE COOKING VIDEO<'
    assert baseline.count(old_text) == 1
    updated = baseline.replace(old_text, ('>' + escape(data['context']) + '<').encode('utf-8'), 1)
    out = HERE / 'LORE-Asmongold-Steak-Final-v2.svg'
    out.write_bytes(updated)
    env = os.environ.copy()
    env['FONTCONFIG_FILE'] = str(MASTER / 'source/fontconfig.xml')
    subprocess.run(['inkscape', str(out), '--export-type=png', f'--export-filename={out.with_suffix(".png")}'], env=env, check=True, capture_output=True)
    print(json.dumps({'png': str(out.with_suffix('.png')), 'context': data['context'], 'context_width': text_width, 'only_context_text_changed': True, 'art_unchanged': True, 'qr_is_demo': True}))

if __name__ == '__main__':
    main()
