#!/usr/bin/env python3
"""Reproduce approved HISTROVE Crypto 045 from exact art and locked shared master.

Install Pillow, qrcode, pypdf and Inkscape. Run from any directory:
  python3 build_card.py
Optional: --repo-root /path/to/Lore --data /path/to/card-data.json --out-dir /path/to/output
The default data file and outputs are beside this script in bitconnect-master-045.
Shared templates/renderers/fonts are never modified.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

ART_SHA256 = '06a19f961a37259c8c3d1bf194cf4b8711a920e92e99a12619092428f939a95b'
TEMPLATE_SHA256 = 'ff9c1a840fca644acf240cf3a76028748105ee4e0d3c945db889d5902207720a'
PINNED_SOURCE_SHA256 = {'cards/crypto/master/histrove-print-v1/source/render_print_card.py': 'ee2ee44ab4ef6649622a1f734b436a152c79e2e24f55c2396926b86aabc55be8', 'cards/crypto/master/histrove-print-v1/source/export_print_pdf.py': 'e3911115a74ae6eede1b00cca3af133ad953398df7c89cfcd1c5754810a081ed', 'cards/master/front-v3/source/fontconfig.xml': '0fc4fe1d9d8d5af9c4f05bf1951bf089b67c501661af7e40dfc52874bb06652f', 'cards/master/front-v3/source/fonts/DejaVuSans.ttf': 'ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280', 'cards/master/front-v3/source/fonts/DejaVuSans-Bold.ttf': '5c1247acef7f2b8522a31742c76d6adcb5569bacc0be7ceaa4dc39dd252ce895'}
BASENAME = 'HISTROVE-Crypto-045-Front-Print-v1'
MASTER_REL = Path('cards/crypto/master/histrove-print-v1')
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root', type=Path)
    p.add_argument('--data', type=Path, default=here/'card-data.json')
    p.add_argument('--out-dir', type=Path, default=here)
    args = p.parse_args()
    root = args.repo_root.resolve() if args.repo_root else next(
        (d for d in [here, *here.parents] if (d/MASTER_REL/'templates/rare.svg').is_file()), None)
    if root is None:
        raise SystemExit('Could not locate repository. Supply --repo-root.')
    master = root/MASTER_REL
    for relative, expected_hash in PINNED_SOURCE_SHA256.items():
        if sha(root/relative) != expected_hash:
            raise SystemExit(f'Pinned source changed: {relative}; review before rebuilding.')
    if sha(master/'templates/rare.svg') != TEMPLATE_SHA256:
        raise SystemExit('Locked Rare template changed; review before rebuilding.')
    data_path = args.data.resolve()
    data = json.loads(data_path.read_text())
    art = Path(data['artwork'])
    if not art.is_absolute(): art = data_path.parent/art
    art = art.resolve()
    if sha(art) != ART_SHA256:
        raise SystemExit('Artwork is not the exact approved v3 source.')
    if Image.open(art).size != (1060, 1484):
        raise SystemExit('Artwork dimensions changed.')
    expected = {'rarity':'rare', 'creator':'BITCONNECT', 'title_line_1':'BITCONNECT',
        'title_line_2':'', 'context':'HEY, HEY, HEY!', 'moment_label':'28 OCT 2017',
        'set_label':'CRYPTO • SEASON 01 • 045/100',
        'qr_url':'https://lore-site-v1.vercel.app/crypto/045/'}
    for key, value in expected.items():
        if data.get(key) != value:
            raise SystemExit(f'Approved field changed: {key}')
    data['artwork'] = str(art)
    data['confirmed_lore_owned_route'] = True
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir/(BASENAME+'.svg')
    spec = importlib.util.spec_from_file_location('histrove_renderer', master/'source/render_print_card.py')
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    with tempfile.TemporaryDirectory() as tmp:
        temp_master = Path(tmp)
        (temp_master/'templates').mkdir()
        tree = ET.parse(master/'templates/rare.svg')
        for node in tree.getroot().iter():
            if node.get('id') == 'title-line-2': node.text = None
        tree.write(temp_master/'templates/rare.svg', encoding='utf-8', xml_declaration=True)
        # One-card approved exception: BITCONNECT is one word; second title stays empty.
        # Its existing baseline, font, size and tracking are retained unchanged.
        renderer.MASTER = temp_master
        renderer.FIELDS = {k:v for k,v in renderer.FIELDS.items() if k != 'title-line-2'}
        renderer.render(data, out)
    pdf = out.with_suffix('.pdf')
    subprocess.run([sys.executable, str(master/'source/export_print_pdf.py'), str(out), str(pdf)], check=True)
    reader = PdfReader(pdf)
    page = reader.pages[0]
    # Eliminate Inkscape float rounding only; content coordinates and scale are unchanged.
    page.mediabox = RectangleObject([0, 0, 195.84, 266.4])
    page.cropbox = RectangleObject([0, 0, 195.84, 266.4])
    writer = PdfWriter()
    writer.add_page(page)
    with pdf.open('wb') as stream: writer.write(stream)
    with Image.open(out.with_suffix('.png')) as image:
        image.crop((36, 36, 780, 1074)).save(args.out_dir/'HISTROVE-Crypto-045-Front-Web-v1.png')
    print(json.dumps({'art_sha256':sha(art), 'output_directory':str(args.out_dir.resolve()),
        'files':[{'path':str(path.resolve()),'sha256':sha(path)} for path in sorted(args.out_dir.glob('HISTROVE-Crypto-045-*'))]}))

if __name__ == '__main__': main()
