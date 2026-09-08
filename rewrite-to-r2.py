#!/usr/bin/env python3
"""Rewrite all local image references in freaklab-local HTML+CSS to R2 public URLs.

Handles:
- <img src>, srcset, data-src, og:image/twitter:image content, <link rel=icon>
- CSS url(...) in inline styles and style-combined.css/style.css
- Depth-relative refs (../, ../../, ./, bare) from any page depth -> prefix substitution
R2_BASE = https://pub-6509346c2fdc47328b748c024f30f006.r2.dev
"""
import os, re, sys

R2 = "https://pub-6509346c2fdc47328b748c024f30f006.r2.dev"
EXTS = ('.jpg','.jpeg','.png','.webp','.gif','.svg','.ico')
SKIP = ('.git', '.vercel', '.venv-r2')

# map of every local image path (repo-root-relative) for existence check
all_imgs = set()
for root, dirs, fs in os.walk('.'):
    if any(s in root for s in SKIP): continue
    for f in fs:
        if f.lower().endswith(EXTS):
            all_imgs.add(os.path.relpath(os.path.join(root, f), '.'))

print(f"local images on disk: {len(all_imgs)}")

ATTR_RE = re.compile(r'(src|srcset|data-src|href|content)\s*=\s*"([^"]*)"')

def resolve(page_dir, ref):
    """Resolve a relative ref against page dir -> repo-root-relative path, or None."""
    ref = ref.split('?')[0].split('#')[0]
    if not ref or ref.startswith(('http://','https://','//','data:','#','mailto:')): return None
    if not ref.lower().endswith(EXTS): return None
    p = os.path.normpath(os.path.join(page_dir, ref))
    if p.startswith('..'): return None
    return p if p in all_imgs else None

def rewrite_attrs(text, page_dir):
    count = 0
    def sub(m):
        nonlocal count
        attr, val = m.group(1), m.group(2)
        if attr == 'srcset':
            parts = []
            changed = False
            for cand in val.split(','):
                cand = cand.strip()
                bits = cand.split()
                if not bits: continue
                key = resolve(page_dir, bits[0])
                if key:
                    bits[0] = f"{R2}/{key}"
                    changed = True
                parts.append(' '.join(bits))
            if changed: count += 1
            return f'{attr}="{", ".join(parts)}"'
        key = resolve(page_dir, val)
        if key:
            count += 1
            return f'{attr}="{R2}/{key}"'
        return m.group(0)
    return ATTR_RE.sub(sub, text), count

CSS_URL_RE = re.compile(r'url\((["\']?)([^"\')]+)\1\)')

def rewrite_css_urls(text, base_dir):
    count = 0
    def sub(m):
        nonlocal count
        q, val = m.group(1), m.group(2)
        key = resolve(base_dir, val)
        if key:
            count += 1
            return f'url({q}{R2}/{key}{q})'
        return m.group(0)
    return CSS_URL_RE.sub(sub, text), count

total = 0
pages = css_files = 0
for root, dirs, fs in os.walk('.'):
    if any(s in root for s in SKIP): continue
    for f in fs:
        p = os.path.join(root, f)
        rel_dir = os.path.dirname(p)
        if f.endswith('.html'):
            h = open(p, encoding='utf-8', errors='replace').read()
            h2, n = rewrite_attrs(h, rel_dir)
            # inline styles url()
            h2, n2 = rewrite_css_urls(h2, rel_dir)
            if h2 != h:
                open(p, 'w', encoding='utf-8').write(h2)
                pages += 1; total += n + n2
        elif f.endswith('.css'):
            c = open(p, encoding='utf-8', errors='replace').read()
            c2, n = rewrite_css_urls(c, rel_dir)
            if c2 != c:
                open(p, 'w', encoding='utf-8').write(c2)
                css_files += 1; total += n

print(f"rewritten refs: {total} across {pages} html + {css_files} css files")
