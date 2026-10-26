from pathlib import Path
import argparse, base64, copy, hashlib, json, os, subprocess, sys, xml.etree.ElementTree as E
from PIL import Image, ImageDraw, ImageFont

ROOT=Path('/workspace/scratch/58d5f7ed8606')
P=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'card069-proof/deps'))
import qrcode, zxingcpp
S='http://www.w3.org/2000/svg'; X='http://www.w3.org/1999/xlink'
E.register_namespace('',S); E.register_namespace('xlink',X)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    a=argparse.ArgumentParser(); a.add_argument('--art',required=True); args=a.parse_args()
    art=Path(args.art).resolve()
    assert art.is_file() and Image.open(art).size==(1060,1484)
    original_sha=sha(art)
    template=P/'sources/common.svg'; t=template.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(t)).encode()+b'\0'+t).hexdigest()=='fe9537de4a82fee22b92c113dd9d7d708c451512'
    root=E.fromstring(t); reference=copy.deepcopy(root)
    ids={e.get('id'):e for e in root.iter() if e.get('id')}
    copy_fields={'creator-name':'YEARN FINANCE','title-line-1':'YFI','title-line-2':'','moment-context':'NO RESERVED SEAT.','moment-number':'17 JUL 2020','set-number':'CRYPTO • SEASON 01 • 058/100'}
    for key,val in copy_fields.items(): ids[key].text=val
    ids['card-illustration'].set('{'+X+'}href','data:image/png;base64,'+base64.b64encode(art.read_bytes()).decode())
    route='https://www.histrove.co.uk/crypto/058/'
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=8)
    qr.add_data(route); qr.make(fit=True); matrix=qr.get_matrix(); size=len(matrix)
    node=ids['moment-qr'];node[:]=[];node.set('viewBox',f'0 0 {size} {size}')
    E.SubElement(node,'{'+S+'}rect',{'width':str(size),'height':str(size),'fill':'#FFFFFF'})
    d=' '.join(f'M{x} {y}h1v1h-1z' for y,row in enumerate(matrix) for x,v in enumerate(row) if v)
    E.SubElement(node,'{'+S+'}path',{'d':d,'fill':'#000000'})
    # Verify exact canonical structure/styles outside the designated content slots.
    audit=copy.deepcopy(root); audit_ids={e.get('id'):e for e in audit.iter() if e.get('id')}; refids={e.get('id'):e for e in reference.iter() if e.get('id')}
    for key in list(copy_fields)+['card-illustration','moment-qr']:
        target=audit_ids[key]; source=refids[key];target.attrib.clear();target.attrib.update(source.attrib);target.text=source.text;target[:]=copy.deepcopy(list(source))
    assert E.tostring(audit)==E.tostring(reference),'Unexpected template modification'
    svg=P/'HISTROVE-Crypto-058-Empty-Throne-Front-Proof-v6.svg'
    E.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
    env=os.environ.copy();env['FONTCONFIG_FILE']=str(ROOT/'card077-release/cards/master/front-v3/source/fontconfig.xml')
    png=svg.with_suffix('.png')
    subprocess.run(['inkscape',str(svg),'--export-width=816','--export-height=1110',f'--export-filename={png}'],env=env,check=True,capture_output=True)
    im=Image.open(png).convert('RGB');assert im.size==(816,1110); im.save(png,dpi=(300,300))
    # Exact finished-cut preview: 36px bleed removed, no extra art crop.
    review=im.crop((36,36,780,1074));rp=P/'HISTROVE-Crypto-058-Empty-Throne-Card-Review-v6.png';review.save(rp,dpi=(300,300))
    # Internal viewing copy matching the existing website thumbnail convention.
    web=im.crop((72,72,744,1038)).convert('RGBA');mask=Image.new('L',web.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,671,965),radius=21,fill=255);web.putalpha(mask)
    web=web.resize((600,863),Image.Resampling.LANCZOS);web.save(P/'inspection-card-display.png')
    decodes={label:sorted(set(x.text for x in zxingcpp.read_barcodes(img))) for label,img in [('native',im),('review',review),('display',web.convert('RGB'))]}
    assert all(v==[route] for v in decodes.values()),decodes
    embedded=base64.b64decode(ids['card-illustration'].get('{'+X+'}href').split(',',1)[1])
    assert hashlib.sha256(embedded).hexdigest()==original_sha==sha(art)
    qa={'card':'058','status':'REVIEW PROOF ONLY — not approved/published/physical-print accepted','art_path':str(art),'art_sha256':original_sha,'raw_dimensions':[1060,1484],'raw_bytes_unchanged_and_exactly_embedded':True,'template_git_blob':'fe9537de4a82fee22b92c113dd9d7d708c451512','template_sha256':sha(template),'template_structural_check':'Exact outside content slots','native_dimensions':[816,1110],'native_dpi':Image.open(png).info.get('dpi'),'trim_box_xywh':[36,36,744,1038],'review_dimensions':[744,1038],'safe_box_xywh':[66,64.5,684,981],'rarity':'Common — current master allocation proposal','copy':copy_fields,'tagline_status':'Proposed editorial wording, derived from brief no-reserved-founder-chair metaphor; not a quote or previously approved','qr_route':route,'qr_status':'Correct intended numbered collection route; 058 is unpublished and its route is not yet live','qr_decodes':decodes,'art_placement':{k:v for k,v in ids['card-illustration'].attrib.items() if 'href' not in k},'art_framing':'Unmodified standard xMidYMid slice. No additional zoom, translation, distortion or pixel editing.','files':{p.name:{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in [rp,png,svg]}}
    (P/'QA-v6.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))

if __name__=='__main__':main()
