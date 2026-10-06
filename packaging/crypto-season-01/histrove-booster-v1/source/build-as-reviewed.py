from pathlib import Path
import fitz, json, hashlib, subprocess, io
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
BRAND=ROOT.parent/'histrove-rollout/repo/brand/assets/svg'
src=(ROOT/'source/build_booster.py').read_text().split("gold=COLORS")[0]
src=src.replace("ASSETS=ROOT.parents[2]","ASSETS=ROOT.parent/'histrove-rollout/repo'")
src=src.replace("import cairosvg, fitz, qrcode", "import fitz")
exec(src)
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
NAME='HISTROVE-Crypto-S01-Booster-Review-v1'
# Source PDF form recovered intact from the approved v2 guide.
doc=fitz.open(ROOT/'source/v2-clean-recovered.pdf');p=doc[0]
black=(11/255,)*3;gold='#D4AF37';bone='#F5F2EB'
regions=[(180,39,310,128),(350,38,442,98),(350,103,442,143),(51,99,133,154),(51,317,133,333)]
for r in regions:p.add_redact_annot(fitz.Rect(r),fill=black)
p.apply_redactions(images=0,graphics=1,text=0)
# Use exact current SVG logos; no redraw or substituted lettering.
parts=[]
for name,x,y,width in [('compact',148.8,29.0,190),('compact',349.5,43,90)]:
 source=BRAND.parent/'png'/f'histrove_{name}_white_transparent-2400.png'
 height=width*1180/2400;p.insert_image(fitz.Rect(x,y,x+width,y+height),filename=str(source))
text('History Worth Holding',(F1+F2)/2,125.5,6.4,'regular',bone,track=.35,align='center')
for i,t in enumerate(['History','Worth','Holding']):text(t,394.5,113+i*10,8.8,'bold',gold if i==2 else bone,align='center')
for i,t in enumerate(['HISTROVE transforms','defining moments','of internet culture','into premium','collectible art.']):text(t,92,108+i*10,6.6,'regular',bone,align='center')
text('10 CARDS',92,326,6.8,'bold',gold,track=.65,align='center')
# Front quantity sits inside the existing heat-seal exclusion boundary.
text('10 CARDS',(F1+F2)/2,335,5.3,'bold',bone,track=.8,align='center')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}pt" height="{H}pt" viewBox="0 0 {W} {H}">'+''.join(parts)+'</svg>'
(ROOT/'overlay.svg').write_text(svg)
subprocess.run(['inkscape',str(ROOT/'overlay.svg'),'--export-type=pdf','--export-text-to-path','--export-filename='+str(ROOT/'overlay.pdf')],check=True,capture_output=True)
over=fitz.open(ROOT/'overlay.pdf');p.show_pdf_page(p.rect,over,0)
doc.set_metadata({'title':'HISTROVE Crypto Season 01 booster review v1','author':'HISTROVE','subject':'Review proof. 10 cards. Exact supplied wrapper template. Flat RGB colour; physical sample approval pending.'})
doc.save(OUT/(NAME+'-Clean.pdf'),garbage=4,deflate=True)
r=PdfReader(OUT/(NAME+'-Clean.pdf'));p=r.pages[0];p.mediabox=RectangleObject([0,0,W,H]);p.bleedbox=RectangleObject([0,0,W,H]);p.trimbox=RectangleObject([CUT[0],H-CUT[3],CUT[2],H-CUT[1]])
w=PdfWriter();w.add_page(p);w.add_metadata({'/Title':'HISTROVE Crypto Season 01 booster review v1','/Author':'HISTROVE'});w.write(OUT/(NAME+'-Clean.pdf'))
doc=fitz.open(OUT/(NAME+'-Clean.pdf'));pix=doc[0].get_pixmap(dpi=300,alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.save(OUT/(NAME+'-300dpi.png'),dpi=(300,300))
proof=fitz.open();pp=proof.new_page(width=760,height=624);pp.draw_rect(pp.rect,color=None,fill=black)
FONTROOT=ROOT.parent/'histrove-rollout/repo/cards/master/front-v3/source/fonts'
def pt(page,pos,t,size=8,color=(.96,.95,.92)):
 page.insert_font(fontname='DS',fontfile=str(FONTROOT/'DejaVuSans.ttf'));page.insert_text(pos,t,fontname='DS',fontsize=size,color=color)
pt(pp,(34,34),'HISTROVE / CRYPTO SEASON 01',14,(.831,.686,.216));pt(pp,(34,54),'BOOSTER PACK / 10 CARDS / DESIGN REVIEW',8)
scale=1.35;top=90;left=79;back=414;hh=(CUT[3]-CUT[1])*scale;half=FW/2
pp.show_pdf_page(fitz.Rect(left,top,left+FW*scale,top+hh),doc,0,clip=fitz.Rect(F1,CUT[1],F2,CUT[3]))
pp.show_pdf_page(fitz.Rect(back,top,back+half*scale,top+hh),doc,0,clip=fitz.Rect(F2,CUT[1],F2+half,CUT[3]))
pp.show_pdf_page(fitz.Rect(back+half*scale,top,back+FW*scale,top+hh),doc,0,clip=fitz.Rect(F1-half,CUT[1],F1,CUT[3]))
pt(pp,(left,78),'FRONT');pt(pp,(back,78),'BACK / ASSEMBLY INDICATIVE')
pt(pp,(34,593),'Flat artwork preview. Wrapper material supplies the physical finish.',7,(.831,.686,.216));pt(pp,(34,609),'Design review only. Printer acceptance and physical sample checks remain pending.',7)
pp2=proof.new_page(width=660,height=580);pt(pp2,(28,30),'PRINTER GUIDE PROOF / DO NOT PRINT THIS PAGE',12,(0,0,0));dx,dy=86,76
pp2.show_pdf_page(fitz.Rect(dx,dy,dx+W,dy+H),doc,0)
pp2.draw_rect(fitz.Rect(dx+CUT[0],dy+CUT[1],dx+CUT[2],dy+CUT[3]),color=(0,1,1),width=.65)
for x in [F1,F2]:pp2.draw_line((dx+x,dy+CUT[1]),(dx+x,dy+CUT[3]),color=(.4,.65,1),width=.6,dashes='[3 3] 0')
pp2.draw_rect(fitz.Rect(dx+37,dy+37,dx+451,dy+337),color=(1,.1,.6),width=.65,dashes='[3 3] 0')
for y,t in [(478,'Cyan: cut. Blue: folds. Magenta: inner heat-seal boundary from supplied template.'),(493,'Bleed canvas: 172 x 132 mm. Trim: 166.333 x 125.678 mm. Front: 70 mm wide.'),(508,'Clean PNG: 2032 x 1560 pixels / 300 DPI. Clean PDF uses exact template page geometry.'),(523,'Print at 100% / actual size. Do not fit to page. Guides are absent from clean artwork.'),(538,'Flat RGB gold. No metallic ink, foil mask, printer ICC or substrate finish specified.'),(553,'Rear assembly is indicative. Confirm fin-seal handling and printed QR on a physical sample.')]:pt(pp2,(28,y),t,8,(0,0,0))
proof.save(OUT/(NAME+'-Guide-Proof.pdf'),garbage=4,deflate=True)
proof[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(OUT/(NAME+'-Front-and-Back.png'))
proof[1].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(ROOT/'guide-qa.png')
print(OUT)
