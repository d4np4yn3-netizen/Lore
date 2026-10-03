"""Rebuild the printer PDF from the unchanged approved 816x1110 PNG.

Run with ReportLab and pypdf installed. The canonical SVG/PNG are created by
cards/crypto/master/print-v1/source/render_print_card.py using card-data.json.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

HERE=Path(__file__).resolve().parent
BASE=HERE/'LORE-Crypto-022-Buried-Fortune-Rare-Print-v1'
with TemporaryDirectory() as temp:
    intermediate=Path(temp)/'front.pdf'
    c=canvas.Canvas(str(intermediate),pagesize=(195.84,266.4),pageCompression=1,invariant=1)
    c.setTitle('LORE Crypto 022 Buried Fortune Rare Print v1')
    c.setAuthor('LORE')
    c.drawImage(str(BASE.with_suffix('.png')),0,0,width=195.84,height=266.4)
    c.showPage();c.save()
    reader=PdfReader(intermediate);writer=PdfWriter();writer.add_page(reader.pages[0])
    writer.pages[0].trimbox=RectangleObject([8.64,8.64,187.2,257.76])
    writer.add_metadata({'/Title':'LORE Crypto 022 Buried Fortune Rare Print v1','/Author':'LORE'})
    with BASE.with_suffix('.pdf').open('wb') as output:
        writer.write(output)
print(BASE.with_suffix('.pdf'))
