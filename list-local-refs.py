#!/usr/bin/env python3
import os, re
SKIP = ('.git', '.vercel', '.venv-r2')
EXT = ('.jpg','.png','.jpeg','.gif','.webp','.svg','.ico')
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        if not f.endswith(('.html','.css')): continue
        p = os.path.join(d,f)
        h = open(p,encoding='utf-8',errors='replace').read()
        for m in re.finditer(r'(?:src|href|content)="([^"]+)"', h):
            v = m.group(1)
            if v.lower().endswith(EXT) and not v.startswith(('http','data:','#')):
                print(p, '->', v[:120])
        for m in re.finditer(r'url\((["\']?)([^"\')]+)\1\)', h):
            v = m.group(2)
            if v.lower().endswith(EXT) and not v.startswith(('http','data:')):
                print(p, 'CSS ->', v[:120])
