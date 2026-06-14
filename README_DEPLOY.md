# Deploying Silverback Flasher

## What is ready in this repository

- Frontend build and deployment workflows are configured in `.github/workflows/deploy.yml`
- Backend Docker deployment is configured in `render.yaml`
- Flask backend entrypoint is `app.py`, and `Dockerfile` starts it with `gunicorn`
- `requirements.txt` includes Flask and gunicorn

## What I can do for you here

- Review and verify the repo deployment config
- Improve documentation so you can deploy cleanly
- Confirm the Flask backend is Docker-ready
- Confirm the GitHub Actions workflows are present

## What you still need to do

1. Create the Cloudflare Pages project in your Cloudflare account.
2. Create the Render service in your Render account.
3. Add all required GitHub Actions secrets to the repository.
4. Push the code to the `main` branch.
5. Monitor GitHub Actions and the Render deployment logs.

## Cloudflare Pages deployment

### Required GitHub secrets
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PROJECT_NAME`

### How to deploy
1. In Cloudflare, create a new Pages project for this repo.
2. Use `main` as the production branch.
3. In GitHub, set the repository secrets above.
4. Push your code to `main`.
5. The workflow `.github/workflows/deploy.yml` will:
   - checkout the code
   - install Node.js dependencies
   - run `npm run build`
   - deploy `dist/` to Cloudflare Pages

### Important note
If the Pages project does not already exist, the GitHub Action may fail. Create the project manually in Cloudflare Pages first, then push again.

## Render backend deployment

### Required GitHub secrets
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`

### How to deploy
1. In Render, create a new Web Service using this repository.
2. Use the `main` branch.
3. Choose Docker deployment and point to this repo root.
4. Copy the Render service ID.
5. Add the GitHub secrets above.
6. Push your code to `main`.
7. The workflow `.github/workflows/deploy-backend.yml` will:
   - checkout the code
   - build the Docker image with `docker build`
   - call Render to deploy the service

### Render environment variables
Add these environment variables in Render service settings:
- `FLASK_SECRET_KEY` — use a strong random string
- `FLASK_DEBUG` — set to `0`

## Local verification

If you want to test before pushing:

1. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Build the frontend locally:
   ```bash
   npm install
   npm run build
   ```
3. Run the backend in Docker:
   ```bash
   docker build -t silverback-web .
   docker run -p 5000:5000 --env FLASK_DEBUG=0 --env FLASK_SECRET_KEY='your-secret' silverback-web
   ```

## Step-by-step summary for you

1. Create Cloudflare Pages project manually.
2. Create Render service manually.
3. Add GitHub Actions secrets.
4. Push to `main`.
5. Watch GitHub Actions logs and Render logs.
6. If frontend deploy fails, confirm Cloudflare Pages project name and account ID.
7. If backend fails, confirm Render service ID and Docker build success.

## Local Frontend Verification

1. Install frontend dependencies:
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
