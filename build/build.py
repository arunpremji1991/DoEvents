#!/usr/bin/env python3
"""Generates the bilingual Do Events static site (English at /, Arabic at /ar/).
Run:  python3 build/build.py"""
import json, os, re, html
from data import (SITE, CATS, CASES, NO_LOCAL_FILM, FEATURED, NOTABLE, MARQUEE_CLIENTS,
                  SITE_AR, CATS_AR, CASES_AR, NOTABLE_AR, MARQUEE_CLIENTS_AR, CLIENT_LOGOS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YT = {d["id"]: d for d in json.load(open(os.path.join(ROOT, "build", "youtube.json"), encoding="utf8"))}
BY = {c["slug"]: c for c in CASES}
e = html.escape
NOEMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")


def v(path):
    """Cache-busting stamp: assets get a new URL whenever their content changes."""
    import hashlib
    full = os.path.join(ROOT, path)
    return path + ("?v=" + hashlib.md5(open(full, "rb").read()).hexdigest()[:8] if os.path.exists(full) else "")


def svg_inline(name):
    s = open(os.path.join(ROOT, "assets", "logo", name), encoding="utf8").read().strip()
    s = re.sub(r'\s(width|height)="[^"]+"', "", s, count=2)
    s = re.sub(r"<title>.*?</title>", "", s)
    return s.replace('role="img"', 'aria-hidden="true" focusable="false"')


LOGO = svg_inline("do-events-logo-current.svg")
MARK = svg_inline("do-mark-current.svg")

ICON = {
    "arrow": '<svg class="btn__arrow" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M1 11L11 1M4 1h7v7"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 3.5v17l15-8.5z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4 5.1 5.1 0 003.2.7 2.7 2.7 0 001.8-1.3 2.2 2.2 0 00.1-1.3c0-.1-.2-.2-.5-.3z"/></svg>',
    "yt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 00-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 001 7.2 31 31 0 00.5 12 31 31 0 001 16.8a3 3 0 002.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 002.1-2.1 31 31 0 00.5-4.8 31 31 0 00-.5-4.8zM9.7 15V9l5.8 3z"/></svg>',
}


class Ctx:
    """Per-page language context. `page` is the path relative to the language root."""
    def __init__(self, lang, page):
        self.lang, self.page = lang, page
        self.ar = lang == "ar"
        depth = page.count("/") + (1 if self.ar else 0)
        self.r = "../" * depth                       # → site root (assets)
        self.L = self.r + ("ar/" if self.ar else "")  # → this language's root
        self.alt = self.r + ("" if self.ar else "ar/") + page
        self.other = "en" if self.ar else "ar"

    def x(self, en, ar):
        return ar if self.ar else en


def btn(label, href="#", kind="", dot=False, arrow=False, attrs=""):
    cls = f"btn {kind}".strip()
    tail = '<i class="btn__dot"></i>' if dot else (ICON["arrow"] if arrow else "")
    return (f'<a class="{cls}" href="{href}" {attrs}><span class="btn__text"><span>{label}</span>'
            f'<span aria-hidden="true">{label}</span></span>{tail}</a>')


def mtag(text, extra=""):
    spans = "".join(f"<span>{text}</span>" for _ in range(4))
    return f'<div class="mtag {extra}" aria-hidden="true"><div class="mtag__inner">{spans}</div><div class="mtag__inner">{spans}</div></div>'


def alt(ctx, en, ar):
    """Secondary line in the *other* language."""
    return f'lang="{ctx.other}" dir="{"ltr" if ctx.ar else "rtl"}"', (en if ctx.ar else ar)


def nav_items(ctx):
    return [("weddings.html", ctx.x("Weddings", "حفلات الزفاف")), ("corporate.html", ctx.x("Corporate", "الشركات")),
            ("work.html", ctx.x("Case Studies", "أعمالنا")), ("about.html", ctx.x("About", "من نحن"))]


def all_links(ctx):
    return [("index.html", ctx.x("Home", "الرئيسية"))] + nav_items(ctx) + [("contact.html", ctx.x("Contact", "تواصل معنا"))]


# ------------------------------------------------------------------ shared chrome
def head(ctx, title, desc, og="assets/img/poster/hero.jpg", loader=False, ld=""):
    x = ctx.x
    en_href = ctx.r + ctx.page
    ar_href = ctx.r + "ar/" + ctx.page
    redirect = ""
    if not ctx.ar and ctx.page == "index.html":
        # Returning visitors who chose Arabic (or Arabic browsers on first visit) land on /ar/
        redirect = ("<script>try{var l=localStorage.getItem('do-lang');if(l==='ar'||(!l&&/^ar\\b/i.test(navigator.language||'')))"
                    "location.replace('ar/index.html')}catch(e){}</script>")
    loader_html = ""
    if loader:
        loader_html = f"""<div class="loader" aria-hidden="true">
  <div class="loader__mark"><img src="{ctx.r}assets/img/brand/frame-do-dark.svg" alt=""><div class="fill"><img src="{ctx.r}assets/img/brand/frame-do-dark.svg" alt=""></div></div>
  <div class="loader__tag">{x("Salalah · Oman", "صلالة · عُمان")}<b {x('lang="ar"', 'lang="en"')}>{x(SITE['tagline_ar'], SITE['tagline'])}</b></div>
  <div class="loader__count">00</div>
</div>
"""
    return f"""<!doctype html>
<html lang="{ctx.lang}" dir="{x('ltr', 'rtl')}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#9b4825">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{x('Do Events', 'دو للمناسبات')}">
<meta property="og:locale" content="{x('en_US', 'ar_OM')}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{ctx.r}{og}">
<link rel="alternate" hreflang="en" href="{en_href}">
<link rel="alternate" hreflang="ar" href="{ar_href}">
<link rel="alternate" hreflang="x-default" href="{en_href}">
<link rel="icon" href="{ctx.r}assets/logo/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{ctx.r}{v("assets/css/fonts.css")}">
<link rel="stylesheet" href="{ctx.r}{v("assets/css/style.css")}">
{redirect}<script>document.documentElement.classList.add('js');try{{if(sessionStorage.getItem('do-seen'))document.documentElement.classList.add('no-loader')}}catch(e){{}}</script>
{ld}
</head>
<body>
<a class="sr-only" href="#main">{x("Skip to content", "تخطَّ إلى المحتوى")}</a>
{loader_html}<div class="curtain" aria-hidden="true">{MARK}</div>
<div class="grain" aria-hidden="true"></div>
"""


def lang_toggle(ctx, cls="lang-toggle"):
    label = ctx.x("العربية", "English")
    return (f'<a class="{cls}" href="{ctx.alt}" hreflang="{ctx.other}" lang="{ctx.other}" data-lang="{ctx.other}" '
            f'aria-label="{ctx.x("Switch to Arabic", "التبديل إلى الإنجليزية")}">{label}</a>')


def header(ctx, active):
    x = ctx.x
    links = "".join(
        f'<a href="{ctx.L}{h}"{" aria-current=page" if h == active else ""}><span class="btn__text"><span>{t}</span><span aria-hidden="true">{t}</span></span></a>'
        for h, t in nav_items(ctx))
    arrow = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M1 11L11 1M4 1h7v7"/></svg>'
    mlinks = "".join(
        f'<a class="big" href="{ctx.L}{h}"{" aria-current=page" if h == active else ""}>'
        f'<span class="mm__num" aria-hidden="true">{n:02d}</span><span class="mm__label">{t}</span>'
        f'<span class="mm__arrow" aria-hidden="true">{arrow}</span></a>'
        for n, (h, t) in enumerate(all_links(ctx), 1))
    return f"""<header class="header">
  <a class="header__logo" href="{ctx.L}index.html" aria-label="{x('Do Events — home', 'دو للمناسبات — الرئيسية')}">{LOGO}</a>
  <nav class="nav" aria-label="{x('Primary', 'القائمة الرئيسية')}">{links}</nav>
  <div class="header__cta">
    <button class="sound-toggle" type="button" aria-pressed="false" aria-label="{x('Background music on/off', 'تشغيل/إيقاف الموسيقى')}" title="{x('Music', 'الموسيقى')}"><span class="sound-toggle__bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>
    {lang_toggle(ctx)}
    {btn(x("Get in touch", "تواصل معنا"), ctx.L + "contact.html", dot=True)}
    <button class="burger" aria-label="{x('Menu', 'القائمة')}" aria-expanded="false" aria-controls="mmenu"><i></i><i></i></button>
  </div>
</header>
<div class="mmenu" id="mmenu">
  <p class="mm__eyebrow">{x('Menu', 'القائمة')}</p>
  <nav class="mm__list" aria-label="{x('Mobile menu', 'قائمة الجوال')}">{mlinks}</nav>
  <div class="mmenu__foot">
    <p class="mm__eyebrow">{x('Get in touch', 'تواصل معنا')}</p>
    <div class="mm__pills"><a href="{SITE['phone_href']}" dir="ltr">{SITE['phone']}</a><a href="{SITE['whatsapp_href']}" target="_blank" rel="noopener">{x('WhatsApp', 'واتساب')}</a><a href="{SITE['instagram']}" target="_blank" rel="noopener">{x('Instagram', 'إنستغرام')}</a>{lang_toggle(ctx, "lang-link")}</div>
  </div>
</div>
<div class="cursor-pill" aria-hidden="true"><span>{x('View project', 'شاهد المشروع')}</span><i></i></div>
"""


def cta(ctx):
    x = ctx.x
    if ctx.ar:
        ring = 'لنصنع معاً مناسبة <tspan class="hl">لا تُنسى</tspan> • مناسبتك <tspan class="hl">حقيقة</tspan> • لنصنع معاً مناسبة <tspan class="hl">لا تُنسى</tspan> • مناسبتك <tspan class="hl">حقيقة</tspan> •'
    else:
        ring = 'Let\'s create something <tspan class="hl">unforgettable</tspan> • your event is <tspan class="hl">reality</tspan> •'
    return f"""<section class="section--dark cta" aria-labelledby="cta-h">
  <div class="cta__circle" aria-hidden="true">
    <svg viewBox="0 0 1000 1000"><defs><path id="circ" d="M500,500 m-440,0 a440,440 0 1,1 880,0 a440,440 0 1,1 -880,0"/></defs>
      <text><textPath href="#circ" data-fit="2740"{x("", ' startOffset="100%"')}>{ring}</textPath></text>
    </svg>
  </div>
  <div class="wrap">
    <div class="cta__content">
      <h2 id="cta-h" class="sr-only">{x('Get in touch', 'تواصل معنا')}</h2>
      <p class="big" data-split>{x("Tell us about your <em>celebration</em>. We'll show you what's possible.", "حدّثنا عن <em>مناسبتك</em>، وسنريك ما هو ممكن.")}</p>
      <div class="btn-group" style="justify-content:center" data-fade>
        {btn(x("Get in touch", "تواصل معنا"), ctx.L + "contact.html", dot=True)}
        {btn(x("WhatsApp us", "راسلنا واتساب"), SITE['whatsapp_href'], "btn--ghost", arrow=True, attrs='target="_blank" rel="noopener"')}
      </div>
    </div>
  </div>
</section>
"""


def footer(ctx, active):
    x = ctx.x
    links = "".join(f'<a href="{ctx.L}{h}"{" aria-current=page" if h == active else ""}>{t}</a>' for h, t in all_links(ctx))
    a_attr, a_txt = alt(ctx, SITE["address"], SITE["address_ar"])
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__info">
        <div><h4>{x('Studio', 'الاستوديو')}</h4><address>{x(SITE['address'], SITE_AR['address'])}<span class="alt" {a_attr}>{a_txt}</span></address></div>
        <div><h4>{x('Contact', 'تواصل')}</h4><p><a href="{SITE['phone_href']}" dir="ltr">{SITE['phone']}</a><br><a href="{SITE['whatsapp_href']}" target="_blank" rel="noopener">{x('WhatsApp', 'واتساب')} <span dir="ltr">{SITE['whatsapp']}</span></a></p>
          <div class="socials">
            <a href="{SITE['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ICON['ig']}</a>
            <a href="{SITE['whatsapp_href']}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON['wa']}</a>
            <a href="https://www.youtube.com/watch?v={SITE['showreel_yt']}" target="_blank" rel="noopener" aria-label="YouTube">{ICON['yt']}</a>
          </div>
        </div>
      </div>
      <nav class="footer__links" aria-label="{x('Footer', 'روابط التذييل')}">{links}{lang_toggle(ctx, "lang-link")}</nav>
    </div>
    <div class="footer__legal"><span>© 2026 {x('Do Events · <span lang="ar">دو للمناسبات</span>', 'دو للمناسبات · <span lang="en">Do Events</span>')}</span><span>{x('Salalah, Sultanate of Oman', 'صلالة، سلطنة عُمان')}</span></div>
  </div>
  <div class="footer__giant wrap" aria-hidden="true">{MARK}</div>
</footer>
<audio id="bgm" src="{ctx.r}assets/audio/moment-of-peace.mp3" preload="auto" loop></audio>
<div class="lightbox" aria-hidden="true" role="dialog" aria-label="{x('Media viewer', 'عارض الوسائط')}">
  <button class="lightbox__close">{x('Close', 'إغلاق')}</button>
  <button class="lightbox__nav lightbox__nav--prev" aria-label="{x('Previous', 'السابق')}">&#8592;</button>
  <div class="lightbox__stage"></div>
  <button class="lightbox__nav lightbox__nav--next" aria-label="{x('Next', 'التالي')}">&#8594;</button>
</div>
<script src="{ctx.r}assets/vendor/gsap.min.js"></script>
<script src="{ctx.r}assets/vendor/ScrollTrigger.min.js"></script>
<script src="{ctx.r}assets/vendor/lenis.min.js"></script>
<script src="{ctx.r}{v("assets/js/main.js")}"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ case helpers
def ar_title(c):
    return YT[c["yt"]]["title"].split("|")[0].strip()


def cf(ctx, c):
    """Localised case fields."""
    if ctx.ar:
        t, cl, v, ex, sh = CASES_AR[c["slug"]]
        return dict(title=t, client=cl, venue=v, excerpt=ex, short=sh, cat=CATS_AR[c["cat"]], other=c["title"])
    return dict(title=c["title"], client=c["client"], venue=c["venue"], excerpt=c["excerpt"], short=c["short"],
                cat=CATS[c["cat"]], other=ar_title(c))


def poster(ctx, c):
    return f"{ctx.r}assets/img/poster/{c['slug']}.jpg"


def card(ctx, c, href=None):
    f = cf(ctx, c)
    href = href or f"{ctx.L}work/{c['slug']}.html"
    media = (f'<img src="{poster(ctx, c)}" alt="" loading="lazy">' if c["slug"] in NO_LOCAL_FILM else
             f'<video muted loop playsinline preload="none" poster="{poster(ctx, c)}" data-src="{ctx.r}assets/video/preview/{c["slug"]}.mp4"></video>')
    oattr = f'lang="{ctx.other}" dir="{"ltr" if ctx.ar else "rtl"}"'
    return f"""<div class="wcard-wrap" data-cat="{c['cat']}">
  <a class="wcard" href="{href}" data-cursor="{ctx.x('View project', 'شاهد المشروع')}">
    <div class="wcard__media">{media}<span class="chip">{f['cat']}</span></div>
    <div class="wcard__details">
      <h3 class="wcard__title">{e(f['title'])}<small {oattr}>{e(f['other'])}</small></h3>
      <div><p class="wcard__desc">{e(f['excerpt'])}</p><span class="wcard__client">{e(f['client'])}</span></div>
    </div>
  </a>
</div>"""


NOWRAP_SKIP = re.compile(r"<(script|style|textarea|option|title)\b[^>]*>.*?</\1>", re.S | re.I)
HYPHENATED = re.compile(r"(?<![\w-])([A-Za-z]+(?:-[A-Za-z]+)+[.,;:!?]?)(?![\w-])")


def keep_hyphenated_together(html_text):
    """Wrap hyphenated words (open-air, all-white…) in a no-wrap span so they never split across lines.
    Only text between tags in <body> is touched — never attributes, scripts or styles."""
    head, sep, body = html_text.partition("<body>")
    if not sep:
        return html_text
    keep = {}
    def stash(m):
        keep[f"\x00{len(keep)}\x00"] = m.group(0)
        return f"\x00{len(keep) - 1}\x00"
    body = NOWRAP_SKIP.sub(stash, body)
    parts = re.split(r"(<[^>]+>)", body)
    for i in range(0, len(parts), 2):
        parts[i] = HYPHENATED.sub(r'<span class="nw">\1</span>', parts[i])
    body = "".join(parts)
    for k, v in keep.items():
        body = body.replace(k, v)
    return head + sep + body


def write(path, s):
    if path.endswith(".html"):
        s = keep_hyphenated_together(s)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf8").write(s)


def out_path(ctx):
    return ("ar/" if ctx.ar else "") + ctx.page


LD = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"Do Events","alternateName":"دو للمناسبات","description":"Event management company in Salalah, Oman — weddings, festivals, corporate and government events.","telephone":"+968 9551 3848","address":{"@type":"PostalAddress","streetAddress":"23 July Street, Way 13408","addressLocality":"Salalah","addressCountry":"OM"},"sameAs":["https://www.instagram.com/do.events_oman/"],"foundingDate":"2018"}</script>"""


def client_item(ctx, c):
    """Logo if a file exists in assets/img/clients/; brands without a logo file are skipped."""
    name = c["ar"] if ctx.ar else c["en"]
    for ext in ("svg", "png", "webp"):
        rel = f"assets/img/clients/{c['logo']}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return f'<span class="ticker__item ticker__item--logo" data-client="{c["key"]}"><img src="{ctx.r}{rel}" alt="{e(name)}" loading="eager" decoding="async"></span>'
    return ""  # no logo file yet — leave it out rather than mixing text with logos


# ------------------------------------------------------------------ HOME
def home(lang):
    ctx = Ctx(lang, "index.html"); x = ctx.x; r = ctx.r
    tick = "".join(client_item(ctx, c) for c in CLIENT_LOGOS) * 4
    feats = "\n".join(card(ctx, BY[s]) for s in FEATURED)
    ig_pick = [("theater-festival", 2), ("white-millennium", 3), ("garden-wedding", 2), ("triple-wedding", 4), ("beach-engagement", 1),
               ("red-rose", 3), ("albarami-lounge", 2), ("mymoon-launch", 1), ("green-wedding", 5), ("royal-blue", 3), ("gold-purple", 4), ("theater-red-carpet", 5)]
    rail = "".join(
        f'<a class="ig" href="{SITE["instagram"]}" target="_blank" rel="noopener"><img src="{r}assets/img/gallery/{s}-{i}.jpg" alt="{e(cf(ctx, BY[s])["title"])}" loading="lazy"><figcaption><span>{e(cf(ctx, BY[s])["venue"])}</span><span>{e(cf(ctx, BY[s])["short"])}</span></figcaption></a>'
        for s, i in ig_pick)
    oattr = f'lang="{ctx.other}"'
    body = f"""{head(ctx, x("Do Events — Luxury Weddings & Event Management in Salalah, Oman", "دو للمناسبات — تنظيم حفلات الزفاف والفعاليات الفاخرة في صلالة، عُمان"),
        x("Do Events (دو للمناسبات) is a premium event management company in Salalah, Oman — luxury weddings, festivals, brand launches and official ceremonies, from concept to reality.",
          "دو للمناسبات شركة تنظيم فعاليات ومناسبات فاخرة في صلالة — حفلات الزفاف والمهرجانات وتدشين المنتجات والمناسبات الرسمية، من الفكرة إلى الحقيقة."), loader=True, ld=LD)}
{header(ctx, "index.html")}
<main id="main">
<section class="hero">
  <div class="hero__media"><video autoplay muted loop playsinline preload="auto" poster="{r}assets/img/poster/hero.jpg" data-autoplay><source src="{r}assets/video/hero.mp4" type="video/mp4"></video></div>
  <div class="hero__inner wrap">
    <h1 class="h-display" data-split="load">{x("We turn your vision into <em>unforgettable celebrations</em> across Oman", "نحوّل رؤيتك إلى <em>احتفالات لا تُنسى</em> في أرجاء عُمان")}</h1>
    <div class="hero__bottom">
      <div class="hero__ticker ticker" data-fade="load" aria-label="{x('Selected clients and events', 'عملاء وفعاليات مختارة')}"><div class="ticker__track">{tick}</div></div>
    </div>
  </div>
