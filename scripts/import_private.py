#!/usr/bin/env python3
"""Restore an owned local project into an ignored, separate preview directory."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('original_project',type=Path)
args=parser.parse_args()
source=args.original_project.resolve()
dest=root/'.private-preview'
manifest=json.loads((root/'config/private-runtime.json').read_text())
if dest.exists():
    raise SystemExit('Private preview already exists. Preserve its edits or choose a fresh checkout.')
# Validate every file before copying any material.
for name,expected in manifest.items():
    p=source/name
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        raise SystemExit('Original snapshot mismatch: '+name)
files=set(manifest)|{'meta.json','hyperframes.json','hyperframes.lock.json'}
for name in manifest:
    files.update(re.findall(r'assets/[\w./-]+',(source/name).read_text()))
missing=[name for name in files if not (source/name).is_file()]
if missing:
    raise SystemExit('Missing original resources: '+', '.join(sorted(missing)))
for name in sorted(files):
    target=dest/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/name,target)
(dest/'meta.json').write_text(json.dumps({'id':'kaguya-pv-private','name':'星降る海 · 本地完整归档'},ensure_ascii=False))
print(f'Restored {len(files)} files to .private-preview/; public sources remain unchanged.')
