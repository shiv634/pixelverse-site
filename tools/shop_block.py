# Software shop pages (Volsplat): executed from build_site.py, shares its namespace (page(), RGB, EMAIL, ...).
# Anything wrapped in ph() is a placeholder that needs the real Volsplat fact before the site goes live.

SHOP = {
    "mor": "Dodo Payments",          # merchant of record: change in one place if you pick another provider
    "updated": "9 November 2026",
}

# Paste the hosted-checkout link for each plan here once the provider account is approved.
# Empty string = the button shows "Get notified" and goes to the contact form instead of a dead "Buy now".
CHECKOUT = {
    "indie": "",
    "perpetual": "",
    "commercial": "",
}

PLACEHOLDERS = []
def ph(text):
    PLACEHOLDERS.append(text)
    return f'<mark class="ph">[[{html.escape(text)}]]</mark>'

PLANS = [
    dict(key="indie", name="Indie", price="$20", per="per month",
         lead="For individual creators.",
         points=["One person, on up to 2 computers",
                 "Personal projects, plus paid work while the revenue it brings in stays under USD 100,000 a year",
                 "Every update while you’re subscribed",
                 "Cancel any time"]),
    dict(key="perpetual", name="Perpetual", price="$100", per="one-time payment",
         lead="Pay once and keep it.",
         points=["Same use rights as Indie",
                 "No renewals. The version you buy is yours to keep",
                 "Updates for the major version you buy (for example, every 1.x release)",
                 "Later major versions are offered as a discounted upgrade"]),
    dict(key="commercial", name="Commercial", price="$50", per="per month, per seat",
         lead="For studios and companies.",
         points=["For companies, studios, and anyone above the Indie revenue limit",
                 "One licence per person, each on up to 2 computers",
                 "Every update while you’re subscribed",
                 "Invoices available from your customer portal"]),
]

def plan_card(p):
    url = CHECKOUT.get(p["key"], "")
    if url:
        btn = f'<a class="btn solid" href="{url}" rel="noopener">{RGB}Buy now</a>'
    else:
        btn = f'<a class="btn" href="/contact/?need=volsplat">{RGB}Get notified at launch</a>'
    lis = "\n".join(f"          <li>{x}</li>" for x in p["points"])
    return f"""      <article class="plan" id="plan-{p['key']}">
        <div>
          <h3>{p['name']}</h3>
          <p class="muted">{p['lead']}</p>
        </div>
        <p class="price">{p['price']}<span class="per">{p['per']}</span></p>
        <ul>
{lis}
        </ul>
        {btn}
      </article>"""

FEATURES = [(ph(f"Feature {i} name"), ph(f"One or two sentences on what this feature does for the user")) for i in range(1, 7)]
feat_html = "\n".join(f'      <div class="feat"><h3>{a}</h3><p>{b}</p></div>' for a, b in FEATURES)

FAQ = [
    ("Which plan should I choose?",
     "Choose Indie if you’re a single creator and your revenue from Volsplat work stays under USD 100,000 a year. Choose Perpetual if you’d rather pay once. Choose Commercial for studios, companies, and anyone above the Indie limit."),
    ("How do updates work?",
     "Volsplat checks for updates when it starts and tells you when a new version is ready. Subscriptions include every update. A Perpetual licence includes every update within the major version you bought."),
    ("How many computers can I use it on?",
     "Each licence works on up to 2 computers. To move to a new machine, deactivate the old one from your customer portal."),
    ("What happens if my subscription ends?",
     "After a short grace period, Volsplat switches off its licensed features. Every file you made stays yours, and you can resubscribe at any time."),
    ("Is there a free trial?", ph("Say whether there is a trial, how long it lasts, and what is limited")),
    ("Can I get a refund?",
     'Yes. Your first purchase of any plan can be refunded within 14 days. The details are in our <a href="/legal/refund-policy/">refund policy</a>.'),
    ("Does this licence cover your other software?",
     "No. A Volsplat licence covers Volsplat only. Any software we release later is licensed and priced separately."),
    ("Who handles payment?",
     f"Payments are processed by {SHOP['mor']}, our merchant of record. They take your payment, add any sales tax or VAT that applies, and send your receipt and licence key."),
]
faq_html = "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

