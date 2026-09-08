#!/usr/bin/env python3
"""Inject a 'Symposium' nav item immediately after each 'Residency' item across freaklab-local.

Single unified pass: matches any menu-item-3875 Residency <li> (desktop nav-top-link
variant OR off-canvas mobile variant), mirrors its class/attrs, drops aria-current
(Symposium is never the current page when we run this).
"""
import os, re

SITE = "/Users/fathomers/workspace/freaklab.org/freaklab-local"

# <li ...3875...><a href="X" [attrs]>Residency</a></li>
RES = re.compile(
    r'<li([^>]*)class="([^"]*\bmenu-item-3875\b[^"]*)"([^>]*)>'
    r'<a href="([^"]*)"([^>]*)>Residency</a></li>'
)
ALREADY = re.compile(r'>Symposium</a>')


def sym_href(href: str) -> str:
    if href.startswith('http'):
        return re.sub(r'residency-program/?$', 'symposium/', href)
    return href.replace('residency-program/', 'symposium/')


def clean_attrs(attrs: str) -> str:
    # never carry over "this page is active" markers
    attrs = re.sub(r'\s*aria-current="[^"]*"', '', attrs)
    return attrs


def clean_li_attrs(pre: str, cls: str, post: str) -> str:
    """Drop current-page classes and give the cloned <li> a unique id."""
    cls2 = cls.replace(' current-menu-item', '').replace(' current_page_item', '')
    cls2 = re.sub(r'\s*\bactive\b', '', cls2)
    cls2 = re.sub(r'\s*current_page_parent\b', '', cls2)
    pre2 = re.sub(r'\s*id="[^"]*"', '', pre)
    post2 = re.sub(r'\s*id="[^"]*"', '', post)
    return f'<li{pre2}class="{cls2}"{post2}'


def main():
    files_changed = items = 0
    skipped = already = 0
    for root, dirs, fs in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('.git', 'symposium')]
        for f in fs:
            if not f.endswith(('.html', '.htm')):
                continue
            fp = os.path.join(root, f)
            try:
                c = open(fp, encoding='utf-8', errors='replace').read()
            except OSError:
                skipped += 1
                continue
            if 'menu-item-3875' not in c:
                skipped += 1
                continue
            if ALREADY.search(c):
                already += 1
                continue

            n = 0
            out = []
            last = 0
            for m in RES.finditer(c):
                li_pre, li_cls, li_post, href, a_attrs = m.groups()
                out.append(c[last:m.end()])
                last = m.end()
                n += 1
                # strip WordPress page-identity classes: Symposium is a static dir, not a WP page
                cls2 = re.sub(r'\s*page_item\b|\s*page-item-\d+|\s*current-menu-item\b|\s*current_page_item\b|\s*current_page_parent\b|\s*\bactive\b', '', li_cls)
                cls2 = re.sub(r'\s+', ' ', cls2).strip()
                pre2 = re.sub(r'\s*id="[^"]*"', '', li_pre)
                post2 = re.sub(r'\s*id="[^"]*"', '', li_post)
                li_open = f'<li{pre2}class="{cls2}"{post2}>'
                out.append(f'{li_open}<a href="{sym_href(href)}"{clean_attrs(a_attrs)}>Symposium</a></li>')
            out.append(c[last:])

            if n == 0:
                skipped += 1
                continue
            open(fp, 'w', encoding='utf-8').write(''.join(out))
            files_changed += 1
            items += n

    print(f"files changed:      {files_changed}")
    print(f"items injected:     {items}")
    print(f"skipped (no menu):  {skipped}")
    print(f"already injected:   {already}")


if __name__ == '__main__':
    main()
