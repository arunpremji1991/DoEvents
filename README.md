# Do Events — Website

Static, premium marketing site for **Do Events (دو للمناسبات)**, Salalah. The layout and motion follow the MDNT Events reference: a video hero with word-mask reveals, a statement block, a split services section, project cards that rise in 3D on scroll with a "View project" cursor, an Instagram rail, rotating circle-text CTA and a giant wordmark footer.

## Languages

The site is fully bilingual. English pages live at the root and Arabic pages at `ar/`, with the same file names (for example `work/royal-blue.html` and `ar/work/royal-blue.html`).

- Arabic pages are right-to-left (`<html lang="ar" dir="rtl">`), with no letter-spacing so the letters stay joined. Fonts are listed under Brand below.
- Every page has an **العربية / English** toggle in the header, the mobile menu and the footer. It links to the same page in the other language.
- The choice is remembered. Visitors who picked Arabic, or whose browser is set to Arabic, are sent to `ar/` when they open the English home page. Choosing English cancels this.
- Each page lists its other-language version with `hreflang` tags. These are relative links. Once a domain is set up, make them absolute in `head()` in `build/build.py` for search engines.

## Brand

The look follows the Do brand pattern and sticker files.

**Colours** (CSS variables at the top of `assets/css/style.css`). The look is a warm black ground with the brand rust and blush as accents:

| Token | Value | Use |
|---|---|---|
| `--bg-dark` | `#0D0A09` | main ground (warm black) |
| `--bg-dark-2` / `--bg-dark-3` | `#161110` / `#211916` | cards, media placeholders, dark buttons |
| `--bg-deep` | `#080605` | footer, menu, page transition |
| `--ember` | `#E39A6C` | copper accent on black (highlights, active links) |
| `--rust` | `#9B4825` | brand rust: buttons, hairlines, cartouche |
| `--blush` / `--cream` | `#FEE0CF` | light sections, text on black |
| `--ink` | `#1C1411` | text on blush |

**Decoration (no patterns).** The site no longer uses the brand patterns. Atmosphere comes from light, line and the logo:

| Element | Where |
|---|---|
| copper/rust "stage light" glows | statement section, projects corner, behind the call-to-action ring, under the footer logo, loading screen, mobile menu |
| thin copper light beam | dropping onto the Do Events logo in the statement section |
| faint outline of the DO monogram (`assets/logo/do-mark-outline.svg`) | page headers, mobile menu |
| small copper diamond | divider between stacked projects |
| soft blush gradient | light sections |

The loading screen fills the Do Events logo with colour.

The pattern and cartouche files are still in `assets/img/brand/` in case they're wanted again, but no page uses them.

**Fonts:**

| | Headings | Text |
|---|---|---|
| English | Thmanyah Sans (falls back to Montserrat), bold caps, with accents in a light weight | Montserrat |
| Arabic | Al-Mohanad ExtraBold for main headings, Thmanyah Serif Display (falls back to Al-Mohanad) for secondary headings | Thmanyah Sans (falls back to IBM Plex Sans Arabic) |