</section>

<section class="section section--dark about center">
  <div class="wrap">
    <div class="about__icon" data-fade>{LOGO}</div>
    <h2 class="h3" data-split>{x("From the first sketch to the final guest, we design moments that <em>spark emotion</em>, <em>honour heritage</em> and become <em>lasting memories</em>.",
                                 "من أول فكرة حتى آخر ضيف، نصمّم لحظات <em>تلامس المشاعر</em> <em>وتحتفي بالأصالة</em> وتبقى <em>ذكرى خالدة</em>.")}</h2>
    <p class="lede" data-fade>{x("Founded in Salalah in 2018 and awarded first place for Best SME in 2021, our team of Omani specialists blends authenticity with modern design — so every event reflects its own character, and nothing is left to chance.",
                                 "تأسست دو للمناسبات في صلالة عام 2018، وحصلت على المركز الأول كأفضل مؤسسة صغيرة ومتوسطة عام 2021. يمزج فريقنا من المختصين العُمانيين بين الأصالة والتصميم العصري — لتعكس كل فعالية شخصيتها الخاصة، دون ترك أي تفصيل للصدفة.")}</p>
  </div>
</section>

<section class="section on-light path">
  <div class="wrap path__grid">
    <div class="path__item">
      {mtag(x("For Weddings", "حفلات الزفاف"))}
      <h2 class="h1" data-split>{x("Luxury <em>weddings</em> &amp; private celebrations", "حفلات <em>زفاف</em> فاخرة ومناسبات خاصة")}</h2>
      <div data-fade>{btn(x("Learn more", "اكتشف المزيد"), ctx.L + "weddings.html", "btn--dark", arrow=True)}</div>
    </div>
    <div class="path__slash" aria-hidden="true">/</div>
    <div class="path__item">
      {mtag(x("For Corporate", "للشركات والجهات"))}
      <h2 class="h1" data-split>{x("Festivals, launches &amp; <em>official</em> events", "مهرجانات وتدشين منتجات <em>ومناسبات رسمية</em>")}</h2>
      <div data-fade>{btn(x("Learn more", "اكتشف المزيد"), ctx.L + "corporate.html", "btn--ghost", arrow=True)}</div>
    </div>
  </div>
