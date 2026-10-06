#!/usr/bin/env python3
"""Deterministic HISTROVE display derivatives; reads approved files, writes only output.

python build_web_brand_assets.py --repo ../repo --out ./output
No source artwork, lettering, crown, typography, QR, or print geometry is edited.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
from PIL import Image, ImageDraw, ImageFont, ImageChops, features

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
parser.add_argument('--qr-deps', type=Path, help='Optional existing zxingcpp import directory')
parser.add_argument('--require-qr', action='store_true', help='Fail if final WebP QR decoding cannot be verified')
args=parser.parse_args(); repo=args.repo.resolve(); out=args.out.resolve()
if args.qr_deps: sys.path.insert(0,str(args.qr_deps.resolve()))
try:
 import zxingcpp
except ImportError:
 zxingcpp=None
 if args.require_qr: raise RuntimeError('zxingcpp is required for --require-qr')
web=out/'site/public'; qa=out/'qa'
for directory in [web/'archive',web/'brand',web/'collection',qa]:directory.mkdir(parents=True,exist_ok=True)
L=Image.Resampling.LANCZOS
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((repo/'brand/brand-lock.json').read_text())
assert lock['brand_name']=='HISTROVE' and lock['copy']['master_tagline']=='History Worth Holding'
brand_manifest=json.loads((repo/'brand/assets/asset-manifest.json').read_text())
brand_records={v['path']:v for v in brand_manifest['approved_exports']}
print_manifest=json.loads((repo/'cards/crypto/print-ready/histrove-v1/manifest.json').read_text())
assert len(print_manifest['fronts'])==39
pack_path='packaging/crypto-season-01/histrove-booster-v1'
pack_manifest=json.loads((repo/pack_path/'manifest.json').read_text())
records=[]; cards=[]; sources={}; checks=[]; qr_results=[]

def approved(path, expected_hash):
 p=repo/path
 assert sha(p)==expected_hash, f'Approved source hash mismatch: {path}'
 sources[path]=expected_hash
 return p

def brand(name):
 path='brand/assets/png/'+name
 return approved(path,brand_records[path]['sha256'])

def record(path,role,source,**extra):
 im=Image.open(path) if path.suffix in ['.png','.webp','.ico'] else None
 rec={'path':str(path.relative_to(out)),'public_path':'/'+str(path.relative_to(web)), 'role':role,
      'sha256':sha(path),'bytes':path.stat().st_size,'source':source,**extra}
 if im: rec.update({'dimensions_px':list(im.size),'mode':im.mode})
 records.append(rec);return rec

for entry in print_manifest['fronts']:
 n=entry['number']; src=approved(entry['png']['path'],entry['png']['sha256'])
 im=Image.open(src).convert('RGB');assert im.size==(816,1110)
 trim=(36,36,780,1074)
 derivative=im.crop(trim).resize((600,837),L)
 dst=web/'archive'/f'{n}-histrove-card.webp'
 derivative.save(dst,format='WEBP',lossless=True,quality=75,method=4,exact=True)
 assert ImageChops.difference(derivative,Image.open(dst).convert('RGB')).getbbox() is None
 rec=record(dst,'Current approved HISTROVE card web preview',entry['png']['path'],
   number=n,title=entry['title'],rarity=entry['rarity'],source_sha256=entry['png']['sha256'],
   source_dimensions_px=[816,1110],trim_box_xywh=[36,36,744,1038],crop_box_ltrb=list(trim),
   resize_filter='Pillow LANCZOS',lossless=True,qr_url=entry['qr_url'],
   decoded_pixels_equal_crop_resample=True,source_unchanged=True)
 if zxingcpp:
  payloads=[v.text for v in zxingcpp.read_barcodes(Image.open(dst))]
  qr_pass=payloads==[entry['qr_url']]
  assert qr_pass, f'Final WebP QR decode failed for {n}: {payloads}'
  rec['qr_decoded_payloads']=payloads;rec['qr_output_decode_pass']=qr_pass
  qr_results.append({'path':str(dst.relative_to(out)),'payloads':payloads,'expected':entry['qr_url'],'pass':qr_pass})
 cards.append(rec)

for tone,name in [('white','histrove-logo.png'),('obsidian','histrove-logo-dark.png')]:
 src=brand(f'histrove_compact_{tone}_transparent-2400.png')
 im=Image.open(src).convert('RGBA'); derivative=im.resize((720,354),L)
 dst=web/'brand'/name;derivative.save(dst,optimize=True)
 decoded=Image.open(dst)
 assert ImageChops.difference(derivative,decoded).getbbox() is None
 assert decoded.getextrema()[3][0]==0 and decoded.getextrema()[3][1]==255
 record(dst,'Exact approved compact lockup scaled uniformly, built-in padding retained',str(src.relative_to(repo)),
   source_sha256=sha(src),scale=0.3,alpha_intact=True,alpha_bbox=list(decoded.getchannel('A').getbbox()),
   lettering_regenerated=False,crown_geometry_changed=False)

avatar=brand('histrove_avatar_gold_obsidian-1024.png')
for name,size in [('histrove-icon.png',192),('histrove-apple-icon.png',180),('histrove-favicon.png',32)]:
 dst=web/'brand'/name
 Image.open(avatar).convert('RGBA').resize((size,size),L).save(dst,optimize=True)
 record(dst,'Approved crown avatar scaled uniformly',str(avatar.relative_to(repo)),source_sha256=sha(avatar))
ico=web/'brand/histrove-favicon.ico'
Image.open(avatar).convert('RGBA').resize((64,64),L).save(ico,sizes=[(16,16),(32,32),(48,48),(64,64)])
record(ico,'Approved crown avatar favicon sizes 16, 32, 48 and 64',str(avatar.relative_to(repo)),source_sha256=sha(avatar))
crown_rel='brand/assets/svg/histrove_crown_gold_transparent.svg'
crown_src=approved(crown_rel,brand_records[crown_rel]['sha256'])
crown_dst=web/'brand/histrove-crown.svg';shutil.copyfile(crown_src,crown_dst)
record(crown_dst,'Byte-identical approved gold Rising Strokes crown',crown_rel,source_sha256=sha(crown_src),crown_geometry_changed=False)

pack_rel=pack_path+'/HISTROVE-Crypto-S01-Booster-Review-v1-300dpi.png'
pack_expected=next(x['sha256'] for x in pack_manifest['files'] if x['name'].endswith('-300dpi.png'))
pack_src=approved(pack_rel,pack_expected)
im=Image.open(pack_src).convert('RGB');assert im.size==(2032,1560)
# Source PDF's actual pt coordinates; fitz rasterizes at 300/72 px/pt.
fold_left,fold_right=144.57130432128906,342.9971008300781
safe_top,safe_bottom=37,337
pack_crop=tuple(round(v*300/72) for v in [fold_left,safe_top,fold_right,safe_bottom])
assert pack_crop==(602,154,1429,1404)
trimmed=im.crop(pack_crop);pack_dims=(800,round(trimmed.height*800/trimmed.width))
assert pack_dims==(800,1209)
pack_derivative=trimmed.resize(pack_dims,L)
pack_dst=web/'collection/histrove-booster-front.webp'
pack_derivative.save(pack_dst,format='WEBP',lossless=True,quality=75,method=4,exact=True)
assert ImageChops.difference(pack_derivative,Image.open(pack_dst).convert('RGB')).getbbox() is None
pack_record=record(pack_dst,'Approved clean front face, excluding bleed and blank horizontal heat-seal strips',pack_rel,
 source_sha256=sha(pack_src),crop_box_ltrb=list(pack_crop),crop_box_pt=[fold_left,safe_top,fold_right,safe_bottom],
 source_dimensions_px=list(im.size),lossless=True,decoded_pixels_equal_crop_resample=True,
 note='Flat digital front-face preview, not a physical sample. Template fold width retained; no QR on front.',
 printer_source_unchanged=True,physical_sample_verified=False)

# Calm dark/gold composition with approved full identity and two complete current cards.
# No new lettering: the full primary logo includes the exact approved outlined tagline.
social=Image.new('RGB',(1200,630),'#0B0B0B');d=ImageDraw.Draw(social)
d.rectangle((716,0,1199,629),fill='#121211')
d.line((715,48,715,582),fill='#514624',width=1)
d.line((81,553,651,553),fill='#D4AF37',width=2)
primary=brand('histrove_primary_white_transparent-2400.png')
logo=Image.open(primary).convert('RGBA').resize((672,403),L)
social.paste(logo,(20,98),logo)
# Use unrotated, full trimmed card previews; neither borders nor QR are cropped.
for number,xy,size in [('006',(744,178),(219,306)),('001',(904,108),(260,363))]:
 card=Image.open(web/'archive'/f'{number}-histrove-card.webp').convert('RGB').resize(size,L)
 social.paste(card,xy)
social_dst=web/'brand/histrove-social.png';social.save(social_dst,optimize=True)
record(social_dst,'Open Graph 1200x630: approved primary identity and current approved card artwork',
 [str(primary.relative_to(repo)),cards[0]['source'],cards[5]['source']],
 tagline='History Worth Holding',new_lettering=False,ai_generated=False,
 composition='Approved primary lockup on obsidian left; two unrotated complete approved cards on a charcoal right panel; fine gold rule.')

# Readable visual QA sheets. QA annotations never appear on website assets.
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(font_path,16);small=ImageFont.truetype(font_path,13);big=ImageFont.truetype(font_path,24)
cols,cell_w,cell_h=7,190,296
sheet=Image.new('RGB',(cols*cell_w+32,6*cell_h+76),'#171717');draw=ImageDraw.Draw(sheet)
draw.text((20,17),'HISTROVE / ALL 39 FINISHED-CUT WEB CARDS',font=big,fill='#D4AF37')
for i,rec in enumerate(cards):
 card=Image.open(out/rec['path']).resize((170,237),L)
 x=16+i%cols*cell_w;y=66+i//cols*cell_h
 sheet.paste(card,(x,y));draw.text((x,y+242),f"{rec['number']} / {rec['rarity']}",font=small,fill='#F5F2EB')
 draw.text((x,y+260),rec['title'][:22],font=small,fill='#C0BEB6')
sheet.save(qa/'cards-contact-sheet.jpg',quality=94,subsampling=0)

# Selected full previews and exact crop/resample equality with logo/QR enlarged.
samples=['001','032','039'];sheet=Image.new('RGB',(1440,1230),'#171717');draw=ImageDraw.Draw(sheet)
draw.text((24,18),'TRIM / BORDER / LOGO / QR QA — source hash and decoded pixels verified',font=big,fill='#D4AF37')
for j,n in enumerate(samples):
 card=Image.open(web/'archive'/f'{n}-histrove-card.webp')
 x=24+j*472
 sheet.paste(card.resize((420,586),L),(x,62))
 draw.text((x,663),f'{n}: 600 × 837 / lossless',font=font,fill='#F5F2EB')
 # Magnified unchanged image regions, nearest-neighbour to show encoded pixels.
 logo=card.crop((400,42,548,120));sheet.paste(logo.resize((370,195),Image.Resampling.NEAREST),(x,700))
 qr=card.crop((410,638,550,782));sheet.paste(qr.resize((280,288),Image.Resampling.NEAREST),(x,916))
sheet.save(qa/'card-detail-qa.jpg',quality=96,subsampling=0)

sheet=Image.new('RGB',(1480,1160),'#1A1A1A');draw=ImageDraw.Draw(sheet)
draw.text((28,20),'HISTROVE / APPROVED BOOSTER FRONT-FACE CROP',font=big,fill='#D4AF37')
source_preview=im.resize((914,702),L);sd=ImageDraw.Draw(source_preview)
rect=tuple(round(v*914/im.width) for v in pack_crop);sd.rectangle(rect,outline='#00E9C4',width=3)
sheet.paste(source_preview,(25,86));sheet.paste(pack_derivative.resize((460,695),L),(978,86))
lines=[
 'Source: 2032 × 1560 pixels / approved clean 300 DPI PNG',
 'Green rectangle: x602–1429, y154–1404 (827 × 1250 pixels)',
 'Template: actual front folds x144.5713–342.9971 pt; inner heat-seal y37–337 pt',
 'Website face: 800 × 1209 pixels / lossless WebP',
 'Only exact crop and LANCZOS downsample; source bytes unchanged',
 'Retains approved HISTROVE mark, History Worth Holding, artwork, Crypto / Season 01 and 10 cards',
 'No printer guides, top/bottom blank seal strips or bleed. Not a physical sample photograph.'
]
for i,line in enumerate(lines):draw.text((28,823+i*38),line,font=font,fill='#F5F2EB')
sheet.save(qa/'booster-crop-qa.jpg',quality=94,subsampling=0)

sheet=Image.new('RGB',(1200,990),'#1A1A1A');draw=ImageDraw.Draw(sheet)
sheet.paste(social,(0,0));draw.rectangle((0,646,599,989),fill='#0B0B0B');draw.rectangle((600,646,1199,989),fill='#F5F2EB')
for name,x in [('histrove-logo.png',0),('histrove-logo-dark.png',600)]:
 logo=Image.open(web/'brand'/name).resize((600,295),L);sheet.paste(logo,(x,665),logo)
sheet.save(qa/'identity-and-social-qa.jpg',quality=96,subsampling=0)

if qr_results: (qa/'qr-decode-results.json').write_text(json.dumps(qr_results,indent=2)+'\n')
for path,expected in sources.items():assert sha(repo/path)==expected
manifest={
 'revision':'HISTROVE-WEB-DERIVATIVES-v1.0','date':'2026-10-06',
 'scope':'Display-only deterministic derivatives of approved identity, print cards and booster. No publication or source edits.',
 'brand_lock_revision':lock['revision'],'master_tagline':lock['copy']['master_tagline'],
 'source_verification':'All read master PNG/SVG SHA-256 values match their approved manifests; rechecked unchanged after build.',
 'pillow_version':Image.__version__,'webp_version':features.version_module('webp'),
 'resampling':'LANCZOS; uniform dimensions rounded to closest integer output pixel',
 'webp_encoding':{'lossless':True,'quality':75,'method':4,'exact':True},
 'card_count':len(cards),'all_39_card_sources_hash_verified':True,
 'all_39_web_cards_exactly_equal_prescribed_crop_resample':True,
 'card_trim_box_xywh':[36,36,744,1038],'card_output_px':[600,837],
 'booster':pack_record,'sources':[{'path':k,'sha256':v} for k,v in sorted(sources.items())],
 'files':records,
 'qr_verification':{'decoder':'zxing-cpp' if zxingcpp else None,'final_webp_count_tested':len(qr_results),'all_39_final_webp_decode_pass':len(qr_results)==39 and all(v['pass'] for v in qr_results),'results':'qa/qr-decode-results.json' if qr_results else None},
 'qa':[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted(qa.glob('*'))],
 'limitations':['Website-only previews; approved print masters remain unchanged.','No manufacturing, trademark or physical sample approval inferred.','Flat RGB gold; no simulated foil.']
}
(out/'web-brand-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'output-map.json').write_text(json.dumps({x['public_path']:{'path':x['path'],'sha256':x['sha256'],'dimensions_px':x.get('dimensions_px')} for x in records},indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f"{sha(p)}  {p.relative_to(out)}\n" for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
print(json.dumps({'output':str(out),'cards':len(cards),'total_public_assets':len(records),'logo_px':[720,354],'booster_px':list(pack_dims),'social_px':[1200,630],'all_source_hashes_match':True,'all_card_and_booster_pixels_match':True},indent=2))
