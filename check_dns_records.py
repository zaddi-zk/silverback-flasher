import requests
import json

account_id = '2fd2522dce24251c8c44c8ae60515974'
token = 'cfat_dVPQ3BPpgliFFYMgEhdhrDkZPn4vJxmBsPxOHqqQ7d8daf6a'

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Get the zone ID for hottboiihitzz.cc
zone_name = 'hottboiihitzz.cc'
r = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers, params={'name': zone_name})
zones = r.json().get('result', [])
if not zones:
    print(f'Zone {zone_name} not found')
    exit(1)

zone_id = zones[0]['id']
print(f'Zone ID: {zone_id}\n')

# Get ALL DNS records for this zone
print('=== ALL DNS RECORDS ===')
r = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers)
if r.status_code == 200:
    records = r.json().get('result', [])
    print(f'Total records: {len(records)}\n')
    for rec in records:
        print(f"Type: {rec['type']}")
        print(f"  Name: {rec['name']}")
        print(f"  Content: {rec.get('content', 'N/A')}")
        print(f"  TTL: {rec.get('ttl')}")
        print(f"  Status: {rec.get('status')}")
        print()
else:
    print(f'Error: {r.status_code}')
    print(r.text)

# Check Pages project details
print('\n=== PAGES PROJECT DETAILS ===')
r = requests.get(f'https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects', headers=headers)
if r.status_code == 200:
    projects = r.json().get('result', [])
    for proj in projects:
        if proj['name'] == 'hottboiihitzz':
            print(f"Project: {proj['name']}")
            print(f"  Default domain: {proj.get('subdomain', 'N/A')}.pages.dev")
            print(f"  Custom domains: {proj.get('domains', [])}")
            print(f"  Production branch: {proj.get('production_branch', 'N/A')}")
