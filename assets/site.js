/* Static interactions only: no WordPress, plugin AJAX, or server-side execution. */
(() => {
  'use strict';
  const all = (selector, root = document) => [...root.querySelectorAll(selector)];
  const button = (label, run) => {
    const b = document.createElement('button'); b.type = 'button'; b.textContent = label;
    b.addEventListener('click', run); return b;
  };
  all('.esg-grid').forEach(grid => {
    const items = all(':scope > ul > li', grid);
    const filters = all('.esg-filterbutton', grid);
    const previous = grid.querySelector('.esg-navigationbutton.esg-left');
    const next = grid.querySelector('.esg-navigationbutton.esg-right');
    if (!filters.length && previous && next && items.length) {
      let page = 0;
      const size = () => (innerWidth <= 480 ? 1 : innerWidth <= 750 ? 2 : innerWidth <= 1000 ? 3 : 4) * 2;
      const status = document.createElement('span'); status.className = 'static-page-status'; status.setAttribute('aria-live','polite');next.after(status);
      const render = () => {
        const count = size(); page = Math.min(page, Math.ceil(items.length/count)-1);
        items.forEach((li,i) => {li.hidden=i<page*count || i>=(page+1)*count;});
        previous.setAttribute('aria-disabled',String(page===0));next.setAttribute('aria-disabled',String((page+1)*count>=items.length));
        status.textContent=` ${page*count+1}–${Math.min(items.length,(page+1)*count)} of ${items.length} `;
      };
      [[previous,-1,'Previous updates'],[next,1,'Next updates']].forEach(([control,direction,label])=>{
        control.style.display='inline-block';control.setAttribute('role','button');control.tabIndex=0;control.setAttribute('aria-label',label);
        const change=()=>{if(control.getAttribute('aria-disabled')==='true')return;page+=direction;render();};
        control.addEventListener('click',change);control.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();change();}});
      });
      render();window.addEventListener('resize',render);
    }

    filters.forEach(filter => {
      const key = filter.dataset.filter;
      filter.setAttribute('role', 'button'); filter.tabIndex = 0;
      const count = key === 'filterall' ? items.length : items.filter(li => li.classList.contains(key)).length;
      const amount = document.createElement('span'); amount.className = 'static-count'; amount.textContent = ` (${count})`; filter.append(amount);
      filter.setAttribute('aria-pressed', String(filter.classList.contains('selected')));
      const apply = () => {
        filters.forEach(f => { f.classList.toggle('selected', f === filter); f.setAttribute('aria-pressed', String(f === filter)); });
        items.forEach(li => { li.hidden = key !== 'filterall' && !li.classList.contains(key); });
      };
      filter.addEventListener('click', apply);
      filter.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); apply(); } });
    });
  });
  const menu = document.querySelector('#main-menu');
  const menuTriggers = all('[data-open="#main-menu"]');
  let previousFocus;
  if (menu) {
    const close = () => { menu.classList.remove('static-menu-open'); document.body.classList.remove('menu-open'); menuTriggers.forEach(a => a.setAttribute('aria-expanded', 'false')); previousFocus?.focus(); };
    all('.menu-item-has-children',menu).forEach(li=>{
      const submenu=li.querySelector(':scope > ul');const anchor=li.querySelector(':scope > a');
      if(!submenu||!anchor||!submenu.querySelector('a'))return;
      submenu.hidden=true;submenu.classList.add('static-mobile-submenu');
      const toggle=button('+',()=>{submenu.hidden=!submenu.hidden;toggle.textContent=submenu.hidden?'+':'−';toggle.setAttribute('aria-expanded',String(!submenu.hidden));});
      toggle.className='static-mobile-submenu-toggle';toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label',`Toggle ${anchor.textContent.trim()} links`);anchor.after(toggle);
    });
    const closeButton = button('Close menu ×', close); closeButton.className = 'static-menu-close'; menu.prepend(closeButton);
    menuTriggers.forEach(a => a.addEventListener('click', e => {
      e.preventDefault(); previousFocus = a; menu.classList.add('static-menu-open'); document.body.classList.add('menu-open');
      menuTriggers.forEach(t => t.setAttribute('aria-expanded', 'true')); closeButton.focus();
    }));
    menu.addEventListener('keydown', e => {
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') {
        const focusables = all('a[href],button,input', menu).filter(x => x.getClientRects().length);
        if (e.shiftKey && document.activeElement === focusables[0]) { e.preventDefault(); focusables.at(-1).focus(); }
        else if (!e.shiftKey && document.activeElement === focusables.at(-1)) { e.preventDefault(); focusables[0].focus(); }
      }
    });
  }
  all('#header .menu-item-has-children').forEach(li => {
    const toggle = button('▾', () => {
      const open = li.classList.toggle('static-dropdown-open'); toggle.setAttribute('aria-expanded', String(open));
    });
    toggle.className = 'static-dropdown-toggle'; toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', `Toggle ${li.querySelector('a')?.textContent.trim()} submenu`); li.prepend(toggle);
    li.addEventListener('keydown', e => { if (e.key === 'Escape') { li.classList.remove('static-dropdown-open'); toggle.setAttribute('aria-expanded','false'); toggle.focus(); } });
  });
  all('.slider, .slider-wrapper > .row-slider').forEach(slider => {
    if (!slider.children.length) return;
    slider.classList.add('static-slider');
    const controls = document.createElement('div'); controls.className = 'static-slider-controls';
    controls.append(button('← Previous', () => slider.scrollBy({left: -slider.clientWidth, behavior:'smooth'})), button('Next →', () => slider.scrollBy({left:slider.clientWidth, behavior:'smooth'})));
    slider.after(controls);
  });
  all('.tabbed-content').forEach(container => {
    const tabs = all('.nav > li > a', container); const panels = all('.tab-panels > .panel', container);
    if (!tabs.length || !panels.length) return;
    const activate = i => { tabs.forEach((a,j) => { a.parentElement.classList.toggle('active',i===j); a.setAttribute('aria-selected',String(i===j)); }); panels.forEach((p,j) => {p.hidden=i!==j;p.classList.toggle('active',i===j);}); };
    tabs.forEach((a,i) => a.addEventListener('click',e => {e.preventDefault();activate(i);}));activate(0);
  });
  all('.accordion-item').forEach(item => {
    const title = item.querySelector('.accordion-title'); const panel = item.querySelector('.accordion-inner');
    if (!title || !panel) return;
    title.setAttribute('role','button');title.setAttribute('aria-expanded','false');panel.hidden=true;
    const toggle = e => { e.preventDefault();panel.hidden=!panel.hidden;title.classList.toggle('active',!panel.hidden);title.setAttribute('aria-expanded',String(!panel.hidden)); };
    title.addEventListener('click',toggle);
    title.addEventListener('keydown', e => {if(e.key===' ')toggle(e);});
  });
  // Native dialog keeps gallery navigation independent of the old popup plugin.
  let dialog; let gallery=[]; let selected=0; let opener;
  const showImage = index => {
    selected=(index+gallery.length)%gallery.length;
    dialog.querySelector('img').src=gallery[selected].href;
    dialog.querySelector('img').alt=gallery[selected].querySelector('img')?.alt || '';
    dialog.querySelector('figcaption').textContent=gallery[selected].querySelector('img')?.alt || '';
  };
  all('a[href]').filter(a => /\.(jpe?g|png|webp|gif)(\?.*)?$/i.test(a.getAttribute('href')) && a.querySelector('img')).forEach(a => {
    a.addEventListener('click',e => {
      e.preventDefault();opener=a;
      gallery=all('a[href]', a.closest('.gallery,.row') || document).filter(x=>/\.(jpe?g|png|webp|gif)(\?.*)?$/i.test(x.getAttribute('href')) && x.querySelector('img'));
      if (!dialog) {
        dialog=document.createElement('dialog');dialog.className='static-lightbox';dialog.setAttribute('aria-label','Image viewer');
        const figure=document.createElement('figure');figure.append(document.createElement('img'),document.createElement('figcaption'));
        dialog.append(button('Close ×',()=>dialog.close()),figure,button('← Previous',()=>showImage(selected-1)),button('Next →',()=>showImage(selected+1)));
        document.body.append(dialog);dialog.addEventListener('close',()=>opener?.focus());
        dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')showImage(selected-1);if(e.key==='ArrowRight')showImage(selected+1);});
      }
      showImage(gallery.indexOf(a));dialog.showModal();
    });
  });
  const search = document.querySelector('#static-search');
  if (search) {
    const query = new URLSearchParams(location.search).get('s') || '';
    search.querySelector('input').value=query;
    const results=document.querySelector('#search-results');
    fetch('/assets/search-index.json').then(r=>{if(!r.ok)throw Error('Search index unavailable');return r.json();}).then(pages=>{
      const terms=query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      const hits=terms.length ? pages.filter(p=>terms.every(t=>(p.title+' '+p.text).toLocaleLowerCase().includes(t))).sort((a,b)=>Number(terms.every(t=>b.title.toLocaleLowerCase().includes(t)))-Number(terms.every(t=>a.title.toLocaleLowerCase().includes(t)))) : [];
      results.textContent=terms.length ? `${hits.length} results for “${query}”` : 'Enter a name, project, or research topic.';
      hits.forEach(p=>{const article=document.createElement('article');const h=document.createElement('h2');const a=document.createElement('a');a.href=p.url;a.textContent=p.title;h.append(a);const text=document.createElement('p');text.textContent=p.text.slice(0,220)+'…';article.append(h,text);results.append(article);});
    }).catch(()=>{results.textContent='Search could not load. Please try again.';});
  }
  // Support existing bookmarked WordPress-style search URLs on the homepage.
  if (location.pathname==='/' && new URLSearchParams(location.search).has('s')) location.replace('/search/'+location.search);
})();
