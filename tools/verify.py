"""Audit every generated route, local resource, published field, and deployment boundary."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,re,sys,warnings
from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings("ignore",category=MarkupResemblesLocatorWarning)
def norm(text):
 text=str(text).translate(str.maketrans({"’":"\'","‘":"\'","–":"-","—":"-","…":"...","“":"\"","”":"\""}))
 return re.sub(r"[\s\U0001F300-\U0001FAFF\ufe0f]+","",text.replace(":)",""))
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'public'
errors=[];warnings=[];pages=list(SITE.rglob('*.html'));assets=set();external_images=set()
def check(u,p,kind):
 if not u or u.startswith(('#','data:','mailto:','tel:','whatsapp:')):return
 z=urlsplit(u)
 if z.scheme or z.netloc:
  if kind=='img':external_images.add(u)
  if z.hostname in ['freaklab.org','www.freaklab.org'] and kind in ['script','stylesheet','img']:errors.append([str(p.relative_to(SITE)),kind,u,'original host dependency'])
  return
 dest=SITE/unquote(z.path).lstrip('/') if z.path.startswith('/') else p.parent/unquote(z.path)
 if dest.is_dir():dest=dest/'index.html'
 if not dest.exists():errors.append([str(p.relative_to(SITE)),kind,u,'missing'])
 else:assets.add(str(dest.relative_to(SITE)))
for p in pages:
 s=Soup(p.read_text(),'lxml')
 if not s.title or not s.select_one('h1'):warnings.append([str(p.relative_to(SITE)),'Missing title or H1'])
 for t in s.select('script[src],link[href],img[src],iframe[src],a[href],source[src],video[poster]'):
  attr='src' if t.name in ['script','img','iframe','source'] else 'poster' if t.name=='video' else 'href'
  if t.name=='link' and t.get('rel') not in [['stylesheet'],['icon'],['shortcut','icon'],['alternate']]:continue
  kind='stylesheet' if t.name=='link' and t.get('rel')==['stylesheet'] else t.name
  check(t[attr],p,kind)
 for im in s.select('img[srcset]'):
  for part in im['srcset'].split(','):
   if part.split():check(part.split()[0],p,'img')
 for t in s.select('style,[style]'):
  css=t.get_text() if t.name=='style' else t['style']
  for u in re.findall(r'url\([\"\']?([^\)\"\']+)',css):check(u,p,'style-asset')
 for t in s.find_all('script'):
  if not t.get('src') and t.get('type')!='application/ld+json' and p.parent.name!='symposium':errors.append([str(p.relative_to(SITE)),'Unexpected inline script'])
 if re.search(r'/wp-admin/|/wp-json/|xmlrpc\.php',str(s.select('script'))):errors.append([str(p.relative_to(SITE)),'WordPress service call'])
for p in (SITE/'assets').rglob('*.css'):
 for u in re.findall(r'url\([\"\']?([^\)\"\']+)',p.read_text()):check(u,p,'css-asset')
for p in SITE.rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.php','.py','.sh','.sql','.env']:errors.append(['Forbidden deployment file',str(p.relative_to(SITE))])
data=json.loads((ROOT/'content/published.json').read_text());recovered=json.loads((ROOT/'audit/content-recovery.json').read_text())
for post in data['posts']:
 if post['type'] not in ['projects','peoples','update','event','talk','sig']:continue
 path=SITE/post['type']/post['slug']/'index.html'
 if not path.exists():errors.append(['Missing published page',post['type'],post['slug']]);continue
 s=Soup(path.read_text(),'lxml');entry=s.select_one('.entry-content.single-page') or s.select_one('main')
 if entry:
  for placeholder in entry.select('.unavailable-image'):placeholder.decompose()
 text=norm(entry.get_text() if entry else '')
 for key in ['project_about','bio','description','project_publication','project_award','external_people']:
  values=(post.get('meta')or{}).get(key) or []
  if not values or not isinstance(values[0],str):continue
  source=values[0]
  def shortcode_text(match):
   label=re.search(r'text="([^"]*)"',match[0]);return label[1] if label else ''
  source=re.sub(r'\[(?:button|title)\b[^\]]*\]',shortcode_text,source)
  original=Soup(source,'html.parser')
  for t in original.select('script,style,iframe'):t.decompose()
  expected=norm(original.get_text())
  if expected and expected not in text:errors.append(['Published field text not preserved',post['type'],post['slug'],key])
 if post.get('content') and 'text="Template"' not in post['content']:
  body=re.sub(r'\[/?(?:section|row|row_inner|col|col_inner|ux_\w+|text_box|title|button|gap|divider|featured_box|blog_posts|follow)[^\]]*\]','',post['content'])
  body_soup=Soup(body,'html.parser')
  for node in body_soup.find_all(string=True):
   expected=norm(node)
   if len(expected)>=30 and expected not in text:errors.append(['Source body text not preserved',post['type'],post['slug'],expected[:60]])
for post in data['posts']:
 route='/'+post['type']+'/'+post['slug']+'/' if post['type'] in ['projects','peoples','update','event','talk','sig'] else urlsplit(post['url']).path
 target=SITE/unquote(route).strip('/')/'index.html'
 if not target.exists():errors.append(['Missing published URL',post['id'],route])
import xml.etree.ElementTree as ET
for name in ['feed.xml','sitemap.xml']:
 try:ET.parse(SITE/name)
 except ET.ParseError as error:errors.append(['Invalid XML',name,str(error)])
report={'published_url_coverage':len(data['posts']),'html_documents':len(pages),'verified_local_targets':len(assets),'external_image_urls':len(external_images),'published_types':dict(Counter(p['type'] for p in data['posts'])),'recovered_detail_pages':len(recovered['restored']),'source_profiles_without_biography_or_gallery':recovered['no_description_or_gallery'],'errors':errors,'warnings':warnings}
(ROOT/'audit/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'html_documents':len(pages),'error_count':len(errors),'warning_count':len(warnings),'sample_errors':errors[:12]},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
