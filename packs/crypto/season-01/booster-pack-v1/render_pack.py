from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from pathlib import Path
import base64, io, math\nimport cairosvg

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
W, H = 2031, 1557

# Coordinates derived from the supplied QPMN template PDF, normalized to 2031x1557.
CUT = (33, 37, 1998, 1520)
FOLD_L = 602
FOLD_R = 1429
HEAT = (154, 154, 1878, 1402)

GOLD = (212, 175, 55)
WHITE = (248, 248, 246)
BLACK = (7, 7, 8)

ASSETS = {
    "logo": ROOT / "brand/assets/png/lore_logo_primary_gold_white.png",
    "logo_compact": ROOT / "brand/assets/png/lore_logo_compact_gold_white.png",
    "pack_logo_svg": OUT / "LORE-Pack-Logo-v6.svg",
    "hodl": ROOT / "cards/crypto/season-01/birth-of-hodl-master-02/art.png",
    "doge": ROOT / "cards/crypto/season-01/birth-of-doge-master-02/art.png",
    "merge": ROOT / "cards/crypto/season-01/the-merge-master-02/art.png",
    "whitepaper": ROOT / "cards/crypto/season-01/the-whitepaper-master-01/art.png",
    "bitconnect": ROOT / "cards/crypto/season-01/bitconnect-master-01/art.png",
    "mtgox": ROOT / "cards/crypto/season-01/mt-gox-master-01/art.png",
    "buried": ROOT / "cards/crypto/season-01/buried-fortune-master-01/art.png",
}

for k,p in ASSETS.items():
    if not p.exists():
        raise FileNotFoundError(f"Missing approved asset {k}: {p}")

def rgba(path):
    return Image.open(path).convert("RGBA")

def fit_inside(img, max_w, max_h):
    s = min(max_w / img.width, max_h / img.height)
    return img.resize((max(1,int(img.width*s)), max(1,int(img.height*s))), Image.Resampling.LANCZOS)

def render_svg_tight(path, max_w, max_h):
    png = cairosvg.svg2png(url=str(path), output_width=1600)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    return fit_inside(im, max_w, max_h)

def cover(img, box, anchor=(0.5,0.5)):
    x0,y0,x1,y1 = box
    bw,bh = x1-x0,y1-y0
    s = max(bw/img.width, bh/img.height)
    rw,rh = int(img.width*s), int(img.height*s)
    r = img.resize((rw,rh), Image.Resampling.LANCZOS)
    cx = int((rw-bw)*anchor[0]); cy = int((rh-bh)*anchor[1])
    cx = max(0,min(cx,rw-bw)); cy = max(0,min(cy,rh-bh))
    return r.crop((cx,cy,cx+bw,cy+bh))

def toned(img, brightness=1.0, color=1.0, contrast=1.0):
    out = ImageEnhance.Brightness(img).enhance(brightness)
    out = ImageEnhance.Color(out).enhance(color)
    out = ImageEnhance.Contrast(out).enhance(contrast)
    return out