</section>

<section class="section work">
  <div class="wrap">
    <div class="work__head">
      <div>
        <h2 class="h2" data-split>{x("From intimate <em>engagements</em> to national <em>festivals</em>.", "من حفلات <em>الخطوبة</em> الحميمة إلى <em>المهرجانات</em> الوطنية.")}</h2>
        <p class="lede" style="margin-top:22px" data-fade>{x("We turn ideas into moments people talk about — across Salalah and the Dhofar governorate.", "نحوّل الأفكار إلى لحظات يتحدث عنها الجميع — في صلالة وأرجاء محافظة ظفار.")}</p>
      </div>
      <div data-fade>{btn(x("View our work", "شاهد أعمالنا"), ctx.L + "work.html", "btn--ghost", arrow=True)}</div>
    </div>
    <div class="work__list">
{feats}
    </div>
    <div class="work__more">{btn(x("All case studies", "جميع الأعمال"), ctx.L + "work.html", dot=True)}</div>
  </div>
</section>

<section class="section on-light follow">
  <div class="wrap">
    <div class="follow__head">
      <div>{mtag(x("Follow us", "تابعنا"))}<h2 class="h2" data-split>{x("Step inside the worlds we <em>create</em>.", "ادخل إلى العوالم التي <em>نصنعها</em>.")}</h2></div>
      <div>
        <p class="lede" data-fade>{x("Our Instagram is a window into the craft — overnight builds, kosha reveals and the quiet details guests remember.", "حسابنا على إنستغرام نافذة على حرفتنا — تجهيزات الليالي الطويلة، ولحظات كشف الكوشة، والتفاصيل الهادئة التي يتذكرها الضيوف.")}</p>
        <div style="margin-top:22px" data-fade>{btn(f'<span dir="ltr">{SITE["instagram_handle"]}</span>', SITE['instagram'], "btn--dark", arrow=True, attrs='target="_blank" rel="noopener"')}</div>
      </div>
    </div>
  </div>
  <div class="follow__rail">{rail}</div>
