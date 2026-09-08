#!/usr/bin/env python3
# The 6 remaining refs point at images that DON'T exist on disk (plugin files not mirrored) — harmless dead refs. Skip.
# Now delete the local image files to offload the repo, keeping only favicon-level critical assets inline? 
# Per plan: strip the image tree entirely; everything is on R2.
import os, shutil
SKIP = ('.git', '.vercel', '.venv-r2')
EXT = ('.jpg','.jpeg','.png','.webp','.gif','.svg','.ico')
removed = 0
freed = 0
for root, dirs, fs in os.walk('.', topdown=False):
    if any(s in root for s in SKIP): continue
    for f in fs:
        if f.lower().endswith(EXT):
            p = os.path.join(root, f)
            freed += os.path.getsize(p)
            os.remove(p)
            removed += 1
print(f"removed {removed} image files, freed {freed/1e6:.1f} MB")
# prune now-empty dirs
for root, dirs, fs in os.walk('.', topdown=False):
    if any(s in root for s in SKIP): continue
    if not os.listdir(root) and root != '.':
        os.rmdir(root)
print("done")
