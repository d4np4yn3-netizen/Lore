"""Static verification for LORE-CRYPTO-PRINT-v1.0 templates."""
from pathlib import Path
import xml.etree.ElementTree as ET

MASTER=Path(__file__).resolve().parents[1]
RARITIES=['common','uncommon','rare','epic','legendary','mythic']

for rarity in RARITIES:
    p=MASTER/'templates'/f'{rarity}.svg'
    root=ET.parse(p).getroot()
    assert root.get('width')=='816'
    assert root.get('height')=='1110'
    assert root.get('viewBox')=='0 0 816 1110'
    by_id={n.get('id'):n for n in root.iter() if n.get('id')}
    phrase=by_id['moment-context']
    assert phrase.get('font-size')=='25'
    assert phrase.get('font-weight')=='700'
    assert phrase.get('letter-spacing')=='1.1'
    group=by_id['locked-crypto-front']
    assert group.get('transform')=='translate(46.515 48.921) scale(0.8033)'
    cut=by_id['cut-line']
    assert (cut.get('x'),cut.get('y'),cut.get('width'),cut.get('height'))==('36','36','744','1038')
    safe=by_id['safe-area']
    assert (safe.get('x'),safe.get('y'),safe.get('width'),safe.get('height'))==('66','64.5','684','981')

print('LORE-CRYPTO-PRINT-v1.0: six templates verified')
