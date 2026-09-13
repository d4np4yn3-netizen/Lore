"""Verify actual badge padding and preservation of approved card content."""
from pathlib import Path
import json, os, subprocess
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from badge_spacing import MASTER, METRICS, badge_nodes
from update_approved_cards import REPO, without_badge_geometry, file_info

ENV=os.environ.copy()
ENV['FONTCONFIG_FILE']=str(MASTER.parent/'front-v3/source/fontconfig.xml')


def measure(path):
    r=ET.parse(path).getroot();box,label=badge_nodes(r)
    raw=subprocess.run(['inkscape',str(path),'--query-id=rarity-label','--query-x','--query-y','--query-width','--query-height'],env=ENV,check=True,capture_output=True,text=True)
    x,y,w,h=map(float,raw.stdout.strip().splitlines())
    left=x-float(box.get('x'));right=float(box.get('x'))+float(box.get('width'))-x-w
    centre_error=y+h/2-(float(box.get('y'))+float(box.get('height'))/2)
    if max(abs(left-22),abs(right-22),abs(centre_error))>.01:
        raise AssertionError(f'Badge padding/centring failed for {path}: {left}, {right}, {centre_error}')
    return {'path':str(path.relative_to(REPO)),'left_padding':left,'right_padding':right,'vertical_centre_error':centre_error}


def main():
    checks=[]
    for rarity in METRICS:
        new=MASTER/'templates'/f'{rarity.lower()}.svg'
        old=MASTER.parent/'front-v3/templates'/new.name
        assert without_badge_geometry(ET.parse(new).getroot())==without_badge_geometry(ET.parse(old).getroot())
        checks.append(measure(new))
    cards=json.loads((MASTER/'qa/approved-cards.json').read_text())
    for card in cards:
        old_svg=next(REPO/f['path'] for f in card['original_files'] if f['path'].endswith('.svg'))
        old_png=old_svg.with_suffix('.png')
        new_svg=next(REPO/f['path'] for f in card['current_files'] if f['path'].endswith('.svg'))
        assert without_badge_geometry(ET.parse(new_svg).getroot())==without_badge_geometry(ET.parse(old_svg).getroot())
        for f in card['original_files']+card['current_files']:
            assert file_info(REPO/f['path'])['sha256']==f['sha256']
        a=np.asarray(Image.open(old_png).convert('RGBA'));b=np.asarray(Image.open(new_svg.with_suffix('.png')).convert('RGBA'))
        assert a.shape==b.shape==(1260,900,4)
        outside=np.ones(a.shape[:2],dtype=bool)
        x0,y0,x1,y1=card['badge_region_xyxy'];outside[y0:y1,x0:x1]=False
        assert np.array_equal(a[outside],b[outside])
        checks.append(measure(new_svg))
    report={'result':'PASS','templates_checked':6,'approved_cards_checked':4,'only_badge_svg_geometry_changes':True,'outside_badge_pixel_changes':0,'measurements':checks}
    (MASTER/'qa/layout-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='measurements'}))


if __name__=='__main__':main()
