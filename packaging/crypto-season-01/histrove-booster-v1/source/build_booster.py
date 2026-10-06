from pathlib import Path
import base64, hashlib, io, json, re, shutil
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import Image
import cairosvg, fitz, qrcode
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT.parents[2]
OUT=ROOT
NAME='LORE-Crypto-S01-Booster-Test-v1'
W,H=487.5589904785156,374.1730041503906
F1,F2=144.57130432128906,342.9971008300781
FW=F2-F1
CUT=(8.032012939453125,8.96002197265625,479.5260009765625,365.2130126953125)
SAFE=(37,37,451,337)
COLORS={'black':'#0B0B0B','bone':'#F5F2EB','gold':'#D4AF37','charcoal':'#1A1A1A','white':'#FFFFFF'}
URL='https://lore-site-v1.vercel.app/'
FONTROOT=ASSETS/'cards/master/front-v3/source/fonts'
FONTS={k:TTFont(FONTROOT/f) for k,f in [('regular','DejaVuSans.ttf'),('bold','DejaVuSans-Bold.ttf')]}
parts=[];used=[]
def put(s):parts.append(s)
def rect(x,y,w,h,fill,stroke=None,sw=.6):
 put(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>')
def line(x1,y1,x2,y2,color,sw=.6):
 put(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{sw}"/>')
def text_width(txt,size,font='regular',track=0):
 f=FONTS[font];cm=f.getBestCmap();return sum(f['hmtx'][cm[ord(c)]][0] for c in txt)/f['head'].unitsPerEm*size+max(0,len(txt)-1)*track
def text(txt,x,y,size=7,font='regular',color='#F5F2EB',track=0,align='left'):
 width=text_width(txt,size,font,track)
 if align=='center':x-=width/2
 if align=='right':x-=width
 f=FONTS[font];cm=f.getBestCmap();gs=f.getGlyphSet();s=size/f['head'].unitsPerEm
 put(f'<g aria-label="{txt.replace("&","&amp;")}" fill="{color}">')
 for c in txt:
  g=cm[ord(c)];pen=SVGPathPen(gs);gs[g].draw(pen);d=pen.getCommands()
  if d:put(f'<path d="{d}" transform="translate({x},{y}) scale({s},{-s})"/>')
  x+=f['hmtx'][g][0]*s+track
 put('</g>')
 return width
def logo(name,x,y,w):
 p=ASSETS/'brand/assets/svg'/name;used.append(str(p.relative_to(ASSETS)))
 r=ET.fromstring(p.read_text());vb=[float(v) for v in r.attrib['viewBox'].split()];sc=w/vb[2]
 content=''.join(ET.tostring(e,encoding='unicode') for e in r if e.tag.split('}')[-1] not in ['title','desc'])
 put(f'<g transform="translate({x} {y}) scale({sc})">{content}</g>')
def art(folder,poly,source_crop=None):
 p=ASSETS/f'cards/crypto/season-01/{folder}/art.png';used.append(str(p.relative_to(ASSETS)))
 iw,ih=Image.open(p).size
 xs=[v[0] for v in poly];ys=[v[1] for v in poly];x,y,w,h=min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
 sx,sy,ex,ey=source_crop or (0,0,iw,ih);scale=max(w/(ex-sx),h/(ey-sy))
 ix=x+(w-(ex-sx)*scale)/2-sx*scale;iy=y+(h-(ey-sy)*scale)/2-sy*scale
 tag='clip'+str(len(parts));points=' '.join(f'{a},{b}' for a,b in poly)
 put(f'<defs><clipPath id="{tag}"><polygon points="{points}"/></clipPath></defs>')
 put(f'<image x="{ix}" y="{iy}" width="{iw*scale}" height="{ih*scale}" clip-path="url(#{tag})" href="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"/>')
 return {'path':str(p.relative_to(ASSETS)),'effective_dpi':72/scale,'crop':source_crop}
def qr(x,y,size):
 q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4,box_size=1);q.add_data(URL);q.make(fit=True)
 m=q.get_matrix();n=len(m);cell=size/n
 rect(x,y,size,size,'#FFFFFF')
 path=[]
 for yy,row in enumerate(m):
  for xx,v in enumerate(row):
   if v:path.append(f'M{x+xx*cell:.5f},{y+yy*cell:.5f}h{cell:.5f}v{cell:.5f}h{-cell:.5f}z')
 put('<path fill="#000000" d="'+''.join(path)+'"/>')
 return {'payload':URL,'modules_with_quiet_zone':n,'size_mm':size*25.4/72,'module_mm':cell*25.4/72,'quiet_zone_modules':4}

gold=COLORS['gold'];black=COLORS['black'];bone=COLORS['bone']
rect(0,0,W,H,black)
# Central front: approved lockup, then two intact illustrations clipped into panels.
logo('lore_logo_primary_gold_white.svg',F1+19,32,FW-38)
art_placements=[]
left=[(F1+9,165),(F1+99,155),(F1+109,279),(F1+9,279)]
right=[(F1+99,155),(F2-9,165),(F2-9,279),(F1+109,279)]
art_placements.append(art('birth-of-hodl-master-02',left,(80,190,990,1430)))
art_placements.append(art('birth-of-doge-master-02',right,(120,190,1030,1430)))
put(f'<path d="M{F1+9} 165L{F1+99} 155L{F2-9} 165V279H{F1+9}Z" fill="none" stroke="{gold}" stroke-width=".75"/>')
line(F1+99,155,F1+109,279,gold,1.0)
text('CRYPTO',(F1+F2)/2,309,25,'bold',gold,track=2.8,align='center')
text('SEASON 01',(F1+F2)/2,324,7.4,'bold',bone,track=2.3,align='center')
line(F1+14,321,F1+47,321,gold,.55);line(F2-47,321,F2-14,321,gold,.55)
# Left wing becomes the right half of the back. Keep all lettering off the seal.
cx=91
text('CRYPTO',cx,58,12,'bold',gold,track=.8,align='center')
text('SEASON 01',cx,73,6.7,'bold',bone,track=1.3,align='center')
line(48,83,134,83,gold,.55)
text('CARD RARITIES',cx,98,5.8,'bold',gold,track=.8,align='center')
for i,word in enumerate(['Common','Uncommon','Rare','Epic','Legendary','Mythic']):
 text(word,cx,111+i*10.3,7.1,'regular',bone,align='center')
text('EXPLORE THE',cx,189,6.2,'bold',bone,track=.6,align='center')
text('COLLECTION',cx,199,6.2,'bold',bone,track=.8,align='center')
qr_info=qr(51,210,80)
text('lore-site-v1.vercel.app',cx,305,5.8,'regular',bone,align='center')
text('BOOSTER PACK',cx,326,6,'bold',gold,track=.65,align='center')
# Right wing becomes the left half of the back. Approved Whitepaper artwork.
cx2=395.5
logo('lore_logo_compact_gold_white.svg',354,38,83)
text('CRYPTO • SEASON 01',cx2,117,6.1,'bold',gold,track=.2,align='center')
art_placements.append(art('the-whitepaper-master-005',[(354,133),(437,133),(437,249.2),(354,249.2)]))
rect(354,133,83,116.2,'none',gold,.55)
for i,s in enumerate(['LORE transforms','defining moments','of internet culture','into premium','collectible art.']):
 text(s,cx2,270+i*10,6.7,'regular',bone,align='center')
line(354,326,437,326,gold,.55)

svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W/72*25.4}mm" height="{H/72*25.4}mm" viewBox="0 0 {W} {H}"><title>LORE Crypto Season 01 - booster test-print artwork v1</title><desc>Exact approved LORE assets. Flat artwork with no printer guides. New packaging composition for review and physical sampling.</desc>'+''.join(parts)+'</svg>'
(OUT/(NAME+'.svg')).write_text(svg)
cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(OUT/(NAME+'-raw.pdf')))
r=PdfReader(OUT/(NAME+'-raw.pdf'));p=r.pages[0]
p.mediabox=RectangleObject([0,0,W,H]);p.bleedbox=RectangleObject([0,0,W,H]);p.trimbox=RectangleObject([CUT[0],H-CUT[3],CUT[2],H-CUT[1]])
w=PdfWriter();w.add_page(p);w.add_metadata({'/Title':'LORE Crypto Season 01 | Booster test-print artwork v1','/Author':'LORE','/Subject':'Exact supplied QPMN template geometry. New packaging layout for sample review. Flat sRGB artwork; no dielines or foil separation.'})
with open(OUT/(NAME+'.pdf'),'wb') as f:w.write(f)
(OUT/(NAME+'-raw.pdf')).unlink()
doc=fitz.open(OUT/(NAME+'.pdf'));page=doc[0]
pix=page.get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False)
im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.save(OUT/(NAME+'-300dpi.png'),dpi=(300,300),icc_profile=Image.open(ASSETS/'cards/crypto/season-01/birth-of-doge-master-02/art.png').info.get('icc_profile'))

