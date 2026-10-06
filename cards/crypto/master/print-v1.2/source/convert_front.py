"""Apply Dan's 6 October 2026 approved 001 framing to an existing print-v1 front.

This edits vector layout only. Embedded illustration bytes, word/brand/QR paths,
typographic styling, and any deliberate artwork translation remain unchanged.
Use render_print_card.py for new cards; use this converter for historical fronts.
"""
from pathlib import Path
import argparse, copy, xml.etree.ElementTree as ET

SVG='http://www.w3.org/2000/svg'
XLINK='http://www.w3.org/1999/xlink'
ET.register_namespace('',SVG); ET.register_namespace('xlink',XLINK)
SCALE=672/886
OFFSET=(816-900*SCALE)/2
HEIGHT_DELTA=27.625
LAYOUT_HEIGHT=1287.625
LOWER_IDS={'creator-name','title-line-1','title-line-2','moment-context','qr-caption','moment-qr','set-number'}
def ns(n):return '{'+SVG+'}'+n
def fmt(n):return f'{n:.9f}'.rstrip('0').rstrip('.')

def convert(root):
    root=copy.deepcopy(root)
    g=root.find(".//*[@id='locked-crypto-front']")
    if g is None or len(g)!=1:raise ValueError('Expected the existing locked crypto print composition')
    n=g[0];old=copy.deepcopy(n)
    if n.get('viewBox')!='0 0 900 1260' or len(n)!=19:raise ValueError('Unexpected source layout; inspect instead of guessing')
    assert n[5].get('height')=='1240' and n[4].get('y')=='879'
    assert n[17].get('d')=='M58 1196H842'
    g.set('transform',f'translate({fmt(OFFSET)} {fmt(OFFSET)}) scale({SCALE:.12f})')
    n.set('height',fmt(LAYOUT_HEIGHT));n.set('viewBox',f'0 0 900 {fmt(LAYOUT_HEIGHT)}')
    n[1].set('height',fmt(LAYOUT_HEIGHT))
    n.find(".//*[@id='clip']")[0].set('height',fmt(1232+HEIGHT_DELTA))
    art=n.find(".//*[@id='card-illustration']")
    art.set('height',fmt(1232+HEIGHT_DELTA))
    assert art.get('preserveAspectRatio')=='xMidYMid slice'
    n[4].set('y',fmt(879+HEIGHT_DELTA));n[5].set('height',fmt(1240+HEIGHT_DELTA))
    n[6].set('d','M32 160V55Q32 32 55 32H225 M675 32H845Q868 32 868 55V160 '
        f'M32 {fmt(1095+HEIGHT_DELTA)}V{fmt(1205+HEIGHT_DELTA)}Q32 {fmt(1228+HEIGHT_DELTA)} 55 {fmt(1228+HEIGHT_DELTA)}H225 '
        f'M675 {fmt(1228+HEIGHT_DELTA)}H845Q868 {fmt(1228+HEIGHT_DELTA)} 868 {fmt(1205+HEIGHT_DELTA)}V{fmt(1095+HEIGHT_DELTA)}')
    for key in LOWER_IDS:
        a=n.find(f".//*[@id='{key}']");a.set('y',fmt(float(a.get('y'))+HEIGHT_DELTA))
    n[17].set('d',f'M58 {fmt(1196+HEIGHT_DELTA)}H842')
    root.set('width','69.088mm');root.set('height','93.98mm')
    metadata=root.find(ns('metadata'))
    if metadata is None:metadata=ET.SubElement(root,ns('metadata'))
    metadata.text=('LORE-CRYPTO-PRINT-v1.2 | Dan approved 001 framing and collection rollout on 2026-10-06. '
        '816x1110 @300 DPI; cut 744x1038; safe 684x981. Even 3.080108 mm straight-edge frame margins. '
        'Artwork proportional centre fill; original bytes and existing translations preserved. '
        'Text/logo/QR sizes match reviewed 001. Physical printer/sample acceptance is separate.')
    # Strong invariants around the elements that are not being redesigned.
    assert ET.tostring(n[10])==ET.tostring(old[10]),'Logo changed'
    old_art=copy.deepcopy(old.find(".//*[@id='card-illustration']"));old_art.set('height',fmt(1232+HEIGHT_DELTA))
    assert ET.tostring(art)==ET.tostring(old_art),'Artwork data, placement or proportions changed unexpectedly'
    for a in old.findall(ns('text'))+[old.find(".//*[@id='moment-qr']")]:
        expected=copy.deepcopy(a)
        if a.get('id') in LOWER_IDS:expected.set('y',fmt(float(a.get('y'))+HEIGHT_DELTA))
        assert ET.tostring(n.find(f".//*[@id='{a.get('id')}']"))==ET.tostring(expected),a.get('id')
    return root

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(convert(ET.parse(a.source).getroot())).write(a.output,encoding='utf-8',xml_declaration=True)
