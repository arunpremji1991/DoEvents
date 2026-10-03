/* DO EVENTS — interactions */
(() => {
  const doc = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const hasGsap = typeof window.gsap !== 'undefined';
  const store = {
    get(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} },
  };
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  if (!hasGsap) { doc.classList.remove('js'); return; }
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- smooth scroll ---------- */
  let lenis = null;
  if (!reduce && typeof window.Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const lock = on => { if (lenis) on ? lenis.stop() : lenis.start(); document.body.style.overflow = on ? 'hidden' : ''; };

  /* ---------- split words ---------- */
  const splitNode = node => {
    [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const parts = n.textContent.split(/(\s+)/);
        const frag = document.createDocumentFragment();
        parts.forEach(p => {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
          const w = document.createElement('span'); w.className = 'w';
          const i = document.createElement('span'); i.className = 'wi'; i.textContent = p;
          w.appendChild(i); frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') splitNode(n);
    });
  };
  $$('[data-split]').forEach(el => {
    el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
    splitNode(el);
    // keep punctuation that directly follows a word (e.g. after </em>) on the same line
    const ws = $$('.w', el);
    ws.forEach((w, i) => {
      const prevNode = w.previousSibling || w.parentNode.previousSibling;
      if (i && /^[,.;:!?…)،؛؟]+$/.test(w.textContent) && !(prevNode && prevNode.nodeType === 3 && /\s$/.test(prevNode.textContent))) {
        ws[i - 1].firstChild.textContent += w.textContent; w.remove();
      }
    });
  });

  const reveal = (el, delay = 0) => gsap.to($$('.wi', el), { y: 0, yPercent: 0, duration: 1.25, ease: 'expo.out', stagger: .045, delay });
  const fadeIn = (el, delay = 0) => gsap.to(el, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', delay });

  const initScrollReveals = () => {
    $$('[data-split]:not([data-split="load"])').forEach(el => {
      ScrollTrigger.create({ trigger: el, start: 'top 88%', once: true, onEnter: () => reveal(el) });
    });
    $$('[data-fade]:not([data-fade="load"])').forEach(el => {
      ScrollTrigger.create({ trigger: el, start: 'top 92%', once: true, onEnter: () => fadeIn(el, +el.dataset.delay || 0) });
    });
  };
  const playIntro = () => {
    $$('[data-split="load"]').forEach((el, i) => reveal(el, .1 + i * .15));
    $$('[data-fade="load"]').forEach((el, i) => fadeIn(el, .45 + i * .12));
    const hv = $('.hero__media video, .hero__media img');
    if (hv) gsap.fromTo(hv, { scale: 1.18 }, { scale: 1.06, duration: 2.4, ease: 'expo.out' });
  };

  /* ---------- preloader / curtain ---------- */
  const loader = $('.loader');
  const curtain = $('.curtain');
  // own the transform in GSAP (percent-only) so CSS translateY(100%) isn't read back as pixels
  if (curtain) gsap.set(curtain, { y: 0, yPercent: 100 });
  const intro = () => {
    if (loader && !doc.classList.contains('no-loader')) {
      store.set('do-seen', '1');
      lock(true);
      const count = $('.loader__count', loader);
      const o = { v: 0 };
      const tl = gsap.timeline({ onComplete: () => { loader.remove(); lock(false); } });
      tl.to(o, { v: 100, duration: 2, ease: 'power2.inOut', onUpdate: () => { count.textContent = String(Math.round(o.v)).padStart(2, '0'); } })
        .to($('.loader__mark .fill', loader), { clipPath: 'inset(0% 0 0 0)', duration: 2, ease: 'power2.inOut' }, 0)
        .to(loader, { yPercent: -100, duration: 1.1, ease: 'expo.inOut' }, '+=.15')
        .add(playIntro, '-=.55');
    } else {
      if (loader) loader.remove();
      if (curtain && store.get('do-curtain')) {
        store.set('do-curtain', '');
        gsap.set(curtain, { yPercent: 0 });
        gsap.set($('svg', curtain), { opacity: 1 });
        gsap.to(curtain, { yPercent: -100, duration: 1, ease: 'expo.inOut', delay: .05 });
        gsap.delayedCall(.45, playIntro);
      } else playIntro();
    }
  };

  /* ---------- background music: one track that carries on from page to page ---------- */
  const music = (() => {
    const el = $('#bgm');
    const toggles = $$('.sound-toggle');
    const noop = { start() {}, duck() {}, restore() {}, leave() {} };
    if (!el) return noop;
    const VOL = .35;
    const pref = {
      get() { try { return localStorage.getItem('do-music'); } catch (e) { return null; } },
      set(v) { try { localStorage.setItem('do-music', v); } catch (e) {} },
    };
    let wanted = pref.get() !== 'off';   // visitor hasn't switched it off
    let ducked = false;                  // paused while a film plays
    let tween = null, resumed = false, armed = false;
    const playing = () => !el.paused && !ducked;
    const ui = () => toggles.forEach(b => { b.classList.toggle('is-on', playing()); b.setAttribute('aria-pressed', String(playing())); });
    // timer-based fade: keeps working where animation frames are paused (background tabs, hidden panes)
    const ramp = (to, d, done) => {
      clearInterval(tween);
      const from = el.volume, t0 = performance.now(), ms = d * 1000;
      tween = setInterval(() => {
        const k = Math.min(1, (performance.now() - t0) / ms);
        el.volume = Math.min(1, Math.max(0, from + (to - from) * (.5 - Math.cos(Math.PI * k) / 2)));
        if (k >= 1) { clearInterval(tween); if (done) done(); }
      }, 30);
    };
    const resumeTime = () => {   // continue where the previous page left off
      if (resumed) return; resumed = true;
      const t = parseFloat(store.get('do-music-t'));
      if (t > 0 && isFinite(t)) { try { el.currentTime = t; } catch (e) {} }
    };
    const arm = () => {          // autoplay blocked: start on the first tap, click or key press
      if (armed) return; armed = true;
      const evts = ['pointerdown', 'keydown', 'touchend'];
      const go = e => {
        if (e.target.closest && e.target.closest('.sound-toggle')) return;
        evts.forEach(t => removeEventListener(t, go, true)); armed = false; play();
      };
      evts.forEach(t => addEventListener(t, go, true));
    };
    const play = () => {
      if (!wanted || ducked || !el.paused) return;
      resumeTime();
      el.volume = 0;
      const p = el.play();
      if (p) p.then(() => { ramp(VOL, 1.8); ui(); }).catch(() => { arm(); ui(); });
    };
    const pause = (d = .6) => { if (el.paused) return; ramp(0, d, () => { el.pause(); ui(); }); };
    const save = () => { if (!el.paused) store.set('do-music-t', el.currentTime.toFixed(2)); };
    setInterval(save, 1000);
    addEventListener('pagehide', save);
    toggles.forEach(b => b.addEventListener('click', () => {
      if (playing()) { wanted = false; pref.set('off'); pause(.4); }
      else { wanted = true; pref.set('on'); ducked = false; play(); }
      ui();
    }));
    ui();
    return {
      start: play,
      duck() { if (ducked) return; ducked = !el.paused || wanted; pause(.5); ui(); },
      restore() { if (!ducked) return; ducked = false; play(); },
      leave() { save(); if (!el.paused) ramp(0, .7); },
    };
  })();

  document.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (a && a.dataset.lang) { try { localStorage.setItem('do-lang', a.dataset.lang); } catch (err) {} }
    if (!a || !curtain || reduce) return;
    const href = a.getAttribute('href');
    if (!href || a.target === '_blank' || a.hasAttribute('download') || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    if (/^(mailto:|tel:|https?:|#|javascript:)/.test(href)) return;
    const url = new URL(a.href, location.href);
    if (url.pathname === location.pathname && url.hash) return;
    e.preventDefault();
    store.set('do-curtain', '1');
    music.leave();
    gsap.set(curtain, { yPercent: 100 });
    gsap.to(curtain, { yPercent: 0, duration: .8, ease: 'expo.inOut', onComplete: () => { location.href = a.href; } });
    gsap.to($('svg', curtain), { opacity: 1, duration: .4, delay: .45 });
  });
  addEventListener('pageshow', e => { if (e.persisted && curtain) gsap.set(curtain, { yPercent: 100 }); });

  /* ---------- header ---------- */
  const header = $('.header');
  let lastY = 0;
  const onScroll = y => {
    if (!header) return;
    if (document.body.classList.contains('menu-open')) return;
    // header stays pinned at the top while scrolling (no hide-on-scroll)
    header.classList.toggle('is-scrolled', y > 60);
    lastY = y;
  };
  if (lenis) lenis.on('scroll', ({ scroll }) => onScroll(scroll)); else addEventListener('scroll', () => onScroll(scrollY), { passive: true });

  if (header) $$('.on-light').forEach(sec => ScrollTrigger.create({
    trigger: sec, start: 'top 40px', end: 'bottom 40px',
    onToggle: self => header.classList.toggle('is-light', self.isActive),
  }));

  const burger = $('.burger');
  if (burger) burger.addEventListener('click', () => {
    const open = document.body.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
    lock(open);
    if (open) gsap.fromTo($$('.mmenu a.big'), { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, stagger: .06, duration: 1, ease: 'expo.out', delay: .25 });
  });

  /* ---------- videos: lazy + play in view ---------- */
  const vids = $$('video[data-src], video[data-autoplay]');
  const vio = new IntersectionObserver(entries => entries.forEach(({ target: v, isIntersecting }) => {
    if (isIntersecting) {
      if (v.dataset.src && !v.src) { v.src = v.dataset.src; v.load(); }
      const p = v.play(); if (p) p.catch(() => {});
    } else v.pause();
  }), { rootMargin: '200px 0px' });
  vids.forEach(v => { v.muted = true; v.playsInline = true; vio.observe(v); });

  /* ---------- hero parallax ---------- */
  const heroMedia = $('.hero__media');
  if (heroMedia && !reduce) {
    gsap.to(heroMedia, { yPercent: 18, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero__inner', { yPercent: -10, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* ---------- 3D rising cards ---------- */
  if (!reduce) {
    const mobile = innerWidth < 760;
    $$('.wcard-wrap').forEach(wrap => {
      const card = $('.wcard', wrap);
      gsap.fromTo(card,
        { rotateX: mobile ? 55 : 78, y: () => innerHeight * (mobile ? .1 : .22), scale: mobile ? 1.08 : 1.22 },
        { rotateX: 0, y: 0, scale: 1, ease: 'none', scrollTrigger: { trigger: wrap, start: 'top bottom', end: mobile ? 'top 45%' : 'top 22%', scrub: .6, invalidateOnRefresh: true } });
      const details = $('.wcard__details', wrap);
      if (details) gsap.from(details, { opacity: 0, y: 30, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: details, start: 'top 95%', once: true } });
    });
  }

  /* ---------- cursor pill ---------- */
  const pill = $('.cursor-pill');
  if (pill && fine) {
    const xTo = gsap.quickTo(pill, 'x', { duration: .45, ease: 'power3' });
    const yTo = gsap.quickTo(pill, 'y', { duration: .45, ease: 'power3' });
    addEventListener('mousemove', e => { xTo(e.clientX); yTo(e.clientY); }, { passive: true });
    $$('[data-cursor]').forEach(el => {
      el.addEventListener('mouseenter', () => { $('span', pill).textContent = el.dataset.cursor; gsap.to(pill, { scale: 1, opacity: 1, xPercent: -50, yPercent: -50, duration: .5, ease: 'expo.out' }); });
      el.addEventListener('mouseleave', () => gsap.to(pill, { scale: 0, opacity: 0, duration: .4, ease: 'expo.out' }));
    });
    gsap.set(pill, { xPercent: -50, yPercent: -50 });
  }

  /* ---------- instagram rail ---------- */
  const rail = $('.follow__rail');
  if (rail && !reduce) {
    // LTR: rail starts at the left edge and travels left. RTL: it is anchored to the right edge and travels right.
    const rtl = doc.dir === 'rtl';
    gsap.fromTo(rail, { x: () => (rtl ? -1 : 1) * innerWidth * .15 }, {
      x: () => (rtl ? 1 : -1) * (rail.scrollWidth - innerWidth * .85), ease: 'none',
      scrollTrigger: { trigger: '.follow', start: 'top bottom', end: 'bottom top', scrub: .8, invalidateOnRefresh: true },
    });
  }

  /* ---------- CTA circle ---------- */
  const fitRing = () => $$('textPath[data-fit]').forEach(tp => {
    const text = tp.closest('text');
    text.style.fontSize = '';
    const len = tp.getComputedTextLength();
    const base = parseFloat(getComputedStyle(text).fontSize) || 66;
    if (len) text.style.fontSize = (base * (+tp.dataset.fit / len)).toFixed(2) + 'px';
  });
  fitRing();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitRing);
  const circle = $('.cta__circle svg');
  if (circle && !reduce) {
    gsap.fromTo(circle, { rotate: -40 }, { rotate: 140, ease: 'none', scrollTrigger: { trigger: '.cta', start: 'top bottom', end: 'bottom top', scrub: .8 } });
  }

  /* ---------- footer giant mark ---------- */
  const giant = $('.footer__giant svg');
  if (giant && !reduce) gsap.fromTo(giant, { yPercent: 45 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: '.footer__giant', start: 'top bottom', end: 'bottom bottom', scrub: true } });

  /* ---------- expanding media ---------- */
  $$('.expand').forEach(sec => {
    const media = $('.expand__media', sec), title = $('.expand__title', sec), copy = $('.expand__copy', sec);
    if (reduce) { gsap.set(media, { clipPath: 'inset(0% 0% 0% 0% round 0px)' }); return; }
    const m = innerWidth < 760;
    const tl = gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top top', end: 'bottom bottom', scrub: .6 } });
    tl.fromTo(media, { clipPath: m ? 'inset(28% 12% 28% 12% round 14px)' : 'inset(32% 33% 32% 33% round 16px)', yPercent: 30 },
                     { clipPath: 'inset(0% 0% 0% 0% round 0px)', yPercent: 0, ease: 'power2.inOut', duration: 1 })
      .to(title, { opacity: 0, scale: .92, duration: .5 }, .15)
      .fromTo(copy, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3 }, .75);
  });

  /* ---------- lightbox ---------- */
  const lb = $('.lightbox');
  if (lb) {
    const stage = $('.lightbox__stage', lb);
    let gallery = [], gi = 0;
    const show = html => { stage.innerHTML = html; lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); lock(true); $('.lightbox__close', lb).focus(); };
    const close = () => { lb.classList.remove('is-open', 'is-gallery'); lb.setAttribute('aria-hidden', 'true'); stage.innerHTML = ''; lock(false); music.restore(); };
    const showImg = () => show(`<img src="${gallery[gi]}" alt="">`);
    document.addEventListener('click', e => {
      const f = e.target.closest('[data-film]');
      if (f) {
        e.preventDefault();
        music.duck();
        if (f.dataset.yt) show(`<iframe src="https://www.youtube-nocookie.com/embed/${f.dataset.yt}?autoplay=1&rel=0&modestbranding=1" allow="autoplay; encrypted-media; fullscreen" allowfullscreen title="Film"></iframe>`);
        else {
          show(`<video src="${f.dataset.film}" controls autoplay playsinline poster="${f.dataset.poster || ''}"></video>`);
          const v = $('video', stage);
          v.addEventListener('ended', () => music.restore());
          v.addEventListener('play', () => music.duck());
        }
        return;
      }
      const g = e.target.closest('[data-gallery]');
      if (g) {
        const group = $$(`[data-gallery="${g.dataset.gallery}"]`);
        gallery = group.map(x => x.dataset.full); gi = group.indexOf(g);
        lb.classList.add('is-gallery'); showImg();
      }
    });
    $('.lightbox__close', lb).addEventListener('click', close);
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    $('.lightbox__nav--prev', lb).addEventListener('click', () => { gi = (gi - 1 + gallery.length) % gallery.length; showImg(); });
    $('.lightbox__nav--next', lb).addEventListener('click', () => { gi = (gi + 1) % gallery.length; showImg(); });
    addEventListener('keydown', e => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (lb.classList.contains('is-gallery') && e.key === 'ArrowRight') $('.lightbox__nav--next', lb).click();
      if (lb.classList.contains('is-gallery') && e.key === 'ArrowLeft') $('.lightbox__nav--prev', lb).click();
    });
  }

  /* ---------- case filters ---------- */
  const filters = $$('.filters button');
  filters.forEach(b => b.addEventListener('click', () => {
    filters.forEach(x => x.setAttribute('aria-pressed', x === b));
    const f = b.dataset.filter;
    $$('.cases .wcard-wrap').forEach(c => c.classList.toggle('is-out', f !== 'all' && c.dataset.cat !== f));
    ScrollTrigger.refresh();
  }));

  /* ---------- contact form → WhatsApp ---------- */
  const form = $('#enquiry');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    let L = {};
    try { L = JSON.parse(form.dataset.msg || '{}'); } catch (err) {}
    const t = (k, fb) => L[k] || fb;
    const lines = [
      t('intro', 'Hello Do Events, I would like to enquire about an event.'),
      `${t('name', 'Name')}: ${d.get('name')}`, `${t('phone', 'Phone')}: ${d.get('phone')}`,
      d.get('type') && `${t('type', 'Event type')}: ${d.get('type')}`, d.get('date') && `${t('date', 'Date')}: ${d.get('date')}`,
      d.get('guests') && `${t('guests', 'Guests')}: ${d.get('guests')}`, d.get('message') && `${t('message', 'Details')}: ${d.get('message')}`,
    ].filter(Boolean).join('\n');
    window.open(`${form.dataset.wa}?text=${encodeURIComponent(lines)}`, '_blank', 'noopener');
  });

  /* ---------- go ---------- */
  music.start();
  initScrollReveals();
  addEventListener('load', () => ScrollTrigger.refresh());
  intro();
})();
