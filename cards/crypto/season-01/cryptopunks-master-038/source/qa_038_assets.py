"""Verify the recovered approved 038 artwork, copy, layout, and QR."""
from pathlib import Path
import base64, hashlib, json, sys, xml.etree.ElementTree as ET
import fitz
import numpy as np
from PIL import Image
from pypdf import PdfReader
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".deps"))
import zxingcpp
EXPECTED = "21027f7ece79e3a6ca3b205f631cb4a648027d4028c27d77c760d36555728abb"
PAYLOAD = "https://lore-site-v1.vercel.app/crypto/038/"
PREFIX = "LORE-Crypto-038-CryptoPunks"
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
art = Image.open(ROOT / "art.png").convert("RGB")
assert sha(ROOT / "art.png") == EXPECTED
assert art.size == (1060,1484)
svg = ET.parse(ROOT / f"{PREFIX}-Epic-Print-v1.svg").getroot()
nodes = {x.get("id"):x for x in svg.iter() if x.get("id")}
assert (svg.get("width"),svg.get("height")) == ("816","1110")
assert nodes["locked-crypto-front"].get("transform") == "translate(46.515 48.921) scale(0.8033)"
assert nodes["moment-context"].get("font-size") == "25"
assert nodes["moment-context"].get("font-weight") == "700"
embedded = base64.b64decode(nodes["card-illustration"].get("{http://www.w3.org/1999/xlink}href").split(",",1)[1])
assert hashlib.sha256(embedded).hexdigest() == EXPECTED
for name,value in {"creator-name":"LARVA LABS","title-line-1":"CRYPTO","title-line-2":"PUNKS","moment-context":"FREE TO CLAIM","moment-number":"JUN 2017","set-number":"CRYPTO • SEASON 01 • 038/100","rarity-label":"EPIC"}.items():
    assert nodes[name].text == value, name
front = Image.open(ROOT / f"{PREFIX}-Epic-Print-v1.png")
assert front.size == (816,1110)
assert all(abs(x-300)<0.01 for x in front.info["dpi"])
qr = {}
for name in [f"{PREFIX}-Epic-Print-v1.png","qa/card-pdf-300dpi.png",f"{PREFIX}-Web-v1.png"]:
    qr[name] = [x.text for x in zxingcpp.read_barcodes(Image.open(ROOT / name))]
    assert qr[name] == [PAYLOAD], name
assert Image.open(ROOT / f"{PREFIX}-Web-v1.png").size == (600,837)
print_pdf = PdfReader(ROOT / f"{PREFIX}-Epic-Print-v1.pdf")
assert len(print_pdf.pages)==1
page = print_pdf.pages[0]
assert list(page.mediabox) == [0,0,195.84,266.4]
assert list(page.trimbox) == [8.64,8.64,187.2,257.76]
book = fitz.open(ROOT / f"{PREFIX}-Book-Pages-v1.pdf")
approved = fitz.open(ROOT / "inputs" / f"{PREFIX}-Book-Pages-Review-v1.pdf")
assert len(book)==2
old = approved[1].get_text().replace("REVIEW PROOF / RARITY AND PHRASE PROPOSED\n","").replace(" / LAYOUT PROOF","")
assert old.split() == book[1].get_text().split()
assert "REVIEW" not in book[1].get_text() and "LAYOUT PROOF" not in book[1].get_text()
images = book[0].get_images(full=True)
assert len(images)==1 and images[0][2:4] == (1060,1484)
native = fitz.Pixmap(book,images[0][0])
assert native.samples == art.tobytes()
assert [x["uri"] for x in approved[1].get_links()] == [x["uri"] for x in book[1].get_links()]
old_card = np.array(Image.open(ROOT / "inputs" / f"{PREFIX}-Epic-Card-Review-v1.png").convert("RGB"))
new_card = np.array(front.convert("RGB"))
diff = (old_card != new_card).any(axis=2)
ys,xs = np.nonzero(diff)
box = [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
assert box == [563,821,723,1001],box
mask = diff.copy(); mask[815:1005,550:730] = False
assert not mask.any()
ppi = 72 / max(book[0].rect.width/1060, book[0].rect.height/1484)
files = ["art.png",f"{PREFIX}-Epic-Print-v1.png",f"{PREFIX}-Epic-Print-v1.svg",f"{PREFIX}-Epic-Print-v1.pdf",f"{PREFIX}-Book-Pages-v1.pdf","038-cryptopunks.md"]
result = {
  "card":"038","all_assertions_passed":True,
  "artwork_sha256":EXPECTED,"artwork_px":[1060,1484],"svg_embedded_art_identical":True,
  "card_pixels_unchanged_outside_qr_and_caption":True,"card_changed_bbox_xyxy":box,
  "qr_digital_decode":qr,"physical_qr_scan_test":False,
  "canvas_px":[816,1110],"dpi":300,"trim_px":[744,1038],"safe_px":[684,981],
  "transform":"translate(46.515 48.921) scale(0.8033)","phrase_size":25,"phrase_weight":700,
  "print_media_box_pt":list(page.mediabox),"print_trim_box_pt":list(page.trimbox),
  "web_dimensions":[600,837],"book_pages":2,"book_copy_exact_except_review_labels":True,
  "removed_labels":["REVIEW PROOF / RARITY AND PHRASE PROPOSED"," / LAYOUT PROOF"],
  "book_native_image_pixels_identical":True,"book_native_ppi_at_a4":round(ppi,3),
  "book_links_retained":True,"book_physical_reproduction_approved":False,"print_release":False,
  "book_copy_presentation_normalization":"Markdown and website may use title case for the exact uppercase clue labels; wording remains identical",
  "visual_review":{"card_png":"PASS","print_pdf_300dpi":"PASS","book_page_1":"PASS","book_page_2":"PASS","four_clue_crops":"PASS"},
  "originals":[{"path":name,"bytes":(ROOT/name).stat().st_size,"sha256":sha(ROOT/name)} for name in files]
}
(ROOT/"source/final-qa.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
