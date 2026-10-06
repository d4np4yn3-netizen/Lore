#!/usr/bin/env python3
"""Make additive HISTROVE book derivatives. Preserve originals, art and factual copy.
Requires PyMuPDF, ReportLab, Pillow, NumPy, and Poppler pdftoppm.
"""
import json,re,hashlib,io,math,subprocess,shutil,argparse
from pathlib import Path
import fitz,numpy as np
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
import html
B=Path(__file__).parent
parser=argparse.ArgumentParser();parser.add_argument('--original-root',type=Path,default=B/'originals');parser.add_argument('--site-root',type=Path,default=B.parent/'repo/site');parser.add_argument('--font-root',type=Path,default=B.parents[1]/'histrove-rollout/repo/cards/master/front-v3/source/fonts');parser.add_argument('--output-root',type=Path,default=B/'release');parser.add_argument('--audit',type=Path,default=B/'layout-audit.json');args=parser.parse_args()
O=args.original_root;S=args.output_root;SOURCE_COMMIT='c887b8ee293e36a0f0c7044a780af77f7b51efa4';A=json.loads(args.audit.read_text());M=json.loads((B/'original-media.json' if (B/'original-media.json').exists() else O/'site/app/cards/media.json').read_text());index=json.loads((args.site_root/'media/index.json').read_text());index={x['path']:x for x in index['assets']};pack_cache={}
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(args.font_root/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rich(s):
 s=html.escape(s);s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<link href="\2" color="#785910">\1</link>',s);s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s);return re.sub(r'\*(.*?)\*',r'<i>\1</i>',s)
def norm(s):return re.sub(r'\s+',' ',s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')).strip()
def plain(s):return norm(re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s).replace('**','').replace('*',''))
def preview_bytes(path):
 e=index[path.lstrip('/')];pack=e['pack']
 if pack not in pack_cache:pack_cache[pack]=(args.site_root/'media'/pack).read_bytes()
 d=pack_cache[pack][e['offset']:e['offset']+e['length']];assert hashlib.sha256(d).hexdigest()==e['sha256'];return d

def rebrand_chapter(md, original_path, chapter_path, number, pdf_path):
 """Replace visible brand words while preserving every URL or asset filename."""
 import posixpath
 from urllib.parse import urlsplit, urlunsplit
 destinations=[]
 def protect(match):
  destination=match.group(1);url=urlsplit(destination)
  if not url.scheme and not url.netloc and url.path:
   resolved=posixpath.normpath(posixpath.join(posixpath.dirname(original_path),url.path))
   if number=='001' and resolved=='cards/crypto/season-01/blind-signatures-master-01/LORE-Blind-Signatures-Legendary-v1-Print-v2.png':
    resolved=f'cards/crypto/print-ready/histrove-v1/fronts/png/HISTROVE-Crypto-{number}-Front-Print-v1.png'
   elif url.path.lower().endswith('.pdf') and resolved.startswith('book/crypto-season-01/proofs/'):
    resolved=pdf_path
   destination=urlunsplit(('', '', posixpath.relpath(resolved,posixpath.dirname(chapter_path)),url.query,url.fragment))
  token=f'@@PROTECTED_DESTINATION_{len(destinations)}@@';destinations.append(destination);return token
 protected=re.sub(r'(?<=\]\()([^)]*)(?=\))',protect,md)
 # Protect any bare or autolink URLs too; never brand-rewrite a URL path.
 def protect_bare(match):
  token=f'@@PROTECTED_DESTINATION_{len(destinations)}@@';destinations.append(match.group(0));return token
 protected=re.sub(r'https?://[^\s<>]+',protect_bare,protected)
 result=re.sub(r'\bLORE\b','HISTROVE',protected)
 for i,destination in enumerate(destinations):result=result.replace(f'@@PROTECTED_DESTINATION_{i}@@',destination)
 return result

results=[];qa=[];replacements=[]
for a in A:
 src=O/a['pdf'];assert sha(src)==a['source_sha256'],f'Original PDF changed: {src}';num=src.name[:3];slug=a['slug'];d=fitz.open(src);orig=fitz.open(src);p=d[1];W,H=p.rect.width,p.rect.height
 assert len(d)==2 and d[0].rect==d[1].rect
 dstrel=f'book/crypto-season-01/histrove-v1/{num}-{slug}-histrove-v1.pdf';dst=S/dstrel;dst.parent.mkdir(parents=True,exist_ok=True)
 changed=[]; replaced_headers=0
 for xref in p.get_contents():
  b=d.xref_stream(xref);old=b;replaced_headers+=b.count(b'LORE / CRYPTO SEASON ONE');b=b.replace(b'LORE / CRYPTO SEASON ONE',b'HISTROVE / CRYPTO SEASON ONE');
  if b!=old:d.update_stream(xref,b)
 assert replaced_headers==1,(src,replaced_headers)
 # Only semantic paragraphs with a brand mention are reset; all other page objects survive.
 for c in a['changes']:
  r=fitz.Rect(c['rect']);r.x1=min(W-43,r.x1+3.3) if num=='017' else r.x1;r+=(-.1,-.2,.1,.2);p.add_redact_annot(r,fill=None);changed.append(list(r))
 if a['changes']:
  p.apply_redactions(images=0,graphics=0,text=0)
  stream=io.BytesIO();cv=canvas.Canvas(stream,pagesize=(W,H),pageCompression=1)
  for c in a['changes']:
   width=(W-43-c['origin'][0]) if num=='017' else 242
   style=ParagraphStyle('replacement',fontName='DV',fontSize=c['size'],leading=c['leading'],textColor=HexColor('#5A574F' if c['section']=='sourceNote' else '#0B0B0B'))
   para=Paragraph(rich(c['new_markdown']),style);_,height=para.wrap(width,H)
   assert len(para.blPara.lines)==c['old_lines'],(num,len(para.blPara.lines),c['old_lines'])
   cv.saveState();para.drawOn(cv,c['origin'][0],H-c['origin'][1]+c['size']-height);cv.restoreState()
   replacements.append({'number':num,'slug':slug,'section':c['section'],'index':c['index'],'before':c['markdown'],'after':c['new_markdown']})
  cv.save();overlay=fitz.open(stream=stream.getvalue(),filetype='pdf');p.show_pdf_page(p.rect,overlay,0)
  for link in overlay[0].get_links():
   if 'uri' in link:p.insert_link({'kind':fitz.LINK_URI,'from':link['from'],'uri':link['uri']})
 meta=d.metadata;meta={k:re.sub(r'\bLORE\b','HISTROVE',v) if isinstance(v,str) else v for k,v in meta.items()};d.set_metadata(meta);d.save(dst,garbage=4,deflate=True)
 new=fitz.open(dst);assert new[0].rect==orig[0].rect and new[1].rect==orig[1].rect
 assert not re.search(r'\bLORE\b',' '.join(p.get_text() for p in new)+' '.join(str(x) for x in new.metadata.values()))
 # Verify all text changes are the brand replacement only, independent of reading-order changes.
 def words(doc):return sorted(re.findall(r'\S+',norm(' '.join(p.get_text() for p in doc))))
 want=norm(' '.join(p.get_text() for p in orig)).replace('LORE','HISTROVE')
 assert sorted(re.findall(r'\S+',want))==words(new),(num,'word-content differs')
 # Restore all sources with exactly the original URI targets.
 old_urls=sorted(l['uri'] for p in orig for l in p.get_links() if 'uri' in l);new_urls=sorted(l['uri'] for p in new for l in p.get_links() if 'uri' in l)
 assert old_urls==new_urls,(num,old_urls,new_urls)
 # Native embedded image samples and full art-page rendering stay identical.
 old_images=[hashlib.sha256(orig.xref_stream(i[0])).hexdigest() for i in orig[0].get_images()];new_images=[hashlib.sha256(new.xref_stream(i[0])).hexdigest() for i in new[0].get_images()];assert old_images==new_images
 assert orig[0].get_pixmap(matrix=fitz.Matrix(1,1)).samples==new[0].get_pixmap(matrix=fitz.Matrix(1,1)).samples
 # At 144 dpi verify exact unchanged pixels outside header/brand-paragraph rectangles.
 op=orig[1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False);npix=new[1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False);oa=np.frombuffer(op.samples,np.uint8).reshape(op.height,op.width,3);na=np.frombuffer(npix.samples,np.uint8).reshape(npix.height,npix.width,3);diff=np.any(oa!=na,axis=2);allowed=np.zeros(diff.shape,bool)
 for r in [[42,30,230,44],*changed]:
  x0,y0,x1,y1=r;allowed[max(0,math.floor(y0*2)-2):min(op.height,math.ceil(y1*2)+2),max(0,math.floor(x0*2)-2):min(op.width,math.ceil(x1*2)+2)]=True
 outside=int(np.count_nonzero(diff & ~allowed));assert outside==0,(num,'outside pixels',outside)
 pages=[]
 for n in [1,2]:
  oldpage=M[slug]['pages'][n-1];rel=f'site/public/archive/{num}-histrove-page-{n}.webp';out=S/rel;out.parent.mkdir(parents=True,exist_ok=True)
  if n==1:out.write_bytes(preview_bytes(oldpage['src']))
  else:
   temp=args.output_root.parent/'rendered';temp.mkdir(exist_ok=True);prefix=temp/f'{num}-page';subprocess.run(['pdftoppm','-f','2','-singlefile','-png','-scale-to-y','1100','-scale-to-x','-1',str(dst),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   image=Image.open(str(prefix)+'.png').convert('RGB');assert image.size==(778,1100);image.save(out,'WEBP',quality=90,method=6)
  im=Image.open(out);assert im.size==(oldpage['width'],oldpage['height']);pages.append({'old':oldpage['src'],'new':'/'+rel.removeprefix('site/public/'),'file':rel,'width':im.width,'height':im.height,'sha256':sha(out),'unchangedBytes':n==1})
 # Branded semantic chapter source is the complete original Markdown with brand words changed.
 chapter_src=next((O/'book/crypto-season-01').glob(num+'-*.md'));chapter_path=f'book/crypto-season-01/histrove-v1/chapters/{chapter_src.name}';ch=S/chapter_path;ch.parent.mkdir(parents=True,exist_ok=True)
 md=chapter_src.read_text();newmd=rebrand_chapter(md,str(chapter_src.relative_to(O)),chapter_path,num,dstrel);assert re.findall(r'https?://[^\s)]+',md)==re.findall(r'https?://[^\s)]+',newmd);ch.write_text(newmd)
 # Every rebased repository target must exist; never invent renamed source filenames.
 from urllib.parse import urlsplit,unquote
 import posixpath
 for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',newmd):
  link=urlsplit(target)
  if not link.scheme and not link.netloc and link.path:
   resolved=posixpath.normpath(posixpath.join(posixpath.dirname(chapter_path),unquote(link.path)))
   assert (O/resolved).is_file() or (S/resolved).is_file(),f'Broken chapter link: {chapter_path} -> {target}'
 result={'number':num,'slug':slug,'oldPdf':M[slug]['originalBook'],'sourcePdf':a['pdf'],'sourceSHA256':sha(src),'newPdf':dstrel,'pdfSHA256':sha(dst),'pdfBytes':dst.stat().st_size,'chapter':chapter_path,'chapterSHA256':sha(ch),'pages':pages};results.append(result)
 qa.append({'number':num,'pageCount':2,'pageDimensionsPt':[list(p.rect) for p in new],'originalArtworkStreamsIdentical':True,'artPageRenderPixelIdentical':True,'unchangedPixelsOutsideBrandTextRegions':True,'outsideChangedPixels144dpi':outside,'wordChangesOnlyLOREtoHISTROVE':True,'sourceUrisUnchanged':True,'remainingOldBrandTextCount':0,'brandParagraphCount':len(a['changes']),'brandParagraphRegionsPt':changed,'fontSizeAndLeadingUnchanged':True,'columnWidthExceptionPt':(W-43-307)-242 if num=='017' else 0})
 print(num,'done',len(a['changes']),'paragraphs',dst.stat().st_size,flush=True)
release=S/'book/crypto-season-01/histrove-v1';source=release/'source';source.mkdir(exist_ok=True)
shutil.copy2(__file__,source/'rebrand_books.py');shutil.copy2(args.audit,source/'layout-audit.json')
(release/'manifest.json').write_text(json.dumps({'revision':'HISTROVE-BOOK-v1','sourceCommit':SOURCE_COMMIT,'scope':'Visual and textual brand replacement only. Preserve original artwork, facts, clues, links and page geometry. Not a physical book print-release claim.','sourceFonts':{f:sha(args.font_root/f) for f in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf']},'books':results},indent=2)+'\n')
(release/'qa.json').write_text(json.dumps({'books':qa,'all39Passed':len(qa)==39},indent=2)+'\n')
(release/'text-replacements.json').write_text(json.dumps(replacements,indent=2)+'\n')
(B/'book-asset-map.json').write_text(json.dumps(results,indent=2)+'\n')
print('COMPLETE',len(results),len(replacements),flush=True)
