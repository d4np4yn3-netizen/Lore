"""Check the approved 032 source assets and digitally decode the final QR."""
from pathlib import Path
import base64,hashlib,json,subprocess,tempfile,xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
import zxingcpp
M=Path(__file__).resolve().parent.parent
REPO=M.parents[3]
ART=M/'art.png';OUT=M/'LORE-Crypto-032-Ethereum-Goes-Live-Mythic-Print-v1'
BOOK=REPO/'book/crypto-season-01/proofs/032-ethereum-goes-live-full-art-spread-v1.pdf'
SHA='5db2bd45176367f74c595925fecb3d537b5a493966ca02850178903563422ef0'
URL='https://lore-site-v1.vercel.app/crypto/032/'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(ART)==SHA
r=ET.parse(OUT.with_suffix('.svg')).getroot();nodes={n.get('id'):n for n in r.iter() if n.get('id')}
embed=base64.b64decode(nodes['card-illustration'].get('{http://www.w3.org/1999/xlink}href').split(',',1)[1]);assert hashlib.sha256(embed).hexdigest()==SHA
assert nodes['locked-crypto-front'].get('transform')=='translate(46.515 48.921) scale(0.8033)'
assert nodes['moment-context'].get('font-size')=='25' and nodes['moment-context'].get('font-weight')=='700'
with Image.open(OUT.with_suffix('.png')) as im:
 assert im.size==(816,1110) and im.info['dpi'][0]>299.5
 assert any(code.text==URL for code in zxingcpp.read_barcodes(im))
pdf=PdfReader(OUT.with_suffix('.pdf'));assert len(pdf.pages)==1
assert list(map(float,pdf.pages[0].mediabox))==[0,0,195.84,266.4]
assert list(map(float,pdf.pages[0].trimbox))==[8.64,8.64,187.2,257.76]
with tempfile.TemporaryDirectory(prefix='lore-032-qr-') as tmp:
 prefix=Path(tmp)/'proof';subprocess.run(['pdftoppm','-r','300','-png','-singlefile',str(OUT.with_suffix('.pdf')),str(prefix)],check=True)
 assert any(code.text==URL for code in zxingcpp.read_barcodes(Image.open(prefix.with_suffix('.png'))))
book=PdfReader(BOOK);assert len(book.pages)==2
text=book.pages[1].extract_text()
assert 'PROPOSED' not in text and 'REVIEW PROOF' not in text
for s in ['THE WORLD COMPUTER WAKES','MYTHIC','Frontier','5,000']:assert s in text
original=Image.open(ART).convert('RGB');im=book.pages[0].images[0].image.convert('RGB');assert original.size==im.size and original.tobytes()==im.tobytes()
copy=json.loads((REPO/'site/app/cards/content/032.json').read_text());assert len(copy['story'])==len(copy['eggs'])==4
qa={'status':'DIGITAL_QA_PASSED_LIVE_VERIFICATION_PENDING','art_sha256':SHA,'art_bytes_unchanged':True,'svg_embedded_art_exact':True,'book_embedded_art_pixels_exact':True,'card_canvas_px':[816,1110],'trim_px':[744,1038],'safe_px':[684,981],'dpi':300,'qr_url':URL,'png_qr_decoded':True,'pdf_300dpi_qr_decoded':True,'book_pages':2,'book_source_art_px':[1060,1484],'book_effective_ppi':126.91,'visual_checks':{'front':'PASS: four unique clues and all three GAS bands visible; exact logo and title geometry retained','book_art':'PASS: approved full-art layout unchanged','book_story':'PASS: approved story and details unchanged; proposal/review labels removed'},'caption':'Approved editorial caption, not historical quotation','proof_to_final_change':'Card differs only in QR rectangle/caption; book differs only in proposal/review labels and metadata','print_release':False,'physical_qr_scan_test':False,'book_reproduction_release':False}
(M/'publication-assets-qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