volsplat = f"""<section class="page-top product-top">
  <div class="wrap">
    <div class="section-head">
      <h1 class="display">Volsplat</h1>
      <p class="lede">{ph("One-line description of what Volsplat does and who it is for")}</p>
      <div class="actions">
        <a class="btn solid" href="#pricing">{RGB}Buy now</a>
        <a class="btn" href="/contact/?need=volsplat">{RGB}Contact the studio</a>
      </div>
      <p class="product-meta"><span>{ph("Platforms, e.g. Windows 10/11 and macOS")}</span><span>Version {ph("1.0")}</span><span>By Pixelverse, Chennai</span></p>
    </div>
    <div class="shot"><p>{ph("Screenshot or demo video of Volsplat")}</p></div>
  </div>
</section>

<section class="section tight" id="features">
  <div class="wrap">
    <div class="section-head">
      <h2 class="display">What it does</h2>
      <p class="lede muted">{ph("Two sentences on what problem Volsplat solves")}</p>
    </div>
    <div class="feat-grid">
{feat_html}
    </div>
  </div>
</section>

<section class="section tight" id="requirements">
  <div class="wrap split">
    <div class="lead"><div class="lead-inner"><h2 class="display">Requirements</h2></div></div>
    <div class="list">
      <dl class="spec">
        <div><dt>Platforms</dt><dd>{ph("Operating systems and versions")}</dd></div>
        <div><dt>Graphics card</dt><dd>{ph("Minimum and recommended GPU")}</dd></div>
        <div><dt>Memory and storage</dt><dd>{ph("Minimum RAM and disk space")}</dd></div>
        <div><dt>Works with</dt><dd>{ph("File formats and other software it connects to")}</dd></div>
        <div><dt>Internet</dt><dd>Needed to activate your licence and to check for updates.</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="section tight" id="pricing">
  <div class="wrap">
    <div class="section-head">
      <h2 class="display">Choose your licence</h2>
      <p class="lede muted">One licence covers Volsplat. Prices are in US dollars, and any tax is added at checkout.</p>
    </div>
    <div class="plans">
{chr(10).join(plan_card(p) for p in PLANS)}
    </div>
    <p class="fine">Payments are handled by {SHOP['mor']}, our merchant of record. By buying you agree to the <a href="/legal/volsplat-eula/">licence agreement</a> and <a href="/legal/terms-of-sale/">terms of sale</a>. <a href="/legal/refund-policy/">14-day refunds</a> on your first purchase.</p>
  </div>
</section>

<section class="section tight" id="faq">
  <div class="wrap split">
    <div class="lead"><div class="lead-inner"><h2 class="display">Questions</h2>
      <p class="lede muted">Not here? <a href="/contact/?need=volsplat" style="border-bottom:1px solid var(--line-strong)">Ask the studio</a>.</p></div></div>
    <div class="list faq">
{faq_html}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap cta-band">
    <h2 class="display">Ready to try Volsplat?</h2>
    <p class="lede muted">Pick a licence above, or write to us if you need something different, such as a studio-wide arrangement.</p>
    <a class="btn solid" href="#pricing">{RGB}See licences</a>
  </div>
</section>"""

page("/volsplat/", "Volsplat – Software by Pixelverse",
     "Volsplat by Pixelverse: features, requirements and licences (Indie, Perpetual, Commercial).",
     "software", volsplat, ["/assets/js/site.js"])

