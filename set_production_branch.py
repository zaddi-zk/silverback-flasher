import requests

account_id = '2fd2522dce24251c8c44c8ae60515974'
token = 'cfat_dVPQ3BPpgliFFYMgEhdhrDkZPn4vJxmBsPxOHqqQ7d8daf6a'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Update the Pages project to use 'main' as production branch
project_name = 'hottboiihitzz'
payload = {
    'production_branch': 'main'
}

print(f'Updating {project_name} production branch to "main"...')
r = requests.patch(
    f'https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}',
    headers=headers,
    json=payload
)
print(f'Status: {r.status_code}')
print(f'Response: {r.text[:500]}')

if r.status_code in (200, 201):
    data = r.json()
    if data.get('success'):
        proj = data.get('result', {})
        print(f'\n✓ Updated successfully!')
        print(f"  Production branch: {proj.get('production_branch')}")
    else:
        print(f'Error: {data.get("errors")}')
else:
    print(f'Failed: {r.text}')