# Proof document is explicitly separate from the clean print file.
proof=fitz.open()
pp=proof.new_page(width=760,height=620)
def proof_text(page,pos,txt,**kw):
 page.insert_font(fontname='LOREsans',fontfile=str(FONTROOT/'DejaVuSans.ttf'))
 page.insert_text(pos,txt,fontname='LOREsans',**kw)
pp.draw_rect(pp.rect,color=None,fill=(.102,.102,.102))
proof_text(pp,(34,36),'LORE / CRYPTO SEASON 01',fontsize=14,color=(.831,.686,.216))
proof_text(pp,(34,55),'BOOSTER PACK - FRONT AND ASSEMBLED BACK',fontsize=8,color=(.96,.95,.92))
scale=1.35;top=90;leftx=78;backx=414
front_rect=fitz.Rect(leftx,top,leftx+FW*scale,top+(CUT[3]-CUT[1])*scale)
pp.show_pdf_page(front_rect,doc,0,clip=fitz.Rect(F1,CUT[1],F2,CUT[3]))
# Joining outer wings illustrates the rear; blank centre gap represents fin-seal allowance.
half=FW/2
pp.show_pdf_page(fitz.Rect(backx,top,backx+half*scale,top+(CUT[3]-CUT[1])*scale),doc,0,clip=fitz.Rect(F2,CUT[1],F2+half,CUT[3]))
pp.show_pdf_page(fitz.Rect(backx+half*scale,top,backx+FW*scale,top+(CUT[3]-CUT[1])*scale),doc,0,clip=fitz.Rect(F1-half,CUT[1],F1,CUT[3]))
proof_text(pp,(leftx,top-12),'FRONT',fontsize=8,color=(.96,.95,.92))
proof_text(pp,(backx,top-12),'BACK - SEAL POSITION INDICATIVE',fontsize=8,color=(.96,.95,.92))
proof_text(pp,(34,597),'FLAT DESIGN PREVIEW  /  NO SIMULATED FOIL, WRINKLES OR MATERIAL LIGHTING',fontsize=7,color=(.831,.686,.216))
pp2=proof.new_page(width=660,height=570)
proof_text(pp2,(28,30),'PRINTER GUIDE PROOF - DO NOT PRINT THIS PAGE',fontsize=13)
dx,dy=86,76
pp2.show_pdf_page(fitz.Rect(dx,dy,dx+W,dy+H),doc,0)
pp2.draw_rect(fitz.Rect(dx+CUT[0],dy+CUT[1],dx+CUT[2],dy+CUT[3]),color=(0,1,1),width=.65)
for x in [F1,F2]:pp2.draw_line((dx+x,dy+CUT[1]),(dx+x,dy+CUT[3]),color=(.4,.65,1),width=.6,dashes='[3 3] 0')
pp2.draw_rect(fitz.Rect(dx+SAFE[0],dy+SAFE[1],dx+SAFE[2],dy+SAFE[3]),color=(1,.1,.6),width=.65,dashes='[3 3] 0')
for a,t in [(dx+45,'BACK / QR'),(dx+F1+60,'FRONT'),(dx+F2+32,'BACK / ART')]:proof_text(pp2,(a,66),t,fontsize=7)
for y,t in [(478,'Cyan: cut line  |  Blue: folds  |  Magenta: inner edge of heat-seal areas'),(493,'Bleed canvas: 172 x 132 mm. Exact page and paths measured from the supplied PDF.'),(508,'Upload the clean 300-DPI PNG, or clean PDF if accepted. Print at 100%; do not fit to page.'),(523,'Flat sRGB gold is printed colour. Metallic foil and printer colour conversions are not specified.'),(538,'New pack layout for review / sample testing. Card quantity and pull-rate claims are intentionally absent.')]:
 proof_text(pp2,(28,y),t,fontsize=8)
