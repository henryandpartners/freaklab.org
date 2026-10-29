from pathlib import Path
import json,hashlib,subprocess
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'audit/verification.json').read_text());paths=sorted({e[2] for e in r['errors'] if len(e)>3 and e[1]=='style-asset' and e[2].startswith('/wp-content/')})
manifest={}
for u in paths:
 path=urlsplit(u).path;url='https://freaklab.org'+path;rel='assets/vendor/'+hashlib.sha256(url.encode()).hexdigest()[:16]+Path(path).suffix;p=ROOT/rel
 result=subprocess.run(['curl','-L','--max-time','25','-sS','-w','%{http_code}',url,'-o',str(p)],capture_output=True,text=True)
 if result.stdout=='200':manifest[u]='/'+rel
 else:p.unlink(missing_ok=True);print('Missing source font',u,result.stdout,flush=True)
(ROOT/'audit/inline-map.json').write_text(json.dumps(manifest,indent=2));print('Saved',len(manifest),'inline font dependencies.')
