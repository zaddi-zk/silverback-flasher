import base64
import json
import requests
from nacl import encoding, public

owner = 'kirui58-sy'
repo = 'silverback-flasher'
pat = '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'
new_token = 'cfat_dVPQ3BPpgliFFYMgEhdhrDkZPn4vJxmBsPxOHqqQ7d8daf6a'

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

public_key_obj = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
sealed_box = public.SealedBox(public_key_obj)

encrypted = sealed_box.encrypt(new_token.encode('utf-8'))
encoded = base64.b64encode(encrypted).decode('utf-8')
put_resp = requests.put(
    f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/CLOUDFLARE_API_TOKEN',
    headers=headers,
    json={'encrypted_value': encoded, 'key_id': key_id}
)
print('put status', put_resp.status_code)
if put_resp.status_code in (201,204):
    print('Secret updated')
else:
    print(put_resp.text)
    raise SystemExit(1)
