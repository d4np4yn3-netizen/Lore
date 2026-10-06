"""Export a HISTROVE printer SVG to an outlined-text PDF with exact physical boxes."""
from pathlib import Path
import argparse,subprocess,tempfile,os
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject
p=argparse.ArgumentParser();p.add_argument('svg',type=Path);p.add_argument('pdf',type=Path);a=p.parse_args()
master=Path(__file__).resolve().parents[1];env=os.environ.copy();env['FONTCONFIG_FILE']=str(master.parents[2]/'master/front-v3/source/fontconfig.xml')
if 'id="tagline"' in a.svg.read_text():env.pop('FONTCONFIG_FILE',None)
with tempfile.TemporaryDirectory() as tmp:
 raw=Path(tmp)/'raw.pdf';subprocess.run(['inkscape',str(a.svg),'--export-type=pdf','--export-text-to-path',f'--export-filename={raw}'],env=env,check=True)
 page=PdfReader(raw).pages[0]
 assert abs(float(page.mediabox.width)-195.84)<.01 and abs(float(page.mediabox.height)-266.4)<.01
 page.trimbox=RectangleObject([8.64,8.64,187.2,257.76]);page.bleedbox=RectangleObject([0,0,195.84,266.4]);page.artbox=RectangleObject([15.84,15.48,180,250.92])
 w=PdfWriter();w.add_page(page)
 with a.pdf.open('wb') as f:w.write(f)
