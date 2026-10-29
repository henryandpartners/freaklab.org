"""Read-only snapshot of public original pages; no WordPress credentials required."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'audit/original'; CACHE.mkdir(parents=True,exist_ok=True)
pages=[p for p in ROOT.rglob('index.html') if not any(x in p.parts for x in ['.git','audit','dist'])]
def get(p):
 rel=p.relative_to(ROOT).as_posix(); url='https://freaklab.org/'+rel.removesuffix('index.html'); out=CACHE/rel
 if out.exists():return {'path':rel,'status':200,'cached':True}
 try:
  out.parent.mkdir(parents=True,exist_ok=True)
  r=subprocess.run(['curl','-L','--max-time','30','-sS','-w','%{http_code}',url,'-o',str(out)],capture_output=True,text=True)
  status=int(r.stdout) if r.stdout.isdigit() else 0
  result={'path':rel,'status':status,'url':url}
  if status!=200:out.unlink(missing_ok=True)
  return result
 except Exception as e:return {'path':rel,'error':str(e)}
results=[]
with ThreadPoolExecutor(max_workers=8) as pool:
 for task in as_completed([pool.submit(get,p) for p in pages]):
  results.append(task.result())
  if len(results)%25==0:print(f'Captured {len(results)}/{len(pages)}',flush=True)
(ROOT/'audit/capture.json').write_text(json.dumps(results,indent=2))
print('Complete',len(results),'pages',sum(r.get('status')==200 for r in results),'OK',flush=True)
