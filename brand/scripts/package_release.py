#!/usr/bin/env python3
"""Package only the current brand release, after export QA has passed."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2];B=ROOT/'brand'
m=json.loads((B/'assets/asset-manifest.json').read_text())
assert m['release_status']=='APPROVED_MASTER_AND_DERIVED_EXPORTS'
for e in m['approved_exports']:
 assert hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
archive=B/'downloads/LORE-Brand-Pack-v1.0.zip';archive.parent.mkdir(exist_ok=True)
files=[p for p in B.rglob('*')if p.is_file() and not any(s in p.parts for s in ['downloads','__pycache__']) and p.name!='release.json']
files += [ROOT/'operations/10-BRAND-APPROVAL-04.md',ROOT/'AGENTS.md']
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for p in sorted(files):z.write(p,'LORE-Brand-Pack-v1.0/'+str(p.relative_to(ROOT)))
 z.writestr('LORE-Brand-Pack-v1.0/START-HERE.md','# LORE — approved brand pack\n\nRevision LORE-04-v1.0 / 04 — Rising Strokes.\n\nOpen brand/README.md for the branding page and brand/assets/README.md for the file catalogue.\n\nPNG files are in brand/assets/png and vector SVGs in brand/assets/svg. The brand guide is in brand/previews. The approved component source, export scripts, hashes and QA records are included. The five social/app PNGs intentionally have backgrounds; all other core PNGs use transparency.\n')
with zipfile.ZipFile(archive)as z:assert z.testzip() is None
paths=[archive,B/'previews/LORE-Brand-Guide.png',B/'previews/LORE-Brand-Guide.svg',B/'assets/asset-manifest.json',B/'source/master-components.json',B/'qa/technical-qa.json']
release={'revision':m['revision'],'date':'2026-09-11','design_count':28,'png_count':28,'svg_count':28,'approved_export_count':56,'approval_record':m['approval_record'],'files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'byte_count':p.stat().st_size}for p in paths]}
(B/'release.json').write_text(json.dumps(release,indent=2)+'\n')
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'pack_files':len(files)+1,'approved_assets':len(m['approved_exports'])}))