**Adding Thmanyah:** the license requires downloading it yourself from [font.thmanyah.com](https://font.thmanyah.com/). Put the Sans and Serif Display files (`.woff2`, `.otf` or `.ttf`) in `assets/fonts/thmanyah/` and run `python3 build/build.py`. The build detects the family and weight from each file name and writes `assets/css/fonts.css`. Nothing else needs changing.

## Screen sizes

The layout is checked from 320px phones to 2560px 27" monitors.

- **Up to 1600px:** `1rem` = 16px and the content column is 1440px.
- **Above 1600px:** the root size grows (about 18px at 1920 and 21px at 2560). Text, spacing, buttons and the 90rem content column all scale together, so a 27" screen looks like a larger version of a laptop, not a small layout floating in the middle.
- **Edge alignment:** the header, Instagram strip and video captions line up with the content edges via the `--edge` variable.

## Background music

`assets/audio/moment-of-peace.mp3` (re-encoded at 128 kbps, 2.4 MB) plays quietly and loops.

- It carries on across pages: the position is saved as you browse, it fades out during the page transition and fades back in on the next page.
- It pauses whenever a film plays in the viewer, and resumes when the film ends or the viewer is closed.
- The equaliser button in the header turns it on and off, and the choice is remembered.
- Browsers block sound until a visitor interacts with a site. On a first visit, the music starts on the first click, tap or key press.

To change the track, replace the file (keep the same name) or edit the `<audio id="bgm">` line in `build/build.py`.

## Preview locally

```bash
node build/serve.js 8080
```

Then open http://localhost:8080. The server supports byte ranges, so video seeking works.

## Edit content

All pages are generated from the data in `build/`:

| File | What it holds |
|---|---|
| `build/data.py` | Contact details, case-study titles, clients, categories, featured order and notable events. The Arabic versions are in `SITE_AR`, `CATS_AR`, `CASES_AR`, `NOTABLE_AR` and `MARQUEE_CLIENTS_AR` |
| `build/youtube.json` | The story, highlights (EN + AR) and title for each film, taken from its YouTube description |
| `build/build.py` | Page templates. Interface text is written as `x("English", "العربية")` pairs, so each string is edited in one place for both languages |

After editing, rebuild:

```bash
python3 build/build.py
```

## Structure

```
index.html  weddings.html  corporate.html  work.html  about.html  contact.html
work/<slug>.html           21 case studies
ar/…                       the same 27 pages in Arabic (RTL)
assets/logo/               SVG logos converted from DO-EVENTS_LOGO.pdf (rust, blush, white, black, currentColor, favicon, app icons)
assets/video/hero.mp4      12-shot montage for the hero
assets/video/preview/      6-second muted loops for cards
assets/video/full/         full films (720p H.264 + AAC) for the lightbox
assets/img/poster|gallery  posters and stills taken from the films
assets/css, assets/js      styles and interactions (GSAP + ScrollTrigger + Lenis, all in assets/vendor)
```

## Client logos (hero strip)

The logos in the strip live in `assets/img/clients/`. The order and the expected file name for each brand are set in `CLIENT_LOGOS` in `build/data.py`. Each logo is shown as a white silhouette over the hero video, and brands without a file are left out. To add one (for example the Ministry of Education or Green Energy Conference 2023):

1. Save it as `assets/img/clients/moe-oman.svg`, or `.png` with a transparent background.
2. Run `python3 build/build.py`.
3. If it looks too big or small, adjust its height with `--h` in `assets/css/style.css` (search for `data-client`).

| Logo | Source |
|---|---|
| OQ | Official vector from OQ Company via Wikimedia Commons (CC BY-SA 4.0) |
| Dhofar University | The university's site header logo (du.edu.om) |
| Millennium Resort Salalah, Mymoon, DITFest, Dhofar Championship | Cut out of Do Events' own event films. Replace them with official files when available for sharper results |

## Deploying

The site is live on Hostinger at https://dodgerblue-koala-528259.hostingersite.com. It deploys automatically from the `main` branch of https://github.com/arunpremji1991/DoEvents: push to GitHub and the live site updates within about a minute.

`.htaccess` (Hostinger/Apache settings):
- hides `build/`, this README and the git files from visitors
- redirects to HTTPS
- turns on compression
- sets browser caching: a year for CSS/JS/fonts, whose links are version-stamped; 30 days for media; HTML is always re-checked
- adds basic security headers

It also works on any other Apache or LiteSpeed host.

The full films take up about 226 MB. To make the site lighter, the case-study lightbox can play the YouTube versions instead: set `NO_LOCAL_FILM` in `build/data.py` to include those slugs, rebuild, and delete the matching files in `assets/video/full/`.

## Notes

- The enquiry form opens WhatsApp (+968 9562 4666) with the details already filled in. There is no server or email backend.
- The Mirror Theme Wedding has no local video file, so its film plays from YouTube.
- Fonts: Montserrat and IBM Plex Sans Arabic load from Google Fonts. Al-Mohanad is self-hosted in `assets/fonts/al-mohanad/`, and Thmanyah will be once its files are added (see Brand).
