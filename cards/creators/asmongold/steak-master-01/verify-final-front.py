"""Verify signed-off v2: context-only change, exact art, QR and file hashes.

Requires Pillow and zxing-cpp. Approval comes from the recorded user instruction.
"""
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
    old = ET.parse(HERE / 'LORE-Asmongold-Steak-Final-v1.svg').getroot()
    final = ET.parse(HERE / 'LORE-Asmongold-Steak-Final-v2.svg').getroot()
    node = next(n for n in final.iter() if n.get('id') == 'card-illustration')
    assert node.get('transform') == 'translate(0 -70)'
    context = next(n for n in final.iter() if n.get('id') == 'moment-context')
    assert context.text == 'I’M A SIMPLE MAN.'
    context.text = 'THE COOKING VIDEO'
    assert signature(old) == signature(final), 'Changes outside approved context wording'
    embedded = base64.b64decode(node.get(XLINK).split(',', 1)[1])
    assert embedded == (HERE / 'art.png').read_bytes()
    assert digest(HERE / 'art.png') == '109b68cc5c662feb5ee587d7e3bb935b02cfdcf6f59a72ff9202902a46680d61'
    assert digest(HERE / 'approved-user-reference.jpeg') == '0a48548d4559cb6cf6c0c4452944e479edba330178eeb447957c4f82e3fb0306'
    image = Image.open(HERE / 'LORE-Asmongold-Steak-Final-v2.png')
    assert image.size == (900, 1260)
    baseline_image = Image.open(HERE / 'LORE-Asmongold-Steak-Final-v1.png')
    difference = ImageChops.difference(image.convert('RGB'), baseline_image.convert('RGB'))
    changed_bbox = difference.getbbox()
    assert changed_bbox is not None
    x0, y0, x1, y1 = changed_bbox
    assert 54 <= x0 < x1 <= 620 and 1130 <= y0 < y1 <= 1160, changed_bbox
    assert ImageChops.difference(image.getchannel('A'), baseline_image.getchannel('A')).getbbox() is None
    payloads = [r.text for r in zxingcpp.read_barcodes(image)]
    assert payloads == ['https://example.com/m/asm/01']
    box = (644, 986, 842, 1184)
    assert ImageChops.difference(image.crop(box).convert('RGB'), baseline_image.crop(box).convert('RGB')).getbbox() is None
    approved_logo = ROOT / 'brand/assets/svg/lore_logo_compact_gold_white.svg'
    assert digest(approved_logo) == '7ab0c09e95441ff4e1b903e540b5155ba88a6bb5d30868019aeec81d1d48828a'
    template = ROOT / 'cards/master/front-v3/templates/common.svg'
    reference = subprocess.check_output(['git', 'show', 'origin/main:cards/master/front-v3/templates/common.svg'], cwd=ROOT)
    assert template.read_bytes() == reference
    fonts = ROOT / 'cards/master/front-v3/source/fonts'
    report = {
        'revision': 'LORE-ASM-STEAK-FRONT-FINAL-v2',
        'artwork_approval': 'APPROVED_BY_DANIEL_PAYNE',
        'placement_adjustment': 'EXPLICITLY_AUTHORISED_BY_USER',
        'delivered_composition': 'VISUAL_APPROVED_BY_DANIEL_PAYNE',
        'approval_record': 'operations/15-STEAK-V2-VISUAL-SIGNOFF-2026-09-12.md',
        'context': 'I’M A SIMPLE MAN.',
        'phrase_primary_source_verified': False,
        'only_context_text_changed_from_v1': True,
        'png_changed_bbox': list(changed_bbox),
        'pixels_outside_context_identical': True,
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
        'visual_review': 'v2 PNG inspected: I’M A SIMPLE MAN. is clear on the existing context baseline. Pixel changes are confined to that line; artwork, art placement, other text, fonts, logo, border, QR and alpha remain unchanged from v1. The potato remains clear of the QR.',
        'art_sha256': digest(HERE / 'art.png'),
        'png_sha256': digest(HERE / 'LORE-Asmongold-Steak-Final-v2.png'),
        'svg_sha256': digest(HERE / 'LORE-Asmongold-Steak-Final-v2.svg'),
        'print_ready': False,
        'rarity_and_set_position': 'Provisional Common and 01/06'
    }
    (HERE / 'final-qa-v2.json').write_text(json.dumps(report, indent=2) + '\n')
    manifest_path = HERE / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['front_status'] = 'VISUAL_APPROVED'
    manifest['front_revision'] = report['revision']
    manifest['front_approval'] = {'approved_by': 'Daniel Payne', 'date': '2026-09-12', 'record': report['approval_record'], 'scope': 'Existing delivered composition with the specified context phrase replacement; visual sign-off only'}
    manifest['current_front'] = 'LORE-Asmongold-Steak-Final-v2.png'
    manifest['current_svg'] = 'LORE-Asmongold-Steak-Final-v2.svg'
    manifest['context_phrase'] = {'text': report['context'], 'selected_by': 'Daniel Payne', 'primary_source_verified': False, 'evidence': 'source-notes.md', 'standard': 'cards/11-MOMENT-PHRASE-STANDARD.md'}
    manifest['placement_authorised_by_user'] = True
    manifest['placement'] = report['art_transform']
    manifest['checks']['visual_inspection'] = report['visual_review']
    manifest['checks']['context_only_change_from_v1'] = True
    manifest['checks']['png_changed_bbox'] = report['png_changed_bbox']
    manifest['final_qa'] = 'final-qa-v2.json'
    manifest['historical_assemblies'] = ['LORE-Asmongold-Steak-Final-v1.png', 'LORE-Asmongold-Steak-Final-v1.svg']
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
