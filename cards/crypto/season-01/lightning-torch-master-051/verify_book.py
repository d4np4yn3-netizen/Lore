"""Verify the frozen 051 book, website content and native detail crops."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import fitz
from PIL import Image, ImageChops

B = Path(__file__).resolve().parent
PDF_NAME = 'HISTROVE-051-Lightning-Torch-Book.pdf'
PREVIEW_NAME = 'HISTROVE-051-Lightning-Torch-Book-Spread.png'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

qa = json.loads((B/'book-qa.json').read_text())
authoring = json.loads((B/'authoring-content.json').read_text())
content = json.loads((B/'051.json').read_text())
assert content['story'] == authoring['story']
assert content['eggs'] == authoring['eggs']
assert content['sources'] == authoring['sources']
assert len(authoring['story']) == 5 and len(authoring['eggs']) == 4
assert '100,000' in ' '.join(authoring['story'])
assert '10,000' in ' '.join(authoring['story'])
assert 'exceptions' in ' '.join(authoring['story'])
assert 'Portofino-inspired' in authoring['art_note']

art = Image.open(B/'art.png').convert('RGB')
provenance = json.loads((B/'art-provenance.json').read_text())
assert sha(B/'art.png') == provenance['sha256'] == qa['source_art_sha256']
assert art.size == (1060,1484)
doc = fitz.open(B/PDF_NAME)
assert len(doc) == 2
assert all(abs(p.rect.width-595.2755905511812)<.001 and abs(p.rect.height-841.8897637795277)<.001 for p in doc)
images=doc[0].get_images(full=True)
assert len(images)==1
embedded=fitz.Pixmap(doc,images[0][0])
assert (embedded.width,embedded.height) == art.size
assert embedded.samples == art.tobytes()

text=doc[1].get_text()
for required in ['LIGHTNING TORCH','051 / 19 JAN 2019 / BITCOIN / COMMON','PASS IT ON.','102','THE DATE TAG','THE STARTING RECEIPT','THE TRAVEL SATCHEL','THE LANTERN INCREMENT']:
    assert required in text,required
assert not any(x in text for x in ['QUADRIGACX','PINEAPPLE','052 /','050 /'])
assert 'PASS IT ON.\n' in text
for page in doc:
    for block in page.get_text('dict')['blocks']:
        if block['type']==0:
            for line in block['lines']:
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    assert min(x0,y0)>=0 and x1<=page.rect.width and y1<=page.rect.height,span
links={x['uri'] for x in doc[1].get_links() if 'uri' in x}
assert links == {s['url'] for s in authoring['sources']},links

crops=json.loads((B/'closeup-boxes.json').read_text())
assert crops['source_dimensions']==list(art.size)
assert crops['titles']==[e['title'] for e in authoring['eggs']]
checks=[]
for n,box in enumerate(crops['boxes'],1):
    assert 0<=box[0]<box[2]<=art.width and 0<=box[1]<box[3]<=art.height
    p=B/'closeups'/f'051-detail-{n}.png'
    crop=Image.open(p).convert('RGB')
    assert ImageChops.difference(crop,art.crop(box)).getbbox() is None
    checks.append({'path':str(p.relative_to(B)),'box':box,'dimensions':list(crop.size),'sha256':sha(p),'exact_native_pixel_crop':True})

render_names=['book-page-1.png','book-page-2.png',PREVIEW_NAME]
for i,name in enumerate(render_names[:2]):
    expected=doc[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
    found=Image.open(B/name).convert('RGB')
    assert expected.samples==found.tobytes()
spread=Image.open(B/PREVIEW_NAME).convert('RGB')
a=Image.open(B/render_names[0]).convert('RGB')
b=Image.open(B/render_names[1]).convert('RGB')
assert spread.size==(a.width+b.width,a.height)
assert ImageChops.difference(spread.crop((0,0,a.width,a.height)),a).getbbox() is None
assert ImageChops.difference(spread.crop((a.width,0,a.width+b.width,b.height)),b).getbbox() is None

with tempfile.TemporaryDirectory(prefix='.book-verify-',dir=B) as d:
    t=Path(d)
    for name in ['art.png','art-provenance.json','authoring-content.json','build_book.py']:
        shutil.copy2(B/name,t/name)
    shutil.copytree(B/'source/fonts',t/'source/fonts')
    subprocess.run([sys.executable,str(t/'build_book.py')],check=True,capture_output=True,text=True)
    for name in [PDF_NAME,PREVIEW_NAME,*render_names[:2],'051.json','051-lightning-torch.md','closeup-boxes.json','sources.json']:
        assert sha(B/name)==sha(t/name),name
    for n in range(1,5):
        name=f'closeups/051-detail-{n}.png'
        assert sha(B/name)==sha(t/name),name

for name in ['authoring-content.json','051.json','051-lightning-torch.md','sources.json','source-notes.md','README.md']:
    s=(B/name).read_text()
    for prohibited in ['libfile_', '/workspace/']:
        assert prohibited not in s,(name,prohibited)
qa.update({
    'embedded_art_pixels_match_original':True,
    'closeups_are_exact_native_pixel_crops':True,
    'all_pdf_text_within_page_bounds':True,
    'unique_linked_sources':len(links),
    'required_text_verified':True,
    'exact_card_phrase_with_period_verified':True,
    'build_deterministic':True,
    'portable_build_from_bundled_inputs_verified':True,
    'portable_rebuild_pdf_sha256_matched':True,
    'expected_final_page_number':'102',
    'crop_checks':checks,
    'story_and_clues_shared_with_site_content':True,
    'render_sha256':{name:sha(B/name) for name in render_names},
    'notes':[
        'A4 format and approximately 128.21 native effective PPI are preserved; no resolution upgrade is claimed.',
        'January 19, 2019 marks the start. April 11 and the relay totals are attributed to CoinGecko.',
        'The 10,000-satoshi increment was requested; the account explicitly acknowledges exceptions.',
        'Portofino-inspired harbour, people, lantern, satchel and boat are fictional imagery, not a documented journey.',
        'PASS IT ON. is an editorial caption, not an attributed historical quotation.'
    ]
})
(B/'book-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({'result':'PASS','pdf_sha256':sha(B/PDF_NAME),'source_art_sha256':sha(B/'art.png'),'page_count':len(doc),'linked_sources':len(links),'native_effective_ppi':qa['native_effective_ppi'],'portable_rebuild':'PASS'},indent=2))
