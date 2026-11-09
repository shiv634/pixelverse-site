# Pixelverse website: go-live guide

This folder is the complete site: Home, Work, About, Contact, Privacy policy and Accessibility statement.
It is plain HTML, CSS and JavaScript, so any static host can serve it. Nothing needs building or installing.

## 1. Put it online (about 10 minutes, free)

**Cloudflare Pages (recommended)**
1. Sign in at dash.cloudflare.com, then go to Workers & Pages, Create, Pages, **Upload assets**.
2. Name the project `pixelverse`, then drag in the contents of this folder (the folder that contains `index.html`).
3. Deploy. You get a preview address like `pixelverse.pages.dev`. Open it and check:
   - the home page entrance assembles the PIXELVERSE wordmark,
   - the three reels on Work play,
   - the pages work on your phone.

Netlify (app.netlify.com/drop) works the same way: drag the folder in.

## 2. Point pixelversefx.com at it
1. In Cloudflare Pages, open the project, Custom domains, add `www.pixelversefx.com`. It shows the DNS record to create (a CNAME to your `pages.dev` address).
2. Add that record where your domain's DNS is managed. If the domain was bought through Wix, that is in your Wix account under Domains, then DNS records.
3. Make the bare domain `pixelversefx.com` redirect to `www.pixelversefx.com` at your domain provider.
4. Once the DNS change spreads (minutes to a few hours) the new site replaces the Wix one.

The old page addresses `/portfolio`, `/about`, `/contact`, `/privacy-policy` and `/accessibility-statement` all still work.

## 3. Important: keep the Wix site (for now)
The three reels are streamed from **Wix's media servers**, the same files your current site uses. They keep playing as long as those files stay in your Wix media library. Do not delete the Wix site or those videos until you have moved the reels:
- Download the original reel files from your Wix media library.
- Put them on any host (your own folder on this site, YouTube, Vimeo, Cloudflare Stream).
- Update `assets/js/work.js` with the new addresses.

Reel sizes are large (up to 60 MB at 1080p), so the site previews at 360p, plays at 720p on desktop, and uses 480p on phones.

## 4. Make the contact form send to your inbox
Until you do this, the form opens the visitor's email app with the message filled in.
1. Create a free form at formspree.io (or a similar form service) and copy its address.
2. Paste it into `formEndpoint` at the top of `assets/js/site.js`.

## 5. Edit things
| To change | Edit |
|---|---|
| Reels (video, poster, titles) | `assets/js/work.js` |
| Hero words, mode lines, colours | the `CONFIG` block at the top of `assets/js/hero.js` |
| Page text | the `index.html` inside each folder (`about/`, `contact/`, `portfolio/`) |
| Colours, fonts, spacing | `assets/css/site.css` (variables at the top) |
| Email, phone, address | the footer and Contact page HTML |

## 6. Please review before launch
- Social links are not included: the ones on the old footer pointed to Wix's own accounts. Add yours to the footer.
- The About text, the four-step "How a project runs" list and the one-line descriptions under VFX, 3D and AI are drafted from your old site. Check they say what you want.
- The Privacy policy and Accessibility statement are plain-language drafts. Have them reviewed before relying on them, especially if you add analytics or ads.
- The old site had a "noindex" setting that asked search engines to skip it. The new site is indexable and includes a sitemap.
