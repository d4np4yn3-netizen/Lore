from pathlib import Path
import subprocess,json,hashlib,re,fitz
from PIL import Image
import zxingcpp
r=Path('/workspace/scratch/58d5f7ed8606/rarity-swap-review');q=r/'review-output'
for p in q.glob('015-*'):p.unlink()
js="const fs=require('fs');let s=fs.readFileSync(process.argv[1],'utf8').replace(/^import .*;\\n/gm,'').replace(/\\.\\.\\.chapter\\d+,?/g,'').replace('export const cards =','const cards =').split('export const getCard')[0];console.log(JSON.stringify(Function(s+'return cards;')()));"
def parse(s):
 p=Path('/tmp/data-review.js');p.write_text(s);return json.loads(subprocess.check_output(['node','-e',js,str(p)]))
old=parse(subprocess.check_output(['git','show','HEAD:site/app/cards/data.js'],cwd=r).decode());new=parse((r/'site/app/cards/data.js').read_text())
from collections import Counter
assert len(old)==len(new)==100
changes=[]
for a,b in zip(old,new):
 if a!=b:
  assert a['number'][:3] in ['064','071','093'];assert {k for k in a if a[k]!=b[k]}=={'rarity'};changes.append([a['number'],a['rarity'],b['rarity']])
assert Counter(a['rarity'] for a in old)==Counter(a['rarity'] for a in new)
qa=json.loads((q/'validation.json').read_text());books={}
for n in ['064','071','093']:
 b=r/Path(qa[n]['source_svg']).parent
 original=next(b.glob('*Book.pdf'));edited=next(q.glob(n+'-*Book.pdf'))
 a=fitz.open(original);c=fitz.open(edited);assert len(a)==len(c)==2
 assert a[0].get_pixmap().samples==c[0].get_pixmap().samples,n
 ta=a[1].get_text();tc=c[1].get_text();assert ta.replace(qa[n]['old'].upper(),qa[n]['new'].upper())==tc,n
 books[n]={'page_count':2,'full_art_page_pixel_identical':True,'text_difference_only_rarity':True,'old':qa[n]['old'],'new':qa[n]['new'],'physical_print_acceptance':False}
 im=Image.open(q/f"{n}-{qa[n]['new']}-card.webp");assert [x.text for x in zxingcpp.read_barcodes(im.convert('RGB'))]==qa[n]['qr_payloads']
 p=q/(n+'-book-qa.json');j=json.loads(p.read_text());j['publication_authorized']=False;j['book_approval_status']='LOCAL_RARITY_REVIEW_ONLY';j['visual_review']='Reviewed 29 October 2026; layout retained; no clipping observed';p.write_text(json.dumps(j,indent=2)+'\n')
report={'base_commit':'8456f7f5216e7d391e10e0e48c1515be497f35af','changed_cards':changes,'before_counts':dict(Counter(a['rarity'] for a in old)),'after_counts':dict(Counter(a['rarity'] for a in new)),'other_97_catalogue_rows_identical':True,'015_and_046_unchanged':True,'book_checks':books,'publication':'NOT_PUBLISHED_LOCAL_REVIEW_ONLY','integration_pending':['Wire versioned frame, book and web image files into active media/print manifests and immutable asset origins as part of an authorised publication release.','Run full site build and package/archive checks after integration.','Physical print QA remains pending; no foil mask or foil test has been produced.']}
(q/'final-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
