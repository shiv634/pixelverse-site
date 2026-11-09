# Pixelverse website

Static site for https://www.pixelversefx.com, published by Cloudflare Pages.

- `site/` is what gets published (plain HTML, CSS, JS, fonts). No build step on Cloudflare.
- `tools/build_site.py` generates the HTML pages in `site/` (header, footer, pages share one template). `tools/shop_block.py` generates the Volsplat product page and shop legal pages.
- Edit the tools or `site/assets/*`, run the build, commit the result. Don't hand-edit the generated `.html` files; the next build overwrites them.

## Build

```
python3 tools/build_site.py            # public site, shop hidden
SHOP_LIVE=1 python3 tools/build_site.py # includes /volsplat/, /legal/*, Software menu link
```

`SHOP_LIVE=1` also prints the Volsplat placeholders (`[[...]]`) that still need real text.
When switching the shop off again, delete `site/volsplat` and `site/legal` first, then rebuild.

## Branches

- `main`: production. Cloudflare publishes it to www.pixelversefx.com.
- `draft`: previews. Cloudflare publishes it to its own preview address, not the live site. Changes are reviewed there first, then merged to `main`.

See `docs/DEPLOY.md` for the one-time Cloudflare setup.
