import json
import os
import requests

account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
token = os.environ.get('CLOUDFLARE_API_TOKEN')
project_name = os.environ.get('CLOUDFLARE_PROJECT_NAME') or os.environ.get('PAGES_PROJECT_NAME')
production_branch = os.environ.get('CLOUDFLARE_PRODUCTION_BRANCH', 'main')

if not account_id or not token or not project_name:
    print('Missing CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, or CLOUDFLARE_PROJECT_NAME in environment')
    raise SystemExit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

payload = {
    'production_branch': production_branch
}

print(f'Updating Cloudflare Pages project "{project_name}" production branch to "{production_branch}"...')
response = requests.patch(
    f'https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}',
    headers=headers,
    json=payload
)
print(f'Status: {response.status_code}')
print(f'Response: {response.text[:500]}')

if response.status_code in (200, 201):
    data = response.json()
    if data.get('success'):
        proj = data.get('result', {})
        print('\n✓ Updated successfully!')
        print(f"  Production branch: {proj.get('production_branch')}")
    else:
        print(f'Error: {data.get("errors")}')
else:
    print(f'Failed: {response.text}')
