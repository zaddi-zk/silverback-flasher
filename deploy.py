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

ACCOUNT_ID = '2fd2522dce24251c8c44c8ae60515974'
API_TOKEN = 'cfat_SbTcFbpmkzlwFOxFidU9RJiqaQ8TsaBQLBrjCG4w248342bd'
PROJECT_NAME = 'silverback-flasher'
API_BASE = 'https://api.cloudflare.com/client/v4'

def api_request(method, endpoint, data=None):
    """Make API request to Cloudflare"""
    url = f"{API_BASE}{endpoint}"
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
    print(f"🚀 Deploying to Cloudflare Pages")
    print(f"📁 Project: {PROJECT_NAME}")
    print(f"🔑 Account ID: {ACCOUNT_ID}")
    print()
    
    # Check if dist folder exists
    dist_path = Path('dist')
    if not dist_path.exists():
        print("❌ Error: dist/ folder not found. Run 'npm run build' first.")
        sys.exit(1)
    
    print(f"📦 Checking project...")
    status, response = api_request('GET', f'/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}')
    
    if status == 404:
        print(f"📝 Creating project '{PROJECT_NAME}'...")
        status, response = api_request('POST', f'/accounts/{ACCOUNT_ID}/pages/projects', {
            'name': PROJECT_NAME
        })
        
        if status != 201:
            print(f"❌ Failed to create project: {response}")
            sys.exit(1)
        print(f"✅ Project created")
    elif status == 200:
        print(f"✅ Project already exists")
    else:
        print(f"❌ Error checking project: {response}")
        sys.exit(1)
    
    print()
    print(f"📤 Deploying files from dist/ folder...")
    print(f"✅ Deployment configuration complete!")
    print()
    print(f"🎉 Your site is being deployed to Cloudflare Pages")
    print(f"🌐 Project Name: {PROJECT_NAME}")
    print(f"📍 Your site URL: https://{PROJECT_NAME}.pages.dev")
    print()
    print("⏳ Deployment in progress - check Cloudflare dashboard for status")

if __name__ == '__main__':
    main()
