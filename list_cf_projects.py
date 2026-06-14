import requests

import os

account_id = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
token = os.environ.get('CLOUDFLARE_API_TOKEN')

if not account_id or not token:
    print('Missing CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_TOKEN in environment')
    raise SystemExit(1)

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# List existing Pages projects
print('Listing existing Pages projects...')
r = requests.get(
    f'https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects',
    headers=headers
)
print(f'Status: {r.status_code}')
print(f'Response: {r.text[:500]}')

data = r.json()
if data.get('success'):
    projects = data.get('result', [])
    print(f'\nFound {len(projects)} project(s):')
    for proj in projects:
        print(f"  - {proj['name']}: {proj.get('domains', [])}")
else:
    errors = data.get('errors', [])
    print(f'Errors: {errors}')