# ───────────── legal pages for the shop ─────────────
def legal_page(path, title, desc, h1, body):
    out = f"""<section class="page-top"><div class="wrap">
  <div class="section-head"><h1 class="display" style="font-size:clamp(36px,6vw,80px)">{h1}</h1><p class="muted">Last updated {SHOP['updated']}</p></div>
  <div class="legal">
{body}
  </div></div></section>"""
    page(path, title, desc, "", out, ["/assets/js/site.js"])

MOR = SHOP["mor"]
WHO = "Pixelverse, C4, Purva Windmere, Pallikaranai, Chennai 600100, India"

legal_page("/legal/volsplat-eula/", "Volsplat licence agreement – Pixelverse",
  "The licence agreement for Volsplat software.", "Volsplat licence agreement", f"""
    <p>This agreement is between you and {WHO} (“Pixelverse”, “we”). By installing or using Volsplat you accept it. If you don’t accept it, don’t install or use Volsplat.</p>
    <h2>1. Your licence</h2>
    <p>We grant you a limited, non-exclusive, non-transferable, revocable licence to install and use Volsplat on up to 2 computers that you own or control, under the plan you bought. This licence covers Volsplat only. Other Pixelverse software is licensed separately.</p>
    <h2>2. Plans</h2>
    <ul>
      <li><strong>Indie (subscription).</strong> For one individual. You may use Volsplat for personal projects and for paid work, as long as the revenue you earn from work made with Volsplat stays under USD 100,000 in a calendar year.</li>
      <li><strong>Perpetual.</strong> The same use rights as Indie, with no renewal. You may keep using the version you bought. You receive updates within the major version you bought. Later major versions may need a separate upgrade purchase.</li>
      <li><strong>Commercial (subscription).</strong> For companies, studios, and anyone above the Indie revenue limit. Each person using Volsplat needs their own licence.</li>
    </ul>
    <h2>3. Subscriptions</h2>
    <p>Subscriptions renew automatically each month until you cancel from your customer portal. If you cancel, you keep access until the end of the period you paid for. If a subscription ends or a payment fails, Volsplat switches off its licensed features after a short grace period. The files you created stay yours.</p>
    <h2>4. Updates</h2>
    <p>Volsplat checks for updates when it starts. Which updates you receive depends on your plan, as set out above. We may change, add or remove features between versions.</p>
    <h2>5. What you may not do</h2>
    <ul>
      <li>Share, sell or publish your licence key, or let others use it.</li>
      <li>Copy, resell, rent, or host Volsplat for others to use.</li>
      <li>Reverse engineer or modify Volsplat, except where the law lets you do so regardless of this agreement.</li>
      <li>Remove or get around the licence check.</li>
    </ul>
    <h2>6. Your work</h2>
    <p>You own what you create with Volsplat. We claim no rights in your files or outputs.</p>
    <h2>7. Licence checks and data</h2>
    <p>To check your licence, Volsplat sends your licence key, an anonymised identifier for your computer, and the app version to our licence service. We use this to confirm your plan and the number of computers in use. Our <a href="/privacy-policy/">privacy policy</a> explains how we handle it.</p>
    <h2>8. Ownership</h2>
    <p>Pixelverse and its licensors own Volsplat and everything in it. This agreement gives you the right to use it, not to own it. Open-source components included in Volsplat are covered by their own licences.</p>
    <h2>9. No warranty, and limits on liability</h2>
    <p>Volsplat is provided “as is”. We don’t promise it will be error-free or suit your particular purpose. To the extent the law allows, our total liability to you for anything connected with Volsplat is limited to what you paid for it in the 12 months before the claim, and we aren’t liable for lost profits, lost data, or indirect losses. Nothing here limits a right you have under law that can’t be limited.</p>
    <h2>10. Ending this agreement</h2>
    <p>You can stop using Volsplat at any time. We may end your licence if you break this agreement, and we will tell you why. When a licence ends, you must stop using Volsplat.</p>
    <h2>11. Governing law</h2>
    <p>This agreement is governed by the laws of India, and the courts at Chennai have jurisdiction, except where consumer law in your country gives you the right to bring a claim where you live.</p>
    <h2>12. Contact</h2>
    <p>Questions about this agreement: {EMAIL}.</p>""")

