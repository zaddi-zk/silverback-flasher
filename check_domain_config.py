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

# List zones (domains) in the account
print('=== CLOUDFLARE ZONES ===')
r = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
print(f'Status: {r.status_code}')
data = r.json()
if data.get('success'):
    zones = data.get('result', [])
    print(f'Found {len(zones)} zone(s):')
    for zone in zones:
        print(f"\n  Zone: {zone['name']}")
        print(f"    ID: {zone['id']}")
        print(f"    Status: {zone.get('status')}")
        print(f"    Nameservers: {zone.get('name_servers', [])}")
        print(f"    Plan: {zone.get('plan', {}).get('name')}")
        
        # Get DNS records for this zone
        r2 = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone['id']}/dns_records", headers=headers)
        if r2.status_code == 200:
            records = r2.json().get('result', [])
            print(f"    DNS Records ({len(records)}):")
            for rec in records[:10]:  # Show first 10
                print(f"      - {rec['type']}: {rec['name']} -> {rec.get('content', 'N/A')}")
else:
    print(f'Error: {data.get("errors")}')

# Check if hottboiihitzz.cc is using Cloudflare nameservers
print('\n=== CHECKING DOMAIN REGISTRATION ===')
import subprocess
try:
    result = subprocess.run(['nslookup', 'hottboiihitzz.cc'], capture_output=True, text=True, timeout=10)
    print(result.stdout)
    if result.stderr:
        print('STDERR:', result.stderr)
except Exception as e:
    print(f'Error running nslookup: {e}')