</section>

{cta(ctx)}
</main>
{footer(ctx, "index.html")}"""
    write(out_path(ctx), body)


# ------------------------------------------------------------------ WORK LIST
def work(lang):
    ctx = Ctx(lang, "work.html"); x = ctx.x
    cats = CATS_AR if ctx.ar else CATS
    counts = {k: sum(1 for c in CASES if c["cat"] == k) for k in CATS}
    fbtn = f'<button data-filter="all" aria-pressed="true">{x("All", "الكل")}<sup>{len(CASES)}</sup></button>' + "".join(
        f'<button data-filter="{k}" aria-pressed="false">{v}<sup>{counts[k]}</sup></button>' for k, v in cats.items())
    cards = "\n".join(card(ctx, c) for c in CASES)
    body = f"""{head(ctx, x("Case Studies — Do Events | Weddings & Events in Salalah", "أعمالنا — دو للمناسبات | حفلات الزفاف والفعاليات في صلالة"),
        x("Explore Do Events case studies — luxury weddings, beach engagements, the Dhofar International Theater Festival and brand launches across Salalah, Oman.",
          "استكشف أعمال دو للمناسبات — حفلات زفاف فاخرة وخطوبة على الشاطئ ومهرجان ظفار الدولي للمسرح وتدشين العلامات التجارية في صلالة."))}
{header(ctx, "work.html")}
<main id="main">
<section class="phero phero--center">
  <div class="wrap">
    {mtag(x("Case studies", "أعمالنا"), "mtag--center")}
    <h1 class="h-display phero__title" data-split="load">{x("Moments we've <em>brought to life</em>", "لحظات <em>صنعناها</em> بشغف")}</h1>
    <p class="phero__ar" lang="{ctx.other}" data-fade="load">{x("أعمالنا — من الفكرة إلى الحقيقة", "Moments we've brought to life")}</p>
    <div class="filters" data-fade="load" role="group" aria-label="{x('Filter case studies', 'تصفية الأعمال')}">{fbtn}</div>
  </div>
</section>
<section class="section work" style="padding-top:40px">
  <div class="wrap"><div class="cases">
{cards}
  </div></div>
</section>
{cta(ctx)}
</main>
{footer(ctx, "work.html")}"""
    write(out_path(ctx), body)


# ------------------------------------------------------------------ CASE PAGES
def case_page(lang, i, c):
    ctx = Ctx(lang, f"work/{c['slug']}.html"); x = ctx.x; r = ctx.r
    f = cf(ctx, c)
    y = YT[c["yt"]]
    paras = lambda s: "".join(f"<p>{e(p)}</p>" for p in s.split("\n\n"))
    lis = lambda l: "".join(f"<li>{e(v)}</li>" for v in l)
    en_blocks = (f'<div class="block" lang="en" dir="ltr"><div><h2 data-split>Overview</h2></div><div data-fade>{paras(y["story_en"])}</div></div>'
                 f'<div class="block" lang="en" dir="ltr"><div><h2 data-split>The <em>highlights</em></h2></div><div data-fade><ul class="checks">{lis(y["hl_en"])}</ul></div></div>')
    ar_blocks = (f'<div class="block" lang="ar" dir="rtl"><div><h2 data-split>نظرة عامة</h2></div><div data-fade>{paras(y["story_ar"])}</div></div>'
                 f'<div class="block" lang="ar" dir="rtl"><div><h2 data-split>أبرز <em>التفاصيل</em></h2></div><div data-fade><ul class="checks">{lis(y["hl_ar"])}</ul></div></div>')
    # primary language first, the other language after it
    if ctx.ar:
        blocks = ar_blocks + en_blocks.replace('class="block"', 'class="block block--alt"', 1)
    else:
        blocks = en_blocks + ar_blocks.replace('class="block"', 'class="block block--alt"', 1)
    nxt = CASES[(i + 1) % len(CASES)]
    nf = cf(ctx, nxt)
    local = c["slug"] not in NO_LOCAL_FILM
    film_attr = (f'data-film="{r}assets/video/full/{c["slug"]}.mp4" data-poster="{poster(ctx, c)}"' if local else f'data-film data-yt="{c["yt"]}"')
    media = (f'<video muted loop playsinline autoplay preload="auto" poster="{poster(ctx, c)}" data-autoplay><source src="{r}assets/video/preview/{c["slug"]}.mp4" type="video/mp4"></video>'
             if local else f'<img src="{poster(ctx, c)}" alt="">')
    gal = ""
    if local:
        imgs = "".join(
            f'<button data-gallery="g" data-full="{r}assets/img/gallery/{c["slug"]}-{k}.jpg" aria-label="{x("Open image", "عرض الصورة")} {k}"><img src="{r}assets/img/gallery/{c["slug"]}-{k}.jpg" alt="{e(f["title"])} — {x("detail", "تفصيل")} {k}" loading="lazy"></button>'
            for k in range(1, 7))
        gal = f"""<div class="block" style="grid-template-columns:1fr"><div><h2 data-split>{x("In <em>detail</em>", "في <em>التفاصيل</em>")}</h2></div><div class="gallery" data-fade>{imgs}</div></div>"""
    year = c["year"] or "—"
    desc = NOEMOJI.sub("", y["tag_ar"] if ctx.ar else y["tag_en"]).strip()
    body = f"""{head(ctx, f"{f['title']} — {f['client']} | " + x("Do Events Salalah", "دو للمناسبات صلالة"), desc, og=f"assets/img/poster/{c['slug']}.jpg")}
{header(ctx, "work.html")}
<main id="main">
<section class="phero">
  <div class="wrap">
    {mtag(x("Case study", "دراسة حالة") + " · " + f['cat'])}
    <h1 class="h1 phero__title" data-split="load">{e(f['title'])}</h1>
    <p class="phero__ar" lang="{ctx.other}" dir="{x('rtl', 'ltr')}" data-fade="load">{e(f['other'])}</p>
    <dl class="phero__meta" data-fade="load">
      <div><dt>{x('Client', 'العميل')}</dt><dd>{e(f['client'])}</dd></div>
      <div><dt>{x('Location', 'الموقع')}</dt><dd>{e(f['venue'])}</dd></div>
      <div><dt>{x('Category', 'الفئة')}</dt><dd>{f['cat']}</dd></div>
      <div><dt>{x('Year', 'السنة')}</dt><dd>{year}</dd></div>
    </dl>
  </div>
