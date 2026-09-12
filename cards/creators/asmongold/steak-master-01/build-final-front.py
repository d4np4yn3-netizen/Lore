"""Build the final-placement steak proof from the pinned LORE template.

Only the artwork receives an authorised upward translation. No image generation,
retouching, non-uniform scaling or fixed-layout modification is performed.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MASTER = ROOT / 'cards/master/front-v3'
EXPECTED_ART = '109b68cc5c662feb5ee587d7e3bb935b02cfdcf6f59a72ff9202902a46680d61'

def main():
    art = HERE / 'art.png'
    assert hashlib.sha256(art.read_bytes()).hexdigest() == EXPECTED_ART
    spec = importlib.util.spec_from_file_location('lore_renderer', MASTER / 'source/render_card.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    data = json.loads((HERE / 'render-data.json').read_text())
    data['artwork'] = str(art)
    out = HERE / 'LORE-Asmongold-Steak-Final-v1.svg'
    renderer.render(data, out, demo=True)
    tree = ET.parse(out)
    illustration = next(n for n in tree.getroot().iter() if n.get('id') == 'card-illustration')
    illustration.set('transform', 'translate(0 -70)')
    tree.write(out, encoding='utf-8', xml_declaration=True)
    env = os.environ.copy()
    env['FONTCONFIG_FILE'] = str(MASTER / 'source/fontconfig.xml')
    subprocess.run(['inkscape', str(out), '--export-type=png', f'--export-filename={out.with_suffix(".png")}'], env=env, check=True, capture_output=True)
    print(json.dumps({'png': str(out.with_suffix('.png')), 'art_translation': [0, -70], 'art_unchanged': True, 'qr_is_demo': True}))

if __name__ == '__main__':
    main()
