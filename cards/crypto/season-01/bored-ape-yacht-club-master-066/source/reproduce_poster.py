"""Reproduce the approved direct-source poster composite from packaged inputs.

Writes a separate rebuilt-art.png beside this script and requires exact output
hash equality. The approved art.png is never overwritten.
"""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image, ImageDraw

B = Path(__file__).resolve().parent
target = Image.open(B / 'original-raw-v1.png').convert('RGB')
crop = Image.open(B / 'approved-038-portrait-source-crop.png').convert('RGB')
width, height = 280, 400
flat = Image.new('RGB', (width, height), (67, 58, 66))
ratio = min(width / crop.width, height / crop.height)
scaled = crop.resize((round(crop.width * ratio), round(crop.height * ratio)), Image.Resampling.LANCZOS)
flat.paste(scaled, ((width - scaled.width) // 2, (height - scaled.height) // 2))
quad = [(719, 151), (782, 148), (776, 241), (712, 243)]
corners = [(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)]
matrix, values = [], []
for (x, y), (u, v) in zip(quad, corners):
    matrix.append([x, y, 1, 0, 0, 0, -u*x, -u*y])
    values.append(u)
    matrix.append([0, 0, 0, x, y, 1, -v*x, -v*y])
    values.append(v)
coefficients = np.linalg.solve(np.array(matrix, float), np.array(values, float))
warped = flat.transform(target.size, Image.Transform.PERSPECTIVE, coefficients, Image.Resampling.BICUBIC)
mask = Image.new('L', target.size, 0)
ImageDraw.Draw(mask).polygon(quad, fill=255)
result = target.copy()
result.paste(warped, (0, 0), mask)
changed = np.any(np.asarray(target) != np.asarray(result), axis=2)
assert np.count_nonzero(changed & (np.asarray(mask) == 0)) == 0
out = B / 'rebuilt-art.png'
result.save(out)
assert hashlib.sha256(out.read_bytes()).hexdigest() == '8bde272b72eb06276bcec1420b5868f51e4d0fbef9fce40d2fc93cbb8c409cee'
print('Poster composite reproduced exactly; zero changed pixels outside poster polygon.')
