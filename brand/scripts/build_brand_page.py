#!/usr/bin/env python3
"""Compose the brand guide from exact approved vector assets."""
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
from build_assets import render

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'brand/previews'
OUT.mkdir(exist_ok=True)
PARTS = []
N = '{http://www.w3.org/2000/svg}'


def rect(x, y, w, h, fill, radius=0, stroke='none'):
    PARTS.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')


def text(x, y, value, size=25, fill='#F5F2EB', weight='normal', tracking=0):
    PARTS.append(f'<text x="{x}" y="{y}" fill="{fill}" font-family="Nimbus Sans,Arial,sans-serif" '
                 f'font-size="{size}" font-weight="{weight}" letter-spacing="{tracking}">{escape(value)}</text>')


def asset(name, x, y, w, h):
    root = ET.parse(ROOT/'brand/assets/svg'/f'{name}.svg').getroot()
    _, _, iw, ih = map(float, root.get('viewBox').split())
    scale = min(w/iw, h/ih)
    body = ''.join(ET.tostring(c, encoding='unicode') for c in root if c.tag not in [N+'title', N+'desc'])
    PARTS.append(f'<g transform="translate({x+(w-iw*scale)/2} {y+(h-ih*scale)/2}) scale({scale})">{body}</g>')


def section(y, number, label):
    rect(90, y-34, 1820, 1, '#37352B')
    text(90, y+10, number+' / '+label, 24, '#D4AF37', 'bold', 2)


rect(0, 0, 2000, 2790, '#0B0B0B')
text(90, 83, 'LORE / BRAND IDENTITY', 26, '#D4AF37', 'bold', 3)
text(1415, 83, '04 / RISING STROKES', 22, '#F5F2EB', 'normal', 2)
asset('lore_logo_primary_gold_white', 65, 135, 1020, 660)
text(1155, 302, 'ICONS ARE', 64, '#F5F2EB', 'bold')
text(1155, 381, 'MADE OF', 64, '#F5F2EB', 'bold')
text(1155, 460, 'MOMENTS.', 64, '#F5F2EB', 'bold')
rect(1155, 509, 90, 4, '#D4AF37')
for i, line in enumerate(['Defining moments from internet culture,', 'reimagined as premium collectible cards.', '', 'Six genuine moments. Six rarity tiers.', 'One creator collection.']):
    text(1155, 568+i*38, line, 25, '#AFAFA7')

section(850, '01', 'THE LOGO')
for i, (name, bg, label, sub, fg) in enumerate([
    ('lore_logo_compact_white', '#1A1A1A', 'WHITE', 'For dark backgrounds', '#F5F2EB'),
    ('lore_logo_compact_black', '#F5F2EB', 'BLACK', 'For light backgrounds', '#0B0B0B'),
    ('lore_logo_compact_gold_black', '#F5F2EB', 'GOLD + BLACK', 'Gold crown with black lettering', '#0B0B0B')]):
    x=90+i*620
    rect(x, 910, 580, 395, bg, 12)
    asset(name, x+35, 925, 510, 355)
    text(x, 1352, label, 23, '#F5F2EB', 'bold', 1)
    text(x, 1387, sub, 22, '#AFAFA7')

section(1470, '02', 'THE SIGNATURE CROWN')
for i, (name, bg, label) in enumerate([
    ('lore_crown_gold', '#1A1A1A', 'GOLD / #D4AF37'),
    ('lore_crown_white', '#1A1A1A', 'WHITE / #FFFFFF'),
    ('lore_crown_black', '#F5F2EB', 'BLACK / #000000')]):
    x=90+i*620
    rect(x, 1520, 580, 300, bg, 12)
    asset(name, x+155, 1532, 270, 270)
    text(x, 1865, label, 23, '#F5F2EB', 'bold', 1)
text(90, 1910, 'One crown silhouette. Flat colour. The approved spacing is built into each logo.', 25, '#AFAFA7')

section(1990, '03', 'THE PALETTE')
for i, (name, code) in enumerate([('OBSIDIAN', '#0B0B0B'), ('BONE', '#F5F2EB'), ('GOLD', '#D4AF37'), ('CHARCOAL', '#1A1A1A')]):
    x=90+i*465
    rect(x, 2050, 425, 88, code, 8, '#45453B')
    text(x, 2180, name, 22, '#F5F2EB', 'bold', 1)
    text(x+280, 2180, code, 22, '#AFAFA7')

section(2270, '04', 'THE LANGUAGE')
text(90, 2338, 'MASTER TAGLINE', 20, '#D4AF37', 'bold', 1)
text(90, 2385, 'COLLECT THE INTERNET.', 33, '#F5F2EB', 'normal', 2)
text(90, 2450, 'SIX-CARD COLLECTION LINE', 20, '#D4AF37', 'bold', 1)
text(90, 2497, 'SIX MOMENTS. ONE ICON.', 33, '#F5F2EB', 'normal', 2)
text(1060, 2338, 'SOCIAL & APP', 20, '#D4AF37', 'bold', 1)
for i, name in enumerate(['lore_avatar_gold_dark', 'lore_avatar_black_light', 'lore_app_icon_dark']):
    asset(name, 1060+i*280, 2370, 210, 210)
rect(90, 2652, 1820, 1, '#37352B')
text(90, 2710, 'APPROVED MASTER / LORE-04-v1.0', 21, '#D4AF37', 'bold', 1)
text(1115, 2710, '11 SEPTEMBER 2026 / PNG + SVG', 21, '#AFAFA7', 'normal', 1)

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="2790" viewBox="0 0 2000 2790"><title>LORE Brand Guide — approved Rising Strokes identity</title>' + ''.join(PARTS) + '</svg>'
path=OUT/'LORE-Brand-Guide.svg';path.write_text(svg)
render(path, OUT/'LORE-Brand-Guide.png', 2400)
print('Updated brand guide composed from approved SVG assets.')