</section>
<section class="section--dark" style="padding-bottom:clamp(70px,9vw,120px)">
  <div class="wrap">
    <div class="film" data-fade="load">
      {media}
      <button class="film__play" {film_attr} aria-label="{x('Play the film', 'تشغيل الفيلم')}">{ICON['play']}</button>
      <span class="chip film__label">{x('Watch the film', 'شاهد الفيلم')}</span>
    </div>
  </div>
</section>
<section class="section on-light" style="padding-top:clamp(40px,5vw,70px)">
  <div class="wrap">
    {blocks}
    {gal}
    <div class="block" style="grid-template-columns:1fr;text-align:center"><div data-fade>{btn(x("Watch on YouTube", "شاهد على يوتيوب"), f"https://www.youtube.com/watch?v={c['yt']}", "btn--ghost", arrow=True, attrs='target="_blank" rel="noopener"')}</div></div>
  </div>
</section>
<section class="section work">
  <div class="wrap">
    <a class="next" href="{nxt['slug']}.html" data-cursor="{x('Next project', 'المشروع التالي')}">
      {mtag(x("Next project", "المشروع التالي"), "mtag--center")}
      <p class="next__title">{e(nf['title'])}</p>
    </a>
    <div class="work__list">{card(ctx, nxt, href=nxt['slug'] + '.html')}</div>
  </div>
</section>
{cta(ctx)}
</main>
{footer(ctx, "work.html")}"""
    write(out_path(ctx), body)


# ------------------------------------------------------------------ SERVICES PAGES
STEPS = [
    (("Consult", "We listen first — your story, guests, venue, culture and budget — and shape a clear brief together."),
     ("الاستشارة", "نبدأ بالإصغاء — قصتكم وضيوفكم والمكان والثقافة والميزانية — ونصوغ معاً تصوراً واضحاً.")),
    (("Design", "Mood boards, 3D concepts, florals, lighting and stationery, refined until every detail feels like you."),
     ("التصميم", "لوحات إلهام وتصاميم ثلاثية الأبعاد وتنسيقات الورد والإضاءة والمطبوعات، حتى يعبّر كل تفصيل عنكم.")),
    (("Build", "Our in-house crew constructs the stage, kosha, runway and installations on site, overnight if needed."),
     ("التنفيذ", "يبني فريقنا المسرح والكوشة والممر والتجهيزات في الموقع، حتى لو تطلّب ذلك العمل طوال الليل.")),
    (("Celebrate", "We run the day — guests, hospitality, timings and teardown — while you enjoy every moment."),
     ("الاحتفال", "ندير يومكم بالكامل — الضيوف والضيافة والتوقيت والتفكيك — لتستمتعوا بكل لحظة.")),
]

WEDDING_SVCS = [
    ("Kosha &amp; stage design", "Sculpted seating, bespoke backdrops and statement stages built around the couple.",
     "تصميم الكوشة والمسرح", "مقاعد منحوتة وخلفيات مصممة خصيصاً ومسارح لافتة تتمحور حول العروسين."),
    ("Runways &amp; dance floors", "Mirror-black, marble and glossy white runways with LED edges and fog reveals.",
     "الممرات وأرضيات الرقص", "ممرات سوداء كالمرآة ورخامية وبيضاء لامعة بحواف مضيئة وتأثيرات الضباب."),
    ("Ceiling installations", "Crystal strands, suspended blossoms, vines and ribbon sculptures overhead.",
     "تجهيزات الأسقف المعلّقة", "خيوط كريستالية وزهور معلّقة وأغصان ومنحوتات من الأشرطة فوق الرؤوس."),
    ("Florals", "Lush, seasonal arrangements — from blush roses to emerald garden themes.",
     "تنسيق الورود", "تنسيقات غنية وموسمية — من الورد الوردي الناعم إلى ثيمات الحدائق الزمردية."),
    ("Table styling", "Chargers, glassware, candelabra, linens and custom printed place cards.",
     "تنسيق الطاولات", "صحون تقديم وكؤوس وشمعدانات ومفارش وبطاقات أماكن مطبوعة خصيصاً."),
    ("Lighting &amp; LED screens", "Mood lighting, illuminated monograms and stage screens with custom visuals.",
     "الإضاءة والشاشات", "إضاءة للأجواء وشعارات مضيئة وشاشات مسرح بمحتوى مرئي مخصص."),
    ("Lounges &amp; furniture", "Curved lounges, VIP seating and side tables curated to your palette.",
     "الجلسات والأثاث الفاخر", "جلسات منحنية ومقاعد لكبار الشخصيات وطاولات جانبية بألوان مناسبتكم."),
    ("Hospitality &amp; sweets", "Dessert carts, Omani sweets, cakes and DO Chocolates &amp; Flowers gifting.",
     "الضيافة والحلويات", "عربات الحلويات والحلويات العُمانية والكيك وهدايا دو للشوكولاتة والزهور."),
    ("Engagements &amp; beach events", "Clear-top marquees and outdoor celebrations on the Salalah shoreline.",
     "حفلات الخطوبة والشاطئ", "خيام شفافة واحتفالات خارجية على شاطئ صلالة."),
]

CORP_SVCS = [
    ("Government &amp; official events", "Protocol-ready ceremonies under royal and ministerial patronage.",
     "الفعاليات الحكومية والرسمية", "مراسم جاهزة وفق البروتوكول تحت الرعاية السامية والوزارية."),
    ("Conferences &amp; forums", "Stages, panels, LED screens and delegate hospitality for multi-day programmes.",
     "المؤتمرات والمنتديات", "مسارح وجلسات نقاش وشاشات LED وضيافة للمشاركين في البرامج متعددة الأيام."),
    ("Festivals &amp; culture", "Entrance arches, red carpets, media walls and open-air gala dinners.",
     "المهرجانات والفعاليات الثقافية", "أقواس مداخل وسجاد أحمر وجدران إعلامية وعشاءات احتفالية في الهواء الطلق."),
    ("Product launches", "Branded backdrops, reveal moments and VIP lounges that fit the brand.",
     "تدشين المنتجات", "خلفيات بهوية العلامة ولحظات كشف وجلسات لكبار الشخصيات تليق بالعلامة."),
    ("Openings &amp; exhibitions", "Booths, signage and guest journeys for openings and trade shows.",
     "الافتتاحات والمعارض", "أجنحة ولافتات ومسارات للضيوف في الافتتاحات والمعارض التجارية."),
    ("Stage, sound &amp; lighting", "High-quality screens, lighting systems, stage platforms and advanced sound.",
     "المسرح والصوت والإضاءة", "شاشات وأنظمة إضاءة عالية الجودة ومنصات مسرح وأنظمة صوت متقدمة."),
    ("VIP furniture", "Luxury chairs, VIP tables and outdoor serving tables.",
     "الأثاث وطاولات كبار الشخصيات", "كراسٍ فاخرة وطاولات VIP وطاولات تقديم خارجية."),
    ("Hospitality", "Coffee service, Omani sweets, cakes and premium chocolate gifting.",
     "الضيافة", "خدمة القهوة والحلويات العُمانية والكيك وهدايا الشوكولاتة الفاخرة."),
    ("Graduations &amp; honouring", "Graduations, Teachers' Day and honouring ceremonies with full production.",
     "حفلات التخرج والتكريم", "حفلات تخرج ويوم المعلم ومراسم تكريم بإنتاج متكامل."),
]


def notable_list(ctx):
    items = NOTABLE_AR if ctx.ar else NOTABLE
    return "".join(f'<li data-fade><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in items)


def services_page(lang, fname, title, meta, tag, h1, h1_alt, video, expand_h, expand_p, svcs, feats, extra=""):
    ctx = Ctx(lang, fname); x = ctx.x; r = ctx.r
    items = ""
    for n, (te, de, ta, da) in enumerate(svcs, 1):
        t, d, o = (ta, da, te) if ctx.ar else (te, de, ta)
        items += f'<div class="svc__item" data-fade><span class="svc__num">{n:02d}</span><h3>{t}</h3><p>{d}</p><span class="alt" lang="{ctx.other}">{o}</span></div>'
    st = "".join(f'<div class="step" data-fade><div><h3>{(a if ctx.ar else en)[0]}</h3><p>{(a if ctx.ar else en)[1]}</p></div></div>' for en, a in STEPS)
    cards = "\n".join(card(ctx, BY[s]) for s in feats)
    body = f"""{head(ctx, x(*title), x(*meta))}
{header(ctx, fname)}
<main id="main">
<section class="expand">
  <div class="expand__stick">
    <div class="expand__title"><div>{mtag(x(*tag), "mtag--center")}<div style="height:28px"></div><h1 class="h-display" data-split="load">{x(*h1)}</h1><p class="phero__ar" lang="{ctx.other}" data-fade="load">{h1_alt[0] if ctx.ar else h1_alt[1]}</p></div></div>
    <div class="expand__media"><video muted loop playsinline autoplay preload="auto" poster="{r}assets/img/poster/{video}.jpg" data-autoplay><source src="{r}assets/video/preview/{video}.mp4" type="video/mp4"></video></div>
    <div class="expand__copy"><p class="h3" style="max-width:20ch">{x(*expand_h)}</p><p>{x(*expand_p)}</p></div>
  </div>
