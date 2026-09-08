#!/usr/bin/env python3
"""Point card thumbnails (esg-entry-media img) at the 500px R2 thumbs.

Reads key->thumbkey map from /tmp/thumb-map.tsv, rewrites only card images
(inside <div class="esg-entry-media">), leaving detail-page featured images at full res.
"""
import os, re
R2 = 'https://pub-6509346c2fdc47328b748c024f30f006.r2.dev/'
SKIP = ('.git','.vercel','.venv-r2')

# build map
thumb = {}
for line in open('/tmp/thumb-map.tsv'):
    line = line.strip()
    if not line or '\t' not in line: continue
    k, tk = line.split('\t', 1)
    thumb[k] = tk
print(f"thumb map: {len(thumb)} keys", flush=True)

total = 0
files_changed = 0
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d,f)
        h = open(p,encoding='utf-8',errors='replace').read()
        orig = h
        # card img: <div class="esg-entry-media"><img ... src="R2/<key>"
        def repl(m):
            global total
            key = m.group(2)
            if key in thumb:
                total += 1
                return m.group(1) + R2 + thumb[key] + m.group(3)
            return m.group(0)
        h = re.sub(r'(class="esg-entry-media"><img[^>]*src=")' + re.escape(R2) + r'([^"?]+)([^"]*")', repl, h)
        if h != orig:
            open(p,'w',encoding='utf-8').write(h)
            files_changed += 1

print(f"rewritten card img srcs: {total} across {files_changed} files", flush=True)
