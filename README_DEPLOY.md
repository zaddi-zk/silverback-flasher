# Deploying Silverback Flasher

## Cloudflare Pages

1. Create a Cloudflare Pages project in your Cloudflare account.
2. Set these repository secrets in the GitHub repo settings:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
   - `CLOUDFLARE_PROJECT_NAME`
3. Push to `main`.

The workflow `.github/workflows/deploy.yml` will:
- install Node.js
- run `npm ci`
- build the site with `npm run build`
- deploy the `dist/` directory to Cloudflare Pages

## Local Verification

1. Install dependencies:
   ```bash
   npm install
   ```
2. Build locally:
   ```bash
   npm run build
   ```
3. Serve locally:
   ```bash
   npm install -g serve
   serve dist
   ```
