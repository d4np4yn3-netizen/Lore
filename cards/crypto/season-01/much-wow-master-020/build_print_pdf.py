from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject

b=Path(__file__).resolve().parent
png=b/'LORE-Much-Wow-Epic-020-Print-v1.png'
pdf=png.with_suffix('.pdf')
scale=72/300
w,h=816*scale,1110*scale
buffer=BytesIO();c=canvas.Canvas(buffer,pagesize=(w,h),pageCompression=1)
c.setTitle('LORE MUCH WOW - Epic 020 - 300 DPI printer front')
c.setAuthor('LORE');c.drawImage(str(png),0,0,width=w,height=h);c.showPage();c.save()
reader=PdfReader(BytesIO(buffer.getvalue()));writer=PdfWriter();writer.clone_document_from_reader(reader)
page=writer.pages[0]
page.bleedbox=RectangleObject([0,0,w,h])
page.trimbox=RectangleObject([36*scale,36*scale,(816-36)*scale,(1110-36)*scale])
with pdf.open('wb') as f:writer.write(f)
print(str(pdf))
