import requests
import json

import os

owner = os.environ.get('GITHUB_REPO_OWNER', 'kirui58-sy')
repo = os.environ.get('GITHUB_REPO_NAME', 'silverback-flasher')
pat = os.environ.get('GITHUB_PAT')

if not pat:
    print('Missing GITHUB_PAT in environment')
    raise SystemExit(1)

headers = {
    'Authorization': f'token {pat}',
    'Accept': 'application/vnd.github+json'
}

# Get latest run
r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/runs?branch=main&status=completed', headers=headers)
print('runs status:', r.status_code)
runs = r.json().get('workflow_runs', [])
if not runs:
    print('No runs found')
    exit(1)
    
latest_run = runs[0]
print(f'Latest run: {latest_run["id"]} - {latest_run["status"]} - {latest_run["conclusion"]}')

# Get the job
r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{latest_run["id"]}/jobs', headers=headers)
print('jobs status:', r.status_code)
jobs = r.json().get('jobs', [])
if not jobs:
    print('No jobs found')
    exit(1)

job = jobs[0]
print(f'Job: {job["name"]} - {job["status"]} - {job["conclusion"]}')
print(f'Steps:')
for step in job['steps']:
    print(f"  {step['name']}: {step.get('status')} - {step.get('conclusion')}")
    if step['name'] == 'Deploy to Cloudflare Pages':
        print(f"    Error?: {step.get('conclusion')}")
        
# Try to fetch step logs directly via job logs API
print(f'\nAttempting to fetch raw job logs URL...')
print(f'Logs URL: {job.get("logs_url", "N/A")}')

# Alternative: fetch via API
r = requests.get(job.get('logs_url', ''), headers=headers, allow_redirects=True, timeout=5)
if r.status_code == 200:
    logs = r.text
    # Find Cloudflare-related errors
    for i, line in enumerate(logs.split('\n')):
        if 'cloudflare' in line.lower() or 'error' in line.lower() or 'failed' in line.lower() or '401' in line:
            print(f"Line {i}: {line[:150]}")
else:
    print(f'Could not fetch logs: status {r.status_code}')
