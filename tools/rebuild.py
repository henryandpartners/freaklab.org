"""Rebuild the frozen migration without connecting to WordPress or R2."""
from pathlib import Path
import subprocess,sys,tarfile
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'audit/original'
CACHE.mkdir(parents=True,exist_ok=True)
with tarfile.open(ROOT/'content/original-pages.tar.gz','r:gz') as archive:
 for member in archive.getmembers():
  relative=Path(member.name)
  if not member.isfile() or relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe snapshot path')
  destination=CACHE/relative;destination.parent.mkdir(parents=True,exist_ok=True)
  destination.write_bytes(archive.extractfile(member).read())
for script in ['migrate.py','restore_content.py','finalize.py','build.py','verify.py']:
 subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,check=True)