</section>
<section class="section on-light">
  <div class="wrap">
    <div class="work__head"><h2 class="h2" data-split>{x("What we <em>design</em> &amp; deliver", "ما <em>نصمّمه</em> وننفّذه")}</h2><div data-fade>{btn(x("Plan your event", "خطّط لمناسبتك"), ctx.L + "contact.html", "btn--dark", dot=True)}</div></div>
    <div class="svc">{items}</div>
  </div>
</section>
{extra}
<section class="section section--dark">
  <div class="wrap">
    <div class="work__head"><h2 class="h2" data-split>{x("How we <em>work</em>", "كيف <em>نعمل</em>")}</h2><p class="lede" data-fade>{x("One dedicated team from first meeting to final pack-down — so you can be a guest at your own event.", "فريق واحد مخصّص من أول لقاء حتى آخر لحظة — لتكون ضيفاً في مناسبتك.")}</p></div>
    <div class="steps">{st}</div>
  </div>
</section>
<section class="section work">
  <div class="wrap">
    <div class="work__head"><h2 class="h2" data-split>{x("Selected <em>work</em>", "أعمال <em>مختارة</em>")}</h2><div data-fade>{btn(x("All case studies", "جميع الأعمال"), ctx.L + "work.html", "btn--ghost", arrow=True)}</div></div>
    <div class="work__list">{cards}</div>
  </div>
</section>
{cta(ctx)}
</main>
{footer(ctx, fname)}"""
    write(out_path(ctx), body)


def weddings(lang):
    services_page(lang, "weddings.html",
                  ("Luxury Wedding Planning & Décor in Salalah — Do Events", "تنسيق وديكور حفلات الزفاف الفاخرة في صلالة — دو للمناسبات"),
                  ("Luxury wedding décor, kosha design, florals, table styling and hospitality in Salalah, Oman — designed and delivered by Do Events.",
                   "ديكور حفلات الزفاف الفاخرة وتصميم الكوشة وتنسيق الورود والطاولات والضيافة في صلالة — من تصميم وتنفيذ دو للمناسبات."),
                  ("For Weddings", "حفلات الزفاف"),
                  ("Weddings worthy of <em>your story</em>", "حفلات زفاف تليق <em>بقصتكم</em>"),
                  ("Weddings worthy of your story", "حفلات الزفاف والخطوبة"),
                  "gold-purple",
                  ("From kosha to ceiling, every detail designed in-house.", "من الكوشة إلى السقف، كل تفصيل نصمّمه بأيدينا."),
                  ("Signature wedding halls across Salalah — each with its own palette, story and atmosphere.", "قاعات زفاف مميّزة في أرجاء صلالة — لكلٍّ منها ألوانها وقصتها وأجواؤها."),
                  WEDDING_SVCS, ["triple-wedding", "royal-blue", "white-millennium", "beach-engagement"])


def corporate(lang):
    ctx = Ctx(lang, "corporate.html"); x = ctx.x
    extra = f"""<section class="section on-light" style="padding-top:0">
  <div class="wrap">
    <div class="work__head"><h2 class="h2" data-split>{x("Trusted for <em>official</em> occasions", "موضع ثقة في <em>المناسبات الرسمية</em>")}</h2><p class="lede" data-fade>{x("A selection of events delivered for government bodies, universities and leading organisations in Dhofar.", "مختارات من الفعاليات التي نفّذناها للجهات الحكومية والجامعات والمؤسسات الرائدة في ظفار.")}</p></div>
    <ul class="notable">{notable_list(ctx)}</ul>
  </div>
