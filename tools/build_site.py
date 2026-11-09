#!/usr/bin/env python3
"""Generates the static Pixelverse site into /home/claude/site (pages share one header/footer)."""
import os, json, html

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
# The Volsplat shop (product page, legal pages, Software menu link) stays hidden until SHOP_LIVE=1.
SHOP_LIVE = os.environ.get("SHOP_LIVE") == "1"
ORIGIN = "https://www.pixelversefx.com"
VER = "4"  # bump on every deploy to bust cached CSS/JS
EMAIL = "pixelverse.va@gmail.com"
PHONE_DISPLAY = "85906 33822"
PHONE_TEL = "+918590633822"
ADDRESS = "C4, Purva Windmere, Pallikaranai<br>Chennai 600100, India"
TAGLINE = "Create what doesn’t exist."

RGB = '<span class="rgb" aria-hidden="true"><i></i><i></i><i></i></span>'

# pieces that only appear when the shop is switched on
SOFT_FOOT = '<a href="/volsplat/">Software</a>' if SHOP_LIVE else ""
LEGAL_FOOT = ('<a href="/legal/terms-of-sale/">Terms of sale</a><a href="/legal/refund-policy/">Refund policy</a>'
              '<a href="/legal/volsplat-eula/">Volsplat licence</a>') if SHOP_LIVE else ""
VOL_OPT = "<option>Volsplat (software)</option>" if SHOP_LIVE else ""
SOFT_PROMO = f'''<section class="section tight" id="software">
  <div class="wrap promo">
    <div>
      <h2 class="display">Software by Pixelverse</h2>
      <p class="lede muted">Volsplat is our first release.</p>
    </div>
    <a class="btn solid" href="/volsplat/">{RGB}See Volsplat</a>
  </div>
</section>''' if SHOP_LIVE else ""

FILTERS_SVG = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<filter id="ch-r" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>
<filter id="ch-g" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0"/></filter>
<filter id="ch-b" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0"/></filter>
</svg>"""

def head(title, desc, path, extra=""):
    t = html.escape(title)
    d = html.escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#05060b">
<link rel="canonical" href="{ORIGIN}{path}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pixelverse">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{ORIGIN}{path}">
<meta property="og:image" content="{ORIGIN}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/syne-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
{extra}</head>
"""

