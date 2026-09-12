"""Check exact art bytes, fixed UI, fonts, decoded QR and export hashes."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops
import zxingcpp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
XLINK = '{http://www.w3.org/1999/xlink}href'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def signature(n):
    return (n.tag, sorted(n.attrib.items()), (n.text or '').strip(), [signature(c) for c in n])

def main():
    old = ET.parse(HERE / 'front.svg').getroot()
    final = ET.parse(HERE / 'LORE-Asmongold-Steak-Final-v1.svg').getroot()
    node = next(n for n in final.iter() if n.get('id') == 'card-illustration')
    assert node.attrib.pop('transform') == 'translate(0 -70)'
    assert signature(old) == signature(final), 'Changes outside authorised art translation'
    embedded = base64.b64decode(node.get(XLINK).split(',', 1)[1])
    assert embedded == (HERE / 'art.png').read_bytes()
    assert digest(HERE / 'art.png') == '109b68cc5c662feb5ee587d7e3bb935b02cfdcf6f59a72ff9202902a46680d61'
    assert digest(HERE / 'approved-user-reference.jpeg') == '0a48548d4559cb6cf6c0c4452944e479edba330178eeb447957c4f82e3fb0306'
    image = Image.open(HERE / 'LORE-Asmongold-Steak-Final-v1.png')
    assert image.size == (900, 1260)
    payloads = [r.text for r in zxingcpp.read_barcodes(image)]
    assert payloads == ['https://example.com/m/asm/01']
    box = (644, 986, 842, 1184)
    assert ImageChops.difference(image.crop(box), Image.open(HERE / 'front.png').crop(box)).getbbox() is None
    approved_logo = ROOT / 'brand/assets/svg/lore_logo_compact_gold_white.svg'
    assert digest(approved_logo) == '7ab0c09e95441ff4e1b903e540b5155ba88a6bb5d30868019aeec81d1d48828a'
    template = ROOT / 'cards/master/front-v3/templates/common.svg'
    reference = subprocess.check_output(['git', 'show', 'origin/main:cards/master/front-v3/templates/common.svg'], cwd=ROOT)
    assert template.read_bytes() == reference
    fonts = ROOT / 'cards/master/front-v3/source/fonts'
    report = {
        'revision': 'LORE-ASM-STEAK-FRONT-FINAL-v1',
        'artwork_approval': 'APPROVED_BY_DANIEL_PAYNE',
        'placement_adjustment': 'EXPLICITLY_AUTHORISED_BY_USER',
        'delivered_composition': 'AWAITING_USER_CONFIRMATION',
        'art_transform': {'translate_x': 0, 'translate_y': -70, 'additional_scale': 1},
        'fixed_ui_structurally_identical': True,
        'approved_art_bytes_unchanged': True,
        'embedded_art_bytes_identical': True,
        'current_github_template_identical': True,
        'approved_logo_sha256': digest(approved_logo),
        'fonts': {p.name: digest(p) for p in sorted(fonts.glob('*.ttf'))},
        'png_dimensions': list(image.size),
        'qr_geometry': {'x': 644, 'y': 986, 'width': 198, 'height': 198},
        'qr_pixels_identical_to_prior_proof': True,
        'decoded_qr': payloads,
        'qr_live': False,
        'visual_review': 'Final PNG inspected: entire potato is above the unchanged QR square and caption; pan, steak, face and hands are clear. Head/hair remain inside the card, clear of the actual badge, counter and logo. Art shifted only; fixed overlay unchanged.',
        'art_sha256': digest(HERE / 'art.png'),
        'png_sha256': digest(HERE / 'LORE-Asmongold-Steak-Final-v1.png'),
        'svg_sha256': digest(HERE / 'LORE-Asmongold-Steak-Final-v1.svg'),
        'print_ready': False,
        'rarity_and_set_position': 'Provisional Common and 01/06'
    }
    (HERE / 'final-qa.json').write_text(json.dumps(report, indent=2) + '\n')
    manifest_path = HERE / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['front_status'] = 'FINAL_ASSEMBLY_AWAITING_USER_CONFIRMATION'
    manifest['current_front'] = 'LORE-Asmongold-Steak-Final-v1.png'
    manifest['current_svg'] = 'LORE-Asmongold-Steak-Final-v1.svg'
    manifest['placement_authorised_by_user'] = True
    manifest['placement'] = report['art_transform']
    manifest['checks']['visual_inspection'] = report['visual_review']
    manifest['final_qa'] = 'final-qa.json'
    manifest['historical_crop_proofs'] = ['front.png', 'front.svg']
    assets = []
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or p.name == 'manifest.json' or '__pycache__' in p.parts:
            continue
        entry = {'path': str(p.relative_to(HERE)), 'bytes': p.stat().st_size, 'sha256': digest(p)}
        if p.suffix.lower() in ['.png', '.jpeg']:
            entry['dimensions'] = list(Image.open(p).size)
        assets.append(entry)
    manifest['assets'] = assets
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
