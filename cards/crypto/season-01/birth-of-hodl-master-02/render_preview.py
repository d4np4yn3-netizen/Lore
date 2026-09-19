from pathlib import Path
import argparse,json,sys
root=Path(__file__).resolve().parent
master=root.parents[2]/'master/front-v4'
sys.path.insert(0,str(master/'source'))
import render_card
p=argparse.ArgumentParser(description='Render an independent preview using the pinned LORE template.')
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
if a.out.resolve() in [root/'LORE-Birth-of-HODL-Epic-v2.svg',root/'LORE-Birth-of-HODL-Epic-v2.png']:
 raise ValueError('Preserve approved exports; choose a separate output path.')
data=json.loads((root/'card-data.json').read_text())
data['artwork']=str(root/'art.png')
render_card.render(data,a.out,demo=True)
