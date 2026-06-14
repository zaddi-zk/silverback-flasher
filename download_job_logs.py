import os
import requests

owner = os.environ.get('GITHUB_REPO_OWNER', 'kirui58-sy')
repo = os.environ.get('GITHUB_REPO_NAME', 'silverback-flasher')
job_id = os.environ.get('GITHUB_JOB_ID', '81189689878')
pat = os.environ.get('GITHUB_PAT')

if not pat:
	print('Missing GITHUB_PAT in environment')
	raise SystemExit(1)

headers = {'Authorization': f'token {pat}', 'Accept': 'application/vnd.github+json'}
url = f'https://api.github.com/repos/{owner}/{repo}/actions/jobs/{job_id}/logs'
resp = requests.get(url, headers=headers)
print('status', resp.status_code)
open('logs.zip','wb').write(resp.content)
print('Saved logs.zip')
