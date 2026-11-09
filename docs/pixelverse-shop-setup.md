# Selling Volsplat: setup checklist

## 1. Open the payment account (about 1 week, mostly waiting for approval)
1. Sign up at Dodo Payments (or Polar). Choose "Individual". You do not need a registered company.
2. Complete verification: product information form, your own ID (KYC), and a bank account in your own name. The name on the bank account must match your ID.
3. Add a product for each plan:
   - Volsplat Indie: $20 / month, subscription
   - Volsplat Perpetual: $100, one-time
   - Volsplat Commercial: $50 / month, subscription (per seat)
4. Turn on licence keys for each product. Set 2 activations per key. Set the key to expire with the subscription (not for Perpetual).
5. Copy each product's hosted checkout link.

## 2. Put the links on the site
Send me the three checkout links and I'll add them and give you a new zip. Until a plan has a link, its button says "Get notified at launch" and goes to the contact form. With a link, it becomes "Buy now".

## 3. Fill the Volsplat facts
Every `[[...]]` on /volsplat/ needs the real text: one-line description, 6 features, platforms and requirements, version, screenshot or demo video, trial policy. Send these to me and I'll fill them in.

## 4. Decisions in the draft that are yours to change
- Indie revenue limit: USD 100,000 a year
- 2 computers per licence
- Perpetual includes updates within the major version you sold (for example all 1.x). The next major version is a discounted upgrade.
- 14-day refund on the first purchase of a plan
- Governing law: India, courts at Chennai
- Have a lawyer review the licence agreement and terms of sale once sales start.

## 5. Before the first payout (talk to a CA)
- GST registration if your services turnover will cross the threshold
- Letter of Undertaking (LUT) for zero-rated exports
- FEMA paperwork for the foreign-currency payouts

## 6. In the app (build next)
- Licence activation: enter key, app calls the provider's licence API, stores the result, re-checks periodically with an offline grace period.
- Update check: app reads a `latest.json` (version, notes, download links) hosted on Cloudflare, on launch and from "Check for updates".
- Perpetual keys: ignore updates beyond the major version you sold.