def paste_cover(canvas, img, box, anchor=(0.5,0.5), opacity=255):
    r = cover(img, box, anchor)
    if opacity != 255:
        a = r.getchannel("A").point(lambda p: p*opacity//255)
        r.putalpha(a)
    canvas.alpha_composite(r, (box[0],box[1]))

def polygon_art(canvas, art, bbox, points, anchor=(0.5,0.5), opacity=255):
    r = cover(art, bbox, anchor)
    layer = Image.new("RGBA", (W,H), (0,0,0,0))
    layer.alpha_composite(r, (bbox[0],bbox[1]))
    mask = Image.new("L",(W,H),0)
    ImageDraw.Draw(mask).polygon(points, fill=opacity)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L",(W,H),0), mask))
    canvas.alpha_composite(layer)

def add_vignette(img, box, strength=170):
    x0,y0,x1,y1=box
    bw,bh=x1-x0,y1-y0
    mask=Image.new("L",(bw,bh),0)
    px=mask.load()
    cx,cy=bw/2,bh/2
    maxd=math.hypot(cx,cy)
    for yy in range(bh):
        for xx in range(bw):
            d=math.hypot(xx-cx,yy-cy)/maxd
            px[xx,yy]=int(max(0,min(255,(d**1.7)*strength)))
    shade=Image.new("RGBA",(bw,bh),(0,0,0,255))
    shade.putalpha(mask)
    img.alpha_composite(shade,(x0,y0))

def font(size,bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

canvas = Image.new("RGBA",(W,H),BLACK+(255,))
draw = ImageDraw.Draw(canvas,"RGBA")

# ---- BACK PANELS ----
whitepaper = toned(rgba(ASSETS["whitepaper"]),0.72,0.72,1.10)
bitconnect = toned(rgba(ASSETS["bitconnect"]),0.82,0.85,1.10)
mtgox = toned(rgba(ASSETS["mtgox"]),0.70,0.70,1.12)
buried = toned(rgba(ASSETS["buried"]),0.76,0.72,1.10)

paste_cover(canvas, whitepaper, (0,0,FOLD_L,H), anchor=(0.38,0.50))
paste_cover(canvas, mtgox, (FOLD_R,0,W,H), anchor=(0.62,0.52))
draw.rectangle((0,0,FOLD_L,H), fill=(0,0,0,118))
draw.rectangle((FOLD_R,0,W,H), fill=(0,0,0,118))

# Secondary approved-art shards on the rear halves.
polygon_art(canvas, bitconnect, (55,430,560,1250),
            [(25,760),(330,420),(602,560),(602,1190),(230,1335),(25,1160)],
            anchor=(0.50,0.48), opacity=190)
polygon_art(canvas, buried, (1470,405,2010,1260),
            [(1429,570),(1710,415),(2015,650),(2015,1170),(1655,1345),(1429,1100)],
            anchor=(0.52,0.56), opacity=178)

# Back panel dark glass overlays.
for bx0,bx1 in [(0,FOLD_L),(FOLD_R,W)]:
    draw.rectangle((bx0,154,bx1,1402), outline=GOLD+(165,), width=4)
    draw.rectangle((bx0+24,178,bx1-24,1378), outline=GOLD+(70,), width=2)

compact = render_svg_tight(ASSETS["pack_logo_svg"], 370, 205)
for cx in [FOLD_L//2, FOLD_R+(W-FOLD_R)//2]:
    canvas.alpha_composite(compact,(int(cx-compact.width/2),210))

small = font(30, True)
tracking_text = "CRYPTO  •  SEASON 01"
for cx in [FOLD_L//2, FOLD_R+(W-FOLD_R)//2]:
    b=draw.textbbox((0,0),tracking_text,font=small)
    draw.text((cx-(b[2]-b[0])/2,465),tracking_text,font=small,fill=WHITE+(225,))

# ---- FRONT PANEL ----
hodl = toned(rgba(ASSETS["hodl"]),0.98,1.06,1.07)
doge = toned(rgba(ASSETS["doge"]),1.02,1.07,1.06)
merge = toned(rgba(ASSETS["merge"]),0.98,1.06,1.08)

paste_cover(canvas, hodl, (FOLD_L,0,FOLD_R,H), anchor=(0.49,0.50))
add_vignette(canvas,(FOLD_L,0,FOLD_R,H),170)

# Black fade for brand plate.
for y in range(145,650):
    t=(y-145)/(650-145)
    a=int(210*(1-t)**1.4)
    draw.rectangle((FOLD_L,y,FOLD_R,y+2),fill=(0,0,0,a))
for y in range(1060,1450):
    t=(y-1060)/(1450-1060)
    a=int(35+180*t)
    draw.rectangle((FOLD_L,y,FOLD_R,y+2),fill=(0,0,0,a))

# Approved art shards.
polygon_art(canvas, doge, (1080,300,1429,880),
            [(1110,320),(1429,245),(1429,865),(1240,805),(1055,540)],
            anchor=(0.53,0.43), opacity=238)
polygon_art(canvas, merge, (602,790,1050,1402),
            [(602,925),(795,785),(1065,1115),(890,1402),(602,1330)],
            anchor=(0.48,0.55), opacity=235)

# Gold separators on shard edges.
draw.line([(1058,540),(1240,805),(1429,865)], fill=GOLD+(235,), width=6)
draw.line([(602,925),(795,785),(1065,1115)], fill=GOLD+(235,), width=6)

# Front double frame, echoing the shared card back.
draw.rounded_rectangle((FOLD_L+24,176,FOLD_R-24,1382), radius=20, outline=GOLD+(230,), width=7)
draw.rounded_rectangle((FOLD_L+43,195,FOLD_R-43,1363), radius=16, outline=GOLD+(78,), width=2)

# Exact approved primary logo.
logo = fit_inside(rgba(ASSETS["logo"]), 540, 250)
canvas.alpha_composite(logo,(int((FOLD_L+FOLD_R-logo.width)/2),214))

f_crypto = font(92, True)
f_season = font(38, True)
t="CRYPTO"
b=draw.textbbox((0,0),t,font=f_crypto)
draw.text(((FOLD_L+FOLD_R-(b[2]-b[0]))/2,465),t,font=f_crypto,fill=WHITE+(255,))
t2="SEASON 01"
b2=draw.textbbox((0,0),t2,font=f_season)
draw.text(((FOLD_L+FOLD_R-(b2[2]-b2[0]))/2,568),t2,font=f_season,fill=GOLD+(255,))

# Minimal pack count lock-up.
pill=(804,1272,1228,1360)
draw.rounded_rectangle(pill, radius=42, fill=(7,7,8,218), outline=GOLD+(238,), width=4)
f6=font(42,True)
t3="6 CARDS"
b3=draw.textbbox((0,0),t3,font=f6)
draw.text(((pill[0]+pill[2]-(b3[2]-b3[0]))/2,1291),t3,font=f6,fill=WHITE+(255,))

# Micro brand rail at bottom of visible front, above heat seal.
micro=font(21,True)
microtext="LORE  /  CRYPTO  /  S01"
mb=draw.textbbox((0,0),microtext,font=micro)
draw.text(((FOLD_L+FOLD_R-(mb[2]-mb[0]))/2,1380),microtext,font=micro,fill=GOLD+(190,))

# ---- FOIL / PACKAGING LANGUAGE ----
# Heat-seal diagonal micro-lines (art extends beneath as required by the template).
for y0,y1 in [(0,154),(1402,H)]:
    draw.rectangle((0,y0,W,y1),fill=(4,4,5,72))
    for x in range(-H,W+H,38):
        draw.line((x,y0,x+150,y1),fill=GOLD+(38,),width=3)

# Side heat-seal zones.
for x0,x1 in [(0,154),(1878,W)]:
    draw.rectangle((x0,154,x1,1402),fill=(4,4,5,58))

# Fine prismatic streaks - restrained, printable, and behind no critical type.
# Keep the print artwork clean: only a whisper of gold foil movement.
for p1,p2 in [
    ((120,1040),(550,790)),
    ((1490,770),(1970,1030)),
]:
    draw.line([p1,p2],fill=GOLD+(18,),width=4)

# Fold-edge shadows to make the review feel like a wrapper without changing print geometry.
draw.rectangle((FOLD_L-4,0,FOLD_L+4,H),fill=(0,0,0,110))
draw.rectangle((FOLD_R-4,0,FOLD_R+4,H),fill=(0,0,0,110))

# Save exact flat print file.
flat = canvas.convert("RGB")
flat_path = OUT/"LORE-Crypto-Booster-Pack-v1-Flat-Print.png"
flat.save(flat_path,"PNG",dpi=(300,300),optimize=True)

# Front crop preview.
front = flat.crop((FOLD_L,0,FOLD_R,H))
front_path=OUT/"LORE-Crypto-Booster-Pack-v1-Front-Preview.png"
front.save(front_path,"PNG",dpi=(300,300),optimize=True)

# Template guide overlay for review only.
guide = canvas.copy()
gd = ImageDraw.Draw(guide,"RGBA")

def dashed_line(draw, pts, dash=22, gap=16, fill=(40,75,235,255), width=5):
    (x1,y1),(x2,y2)=pts
    dx,dy=x2-x1,y2-y1
    L=math.hypot(dx,dy)
    ux,uy=dx/L,dy/L
    t=0
    while t<L:
        e=min(L,t+dash)
        draw.line((x1+ux*t,y1+uy*t,x1+ux*e,y1+uy*e),fill=fill,width=width)
        t+=dash+gap

# Cut line.
gd.rectangle(CUT, outline=(255,255,255,210), width=7)
gd.rectangle((CUT[0]+3,CUT[1]+3,CUT[2]-3,CUT[3]-3), outline=(0,0,0,240), width=2)
# Fold lines.
dashed_line(gd,((FOLD_L,0),(FOLD_L,H)),fill=(35,70,235,245),width=6)
dashed_line(gd,((FOLD_R,0),(FOLD_R,H)),fill=(35,70,235,245),width=6)
# Heat seal boundary.
hx0,hy0,hx1,hy1=HEAT
for a,b in [((hx0,hy0),(hx1,hy0)),((hx1,hy0),(hx1,hy1)),((hx1,hy1),(hx0,hy1)),((hx0,hy1),(hx0,hy0))]:
    dashed_line(gd,(a,b),fill=(250,0,145,245),width=6)

# Small guide labels.
lab=font(24,True)
gd.text((FOLD_L+16,80),"FRONT PANEL",font=lab,fill=(255,255,255,220),stroke_width=2,stroke_fill=(0,0,0,180))
gd.text((38,80),"BACK HALF",font=lab,fill=(255,255,255,210),stroke_width=2,stroke_fill=(0,0,0,180))
gd.text((FOLD_R+18,80),"BACK HALF",font=lab,fill=(255,255,255,210),stroke_width=2,stroke_fill=(0,0,0,180))
guide_path=OUT/"LORE-Crypto-Booster-Pack-v1-Template-Overlay.png"
guide.convert("RGB").save(guide_path,"PNG",dpi=(300,300),optimize=True)

# Small JPEG preview encoded as text so the review image can be surfaced through text-only GitHub access.
preview=front.copy()
preview.thumbnail((650,1225),Image.Resampling.LANCZOS)
buf=io.BytesIO()
preview.save(buf,"JPEG",quality=88,optimize=True)
(OUT/"front-preview-base64.txt").write_text(base64.b64encode(buf.getvalue()).decode("ascii"))

print("Rendered:", flat_path)
print("Canvas:", flat.size, "DPI 300")
print("Front crop:", front.size)
