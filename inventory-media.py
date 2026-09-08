#!/usr/bin/env python3
"""Inventory: on-disk font/video files vs referenced, with resolved paths."""
import os, re, urllib.parse
SKIP = ('.git','.vercel','.venv-r2')
FONT_EXT = ('woff','woff2','ttf','eot')
MEDIA_EXT = ('mp4','m4v','mov','webm')

# 1. on-disk media/font files (relative paths, no leading ./)
on_disk = {}
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        ext = f.rsplit('.',1)[-1].lower() if '.' in f else ''
        if ext in FONT_EXT or ext in MEDIA_EXT:
            p = os.path.join(d,f).lstrip('./')
            on_disk[p] = os.path.getsize(os.path.join(d,f))

print(f"on-disk media/font files: {len(on_disk)}, total {sum(on_disk.values())/1024:.0f} KB")
for p,s in sorted(on_disk.items()):
    print(f"  {s/1024:6.1f} KB  {p}")

# 2. referenced url() with media/font ext across css+html, resolve relative to each file
refs = {}  # resolved_rel_path -> set of (ref_file, raw)
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        if not f.endswith(('.css','.html')): continue
        p = os.path.join(d,f)
        h = open(p,encoding='utf-8',errors='replace').read()
        for m in re.finditer(r'url\(\s*[\'"]?([^\'")]+?)[\'"]?\s*\)', h):
            raw = m.group(1).strip()
            if raw.startswith(('data:','http:','https:','//')): continue
            # strip ?query and #frag
            pathpart = raw.split('?')[0].split('#')[0]
            ext = pathpart.rsplit('.',1)[-1].lower() if '.' in pathpart else ''
            if ext not in FONT_EXT and ext not in MEDIA_EXT: continue
            # resolve relative to the referencing file's directory
            basedir = os.path.dirname(p)
            resolved = os.path.normpath(os.path.join(basedir, pathpart)).lstrip('./')
            refs.setdefault(resolved, set()).add((p, raw))

print(f"\nreferenced media/font paths: {len(refs)}")
missing = {r for r in refs if r not in on_disk}
present = {r for r in refs if r in on_disk}
print(f"  present on disk: {len(present)}")
print(f"  MISSING (never downloaded): {len(missing)}")
for r in sorted(missing):
    files = refs[r]
    print(f"    MISSING {r}  (from {len(files)} refs, e.g. {list(files)[0][0]})")
