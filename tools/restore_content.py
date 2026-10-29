"""Render recovered published WordPress custom fields as plain static HTML."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlsplit,urljoin
import json,re,html,warnings
from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings('ignore',category=MarkupResemblesLocatorWarning)
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'content/published.json').read_text())
media_map=json.loads((ROOT/'audit/media-map.json').read_text())
posts={str(p['id']):p for p in data['posts']};media={str(m['id']):m for m in data['media']}
R2='https://pub-6509346c2fdc47328b748c024f30f006.r2.dev'
def route(p):
 if p['type'] in ['projects','peoples','update','event','talk','sig']:return '/'+p['type']+'/'+p['slug']+'/'
 return urlsplit(p['url']).path

def media_url(m):
 u=m['url'];mapped=media_map.get(u,{})
 if mapped.get('missing'):return ''
 return mapped.get('url',u.replace('https://freaklab.org/wp-content/uploads/',R2+'/images/'))

def clean_fragment(value,featured=None):
 # Only published editorial content is rendered. Plugin/embedded scripts are never copied.
 text=str(value)
 def shortcode(match):
  kind=match[1];attrs=dict(re.findall(r'(\w+)="([^"]*)"',match[2]))
  if kind=='follow':
   links=[]
   for key,label in [('facebook','Facebook'),('instagram','Instagram'),('linkedin','Profile'),('twitter','Twitter'),('email','Email')]:
    target=attrs.get(key,'').strip()
    if not target:continue
    if key=='email':target='mailto:'+target
    links.append('<a href="'+html.escape(target,quote=True)+'">'+label+'</a>')
   return '<p>'+' · '.join(links)+'</p>' if links else ''
  if kind=='title':return '<h2>'+html.escape(attrs.get('text',''))+'</h2>'
  if kind=='button':return '<p><a href="'+html.escape(attrs.get('link','#'),quote=True)+'">'+html.escape(attrs.get('text','Learn more'))+'</a></p>'
  if kind=='ux_video':return '<p><a href="'+html.escape(attrs.get('url','#'),quote=True)+'">Watch video</a></p>'
  mid=attrs.get('id') if kind=='ux_image' else attrs.get('bg')
  if str(mid)==str(featured):return ''
  image=media.get(str(mid))
  if image and media_url(image):return '<figure><a href="'+html.escape(media_url(image),quote=True)+'"><img src="'+html.escape(media_url(image),quote=True)+'" alt="'+html.escape(image['title'],quote=True)+'" loading="lazy"></a></figure>'
  return ''
 text=re.sub(r'\[(ux_image|title|button|ux_video|ux_banner|follow)\b([^\]]*)\]',shortcode,text)
 # Convert common content-only shortcodes, retaining their text.
 text=re.sub(r'\[/?(?:vc_[^\]\s]+|row|col|section|ux_[^\]\s]+|tab|tabgroup|accordion|accordion-item|text_box|featured_box|message_box|scroll_to|gap|divider)[^\]]*\]','',text)
 s=Soup(text,'html.parser')
 for t in list(s.select('script,style,form,input,textarea,object,embed')):t.decompose()
 for t in s.find_all(True):
  for a in list(t.attrs):
   if a.lower().startswith('on') or a in ['srcdoc','nonce']:del t[a]
  for a in ['src','href','poster']:
   if t.get(a):
    u=t[a]
    if re.match(r'\s*(javascript|data|vbscript):',u,re.I):del t[a];continue
    if '/wp-content/uploads/' in u:t[a]=media_map.get(u,{}).get('url',u.replace('https://freaklab.org/wp-content/uploads/',R2+'/images/'))
    elif u.startswith('https://freaklab.org/'):t[a]=urlsplit(u).path
  if t.name=='iframe':
   host=urlsplit(t.get('src','')).hostname or ''
   if not any(host==x or host.endswith('.'+x) for x in ['youtube.com','youtube-nocookie.com','youtu.be','vimeo.com','google.com','soundcloud.com']):t.decompose();continue
   t['loading']='lazy';t['title']=t.get('title','Embedded media');t['referrerpolicy']='strict-origin-when-cross-origin'
  if t.name=='a' and t.get('target')=='_blank':t['rel']='noopener noreferrer'
 # WordPress custom text fields often store plain newlines rather than paragraph tags.
 if not s.find(['p','div','section','h1','h2','h3','ul','ol','table']):
  paragraphs=[]
  for block in re.split(r'\r?\n\s*\r?\n',str(s).strip()):
   if not block.strip():continue
   if '<iframe' in block:paragraphs.append(block)
   else:paragraphs.append('<p>'+block.replace('\r\n','\n').replace('\n','<br>')+'</p>')
  return ''.join(paragraphs)
 return str(s)

def values(value):
 if not value:return []
 first=value[0] if isinstance(value,list) else value
 if isinstance(first,list):return first
 if isinstance(first,dict):return list(first.values())
 return [first] if first else []

restored=[];empty=[]
for p in data['posts']:
 if p['type'] not in ['projects','peoples','update','event','talk','sig']:continue
 url=route(p);path=ROOT/url.strip('/')/'index.html'
 if not path.exists():
  template=Soup((ROOT/'projects/messe/index.html').read_text(),'lxml');template.title.string=p['title']+' – FREAK lab';path.parent.mkdir(parents=True,exist_ok=True)
 else:template=Soup(path.read_text(),'lxml')
 entry=template.select_one('.entry-content.single-page')
 if not entry:continue
 meta=p.get('meta') or {};entry.clear()
 title=template.new_tag('h1');title.string=p['title'];entry.append(title)
 m=media.get(str(p.get('featured')))
 if m and media_url(m):
  figure=template.new_tag('figure',attrs={'class':'entry-featured-img'});img=template.new_tag('img',src=media_url(m),alt=p['title'],decoding='async')
  dimensions=m.get('meta') or {}
  if isinstance(dimensions,dict):
   for k in ['width','height']:
    if dimensions.get(k):img[k]=dimensions[k]
  a=template.new_tag('a',href=media_url(m));a.append(img);figure.append(a);entry.append(figure)
 sections=[]
 description=values(meta.get('project_about'));body=p.get('content','')
 if body and 'text="Template"' not in body:sections.append(body)
 sections.extend(str(v) for v in description if v)
 for key in ['people_about','people_bio','person_about','about','bio','biography','description']:
  sections.extend(str(v) for v in values(meta.get(key)) if v)
 for key,label in [('affliation','Affiliation'),('date','Date'),('start_time','Start time'),('date_end','End date'),('end_time','End time'),('location','Location')]:
  for value in values(meta.get(key)):
   if value:
    para=template.new_tag('p');strong=template.new_tag('strong');strong.string=label+': ';para.append(strong);para.append(str(value));entry.append(para)
 rendered_text=''
 for value in dict.fromkeys(sections):
  fragment=Soup(clean_fragment(value,p.get('featured')),'html.parser')
  normalized=re.sub(r'\W+','',fragment.get_text()).casefold()
  if normalized and len(normalized)>30 and normalized in rendered_text:continue
  entry.append(fragment);rendered_text+=normalized
 gallery_ids=values(meta.get('project_gallery'))
 if gallery_ids:
  gallery=template.new_tag('div',attrs={'class':'static-gallery gallery'})
  for mid in gallery_ids:
   if str(mid)==str(p.get('featured')):continue
   image=media.get(str(mid))
   if not image or not media_url(image):continue
   figure=template.new_tag('figure');a=template.new_tag('a',href=media_url(image));a.append(template.new_tag('img',src=media_url(image),alt=image.get('caption') or image['title'],loading='lazy',decoding='async'));figure.append(a)
   if image.get('caption'):
    cap=template.new_tag('figcaption');cap.string=Soup(image['caption'],'html.parser').get_text();figure.append(cap)
   gallery.append(figure)
  entry.append(gallery)
 for key in ['project_video-1','project_video-2','project_video-3','video']:
  for value in values(meta.get(key)):
   if not value:continue
   if str(value).startswith('http'):
    z=urlsplit(value);video_id=None
    if z.hostname in ['youtube.com','www.youtube.com']:
     from urllib.parse import parse_qs
     video_id=parse_qs(z.query).get('v',[None])[0]
    elif z.hostname=='youtu.be':video_id=z.path.strip('/')
    if video_id:value='<iframe src="https://www.youtube-nocookie.com/embed/'+html.escape(video_id)+'" title="Project video" allowfullscreen></iframe>'
    else:value='<p><a href="'+html.escape(value,quote=True)+'">Watch video</a></p>'
   entry.append(Soup(clean_fragment(value),'html.parser'))
 for key,label in [('project_people','People'),('project_press','Press'),('project_award','Awards'),('project_publication','Publications'),('achievement','Projects and achievements')]:
  ids=values(meta.get(key));related=[posts[str(i)] for i in ids if str(i) in posts]
  prose=[i for i in ids if str(i) not in posts and not str(i).isdigit()]
  if prose:
   h=template.new_tag('h2');h.string=label;entry.append(h)
   for value in prose:entry.append(Soup(clean_fragment(value),'html.parser'))
  if related:
   h=template.new_tag('h2');h.string=label;entry.append(h);ul=template.new_tag('ul')
   for item in related:
    li=template.new_tag('li');a=template.new_tag('a',href=route(item));a.string=item['title'];li.append(a);ul.append(li)
   entry.append(ul)
 for value in values(meta.get('external_people')):
  if value:
   h=template.new_tag('h2');h.string='Collaborators';entry.append(h);entry.append(Soup(clean_fragment(value),'html.parser'))
 # Restore roles and group membership from the original public directory cards.
 if p['type']=='peoples':
  if p.get('public_role'):
   para=template.new_tag('p');para.string=p['public_role'];entry.insert(1,para)
  if p.get('public_groups'):
   para=template.new_tag('p',attrs={'class':'static-member-groups'})
   for group in p['public_groups']:
    a=template.new_tag('a',href=group['url']);a.string=group['title'];para.append(a);para.append(' · ')
   entry.append(para)
 # Turn text-only source URLs into usable links without interpreting them as markup.
 for text_node in list(entry.find_all(string=True)):
  if text_node.parent.name in ['a','script','style']:continue
  matches=list(re.finditer(r'https?://[^\s<>]+',str(text_node)))
  if not matches:continue
  cursor=0
  for match in matches:
   text_node.insert_before(str(text_node)[cursor:match.start()]);a=template.new_tag('a',href=match[0]);a.string=match[0];text_node.insert_before(a);cursor=match.end()
  text_node.insert_before(str(text_node)[cursor:]);text_node.extract()
 for obsolete in template.select('.entry-meta'):
  if 'This entry was posted in' in obsolete.get_text():obsolete.decompose()
 # Public editorial contact/profile links only; internal plugin metadata never gets rendered.
 for key,label in [('email','Email'),('website','Website'),('facebook','Facebook'),('twitter','Twitter'),('linkedin','LinkedIn')]:
  for v in values(meta.get(key)):
   if not isinstance(v,str) or not v:continue
   target='mailto:'+v if key=='email' else v
   if key!='email' and not target.startswith(('https://','http://')):continue
   para=template.new_tag('p');a=template.new_tag('a',href=target);a.string=label;para.append(a);entry.append(para)
 if not sections and not gallery_ids:empty.append(url)
 for t in template.select('link[rel=canonical]'):t['href']='https://freaklab.org'+url
 for t in template.select('meta[property="og:title"],meta[name="twitter:title"]'):t['content']=p['title']
 for t in template.select('meta[property="og:url"]'):t['content']='https://freaklab.org'+url
 path.write_text('<!DOCTYPE html>\n'+str(template.html)+'\n')
 restored.append({'url':url,'title':p['title'],'body_fields':len(sections),'gallery_images':len(gallery_ids)})
(ROOT/'audit/content-recovery.json').write_text(json.dumps({'restored':restored,'no_description_or_gallery':empty},ensure_ascii=False,indent=2))
print('Recovered',len(restored),'detail pages;',len(empty),'without descriptions or galleries.')
