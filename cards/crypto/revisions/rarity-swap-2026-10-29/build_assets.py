from pathlib import Path
import json,hashlib,shutil,subprocess,os
import fitz
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
R=Path(__file__).resolve().parent; Q=R.parents[1]/'rarity-swap-review'; A=R/'assets'; REV='rarity-swap-2026-10-29'; ROOT='cards/crypto/revisions/'+REV
BASE='8456f7f5216e7d391e10e0e48c1515be497f35af'
D={'064':('everydays-at-auction','everydays-at-auction-master-064','common','Everydays-at-Auction','064-everydays-at-auction.md'), '071':('bitcoin-becomes-legal-tender','bitcoin-becomes-legal-tender-master-071','epic','Legal-Tender','071-bitcoin-becomes-legal-tender.md'), '093':('the-fourth-halving','golden-river-fourth-halving-master-093','legendary','The-Fourth-Halving','093-fourth-halving-golden-river.md')}
def write(p,b):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def dump(p,j):write(p,(json.dumps(j,indent=2,ensure_ascii=False)+'\n').encode())
def copy(src,dst):write(A/dst,src.read_bytes());return dst
def meta(p):b=p.read_bytes();return {'path':str(p.relative_to(A)),'local_path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
validation=json.loads((Q/'review-output/validation.json').read_text()); cards={}
for n,(slug,folder,tier,title,chapter) in D.items():
 src=Q/'cards/crypto/season-01'/folder; dest=ROOT+'/'+n; f={}
 assert hashlib.sha256((src/'art.png').read_bytes()).hexdigest()==validation[n]['art_sha256']
 for ext in ['png','svg']:f[ext]=copy((R.parent/f'font-diagnostic/{n}-corrected.png') if ext=='png' else (Q/f'review-output/{n}-{tier}-review.svg'),f'{dest}/HISTROVE-Crypto-{n}-{tier.title()}-Front.{ext}')
 f['web']=copy(R.parent/f'font-diagnostic/{n}-corrected.webp',f'site/public/archive/{n}-{REV}-card.webp')
 f['book']=copy(Q/f'review-output/{n}-HISTROVE-{n}-{title}-Book.pdf',f'book/crypto-season-01/histrove-v1/{n}-{REV}-histrove-v1.pdf')
 f['spread']=copy(Q/f'review-output/{n}-HISTROVE-{n}-{title}-Book-Spread.png',f'{dest}/HISTROVE-{n}-{title}-Book-Spread.png')
 f['chapter']=copy(Q/'book/crypto-season-01/histrove-v1/chapters'/chapter,f'book/crypto-season-01/histrove-v1/chapters/{n}-{REV}.md')
 for name in ['card-data.json','build_book.py','authoring-content.json','sources.json','source-verification.json']:
  if (src/name).exists():copy(src/name,f'{dest}/source/{name}')
 copy(Q/f'review-output/{n}-book-qa.json',f'{dest}/source/historical-review-book-qa.json')
 copy(src/'source/fonts/DejaVuSans.ttf',f'{dest}/source/fonts/DejaVuSans.ttf');copy(src/'source/fonts/DejaVuSans-Bold.ttf',f'{dest}/source/fonts/DejaVuSans-Bold.ttf')
 f['pages']=[]
 pdf=fitz.open(A/f['book']);assert len(pdf)==2
 # Preserve existing book preview dimensions for each card.
 size=(893,1263) if n=='093' else (778,1100)
 for i in range(2):
  page=pdf[i];pix=page.get_pixmap(matrix=fitz.Matrix(size[0]/page.rect.width,size[1]/page.rect.height),alpha=False)
  im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples).resize(size,Image.Resampling.LANCZOS)
  path=f'site/public/archive/{n}-{REV}-page-{i+1}.webp';(A/path).parent.mkdir(parents=True,exist_ok=True);im.save(A/path,'WEBP',quality=94);f['pages'].append(path)
 f['page_dimensions']=size
 if n!='093':
  for ext in ['png','svg']:f['print_'+ext]=copy(A/f[ext],f'cards/crypto/print-ready/histrove-v1/fronts/{ext}/HISTROVE-Crypto-{n}-Front-Print-{REV}.{ext}')
  out=A/f'cards/crypto/print-ready/histrove-v1/fronts/pdf/HISTROVE-Crypto-{n}-Front-Print-{REV}.pdf';out.parent.mkdir(parents=True,exist_ok=True)
  tmp=R/f'{n}-outlined.pdf';subprocess.run(['inkscape',str(A/f['svg']),'--export-type=pdf','--export-text-to-path',f'--export-filename={tmp}'],env=dict(os.environ,FONTCONFIG_FILE=str(R.parents[1]/'card078-release/cards/master/front-v3/source/fontconfig.xml'),XDG_CACHE_HOME=str(R/'font-cache')),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  reader=PdfReader(tmp);page=reader.pages[0];page.mediabox=RectangleObject([0,0,195.84,266.4]);page.bleedbox=RectangleObject([0,0,195.84,266.4]);page.trimbox=RectangleObject([8.64,8.64,187.2,257.76]);page.artbox=RectangleObject([15.84,15.48,180,250.92]);w=PdfWriter();w.add_page(page)
  with out.open('wb') as fp:w.write(fp)
  f['print_pdf']=str(out.relative_to(A));tmp.unlink()
 f.update(slug=slug,rarity=tier,revision_root=dest,original_art=validation[n]['art_sha256'],print_pending=n=='093')
 cards[n]=f
approval={'status':'PUBLICATION_AUTHORIZED','approved_at':'2026-10-29T07:26:18Z','scope':'Publish approved 093 Common to Legendary, 071 Legendary to Epic, 064 Epic to Common rarity swap to existing d4np4yn3-netizen/Lore and Histrove website. Artwork, QR, footer and all other 97 cards unchanged; narrow 015 shared-frame source-note correction only.','physical_print_acceptance':False,'093_print_qa':'PENDING','history':'Review source flags remain historical and are superseded only for publication authorization by this record.'}
dump(A/ROOT/'approval.json',approval)
for name in ['validation.json','final-qa.json','README.md','build_rarity_review.py','validate_rarity_review.py']:copy(Q/'review-output'/name,ROOT+'/source-review/'+name)
copy(Path(__file__),ROOT+'/build_assets.py')
old={x['path'] for x in json.loads((R/'base-tree.json').read_text())['tree']};files=[meta(p) for p in sorted(A.rglob('*')) if p.is_file()];assert not old.intersection(x['path'] for x in files)
dump(R/'ASSET-UPLOAD-MANIFEST.json',{'base_commit':BASE,'asset_root':str(A),'revision':REV,'cards':cards,'files':files,'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'status':'LOCAL_PREPARED_PENDING_FINAL_QA'})
print(len(files),sum(x['bytes'] for x in files))
