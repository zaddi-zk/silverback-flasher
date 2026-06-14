import base64
import json
import os
import sys
import requests
from nacl import encoding, public


def get_repo_owner_and_name():
    repository = os.environ.get('GITHUB_REPOSITORY')
    if repository and '/' in repository:
        owner, repo_name = repository.split('/', 1)
        return owner, repo_name

    owner = os.environ.get('GITHUB_REPO_OWNER')
    repo_name = os.environ.get('GITHUB_REPO_NAME')
    if owner and repo_name:
        return owner, repo_name

    print('Missing repository information. Set GITHUB_REPOSITORY or both GITHUB_REPO_OWNER and GITHUB_REPO_NAME.')
    sys.exit(1)


def main():
    owner, repo = get_repo_owner_and_name()
    pat = os.environ.get('GITHUB_PAT')

    if not pat:
        print('Missing GITHUB_PAT in environment')
        raise SystemExit(1)

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

    secrets_to_upload = {
        'CLOUDFLARE_ACCOUNT_ID': os.environ.get('CLOUDFLARE_ACCOUNT_ID'),
        'CLOUDFLARE_API_TOKEN': os.environ.get('CLOUDFLARE_API_TOKEN'),
        'CLOUDFLARE_PROJECT_NAME': os.environ.get('CLOUDFLARE_PROJECT_NAME'),
        'RENDER_API_KEY': os.environ.get('RENDER_API_KEY'),
        'RENDER_SERVICE_ID': os.environ.get('RENDER_SERVICE_ID')
    }

    public_key_obj = public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key_obj)

    for name, value in secrets_to_upload.items():
        if not value:
            print(f'Skipping {name}: no value in environment')
            continue
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


if __name__ == '__main__':
    main()
