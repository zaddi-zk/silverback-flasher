import requests
owner='kirui58-sy'; repo='silverback-flasher'; run_id='27466520199'
pat='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'
headers={'Authorization':f'token {pat}','Accept':'application/vnd.github+json'}

r=requests.get(f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs', headers=headers)
print('status', r.status_code)
jobs=r.json().get('jobs', [])
for job in jobs:
    print(job['name'], job['id'], job['status'], job['conclusion'])
    for step in job['steps']:
        print('  -', step['name'], step.get('status'), step.get('conclusion'))
