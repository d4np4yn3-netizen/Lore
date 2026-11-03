#!/usr/bin/env python3
"""Recreate the original X-header source ZIP from its verified archive parts."""
from pathlib import Path
import hashlib
import json
import tempfile
import os

root = Path(__file__).resolve().parent
manifest = json.loads((root / "archive-manifest.json").read_text())
record = next(f for f in manifest["files"] if f["name"] == "HISTROVE-Family-Header-Source-v4.zip")
destination = root / record["name"]

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

if destination.exists():
    if destination.stat().st_size == record["size"] and sha256(destination) == record["sha256"]:
        print(f"Already restored and verified: {destination.name}")
        raise SystemExit(0)
    raise SystemExit("A different output file exists. Move it before running this script.")

for part in record["parts"]:
    path = root / part["path"]
    if path.stat().st_size != part["size"] or sha256(path) != part["sha256"]:
        raise SystemExit(f"Part verification failed: {part['name']}")

temporary = None
try:
    with tempfile.NamedTemporaryFile(dir=root, prefix=".restore-header-", delete=False) as output:
        temporary = Path(output.name)
        for part in record["parts"]:
            with (root / part["path"]).open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    output.write(block)
    if temporary.stat().st_size != record["size"] or sha256(temporary) != record["sha256"]:
        raise SystemExit("Restored ZIP verification failed.")
    os.link(temporary, destination)
    print(f"Restored and SHA-256 verified: {destination.name}")
finally:
    if temporary is not None:
        temporary.unlink(missing_ok=True)
