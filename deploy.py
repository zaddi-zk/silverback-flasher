#!/usr/bin/env python3
"""
Cloudflare Pages Deployment Script
Deploy dist/ folder to Cloudflare Pages
"""

import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
PROJECT_NAME = os.environ.get('CLOUDFLARE_PROJECT_NAME', 'silverback-flasher')
API_BASE = os.environ.get('CLOUDFLARE_API_BASE', 'https://api.cloudflare.com/client/v4')


def api_request(method, endpoint, data=None):
    """Make API request to Cloudflare."""
    url = f"{API_BASE}{endpoint}"
    if not API_TOKEN or not ACCOUNT_ID:
        print("❌ Missing required environment variables: CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_TOKEN")
        sys.exit(1)

    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'User-Agent': 'SilverFlasher-Deploy/1.0'
    }

    if data:
        headers['Content-Type'] = 'application/json'
        body = json.dumps(data).encode('utf-8')
    else:
        body = None

    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            return response.status, response_data
    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_body}")
        return e.code, None
    except URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return None, None


def main():
    print(f"🚀 Preparing Cloudflare Pages deployment")
    print(f"📁 Project: {PROJECT_NAME}")
    print(f"🔑 Account ID: {ACCOUNT_ID}")
    print()

    dist_path = Path('dist')
    if not dist_path.exists():
        print("❌ Error: dist/ folder not found. Run 'npm run build' first.")
        sys.exit(1)

    print("📦 Checking Cloudflare Pages project...")
    status, response = api_request('GET', f'/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}')

    if status == 404:
        print(f"📝 Cloudflare Pages project '{PROJECT_NAME}' not found. Creating it now...")
        status, response = api_request(
            'POST',
            f'/accounts/{ACCOUNT_ID}/pages/projects',
            {'name': PROJECT_NAME}
        )

        if status != 201:
            print(f"❌ Failed to create project: {response}")
            sys.exit(1)
        print("✅ Project created")
    elif status == 200:
        print("✅ Project already exists")
    else:
        print(f"❌ Error checking project: {response}")
        sys.exit(1)

    print()
    print("✅ Cloudflare Pages project is configured.")
    print("ℹ️ This script does not upload the site assets.")
    print("   Use GitHub Actions or `wrangler pages publish dist --project-name <name>` to complete the deployment.")
    print()
    print(f"🌐 Expected site URL: https://{PROJECT_NAME}.pages.dev")


if __name__ == '__main__':
    main()