proof.save(OUT/(NAME+'-Proof.pdf'),garbage=4,deflate=True)
preview=proof[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
Image.frombytes('RGB',[preview.width,preview.height],preview.samples).save(OUT/(NAME+'-Preview.png'))
guide=proof[1].get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False)
guide.save(ROOT/'guide-review.png')
manifest={'revision':NAME,'status':'NEW_PACKAGING_LAYOUT_FOR_REVIEW_AND_TEST_PRINT','source_repository':'https://github.com/d4np4yn3-netizen/Lore','source_commit':'26bb69ef670b1a2b28cb342c3df601bd08ad2277','template':{'path':'Booster-Pack-Printer-Template.pdf','sha256':hashlib.sha256((ROOT/'Booster-Pack-Printer-Template.pdf').read_bytes()).hexdigest(),'page_pt':[W,H],'page_mm':[W/72*25.4,H/72*25.4],'trim_rect_top_left_pt':CUT,'fold_x_pt':[F1,F2],'inner_heat_seal_rect_top_left_pt':SAFE,'png_px':[pix.width,pix.height],'dpi':300,'note':'Template page geometry and vector lines take priority over rounded and inconsistent template prose.'},'palette':COLORS,'qr':qr_info,'art_placements':art_placements,'assets':[{'path':s,'sha256':hashlib.sha256((ASSETS/s).read_bytes()).hexdigest()} for s in sorted(set(used))],'typography':['DejaVuSans-Bold.ttf','DejaVuSans.ttf'],'production_notes':['Exact approved source assets; clipping and uniform placement only; no AI repainting or logo reconstruction.','Fonts outlined in SVG/PDF; artwork embedded at original source resolution.','No die, fold, safe, dimension or heat-seal guide lines in the clean print files.','No quantity, pull rate, foil guarantee, barcode or unconfirmed commercial claim.','Colour output is RGB; printer profile, substrate and any metallic finish must be handled by printer.','Rear assembly preview is indicative; follow printer template for manufacturing.'],'files':[]}
for p in OUT.glob(NAME+'*'):
 manifest['files'].append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT/(NAME+'-Manifest.json')).write_text(json.dumps(manifest,indent=2))
print(json.dumps({'outputs':[p.name for p in OUT.iterdir()],'size_px':[pix.width,pix.height],'art_effective_dpi':[round(a['effective_dpi']) for a in art_placements],'qr':qr_info},indent=2))