legal_page("/legal/terms-of-sale/", "Terms of sale – Pixelverse",
  "Terms for buying Volsplat licences from Pixelverse.", "Terms of sale", f"""
    <h2>Who you are buying from</h2>
    <p>Volsplat is made by {WHO}. Orders are taken and processed by {MOR}, our merchant of record. {MOR} is the seller of your licence, charges your payment method, collects any sales tax or VAT, and issues your receipt. Their own terms and privacy policy apply to the checkout.</p>
    <h2>Prices and tax</h2>
    <p>Prices are in US dollars. Tax that applies where you live is added at checkout and shown before you pay. We may change prices for new purchases at any time. For existing subscribers we will give at least 30 days’ notice before a change applies to their next renewal.</p>
    <h2>Your licence</h2>
    <p>After payment you receive a receipt and a licence key by email. Use is governed by the <a href="/legal/volsplat-eula/">licence agreement</a>.</p>
    <h2>Subscriptions</h2>
    <p>A subscription renews each month at the price shown at checkout until you cancel it. You can cancel any time from your customer portal. You keep access until the end of the period you paid for.</p>
    <h2>Refunds</h2>
    <p>See our <a href="/legal/refund-policy/">refund policy</a>.</p>
    <h2>Support</h2>
    <p>For help with your purchase or your licence, email {EMAIL}. Include your order number or the email you bought with.</p>
    <h2>Governing law</h2>
    <p>These terms are governed by the laws of India, subject to any rights you have under consumer law where you live.</p>""")

legal_page("/legal/refund-policy/", "Refund policy – Pixelverse",
  "Refund policy for Volsplat licences.", "Refund policy", f"""
    <h2>14-day refunds</h2>
    <p>If Volsplat isn’t right for you, ask for a refund within 14 days of your first purchase of a plan and we will refund it in full. Email {EMAIL} with the email you bought with, or your order number.</p>
    <h2>Subscription renewals</h2>
    <p>You can cancel a subscription at any time and you won’t be charged again. We don’t refund the part of a period that has already started, except where the law requires it. If a renewal charge surprises you, write to us within 3 days of the charge and we will review it.</p>
    <h2>How refunds are paid</h2>
    <p>Refunds are issued by {MOR}, our merchant of record, to the payment method you used. Banks usually take 5 to 10 working days to show them. When a refund is issued, the licence key for that purchase stops working.</p>
    <h2>Your legal rights</h2>
    <p>This policy doesn’t limit any rights you have under consumer law where you live.</p>""")

# privacy policy: add software purchase section (replaces the page generated earlier in build_site.py)
priv2 = privacy.replace("""    <h2>Videos and fonts</h2>""", f"""    <h2>Software purchases and licences</h2>
    <p>If you buy Volsplat, the purchase is handled by {MOR}, our merchant of record. They collect your payment details and tell us your name, email address, country, order details and licence key. We never see your card number. {MOR}’s privacy policy covers what they do with your data. When Volsplat starts, it sends your licence key, an anonymised identifier for your computer, and the app version to our licence service so we can confirm your plan and check for updates. We use this only to run licences and support.</p>
    <h2>Videos and fonts</h2>""").replace("Last updated 4 November 2026", f"Last updated {SHOP['updated']}")
page("/privacy-policy/", "Privacy policy – Pixelverse", "How Pixelverse handles information on this website.", "", priv2, ["/assets/js/site.js"])

if PLACEHOLDERS:
    print(f"\n!! {len(PLACEHOLDERS)} Volsplat placeholders still on /volsplat/ (fill before going live):")
    for t in dict.fromkeys(PLACEHOLDERS): print("   -", t)