def header(current):
    def a(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <a class="logo" href="/" aria-label="Pixelverse, home">{RGB}<span>PIXELVERSE</span></a>
  <button class="btn menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">
    {a("/portfolio/", "Work", "work")}
    {a("/volsplat/", "Software", "software") if SHOP_LIVE else ""}
    {a("/about/", "About", "about")}
    {a("/contact/", "Contact", "contact")}
  </nav>
</header>
"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <p class="word">PIXELVERSE</p>
        <p class="muted">{TAGLINE}</p>
      </div>
      <nav class="foot-col" aria-label="Footer">
        <h2>Explore</h2>
        <a href="/portfolio/">Work</a>
        {SOFT_FOOT}
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </nav>
      <div class="foot-col">
        <h2>Studio</h2>
        <address>{ADDRESS}</address>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; 2026 Pixelverse. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy policy</a>{LEGAL_FOOT}<a href="/accessibility-statement/">Accessibility statement</a></span>
    </div>
  </div>
</footer>
"""

def page(path, title, desc, current, main, scripts, extra_head="", body_class=""):
    out = head(title, desc, path, extra_head)
    out += f'<body class="{body_class}">\n' + FILTERS_SVG + "\n" + header(current)
    out += f'<main id="main">\n{main}\n</main>\n' + FOOTER
    out += "".join(f'<script src="{s}?v={VER}" defer></script>\n' for s in scripts)
    out += "</body>\n</html>\n"
    p = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)

CTA = f"""<section class="section">
  <div class="wrap cta-band">
    <h2 class="display">Tell us what doesn’t exist yet.</h2>
    <p class="lede muted">Share the idea, the property or the shot you can’t film.</p>
    <a class="btn solid" href="/contact/">{RGB}Start a project</a>
  </div>
</section>"""

# ───────────── HOME ─────────────
ld = json.dumps({
    "@context": "https://schema.org", "@type": "Organization", "name": "Pixelverse", "url": ORIGIN,
    "email": EMAIL, "telephone": PHONE_TEL, "slogan": TAGLINE,
    "address": {"@type": "PostalAddress", "streetAddress": "C4, Purva Windmere, Pallikaranai", "addressLocality": "Chennai", "postalCode": "600100", "addressCountry": "IN"}
})

def reel_row(key, name, blurb, meta, link_label):
    return f"""      <article class="reel-row" id="{key}-row">
        <div class="info">
          <h3 class="name">{name}</h3>
          <p>{blurb}</p>
          <p class="meta">{meta}</p>
          <a class="textlink" href="/portfolio/#{key}" style="width:fit-content">{link_label}</a>
        </div>
        <div class="media" data-reel="{key}"></div>
      </article>"""


LOGO_LIST = [
    ("kaminho", "Kaminho", 177, 120, 76),
    ("woodfibre-lng", "Woodfibre LNG", 357, 120, 44),
    ("hunting", "Hunting", 336, 120, 46),
    ("baker-hughes", "Baker Hughes", 204, 120, 62),
    ("total", "Total", 420, 102, 40),
    ("microsoft", "Microsoft", 420, 90, 34),
    ("honeywell", "Honeywell", 420, 77, 30),
    ("energy-transfer", "Energy Transfer", 420, 89, 34),
]
def logo_cells(hidden=False):
    out = []
    for key, name, w, h, dh in LOGO_LIST:
        alt = "" if hidden else name
        out.append(f'''        <li><img src="/assets/img/logos/{key}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async" style="--h:{dh}"></li>''')
    return "\n".join(out)

LOGOS_SECTION = f"""<section class="section tight" id="clients" aria-labelledby="clients-h">
  <div class="wrap">
    <h2 class="clients-h" id="clients-h">Worked with</h2>
  </div>
  <div class="logo-marquee">
    <div class="logo-track">
      <ul class="logo-set">
{logo_cells()}
      </ul>
      <ul class="logo-set" aria-hidden="true">
{logo_cells(True)}
      </ul>
      <ul class="logo-set" aria-hidden="true">
{logo_cells(True)}
      </ul>
      <ul class="logo-set" aria-hidden="true">
{logo_cells(True)}
      </ul>
    </div>
  </div>
</section>
"""

home = f"""<section class="hero" id="hero" aria-label="Pixelverse">
  <canvas id="gl" aria-hidden="true"></canvas>
  <div class="fallback" aria-hidden="true">PIXELVERSE</div>
  <h1 class="sr">Pixelverse. {TAGLINE}</h1>
  <div class="copy" id="copy">
    <p class="tag" id="tag">{TAGLINE}</p>
    <p class="sub" id="sub">Visual storytelling meets creative technology.</p>
  </div>
  <nav class="modes" id="modes" aria-label="Explore our work">
    <a class="btn" data-mode="vfx" href="/portfolio/#vfx">{RGB}VFX</a>
    <a class="btn" data-mode="3d" href="/portfolio/#3d">{RGB}3D</a>
    <a class="btn" data-mode="ai" href="/portfolio/#ai">{RGB}AI</a>
  </nav>
  <p class="corner l" id="hint">Move through it. Click to break it.</p>
  <p class="corner r">Chennai, India</p>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <h2 class="display">Selected work</h2>
      <p class="lede muted">Reels from the three disciplines we work in.</p>
    </div>
    <div class="reels">
{reel_row("vfx", "VFX", "Simulation, compositing and the shots that can’t be filmed.", "Reel · 0:56", "Watch the VFX reel")}
{reel_row("3d", "3D", "Worlds modelled, lit and rendered from nothing.", "Reel · 1:55", "Watch the 3D reel")}
{reel_row("ai", "AI", "Generative imagery, directed like a shoot.", "Reel · 0:58", "Watch the AI reel")}
    </div>
  </div>
</section>

{LOGOS_SECTION}
{SOFT_PROMO}
<section class="section tight" id="spatial">
  <div class="wrap split">
    <div class="lead">
      <div class="lead-inner">
        <h2 class="display">Spaces, shown at their best.</h2>
        <p class="lede muted">For brokers, developers and designers who need a building to look the way it feels.</p>
        <a class="textlink" href="/contact/" style="width:fit-content">Talk to us about a property</a>
      </div>
    </div>
    <div class="list">
      <ul class="services">
        <li><h3>Twilight photography</h3><p>Dusk light brings out what daylight flattens: the texture of the architecture, the warmth of the interiors, the depth of the facade.</p></li>
        <li><h3>Aerial and drone</h3><p>Estates and commercial developments seen at the scale, and in the context, that ground-level photography can’t give.</p></li>
        <li><h3>Cinematic walkthroughs</h3><p>Composition and lighting that make each room feel considered, cut into a film that moves through the whole space.</p></li>
        <li><h3>Landscape installation</h3><p>Careful, well-finished installation, built to look right on the first day and keep looking right.</p></li>
        <li><h3>Sustainable landscapes</h3><p>Low-maintenance planting with native species and efficient irrigation.</p></li>
      </ul>
    </div>
  </div>
</section>

<section class="section statement" id="story">
  <div class="wrap">
    <h2 class="display">We turn buildings into visual essays.</h2>
    <div class="row">
      <p class="lede muted" style="max-width:30em">Every project starts with what the space is trying to say, and ends with images and films that say it clearly.</p>
    </div>
    <div class="row">
      <a class="textlink" href="/about/">Read our story</a>
      <a class="textlink" href="/portfolio/">See all work</a>
    </div>
  </div>
</section>

{CTA}"""

page("/", "Pixelverse – Create what doesn’t exist",
     "Pixelverse is a creative studio in Chennai: VFX, 3D and AI imagery, plus property photography, aerial film and landscape design.",
     "home", home, ["/assets/js/work.js", "/assets/js/site.js", "/assets/js/hero.js"],
     extra_head=f'<script type="application/ld+json">{ld}</script>\n', body_class="home")

# ───────────── PORTFOLIO ─────────────
def work_item(key, title, time, blurb):
    return f"""      <article class="work-item" data-id="{key}">
        <div data-reel="{key}"></div>
        <div class="top"><h2>{title}</h2><span class="time">{time}</span></div>
        <p>{blurb}</p>
      </article>"""

portfolio = f"""<section class="page-top">
  <div class="wrap">
    <div class="section-head">
      <h1 class="display">Work</h1>
      <p class="lede muted">VFX, 3D and AI reels. Choose one to watch.</p>
    </div>
    <div class="filters" role="group" aria-label="Filter by discipline">
      <button class="btn" type="button" data-filter="all" aria-pressed="true">{RGB}All</button>
      <button class="btn" type="button" data-filter="vfx" aria-pressed="false">{RGB}VFX</button>
      <button class="btn" type="button" data-filter="3d" aria-pressed="false">{RGB}3D</button>
      <button class="btn" type="button" data-filter="ai" aria-pressed="false">{RGB}AI</button>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap">
    <div class="grid-work">
{work_item("vfx", "VFX reel", "0:56", "Simulation, compositing and the shots that can’t be filmed.")}
{work_item("3d", "3D reel", "1:55", "Worlds modelled, lit and rendered from nothing.")}
{work_item("ai", "AI reel", "0:58", "Generative imagery, directed like a shoot.")}
      <aside class="invite">
        <h2 class="display" style="font-size:clamp(26px,3vw,40px)">Your project could be next.</h2>
        <p class="muted">Property, aerial and landscape work is available on request.</p>
        <a class="btn" href="/contact/">{RGB}Start a project</a>
      </aside>
    </div>
  </div>
</section>"""

page("/portfolio/", "Work – Pixelverse", "Watch Pixelverse reels in VFX, 3D and AI imagery.", "work", portfolio,
     ["/assets/js/work.js", "/assets/js/site.js"])

# ───────────── ABOUT ─────────────
about = f"""<section class="page-top">
  <div class="wrap">
    <div class="section-head">
      <h1 class="display">About</h1>
      <p class="lede">Pixelverse is a creative studio in Chennai. We make images and films from nothing, and we help real places look like themselves.</p>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap about-grid">
    <div class="a"><h2 class="display" style="font-size:clamp(28px,3.6vw,48px)">Where visual storytelling meets creative technology.</h2></div>
    <div class="b prose">
      <p>We work in VFX, 3D and AI imagery: simulations, composites, modelled worlds and generative visuals, directed with the same care as a live shoot.</p>
      <p>The same eye goes into spatial work. For brokers, developers and designers we shoot twilight exteriors, aerial views and cinematic walkthroughs, and we install landscapes that are low-maintenance and built around native plants and efficient irrigation.</p>
      <p>Whatever the medium, the aim is the same: make something people haven’t seen before, and make it clear enough to understand at a glance.</p>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap">
    <h2 class="display" style="font-size:clamp(26px,3vw,40px);margin-bottom:32px">What we make</h2>
    <div class="disciplines">
      <article><h3 class="display">VFX</h3><p>Simulation, compositing and shots that can’t be filmed.</p></article>
      <article><h3 class="display">3D</h3><p>Worlds modelled, lit and rendered from nothing.</p></article>
      <article><h3 class="display">AI</h3><p>Generative imagery, directed like a shoot.</p></article>
      <article><h3 class="display">Spatial</h3><p>Property photography, aerial film and landscape design.</p></article>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap about-grid">
    <div class="a"><h2 class="display" style="font-size:clamp(26px,3vw,40px)">How a project runs</h2></div>
    <div class="b">
      <ol class="process">
        <li><h3>Brief</h3><p>We start with what the work needs to do and who needs to see it.</p></li>
        <li><h3>Look development</h3><p>Frames, tests and references until the look is agreed.</p></li>
        <li><h3>Production</h3><p>Shooting, simulating, modelling or generating, with progress shared along the way.</p></li>
        <li><h3>Delivery</h3><p>Final files in the formats and sizes you need.</p></li>
      </ol>
    </div>
  </div>
</section>
{CTA}"""
page("/about/", "About – Pixelverse", "Pixelverse is a creative studio in Chennai working in VFX, 3D and AI imagery, property photography and landscape design.",
     "about", about, ["/assets/js/site.js"])

# ───────────── CONTACT ─────────────
contact = f"""<section class="page-top">
  <div class="wrap">
    <div class="section-head">
      <h1 class="display">Start a project</h1>
      <p class="lede muted">Tell us what you want to make or show. Include a link, a location or a reference if you have one.</p>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap contact-grid">
    <div class="info">
      <dl class="details">
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Phone</dt><dd><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></dd></div>
        <div><dt>Studio</dt><dd>{ADDRESS}</dd></div>
      </dl>
    </div>
    <div class="form">
      <form class="pv" novalidate>
        <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="err-name"><div class="err" id="err-name"></div></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required aria-describedby="err-email"><div class="err" id="err-email"></div></div>
        <div class="field"><label for="f-need">What do you need?</label>
          <select id="f-need" name="need">
            <option>VFX</option><option>3D</option><option>AI imagery</option>
            {VOL_OPT}<option>Property photography or film</option><option>Landscape design</option><option>Something else</option>
          </select></div>
        <div class="field"><label for="f-message">Project details</label><textarea id="f-message" name="message" required aria-describedby="err-message"></textarea><div class="err" id="err-message"></div></div>
        <div class="hp" aria-hidden="true"><label for="f-company">Company</label><input id="f-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
        <div><button class="btn solid" type="submit">{RGB}Send message</button></div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </div>
</section>"""
page("/contact/", "Contact – Pixelverse", "Start a project with Pixelverse. Studio in Pallikaranai, Chennai.", "contact", contact, ["/assets/js/site.js"])

# ───────────── LEGAL ─────────────
privacy = f"""<section class="page-top"><div class="wrap">
  <div class="section-head"><h1 class="display" style="font-size:clamp(36px,6vw,80px)">Privacy policy</h1><p class="muted">Last updated 4 November 2026</p></div>
  <div class="legal">
    <h2>What this site collects</h2>
    <p>This site does not use cookies or analytics. If you use the contact form, the details you type (name, email, project type and message) are used only to reply to your enquiry.</p>
    <h2>How the contact form works</h2>
    <p>The form either opens your email app with your message ready to send, or sends it to the studio inbox through a form service. Either way, we read it at {EMAIL} and keep it only as long as needed to respond and to run the project.</p>
    <h2>Videos and fonts</h2>
    <p>Our reels are streamed from Wix’s media servers. When you play or preview a reel, your browser connects to those servers, which will receive your IP address and browser details as part of any web request. Fonts are served from this site.</p>
    <h2>Your choices</h2>
    <p>You can ask us to show, correct or delete anything you have sent us by emailing {EMAIL}.</p>
    <h2>Contact</h2>
    <p>Pixelverse, {ADDRESS.replace("<br>", ", ")}. {EMAIL}</p>
  </div></div></section>"""
page("/privacy-policy/", "Privacy policy – Pixelverse", "How Pixelverse handles information on this website.", "", privacy, ["/assets/js/site.js"])

access = f"""<section class="page-top"><div class="wrap">
  <div class="section-head"><h1 class="display" style="font-size:clamp(36px,6vw,80px)">Accessibility statement</h1><p class="muted">Last updated 4 November 2026</p></div>
  <div class="legal">
    <h2>Our aim</h2>
    <p>We want everyone to be able to use this site. We build to the Web Content Accessibility Guidelines (WCAG) 2.2, level AA.</p>
    <h2>What we have done</h2>
    <ul>
      <li>All pages work with a keyboard, with a visible focus outline on every control.</li>
      <li>The animated entrance on the home page is decorative. It stops moving when your device is set to reduce motion, and the page’s content is available as ordinary text.</li>
      <li>Text and controls meet colour-contrast requirements on the dark background.</li>
      <li>Forms have labels and plain error messages.</li>
    </ul>
    <h2>Known limits</h2>
    <p>Our reels do not yet have captions or audio descriptions. We are working on adding them.</p>
    <h2>Tell us about a problem</h2>
    <p>If something on this site is hard to use, email {EMAIL} or call {PHONE_DISPLAY}. Tell us the page and what happened, and we will help and fix it.</p>
  </div></div></section>"""
page("/accessibility-statement/", "Accessibility statement – Pixelverse", "Accessibility on the Pixelverse website.", "", access, ["/assets/js/site.js"])

if SHOP_LIVE:
  exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop_block.py"), encoding="utf-8").read(), "shop_block.py", "exec"))

# ───────────── static support files ─────────────
open(os.path.join(ROOT, "assets/img/favicon.svg"), "w").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#05060b"/>'
 '<rect x="5" y="12" width="12" height="12" fill="#ff1a4d" style="mix-blend-mode:screen"/>'
 '<rect x="10" y="12" width="12" height="12" fill="#1aff8c" style="mix-blend-mode:screen"/>'
 '<rect x="15" y="12" width="12" height="12" fill="#4073ff" style="mix-blend-mode:screen"/></svg>')
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
urls = ["/", "/portfolio/", "/about/", "/contact/", "/privacy-policy/", "/accessibility-statement/"]
if SHOP_LIVE: urls[4:4] = ["/volsplat/", "/legal/volsplat-eula/", "/legal/terms-of-sale/", "/legal/refund-policy/"]
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
 "".join(f"  <url><loc>{ORIGIN}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(ROOT, "_redirects"), "w").write("/portfolio-collections/portfolio /portfolio/ 301\n/portfolio-collections /portfolio/ 301\n")
open(os.path.join(ROOT, "_headers"), "w").write(
 "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
 "/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n"
 "/assets/css/*\n  Cache-Control: public, max-age=0, must-revalidate\n/assets/js/*\n  Cache-Control: public, max-age=0, must-revalidate\n")
print("built", len(urls), "pages")
