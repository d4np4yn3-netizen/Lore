"""Non-mutating technical checks for the finished 091 book and actual-art details."""
from pathlib import Path
import hashlib
import json
import fitz
from PIL import Image, ImageChops

B = Path(__file__).resolve().parent
pdf = B / 'HISTROVE-091-Spot-Bitcoin-ETFs-Approved-Book.pdf'
art = Image.open(B / 'art.png').convert('RGB')
doc = fitz.open(pdf)
assert len(doc) == 2
assert all(abs(p.rect.width - 595.2755905511812) < 0.001 and abs(p.rect.height - 841.8897637795277) < 0.001 for p in doc)
images = doc[0].get_images(full=True)
assert len(images) == 1
pix = fitz.Pixmap(doc, images[0][0])
embedded = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
assert embedded.size == art.size
assert ImageChops.difference(embedded, art).getbbox() is None
crops = json.loads((B / 'closeup-boxes.json').read_text())
assert crops['source_dimensions'] == list(art.size)
assert len(crops['boxes']) == 4
for i, box in enumerate(crops['boxes'], 1):
    crop = Image.open(B / f'closeups/091-detail-{i}.png').convert('RGB')
    assert ImageChops.difference(art.crop(box), crop).getbbox() is None
text = doc[1].get_text()
for snippet in ['SPOT BITCOIN ETFS APPROVED', 'FINALLY.', '34-99306', 'LEGENDARY', '182', 'Percival Kestreltail']:
    assert snippet in text, snippet
assert '090 /' not in text
for block in doc[1].get_text('dict')['blocks']:
    for line in block.get('lines', []):
        for span in line['spans']:
            x0, y0, x1, y1 = span['bbox']
            assert 0 <= x0 < x1 <= doc[1].rect.width and 0 <= y0 < y1 <= doc[1].rect.height, span
expected_urls = {s['url'] for s in json.loads((B / 'sources.json').read_text())}
actual_urls = {link.get('uri') for link in doc[1].get_links()}
assert expected_urls <= actual_urls, expected_urls - actual_urls
print(json.dumps({
    'page_count': 2,
    'embedded_art_pixel_exact': True,
    'four_crops_pixel_exact': True,
    'all_text_bounds_inside_pages': True,
    'all_source_urls_linked': True,
    'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
    'art_sha256': hashlib.sha256((B / 'art.png').read_bytes()).hexdigest()
}, indent=2))
