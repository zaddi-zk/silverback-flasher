import os
import requests

owner = os.environ.get('GITHUB_REPO_OWNER', 'kirui58-sy')
repo = os.environ.get('GITHUB_REPO_NAME', 'silverback-flasher')
run_id = os.environ.get('GITHUB_RUN_ID', '27466520199')
pat = os.environ.get('GITHUB_PAT')

if not pat:
    print('Missing GITHUB_PAT in environment')
    raise SystemExit(1)

headers = {'Authorization': f'token {pat}', 'Accept': 'application/vnd.github+json'}

r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs', headers=headers)
print('status', r.status_code)
jobs=r.json().get('jobs', [])
for job in jobs:
    print(job['name'], job['id'], job['status'], job['conclusion'])
    for step in job['steps']:
        print('  -', step['name'], step.get('status'), step.get('conclusion'))
