#!/usr/bin/env python3
import os, re
R2 = "https://pub-6509346c2fdc47328b748c024f30f006.r2.dev"
SKIP = ('.git', '.vercel', '.venv-r2')
EXT = ('.jpg','.png','.jpeg','.gif','.webp','.svg','.ico')
left_local = 0
r2_refs = set()
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        if not f.endswith(('.html','.css')): continue
        p = os.path.join(d,f)
        h = open(p,encoding='utf-8',errors='replace').read()
        for m in re.finditer(r'(?:src|href|content)="([^"]+)"', h):
            v = m.group(1)
            if v.startswith(R2+'/'): r2_refs.add(v[len(R2)+1:].split('?')[0])
            elif v.lower().endswith(EXT) and not v.startswith(('http','data:','#')):
                left_local += 1
        for m in re.finditer(r'url\((["\']?)([^"\')]+)\1\)', h):
            v = m.group(2)
            if v.startswith(R2+'/'): r2_refs.add(v[len(R2)+1:].split('?')[0])
            elif v.lower().endswith(EXT) and not v.startswith(('http','data:')):
                left_local += 1
print(f"remaining local img refs: {left_local}")
print(f"unique R2 keys referenced: {len(r2_refs)}")
missing = [k for k in r2_refs if not os.path.exists(k)]
print(f"referenced keys missing on disk: {len(missing)}", missing[:5])
