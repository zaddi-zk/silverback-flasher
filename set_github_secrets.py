import base64
import json
import requests
from nacl import encoding, public

owner = 'kirui58-sy'
repo = 'silverback-flasher'
pat = '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'
headers = {
    'Authorization': f'token {pat}',
    'Accept': 'application/vnd.github+json'
}

key_url = f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key'
resp = requests.get(key_url, headers=headers)
resp.raise_for_status()
key = resp.json()
public_key = key['key']
key_id = key['key_id']

secrets = {
    'CLOUDFLARE_ACCOUNT_ID': '2fd2522dce24251c8c44c8ae60515974',
    'CLOUDFLARE_API_TOKEN': 'cfat_dVPQ3BPpgliFFYMgEhdhrDkZPn4vJxmBsPxOHqqQ7d8daf6a',
    'CLOUDFLARE_PROJECT_NAME': 'hottboiihitzz'
}

public_key_obj = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
sealed_box = public.SealedBox(public_key_obj)

for name, value in secrets.items():
    encrypted = sealed_box.encrypt(value.encode('utf-8'))
    encoded = base64.b64encode(encrypted).decode('utf-8')
    put_resp = requests.put(
        f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/{name}',
        headers=headers,
        json={'encrypted_value': encoded, 'key_id': key_id}
    )
    print(name, put_resp.status_code)
    if put_resp.status_code not in (201, 204):
        print(put_resp.text)
        raise SystemExit(1)
print('Secrets uploaded successfully.')
