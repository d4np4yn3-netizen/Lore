"""Build standalone website/card and book-spread preview derivatives."""
from pathlib import Path
import json, subprocess
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
PREFIX = "LORE-Crypto-038-CryptoPunks"
QA = ROOT / "qa"
QA.mkdir(exist_ok=True)
book = ROOT / f"{PREFIX}-Book-Pages-v1.pdf"
front = ROOT / f"{PREFIX}-Epic-Print-v1"
subprocess.run(["pdftoppm","-png","-r","130",str(book),str(QA/"book")],check=True)
subprocess.run(["pdftoppm","-png","-r","300","-singlefile",str(front.with_suffix(".pdf")),str(QA/"card-pdf-300dpi")],check=True)
a,b = [Image.open(QA/f"book-{n}.png").convert("RGB") for n in (1,2)]
spread = Image.new("RGB",(a.width+b.width,max(a.height,b.height)))
spread.paste(a,(0,0));spread.paste(b,(a.width,0))
spread.save(ROOT/f"{PREFIX}-Book-Spread-v1.png")
card = Image.open(front.with_suffix(".png")).convert("RGB")
card.crop((36,36,780,1074)).resize((600,837),Image.Resampling.LANCZOS).save(ROOT/f"{PREFIX}-Web-v1.png")
art = Image.open(ROOT/"art.png")
for crop in json.loads((ROOT/"source/crop-suggestions.json").read_text())["clues"]:
    art.crop(crop["sourceBoxXYXY"]).save(QA/f"clue-{crop['number']:02}.png")
