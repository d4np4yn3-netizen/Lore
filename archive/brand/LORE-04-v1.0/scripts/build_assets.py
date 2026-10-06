#!/usr/bin/env python3
"""Export the approved LORE artwork. Requires Inkscape and Pillow."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from xml.sax.saxutils import escape
import hashlib
import json
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / 'brand'
MASTER = BRAND / 'source/master-components.json'
M = json.loads(MASTER.read_text())
ASSETS = []
GOLD = '#D4AF37'
INK = '#0B0B0B'
BONE = '#F5F2EB'


def component(shape, x, y, width, colour):
    x0, y0, x1, y1 = shape['bounds']
    scale = width / (x1 - x0)
    return (f'<g transform="translate({x:.6f} {y:.6f}) scale({scale:.8f}) '
            f'translate({-x0:.6f} {-y0:.6f})"><path fill="{colour}" '
            f'fill-rule="evenodd" d="{shape["d"]}"/></g>')


def crown(x, y, width, colour):
    return component(M['crown'], x, y, width, colour)


def wordmark(x, y, width, colour):
    return component(M['wordmark'], x, y, width, colour)


def tagline(key, x, y, width, colour):
    return component(M['taglines'][key], x, y, width, colour)


def document(width, height, body, title, description):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">'
            f'{escape(description)}</desc>{body}</svg>')


def add(name, width, height, body, png_width, role, colours, transparent=True, copy=None):
    svg = BRAND / 'assets/svg' / (name + '.svg')
    png = BRAND / 'assets/png' / (name + '.png')
    svg.parent.mkdir(parents=True, exist_ok=True)
    png.parent.mkdir(parents=True, exist_ok=True)
    svg.write_text(document(width, height, body, f'LORE — {role}',
        'LORE-04-v1.0. Approved Rising Strokes crown and preserved LORE lettering. '
        'Vector paths; flat fills; derived from the locked component master.'))
    ASSETS.append(dict(name=name, svg=str(svg.relative_to(ROOT)), png=str(png.relative_to(ROOT)),
        png_width=png_width, viewbox=[0, 0, width, height], role=role, colours=colours,
        transparent=transparent, copy=copy))


def render(svg, png, width):
    for attempt in range(3):
        subprocess.run(['inkscape', str(svg), '--export-type=png',
            f'--export-width={width}', f'--export-filename={png}'], check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            with Image.open(png) as im:
                im.load()
                if im.width != width:
                    raise ValueError('Incorrect PNG export width')
            return
        except (OSError, ValueError):
            if attempt == 2:
                raise


def main():
    ASSETS.clear()
    for name, colour in [('gold', GOLD), ('white', '#FFFFFF'), ('black', '#000000')]:
        b = M['crown']['bounds']
        height = 1000 * (b[3] - b[1]) / (b[2] - b[0])
        add(f'lore_crown_{name}', 1200, 1200, crown(100, (1200-height)/2, 1000, colour),
            2048, 'Crown', [colour])
    for variant, cc, lc in [('gold_white', GOLD, '#FFFFFF'), ('gold_black', GOLD, '#000000'),
                            ('white', '#FFFFFF', '#FFFFFF'), ('black', '#000000', '#000000')]:
        # Keep the exact groups and transforms from the approved option 04 proof.
        groups = [M['primary_groups'][0].replace(GOLD, cc)] + [
            g.replace('#FFFFFF', lc) for g in M['primary_groups'][1:]]
        add(f'lore_logo_primary_{variant}', 1200, 1020, ''.join(groups), 4096,
            'Primary logo with tagline', [cc, lc], copy='COLLECT THE INTERNET.')
        add(f'lore_logo_compact_{variant}', 1200, 950, ''.join(groups[:2]), 4096,
            'Compact logo', [cc, lc])
        cb = M['crown']['bounds']; wb = M['wordmark']['bounds']
        ch = 240 * (cb[3]-cb[1])/(cb[2]-cb[0])
        wh = 1050 * (wb[3]-wb[1])/(wb[2]-wb[0])
        body = crown(100, 100 + wh/2 - ch/2, 240, cc) + wordmark(410, 100, 1050, lc)
        body += tagline('tagline_primary', 455, 710, 960, lc)
        add(f'lore_lockup_horizontal_{variant}', 1560, 860, body, 4096,
            'Horizontal logo with tagline', [cc, lc], copy='COLLECT THE INTERNET.')
    for name, colour in [('white', '#FFFFFF'), ('black', '#000000')]:
        add(f'lore_wordmark_{name}', 1200, 740, wordmark(100, 100, 1000, colour),
            4096, 'Wordmark', [colour])
        for key, shape in M['taglines'].items():
            add('lore_' + key + '_' + name, 1400, 300, tagline(key, 100, 110, 1200, colour),
                4096, shape['text'], [colour], copy=shape['text'])
    for name, fg, bg in [('gold_dark', GOLD, INK), ('white_dark', '#FFFFFF', INK),
                          ('black_light', '#000000', BONE), ('gold_light', GOLD, BONE)]:
        cb = M['crown']['bounds']; height = 340 * (cb[3]-cb[1])/(cb[2]-cb[0])
        body = f'<rect width="512" height="512" fill="{bg}"/>' + crown(86, (512-height)/2, 340, fg)
        add('lore_avatar_' + name, 512, 512, body, 1024, 'Social avatar', [fg, bg], False)
    add('lore_app_icon_dark', 512, 512, '<rect width="512" height="512" fill="#0B0B0B"/>' +
        wordmark(48, 145, 416, '#FFFFFF'), 512, 'App icon', ['#FFFFFF', INK], False)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda a: render(ROOT/a['svg'], ROOT/a['png'], a['png_width']), ASSETS))
    manifest = dict(revision=M['revision'], date='2026-09-11', release_status='VALIDATION_PENDING',
        source_master='brand/source/master-components.json', source_master_sha256=hashlib.sha256(MASTER.read_bytes()).hexdigest(),
        approval_record='operations/10-BRAND-APPROVAL-04.md', approved_by='Daniel Payne',
        approved_at='2026-09-11', approved_exports=[], assets=ASSETS)
    (BRAND/'assets/asset-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'Exported {len(ASSETS)} SVGs and {len(ASSETS)} PNGs from the approved master.')


if __name__ == '__main__':
    main()
