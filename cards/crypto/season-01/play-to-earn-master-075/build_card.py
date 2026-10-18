from pathlib import Path
import json,subprocess,sys
B=Path(__file__).resolve().parent
R=B.parents[3]
d=json.loads((B/'card-data.json').read_text())
d['artwork']=str(B/'art.png')
temp=B/'render-data.local.json'
temp.write_text(json.dumps(d))
try:
 subprocess.run([sys.executable,str(R/'cards/crypto/master/histrove-print-v1/source/render_print_card.py'),'--data',str(temp),'--out',str(B/'HISTROVE-Crypto-075-Front-Print-v1.svg')],check=True)
 subprocess.run([sys.executable,str(R/'cards/crypto/master/histrove-print-v1/source/export_print_pdf.py'),str(B/'HISTROVE-Crypto-075-Front-Print-v1.svg'),str(B/'HISTROVE-Crypto-075-Front-Print-v1.pdf')],check=True)
finally:
 temp.unlink(missing_ok=True)
