#!/usr/bin/env python3
"""Rebuild approved HISTROVE Crypto 048 using its exact art and pinned print master."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,subprocess,sys
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 here=Path(__file__).resolve().parent;p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo-root',type=Path,required=True);p.add_argument('--data',type=Path,default=here.parent/'card-data.json');p.add_argument('--out-dir',type=Path,default=here.parent);a=p.parse_args();root=a.repo_root.resolve();lock=json.loads((here/'source-lock.json').read_text())
 for name,expected in lock['files'].items():assert sha(root/name)==expected,'Pinned source changed: '+name
 dpath=a.data.resolve();data=json.loads(dpath.read_text());art=Path(data['artwork']);art=art if art.is_absolute() else dpath.parent/art
 assert sha(art)=='40f90c2493495e519f4c53d2333dbfb37aa13b5c7e0e49efd1b2df1a78fbd662','Approved art changed';assert Image.open(art).size==(1060,1484)
 expected={'rarity':'uncommon','creator':'BITCOIN','title_line_1':'LIGHTNING','title_line_2':'GOES LIVE','context':'THE VERY BEGINNING.','moment_label':'15 MAR 2018','set_label':'CRYPTO • SEASON 01 • 048/100','qr_url':'https://lore-site-v1.vercel.app/crypto/048/'}
 for k,v in expected.items():assert data[k]==v,'Approved field changed: '+k
 data['artwork']=str(art);data['confirmed_lore_owned_route']=True;master=root/'cards/crypto/master/histrove-print-v1';s=importlib.util.spec_from_file_location('renderer',master/'source/render_print_card.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);a.out_dir.mkdir(parents=True,exist_ok=True);svg=a.out_dir/'HISTROVE-Crypto-048-Front-Print-v1.svg';m.render(data,svg);pdf=svg.with_suffix('.pdf');subprocess.run([sys.executable,str(master/'source/export_print_pdf.py'),str(svg),str(pdf)],check=True)
 page=PdfReader(pdf).pages[0];page.mediabox=RectangleObject([0,0,195.84,266.4]);page.cropbox=RectangleObject([0,0,195.84,266.4]);w=PdfWriter();w.add_page(page);w.add_metadata({'/Title':'HISTROVE 048 Lightning Goes Live','/Subject':'Approved card illustration and layout, 8 October 2026. Digital publication authorized. Physical printing approval remains separate.'})
 with pdf.open('wb') as f:w.write(f)
 with Image.open(svg.with_suffix('.png')) as im:im.crop((36,36,780,1074)).save(a.out_dir/'HISTROVE-Crypto-048-Front-Web-v1.png',dpi=(300,300))
 print(json.dumps({'source_art_sha256':sha(art),'files':[str(f) for f in a.out_dir.glob('HISTROVE-*')]}))
if __name__=='__main__':main()
