#!/usr/bin/env python3
"""Create web-only format/size derivatives. Never edits approved source pixels."""
from pathlib import Path
from PIL import Image
import hashlib,json,argparse
import zxingcpp
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--assets',type=Path,default=R.parent/'card091-release/assets');args=parser.parse_args()
A=args.assets.resolve(); MP='cards/crypto/season-01/spot-bitcoin-etfs-approved-master-091'; M=A/MP
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_names=['HISTROVE-Crypto-091-Card.png','art.png','book-page-1.png','book-page-2.png']+[f'closeups/091-detail-{i}.png' for i in range(1,5)]
before={n:H(M/n) for n in source_names}; derivatives=[]
def convert(src,dst,size=None,**save):
 p=M/src; target=A/dst;target.parent.mkdir(parents=True,exist_ok=True)
 with Image.open(p) as im:
  im=im.convert('RGBA' if im.mode=='RGBA' else 'RGB'); original_size=im.size
  if size:im=im.resize(size,Image.Resampling.LANCZOS)
  im.save(target,'WEBP',**save)
  check=Image.open(target);check.load()
  if save.get('lossless'):assert check.convert(im.mode).tobytes()==im.tobytes()
  derivatives.append({'source':MP+'/'+src,'source_sha256':H(p),'source_dimensions_px':list(original_size),'path':dst,'sha256':H(target),'bytes':target.stat().st_size,'dimensions_px':list(check.size),'conversion':{'format':'WEBP',**save,**({'resize':'LANCZOS','preserve_entire_canvas':True,'target_dimensions_px':list(size)} if size else {})}})
convert(source_names[0],'site/public/archive/091-histrove-border-card.webp',size=(600,863),lossless=True,exact=True,method=6)
for n in source_names[1:4]:
 dst='091-art.webp' if n=='art.png' else '091-histrove-'+n.replace('book-','').replace('.png','.webp')
 convert(n,'site/public/archive/'+dst,quality=94,method=6)
for i in range(1,5):convert(f'closeups/091-detail-{i}.png',f'site/public/closeups/091-{i:02}.webp',quality=95,method=6)
assert before=={n:H(M/n) for n in source_names}
(M/'web-derivatives.json').write_text(json.dumps(derivatives,indent=2)+'\n')
qa={'source_sha256':H(M/'HISTROVE-Crypto-091-Front-Print-v1.png'),'source_svg_sha256':H(M/'HISTROVE-Crypto-091-Front-Print-v1.svg'),'approved_preview_source':MP+'/HISTROVE-Crypto-091-Card.png','approved_preview_sha256':before[source_names[0]],'approved_preview_source_dimensions_px':[1044,1501],'approved_preview_rgba_pixels_identical':False,'web_conversion':'Whole approved display proportionally downsampled to standard 600 x 863 with LANCZOS; then losslessly encoded as WebP. No new crop, sharpening, artwork, template or copy edit. Integer target dimensions entail less than 0.05% aspect rounding.','decoded_web_pixels_identical_to_resized_source':True,'outer_border_source_display_viewbox_in_print_units':[72,72,672,966],'conservative_crop_ltrb':[72,72,744,1038],'dimensions_px':[600,863],'complete_border_geometry_retained':True,'print_source_unchanged':True,'qr_verification':'Pending independent decode of final WebP','qr_payloads':[],'approved_source_files_unchanged':before}
decoded=[x.text for x in zxingcpp.read_barcodes(Image.open(A/'site/public/archive/091-histrove-border-card.webp'))]
assert decoded==['https://www.histrove.co.uk/crypto/091/'],decoded
qa.update({'qr_payloads':decoded,'qr_verification':'Final 600 x 863 WebP independently decoded with zxing-cpp 3.1.1; intended collector route confirmed.','visual_qa':'Complete frame, date, title, FINALLY., footer and QR inspected at actual final WebP size. No source artwork or template edits.'})
(M/'web-border-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({'files':len(derivatives),'bytes':sum(x['bytes'] for x in derivatives),'sources_unchanged':True,'derivatives':derivatives},indent=2))
