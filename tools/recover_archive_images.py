"""Recover exact historical image URLs from public archive snapshots."""
from pathlib import Path
from urllib.parse import urlsplit,unquote,urlencode
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import json,subprocess,hashlib,re
ROOT=Path(__file__).resolve().parents[1];mapping=json.loads((ROOT/'audit/external-image-map.json').read_text());records=json.loads((ROOT/'audit/archive-candidates.json').read_text())
queries=['http://pat.design/wp-content/uploads/2017/12/'+n+'.jpg' for n in ['sxsw','tcdc','theguardian']]+['http://www.iafastro.org/wp-content/uploads/2018/06/heatshot_Wares.jpg','https://freaklab.org/wp-content/uploads/2022/04/Alan.jpg']
def cdx(u):
 query='https://web.archive.org/cdx/search/cdx?'+urlencode({'url':u,'output':'json','filter':'statuscode:200','limit':'1'})
 r=subprocess.run(['curl','-L','--max-time','25','-sS',query],capture_output=True,text=True)
 try:
  data=json.loads(r.stdout)
  return data[1:] if len(data)>1 else []
 except:return []
with ThreadPoolExecutor(max_workers=5) as pool:
 for rows in pool.map(cdx,queries):records.extend(rows)
(ROOT/'audit/archive-candidates.json').write_text(json.dumps(records,indent=2))
def download(record):
 u=record[2];timestamp=record[1];archive='https://web.archive.org/web/'+timestamp+'id_/'+u
 extension=Path(urlsplit(u).path).suffix or '.jpg';rel='assets/external/'+hashlib.sha256(u.encode()).hexdigest()[:16]+extension;path=ROOT/rel
 r=subprocess.run(['curl','-L','--max-time','30','-sS','-w','%{http_code}',archive,'-o',str(path)],capture_output=True,text=True)
 if r.stdout=='200':
  try:
   with Image.open(path) as image:width,height=image.size;image.verify()
   return u,{'url':'/'+rel,'status':200,'recovered_from':archive,'source_timestamp':timestamp,'width':width,'height':height,'match':'exact original URL'}
  except:pass
 path.unlink(missing_ok=True);return u,None
with ThreadPoolExecutor(max_workers=4) as pool:
 for u,result in pool.map(download,records):
  if not result:print('Archive unavailable',u,flush=True);continue
  basename=unquote(urlsplit(u).path).rsplit('/',1)[-1]
  for source in list(mapping):
   normalized=re.sub(r'-\d+x\d+(?=\.[^.]+$)','',unquote(urlsplit(source).path).rsplit('/',1)[-1])
   if normalized==basename:mapping[source]=result
  print('Recovered archive image',basename,result['width'],result['height'],flush=True)
(ROOT/'audit/external-image-map.json').write_text(json.dumps(mapping,indent=2))
