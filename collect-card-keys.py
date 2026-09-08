#!/usr/bin/env python3
import os, re
SKIP = ('.git','.vercel','.venv-r2')
R2 = 'https://pub-6509346c2fdc47328b748c024f30f006.r2.dev/'
all_keys = set()
card_keys = set()
for d,_,fs in os.walk('.'):
    if any(s in d for s in SKIP): continue
    for f in fs:
        if not f.endswith('.html'): continue
        p = os.path.join(d,f)
        h = open(p,encoding='utf-8',errors='replace').read()
        for m in re.finditer(r'src="('+re.escape(R2)+r'[^"]+)"', h):
            all_keys.add(m.group(1)[len(R2):].split('?')[0])
        for m in re.finditer(r'class="esg-entry-media"><img[^>]*src="('+re.escape(R2)+r'[^"]+)"', h):
            card_keys.add(m.group(1)[len(R2):].split('?')[0])
print("total distinct R2 image keys referenced:", len(all_keys))
print("distinct CARD thumbnail keys (esg-entry-media):", len(card_keys))
# show first 5 card keys
for k in sorted(card_keys)[:5]: print("  ", k)
# write card keys to file
with open('/tmp/card-keys.txt','w') as fh:
    fh.write('\n'.join(sorted(card_keys)))
