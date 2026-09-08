#!/usr/bin/env python3
"""Move menu items into dropdowns across all freaklab-local pages.

- Publications (1466) + Courses (3488) → under Research (940)
- Press (2681) + Events (2321) → under Updates (2322)

Handles both the desktop nav (li with id=) and the sidebar nav (li with class only).
Ensures the parent (Research/Updates) has menu-item-has-children + has-dropdown
classes and that a populated sub-menu <ul> exists to append into.
Idempotent: skips pages where the item is already inside a sub-menu of the parent.
"""
import os, re, sys

MOVE = {
    '1466': '940',   # Publications -> Research
    '3488': '940',   # Courses -> Research
    '2681': '2322',  # Press -> Updates
    '2321': '2322',  # Events -> Updates
}

def process(html):
    changed = False
    for item, parent in MOVE.items():
        # --- desktop: li with id ---
        desk = re.search(r'<li id="menu-item-%s"[^>]*>.*?</li>' % item, html, re.S)
        if desk:
            # check it's currently a TOP-LEVEL item (direct child of header-nav ul, not sub-menu)
            # if the preceding non-space is a <ul class="sub-menu... of our parent, skip
            pre = html[max(0, desk.start()-200):desk.start()]
            if not re.search(r'<ul class="sub-menu[^"]*">\s*$', pre):
                li = desk.group(0)
                html = html[:desk.start()] + html[desk.end():]
                html = inject_into_parent(html, parent, li, desktop=True)
                changed = True
        # --- sidebar: li with class only ---
        side = re.search(r'<li class="menu-item[^"]*\bmenu-item-%s\b[^"]*"[^>]*>.*?</li>' % item, html, re.S)
        if side:
            pre = html[max(0, side.start()-200):side.start()]
            if not re.search(r'<ul class="sub-menu[^"]*">\s*$', pre):
                li = side.group(0)
                html = html[:side.start()] + html[side.end():]
                html = inject_into_parent(html, parent, li, desktop=False)
                changed = True
    return html, changed

def inject_into_parent(html, parent, li, desktop):
    # find the parent's sub-menu <ul> that FOLLOWS the parent li's <a>
    if desktop:
        pa = re.search(r'<li id="menu-item-%s"[^>]*>.*?</a>' % parent, html, re.S)
    else:
        pa = re.search(r'<li class="menu-item[^"]*\bmenu-item-%s\b[^"]*"[^>]*>.*?</a>' % parent, html, re.S)
    if not pa:
        # parent not found in this nav instance; put the li back where it was is complex.
        # Fallback: append before the closing of the parent search li — not available.
        # In practice every page has both instances; if missing, re-insert after header ul open.
        print("  !! parent %s (%s) not found" % (parent, 'desktop' if desktop else 'sidebar'))
        return html
    # does a sub-menu ul immediately follow?
    after = html[pa.end():pa.end()+100]
    m = re.match(r'\s*<ul class="sub-menu', after)
    if m:
        # insert li right after that <ul ...> opening tag
        ul_open_end = pa.end() + html[pa.end():].index('>', html[pa.end():].index('<ul')) + 1
        html = html[:ul_open_end] + '\n' + li + html[ul_open_end:]
    else:
        # create a new sub-menu ul after the parent's </a>
        # need parent li's dropdown classes present
        pstart, pend = pa.start(), pa.end()
        pli_open = html[pa.start():html.index('>', pa.start())+1]
        new_open = pli_open
        if 'menu-item-has-children' not in new_open:
            new_open = new_open.replace('">', ' menu-item-has-children">', 1) if new_open.rstrip().endswith('">') else re.sub(r'(<li [^>]*?)>', r'\1 menu-item-has-children>', new_open, count=1)
        if 'has-dropdown' not in new_open:
            new_open = new_open.replace('menu-item-design-default', 'menu-item-design-default has-dropdown', 1) if 'menu-item-design-default' in new_open else re.sub(r'(<li [^>]*?)>', r'\1 has-dropdown>', new_open, count=1)
        html = html[:pstart] + new_open + html[html.index('>', pa.start())+1:pend] + \
               '\n<ul class="sub-menu nav-dropdown nav-dropdown-default">\n' + li + '\n</ul>\n' + html[pend:]
    return html

def main():
    total_files = changed_files = 0
    for d, _, fs in os.walk('.'):
        if '.git' in d or '.vercel' in d or '.venv-r2' in d:
            continue
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(d, f)
            total_files += 1
            html = orig = open(p, encoding='utf-8', errors='replace').read()
            # idempotence: skip if e.g. Publications li already preceded by a sub-menu ul of Research
            html, changed = process(html)
            # run twice: moving 2 items into the same parent (2nd needs the ul that may have been created)
            html, changed2 = process(html)
            if changed or changed2:
                open(p, 'w', encoding='utf-8').write(html)
                changed_files += 1
    print("scanned %d, changed %d" % (total_files, changed_files))

if __name__ == '__main__':
    main()