</section>"""
    services_page(lang, "corporate.html",
                  ("Corporate, Government & Festival Events in Oman — Do Events", "فعاليات الشركات والجهات الحكومية والمهرجانات في عُمان — دو للمناسبات"),
                  ("Conferences, festivals, product launches and official ceremonies in Salalah — staging, lighting, hospitality and full production by Do Events.",
                   "مؤتمرات ومهرجانات وتدشين منتجات ومناسبات رسمية في صلالة — مسارح وإضاءة وضيافة وإنتاج متكامل من دو للمناسبات."),
                  ("For Corporate", "للشركات والجهات"),
                  ("Festivals, launches &amp; <em>official</em> ceremonies", "مهرجانات وتدشين منتجات <em>ومناسبات رسمية</em>"),
                  ("Festivals, launches & official ceremonies", "الفعاليات الحكومية والمؤتمرات والمهرجانات"),
                  "theater-festival",
                  ("Production you can count on.", "إنتاج يمكنك الاعتماد عليه."),
                  ("From the Dhofar International Theater Festival to ministry ceremonies — on time, on brand, on protocol.",
                   "من مهرجان ظفار الدولي للمسرح إلى احتفالات الوزارات — في الموعد، وبهوية العلامة، ووفق البروتوكول."),
                  CORP_SVCS, ["theater-festival", "theater-red-carpet", "mymoon-launch"], extra)


# ------------------------------------------------------------------ ABOUT
def about(lang):
    ctx = Ctx(lang, "about.html"); x = ctx.x
    why_en = [
        "Venues equipped with the latest technology — stage, sound and lighting — blending authenticity, modernity and Omani heritage.",
        "Every event designed from scratch: conferences, government occasions and private celebrations alike.",
        "Complete logistics handled in-house, to the highest standards of organisation.",
        "We care about every detail — because we are partners in your event, not just its organisers.",
    ]
    why_ar = [
        "قاعات مجهّزة بأحدث التقنيات من مسرح وصوت وإضاءة، تجمع بين الأصالة والحداثة والتراث والثقافة العُمانية.",
        "نصمّم كل فعالية من البداية، سواء أكانت مؤتمراً أو فعالية حكومية أو مناسبة خاصة كحفلات الزفاف.",
        "نوفّر كافة الخدمات اللوجستية التي تحتاجها القاعة وبأعلى درجات التنظيم.",
        "نهتم بتنفيذ تفاصيل الفعالية لإنجاحها، لأننا نعتبر أنفسنا شركاء في الحدث وليس مجرد منظّمين.",
    ]
    story_en = """<p>Do Events was founded in 2018 and quickly established itself as a leader in planning and organising events. From day one we have shaped events through a modern vision built on credibility, organisation and precision.</p>
      <p>Every event begins with planning, design and study — so the result reflects its own character and guarantees its success. We offer a complete suite of services that make every occasion unforgettable and exceptional.</p>
      <p>In 2021, Do Events won first place as the best small and medium enterprise, under the patronage of H.E. Sayyid Saeed bin Sultan, Undersecretary of the Ministry of Culture, Sports and Youth. Our work is delivered by a team of Omani specialists who craft a dedicated plan for every event — a company built by Omani hands.</p>"""
    story_ar = """<p>تأسست شركتنا في عام 2018 وسرعان ما أثبتت نفسها كقائدة في صناعة تخطيط وتنظيم الفعاليات، وعملت منذ بداية تأسيسها على تنظيم الفعاليات برؤية عصرية تتضمن المصداقية والتنظيم والدقة.</p>
      <p>تعمل الشركة في رؤية تنطلق من التخطيط والتصميم ودراسة كل فعالية بشكل يعكس طبيعتها ويضمن نجاحها، لذلك نقدّم مجموعة شاملة من الخدمات المصمّمة لجعل كل فعالية لا تُنسى واستثنائية.</p>
      <p>وقد حصلت شركة دو على المركز الأول كأفضل مؤسسة من المؤسسات الصغيرة والمتوسطة عام 2021 تحت رعاية سعادة السيد سعيد بن سلطان، وكيل وزارة الثقافة والرياضة والشباب. وتعمل الشركة مع فريق من المختصين العُمانيين لإعداد المخططات الخاصة بكل فعالية، لتكون الشركة صرحاً مميزاً بأيادي شباب عُماني.</p>"""
    lis = lambda l: "".join(f"<li>{v}</li>" for v in l)
    choc = SITE["chocolate"]
    sister = x(f"Our hospitality signature — premium chocolates, Omani sweets, cakes and floral gifting — comes from our sister house, DO Chocolates &amp; Flowers ({choc}).",
               f'توقيعنا في الضيافة — أفخم أنواع الشوكولاتة والحلويات العُمانية والكيك وتنسيقات الزهور — يأتي من علامتنا الشقيقة دو للشوكولاتة والزهور (<span dir="ltr">{choc}</span>).')
    primary = (f'<div class="block"><div><h2 data-split>{x("Our <em>story</em>", "<em>قصتنا</em>")}</h2></div><div data-fade>{x(story_en, story_ar)}</div></div>'
               f'<div class="block"><div><h2 data-split>{x("Why <em>Do Events</em>", "لماذا <em>دو للمناسبات</em>؟")}</h2></div><div data-fade><ul class="checks">{lis(why_ar if ctx.ar else why_en)}</ul></div></div>')
    secondary = (f'<div class="block block--alt" lang="en" dir="ltr"><div><h2 data-split>Who we are</h2></div><div data-fade>{story_en}</div></div>' if ctx.ar else
                 f'<div class="block block--alt" lang="ar" dir="rtl"><div><h2 data-split>من نحن</h2></div><div data-fade>{story_ar}</div></div>')
    body = f"""{head(ctx, x("About Do Events — Omani Event House in Salalah since 2018", "من نحن — دو للمناسبات، بيت فعاليات عُماني في صلالة منذ 2018"),
        x("Founded in 2018, Do Events is an Omani event management company in Salalah — Best SME 2021 — delivering weddings, conferences and official events.",
          "تأسست دو للمناسبات عام 2018، وهي شركة عُمانية لتنظيم الفعاليات في صلالة — حاصلة على المركز الأول كأفضل مؤسسة صغيرة ومتوسطة 2021."))}
{header(ctx, "about.html")}
<main id="main">
<section class="phero">
  <div class="wrap">
    {mtag(x("About Do Events", "عن دو للمناسبات"))}
    <h1 class="h1 phero__title" data-split="load">{x("An Omani event house built on <em>credibility</em> and craft", "بيت فعاليات عُماني قائم على <em>المصداقية</em> والإتقان")}</h1>
    <p class="phero__ar" lang="{ctx.other}" data-fade="load">{x("شركة دو للفعاليات — متخصصون بتنظيم الحفلات والمؤتمرات", "An Omani event house built on credibility and craft")}</p>
  </div>
</section>
<section class="section--dark" style="padding-bottom:clamp(80px,10vw,140px)">
  <div class="wrap">
    <div class="stats" data-fade>
      <div class="stat"><b>2018</b><span>{x("Founded in Salalah", "التأسيس في صلالة")}</span></div>
      <div class="stat"><b>{x("1<em>st</em>", "<em>الأول</em>")}</b><span>{x("Best SME Award 2021", "أفضل مؤسسة صغيرة ومتوسطة 2021")}</span></div>
      <div class="stat"><b>360°</b><span>{x("Concept to execution", "من الفكرة إلى التنفيذ")}</span></div>
      <div class="stat"><b><em>{x("Omani", "عُماني")}</em></b><span>{x("Specialist team", "فريق من المختصين")}</span></div>
    </div>
  </div>
</section>
<section class="section on-light" style="padding-top:clamp(40px,5vw,70px)">
  <div class="wrap">
    {primary}
    {secondary}
  </div>
</section>
<section class="section section--dark center">
  <div class="wrap"><p class="quote" data-split>{x("We are <em>partners</em> in your event — not just its organisers.", "نحن <em>شركاء</em> في مناسبتك — ولسنا مجرد منظّمين.")}</p></div>
</section>
<section class="section on-light">
  <div class="wrap">
    <div class="work__head"><h2 class="h2" data-split>{x("Events we're <em>proud</em> of", "فعاليات <em>نفخر</em> بها")}</h2><p class="lede" data-fade>{x("Over the years we have organised many distinguished events, including:", "على مدى السنوات، نظّمنا العديد من الفعاليات المرموقة، منها:")}</p></div>
    <ul class="notable">{notable_list(ctx)}</ul>
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="block" style="border:0;padding:0"><div><h2 data-split>{x("Sister brand: <em>DO Chocolates &amp; Flowers</em>", "علامتنا الشقيقة: <em>دو للشوكولاتة والزهور</em>")}</h2></div><div data-fade>
      <p>{sister}</p>
      <div class="btn-group">{btn(x("Our services", "خدماتنا"), ctx.L + "weddings.html", "btn--dark", arrow=True)}{btn(x("Contact us", "تواصل معنا"), ctx.L + "contact.html", "btn--ghost", arrow=True)}</div>
    </div></div>
  </div>
