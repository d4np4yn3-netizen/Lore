"""Apply Dan's approved LORE badge spacing using pinned visible-glyph metrics.

All dimensions use the 900 x 1260 card master. Font and tracking are fixed;
metrics are measured from the actual Inkscape glyph bounds, not letter counts.
"""
from pathlib import Path
import json

MASTER = Path(__file__).resolve().parents[1]
SPEC = json.loads((MASTER / 'badge-spacing.json').read_text())
METRICS = {row['rarity']: row for row in SPEC['measurements']}


def badge_nodes(root):
    label = next(n for n in root.iter() if n.get('id') == 'rarity-label')
    boxes = [n for n in root.iter() if n.tag.endswith('rect')
             and n.get('x') == '50' and n.get('y') == '49'
             and n.get('height') == '47']
    if len(boxes) != 1:
        raise ValueError('Expected exactly one pinned rarity badge rectangle.')
    return boxes[0], label


def apply_badge_spacing(root, rarity):
    box, label = badge_nodes(root)
    name = rarity.upper()
    if name not in METRICS or label.text != name:
        raise ValueError('Rarity must match one of the six approved labels.')
    fixed = {'font-family': 'DejaVu Sans', 'font-size': '25',
             'font-weight': '700', 'letter-spacing': '3', 'text-anchor': 'start'}
    if any(label.get(key) != value for key, value in fixed.items()):
        raise ValueError('Badge lettering differs from the approved font/spacing.')
    if box.get('rx') != '5' or box.get('stroke-width') != '1.5':
        raise ValueError('Badge border differs from the approved geometry.')
    m = METRICS[name]
    box.set('width', f"{m['proposed_box_width']:.4f}")
    label.set('x', f"{m['proposed_text_x']:.4f}")
    label.set('y', f"{m['proposed_text_baseline']:.4f}")
    return root
