"""Produce the approved badge-only revision of existing LORE cards.

Run from any directory. Original SVG/PNG/art files remain immutable. The
new SVG differs only at the badge. Existing PNG pixels outside that badge's
rectangle are retained, protecting against renderer-version raster drift.
"""
from pathlib import Path
import copy, hashlib, json, os, subprocess, tempfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from badge_spacing import apply_badge_spacing, badge_nodes, MASTER

REPO = MASTER.parents[2]
ENV = os.environ.copy()
ENV['FONTCONFIG_FILE'] = str(MASTER.parent/'front-v3/source/fontconfig.xml')
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)
CARDS = [
    ('steak-master-01', 'LORE-Asmongold-Steak-Final-v2', 'LORE-Asmongold-Steak-Final-v3', 'common'),
    ('shower-master-01', 'LORE-Asmongold-Shower-Legendary-Review-v1', 'LORE-Asmongold-Shower-Legendary-v2', 'legendary'),
    ('mail-muncher-master-01', 'LORE-Asmongold-Mail-Muncher-Epic-Layout-Review-v4', 'LORE-Asmongold-Mail-Muncher-Epic-v5', 'epic'),
    ('rat-alarm-master-01', 'LORE-Asmongold-Rat-Alarm-Rare-Review-v1', 'LORE-Asmongold-Rat-Alarm-Rare-v2', 'rare'),
]


def file_info(path):
    b = path.read_bytes()
    return {'path': str(path.relative_to(REPO)), 'bytes': len(b),
            'sha256': hashlib.sha256(b).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def without_badge_geometry(root):
    r = copy.deepcopy(root)
    box, label = badge_nodes(r)
    for attr in ['width']:
        box.set(attr, 'BADGE_REVISION')
    for attr in ['x', 'y']:
        label.set(attr, 'BADGE_REVISION')
    return ET.tostring(r)


def main():
    results=[]
    for folder,old_name,new_name,rarity in CARDS:
        p=REPO/'cards/creators/asmongold'/folder
        old_svg=p/f'{old_name}.svg'; old_png=old_svg.with_suffix('.png')
        new_svg=p/f'{new_name}.svg'; new_png=new_svg.with_suffix('.png')
        before=ET.parse(old_svg).getroot(); after=copy.deepcopy(before)
        old_box,_=badge_nodes(before)
        apply_badge_spacing(after,rarity)
        assert without_badge_geometry(before)==without_badge_geometry(after)
        originals=[file_info(old_svg),file_info(old_png)]
        ET.ElementTree(after).write(new_svg,encoding='utf-8',xml_declaration=True)
        with tempfile.TemporaryDirectory(prefix='lore-badge-') as t:
            rendered=Path(t)/'rendered.png'
            subprocess.run(['inkscape',str(new_svg),'--export-type=png',f'--export-filename={rendered}'],env=ENV,check=True,capture_output=True)
            original=Image.open(old_png).convert('RGBA'); generated=Image.open(rendered).convert('RGBA')
            assert original.size==generated.size==(900,1260)
            # Covers old/new border and antialiasing, without touching the counter.
            region=(48,47,int(50+float(old_box.get('width'))+2),98)
            a=np.asarray(original); g=np.asarray(generated)
            outside=np.ones(a.shape[:2],dtype=bool)
            x0,y0,x1,y1=region;outside[y0:y1,x0:x1]=False
            renderer_differences=int(np.any(a[outside]!=g[outside],axis=1).sum())
            if renderer_differences:
                final=original.copy();final.paste(generated.crop(region),region[:2])
            else:
                final=generated
            final.save(new_png)
            b=np.asarray(Image.open(new_png).convert('RGBA'))
            assert np.array_equal(a[outside],b[outside])
            changed=int(np.any(a!=b,axis=2).sum())
            assert changed>0
        assert all(file_info(REPO/f['path'])['sha256']==f['sha256'] for f in originals)
        qa={'status':'APPROVED_BADGE_CHANGE_APPLIED','rarity':rarity,'front_revision':'LORE-FRONT-v4',
            'approval_quote':'agreed, right hand version is approved','approved_by':'Dan Payne','approved_at':'2026-09-13',
            'approval_scope':'Approved right-hand badge spacing applied to the previously approved card; no other changes.',
            'svg_changes':['rarity badge width','rarity label x','rarity label baseline'],
            'embedded_art_and_qr_unchanged':True,'outside_badge_changed_pixels':0,'changed_pixels':changed,
            'badge_region_xyxy':region,'native_renderer_outside_region_differences':renderer_differences,
            'original_files':originals,'current_files':[file_info(new_png),file_info(new_svg)],
            'physical_trim_mm':[63,88],'print_release':False,'source_and_qr_status':'Inherited from the prior approved card; no change.'}
        (p/'badge-v4-approval.json').write_text(json.dumps(qa,indent=2)+'\n')
        results.append(qa)
        print(json.dumps({'card':folder,'outside_badge_changed_pixels':0,'renderer_differences':renderer_differences}),flush=True)
    (MASTER/'qa/approved-cards.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    main()