</section>
{cta(ctx)}
</main>
{footer(ctx, "about.html")}"""
    write(out_path(ctx), body)


# ------------------------------------------------------------------ CONTACT
def contact(lang):
    ctx = Ctx(lang, "contact.html"); x = ctx.x
    types_en = ["Wedding", "Engagement", "Corporate event", "Government / official ceremony", "Conference", "Festival", "Product launch", "Graduation", "Other"]
    types_ar = ["حفل زفاف", "حفل خطوبة", "فعالية شركة", "مناسبة حكومية / رسمية", "مؤتمر", "مهرجان", "تدشين منتج", "حفل تخرج", "أخرى"]
    types = "".join(f"<option>{t}</option>" for t in (types_ar if ctx.ar else types_en))
    msg = json.dumps(dict(
        intro=x("Hello Do Events, I would like to enquire about an event.", "مرحباً دو للمناسبات، أودّ الاستفسار عن مناسبة."),
        name=x("Name", "الاسم"), phone=x("Phone", "الهاتف"), type=x("Event type", "نوع المناسبة"),
        date=x("Date", "التاريخ"), guests=x("Guests", "عدد الضيوف"), message=x("Details", "التفاصيل")), ensure_ascii=False)
    a_attr, a_txt = alt(ctx, SITE["address"], SITE["address_ar"])
    body = f"""{head(ctx, x("Contact Do Events — Event Management in Salalah, Oman", "تواصل مع دو للمناسبات — تنظيم الفعاليات في صلالة، عُمان"),
        x("Plan your wedding or event with Do Events. Visit us at 23 July Street, Way 13408, Salalah, call +968 9551 3848 or WhatsApp +968 9562 4666.",
          "خطّط لحفل زفافك أو مناسبتك مع دو للمناسبات. زورونا في شارع 23 يوليو، طريق 13408، صلالة، أو اتصلوا على 96895513848+ أو واتساب 96895624666+."), ld=LD)}
{header(ctx, "contact.html")}
<main id="main">
<section class="phero">
  <div class="wrap">
    {mtag(x("Get in touch", "تواصل معنا"))}
    <h1 class="h-display phero__title" data-split="load">{x("Let's create something <em>unforgettable</em>", "لنصنع معاً مناسبة <em>لا تُنسى</em>")}</h1>
    <p class="phero__ar" lang="{ctx.other}" data-fade="load">{x("تواصل معنا — " + SITE['tagline_ar'], "Get in touch — " + SITE['tagline'])}</p>
  </div>
</section>
<section class="section on-light">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-list" data-fade>
        <div><h4>{x("Call", "اتصل بنا")}</h4><a href="{SITE['phone_href']}" dir="ltr">{SITE['phone']}</a></div>
        <div><h4>{x("WhatsApp", "واتساب")}</h4><a href="{SITE['whatsapp_href']}" target="_blank" rel="noopener" dir="ltr">{SITE['whatsapp']}</a></div>
        <div><h4>{x("Visit", "زورونا")}</h4><address>{x(SITE['address'], SITE_AR['address'])}</address><div class="alt" {a_attr}>{a_txt}</div></div>
        <div><h4>{x("Follow", "تابعنا")}</h4><a href="{SITE['instagram']}" target="_blank" rel="noopener" dir="ltr">{SITE['instagram_handle']}</a></div>
      </div>
      <form class="form" id="enquiry" data-wa="{SITE['whatsapp_href']}" data-msg='{e(msg, quote=True)}' data-fade novalidate>
        <div class="field"><label for="f-name">{x("Your name", "الاسم")}</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="f-phone">{x("Phone", "رقم الهاتف")}</label><input id="f-phone" name="phone" type="tel" dir="ltr" required autocomplete="tel"></div>
        <div class="field"><label for="f-type">{x("Event type", "نوع المناسبة")}</label><select id="f-type" name="type">{types}</select></div>
        <div class="field"><label for="f-date">{x("Event date", "تاريخ المناسبة")}</label><input id="f-date" name="date" type="date"></div>
        <div class="field field--full"><label for="f-guests">{x("Guests (approx.)", "عدد الضيوف (تقريباً)")}</label><input id="f-guests" name="guests" inputmode="numeric"></div>
        <div class="field field--full"><label for="f-msg">{x("Tell us about it", "حدّثنا عن مناسبتك")}</label><textarea id="f-msg" name="message" placeholder="{x('Venue, theme, colours, anything you have in mind…', 'المكان، الثيم، الألوان، وأي فكرة تدور في بالك…')}"></textarea></div>
        <div class="form__actions">
          <button type="submit" class="btn btn--rust"><span class="btn__text"><span>{x("Send via WhatsApp", "أرسل عبر واتساب")}</span><span aria-hidden="true">{x("Send via WhatsApp", "أرسل عبر واتساب")}</span></span><i class="btn__dot"></i></button>
          <span class="form__note">{x("Opens WhatsApp with your details pre-filled.", "يفتح واتساب مع تفاصيلك جاهزة للإرسال.")}</span>
        </div>
      </form>
    </div>
    <div class="map" data-fade>
      <iframe src="{SITE['map_embed']}{x('', '&hl=ar')}" title="{x('Do Events location, Salalah', 'موقع دو للمناسبات، صلالة')}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      {btn(x("Open in Google Maps", "افتح في خرائط Google"), SITE['map_link'], "btn--dark", arrow=True, attrs='target="_blank" rel="noopener"')}
    </div>
  </div>
</section>
</main>
{footer(ctx, "contact.html")}"""
    write(out_path(ctx), body)


FONT_WEIGHTS = [("extrabold", 800), ("extra-bold", 800), ("semibold", 600), ("semi-bold", 600), ("black", 900), ("heavy", 900),
                ("bold", 700), ("medium", 500), ("light", 300), ("thin", 200), ("regular", 400), ("book", 400)]


def write_fonts_css():
    """@font-face for the brand fonts that are actually present in assets/fonts/."""
    fmt = {"woff2": "woff2", "woff": "woff", "otf": "opentype", "ttf": "truetype"}
    faces = [
        # Al-Mohanad: Arabic display (the "Regular" cut is light, ExtraBold is the headline weight)
        ("Al-Mohanad", 400, "al-mohanad/al-mohanad-regular.woff2"),
        ("Al-Mohanad", 800, "al-mohanad/al-mohanad-extrabold.woff2"),
    ]
    tdir = os.path.join(ROOT, "assets", "fonts", "thmanyah")
    for f in sorted(os.listdir(tdir)) if os.path.isdir(tdir) else []:
        base, ext = os.path.splitext(f)
        if ext[1:].lower() not in fmt:
            continue
        key = re.sub(r"[\s_]+", "-", base.lower())
        if "serif" in key and "display" in key:
            fam = "Thmanyah Serif Display"
        elif "serif" in key:
            fam = "Thmanyah Serif Text"
        elif "sans" in key:
            fam = "Thmanyah Sans"
        else:
            continue
        w = next((v for k, v in FONT_WEIGHTS if k in key.replace("thmanyah", "")), 400)
        faces.append((fam, w, "thmanyah/" + f))
    # one file per family/weight; prefer woff2 > woff > otf > ttf
    order = {"woff2": 0, "woff": 1, "otf": 2, "ttf": 3}
    best = {}
    for fam, w, path in faces:
        ext = path.rsplit(".", 1)[1].lower()
        if (fam, w) not in best or order[ext] < order[best[(fam, w)].rsplit(".", 1)[1].lower()]:
            best[(fam, w)] = path
    css = ["/* Generated by build/build.py — brand fonts found in assets/fonts/ */"]
    for (fam, w), path in sorted(best.items()):
        ext = path.rsplit(".", 1)[1].lower()
        # Al-Mohanad's dash/quote glyphs are decorative — let punctuation fall back to the text face
        urange = " unicode-range: U+0000-2012, U+2016-201B, U+201E-FFFF;" if fam == "Al-Mohanad" else ""
        css.append(f'@font-face {{ font-family: "{fam}"; src: url("../fonts/{path}") format("{fmt[ext]}"); '
                   f'font-weight: {w}; font-style: normal; font-display: swap;{urange} }}')
    write("assets/css/fonts.css", "\n".join(css) + "\n")
    return sorted({fam for fam, _ in best})


if __name__ == "__main__":
    print("brand fonts:", ", ".join(write_fonts_css()))
    n = 0
    for lang in ("en", "ar"):
        home(lang); work(lang); weddings(lang); corporate(lang); about(lang); contact(lang)
        for i, c in enumerate(CASES):
            case_page(lang, i, c)
        n += 6 + len(CASES)
    print(f"built {n} pages (en + ar)")
