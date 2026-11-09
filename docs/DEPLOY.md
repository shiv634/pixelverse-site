# One-time setup: publish from GitHub

## 1. Create the GitHub repository
1. On github.com click New repository. Name: `pixelverse-site`. Private is fine. Leave it empty (no README).
2. In Claude, make sure GitHub is connected (Settings, Connectors) and the Claude GitHub app has access to this repository.
3. Tell Claude the repository name. Claude uploads the site files.

## 2. Connect Cloudflare Pages to the repository
Cloudflare can't turn your current "pixelverse" upload-based project into a Git one, so you create a new project.
1. Cloudflare dashboard, Workers & Pages, Create, Pages, Connect to Git. Pick `pixelverse-site`.
2. Settings: Production branch `main`. Framework preset: None. Build command: leave empty. Build output directory: `site`.
3. Save and deploy. You get an address like `pixelverse-site.pages.dev`. Check that it looks right.

## 3. Point the domain at the new project
1. In the new project, open Custom domains and add `www.pixelversefx.com`.
2. In your DNS (Wix, where the domain's DNS is managed), change the `www` CNAME to the new project's `.pages.dev` address.
3. Once the site loads from the new project, you can delete the old "pixelverse" upload project.

## 4. Preview branch
In the project's Settings, Builds, make sure branch previews are on. Every push to the `draft` branch then gets its own preview address.

## How day-to-day changes work
1. You ask Claude for a change.
2. Claude pushes it to `draft` and sends you the preview address.
3. You say "publish". Claude merges `draft` into `main`, and Cloudflare publishes it within a minute or two.
4. To undo, tell Claude to revert, or use Cloudflare's Deployments tab, Rollback.
