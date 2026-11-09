# Publishing: GitHub -> Cloudflare

The site is a Cloudflare Worker (static assets) named `pixelverse-site`, built from this repository by Cloudflare Workers Builds.
`wrangler.jsonc` at the repository root tells it to publish the `site/` folder. There is no build command.

## Cloudflare settings (Worker > Settings > Builds)
- Production branch: `main`. Build command: empty. Deploy command: `npx wrangler deploy`.
- Turn on builds for non-production branches. Pushes to `draft` then get their own preview address.

## Custom domain
Workers custom domains only work for a domain that is a zone on the same Cloudflare account, so DNS must move to Cloudflare:
1. Add `pixelversefx.com` to Cloudflare (Add a domain). Check the imported DNS records against Wix's.
2. At the domain registrar (Wix), change the nameservers to the two Cloudflare gives you.
3. Delete the old `www` CNAME record in Cloudflare DNS (a custom domain can't be added over an existing CNAME).
4. Worker > Settings > Domains & Routes > Add > Custom domain: add `www.pixelversefx.com`, then `pixelversefx.com`.

## Day-to-day
1. Ask Claude for a change. Claude pushes it to `draft` and sends the preview address.
2. Say "publish". Claude merges `draft` into `main`, and Cloudflare publishes it within a minute or two.
3. To undo: ask Claude to revert, or use Rollback under the Worker's Deployments.
