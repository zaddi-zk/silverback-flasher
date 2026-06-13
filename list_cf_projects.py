import requests

account_id = '2fd2522dce24251c8c44c8ae60515974'
token = 'cfat_dVPQ3BPpgliFFYMgEhdhrDkZPn4vJxmBsPxOHqqQ7d8daf6a'

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
