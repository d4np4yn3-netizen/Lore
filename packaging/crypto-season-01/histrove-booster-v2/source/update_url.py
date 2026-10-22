from pathlib import Path
import fitz, subprocess, hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
R=Path(__file__).resolve().parent
REPO=next(p for p in R.parents if (p/'packaging/crypto-season-01/histrove-booster-v1').is_dir())
source=REPO/'packaging/crypto-season-01/histrove-booster-v1/HISTROVE-Crypto-S01-Booster-Review-v1-Clean.pdf'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='26965c3d43884a1c51b9b84f7304306022cb55544a46664b4f4176559927e83e'
fpath=REPO/'cards/master/front-v3/source/fonts/DejaVuSans.ttf'
b=fpath.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='fb0bd945a4f5aa716dcb8d9b7476bfa30e365a1e'
f=TTFont(fpath);cm=f.getBestCmap();gs=f.getGlyphSet();size=5.9
# Infer exact size from the unchanged outlined l glyph's height, not the historical v1 builder.
gs['l'].draw(pen:=SVGPathPen(gs))
from fontTools.pens.boundsPen import BoundsPen
bp=BoundsPen(gs);gs['l'].draw(bp)
old=fitz.open(source);p=old[0];W,H=p.rect.width,p.rect.height
url_region=fitz.Rect(58,289.5,126,297)
paths=[d for d in p.get_drawings() if url_region.contains(d['rect'])]
assert len(paths)==23
size=(paths[0]['rect'].height)/(bp.bounds[3]-bp.bounds[1])*f['head'].unitsPerEm
# Original PDF paths are rounded to 0.001 pt; canonical 5.9 pt matches them.
assert abs(size-5.9)<.002
size=5.9;s=size/f['head'].unitsPerEm
new='histrove.co.uk';width=sum(f['hmtx'][cm[ord(c)]][0]*s for c in new);x=92-width/2
parts=[]
for c in new:
 g=cm[ord(c)];pen=SVGPathPen(gs);gs[g].draw(pen)
 if pen.getCommands():parts.append(f'<path d="{pen.getCommands()}" transform="translate({x},295) scale({s},{-s})"/>')
 x+=f['hmtx'][g][0]*s
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}"><g fill="#F5F2EB" aria-label="{new}">'+''.join(parts)+'</g></svg>'
(R/'url-overlay.svg').write_text(svg)
subprocess.run(['inkscape',str(R/'url-overlay.svg'),'--export-type=pdf','--export-filename='+str(R/'url-overlay.pdf')],check=True,capture_output=True)
doc=fitz.open(source);p=doc[0]
import re
stream=doc.xref_stream(5);start=stream.index(b'59.367 290.516');end=start+list(re.finditer(rb'(?<!\S)f(?!\S)',stream[start:]))[22].end()
doc.update_stream(5,stream[:start]+stream[end:])
over=fitz.open(R/'url-overlay.pdf');p.show_pdf_page(p.rect,over,0)
name='HISTROVE-Crypto-S01-Booster-URL-Update-v2'
out=R/(name+'-Clean.pdf');doc.save(out,garbage=4,deflate=True)
a=old[0].get_pixmap(dpi=300,alpha=False);b=doc[0].get_pixmap(dpi=300,alpha=False)
ai=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3);bi=np.frombuffer(b.samples,dtype=np.uint8).reshape(b.height,b.width,3)
diff=np.any(ai!=bi,axis=2);yy,xx=np.where(diff);bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
mask=np.ones(diff.shape,bool);mask[1205:1240,240:530]=False
assert not diff[mask].any(),bounds
im=Image.fromarray(bi);im.save(R/(name+'-300dpi.png'),dpi=(300,300))
Image.fromarray(ai).save(R/'before-300dpi.png',dpi=(300,300))
# Side-by-side URL crop for review.
proof=Image.new('RGB',(1400,500),'#0b0b0b');dr=ImageDraw.Draw(proof);font=ImageFont.truetype(str(fpath),25)
for i,(arr,label) in enumerate([(ai,'BEFORE'),(bi,'AFTER')]):
 crop=Image.fromarray(arr).crop((210,1155,560,1355)).resize((630,360))
 proof.paste(crop,(25+i*700,80));dr.text((25+i*700,25),label,font=font,fill='#d4af37')
proof.save(R/'URL-change-before-after.png')
# Full front/back assembly uses exactly the approved crop geometry.
pr=fitz.open();pp=pr.new_page(width=760,height=624);pp.draw_rect(pp.rect,fill=(11/255,)*3,color=None)
pp.insert_font(fontname='DS',fontfile=str(fpath))
for pos,t,sz in [((34,34),'HISTROVE / CRYPTO SEASON 01',14),((34,54),'WEBSITE TEXT UPDATE / DESIGN REVIEW',8),((79,78),'FRONT',8),((414,78),'BACK / ASSEMBLY INDICATIVE',8),((34,593),'Only the printed website address has changed. Artwork and QR are unchanged.',7),((34,609),'Design review only. Existing printer and physical sample limitations still apply.',7)]:pp.insert_text(pos,t,fontname='DS',fontsize=sz,color=(.96,.95,.92))
F1,F2=144.57130432128906,342.9971008300781;FW=F2-F1;half=FW/2;top=8.96002197265625;bottom=365.2130126953125;sc=1.35;hh=(bottom-top)*sc
for dest,clip in [(fitz.Rect(79,90,79+FW*sc,90+hh),fitz.Rect(F1,top,F2,bottom)),(fitz.Rect(414,90,414+half*sc,90+hh),fitz.Rect(F2,top,F2+half,bottom)),(fitz.Rect(414+half*sc,90,414+FW*sc,90+hh),fitz.Rect(F1-half,top,F1,bottom))]:pp.show_pdf_page(dest,doc,0,clip=clip)
pr.save(R/(name+'-Review.pdf'));pp.get_pixmap(matrix=fitz.Matrix(2,2)).save(R/(name+'-Front-and-Back.png'))
qa={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_repository_path':'packaging/crypto-season-01/histrove-booster-v1/HISTROVE-Crypto-S01-Booster-Review-v1-Clean.pdf','changed_only':'Printed address lore-site-v1.vercel.app to histrove.co.uk','font':'Repository-pinned DejaVuSans.ttf, outlined','font_size_pt':5.9,'baseline_pt':295,'center_x_pt':92,'changed_pixel_bbox_300dpi':bounds,'all_pixels_outside_URL_region_identical':True,'qr_pixels_identical':True,'page_boxes_preserved':all(old[0].__getattribute__(x)==doc[0].__getattribute__(x) for x in ['mediabox','trimbox','bleedbox','cropbox']),'status':'REVIEW_ONLY_NOT_PUBLISHED','files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in R.glob(name+'*')]}
(R/'QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
