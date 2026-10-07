#!/usr/bin/env python3
"""Reproduce HISTROVE Crypto 047 from exact corrected artwork and locked master.

Run with --repo-root PATH --data PATH --out-dir PATH. Templates and fonts are
hash-pinned and never modified. This card uses both unchanged title lines.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,subprocess,sys
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 here=Path(__file__).resolve().parent
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--repo-root',type=Path)
 p.add_argument('--data',type=Path,default=here.parent/'card-data.json')
 p.add_argument('--out-dir',type=Path,default=here)
 a=p.parse_args()
 master_rel=Path('cards/crypto/master/histrove-print-v1')
 root=a.repo_root.resolve() if a.repo_root else next((d for d in [here,*here.parents] if (d/master_rel/'templates/rare.svg').is_file()),None)
 if root is None:raise SystemExit('Supply --repo-root for the locked repository.')
 lock=json.loads((here/'source-lock.json').read_text())
 for relative,expected in lock['files'].items():
  if sha(root/relative)!=expected:raise SystemExit('Pinned source changed: '+relative)
 data_path=a.data.resolve();data=json.loads(data_path.read_text())
 art=Path(data['artwork']);art=art if art.is_absolute() else (data_path.parent/art).resolve()
 if sha(art)!=lock['artwork_sha256']:raise SystemExit('Artwork differs from approved corrected source.')
 if list(Image.open(art).size)!=lock['artwork_native_px']:raise SystemExit('Native artwork dimensions changed.')
 expected={'rarity':'rare','creator':'MAKERDAO','title_line_1':'DAI','title_line_2':'GOES LIVE','context':'DAI IS NOW LIVE!','moment_label':'18 DEC 2017','set_label':'CRYPTO • SEASON 01 • 047/100','qr_url':'https://lore-site-v1.vercel.app/crypto/047/'}
 for key,value in expected.items():
  if data.get(key)!=value:raise SystemExit('Approved field changed: '+key)
 data['artwork']=str(art);data['confirmed_lore_owned_route']=True
 master=root/master_rel
 spec=importlib.util.spec_from_file_location('histrove_renderer',master/'source/render_print_card.py')
 renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
 a.out_dir.mkdir(parents=True,exist_ok=True)
 out=a.out_dir/'HISTROVE-Crypto-047-Front-Print-v1.svg';renderer.render(data,out)
 pdf=out.with_suffix('.pdf')
 subprocess.run([sys.executable,str(master/'source/export_print_pdf.py'),str(out),str(pdf)],check=True)
 page=PdfReader(pdf).pages[0]
 page.mediabox=RectangleObject([0,0,195.84,266.4]);page.cropbox=RectangleObject([0,0,195.84,266.4])
 w=PdfWriter();w.add_page(page)
 with pdf.open('wb') as f:w.write(f)
 with Image.open(out.with_suffix('.png')) as im:im.crop((36,36,780,1074)).save(a.out_dir/'HISTROVE-Crypto-047-Front-Web-v1.png')
 print(json.dumps({'artwork_sha256':sha(art),'files':[{'name':f.name,'sha256':sha(f)} for f in sorted(a.out_dir.glob('HISTROVE-Crypto-047-*'))]}))

if __name__=='__main__':main()

